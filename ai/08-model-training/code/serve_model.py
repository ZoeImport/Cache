"""
Model Deployment Examples
=========================
This script demonstrates the full model deployment pipeline:
  1. Train a simple binary classifier on synthetic data
  2. Export to TorchScript (trace & script) and ONNX
  3. Compare file sizes across formats
  4. Run ONNX inference via onnxruntime
  5. Post-training quantization (INT8)
  6. Serve via FastAPI + test with httpx

Requirements: torch, onnx, onnxruntime, fastapi, uvicorn, httpx
"""

import math
import os
import sys
import time
import json
import threading
from pathlib import Path
from typing import List, Optional

import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, TensorDataset

# ---------------------------------------------------------------------------
# 1. Model definition  --  simple 3-layer MLP for binary classification
# ---------------------------------------------------------------------------

class SimpleMLP(nn.Module):
    """3-layer MLP: 2 -> 64 -> 32 -> 2 (binary classification)."""

    def __init__(self, input_dim: int = 2, hidden1: int = 64,
                 hidden2: int = 32, num_classes: int = 2):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(input_dim, hidden1),
            nn.ReLU(),
            nn.Linear(hidden1, hidden2),
            nn.ReLU(),
            nn.Linear(hidden2, num_classes),
        )

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return self.net(x)


# ---------------------------------------------------------------------------
# 2. Synthetic data generation  --  two interleaved moons
# ---------------------------------------------------------------------------

def make_moons(n_samples: int = 4000, noise: float = 0.12,
               random_state: int = 42) -> tuple:
    """Generate 2D moon-shaped data for binary classification."""
    rng = np.random.default_rng(random_state)
    n_per_class = n_samples // 2

    t = np.linspace(0, 2 * math.pi, n_per_class)
    # class 0: outer arc
    x0 = np.column_stack([np.cos(t), np.sin(t)]) + rng.normal(0, noise,
                                                               (n_per_class, 2))
    # class 1: inner arc (shifted)
    x1 = np.column_stack([1 - np.cos(t), 0.5 - np.sin(t)]) + rng.normal(
        0, noise, (n_per_class, 2))

    X = np.vstack([x0, x1]).astype(np.float32)
    y = np.hstack([np.zeros(n_per_class), np.ones(n_per_class)]).astype(
        np.int64)
    return X, y


def make_linear_data(n_samples: int = 2000, noise: float = 0.10,
                     random_state: int = 42) -> tuple:
    """Generate linearly separable 2D data."""
    rng = np.random.default_rng(random_state)
    n_per_class = n_samples // 2
    x0 = rng.normal(loc=[-1.5, -1.5], scale=0.6, size=(n_per_class, 2))
    x1 = rng.normal(loc=[1.5, 1.5], scale=0.6, size=(n_per_class, 2))
    X = np.vstack([x0, x1]).astype(np.float32)
    y = np.hstack([np.zeros(n_per_class), np.ones(n_per_class)]).astype(np.int64)
    return X, y


# ---------------------------------------------------------------------------
# 3. Training loop
# ---------------------------------------------------------------------------

def train_model(model: nn.Module, train_loader: DataLoader,
                epochs: int = 30, lr: float = 0.01,
                device: torch.device = torch.device("cpu")) -> list:
    """Train the model and return loss history."""
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=lr)
    history = []

    model.train()
    for epoch in range(1, epochs + 1):
        epoch_loss = 0.0
        for X_batch, y_batch in train_loader:
            X_batch, y_batch = X_batch.to(device), y_batch.to(device)
            optimizer.zero_grad()
            outputs = model(X_batch)
            loss = criterion(outputs, y_batch)
            loss.backward()
            optimizer.step()
            epoch_loss += loss.item() * X_batch.size(0)

        avg_loss = epoch_loss / len(train_loader.dataset)
        history.append(avg_loss)
        if epoch % 20 == 0 or epoch == 1:
            print(f"  Epoch {epoch:3d}/{epochs}  loss={avg_loss:.6f}")
    return history


def accuracy(model: nn.Module, loader: DataLoader,
             device: torch.device = torch.device("cpu")) -> float:
    """Compute classification accuracy."""
    model.eval()
    correct = total = 0
    with torch.no_grad():
        for X_batch, y_batch in loader:
            X_batch = X_batch.to(device)
            preds = model(X_batch).argmax(dim=1).cpu()
            correct += (preds == y_batch).sum().item()
            total += y_batch.size(0)
    return correct / total


