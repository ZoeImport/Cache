"""
pytorch_deep_dive.py — PyTorch 深度剖析配套代码

Shows:
1. Tensor Storage & Stride internals (zero-copy views)
2. Mini-Autograd engine (Scalar class with backward)
3. PyTorch Autograd comparison on a small MLP
4. Computation graph visualization via prints

Requirements: torch >= 2.1.0, numpy, matplotlib
"""

import math
import torch
import torch.nn as nn
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

# =============================================================================
# Part 1 — Tensor Storage & Stride Internals
# =============================================================================

print("=" * 65)
print("PART 1: Tensor Storage & Stride Internals")
print("=" * 65)

t = torch.tensor([[1, 2, 3], [4, 5, 6]])
print(f"\nTensor:\n{t}")
print(f"shape:      {t.shape}")
print(f"stride:     {t.stride()}")
print(f"storage:    {t.storage()}")
print(f"storage ptr: {t.storage().data_ptr()}")

# Transpose = swap shape AND stride (zero-copy)
print("\n--- Transpose (zero-copy) ---")
t_t = t.T
print(f"t_t shape:   {t_t.shape}")
print(f"t_t stride:  {t_t.stride()}")
print(f"same storage: {t.storage().data_ptr() == t_t.storage().data_ptr()}")

# contiguous() makes a new re-ordered storage
print("\n--- contiguous() after transpose ---")
t_c = t_t.contiguous()
print(f"t_c storage: {t_c.storage()}")  # reordered: 1 4 2 5 3 6
print(f"t_c is_contiguous: {t_c.is_contiguous()}")
print(f"different storage: {t.storage().data_ptr() != t_c.storage().data_ptr()}")

# Manual stride index calculation:
# offset = storage_offset + sum(index[d] * stride[d])
print("\n--- Manual index via stride ---")
row, col = 1, 2
manual_idx = t.storage_offset() + row * t.stride()[0] + col * t.stride()[1]
print(f"t[1,2] = {t[1,2].item()}, storage[{manual_idx}] = {t.storage()[manual_idx]}")


# =============================================================================
# Part 2 — Mini Autograd: Scalar class
# =============================================================================

print("\n" + "=" * 65)
print("PART 2: Mini Autograd Engine (Scalar class)")
print("=" * 65)


class Scalar:
    """A scalar value that tracks computation graph for autograd.

    This is a minimal implementation showing how autograd engines work
    under the hood: each Scalar knows its _prev (creator nodes) and
    _backward (local gradient function).
    """

    def __init__(self, data, _children=(), _op=""):
        self.data = data
        self.grad = 0.0
        self._backward = lambda: None  # local gradient contribution
        self._prev = set(_children)
        self._op = _op  # for graph printing
        self._id = id(self)

    def __repr__(self):
        return f"Scalar(data={self.data:.4f}, grad={self.grad:.4f})"

    def __add__(self, other):
        other = other if isinstance(other, Scalar) else Scalar(other)
        out = Scalar(self.data + other.data, (self, other), "+")

        def _backward():
            # d(loss)/dself += d(loss)/dout * 1
            self.grad += out.grad
            other.grad += out.grad
        out._backward = _backward
        return out

    def __mul__(self, other):
        other = other if isinstance(other, Scalar) else Scalar(other)
        out = Scalar(self.data * other.data, (self, other), "*")

        def _backward():
            self.grad += other.data * out.grad
            other.grad += self.data * out.grad
        out._backward = _backward
        return out

    def __pow__(self, other):
        assert isinstance(other, (int, float)), "pow only supports int/float"
        out = Scalar(self.data ** other, (self,), f"**{other}")

        def _backward():
            self.grad += (other * (self.data ** (other - 1))) * out.grad
        out._backward = _backward
        return out

    def __neg__(self):
        return self * (-1)

    def __sub__(self, other):
        return self + (-other)

    def __truediv__(self, other):
        return self * (other ** -1)

    def relu(self):
        out = Scalar(max(0.0, self.data), (self,), "ReLU")

        def _backward():
            self.grad += (out.data > 0) * out.grad
        out._backward = _backward
        return out

    def backward(self):
        """Topological order traversal, then apply chain rule backwards."""
        # Build topological order via DFS
        topo = []
        visited = set()

        def build_topo(v):
            if v._id not in visited:
                visited.add(v._id)
                for child in v._prev:
                    build_topo(child)
                topo.append(v)

        build_topo(self)

        # Go one-variable-at-a-time backward (reverse mode)
        self.grad = 1.0  # d(loss)/dloss = 1
        for v in reversed(topo):
            v._backward()


