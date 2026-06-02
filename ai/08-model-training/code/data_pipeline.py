#!/usr/bin/env python3
"""data_pipeline.py -- Benchmark DataLoader: num_workers & prefetch_factor vs throughput."""

import time, sys, numpy as np

SEP = "=" * 72


class SyntheticDataset:
    def __init__(self, size=10000, shape=(3, 224, 224), latency_ms=1.0):
        self.size, self.shape, self.lat = size, shape, latency_ms / 1000.0
        self.data = np.random.randint(0, 256, (size, *shape), dtype=np.uint8)
        self.labels = np.random.randint(0, 1000, size, dtype=np.int64)

    def __len__(self):
        return self.size

    def __getitem__(self, idx):
        time.sleep(self.lat)
        img = self.data[idx].astype(np.float32) / 255.0
        return img, self.labels[idx]


def bench(dataset, bs=64, nw=0, pf=2):
    from torch.utils.data import DataLoader
    lbl = f"workers={nw}, prefetch={pf}"
    print(f"\n  {lbl}")

    loader = DataLoader(dataset, batch_size=bs, shuffle=True, num_workers=nw,
                        prefetch_factor=pf if nw > 0 else None, drop_last=True)

    times, samples = [], 0
    print("  Running...", end=" ", flush=True)
    for i, batch in enumerate(loader):
        if i >= 20:
            break
        t0 = time.perf_counter()
        imgs, lbls = batch
        dt = time.perf_counter() - t0
        times.append(dt)
        samples += imgs.size(0)

    sps = samples / sum(times)
    arr = np.array(times)
    res = {"label": lbl, "sps": sps, "mean": float(np.mean(arr)) * 1000,
           "p99": float(np.percentile(arr, 99)) * 1000, "nw": nw}
    print(f"done - {sps:.0f} samples/sec, mean {res['mean']:.1f}ms")
    return res


def main():
    print(f"  DataLoader Benchmark  |  PyTorch {__import__('torch').__version__}  |  NumPy {np.__version__}")
    print(SEP)

    ds = SyntheticDataset(size=10000, latency_ms=1.0)
    print(f"\n  Dataset: {len(ds)} samples, 3x224x224, 1ms/sample latency, batch=64\n")

    results = []

    print("  --- Config A: num_workers ---")
    for nw in [0, 2, 4]:
        results.append(bench(ds, nw=nw, pf=2))

    print("\n  --- Config B: prefetch_factor (workers=2) ---")
    for pf in [2, 4, 8]:
        results.append(bench(ds, nw=2, pf=pf))

    print(f"\n{SEP}\n  Throughput Comparison Table\n{SEP}")
    bl = max(r["sps"] for r in results if r["nw"] == 0)
    print(f"  {'Config':<30} {'Samples/sec':<14} {'Mean':<10} {'P99':<10} {'Speedup':<8}")
    print(f"  {'-'*72}")
    for r in results:
        print(f"  {r['label']:<30} {r['sps']:>8.0f}       {r['mean']:>5.1f}ms   {r['p99']:>5.1f}ms   {r['sps']/bl:>4.2f}x")

    best = max(results, key=lambda r: r["sps"])
    print(f"\n  Best: {best['label']} ({best['sps']:.0f} samples/sec, speedup {best['sps']/bl:.2f}x)")
    print("""
  Guidelines:
    workers=0: debugging, low throughput
    workers=2: good balance
    workers=4: CPU-bound preprocessing
    Higher prefetch = better overlap of I/O and compute""")
    print(SEP, "\n  Benchmark Complete\n")


if __name__ == "__main__":
    main()