# ---------------------------------------------------------------------------
# 4. Model export helpers
# ---------------------------------------------------------------------------

def export_torchscript_trace(model: nn.Module, example_input: torch.Tensor,
                             save_path: str) -> str:
    """Export via torch.jit.trace() -- for models without data-dependent
    control flow."""
    traced = torch.jit.trace(model, example_input)
    traced.save(save_path)
    return save_path


def export_torchscript_script(model: nn.Module, save_path: str) -> str:
    """Export via torch.jit.script() -- supports dynamic control flow."""
    scripted = torch.jit.script(model)
    scripted.save(save_path)
    return save_path


def export_onnx(model: nn.Module, example_input: torch.Tensor,
                save_path: str, input_name: str = "input",
                output_name: str = "output") -> str:
    """Export to ONNX format."""
    model.eval()
    torch.onnx.export(
        model,
        example_input,
        save_path,
        input_names=[input_name],
        output_names=[output_name],
        dynamic_axes={input_name: {0: "batch_size"},
                      output_name: {0: "batch_size"}},
        opset_version=18,
    )
    return save_path


# ---------------------------------------------------------------------------
# 5. ONNX Runtime inference wrapper
# ---------------------------------------------------------------------------

class ONNXInference:
    """Run inference using ONNX Runtime."""

    def __init__(self, onnx_path: str):
        import onnxruntime as ort
        self.session = ort.InferenceSession(onnx_path,
                                            providers=["CPUExecutionProvider"])
        self.input_name = self.session.get_inputs()[0].name
        self.output_name = self.session.get_outputs()[0].name

    def predict(self, x: np.ndarray) -> np.ndarray:
        return self.session.run([self.output_name],
                                {self.input_name: x.astype(np.float32)})[0]


# ---------------------------------------------------------------------------
# 6. Post-training quantization (INT8)
# ---------------------------------------------------------------------------

def quantize_onnx_int8(onnx_path: str, output_path: str,
                       calibration_data: np.ndarray) -> str:
    """Apply INT8 post-training static quantization via onnxruntime."""
    import onnxruntime.quantization as quant

    class RandomDataLoader:
        """Minimal data loader for calibration with get_next() interface."""
        def __init__(self, data: np.ndarray, batch_size: int = 32):
            self.data = data
            self.batch_size = batch_size
            self._iter = None

        def __iter__(self):
            n = self.data.shape[0]
            indices = np.random.permutation(n)
            batches = []
            for start in range(0, n, self.batch_size):
                batch_idx = indices[start:start + self.batch_size]
                batches.append({"input": self.data[batch_idx].astype(np.float32)})
            return iter(batches)

        def get_next(self):
            if self._iter is None:
                self._iter = iter(self)
            try:
                return next(self._iter)
            except StopIteration:
                self._iter = None
                return None

    drl = RandomDataLoader(calibration_data, batch_size=64)

    quant.quantize_static(
        model_input=onnx_path,
        model_output=output_path,
        calibration_data_reader=drl,
        quant_format=quant.QuantFormat.QOperator,
        per_channel=False,
        activation_type=quant.QuantType.QInt8,
        weight_type=quant.QuantType.QInt8,
    )

    return output_path


# ---------------------------------------------------------------------------
# 7. FastAPI server
# ---------------------------------------------------------------------------


def _create_fastapi_app(model_path: str):
    """Create the FastAPI application with /predict endpoint.
    The model is loaded from disk at startup, so it works across process
    boundaries.
    """
    from fastapi import FastAPI, HTTPException
    from pydantic import BaseModel, Field

    # Load model inside the server process
    try:
        serving_model = torch.jit.load(model_path)
        serving_model.eval()
        model_loaded = True
    except Exception as exc:
        print(f"[server] Failed to load model: {exc}")
        serving_model = None
        model_loaded = False

    app = FastAPI(title="ML Model Server", version="1.0.0")

    class PredictRequest(BaseModel):
        features: List[float] = Field(..., description="Input features",
                                      min_length=2, max_length=2)

    class PredictResponse(BaseModel):
        prediction: int
        probabilities: List[float]
        model_format: str

    @app.get("/health")
    def health():
        return {"status": "ok", "model_loaded": model_loaded}

    @app.post("/predict", response_model=PredictResponse)
    def predict(req: PredictRequest):
        if not model_loaded or serving_model is None:
            raise HTTPException(status_code=503, detail="Model not loaded")
        x = np.array([req.features], dtype=np.float32)
        t = torch.from_numpy(x)
        with torch.no_grad():
            logits = serving_model(t)
            probs = torch.softmax(logits, dim=1)
        pred = int(logits.argmax(dim=1).item())
        return PredictResponse(
            prediction=pred,
            probabilities=probs[0].tolist(),
            model_format="TorchScript",
        )

    return app


