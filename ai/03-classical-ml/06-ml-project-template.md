# 第6章 ML项目模板 — 可复用的机器学习管道
# Chapter 6: ML Project Template — A Reusable Machine Learning Pipeline

> **在真实项目中，ML 工作流不仅仅是训练一个模型。** 你需要加载数据、清理特征、划分数据集、尝试多种模型、评估效果、保存最佳模型，最后还要能加载它进行推理（inference /ˈɪnfərəns/）。将这些步骤组织成可复用的管道，是每个 ML 工程师的核（kernel /ˈkɜːrnl/）心能力。
>
> **In real projects, ML workflows go far beyond just training a model.** You need to load data, clean features, split datasets, try multiple models, evaluate performance, save the best model, and finally load it for inference. Organizing these steps into a reusable pipeline is a core skill for every ML engineer.

**前置知识 (Prerequisites):** Python 基础，scikit-learn 基本用法
**依赖库 (Dependencies):** `numpy`, `pandas`, `scikit-learn`, `matplotlib`, `joblib`
**Code companion:** [`code/ml_project_template.py`](code/ml_project_template.py)

---

## 目录 (Table of Contents)

1. [为什么需要 ML 管道模板？](#1-为什么需要-ml-管道模板-why-a-ml-pipeline-template)
2. [模块概览](#2-模块概览-module-overview)
3. [函数详解](#3-函数详解-function-details)
   - [3.1 load_data()](#31-load_data-数据加载)
   - [3.2 Preprocessor 类与 preprocess_pipeline()](#32-preprocessor-类与-preprocess_pipeline-预处理)
   - [3.3 split_data()](#33-split_data-数据划分)
   - [3.4 train_model()](#34-train_model-模型训练)
   - [3.5 evaluate_model()](#35-evaluate_model-模型评估)
   - [3.6 save_model()](#36-save_model-模型保存)
   - [3.7 load_and_predict()](#37-load_and_predict-加载与推理)
4. [端到端示例](#4-端到端示例-end-to-end-example)
5. [如何自定义](#5-如何自定义-how-to-customize)
6. [小结](#6-小结-summary)

---

## 1. 为什么需要 ML 管道模板？ (Why a ML Pipeline Template?)

任何 ML 项目都遵循几个固定步骤。如果没有标准化模板，你可能会：

**Without a standardized template, you might:**

- 🌀 在每个新项目中重复编写相同的样板代码 (Rewrite the same boilerplate in every project)
- 🐛 忘记处理缺失值或特征缩放 (Forget to handle missing values or scaling)
- 📊 评估指标不统一，难以横向比较模型 (Inconsistent metrics across models)
- 💾 模型保存格式混乱，部署时找不到正确的预处理器 (Chaotic model saving, missing preprocessor at deployment)

**这个模板解决什么问题？(What this template solves):**

| 问题 (Problem) | 解决方案 (Solution) |
|---|---|
| 重复代码 | 7 个函数覆盖完整 ML 生命周期 |
| 预处理不一致 | `Preprocessor` 类统一管理 fit/transform |
| 模型选择困难 | 可插拔模型注册表，一键切换 |
| 评估不全面 | 自动输出指标 + 可视化图表 |
| 部署断层 | 模型 + 预处理器 + 元数据一起保存 |

---

## 2. 模块概览 (Module Overview)

```
┌─────────────────────────────────────────────────────────┐
│                   ML Pipeline Template                    │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  load_data()         ────  数据加载 (CSV / sklearn)      │
│       │                                                   │
│  split_data()        ────  分层划分 train/val/test       │
│       │                                                   │
│  Preprocessor        ────  缺失值填充 + 缩放 + 编码      │
│  ├─ fit_transform()                                       │
│  └─ transform()                                           │
│       │                                                   │
│  train_model()       ────  可插拔模型训练                 │
│       │                                                   │
│  evaluate_model()    ────  指标 + 混淆矩阵 / ROC / 残差  │
│       │                                                   │
│  save_model()        ────  joblib 持久化                  │
│       │                                                   │
│  load_and_predict()  ────  加载模型并推理                 │
│                                                          │
└─────────────────────────────────────────────────────────┘
```

---

## 3. 函数详解 (Function Details)

### 3.1 `load_data()` — 数据加载

```python
def load_data(
    source: Union[str, Path, None] = None,
    dataset_name: str = "iris",
    ...
) -> Tuple[np.ndarray, np.ndarray, pd.DataFrame, str]:
```

**功能 (Purpose):**
提供统一的入口来加载数据，无论是本地 CSV 文件还是 sklearn 内置数据集。

**参数（parameter /pəˈræmɪtər/）说明 (Parameters):**

| 参数 | 类型 | 说明 |
|---|---|---|
| `source` | `str` or `None` | CSV 文件路径（为 None 时使用 sklearn 数据集） |
| `dataset_name` | `str` | sklearn 数据集名称: `iris`, `breast_cancer`, `wine`, `digits`, `diabetes` |

**自动检测任务类型 (Auto-detect task type):**
- 如果目标列是整数且类别 < 20 → `classification`
- 否则 → `regression`

**自定义 CSV 格式 (Custom CSV format):**
CSV 文件的**最后一列**被视为目标变量 y，其余列作为特征 X。

```python
# 从 sklearn 数据集加载 (From sklearn)
X, y, features, task = load_data(dataset_name="breast_cancer")

# 从 CSV 加载 (From CSV)
X, y, features, task = load_data(source="my_data.csv")
```

---

### 3.2 `Preprocessor` 类与 `preprocess_pipeline()` — 预处理

```python
class Preprocessor:
    def __init__(self, impute_strategy="mean", scale=True):
        ...

    def fit(self, X, y=None) -> "Preprocessor":
        ...

    def transform(self, X, y=None) -> Union[np.ndarray, Tuple]:
        ...

pre = Preprocessor()
X_train_proc = pre.fit_transform(X_train, y_train)
X_test_proc  = pre.transform(X_test)     # 只用 transform！
```

**为什么 Preprocessor 需要 fit/transform 分离？**
**Why separate fit and transform?**

这是 ML 中最重要的原则之一——**永远不要用测试集的信息来转换训练集**。

- `fit()` — 在**训练集**上计算均值、标准差等统计量
- `transform()` — 将这些统计量应用到训练集或测试集

**预处理三大件 (Three Preprocessing Steps):**

| 组件 | 方法 | 说明 |
|---|---|---|
| `SimpleImputer` | `impute_strategy` | 处理缺失值 ('mean', 'median', 'most_frequent') |
| `StandardScaler` | `scale` | Z-score 标准化 (均值为0，方差为1) |
| `LabelEncoder` | 自动 | 将分类（classification /ˌklæsɪfɪˈkeɪʃən/）标签编码为整数 |

**便捷函数 (Convenience Function):**

```python
X_train_p, X_test_p, y_train, y_test, pre = preprocess_pipeline(
    X_train, X_test, y_train, y_test
)
```

---

### 3.3 `split_data()` — 数据划分

```python
def split_data(
    X, y,
    task_type="classification",
    train_size=0.7, val_size=0.15, test_size=0.15,
    stratify=True,
) -> Tuple[X_train, X_val, X_test, y_train, y_val, y_test]:
```

**分层策略 (Stratification Strategy):**

- **分类任务 (Classification):** 按标签比例分层，确保每个子集的类别分布与原始数据一致
- **回归（regression /rɪˈɡreʃən/）任务 (Regression):** 使用 `pd.qcut()` 将目标值分桶后按桶分层

**为什么需要验证集？(Why a Validation Set?)**

| 数据集 | 用途 |
|---|---|
| **训练集 (Train)** | 模型学习参数 |
| **验证集 (Validation)** | 模型选择、超参数（hyperparameter /ˈhaɪpərpəˈræmɪtər/）调优、早停 |
| **测试集 (Test)** | 最终评估，**只在最后一刻使用一次** |

```python
X_tr, X_val, X_te, y_tr, y_val, y_te = split_data(X, y)
```

---

### 3.4 `train_model()` — 模型训练

```python
def train_model(
    X_train, y_train,
    task_type="classification",
    model_type="logistic",
    model_params=None,
    model=None,
    X_val=None, y_val=None,
) -> BaseEstimator:
```

**可插拔设计 (Pluggable Design):**

分类模型注册表 (`CLASSIFICATION_MODELS`):
| 键 (Key) | 模型 (Model) |
|---|---|
| `logistic` | LogisticRegression |
| `decision_tree` | DecisionTreeClassifier |
| `random_forest` | RandomForestClassifier |
| `svm` | SVC (with probability=True) |
| `gradient_boosting` | GradientBoostingClassifier |

回归模型注册表 (`REGRESSION_MODELS`):
| 键 (Key) | 模型 (Model) |
|---|---|
| `decision_tree` | DecisionTreeRegressor |
| `random_forest` | RandomForestRegressor |
| `svm` | SVR |
| `gradient_boosting` | GradientBoostingRegressor |

**三种使用方式 (Three Usage Modes):**

```python
# 1. 从注册表选择 (From registry)
model = train_model(X, y, model_type="random_forest")

# 2. 传入自定义参数 (With custom params)
model = train_model(X, y, model_type="random_forest",
                    model_params={"n_estimators": 200, "max_depth": 10})

# 3. 传入自定义模型 (Custom model)
from xgboost import XGBClassifier
custom = XGBClassifier(n_estimators=100)
model = train_model(X, y, model=custom)
```

---

### 3.5 `evaluate_model()` — 模型评估

```python
def evaluate_model(
    model, X_test, y_test,
    task_type="classification",
    class_names=None,
    model_name="model",
    save_plot=True,
) -> Dict[str, float]:
```

**分类任务输出 (Classification Outputs):**

| 指标 (Metric) | 说明 |
|---|---|
| `accuracy` | 准确率 |
| `precision` | 精确率 (weighted) |
| `recall` | 召回率 (weighted) |
| `f1` | F1 分数 (weighted) |
| `roc_auc` | ROC-AUC (仅二分类) |

**回归任务输出 (Regression Outputs):**

| 指标 (Metric) | 说明 |
|---|---|
| `mse` | 均方误差 |
| `rmse` | 均方根误差 |
| `mae` | 平均绝对误差 |
| `r2` | R² 决定系数 |

**自动生成的可视化 (Auto-generated Plots):**

- **分类 (Classification):** 混淆矩阵热力图 + ROC 曲线 (二分类)
- **回归 (Regression):** 预测 vs 真实散点图 + 残差图

```python
metrics = evaluate_model(model, X_test, y_test, task_type="classification",
                         class_names=["cat", "dog"], model_name="my_model")
print(f"Accuracy: {metrics['accuracy']:.4f}")
```

---

### 3.6 `save_model()` — 模型保存

```python
def save_model(
    model, path,
    preprocessor=None,
    metadata=None,
) -> Path:
```

**保存的内容 (What Gets Saved):**

```
my_model.joblib
├── model          ← 训练好的模型
├── preprocessor   ← 拟合好的预处理器 (重要！)
└── metadata       ← 数据集名称、评估指标、特征名等
```

**为什么预处理器必须和模型一起保存？**
**Why save the preprocessor with the model?**

如果在训练时使用了标准化 (`StandardScaler`)，推理时的新数据必须使用**相同的均值和标准差**进行转换。如果预处理器没有和模型一起保存，部署时就需要重新拟合，导致预测结果不一致。

```python
save_model(model, "models/iris_rf.joblib",
           preprocessor=pre,
           metadata={"dataset": "iris", "accuracy": 0.97})
```

---

### 3.7 `load_and_predict()` — 加载与推理

```python
def load_and_predict(
    model_path, X_new,
    return_proba=False,
) -> Union[np.ndarray, Tuple[np.ndarray, Optional[np.ndarray]]]:
```

**自动加载预处理器 (Auto-loads Preprocessor):**
如果保存时包含了预处理器，`load_and_predict()` 会自动对新数据进行转换，无需手动处理。

```python
# 推理 (Inference)
y_pred = load_and_predict("models/iris_rf.joblib", X_new)

# 同时获取概率 (With probabilities)
y_pred, y_prob = load_and_predict("models/iris_rf.joblib", X_new, return_proba=True)
```

---

## 4. 端到端示例 (End-to-End Example)

完整示例在 [`code/ml_project_template.py`](code/ml_project_template.py) 的 `run_demo()` 函数中。以下是运行结果预览：

```python
python code/ml_project_template.py
```

输出示例 (Expected Output):

```
============================================================
ML Project Template — End-to-End Demo
============================================================

[1/6] Loading data...
Loaded dataset: iris  |  Samples: 150, Features: 4  |  Task: classification
  Features (4): ['sepal length (cm)', 'sepal width (cm)', ...]

[2/6] Splitting data...
Data split complete: train=105, val=22, test=23

[3/6] Preprocessing...

[4/6] Training models...
Training LogisticRegression...
  → logistic: val_acc = 0.9545
Training DecisionTreeClassifier...
  → decision_tree: val_acc = 0.9545
Training RandomForestClassifier...
  → random_forest: val_acc = 0.9545

  Best model: logistic (val_acc = 0.9545)

[5/6] Evaluating best model (logistic) on test set...

=== Classification Report (iris_logistic) ===
              precision    recall  f1-score   support
      setosa       1.00      1.00      1.00         8
  versicolor       1.00      1.00      1.00         8
   virginica       1.00      1.00      1.00         7

    accuracy                           1.00        23
   macro avg       1.00      1.00      1.00        23
weighted avg       1.00      1.00      1.00        23

  Test accuracy: 1.0000
  Test F1 score: 1.0000

[6/6] Saving and reloading model...
Model saved: .../output/iris_logistic.joblib (2.3 KB)

  → Inference on 5 random test samples:
    [✓] True: 0, Predicted: 0
    [✓] True: 2, Predicted: 2
    [✓] True: 1, Predicted: 1
    [✓] True: 0, Predicted: 0
    [✓] True: 1, Predicted: 1

============================================================
Demo complete! All pipeline steps verified successfully.
============================================================
```

**使用自己的数据 (Using Your Own Data):**

```python
# 1. 加载自己的 CSV (Load your CSV)
X, y, features, task = load_data(source="my_dataset.csv")

# 2. 划分数据 (Split)
X_tr, X_val, X_te, y_tr, y_val, y_te = split_data(X, y, task_type=task)

# 3. 预处理 (Preprocess)
X_tr, X_te, y_tr, y_te, pre = preprocess_pipeline(X_tr, X_te, y_tr, y_te)

# 4. 训练并选择最佳模型 (Train & select best)
for name in ["logistic", "random_forest", "svm"]:
    model = train_model(X_tr, y_tr, task, name, X_val=X_val, y_val=y_val)

# 5. 评估最佳模型 (Evaluate best)
metrics = evaluate_model(best_model, X_te, y_te, task)

# 6. 保存 (Save)
save_model(best_model, "model.joblib", preprocessor=pre, metadata=metrics)
```

---

## 5. 如何自定义 (How to Customize)

### 添加新模型 (Add a New Model)

```python
from sklearn.naive_bayes import GaussianNB

# 注册到模型字典 (Register in the dictionary)
CLASSIFICATION_MODELS["naive_bayes"] = GaussianNB()

# 然后就可以直接使用 (Then use directly)
model = train_model(X, y, model_type="naive_bayes")
```

### 扩展预处理器 (Extend the Preprocessor)

```python
class MyPreprocessor(Preprocessor):
    def transform(self, X, y=None):
        X = super().transform(X, y)
        # 添加自定义特征工程 (Add custom feature engineering)
        if hasattr(self, 'poly_features'):
            X = self.poly_features.transform(X)
        return X
```

### 自定义评估指标 (Custom Metrics)

`evaluate_model()` 返回的是一个字典，你可以轻松地扩展它：

```python
metrics = evaluate_model(model, X_test, y_test)
metrics["custom_metric"] = my_custom_function(y_test, y_pred)
```

### 支持更多数据格式 (Support More Data Formats)

可以扩展 `load_data()` 来支持 Parquet、Excel、JSON 等格式：

```python
if source.endswith(".parquet"):
    df = pd.read_parquet(source)
elif source.endswith(".xlsx"):
    df = pd.read_excel(source)
```

---

## 6. 小结 (Summary)

**这个模板提供了什么？(What This Template Provides):**

| 步骤 (Step) | 函数 (Function) | 核心价值 (Value) |
|---|---|---|
| 数据加载 | `load_data()` | 统一接口，支持 CSV 和内置数据集 |
| 划分 | `split_data()` | 三层划分 + 分层抽样 |
| 预处理 | `Preprocessor` | fit/transform 分离，防止数据泄露 |
| 训练 | `train_model()` | 可插拔模型，一键切换 |
| 评估 | `evaluate_model()` | 完整指标 + 可视化 |
| 保存 | `save_model()` | 模型 + 预处理器 + 元数据打包 |
| 推理 | `load_and_predict()` | 开箱即用的预测函数 |

**关键设计原则 (Key Design Principles):**

1. **fit/transform 分离** — 防止数据泄露 (Prevent data leakage)
2. **模型注册表** — 添加新模型无需修改管道代码 (Pluggable models)
3. **打包保存** — 模型和预处理器永不分离 (Bundle model + preprocessor)
4. **自动类型检测** — 分类/回归自适应 (Auto-detect task type)

这个模板是一个**起点**。随着项目复杂度增加，你可以在此基础上添加交叉验证、超参数搜索、特征选择、实验跟踪等功能。但最基本、最常用的 7 个步骤已经在这里了，直接复制、粘贴、修改即可。

> **This template is a starting point.** As your projects grow, you can add cross-validation, hyperparameter search, feature selection, experiment tracking, and more on top of it. But the core 7 steps are here — ready to copy, paste, and adapt.

<!-- 演算盒审查完成: 无需 -->