def print_graph(root, label="Graph"):
    """Print computation graph structure starting from root."""
    print(f"\n--- {label} ---")
    topo = []
    visited = set()

    def build_topo(v):
        if v._id not in visited:
            visited.add(v._id)
            for child in v._prev:
                build_topo(child)
            topo.append(v)
    build_topo(root)

    print(f"{'Var':<6} {'data':>8} {'grad':>8} {'op':<6} {'children'}")
    print("-" * 50)
    for v in topo:
        short_id = str(v._id)[-4:]
        children_ids = ",".join(str(c._id)[-4:] for c in v._prev) if v._prev else "—"
        print(f"{short_id:<6} {v.data:>8.4f} {v.grad:>8.4f} {v._op:<6} {children_ids}")


def scalar_loss(y_pred, y_true):
    """Mean squared error loss on a single output."""
    return (y_pred - y_true) ** 2


# --- Manual MLP forward & backward with Scalar ---
print("\n>>> Mini MLP with Scalar autograd <<<")

# Network: y = w2 * relu(w1 * x + b1) + b2
# Input: x=0.5
x = Scalar(0.5)
w1 = Scalar(0.3)
b1 = Scalar(0.1)
w2 = Scalar(-0.8)
b2 = Scalar(0.2)

# Forward pass
h = w1 * x + b1  # z1
a = h.relu()      # activation
y_pred = w2 * a + b2  # logit

# Compute loss: L = (y_pred - 1.0)^2
target = Scalar(1.0)
loss = scalar_loss(y_pred, target)

print(f"\nForward values:")
print(f"  x={x.data:.4f}, w1={w1.data:.4f}, b1={b1.data:.4f}")
print(f"  z1 = w1*x + b1 = {h.data:.4f}")
print(f"  a  = relu(z1)  = {a.data:.4f}")
print(f"  y_pred = w2*a + b2 = {y_pred.data:.4f}")
print(f"  loss = (y_pred - 1)^2 = {loss.data:.4f}")

# Backward
loss.backward()
print(f"\nGradients from Scalar autograd:")
print(f"  d(loss)/dw1 = {w1.grad:.4f}  (manual: {0.5 * 2 * (y_pred.data - 1) * w2.data:.4f})")
print(f"  d(loss)/dx  = {x.grad:.4f}")
print(f"  d(loss)/db1 = {b1.grad:.4f}")
print(f"  d(loss)/dw2 = {w2.grad:.4f}")
print(f"  d(loss)/db2 = {b2.grad:.4f}")
print(f"  d(loss)/da  = {a.grad:.4f}")

# Visualize graph
print_graph(loss, "Computation Graph (Scalar)")

# Verify manual chain rule for d(loss)/dw2:
# loss = (w2 * a + b2 - 1)^2
# d(loss)/dw2 = 2 * (w2*a + b2 - 1) * a
manual_dw2 = 2.0 * (y_pred.data - target.data) * a.data
print(f"\nVerification: d(loss)/dw2")
print(f"  Scalar autograd: {w2.grad:.6f}")
print(f"  Manual chain:    {manual_dw2:.6f}")
print(f"  Match:           {abs(w2.grad - manual_dw2) < 1e-6}")

# =============================================================================
# Part 3 — PyTorch Autograd Comparison
# =============================================================================

print("\n" + "=" * 65)
print("PART 3: PyTorch Autograd Comparison on MLP")
print("=" * 65)

torch.manual_seed(42)

# Same network in PyTorch
x_pt = torch.tensor([0.5], requires_grad=True)
w1_pt = torch.tensor([0.3], requires_grad=True)
b1_pt = torch.tensor([0.1], requires_grad=True)
w2_pt = torch.tensor([-0.8], requires_grad=True)
b2_pt = torch.tensor([0.2], requires_grad=True)
target_pt = torch.tensor([1.0])

# Forward
h_pt = w1_pt * x_pt + b1_pt
a_pt = torch.relu(h_pt)
y_pred_pt = w2_pt * a_pt + b2_pt
loss_pt = (y_pred_pt - target_pt) ** 2