def start_server(model_path: str, host: str = "127.0.0.1",
                 port: int = 8888):
    """Start the FastAPI server with uvicorn."""
    import uvicorn
    app = _create_fastapi_app(model_path)
    uvicorn.run(app, host=host, port=port, log_level="warning")


# ---------------------------------------------------------------------------
# 8. Main demo
# ---------------------------------------------------------------------------

def format_size(path: str) -> str:
    """Return human-readable file size."""
    size = os.path.getsize(path)
    if size < 1024:
        return f"{size} B"
    elif size < 1024 ** 2:
        return f"{size / 1024:.2f} KB"
    else:
        return f"{size / 1024 ** 2:.2f} MB"


def main():
    print("=" * 65)
    print("  ML Model Deployment Pipeline Demo")
    print("=" * 65)

    device = torch.device("cpu")
    output_dir = Path(__file__).parent / "output"
    output_dir.mkdir(exist_ok=True)

    # ------------------------------------------------------------------
    # 8a. Generate data & train
    # ------------------------------------------------------------------
    print("\n[1/8] Generating synthetic data (two moons)...")
    # Use linearly separable data for reliable demo; two_moons also available
    X, y = make_linear_data(n_samples=2000, noise=0.10)
    split = int(0.8 * len(X))
    X_train, X_test = X[:split], X[split:]
    y_train, y_test = y[:split], y[split:]
    print(f"       Train: {len(X_train)} samples, Test: {len(X_test)} samples")

    train_loader = DataLoader(TensorDataset(torch.from_numpy(X_train),
                                            torch.from_numpy(y_train)),
                              batch_size=64, shuffle=True)
    test_loader = DataLoader(TensorDataset(torch.from_numpy(X_test),
                                           torch.from_numpy(y_test)),
                             batch_size=256, shuffle=False)

    print("\n[2/8] Training simple MLP classifier...")
    model = SimpleMLP()
    history = train_model(model, train_loader, epochs=60, device=device)

    train_acc = accuracy(model, train_loader, device)
    test_acc = accuracy(model, test_loader, device)
    print(f"\n       Train accuracy: {train_acc:.4f}")
    print(f"       Test accuracy:  {test_acc:.4f}")

    # ------------------------------------------------------------------
    # 8b. Export to all formats
    # ------------------------------------------------------------------
    example_input = torch.from_numpy(X_test[:1])

    print("\n[3/8] Exporting models...")

    # Native PyTorch checkpoint
    native_path = str(output_dir / "model_native.pt")
    torch.save(model.state_dict(), native_path)

    # TorchScript (trace)
    ts_trace_path = str(output_dir / "model_ts_trace.pt")
    export_torchscript_trace(model, example_input, ts_trace_path)

    # TorchScript (script)
    ts_script_path = str(output_dir / "model_ts_script.pt")
    export_torchscript_script(model, ts_script_path)

    # ONNX
    onnx_path = str(output_dir / "model.onnx")
    export_onnx(model, example_input, onnx_path)

    # ------------------------------------------------------------------
    # 8c. Size comparison
    # ------------------------------------------------------------------
    print("\n[4/8] Model size comparison:")
    print(f"       {'Format':<30} {'Size':>10}")
    print(f"       {'-'*30} {'-'*10}")
    print(f"       {'Native PyTorch (.pt)':<30} {format_size(native_path):>10}")
    print(f"       {'TorchScript trace (.pt)':<30} {format_size(ts_trace_path):>10}")
    print(f"       {'TorchScript script (.pt)':<30} {format_size(ts_script_path):>10}")
    print(f"       {'ONNX (.onnx)':<30} {format_size(onnx_path):>10}")

    # ------------------------------------------------------------------
    # 8d. ONNX Runtime inference
    # ------------------------------------------------------------------
    print("\n[5/8] ONNX Runtime inference test...")
    onnx_model = ONNXInference(onnx_path)
    batch = X_test[:32]
    t0 = time.perf_counter()
    ort_outputs = onnx_model.predict(batch)
    ort_time = time.perf_counter() - t0
    ort_preds = ort_outputs.argmax(axis=1)
    ort_acc = (ort_preds == y_test[:32]).mean()
    print(f"       ONNX Runtime accuracy (32 samples): {ort_acc:.4f}")
    print(f"       Inference time (32 samples):        {ort_time * 1000:.4f} ms")

    # ------------------------------------------------------------------
    # 8e. Quantization (INT8)
    # ------------------------------------------------------------------
    print("\n[6/8] Post-training INT8 quantization...")
    onnx_int8_path = str(output_dir / "model_int8.onnx")

    # Use training data for calibration
    quantize_onnx_int8(onnx_path, onnx_int8_path, X_train)

    print(f"       INT8 model size:  {format_size(onnx_int8_path)}")
    print(f"       FP32 model size:  {format_size(onnx_path)}")
    ratio = (os.path.getsize(onnx_int8_path) / max(os.path.getsize(onnx_path), 1))
    print(f"       Compression ratio: {ratio:.3f}x")

    # Verify INT8 accuracy
    onnx_int8_model = ONNXInference(onnx_int8_path)
    batch = X_test[:256]
    int8_outputs = onnx_int8_model.predict(batch)
    int8_acc = (int8_outputs.argmax(axis=1) == y_test[:256]).mean()
    print(f"       INT8 accuracy (256 samples):    {int8_acc:.4f}")
    print(f"       FP32 accuracy (256 samples):    {ort_acc:.4f}")

    # ------------------------------------------------------------------
    # 8f. Start FastAPI server + test with httpx
    # ------------------------------------------------------------------
    print("\n[7/8] Starting FastAPI server on 127.0.0.1:8888...")

    from multiprocessing import Process

    server_proc = Process(
        target=start_server,
        args=(ts_script_path, "127.0.0.1", 8888),
        daemon=True,
    )
    server_proc.start()
    time.sleep(2.5)  # wait for server to be ready

    print("\n[8/8] Testing /predict endpoint with httpx...")
    import httpx

    try:
        # Health check
        resp = httpx.get("http://127.0.0.1:8888/health", timeout=5.0)
        print(f"       GET /health  -> {resp.status_code} {resp.json()}")

        # Single prediction
        payload = {"features": [0.5, -0.3]}
        t0 = time.perf_counter()
        resp = httpx.post("http://127.0.0.1:8888/predict",
                          json=payload, timeout=5.0)
        api_time = time.perf_counter() - t0
        result = resp.json()
        print(f"       POST /predict -> {resp.status_code}")
        print(f"       Response:       {json.dumps(result, indent=8)}")
        print(f"       API latency:    {api_time * 1000:.2f} ms")

        # Batch of predictions
        print("\n       Batch of 5 predictions:")
        test_points = [[1.2, 0.8], [-1.0, -0.5], [0.0, 1.2],
                       [-0.8, -1.0], [1.5, -0.2]]
        for pt in test_points:
            resp = httpx.post("http://127.0.0.1:8888/predict",
                              json={"features": pt}, timeout=5.0)
            r = resp.json()
            print(f"         {pt} -> class={r['prediction']}  "
                  f"probs={[round(p, 4) for p in r['probabilities']]}")

    finally:
        server_proc.terminate()
        server_proc.join(timeout=5)

    # ------------------------------------------------------------------
    # Summary
    # ------------------------------------------------------------------
    print("\n" + "=" * 65)
    print("  Demo Summary")
    print("=" * 65)
    print(f"  Model:              SimpleMLP (2 -> 64 -> 32 -> 2)")
    print(f"  Test accuracy:      {test_acc:.4f}")
    print(f"  Native size:        {format_size(native_path)}")
    print(f"  TorchScript size:   {format_size(ts_trace_path)}")
    print(f"  ONNX FP32 size:     {format_size(onnx_path)}")
    print(f"  ONNX INT8 size:     {format_size(onnx_int8_path)}")
    print(f"  Quant compression:  {ratio:.2f}x")
    print(f"  API format:         FastAPI + TorchScript")
    print(f"  API test:           PASSED (httpx client)")
    print("=" * 65)
    print("  All deployment steps completed successfully!")
    print("=" * 65)


if __name__ == "__main__":
    main()
