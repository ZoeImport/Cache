# 第3章 分布式训练
# Chapter 3: Distributed Training

> **随着模型规模增长到万亿参数（parameter /pəˈræmɪtər/），单卡训练已不可行。分布式训练通过将计算和内存分摊到多卡，使超大模型训练成为现实。本章介绍 DDP、模型并行 (Tensor（/ˈtensər/）/Pipeline)、FSDP 和 DeepSpeed ZeRO 四大范式。**
> **As models grow to trillions of parameters, single-GPU training is infeasible. Distributed training spreads computation and memory across accelerators. This chapter covers DDP, Model Parallelism (Tensor/Pipeline), FSDP, and DeepSpeed ZeRO.**

**前置:** 训练循环 (Ch2), PyTorch `nn.Module` | **依赖:** `torch>=2.1.0`, `torch.distributed`, `DeepSpeed` (opt)

---

## 1. 分布式训练概览 | Overview

核（kernel /ˈkɜːrnl/）心问题：**如何将大模型的计算和存储分摊到多卡？**

| 范式 | 核心思想 | 单机扩展 | 跨机扩展 |
|---|---|---|---|
| **DDP** | 每卡完整模型，分摊 Batch | ★★★ | ★★★ |
| **模型并行** | 切分模型到多卡 | ★★ | ★★ |
| **FSDP / ZeRO** | 分片优化器/梯度（gradient /ˈɡreɪdiənt/）/参数 | ★★★ | ★★★ |

**选型:** 模型能塞进单卡→DDP；放不下→FSDP/ZeRO；层数极深→Pipeline；单层超大→Tensor。

---

## 2. DDP: 数据分布式并行 | Data Distributed Parallel

### 2.1 原理

DDP (`torch.nn.parallel.DistributedDataParallel`) 是最成熟的分布式训练方法：

1. **每卡一份完整模型副本**，每卡处理不同数据子集
2. 前向+反向各自独立计算梯度
3. 反向时通过 **All-Reduce** 同步平均梯度
4. 每卡用平均梯度独立更新参数 → 所有卡同步

```
GPU 0: [data_0] -> forward -> backward -> grad_0 --\
GPU 1: [data_1] -> forward -> backward -> grad_1 ---> All-Reduce -> avg_grad -> step
GPU N: [data_N] -> forward -> backward -> grad_N --/
```

### 2.2 关键特性

- **通信量:** 每步 2× 参数量 (All-Reduce ping-pong)
- **同步训练:** 每步等待最慢卡
- **全局 Batch:** = per_gpu_batch × num_gpus，需 linear scaling 调整 LR
- **初始化:** `init_process_group(backend="nccl")` + `DistributedSampler`

### 2.3 局限性

DDP 要求**每卡完整容纳模型**，参数超单卡显存时失效。

---

## 3. 模型并行 | Model Parallelism

### 3.1 Tensor Parallel (张量并行)

将**单层权重**沿某个维度切分到多卡：

- **行并行:** 按行切分，每卡算部分 hidden state
- **列并行:** 按列切分，每卡输出部分维度后拼接

```
# 列并行: Linear(4096, 4096) 切到 2 卡
GPU 0: Linear(4096, 2048)  # 前 2048 列
GPU 1: Linear(4096, 2048)  # 后 2048 列
```

每步需 All-Reduce/All-Gather 合并结果，通信量大。适合**单层超大**场景。代表: Megatron-LM。

### 3.2 Pipeline Parallel (流水线并行)

将**不同层**分配到不同 GPU，数据像流水线传递：

```
GPU 0: [layers 0-3] -> GPU 1: [layers 4-7] -> GPU 2: [layers 8-11]
```

**调度:** Naive 利用率低 ❌ → GPipe (micro-batch 填满流水线) → **1F1B** (主流，省显存)。存在**流水线气泡**，层数/微批越多气泡越小。

### 3.3 对比

| 维度 | Tensor Parallel | Pipeline Parallel |
|---|---|---|
| 切分粒度 | 层内 (intra-layer) | 层间 (inter-layer) |
| 通信量 | 大 (每步 All-Reduce) | 小 (仅 activation) |
| 适用 | 单层超大 (>10B) | 层数极深 (>100) |
| 气泡 | 无 | 有 |
| 实现难度 | 高 (需改写模块) | 中 (需调度器) |

---

## 4. FSDP: 全分片数据并行 | Fully Sharded Data Parallel

### 4.1 问题

DDP 每卡完整复制模型 → 显存浪费。FSDP 将优化器状态、梯度、参数**分片**到各 GPU，按需收集。

### 4.2 分片策略

