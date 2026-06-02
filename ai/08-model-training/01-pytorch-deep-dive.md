# 第1章 PyTorch 深度剖析 — 从 Tensor 到编译优化
# Chapter 1: PyTorch Deep Dive — From Tensor to Compiled Optimization

> **PyTorch 是深度学习的事实标准框架。** 理解其底层机制（Tensor（/ˈtensər/） 存储结构、Autograd 计算图、nn.Module 系统）能帮助你写出更高效、更可维护的代码。本章从零开始剖析 PyTorch 的核（kernel /ˈkɜːrnl/）心组件。
>
> **PyTorch is the de-facto standard framework for deep learning.** Understanding its internals — Tensor storage/layout, Autograd computation graph, nn.Module system — helps you write more efficient and maintainable code. This chapter dissects PyTorch's core components from the ground up.

**前置知识 (Prerequisites):** NumPy 基础, 神经网络基本概念
**依赖库 (Dependencies):** `torch >= 2.1.0`, `numpy`, `matplotlib`

---

## 目录 (Table of Contents)

1. [Tensor 底层：Storage & Stride (Tensor Internals)](#1-tensor-底层storage--stride-tensor-internals)
2. [Autograd 引擎：计算图与自动微分 (Autograd Engine)](#2-autograd-引擎计算图与自动微分-autograd-engine)
3. [nn.Module 系统：构建可复用的网络 (The Module System)](#3-nnmodule-系统构建可复用的网络-the-module-system)
4. [数据加载：Dataset & DataLoader (Data Loading)](#4-数据加载dataset--dataloader-data-loading)
5. [torch.compile：即时编译优化 (JIT Compilation)](#5-torchcompile即时编译优化-jit-compilation)

---

## 1. Tensor 底层：Storage & Stride (Tensor Internals)

### 1.1 Storage：原始一维数据数组 (The Raw Data Array)

PyTorch 的 Tensor 实际上是**一个指向 Storage 对象的视图 (view)**。Storage 是一块连续的一维内存区域，存储着实际的数值数据。

```python
import torch

t = torch.tensor([[1, 2, 3], [4, 5, 6]])
print(t)
print(f"storage: {t.storage()}")
print(f"storage offset: {t.storage_offset()}")
```

输出:

```
tensor([[1, 2, 3],
        [4, 5, 6]])
storage:  1
 2
 3
 4
 5
 6
[torch.LongStorage of size 6]
storage offset: 0
```

**关键洞察 (Key Insight):** Tensor 本身只存储三个元数据——`storage` 引用、`shape`、`stride`。所有数据都在 Storage 中。这意味着创建不同的 Tensor "视图"（view）不会复制数据，只需修改 shape 和 stride。

### 1.2 Stride：如何从逻辑索引映射到物理位置 (The Index Mapping)

**Stride** 定义了在每个维度上移动一步需要跳过多少个元素。

$$ \text{offset} = \text{storage\_offset} + \sum_{d=0}^{n-1} \text{index}[d] \times \text{stride}[d] $$

```python
t = torch.tensor([[1, 2, 3], [4, 5, 6]])
print(f"shape: {t.shape}, stride: {t.stride()}")
# shape: (2, 3), stride: (3, 1)
# t[1, 2] 的存储位置 = 0 + 1*3 + 2*1 = 5 → storage[5] = 6
```

**物理含义:** `stride[0] = 3` 表示从第 0 行到第 1 行要跳过 3 个元素（整行的宽度）；`stride[1] = 1` 表示在同一行中相邻列是连续存储的。

### 1.3 转置不会复制数据 (Transpose Without Copy)

```python
t = torch.tensor([[1, 2, 3], [4, 5, 6]])
t_t = t.T  # 转置

print(f"t_t shape: {t_t.shape}, stride: {t_t.stride()}")
# t_t shape: (3, 2), stride: (1, 3)
# 注意 stride 交换了！存储没有变化
print(f"t_t storage: {t_t.storage()}")  # 和 t 共享同一个 storage
print(f"storage id same: {t.storage().data_ptr() == t_t.storage().data_ptr()}")
# True — 零拷贝
```

**输出:**

```
t_t shape: (3, 2), stride: (1, 3)
t_t storage:  1
 2
 3
 4
 5
 6
storage id same: True
```

**直觉:** 转置只是交换了 `shape` 和 `stride` 的维度顺序，物理数据纹丝不动。这也解释了为什么转置后的张量不连续（`t_t.is_contiguous() → False`），因为元素在物理上不是按行排列的。

### 1.4 contiguous() 与 clone() 的区别

- **`contiguous()`:** 返回一个新的 Tensor，其 Storage 中的数据按行优先重新排列（保持逻辑内容不变）。
- **`clone()`:** 复制一个新的 Tensor（含新的 Storage），两者完全独立。

```python
t = torch.tensor([[1, 2, 3], [4, 5, 6]])
t_t = t.T
t_c = t_t.contiguous()
print(f"t_t is_contiguous: {t_t.is_contiguous()}")  # False
print(f"t_c is_contiguous: {t_c.is_contiguous()}")  # True
print(f"t_c storage: {t_c.storage()}")
# t_c storage:  1  4  2  5  3  6  — 转置后行优先排列
```

### 1.5 内存布局对性能的影响 (Performance Impact)

当我们遍历 Tensor 时，**按存储顺序访问速度更快**，因为 CPU 缓存利用率更高（空间局部性）。

```python
n = 4096
x = torch.randn(n, n)

# 按行优先访问（快速）
def row_first():
    s = 0
    for i in range(n):
        for j in range(n):
            s += x[i, j].item()
    return s

# 按列优先访问（慢速—缓存不命中）
def col_first():
    s = 0
    for i in range(n):
        for j in range(n):
            s += x[j, i].item()  # 跨步访问
    return s
```

**经验法则:** 始终按连续维度的顺序循环。对于行优先存储的 Tensor，外层循环行、内层循环列。

---

## 2. Autograd 引擎：计算图与自动微分 (Autograd Engine)

### 2.1 计算图 (Computation Graph)

PyTorch 的 Autograd 通过构建**有向无环图 (DAG)** 来跟踪运算历史：

- **节点 (Node):** 张量 (Tensor) 或运算函数 (Function)
- **边 (Edge):** 数据流向

```
        ┌───┐     ┌───┐
        │ x │     │ y │     ← 叶子节点 (leaf nodes)
        └─┬─┘     └─┬─┘
          │         │
          └────┬────┘
               │  +
               ▼
          ┌────────┐
          │   z    │         ← 中间节点
          └───┬────┘
              │  * 2
              ▼
          ┌────────┐
          │   f    │         ← 输出
          └────────┘
```

**前向 (Forward):** 从叶子节点到输出节点，计算并记录每个运算。
**反向 (Backward):** 从输出节点到叶子节点，应用链式法则计算梯度（gradient /ˈɡreɪdiənt/）。

### 2.2 链式法则 (Chain Rule)

对于 $f = 2 \times (x + y)$:

$$ \frac{\partial f}{\partial x} = \frac{\partial f}{\partial z} \cdot \frac{\partial z}{\partial x} = 2 \times 1 = 2 $$

$$ \frac{\partial f}{\partial y} = \frac{\partial f}{\partial z} \cdot \frac{\partial z}{\partial y} = 2 \times 1 = 2 $$

### 2.3 梯度累积 (Gradient Accumulation)

每次调用 `backward()`，梯度会 **累加** 到 `.grad` 属性中，而不是覆盖。

```python
x = torch.tensor([1.0], requires_grad=True)
w = torch.tensor([2.0], requires_grad=True)

y = x * w
y.backward()
print(f"After 1st backward: x.grad={x.grad}, w.grad={w.grad}")
# After 1st backward: x.grad=tensor([2.]), w.grad=tensor([1.])

y = x * w  # 新的前向
y.backward()
print(f"After 2nd backward: x.grad={x.grad}, w.grad={w.grad}")
# After 2nd backward: x.grad=tensor([4.]), w.grad=tensor([2.])
# ∇ 梯度累加了！
```

**这就是为什么每个训练迭代都要调用 `optimizer.zero_grad()`**——清空累积的梯度，否则梯度会不断叠加。

### 2.4 计算图可视化 (在配套代码中实现)

配套代码 `pytorch_deep_dive.py` 实现了一个**从零开始的微型 Autograd 引擎**（`Scalar` 类），并打印以下内容：

1. 计算图的结构（所有节点的连接关系）
2. 前向传播的输出值
3. 手动链式法则计算的梯度值
4. PyTorch Autograd 计算的梯度值
5. 手动梯度与 Autograd 梯度的对比验证

```python
# 在配套代码中 (from code/pytorch_deep_dive.py):
# Manually:
#   f = w * x + b
#   df/dw = x = 0.5, df/dx = w = 2.0, df/db = 1.0
#
# PyTorch:
#   f.backward()
#   w.grad = tensor([0.5000]), x.grad = tensor([2.0000]), b.grad = tensor([1.])
```

### 2.5 禁用梯度追踪 (Disabling Gradient Tracking)

```python
# 方法 1: torch.no_grad() — 推理时使用
with torch.no_grad():
    y_pred = model(x)  # 不构建计算图

# 方法 2: requires_grad_(False) — 冻结参数
for param in model.parameters():
    param.requires_grad_(False)

# 方法 3: detach() — 从计算图中分离
y = x * w
z = y.detach()  # z 不追踪梯度
print(z.requires_grad)  # False
```

---

## 3. nn.Module 系统：构建可复用的网络 (The Module System)

### 3.1 核心机制 (Core Mechanism)

`nn.Module` 的核心是**参数（parameter /pəˈræmɪtər/）注册 (parameter registration)** 和**模块注册 (module registration)**：

- `register_parameter(name, param)`: 将 `nn.Parameter` 注册为该模块的参数
- `register_module(name, module)`: 将子模块注册（通过 `__setattr__` 自动调用）

```python
import torch.nn as nn

class MyLinear(nn.Module):
    def __init__(self, in_features, out_features):
        super().__init__()
        # 显式注册参数
        self.weight = nn.Parameter(torch.randn(out_features, in_features))
        self.bias = nn.Parameter(torch.zeros(out_features))

    def forward(self, x):
        return x @ self.weight.T + self.bias

# 实际上 nn.Linear 内部实现与此类似
```

**为什么需要注册?** 因为 `model.parameters()`, `model.state_dict()`, `model.to(device)` 等方法都依赖注册机制来递归收集所有参数。

```python
layer = MyLinear(4, 3)
print(list(layer.parameters()))
# 包含 weight 和 bias

# 未注册的普通属性不会被收集
class BadLinear(nn.Module):
    def __init__(self, in_f, out_f):
        super().__init__()
        self.W = torch.randn(out_f, in_f)  # 普通 Tensor，不是 Parameter！
```

### 3.2 Sequential, ModuleList, ModuleDict

| 容器 | 说明 | 适用场景 |
|------|------|----------|
| `nn.Sequential` | 按顺序执行模块 | 线性堆叠的网络 |
| `nn.ModuleList` | 存储模块列表 | 循环中需要索引的模块群 |
| `nn.ModuleDict` | 按名称存储模块 | 需要按名称选择模块 |

```python
# Sequential — 简单的层叠
model = nn.Sequential(
    nn.Linear(784, 256),
    nn.ReLU(),
    nn.Linear(256, 10),
)

# ModuleList — 可索引的模块组
class MyResNet(nn.Module):
    def __init__(self):
        super().__init__()
        self.layers = nn.ModuleList([
            nn.Linear(64, 64) for _ in range(5)
        ])

    def forward(self, x):
        for layer in self.layers:
            x = layer(x) + x  # 残差连接
        return x

# ModuleDict — 按名称选择
class SwitchableNet(nn.Module):
    def __init__(self):
        super().__init__()
        self.activations = nn.ModuleDict({
            'relu': nn.ReLU(),
            'tanh': nn.Tanh(),
            'sigmoid': nn.Sigmoid(),
        })

    def forward(self, x, activation='relu'):
        return self.activations[activation](x)
```

### 3.3 forward 钩子 (Hooks)

Hooks 允许你在不修改 `forward` 方法的情况下插入额外逻辑：

```python
layer = nn.Linear(4, 2)

# 前向钩子：在 forward 执行前调用
def pre_hook(module, input):
    print(f"[pre_hook] input shape: {input[0].shape}")

# 后向钩子：在 forward 执行后调用
def post_hook(module, input, output):
    print(f"[post_hook] output shape: {output.shape}")

handle1 = layer.register_forward_pre_hook(pre_hook)
handle2 = layer.register_forward_hook(post_hook)

x = torch.randn(2, 4)
y = layer(x)
# [pre_hook] input shape: torch.Size([2, 4])
# [post_hook] output shape: torch.Size([2, 2])

# 用完移除
handle1.remove()
handle2.remove()
```

### 3.4 自定义 Autoencoder 示例

```python
class Autoencoder(nn.Module):
    def __init__(self, dims=[784, 256, 64, 256, 784]):
        super().__init__()
        layers = []
        for i in range(len(dims) - 1):
            layers.append(nn.Linear(dims[i], dims[i+1]))
            if i < len(dims) // 2:  # 编码器部分
                layers.append(nn.ReLU())
            else:                     # 解码器部分
                layers.append(nn.Sigmoid())
        self.net = nn.Sequential(*layers)

    def forward(self, x):
        return self.net(x)
```

---

## 4. 数据加载：Dataset & DataLoader (Data Loading)

### 4.1 Dataset：数据集的抽象接口

所有数据集必须实现两个方法：

```python
from torch.utils.data import Dataset

class MyDataset(Dataset):
    def __init__(self, data, targets):
        self.data = data
        self.targets = targets

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        return self.data[idx], self.targets[idx]
```

**为什么需要 Dataset 抽象?** 它将"数据在哪里/如何存储"与"如何使用数据"解耦。无论数据在内存、磁盘、数据库还是云端，Dataset 接口都一致。

### 4.2 DataLoader：批量加载与多进程

```python
from torch.utils.data import DataLoader

dataset = MyDataset(...)
loader = DataLoader(
    dataset,
    batch_size=32,
    shuffle=True,       # 每个 epoch 打乱数据
    num_workers=4,       # 4 个子进程预加载数据
    pin_memory=True,     # 使用锁页内存加速 GPU 传输
    drop_last=True,      # 丢弃最后一个不完整的 batch
)
```

**DataLoader 内部流程:**

```
Dataset (原始数据)
    │
    ▼
Sampler (采样策略)
    │  SequentialSampler: 顺序采样
    │  RandomSampler: 随机采样
    │  WeightedRandomSampler: 加权采样
    │  SubsetRandomSampler: 子集采样
    ▼
BatchSampler (批次组装)
    │  将 index 分组为 batch
    ▼
DataLoader (collate_fn)
    │  将样本列表组装为 batch tensor
    ▼
Training Loop
```

### 4.3 Sampler：控制数据采样策略

```python
from torch.utils.data import Sampler, SequentialSampler, RandomSampler, WeightedRandomSampler

# 自定义 Sampler — 按特定顺序取数据
class OrderedSampler(Sampler):
    def __init__(self, data_source, order):
        self.data_source = data_source
        self.order = order

    def __iter__(self):
        return iter(self.order)

    def __len__(self):
        return len(self.order)

# 加权采样 — 处理类别不均衡
weights = torch.tensor([1.0, 10.0, 1.0])  # 类别 1 被过度采样
sampler = WeightedRandomSampler(weights, num_samples=100, replacement=True)
```

### 4.4 自定义 collate_fn

当样本结构不是简单的 (data, label) 时，需要自定义 `collate_fn`：

```python
def collate_fn(batch):
    # batch = [(img1, label1, path1), (img2, label2, path2), ...]
    images = torch.stack([item[0] for item in batch])
    labels = torch.tensor([item[1] for item in batch])
    paths = [item[2] for item in batch]
    return images, labels, paths

loader = DataLoader(dataset, batch_size=32, collate_fn=collate_fn)
```

---

## 5. torch.compile：即时编译优化 (JIT Compilation)

### 5.1 什么是 torch.compile? (What is it?)

PyTorch 2.0 引入的 `torch.compile` 是一种**即时 (JIT) 编译器**，它将 PyTorch 代码动态编译为高效的 GPU 内核：

```
Python 代码
    │
    ▼
TorchDynamo (捕获 FX Graph)
    │  拦截 Python 字节码，提取计算图
    ▼
FX Graph (中间表示)
    │
    ▼
后端编译器 (如 Inductor/AOTAutograd)
    │  图优化、内核融合、代码生成
    ▼
Triton / CUDA 内核
```

### 5.2 用法 (Usage)

```python
import torch

model = MyModel()
model = torch.compile(model)  # 一行代码加速

# 或者
model = torch.compile(model, mode="reduce-overhead")
```

**mode 参数:**

| mode | 说明 | 适用场景 |
|------|------|----------|
| `"default"` | 平衡编译时间和运行时性能 | 通用 |
| `"reduce-overhead"` | 减少小 batch 的启动开销 | 小模型/小 batch |
| `"max-autotune"` | 花费更多时间寻找最优内核 | 生产环境频繁调用 |
| `"max-autotune-no-cudagraphs"` | 同上但不使用 CUDA graphs | 有动态图形 |

### 5.3 编译效果 (Expected Speedup)

对于典型的 Transformer（/trænsˈfɔːrmər/） 模型，`torch.compile` 通常能带来 **~20% 的端到端加速**，在某些计算密集操作上可达 **2-5 倍**。

```python
# 典型加速效果：
# 未编译: 100ms / 步
# 编译后:  80ms / 步  ← ~20% 加速
# （第一次调用较慢，因为需要编译预热）
```

### 5.4 何时使用? (When to Use?)

**适用:**
- 训练循环（特别是大模型）
- 计算密集的操作（矩阵乘法、卷积（convolution /ˌkɒnvəˈluːʃən/））
- 生产环境推理（inference /ˈɪnfərəns/）（预热后）

**不适用:**
- 一次性小计算（编译开销超过收益）
- 极度动态的控制流（条件分支多）
- 已有高度优化 CUDA 内核的自定义操作

### 5.5 调试与回溯 (Debugging & Fallback)

```python
# 查看编译效果
print(model._torchdynamo_compiled)

# 如果编译失败，自动回退到 eager 模式
# 可以设置环境变量查看详细信息
# TORCH_COMPILE_DEBUG=1 python train.py
```

---

## 总结 (Summary)

| 概念 | 核心要点 | 一句话总结 |
|------|----------|-----------|
| **Storage** | 连续一维数据数组 | Tensor 的本质是 Storage 的视图 |
| **Stride** | 维度到物理地址的映射 | 转置/切片不复制数据 |
| **Autograd** | 前向构建 DAG，反向传播（backpropagation /ˌbækprəpəˈɡeɪʃən/）梯度 | `backward()` 累加梯度需 `zero_grad()` |
| **nn.Module** | 参数注册与递归管理 | 自定义层需继承 `nn.Module` |
| **Dataset/DataLoader** | 数据抽象 + 批量加载 | Sampler 控制采样策略 |
| **torch.compile** | JIT 编译 + 内核融合 | 一行代码 ~20% 加速 |

## 配套代码 (Accompanying Code)

运行 `code/pytorch_deep_dive.py` 查看:

1. **微型 Autograd 引擎** — 从零实现的 `Scalar` 类展示了计算图的本质
2. **手动梯度计算** — 用链式法则逐层验证
3. **PyTorch Autograd 对比** — 手动结果与自动微分的精确匹配
4. **计算图可视化** — 打印完整的图结构

```bash
python ai/08-model-training/code/pytorch_deep_dive.py
```