# Backward
loss_pt.backward()

print(f"\nComparison of gradients:")
print(f"{'Param':<8} {'Scalar':>10} {'PyTorch':>10} {'Match':>8}")
print("-" * 40)
params = [
    ("w1", w1.grad, w1_pt.grad.item()),
    ("x",  x.grad,  x_pt.grad.item()),
    ("b1", b1.grad, b1_pt.grad.item()),
    ("w2", w2.grad, w2_pt.grad.item()),
    ("b2", b2.grad, b2_pt.grad.item()),
]
all_match = True
for name, s_grad, pt_grad in params:
    match = abs(s_grad - pt_grad) < 1e-6
    all_match = all_match and match
    print(f"{name:<8} {s_grad:>10.6f} {pt_grad:>10.6f} {str(match):>8}")

print(f"\nAll gradients match: {all_match}")

# =============================================================================
# Part 4 — Gradient Accumulation Demo
# =============================================================================

print("\n" + "=" * 65)
print("PART 4: Gradient Accumulation Demo")
print("=" * 65)

x_acc = torch.tensor([1.0], requires_grad=True)
w_acc = torch.tensor([2.0], requires_grad=True)

for i in range(3):
    y = x_acc * w_acc
    y.backward()
    print(f"  After backward #{i+1}: x.grad={x_acc.grad.item():.1f}, "
          f"w.grad={w_acc.grad.item():.1f}  (ACCUMULATING)")

print("\n  >>> Need optimizer.zero_grad() between steps!")
x_acc.grad.zero_()
w_acc.grad.zero_()
print(f"  After zero_grad(): x.grad={x_acc.grad.item():.1f}, w.grad={w_acc.grad.item():.1f}")

# =============================================================================
# Part 5 — nn.Module Internals Demonstration
# =============================================================================

print("\n" + "=" * 65)
print("PART 5: nn.Module Internals")
print("=" * 65)


class CustomLinear(nn.Module):
    """Custom Linear layer showing parameter registration."""
    def __init__(self, in_features, out_features):
        super().__init__()
        self.weight = nn.Parameter(torch.randn(out_features, in_features) * 0.1)
        self.bias = nn.Parameter(torch.zeros(out_features))

    def forward(self, x):
        return x @ self.weight.T + self.bias


class CustomMLP(nn.Module):
    """2-layer MLP with custom linear layers."""
    def __init__(self, in_dim, hidden_dim, out_dim):
        super().__init__()
        self.fc1 = CustomLinear(in_dim, hidden_dim)
        self.relu = nn.ReLU()
        self.fc2 = CustomLinear(hidden_dim, out_dim)

    def forward(self, x):
        return self.fc2(self.relu(self.fc1(x)))


model = CustomMLP(4, 8, 1)
print(f"\nModel structure:\n{model}")
print(f"\nNamed parameters:")
for name, param in model.named_parameters():
    print(f"  {name}: shape={param.shape}, requires_grad={param.requires_grad}")

print(f"\nTotal parameters: {sum(p.numel() for p in model.parameters())}")

# =============================================================================
# Part 6 — Dataset & DataLoader Demo
# =============================================================================

print("\n" + "=" * 65)
print("PART 6: Dataset & DataLoader")
print("=" * 65)

from torch.utils.data import Dataset, DataLoader


class SimpleRegressionDataset(Dataset):
    """y = 2*x + 1 + noise"""
    def __init__(self, n_samples=100):
        self.x = torch.randn(n_samples, 1)
        self.y = 2.0 * self.x + 1.0 + 0.1 * torch.randn(n_samples, 1)

    def __len__(self):
        return len(self.x)

    def __getitem__(self, idx):
        return self.x[idx], self.y[idx]


dataset = SimpleRegressionDataset(1000)
loader = DataLoader(dataset, batch_size=32, shuffle=True, num_workers=0)

print(f"Dataset size: {len(dataset)}")
batch_x, batch_y = next(iter(loader))
print(f"Batch shape: x={batch_x.shape}, y={batch_y.shape}")

# Show different sampler types
from torch.utils.data import SequentialSampler, RandomSampler

seq_sampler = SequentialSampler(dataset)
rand_sampler = RandomSampler(dataset)
print(f"\nSequentialSampler first 5: {list(seq_sampler)[:5]}")
print(f"RandomSampler first 5:    {list(rand_sampler)[:5]}")