| 策略 | 参数分片 | 梯度分片 | 优化器状态分片 | 显存 (vs DDP) |
|---|---|---|---|---|
| `NO_SHARD` | ✗ | ✗ | ✗ | O(1) |
| `SHARD_GRAD_OP` | ✗ | ✓ | ✓ | ~O(1/N) |
| `FULL_SHARD` (默认) | ✓ | ✓ | ✓ | ~O(1/N) |

### 4.3 流程 (FULL_SHARD)

```
前向: All-Gather 收集参数 → forward → 丢弃非本卡分片
反向: All-Gather 再次收集参数 → backward → Reduce-Scatter 平均并分片梯度
优化: 每卡只更新自己分片
```

**核心:** 参数"按需全量、用完即弃"，**通信换显存**。

### 4.4 通信重叠

支持 All-Gather/Reduce-Scatter 与计算重叠：
- **前向预取:** 当前层计算时提前收集下一层参数
- **反向预取:** 当前层反向时提前收集下一层对应参数

### 4.5 建议

- **<1B:** DDP 即可 (FSDP 通信开销可能超显存节省)
- **1B-7B:** FSDP `FULL_SHARD` 最优
- **>7B:** FSDP + CPU Offload
- **多节点:** 用 `SHARD_GRAD_OP` 减少跨节点通信

---

## 5. DeepSpeed ZeRO

### 5.1 概述

ZeRO (Zero Redundancy Optimizer) 由 Microsoft 提出，与 FSDP 目标一致：**消除数据并行冗余**，工程化更成熟。

### 5.2 三阶段

| 阶段 | 分片内容 | 显存节省 | 通信量 |
|---|---|---|---|
| **ZeRO-1** | 优化器状态 (momentum（/məˈmentəm/）+variance) | 4× | ≈ DDP |
| **ZeRO-2** | + 梯度 (Gradients) | 8× | ≈ DDP |
| **ZeRO-3** | + 参数 (Parameters) | 与 GPU 数成反比 | +1.5× |

**ZeRO-1:** Adam 需存 momentum+variance (~2× 参数量)，分片到各卡。参数和梯度仍全量。

**ZeRO-2:** 梯度通过 Reduce-Scatter 分片，每卡只持部分梯度，省去完整梯度存储。

**ZeRO-3:** 参数按需 All-Gather 收集 (与 FSDP 一致)，通信开销最大但显存最省。

### 5.3 ZeRO vs FSDP

| 维度 | DeepSpeed ZeRO | PyTorch FSDP |
|---|---|---|
| 易用性 | 需插件，配置稍复杂 | 原生 PyTorch |
| 特性 | 更丰富 (offload, 混合引擎等) | 核心功能完整 |
| 生态 | 广泛用于大模型训练 | PyTorch 原生整合好 |

### 5.4 Offload (卸载)

将 optimizer states 甚至参数卸载到 CPU：

```
ZeRO-2 + Offload: optimizer states → CPU, 梯度+参数 → GPU
ZeRO-3 + Offload: optimizer states + 参数 → CPU, 仅梯度 → GPU (临时)
```

可在 24GB 消费级 GPU 上微调 13B 模型 (速度慢但可行)。

---

## 6. 总结与选型建议 | Summary

### 决策树

```
模型能放进单卡? → 是 → DDP
                → 否 → FSDP/ZeRO
                        → 多卡总显存够? → FULL_SHARD / ZeRO-3
                        → 不够? → + CPU Offload
                        → 单层超大? → 结合 Tensor Parallel
```

### 典型配置

| 模型规模 | GPU 数 | 推荐方案 | 全局 Batch Size |
|---|---|---|---|
| <1B | 2-8 | DDP | 64-256 |
| 1B-7B | 8-64 | FSDP / ZeRO-3 | 128-512 |
| 7B-70B | 64-512 | ZeRO-3 + TP + PP | 256-1024 |
| >70B | 512+ | 3D Parallelism | 512-2048 |

### 核心要点

1. **DDP** — 最简单起点，要求模型塞进单卡
2. **FSDP/ZeRO** — 通过分片消除冗余，大模型训练标配
3. **张量并行** — 解决单层过大问题，适合节点内高带宽
4. **流水线并行** — 解决层数过多问题，有气泡开销
5. 现代大模型通常组合多种并行策略 (3D Parallelism)
6. **显存节省 vs 通信开销 vs 易用性** 的三角权衡

---

> **延伸阅读:** [PyTorch DDP](https://pytorch.org/docs/stable/distributed.html) | [FSDP](https://pytorch.org/docs/stable/fsdp.html) | [ZeRO 论文](https://arxiv.org/abs/1910.02054) | [Megatron-LM](https://arxiv.org/abs/1909.08053)
