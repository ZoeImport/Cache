"""
NumPy 基础演示（NumPy Basics Demo）
===================================
依赖：numpy>=1.24.0

展示 ndarray 创建、shape/reshape/axis、广播机制，以及向量化 vs Python 循环的性能对比。
"""

import numpy as np
import time


# ============================================================
# 1. ndarray 创建
# ============================================================
print("=" * 60)
print("1. ndarray 创建（Array Creation）")
print("=" * 60)

# 从列表创建
a = np.array([1, 2, 3])
print(f"np.array([1,2,3])  ->  {a},  shape: {a.shape}")

b = np.array([[1, 2], [3, 4]])
print(f"np.array([[1,2],[3,4]])  ->  shape: {b.shape}\n{b}")

# 特殊数组
zeros = np.zeros((2, 3))
print(f"\nnp.zeros((2,3)):\n{zeros}")

ones = np.ones((2, 3))
print(f"\nnp.ones((2,3)):\n{ones}")

eye = np.eye(3)
print(f"\nnp.eye(3):\n{eye}")

# 序列
arange = np.arange(0, 10, 2)
print(f"\nnp.arange(0, 10, 2)  ->  {arange}")

linspace = np.linspace(0, 1, 5)
print(f"np.linspace(0, 1, 5)  ->  {linspace}")

# 随机数
rand = np.random.rand(2, 3)
print(f"\nnp.random.rand(2,3):\n{rand}")

randint = np.random.randint(0, 10, size=(2, 4))
print(f"\nnp.random.randint(0, 10, (2,4)):\n{randint}")


# ============================================================
# 2. Shape, Reshape, Axis
# ============================================================
print("\n" + "=" * 60)
print("2. Shape, Reshape, Axis")
print("=" * 60)

arr = np.arange(12)
print(f"原始（Original）: {arr}, shape: {arr.shape}")

arr_2d = arr.reshape(3, 4)
print(f"\nreshape(3, 4):\n{arr_2d}")
print(f"shape: {arr_2d.shape}")

arr_3d = arr.reshape(2, 3, 2)
print(f"\nreshape(2, 3, 2):\n{arr_3d}")
print(f"shape: {arr_3d.shape}")

# axis 演示
print(f"\naxis=0 求和（Sum along axis=0）: {arr_2d.sum(axis=0)}")
print(f"axis=1 求和（Sum along axis=1）: {arr_2d.sum(axis=1)}")

# 在二维数组中，flatten 与 ravel 将数组展平为一维
print(f"\nflatten()  ->  {arr_2d.flatten()}")
print(f"ravel()    ->  {arr_2d.ravel()}")


# ============================================================
# 3. 广播机制（Broadcasting）
# ============================================================
print("\n" + "=" * 60)
print("3. 广播机制（Broadcasting）")
print("=" * 60)

# 标量 + 向量
a_vec = np.array([1, 2, 3])
print(f"\n{a_vec} + 10  ->  {a_vec + 10}")

# 列向量 + 行向量
col = np.array([[1], [2], [3]])           # shape (3, 1)
row = np.array([10, 20, 30, 40])          # shape (4,)
result = col + row                         # shape (3, 4)
print(f"\n列向量（Column）:\n{col}")
print(f"行向量（Row）: {row}")
print(f"相加结果（Result）:\n{result}")
print(f"结果 shape: {result.shape}")

# 广播在距离计算中的应用 —— 归一化（Normalization）示例
data = np.array([[1.0, 2.0], [3.0, 4.0], [5.0, 6.0]])
mean = data.mean(axis=0)                   # shape (2,)
std = data.std(axis=0)                     # shape (2,)
normalized = (data - mean) / std           # 广播: (3,2) - (2,) → (3,2);  (3,2) / (2,) → (3,2)
print(f"\n数据（Data）:\n{data}")
print(f"均值（Mean）: {mean}")
print(f"标准差（Std）: {std}")
print(f"标准化后（Normalized）:\n{normalized}")


# ============================================================
# 4. 向量化 vs Python 循环 —— 性能对比
# ============================================================
print("\n" + "=" * 60)
print("4. 向量化 vs Python 循环（Vectorization vs Loop）")
print("=" * 60)


def py_square(x):
    """Python 循环版本平方"""
    result = []
    for i in range(len(x)):
        result.append(x[i] ** 2)
    return np.array(result)


def np_square(x):
    """NumPy 向量化版本平方"""
    return x ** 2


# 小规模数据验证结果相同
small = np.arange(10)
assert np.allclose(py_square(small), np_square(small)), "结果不一致（Results differ!）"
print("验证通过：两个版本结果相同（Verification passed: identical results）")

# 大规模数据性能对比
size = 10_000_000
large = np.random.randn(size)

start = time.time()
_ = py_square(large)
loop_time = time.time() - start

start = time.time()
_ = np_square(large)
numpy_time = time.time() - start

print(f"\n数组大小（Array size）: {size:,}")
print(f"Python 循环（Loop）: {loop_time:.4f}s")
print(f"NumPy 向量化（Vectorized）: {numpy_time:.4f}s")
print(f"加速比（Speedup）: {loop_time / numpy_time:.1f}x")


# ============================================================
# 5. 索引与切片（Indexing & Slicing）
# ============================================================
print("\n" + "=" * 60)
print("5. 索引与切片（Indexing & Slicing）")
print("=" * 60)

mat = np.arange(16).reshape(4, 4)
print(f"原始矩阵（Original）:\n{mat}")

# 花式索引（Fancy Indexing）
print(f"\n第 1、3 行（Rows 1 & 3）:\n{mat[[0, 2]]}")
print(f"第 1、3 列（Cols 1 & 3）:\n{mat[:, [1, 3]]}")

# 布尔索引（Boolean Indexing）
mask = mat > 5
print(f"\n布尔掩码（Boolean Mask > 5）:\n{mask}")
print(f"满足条件的值（Values > 5）: {mat[mask]}")

# where 条件索引
where_result = np.where(mat > 8, mat, -1)
print(f"\nnp.where(mat > 8, mat, -1):\n{where_result}")


# ============================================================
# 6. 常用统计与聚合函数
# ============================================================
print("\n" + "=" * 60)
print("6. 统计与聚合（Statistics & Aggregation）")
print("=" * 60)

stats_data = np.random.randn(100_000)
print(f"均值（Mean）:   {stats_data.mean():.6f}")
print(f"标准差（Std）:  {stats_data.std():.6f}")
print(f"最小值（Min）:  {stats_data.min():.6f}")
print(f"最大值（Max）:  {stats_data.max():.6f}")
print(f"中位数（Median）: {np.median(stats_data):.6f}")

# 按 axis 聚合
agg_mat = np.array([[1, 2, 3], [4, 5, 6]])
print(f"\n矩阵（Matrix）:\n{agg_mat}")
print(f"axis=0 求均值: {agg_mat.mean(axis=0)}  (每列均值)")
print(f"axis=1 求均值: {agg_mat.mean(axis=1)}  (每行均值)")

print("\n✅ NumPy 基础演示完毕！（NumPy Basics Demo Complete!）")