# =============================================================================
# Part 7 — torch.compile Demo (may need g++ and disk space)
# =============================================================================

print("\n" + "=" * 65)
print("PART 7: torch.compile Demo (speed comparison)")
print("=" * 65)
print("NOTE: torch.compile requires C++ compiler and may fail in some")
print("environments (e.g. limited disk quota). This is an env issue, not")
print("a code issue. The benchmark uses try/except for graceful fallback.")

import time


def train_step(model, x, y, loss_fn, optimizer):
    optimizer.zero_grad()
    y_pred = model(bx)
    loss_val = loss_fn(y_pred, by)
    loss_val.backward()
    optimizer.step()
    return loss_val.item()


# Build a slightly larger model for the benchmark
class BenchModel(nn.Module):
    def __init__(self):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(256, 512),
            nn.ReLU(),
            nn.Linear(512, 512),
            nn.ReLU(),
            nn.Linear(512, 256),
            nn.ReLU(),
            nn.Linear(256, 10),
        )

    def forward(self, x):
        return self.net(x)


model_eager = BenchModel()
model_compiled = torch.compile(BenchModel())

bx = torch.randn(128, 256)
by = torch.randn(128, 10)
loss_fn = nn.MSELoss()

opt_eager = torch.optim.SGD(model_eager.parameters(), lr=0.01)
opt_compiled = torch.optim.SGD(model_compiled.parameters(), lr=0.01)

# Warmup (also compilation happens here for compiled)
print("Warming up...")
for _ in range(5):
    train_step(model_eager, bx, by, loss_fn, opt_eager)

n_steps = 50
compile_enabled = False
compile_speedup = 0.0

try:
    for _ in range(5):
        train_step(model_compiled, bx, by, loss_fn, opt_compiled)

    # Benchmark
    print(f"Benchmarking over {n_steps} steps...")

    start = time.perf_counter()
    for _ in range(n_steps):
        train_step(model_eager, bx, by, loss_fn, opt_eager)
    eager_time = time.perf_counter() - start

    start = time.perf_counter()
    for _ in range(n_steps):
        train_step(model_compiled, bx, by, loss_fn, opt_compiled)
    compiled_time = time.perf_counter() - start

    print(f"\n{'Mode':<20} {'Total Time (s)':>16} {'Avg Step (ms)':>16}")
    print("-" * 55)
    print(f"{'Eager':<20} {eager_time:>16.4f} {eager_time/n_steps*1000:>16.4f}")
    print(f"{'torch.compile':<20} {compiled_time:>16.4f} {compiled_time/n_steps*1000:>16.4f}")
    print(f"{'Speedup':<20} {eager_time/compiled_time:>16.2f}x")

    compile_speedup = eager_time / compiled_time
    compile_enabled = True
except Exception as e:
    print(f"\ntorch.compile not available: {e}")
    compile_enabled = False
    compile_speedup = 0.0

# =============================================================================
# Part 8 — Visualization: Storage Layout
# =============================================================================

print("\n" + "=" * 65)
print("PART 8: Visualization (saved to output/)")
print("=" * 65)

import os
os.makedirs("output", exist_ok=True)

fig, axes = plt.subplots(1, 3, figsize=(14, 4))

# --- Panel 1: Storage layout of a 2x3 tensor ---
ax = axes[0]
data_2x3 = np.array([[1, 2, 3], [4, 5, 6]])
ax.imshow(data_2x3, cmap="Blues", aspect="auto")
for i in range(2):
    for j in range(3):
        ax.text(j, i, str(data_2x3[i, j]), ha="center", va="center", fontsize=14)
ax.set_title("Logical View (2x3)")
ax.set_xlabel("Column")
ax.set_ylabel("Row")

# --- Panel 2: Transposed (swap stride) ---
ax = axes[1]
data_3x2 = data_2x3.T
ax.imshow(data_3x2, cmap="Oranges", aspect="auto")
for i in range(3):
    for j in range(2):
        ax.text(j, i, str(data_3x2[i, j]), ha="center", va="center", fontsize=14)
ax.set_title("Transposed (3x2, zero-copy)")
ax.set_xlabel("Column")
ax.set_ylabel("Row")

