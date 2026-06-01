"""
Python Quickstart — Companion Code
====================================
Demonstrates the 20% of Python covering 80% of ML use cases.
Run with: python ai/01-overview/code/python_quickstart.py
"""

# ============================================================
# 1. DATA TYPES (数据类型)
# ============================================================
print("=" * 60)
print("1. DATA TYPES")
print("=" * 60)

# Basic types
x = 42                # int
y = 3.14159           # float
z = "hello"           # str
flag = True           # bool
nothing = None        # NoneType

print(f"int: {x}, float: {y:.4f}, str: {z}, bool: {flag}, None: {nothing}")

# Type checking
print(f"type(x)={type(x)}, isinstance(x, int)={isinstance(x, int)}")

# Type conversion
print(f"float(x)={float(x)}, int('42')={int('42')}")

# Container types
lst = [1, 2, 3, 2]
lst.append(4)
print(f"\nlist: {lst}, lst[0]={lst[0]}, lst[-1]={lst[-1]}")

tup = (1, 2, 3)
print(f"tuple: {tup}, tup[0]={tup[0]}")

d = {"name": "Alice", "age": 25}
print(f"dict: {d}, name={d['name']}, get score={d.get('score', 0)}")

s = {1, 2, 3, 2}
s.add(4)
print(f"set: {s}")

# ============================================================
# 2. CONTROL FLOW (控制流)
# ============================================================
print("\n" + "=" * 60)
print("2. CONTROL FLOW")
print("=" * 60)

# if / elif / else
score = 85
if score >= 90:
    grade = "A"
elif score >= 80:
    grade = "B"
else:
    grade = "C"
print(f"score={score}, grade={grade}")

# for loop
print("for loop (range):", end=" ")
for i in range(5):
    print(i, end=" ")
print()

# enumerate
print("enumerate:")
for idx, val in enumerate(["a", "b", "c"]):
    print(f"  [{idx}] = {val}")

# dict iteration
print("dict items:")
for k, v in {"lr": 0.001, "epochs": 10}.items():
    print(f"  {k}: {v}")

# while loop
epoch = 0
while epoch < 3:
    epoch += 1
print(f"while loop: {epoch} epochs")

# List comprehension — critical for ML
squares = [x**2 for x in range(10)]
evens = [x for x in range(20) if x % 2 == 0]
print(f"\nlist comprehension — squares: {squares}")
print(f"list comprehension — evens: {evens}")

# Dict comprehension
square_dict = {x: x**2 for x in range(5)}
print(f"dict comprehension: {square_dict}")

# ============================================================
# 3. FUNCTIONS (函数)
# ============================================================
print("\n" + "=" * 60)
print("3. FUNCTIONS")
print("=" * 60)

# Basic function
def mean(values):
    """Compute the mean of a list."""
    return sum(values) / len(values)

print(f"mean([1, 2, 3, 4, 5]) = {mean([1, 2, 3, 4, 5])}")

# Default arguments
def normalize(x, eps=1e-8):
    mx = max(x)
    return [v / (mx + eps) for v in x]

print(f"normalize([3, 1, 2]) = {normalize([3, 1, 2])}")

# *args
def concat(*args):
    return " ".join(args)

print(f"concat('a', 'b', 'c') = {concat('a', 'b', 'c')}")

# **kwargs
def print_config(**kwargs):
    for k, v in kwargs.items():
        print(f"  config {k} = {v}")

print("print_config:")
print_config(lr=0.001, epochs=10, batch_size=32)

# lambda
square = lambda x: x**2
doubled = list(map(lambda x: x * 2, [1, 2, 3]))
print(f"\nlambda square(5) = {square(5)}")
print(f"map(lambda x: x*2, [1,2,3]) = {doubled}")

# Type hints
def add(a: int, b: int) -> int:
    return a + b

print(f"type-hinted add(3, 4) = {add(3, 4)}")

# filter
positive = list(filter(lambda x: x > 0, [1.5, -2.3, 3.7, -0.5]))
print(f"filter positive: {positive}")

# sorted with key
pairs = [(3, "a"), (1, "c"), (2, "b")]
sorted_pairs = sorted(pairs, key=lambda x: x[0])
print(f"sorted by key: {sorted_pairs}")

# ============================================================
# 4. SLICING (切片)
# ============================================================
print("\n" + "=" * 60)
print("4. SLICING")
print("=" * 60)

