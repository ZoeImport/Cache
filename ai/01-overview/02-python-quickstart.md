# Python 快速入门 (Python Quickstart)

> 面向机器学习的 Python 最小必要知识子集。覆盖 20% 的语法，应对 80% 的 ML 日常编码。
> The minimal Python subset for ML. Covers 20% of the syntax for 80% of daily ML coding.

---

## 环境搭建 (Environment Setup)

### 三种选择

| 工具 (Tool) | 适用场景 | 推荐度 |
|-------------|----------|--------|
| **conda** | 数据科学全家桶，跨 Python 版本管理 | ⭐⭐⭐ |
| **venv** | Python 标准库自带，轻量 | ⭐⭐ |
| **uv** | 极速包管理器，Rust 编写，现代替代 | ⭐⭐⭐⭐⭐ |

> 本书建议使用 **uv**。安装: `curl -LsSf https://astral.sh/uv/install.sh | sh`

### 安装依赖

```bash
# conda
conda create -n ai-env python=3.11
conda activate ai-env
pip install -r ai/requirements.txt

# uv (推荐 / recommended)
uv venv --python 3.11
source .venv/bin/activate
uv pip install -r ai/requirements.txt
```

---

## 核心语法速成 (Core Syntax Crash Course)

### 1. 数据类型 (Data Types)

Python 是动态类型语言 (dynamically typed)，变量无需声明类型。

```python
# 基本类型
x = 42           # int — 整数
y = 3.14159      # float — 浮点数
z = "hello"      # str — 字符串
flag = True      # bool — 布尔值
nothing = None   # NoneType — 空值

# 类型检查 / 转换
type(x)          # <class 'int'>
isinstance(x, int)  # True
float(x)         # 42.0
int("42")        # 42
```

#### 容器类型 (Container Types)

```python
# 列表 (list) — 可变，有序
lst = [1, 2, 3, 2]
lst.append(4)        # [1, 2, 3, 2, 4]
lst[0]               # 1 (索引从0开始)
lst[-1]              # 4 (负索引从末尾开始)

# 元组 (tuple) — 不可变，有序
tup = (1, 2, 3)
# tup[0] = 99  ← 报错! 元组不可修改

# 字典 (dict) — 键值对
d = {"name": "Alice", "age": 25}
d["name"]            # "Alice"
d.get("score", 0)    # 0 (带默认值)

# 集合 (set) — 无序，不重复
s = {1, 2, 3, 2}     # {1, 2, 3}
s.add(4)
```

**ML 场景常见的用法**:
- `list`: 数据集、批次 (batches)、训练循环中的索引
- `dict`: 模型参数（parameter /pəˈræmɪtər/）字典 `model.state_dict()`、超参数（hyperparameter /ˈhaɪpərpəˈræmɪtər/）配置 `config`
- `tuple`: 图像尺寸 `(H, W, C)`、批次形状 `(batch, seq_len)`
- `set`: 标签去重、类别集合

### 2. 控制流 (Control Flow)

```python
# if / elif / else
score = 85
if score >= 90:
    grade = "A"
elif score >= 80:
    grade = "B"
else:
    grade = "C"

# for 循环 — 遍历可迭代对象
for i in range(5):       # 0, 1, 2, 3, 4
    print(i)

for idx, val in enumerate(lst):
    print(idx, val)

for key, val in d.items():
    print(key, val)

# while 循环
epoch = 0
while epoch < 10:
    epoch += 1

# 列表推导式 (List Comprehension) — ML 代码中极常见
squares = [x**2 for x in range(10)]          # [0, 1, 4, ..., 81]
evens   = [x for x in range(20) if x % 2 == 0]

# 字典推导式
square_dict = {x: x**2 for x in range(5)}    # {0: 0, 1: 1, 2: 4, 3: 9, 4: 16}
```

> **列表推导式是 ML 代码中最常用的 Python 特性之一**，用于批量数据转换、过滤、预处理。

### 3. 函数 (Functions)

```python
# 基本函数定义
def mean(values):
    """计算平均值 (Compute the mean)."""
    return sum(values) / len(values)

# 默认参数
def normalize(x, eps=1e-8):
    return x / (max(x) + eps)

# *args / **kwargs — 可变参数
def concat(*args):
    return " ".join(args)

def print_config(**kwargs):
    for k, v in kwargs.items():
        print(f"{k}: {v}")

concat("a", "b", "c")        # "a b c"
print_config(lr=0.001, epochs=10)

# Lambda 匿名函数
square = lambda x: x ** 2
list(map(lambda x: x * 2, [1, 2, 3]))   # [2, 4, 6]

# 类型提示 (Type Hints) — Python 3.5+
def add(a: int, b: int) -> int:
    return a + b
```