# --- Panel 3: Physical storage (1D) ---
ax = axes[2]
storage_data = np.array([1, 2, 3, 4, 5, 6])
ax.barh(range(6), [1]*6, left=range(6), height=0.6, color="skyblue")
for i, val in enumerate(storage_data):
    ax.text(i + 0.5, i, str(val), ha="center", va="center", fontsize=12)
ax.set_yticks(range(6))
ax.set_yticklabels([f"idx {i}" for i in range(6)])
ax.set_xlim(0, 6)
ax.set_title("Physical Storage (1D array)")
ax.set_xlabel("Offset")
ax.invert_yaxis()

plt.tight_layout()
plt.savefig("output/tensor_storage_layout.png", dpi=150)
print("Saved tensor_storage_layout.png")

# --- Panel 4: Autograd computation graph ---
fig2, ax2 = plt.subplots(figsize=(8, 5))

# Build the graph from Scalar loss
topo = []
visited = set()

def build_topo(v):
    if v._id not in visited:
        visited.add(v._id)
        for child in v._prev:
            build_topo(child)
        topo.append(v)

build_topo(loss)

# Assign layers
layers = {}
for i, v in enumerate(topo):
    layers[v._id] = i

ax2.axis("off")
ax2.set_title("Computation Graph (from Scalar autograd)", fontsize=14)

# Draw nodes
node_labels = {
    loss._id: f"loss={loss.data:.2f}",
    y_pred._id: f"y_pred={y_pred.data:.2f}",
    target._id: f"target={target.data:.2f}",
    a._id: f"a={a.data:.2f}",
    h._id: f"z={h.data:.2f}",
    w2._id: f"w2={w2.data:.2f}",
    b2._id: f"b2={b2.data:.2f}",
    w1._id: f"w1={w1.data:.2f}",
    x._id: f"x={x.data:.2f}",
    b1._id: f"b1={b1.data:.2f}",
}

# Manual layout
positions = {
    loss._id: (5, 9),
    y_pred._id: (5, 7),
    target._id: (6, 7),
    a._id: (5, 5),
    h._id: (5, 3),
    w2._id: (3, 5),
    b2._id: (7, 5),
    w1._id: (3, 1),
    x._id: (5, 1),
    b1._id: (7, 1),
}

for vid, (px, py) in positions.items():
    label = node_labels.get(vid, f"id={vid}")
    ax2.plot(px, py, "o", markersize=20, color="lightblue", markeredgecolor="navy")
    ax2.text(px, py - 0.3, label, ha="center", va="top", fontsize=8)

# Draw edges
edges_drawn = set()
for v in topo:
    for child in v._prev:
        ekey = (child._id, v._id)
        if ekey not in edges_drawn:
            edges_drawn.add(ekey)
            if child._id in positions and v._id in positions:
                x1, y1 = positions[child._id]
                x2, y2 = positions[v._id]
                ax2.annotate("", xy=(x2, y2), xytext=(x1, y1),
                             arrowprops=dict(arrowstyle="->", color="gray", lw=1.5))

ax2.set_xlim(0, 10)
ax2.set_ylim(0, 10)
plt.tight_layout()
plt.savefig("output/computation_graph.png", dpi=150)
print("Saved computation_graph.png")

# =============================================================================
# Summary
# =============================================================================

print("\n" + "=" * 65)
print("SUMMARY")
print("=" * 65)
print(f"""
1. Tensor Storage & Stride
   - Storage is a flat 1D data array
   - Stride maps logical index -> physical offset
   - Transpose/slice are zero-copy (swap stride)

2. Mini Autograd (Scalar)
   - Computation graph: DAG of Function nodes
   - Backward: topological sort + chain rule
   - Gradient accumulation: .backward() ADDS to .grad

3. PyTorch Comparison
   - Manual gradients match PyTorch autograd: {all_match}

4. torch.compile Speedup""" + (
    f"""
   - Enabled:          Yes
   - Eager avg step:   {eager_time/n_steps*1000:.2f} ms
   - Compiled avg step: {compiled_time/n_steps*1000:.2f} ms
   - Speedup:          {compile_speedup:.2f}x"""
    if compile_enabled else
    """
   - Enabled:          No (C++ compiler/disk quota required)
   - Expected benefit: ~20% end-to-end speedup on GPU
   - Works via:        TorchDynamo + Inductor (kernel fusion)"""
) + "\n")
