# 第4章 数据管道 — 加载、增强与流式处理
# Chapter 4: Data Pipeline — Loading, Augmentation & Streaming

> **数据管道是深度学习训练的生命线。** GPU 算力再强，如果数据加载跟不上，训练就会卡在 I/O 瓶颈上。本章覆盖 DataLoader 调优、流式加载、数据增强策略和 HuggingFace Datasets 的最佳实践。
>
> **The data pipeline is the lifeline of deep learning training.** No matter how powerful your GPU, if data loading cannot keep up, training stalls on I/O bottlenecks. This chapter covers DataLoader tuning, streaming loading, data augmentation strategies, and HuggingFace Datasets best practices.

**前置知识 (Prerequisites):** PyTorch Dataset/DataLoader 基本使用, torchvision 基础
**核（kernel /ˈkɜːrnl/）心概念 (Key Concepts):** 数据加载, 数据增强, 流式处理, 内存效率

---

## 1. DataLoader 调优 (DataLoader Tuning)

### 1.1 核心参数详解 (Core Parameters)

PyTorch DataLoader 的配置直接影响训练吞吐量。最关键的三个参数（parameter /pəˈræmɪtər/）：

| 参数 | 作用 | 推荐值 |
|------|------|--------|
| `num_workers` | 子进程数，并行加载数据 | GPU: CPU 核心数 (通常 4–8) |
| `prefetch_factor` | 每个 worker 预取批次数 | `2` (默认) → `4` 或 `8` 可压榨 IO |
| `pin_memory` | 锁定页内存 → 加速 CPU→GPU 传输 | `True` (GPU 训练必备) |

**配置策略：**

```python
# 典型配置 — 中等规模 (ResNet, ViT 等)
DataLoader(dataset, batch_size=128, num_workers=8,
           prefetch_factor=4, pin_memory=True)

# 高 IO 场景 — 大图像 / 视频
DataLoader(dataset, batch_size=32, num_workers=16,
           prefetch_factor=8, pin_memory=True,
           persistent_workers=True)  # worker 复用以减少创建开销
```

### 1.2 瓶颈识别 (Bottleneck Identification)

判断数据加载是否为瓶颈：

| 指标 | 健康值 | 警告线 |
|------|--------|--------|
| GPU 利用率 | > 90% | < 70% |
| CPU→GPU 传输 % | < 5% 总步时 | > 15% |
| `num_workers` 空闲 | 少量 | 大量 |

> **经验法则：** `num_workers` 通常设为 CPU 核心数。当 `prefetch_factor` 增加到 `8` 以上收益递减时，说明 I/O 已达上限。

---

## 2. 流式加载 (Streaming Loading)

### 2.1 何时需要流式 (When Streaming Matters)

传统随机（stochastic /stəˈkæstɪk/）访问要求所有数据在本地可用。当以下场景出现时，流式加载是更好的选择：

- **超大规模数据集** (TB 级，无法全部载入内存)
- **远程存储训练** (数据在 S3 / GCS 等云存储上)
- **快速实验迭代** (无需等待完整下载)

### 2.2 WebDataset：基于 TAR 分片的流式方案 (TAR Shard Streaming)

WebDataset 将数据集打包为 TAR 分片，每个分片包含数百到数千个样本，实现 **O(1) 随机访问** 和 **顺序流式加载** 的统一。

```
dataset/
├── shard-000000.tar   # 1000 个样本
├── shard-000001.tar   # 1000 个样本
├── shard-000002.tar   # 1000 个样本
└── ...
```

```python
import webdataset as wds

dataset = (
    wds.WebDataset("dataset/shard-{000000..000999}.tar")
    .decode("pil")
    .to_tuple("jpg;png", "json")
    .map(preprocess)
    .batched(64)
)
```

**流式 vs 随机访问：**

| 特性 | 随机访问 (传统) | 流式 (WebDataset) |
|------|----------------|-------------------|
| 内存需求 | O(数据集大小) | O(分片大小) |
| 启动时间 | 完整下载 | 秒级 |
| 混洗精度 | 全局混洗 | 分片级混洗 (需跨分片 buffer) |
| 适用场景 | 小/中等数据集 | 超大数据集 / 远程训练 |