arr = [10, 20, 30, 40, 50]
print(f"arr: {arr}")
print(f"arr[1:4]  = {arr[1:4]}")    # [20, 30, 40]
print(f"arr[:3]   = {arr[:3]}")     # [10, 20, 30]
print(f"arr[::2]  = {arr[::2]}")    # [10, 30, 50]
print(f"arr[::-1] = {arr[::-1]}")   # [50, 40, 30, 20, 10]

# ============================================================
# 5. ZIP / ENUMERATE
# ============================================================
print("\n" + "=" * 60)
print("5. ZIP / ENUMERATE")
print("=" * 60)

for i, (x, y) in enumerate(zip([1, 2, 3], [4, 5, 6])):
    print(f"  [{i}] {x} + {y} = {x + y}")

# ============================================================
# 6. TERNARY / F-STRINGS (三元表达式 / 格式化)
# ============================================================
print("\n" + "=" * 60)
print("6. TERNARY EXPRESSIONS & F-STRINGS")
print("=" * 60)

x_val = 10
label = "positive" if x_val > 0 else "negative"
print(f"ternary: {x_val} -> {label}")

model_name, acc = "ResNet", 0.9523
print(f"f-string: Model={model_name}, Acc={acc:.2%}")

# ============================================================
# 7. CONTEXT MANAGER (上下文管理器 — with 语句)
# ============================================================
print("\n" + "=" * 60)
print("7. CONTEXT MANAGER (with statement)")
print("=" * 60)

# Write and read a temp file to demonstrate with
with open("/tmp/python_quickstart_demo.txt", "w") as f:
    f.write("Hello from Python Quickstart!\n")
    f.write("File auto-closed after with block.")

with open("/tmp/python_quickstart_demo.txt", "r") as f:
    content = f.read()

print(f"File content:\n{content}")

# ============================================================
# 8. ERROR HANDLING (错误处理)
# ============================================================
print("\n" + "=" * 60)
print("8. ERROR HANDLING")
print("=" * 60)

try:
    result = 1 / 0
except ZeroDivisionError as e:
    print(f"Caught ZeroDivisionError: {e}")
except Exception as e:
    print(f"Caught Exception: {e}")
finally:
    print("Finally block: always executes.")

# ============================================================
# 9. OOP (面向对象)
# ============================================================
print("\n" + "=" * 60)
print("9. OOP — CLASSES & INHERITANCE")
print("=" * 60)

class Layer:
    """A simple linear layer (simulating nn.Module)."""
    def __init__(self, in_features: int, out_features: int):
        self.in_features = in_features
        self.out_features = out_features
        # Initialize weights with a simple scheme
        self.weight = [[0.1 * (i + j) for j in range(out_features)] for i in range(in_features)]
        self.bias = [0.0] * out_features

    def forward(self, x):
        """Simulate a forward pass (dot product per output)."""
        outputs = []
        for x_i in x:
            out = []
            for j in range(self.out_features):
                val = sum(x_i[k] * self.weight[k][j] for k in range(self.in_features))
                out.append(val + self.bias[j])
            outputs.append(out)
        return outputs

    def __repr__(self):
        return f"Layer(in={self.in_features}, out={self.out_features})"

# Create and use a layer
layer = Layer(3, 2)
print(f"Layer: {layer}")
inp = [[1.0, 2.0, 3.0]]
out = layer.forward(inp)
print(f"Forward({inp}) -> {out}")

# Inheritance
class MyLinear(Layer):
    """Inherits Layer, adds bias toggle."""
    def __init__(self, in_f, out_f, bias=True):
        super().__init__(in_f, out_f)
        self.use_bias = bias

    def forward(self, x):
        if not self.use_bias:
            # Temporarily zero out bias
            saved = self.bias
            self.bias = [0.0] * self.out_features
            result = super().forward(x)
            self.bias = saved
            return result
        return super().forward(x)

linear = MyLinear(2, 2, bias=False)
print(f"MyLinear (no bias): {linear}")
print(f"Forward: {linear.forward([[1.0, 2.0]])}")

# ============================================================
# SUMMARY (总结)
# ============================================================
print("\n" + "=" * 60)
print("ALL DEMOS PASSED — Python Quickstart Complete!")
print("=" * 60)
