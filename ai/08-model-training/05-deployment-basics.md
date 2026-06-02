# 第5章 模型部署基础 — 从导出到服务化
# Chapter 5: Model Deployment Basics — From Export to Serving

> **训练完模型只是第一步，真正的挑战是如何将它部署到生产环境。** 本章涵盖模型导出（TorchScript / ONNX）、推理服务构建（FastAPI）、量化压缩（INT8 / INT4）以及 Docker 容器化的完整流程。
>
> **Training a model is only the first step; the real challenge is deploying it to production.** This chapter covers the complete pipeline: model export (TorchScript / ONNX), inference service (FastAPI), quantization compression (INT8 / INT4), and Docker containerization.

**前置知识 (Prerequisites):** PyTorch 模型训练, FastAPI 基础
**依赖库 (Dependencies):** `torch >= 2.0.0`, `onnx`, `onnxruntime`, `fastapi`, `uvicorn`, `httpx`

对应代码 (Companion code): `code/serve_model.py`

---

## 目录 (Table of Contents)

1. [模型导出：TorchScript 与 ONNX (Model Export)](#1-模型导出torchscript-与-onnx-model-export)
2. [推理服务：FastAPI (Inference Service)](#2-推理服务fastapi-inference-service)
3. [量化：INT8 / INT4 (Quantization)](#3-量化int8--int4-quantization)
4. [Docker 容器化 (Docker Containerization)](#4-docker-容器化-docker-containerization)
5. [完整示例运行结果 (Full Demo Output)](#5-完整示例运行结果-full-demo-output)

---

## 1. 模型导出：TorchScript 与 ONNX (Model Export)

训练好的 PyTorch 模型不能直接放到生产环境中运行，因为生产环境往往没有 Python 解释器或完整的 PyTorch 库。**模型导出** 将模型序列化为可移植的格式，使其能在 C++ 运行时、移动设备或其它框架中执行。

A trained PyTorch model cannot be dropped directly into production — production environments often lack a Python interpreter or the full PyTorch library. **Model export** serializes the model into a portable format that can run on C++ runtimes, mobile devices, or other frameworks.

### 1.1 TorchScript

TorchScript 是 PyTorch 的中间表示（IR），它将 Python 模型转换为静态可优化的计算图。有两种导出方式：

TorchScript is PyTorch's intermediate representation (IR) that converts Python models into static, optimizable computation graphs. Two export methods exist:

**torch.jit.trace() — 跟踪导出 (Tracing)**

```python
traced = torch.jit.trace(model, example_input)
traced.save("model.pt")
```

`trace()` 用实际输入执行模型，**记录** 所有执行过的操作。适用于**不含数据依赖控制流**的模型（如标准的 CNN、MLP）。

`trace()` executes the model with a real input and **records** all operations that run. Suitable for models **without data-dependent control flow** (standard CNNs, MLPs).

| 优点 (Pros) | 缺点 (Cons) |
|------------|-------------|
| 简单、快速 (Simple, fast) | 不支持动态分支 (No dynamic branches) |
| 结果紧凑 (Compact) | 输入尺寸变化需重新 trace (Input size changes need re-trace) |

**torch.jit.script() — 脚本导出 (Scripting)**

```python
scripted = torch.jit.script(model)
scripted.save("model.pt")
```

`script()` 直接**解析 Python 源码**，支持 `if`、`for`、`while` 等控制流。推荐用于包含动态逻辑的模型。

`script()` directly **parses Python source code** and supports `if`, `for`, `while` control flow. Recommended for models with dynamic logic.

### 1.2 ONNX (Open Neural Network Exchange)

ONNX 是一种**跨框架**的模型格式标准。导出的 ONNX 模型可以在 PyTorch、TensorFlow、TensorRT 甚至专用硬件上运行。

ONNX is a **cross-framework** model format standard. Exported ONNX models can run on PyTorch, TensorFlow, TensorRT, or specialized hardware.

```python
torch.onnx.export(
    model,
    example_input,
    "model.onnx",
    input_names=["input"],
    output_names=["output"],
    dynamic_axes={"input": {0: "batch_size"}},
    opset_version=18,
)
```

关键参数 (Key arguments):

| 参数 (Argument) | 作用 (Purpose) |
|----------------|---------------|
| `dynamic_axes` | 允许动态 batch 大小 (Allow dynamic batch size) |
| `opset_version` | ONNX 算子集版本 (ONNX operator set version) |
| `input_names` / `output_names` | 输入输出张量命名 (Name tensors for runtime lookup) |

### 1.3 格式对比 (Format Comparison)

| 格式 (Format) | 文件大小 (Size) | 运行时 (Runtime) | 适用场景 (Use case) |
|--------------|----------------|-----------------|-------------------|
| `.pt` (Native) | 12.20 KB | PyTorch | 训练 / 研究 (Training / Research) |
| `.pt` (TorchScript) | 20.53 KB | LibTorch (C++) / PyTorch | C++ 部署、移动端 (C++ deployment, mobile) |
| `.onnx` | 8.43 KB | ONNX Runtime / TensorRT / ... | 跨框架 / 边缘设备 (Cross-framework / Edge) |

> 💡 **为什么需要导出？** 生产环境不需要完整的 PyTorch 安装（数百 MB）。ONNX Runtime 只有几十 MB，且支持 C、Python、Java、C# 等多种语言接口。
>
> **Why export?** Production doesn't need the full PyTorch installation (hundreds of MB). ONNX Runtime is only tens of MB and supports C, Python, Java, C# interfaces.

---

## 2. 推理服务：FastAPI (Inference Service)

模型导出后需要暴露为 HTTP API。FastAPI 是构建 ML 推理服务的首选框架，因为它原生支持异步、Pydantic 验证和自动文档。

After export, the model needs to be exposed as an HTTP API. FastAPI is the go-to framework for ML inference services thanks to native async support, Pydantic validation, and auto-generated docs.

### 2.1 端点设计 (Endpoint Design)

```
POST /predict  — 模型推理 (Model inference)
GET  /health   — 健康检查 (Health check)
```

### 2.2 请求 / 响应模型 (Request/Response Model)

```python
from pydantic import BaseModel, Field

class PredictRequest(BaseModel):
    features: List[float] = Field(..., min_length=2, max_length=2)

class PredictResponse(BaseModel):
    prediction: int
    probabilities: List[float]
    model_format: str
```

Pydantic 自动完成类型校验和 JSON 解析，无需手写验证逻辑。

Pydantic handles type validation and JSON parsing automatically — no manual validation code needed.

### 2.3 异步处理 & 批推理 (Async & Batch Inference)

对于高吞吐场景，可以收集多个请求合并为一个 batch：

For high-throughput scenarios, collect multiple requests and merge into one batch:

```python
@app.post("/predict_batch")
async def predict_batch(reqs: List[PredictRequest]):
    inputs = np.array([r.features for r in reqs], dtype=np.float32)
    outputs = model(torch.from_numpy(inputs))
    preds = outputs.argmax(dim=1).tolist()
    return {"predictions": preds}
```

### 2.4 负载测试 (Load Testing)

使用 `locust` 或 `httpx` 进行简单测试 (Simple load test with httpx):

```python
# Sequential test
for _ in range(100):
    resp = httpx.post("http://localhost:8888/predict",
                      json={"features": [0.5, -0.3]})
    assert resp.status_code == 200
```

### 2.5 日志记录 (Request Logging)

在 FastAPI 中添加 middleware 记录推理请求的耗时、输入、输出：

Add middleware to log inference latency, inputs, and outputs:

```python
@app.middleware("http")
async def log_requests(request, call_next):
    t0 = time.perf_counter()
    response = await call_next(request)
    latency = time.perf_counter() - t0
    logger.info(f"{request.url.path} {latency*1000:.2f}ms")
    return response
```

---

## 3. 量化：INT8 / INT4 (Quantization)

量化是将模型权重和激活值从 FP32 降低到更低精度（INT8、INT4）的过程，以减少模型大小和推理延迟。

Quantization reduces model weights and activations from FP32 to lower precision (INT8, INT4) to shrink model size and reduce inference latency.

### 3.1 训练后量化 PTQ (Post-Training Quantization)

PTQ 是最简单的量化方式：用少量校准数据统计激活值的范围，然后将 FP32 映射到 INT8。

PTQ is the simplest approach: use a small calibration dataset to estimate activation ranges, then map FP32 values to INT8.

```python
from onnxruntime.quantization import quantize_static, QuantType

quantize_static(
    model_input="model.onnx",
    model_output="model_int8.onnx",
    calibration_data_reader=calib_loader,
    weight_type=QuantType.QInt8,
    activation_type=QuantType.QInt8,
)
```

**实际效果 (Actual result from demo):**

| 指标 (Metric) | FP32 | INT8 | 变化 (Change) |
|--------------|------|------|--------------|
| 模型大小 (Model size) | 8.43 KB | 6.46 KB | **-23%** |
| 推理精度 (Accuracy) | 1.0000 | 1.0000 | 无损失 (No loss) |

> 注意：本例模型较小，INT8 压缩比不显著。实际大模型（如 ResNet-50）通常可以获得 **4 倍** 的压缩。
>
> Note: Our small model shows modest compression; real models (e.g., ResNet-50) typically achieve **4x** compression.

### 3.2 PTQ vs QAT (Quantization-Aware Training)

| 方法 (Method) | 是否需要重训练 (Re-train?) | 精度 (Accuracy) | 工作难度 (Effort) |
|--------------|--------------------------|-----------------|------------------|
| PTQ | ❌ 否 (No) | 小损失 (Small loss) | ⭐ 低 (Low) |
| QAT | ✅ 需要模拟量化训练 (Simulate quant in training) | 几乎无损 (Near lossless) | ⭐⭐⭐ 高 (High) |

**QAT 原理：** 在训练过程中插入伪量化节点（`torch.quantization.FakeQuantize`），让模型学习适应低精度表示的权重分布。

**QAT principle:** Insert fake quantization nodes (`torch.quantization.FakeQuantize`) during training so the model learns weight distributions robust to low-precision representation.

### 3.3 INT4 量化：GPTQ / AWQ

对于 7B+ 参数的大语言模型，INT8 仍然太大。INT4 量化可以进一步将模型压缩到原来的 **1/4**。

For 7B+ parameter LLMs, INT8 is still too large. INT4 quantization further compresses to **1/4** of the original size.

| 方法 (Method) | 特点 (Characteristics) | 适用模型 (Suitable for) |
|-------------|----------------------|----------------------|
| **GPTQ** | 基于 Hessian 矩阵的逐层量化 (Layer-wise, Hessian-based) | 7B-70B LLM |
| **AWQ** | 基于激活值感知的权重裁剪 (Activation-aware weight clipping) | 7B-70B LLM |
| **GGML/GGUF** | K-quant 混合精度 (Mixed-precision K-quant) | CPU 推理 (CPU inference) |

```python
# GPTQ 示例 (使用 auto_gptq 库)
from auto_gptq import AutoGPTQForCausalLM

model = AutoGPTQForCausalLM.from_pretrained("model", quantize_config=...)
model.quantize(tokenizer, calibration_dataset)
```

### 3.4 精度-大小权衡曲线 (Accuracy-Size Tradeoff)

```
精度 (Accuracy)
 1.0 | FP32
     |  ●──● INT8 (PTQ)
     |     └──● INT8 (QAT)
     |        └──● INT4 (GPTQ/AWQ)
 0.9 |              └──● INT4 (naive)
     |
     +──────────────────────────
        原始    1/2    1/4   模型大小 (Model size)
```

---

## 4. Docker 容器化 (Docker Containerization)

将推理服务打包为 Docker 镜像，确保环境一致性。

Package the inference service as a Docker image to ensure environment consistency.

### 4.1 Dockerfile 最佳实践 (Best Practices)

```dockerfile
# === Stage 1: Build (multi-stage build) ===
FROM python:3.11-slim AS builder

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# === Stage 2: Runtime ===
FROM python:3.11-slim

# 创建非 root 用户 (Create non-root user)
RUN groupadd -r ml && useradd -r -g ml -d /app ml

WORKDIR /app
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY serve_model.py /app/
COPY output/model_ts_script.pt /app/model.pt

# 健康检查 (Health check)
HEALTHCHECK --interval=30s --timeout=5s \
  CMD python -c "import httpx; httpx.get('http://localhost:8888/health').raise_for_status()"

# 非 root 用户运行 (Run as non-root)
USER ml

EXPOSE 8888
CMD ["uvicorn", "serve_model:app", "--host", "0.0.0.0", "--port", "8888"]
```

### 4.2 构建与运行 (Build & Run)

```bash
docker build -t ml-server:latest .
docker run -d --name ml-api -p 8888:8888 ml-server:latest
docker logs -f ml-api
```

### 4.3 设计原则 (Design Principles)

| 原则 (Principle) | 说明 (Explanation) |
|-----------------|-------------------|
| **最小基础镜像 (Minimal base image)** | `slim` / `alpine` 比 `full` 小 5-10 倍 (5-10x smaller than `full`) |
| **多阶段构建 (Multi-stage build)** | 构建时依赖不进入最终镜像 (Build deps don't enter final image) |
| **非 root 用户 (Non-root user)** | 安全最佳实践，防止容器逃逸 (Security best practice, prevent container escape) |
| **HEALTHCHECK** | 让编排系统（K8s）自动检测服务健康 (Let orchestrators detect service health) |
| **固定版本标签 (Pin versions)** | 确保可复现构建 (Ensure reproducible builds) |

---

## 5. 完整示例运行结果 (Full Demo Output)

以下为运行 `code/serve_model.py` 的实际输出：

Below is the actual console output from running `code/serve_model.py`:

```
=================================================================
  ML Model Deployment Pipeline Demo
=================================================================

[1/8] Generating synthetic data (two moons)...
       Train: 1600 samples, Test: 400 samples

[2/8] Training simple MLP classifier...
  Epoch   1/60  loss=0.072022
  Epoch  20/60  loss=0.000004
  Epoch  60/60  loss=0.000001

       Train accuracy: 1.0000
       Test accuracy:  1.0000

[3/8] Exporting models...

[4/8] Model size comparison:
       Format                               Size
       ------------------------------ ----------
       Native PyTorch (.pt)             12.20 KB
       TorchScript trace (.pt)          20.53 KB
       TorchScript script (.pt)         20.44 KB
       ONNX (.onnx)                      8.43 KB

[5/8] ONNX Runtime inference test...
       ONNX Runtime accuracy (32 samples): 1.0000
       Inference time (32 samples):        0.4504 ms

[6/8] Post-training INT8 quantization...
       INT8 model size:  6.46 KB
       FP32 model size:  8.43 KB
       Compression ratio: 0.766x
       INT8 accuracy (256 samples):    1.0000
       FP32 accuracy (256 samples):    1.0000

[7/8] Starting FastAPI server on 127.0.0.1:8888...

[8/8] Testing /predict endpoint with httpx...
       GET /health  -> 200 {'status': 'ok', 'model_loaded': True}
       POST /predict -> 200
       Response:       {
        "prediction": 1,
        "probabilities": [0.3514, 0.6486],
        "model_format": "TorchScript"
       }
       API latency:    143.16 ms

       Batch of 5 predictions:
         [1.2, 0.8] -> class=1  probs=[0.0, 1.0]
         [-1.0, -0.5] -> class=0  probs=[1.0, 0.0]
         [0.0, 1.2] -> class=1  probs=[0.0, 1.0]
         [-0.8, -1.0] -> class=0  probs=[1.0, 0.0]
         [1.5, -0.2] -> class=1  probs=[0.0, 1.0]

=================================================================
  Demo Summary
=================================================================
  Model:              SimpleMLP (2 -> 64 -> 32 -> 2)
  Test accuracy:      1.0000
  Native size:        12.20 KB
  TorchScript size:   20.53 KB
  ONNX FP32 size:     8.43 KB
  ONNX INT8 size:     6.46 KB
  Quant compression:  0.77x
  API format:         FastAPI + TorchScript
  API test:           PASSED (httpx client)
=================================================================
  All deployment steps completed successfully!
=================================================================
```

---

## 本章总结 (Chapter Summary)

- **模型导出**：TorchScript（`trace` 与 `script`）适用于 PyTorch 原生部署；ONNX 提供跨框架互操作性。
- **推理服务**：FastAPI + Pydantic 提供类型安全的 HTTP API，支持异步、批推理和自动文档。
- **量化**：PTQ 是最简单的 INT8 方案；QAT 提供更高精度；INT4（GPTQ/AWQ）用于大模型压缩。
- **容器化**：多阶段构建 + 最小基础镜像 + 非 root 用户是最佳实践。

- **Model Export**: TorchScript (`trace` vs `script`) for native PyTorch deployment; ONNX for cross-framework interoperability.
- **Inference Service**: FastAPI + Pydantic provides type-safe HTTP APIs with async, batch inference, and auto-docs.
- **Quantization**: PTQ is the simplest INT8 approach; QAT offers higher accuracy; INT4 (GPTQ/AWQ) for large model compression.
- **Containerization**: Multi-stage build + minimal base image + non-root user are best practices.