### 2.3 内存效率对比 (Memory Efficiency Comparison)

| 方法 | 内存峰值 | 吞吐量 | 适用规模 |
|------|---------|--------|---------|
| 全量载入 | 最高 | 最快 | 可放入内存 (< 10 GB) |
| 按需读取 | 中等 | 较慢 | ≤ 几百 GB |
| WebDataset 流式 | 最低 | 接近全量 | TB 级 |

---

## 3. 数据增强 (Data Augmentation)

### 3.1 主流工具对比 (Tool Comparison)

| 工具 | 速度 | 复杂度 | 适用场景 |
|------|------|--------|---------|
| `torchvision.transforms` | 快 | 低 | 标准分类（classification /ˌklæsɪfɪˈkeɪʃən/）任务 |
| `albumentations` | 极快 | 中 | 检测/分割/定位 |
| `kornia` | GPU 加速 | 高 | 需要可微分增强 |

### 3.2 弱增强 vs 强增强 (Weak vs Strong Augmentation)

| 类型 | 目的 | 典型操作 | 适用阶段 |
|------|------|---------|---------|
| **弱增强** | 基础泛化，不改变语义 | `RandomCrop`, `HorizontalFlip`, `ColorJitter (轻度)` | 所有任务 |
| **强增强** | 掩膜不变性，正则化（regularization /ˌreɡjələraɪˈzeɪʃən/） | `RandAugment`, `Cutout`, `MixUp`, `CutMix` | 预训练 / 大模型 |

**最佳实践栈 (Best Practice Stack)：**

```
# 弱增强基线
Weak: RandomResizedCrop → RandomHorizontalFlip → ColorJitter → Normalize

# 强增强 (用于 ViT/CLIP 等)
Strong: RandomResizedCrop → RandAugment → RandomErasing → MixUp → CutMix
```

> **注意：** 强增强会增加训练时间 10–30%，需配合 DataLoader 调优抵消开销。`albumentations` 比 `torchvision` 快 2–4 倍，推荐在检测/分割任务中使用。

---

## 4. HuggingFace Datasets (HF Datasets)

### 4.1 核心优势 (Core Advantages)

HuggingFace Datasets 通过 **Arrow 内存格式** 实现零拷贝读取，无需将整个数据集加载到 Python 内存中。

```python
from datasets import load_dataset

# 流式模式 — 数据不下载到本地
dataset = load_dataset("imagenet-1k", split="train", streaming=True)

# 内存效率：Arrow 零拷贝
print(dataset[0])  # O(1) 访问，无需全量载入
```

### 4.2 Map vs Iterable 数据集 (Comparison)

| 特性 | `Dataset` (Map) | `IterableDataset` |
|------|----------------|-------------------|
| 随机访问 | ✅ `dataset[i]` | ❌ 只能顺序迭代 |
| 混洗 | ✅ 内置 shuffle | ⚠️ 需 `shuffle_buffer` |
| 流式 | ❌ 全部下载 | ✅ 按需生成 |
| 适用场景 | 中小规模 | 超大规模 / 远程 |

### 4.3 选择策略 (Selection Strategy)

```
数据集 < 10 GB → Map Dataset (随机访问灵活)
数据集 10 GB ~ 1 TB → IterableDataset + shuffle_buffer=1000
数据集 > 1 TB → WebDataset TAR shards (分片级控制更细)
```

> **性能提示：** 使用 `datasets.set_caching_enabled(False)` 可避免 HF Datasets 的磁盘缓存开销，在流式场景下尤其有用。

---

## 总结 (Summary)

| 层级 | 关键点 | 一句话建议 |
|------|--------|-----------|
| DataLoader | `num_workers`, `pin_memory`, `prefetch_factor` | GPU 利用率 < 90% 时优先调参 |
| WebDataset | TAR 分片流式，O(1) 随机访问 | TB 级数据集默认选择 |
| 数据增强 | `albumentations` 快，`torchvision` 易用 | 大模型用强增强 + RandAugment |
| HF Datasets | Arrow 零拷贝，Map vs Iterable | 流式任务用 `IterableDataset` + `shuffle_buffer` |
