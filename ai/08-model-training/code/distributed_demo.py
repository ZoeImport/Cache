#!/usr/bin/env python3
"""distributed_demo.py -- Simulate DDP: model shards, all-reduce, memory comparison."""

import numpy as np
import sys

SEP = "=" * 72


class ModelShard:
    def __init__(self, sid: int, params: np.ndarray):
        self.sid, self.params = sid, params.copy()
        self.gradients = np.zeros_like(params)
        self.count = params.size

    def forward(self, x: np.ndarray) -> float:
        sz = min(len(self.params), len(x))
        return float(np.dot(self.params[:sz], x[:sz]))

    def backward(self, grad: np.ndarray) -> None:
        sz = min(len(self.gradients), len(grad))
        self.gradients[:sz] = grad[:sz]


def build_shards(n: int, total: int) -> list[ModelShard]:
    full = np.random.randn(total).astype(np.float32)
    size = total // n
    return [ModelShard(i, full[i * size:(i + 1) * size])
            for i in range(n - 1)] + [ModelShard(n - 1, full[(n - 1) * size:])]


def all_reduce(shards: list[ModelShard]) -> dict:
    all_g = [s.gradients.copy() for s in shards]
    total_b = sum(g.nbytes for g in all_g)
    summed = np.sum(all_g, axis=0)
    for s in shards:
        s.gradients[:] = summed[:len(s.gradients)] / len(shards)
    return {"n": len(shards), "bytes_per": total_b // len(shards),
            "total_mb": total_b * 2 / (1024 * 1024)}


def main():
    print("  DDP Simulation  |  NumPy", np.__version__, "| Python", sys.version.split()[0])
    print(SEP)
    N, TOTAL = 4, 10_000_000

    print("\n  [Phase 1] Sharding -- {} params across {} GPUs".format(TOTAL, N))
    shards = build_shards(N, TOTAL)
    print("  {:<6} {:<20} {:<10} {:<8}".format("GPU", "Range", "Count", "%"))
    print("  " + "-" * 44)
    for i, s in enumerate(shards):
        st = i * (TOTAL // N)
        ed = st + s.count
        print(f"  GPU-{i:<2} [{st:>7,}-{ed:>7,})  {s.count:>8,}  {s.count/TOTAL*100:>5.1f}%")

    print("\n  [Phase 2] Training (5 steps)")
    for step in range(1, 6):
        for s in shards:
            s.backward(np.random.randn(s.count) * 0.1)
        c = all_reduce(shards)
        for s in shards:
            s.params -= 0.01 * s.gradients; s.gradients.fill(0.0)
        print(f"  Step {step}: {c['total_mb']:.2f}MB, {c['bytes_per']/1024:.1f}KB/shard")

    print("\n  [Phase 3] Comm Volume Scaling")
    print("  {:<5} {:<14} {:<14} {:<10}".format("GPUs", "Grad/GPU", "Per shard KB", "Total MB"))
    print("  " + "-" * 43)
    for ng in [1, 2, 4, 8, 16, 32]:
        gb = (TOTAL // ng) * 4
        vol = gb * (ng - 1) / ng * 2 / (1024 * 1024)
        print(f"  {ng:<5} {gb/1024:>8.1f} KB     {gb/1024:>8.1f}       {vol:>6.2f}")

    print("\n  [Phase 4] Memory: Single vs {} GPUs".format(N))
    ms = TOTAL * 4 / (1024 * 1024) * 4
    mp = (TOTAL * 4 / N) * 4 / (1024 * 1024)
    print("  {:<30} {:>10} {:>14}".format("Metric", "Single", f"{N} GPUs"))
    print("  " + "-" * 54)
    for lbl, r in [("Params (MB)", 0.25), ("Gradients (MB)", 0.25),
                    ("Optimizer (MB)", 0.5), ("Peak (MB)", 1.0)]:
        print(f"  {lbl:<30} {ms*r:>8.2f} MB    {mp*r:>8.2f} MB")
    print(f"\n  Savings/GPU: {100 - 100//N}%")

    print("\n  [Phase 5] DDP Summary")
    print("""
  1. Each GPU holds 1/{n} of model params
  2. Forward: each GPU processes a micro-batch
  3. Backward: local gradients computed
  4. All-reduce: average gradients across GPUs
  5. Optimizer step applied locally
""".format(n=N))
    print(SEP, "\n  DDP Simulation Complete\n")


if __name__ == "__main__":
    main()