#### 函数式编程在 ML 中的应用

```python
# map / filter 配合 lambda
data = [1.5, -2.3, 3.7, -0.5]
abs_data = list(map(abs, data))
positive = list(filter(lambda x: x > 0, data))

# sorted 自定义键
pairs = [(3, "a"), (1, "c"), (2, "b")]
sorted(pairs, key=lambda x: x[0])   # [(1, 'c'), (2, 'b'), (3, 'a')]
```

### 4. 上下文管理器 (Context Managers) — `with` 语句

`with` 语句自动管理资源的获取和释放，最常见于文件 I/O 和 PyTorch 的梯度（gradient /ˈɡreɪdiənt/）管理。

```python
# 文件 I/O (核心场景)
with open("data.txt", "r") as f:
    content = f.read()
# 文件自动关闭，无需显式 f.close()

# PyTorch 中的 with 用法 (后续章节详解)
with torch.no_grad():
    predictions = model(x)
# 推理时不计算梯度，节省显存和计算
```

### 5. 错误处理 (Error Handling)

```python
try:
    result = 1 / 0
except ZeroDivisionError as e:
    print(f"除零错误: {e}")
except Exception as e:
    print(f"其他错误: {e}")
finally:
    print("无论是否异常，总会执行")

# ML 中常见的错误处理场景:
# - 加载模型权重时版本不匹配
# - 数据加载时文件缺失
# - 超参数配置类型错误
```

### 6. 面向对象速览 (OOP Overview)

ML 中 OOP 的核（kernel /ˈkɜːrnl/）心用途:
- **封装模型结构**: `nn.Module` 子类
- **封装数据集**: `Dataset` 子类
- **封装训练逻辑**: 训练器类

```python
class Layer:
    """一个简单的线性层 (A simple linear layer)."""
    def __init__(self, in_features: int, out_features: int):
        # __init__: 构造函数，初始化参数
        self.weight = [[0.0] * out_features for _ in range(in_features)]
        self.bias = [0.0] * out_features

    def forward(self, x):
        """前向传播 (Forward pass)."""
        # self: 实例方法第一个参数，指向对象自身
        return [self._compute(x_i) for x_i in x]

    def _compute(self, x_i):
        """私有方法 (由前导下划线标识)."""
        return sum(w * x_i for w in self.weight) + self.bias

# 继承 (Inheritance)
class MyLinear(Layer):
    """继承 Layer，添加新功能. (Inherits Layer, adds new functionality.)"""
    def __init__(self, in_f, out_f, bias=True):
        super().__init__(in_f, out_f)  # 调用父类构造函数
        self.use_bias = bias

    def forward(self, x):
        # 方法重写 (Override)
        return super().forward(x)
```

> **PyTorch 的 `nn.Module`** 大量使用 OOP 模式。理解 `class`、`__init__`、`self`、`super()` 和继承，是阅读和编写 PyTorch 代码的基础。
> PyTorch's `nn.Module` uses OOP heavily. Understanding `class`, `__init__`, `self`, `super()`, and inheritance is essential for reading and writing PyTorch code.

---

## ML 日常高频 Python 用法 (Daily ML Python Patterns)

### NumPy 风格切片

```python
arr = [10, 20, 30, 40, 50]
arr[1:4]        # [20, 30, 40]  — 左闭右开
arr[:3]         # [10, 20, 30]  — 从头开始
arr[::2]        # [10, 30, 50]  — 步长为2
arr[::-1]       # [50, 40, 30, 20, 10] — 反转
```

### enumerate / zip

```python
# 同时遍历索引和值
for i, x in enumerate([10, 20, 30]):
    print(i, x)

# 同时遍历多个序列
for x, y in zip([1, 2, 3], [4, 5, 6]):
    print(x + y)  # 5, 7, 9
```

### 三元表达式

```python
x = 10
label = "positive" if x > 0 else "negative"
# 等价于:
# if x > 0: label = "positive"
# else: label = "negative"
```

### f-string 格式化

```python
name, acc = "ResNet", 0.9523
print(f"Model: {name}, Accuracy: {acc:.2%}")
# Model: ResNet, Accuracy: 95.23%
```

---

## 下一步 (Next Steps)

- 从 `code/python_quickstart.py` 运行本章配套代码
- 阅读下一章: [03-python-data-science.md](03-python-data-science.md) (NumPy / Pandas 速成)
- 或在 Python 交互环境中自己动手试每个例子
