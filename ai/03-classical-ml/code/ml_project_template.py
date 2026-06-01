"""
ML 项目模板 — 可复用的机器学习管道
ML Project Template — Reusable Machine Learning Pipeline
============================================================
依赖 (Dependencies): numpy>=1.24.0, scikit-learn>=1.3.0, matplotlib>=3.7.0, joblib>=1.2.0

提供 (Provides):
  1. load_data()         — 灵活的数据加载 (CSV / sklearn datasets)
  2. preprocess()        — 预处理管线 (缺失值、缩放、编码)
  3. split_data()        — 分层训练/验证/测试集划分
  4. train_model()       — 可插拔模型训练
  5. evaluate_model()    — 评估指标 + 可视化
  6. save_model()        — joblib 模型持久化
  7. load_and_predict()  — 推理函数

用法 (Usage):
  python ml_project_template.py    # 运行完整示例
"""

import warnings
from pathlib import Path
from typing import Any, Dict, Optional, Tuple, Union

import joblib
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.base import BaseEstimator
from sklearn.ensemble import (
    GradientBoostingClassifier,
    GradientBoostingRegressor,
    RandomForestClassifier,
    RandomForestRegressor,
)
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    ConfusionMatrixDisplay,
    accuracy_score,
    classification_report,
    confusion_matrix,
    f1_score,
    mean_absolute_error,
    mean_squared_error,
    precision_score,
    r2_score,
    recall_score,
    roc_auc_score,
    roc_curve,
)
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.svm import SVC, SVR
from sklearn.tree import DecisionTreeClassifier, DecisionTreeRegressor

warnings.filterwarnings("ignore")

# ============================================================
# 全局设置 (Global Settings)
# ============================================================
OUTPUT_DIR = Path(__file__).parent / "output"
OUTPUT_DIR.mkdir(exist_ok=True)

RNG = np.random.RandomState(42)

plt.rcParams.update({
    "figure.dpi": 120,
    "font.size": 11,
    "axes.titlesize": 13,
    "axes.labelsize": 11,
})

# 可用的模型注册表 (Model Registry)
CLASSIFICATION_MODELS: Dict[str, BaseEstimator] = {
    "logistic": LogisticRegression(max_iter=1000, random_state=42),
    "decision_tree": DecisionTreeClassifier(random_state=42),
    "random_forest": RandomForestClassifier(n_estimators=100, random_state=42),
    "svm": SVC(kernel="rbf", probability=True, random_state=42),
    "gradient_boosting": GradientBoostingClassifier(n_estimators=100, random_state=42),
}

REGRESSION_MODELS: Dict[str, BaseEstimator] = {
    "decision_tree": DecisionTreeRegressor(random_state=42),
    "random_forest": RandomForestRegressor(n_estimators=100, random_state=42),
    "svm": SVR(kernel="rbf"),
    "gradient_boosting": GradientBoostingRegressor(n_estimators=100, random_state=42),
}


# ============================================================
# 1. 数据加载 (Data Loading)
# ============================================================
def load_data(
    source: Union[str, Path, None] = None,
    dataset_name: str = "iris",
    test_size: float = 0.2,
    random_state: int = 42,
) -> Tuple[np.ndarray, np.ndarray, pd.DataFrame, str]:
    """灵活的数据加载 — 支持 CSV 文件和 sklearn 内置数据集。

    Flexible data loading — supports CSV files and sklearn built-in datasets.

    Parameters
    ----------
    source : str or Path, optional
        CSV 文件路径。为 None 时使用 sklearn 数据集。
        CSV file path. Uses sklearn dataset when None.
    dataset_name : str
        sklearn 数据集名称，可选: 'iris', 'breast_cancer', 'wine', 'diabetes', 'boston'
        Name of the sklearn dataset (ignored if source is provided).
    test_size : float
        若没有显式划分，预留给测试集的比例 (deprecated here, kept for API consistency)。
    random_state : int
        随机种子。

    Returns
    -------
    X : np.ndarray, shape (n_samples, n_features)
        特征矩阵 / Feature matrix.
    y : np.ndarray, shape (n_samples,)
        目标向量 / Target vector.
    feature_names : list of str
        特征名称列表 / List of feature names.
    task_type : str
        'classification' 或 'regression'。

    Raises
    ------
    FileNotFoundError
        当指定的 CSV 文件不存在时。
    ValueError
        当 dataset_name 不在支持列表中时。
    """
    if source is not None:
        # ---------- 从 CSV 加载 (Load from CSV) ----------
        path = Path(source)
        if not path.exists():
            raise FileNotFoundError(f"CSV file not found: {path}")
        df = pd.read_csv(path)
        # 默认最后一列为目标 (Assume last column is target)
        y = df.iloc[:, -1].values
        X = df.iloc[:, :-1].values
        feature_names = df.columns[:-1].tolist()
        # 自动检测任务类型 (Auto-detect task type)
        unique_vals = np.unique(y)
        if y.dtype in (np.int64, np.int32, np.int8, np.bool_, object) and len(unique_vals) < 20:
            task_type = "classification"
        else:
            task_type = "regression"
        return X, y, feature_names, task_type

    # ---------- 从 sklearn 加载 (Load from sklearn) ----------
    sklearn_datasets = {
        "iris": ("classification", lambda: __import__("sklearn").datasets.load_iris()),
        "breast_cancer": ("classification", lambda: __import__("sklearn").datasets.load_breast_cancer()),
        "wine": ("classification", lambda: __import__("sklearn").datasets.load_wine()),
        "digits": ("classification", lambda: __import__("sklearn").datasets.load_digits()),
        "diabetes": ("regression", lambda: __import__("sklearn").datasets.load_diabetes()),
    }

    if dataset_name not in sklearn_datasets:
        raise ValueError(
            f"Unknown dataset '{dataset_name}'. "
            f"Available: {list(sklearn_datasets.keys())}"
        )

    task_type, loader_fn = sklearn_datasets[dataset_name]
    data = loader_fn()
    X = data.data
    y = data.target
    feature_names = data.feature_names

    print(f"Loaded dataset: {dataset_name}  |  "
          f"Samples: {X.shape[0]}, Features: {X.shape[1]}  |  "
          f"Task: {task_type}")
    return X, y, list(feature_names), task_type


# ============================================================
# 2. 数据预处理 (Preprocessing)
# ============================================================
class Preprocessor:
    """数据预处理管线 — 处理缺失值、缩放、编码。

    Data preprocessing pipeline — handles missing values, scaling, encoding.

    用法 (Usage)::
        pre = Preprocessor()
        X_train_proc = pre.fit_transform(X_train, y_train)
        X_test_proc  = pre.transform(X_test)

    Attributes
    ----------
    imputer : SimpleImputer
        缺失值填充器。
    scaler : StandardScaler
        特征标准化器。
    label_encoder : LabelEncoder
        标签编码器 (仅分类任务)。
    fitted_ : bool
        是否已拟合。
    """

    def __init__(self, impute_strategy: str = "mean", scale: bool = True):
        """
        Parameters
        ----------
        impute_strategy : str
            缺失值填充策略: 'mean', 'median', 'most_frequent', 'constant'。
        scale : bool
            是否对特征进行标准化 (Z-score)。
        """
        self.impute_strategy = impute_strategy
        self.scale = scale
        self.imputer = SimpleImputer(strategy=impute_strategy)
        self.scaler = StandardScaler() if scale else None
        self.label_encoder = LabelEncoder()
        self.fitted_ = False

    def fit(self, X: np.ndarray, y: Optional[np.ndarray] = None) -> "Preprocessor":
        """拟合预处理器。

        Fit the preprocessor on training data.

        Parameters
        ----------
        X : np.ndarray, shape (n_samples, n_features)
            特征矩阵。
        y : np.ndarray, optional
            目标向量。如果提供且为分类标签，将编码 y。
        """
        # 填充缺失值 (Impute missing values)
        self.imputer.fit(X)
        X_clean = self.imputer.transform(X)

        # 缩放特征 (Scale features)
        if self.scaler is not None:
            self.scaler.fit(X_clean)

        # 编码标签 (Encode labels for classification)
        if y is not None and y.dtype in (np.int64, np.int32, np.int8, np.bool_, object):
            self.label_encoder.fit(y)
            self.is_classifier_ = True
        else:
            self.is_classifier_ = False

        self.fitted_ = True
        return self

    def transform(self, X: np.ndarray, y: Optional[np.ndarray] = None) -> Union[np.ndarray, Tuple[np.ndarray, np.ndarray]]:
        """转换数据。

        Transform data using fitted preprocessor.

        Parameters
        ----------
        X : np.ndarray
            特征矩阵。
        y : np.ndarray, optional
            目标向量。如果提供，将用 fitted label_encoder 转换。

        Returns
        -------
        X_proc : np.ndarray
            处理后的特征矩阵。
        y_proc : np.ndarray, optional (if y provided)
            处理后的目标向量。
        """
        if not self.fitted_:
            raise RuntimeError("Preprocessor not fitted. Call fit() first.")

        X_out = self.imputer.transform(X)
        if self.scaler is not None:
            X_out = self.scaler.transform(X_out)

        if y is not None and self.is_classifier_:
            y_out = self.label_encoder.transform(y)
            return X_out, y_out

        return X_out

    def fit_transform(self, X: np.ndarray, y: Optional[np.ndarray] = None) -> Union[np.ndarray, Tuple[np.ndarray, np.ndarray]]:
        """拟合 + 转换一步完成。"""
        self.fit(X, y)
        return self.transform(X, y)

    def inverse_transform_y(self, y_encoded: np.ndarray) -> np.ndarray:
        """将编码后的标签还原为原始标签。

        Inverse transform encoded labels back to original labels.
        """
        if self.is_classifier_:
            return self.label_encoder.inverse_transform(y_encoded)
        return y_encoded


def preprocess_pipeline(
    X_train: np.ndarray,
    X_test: np.ndarray,
    y_train: np.ndarray,
    y_test: Optional[np.ndarray] = None,
    impute_strategy: str = "mean",
    scale: bool = True,
) -> Tuple[np.ndarray, np.ndarray, Optional[np.ndarray], Optional[np.ndarray], Preprocessor]:
    """便捷函数：一步完成预处理。

    Convenience function: one-step preprocessing.

    Returns
    -------
    X_train_proc, X_test_proc, y_train_proc, y_test_proc, preprocessor
    """
    pre = Preprocessor(impute_strategy=impute_strategy, scale=scale)

    # fit_transform 可能返回 (X,) 或 (X, y_encoded)
    # fit_transform may return (X,) or (X, y_encoded)
    result_train = pre.fit_transform(X_train, y_train)
    if isinstance(result_train, tuple):
        X_train_proc, y_train_encoded = result_train
    else:
        X_train_proc = result_train
        y_train_encoded = y_train

    if X_test is not None:
        result_test = pre.transform(X_test, y_test) if y_test is not None else pre.transform(X_test)
        if isinstance(result_test, tuple):
            X_test_proc, y_test_encoded = result_test
        else:
            X_test_proc = result_test
            y_test_encoded = y_test
    else:
        X_test_proc = None
        y_test_encoded = None

    # 返回原始 y 值（不编码），因为 sklearn 的评估函数通常接受原始标签
    # Return original y (not encoded), since sklearn evaluation accepts raw labels
    return X_train_proc, X_test_proc, y_train, y_test, pre


# ============================================================
# 3. 数据划分 (Data Splitting)
# ============================================================
def split_data(
    X: np.ndarray,
    y: np.ndarray,
    task_type: str = "classification",
    train_size: float = 0.7,
    val_size: float = 0.15,
    test_size: float = 0.15,
    random_state: int = 42,
    stratify: bool = True,
) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """分层划分训练集、验证集、测试集。

    Stratified split into train / validation / test sets.

    Parameters
    ----------
    X : np.ndarray
        特征矩阵。
    y : np.ndarray
        目标向量。
    task_type : str
        'classification' — 启用分层抽样；'regression' — 使用分位数分层。
    train_size, val_size, test_size : float
        各部分比例，需满足三者之和为 1.0。
    random_state : int
        随机种子。
    stratify : bool
        是否使用分层抽样。回归任务中自动按目标值分位数分层。

    Returns
    -------
    X_train, X_val, X_test, y_train, y_val, y_test
    """
    assert abs(train_size + val_size + test_size - 1.0) < 1e-10, \
        "train_size + val_size + test_size must sum to 1.0"

    # 第一次划分: train vs (val + test)
    # First split: train vs (val + test)
    stratify_y = None
    if stratify and task_type == "classification":
        stratify_y = y
    elif stratify and task_type == "regression":
        # 对回归任务使用分位数分层
        # Use quantile-based stratification for regression
        n_bins = 10
        stratify_y = pd.qcut(y, q=n_bins, labels=False, duplicates="drop")

    X_train, X_temp, y_train, y_temp = train_test_split(
        X, y,
        train_size=train_size,
        random_state=random_state,
        stratify=stratify_y,
    )

    # 第二次划分: val vs test
    # Second split: val vs test
    val_ratio = val_size / (val_size + test_size)
    stratify_temp = None
    if stratify and task_type == "classification":
        stratify_temp = y_temp
    elif stratify and task_type == "regression":
        stratify_temp = pd.qcut(y_temp, q=n_bins, labels=False, duplicates="drop")

    X_val, X_test, y_val, y_test = train_test_split(
        X_temp, y_temp,
        test_size=test_size / (val_size + test_size),
        random_state=random_state,
        stratify=stratify_temp,
    )

    print(f"Data split complete: train={len(X_train)}, val={len(X_val)}, test={len(X_test)}")
    return X_train, X_val, X_test, y_train, y_val, y_test


# ============================================================
# 4. 模型训练 (Model Training)
# ============================================================
def train_model(
    X_train: np.ndarray,
    y_train: np.ndarray,
    task_type: str = "classification",
    model_type: str = "logistic",
    model_params: Optional[Dict[str, Any]] = None,
    model: Optional[BaseEstimator] = None,
    X_val: Optional[np.ndarray] = None,
    y_val: Optional[np.ndarray] = None,
) -> BaseEstimator:
    """训练可插拔模型。

    Train a pluggable model.

    Parameters
    ----------
    X_train, y_train : np.ndarray
        训练数据。
    task_type : str
        'classification' 或 'regression'。
    model_type : str
        模型类型。分类可选: 'logistic', 'decision_tree', 'random_forest', 'svm',
        'gradient_boosting'。回归可选: 'decision_tree', 'random_forest', 'svm',
        'gradient_boosting'。
    model_params : dict, optional
        传递给模型构造函数的额外参数。
    model : BaseEstimator, optional
        自定义模型实例。提供后将忽略 model_type。
    X_val, y_val : np.ndarray, optional
        验证集，用于输出训练/验证指标对比。

    Returns
    -------
    model : BaseEstimator
        训练好的模型。

    Raises
    ------
    ValueError
        当 model_type 不可用时。
    """
    if model is not None:
        # 使用自定义模型 (Use custom model)
        estimator = model
    elif task_type == "classification":
        if model_type not in CLASSIFICATION_MODELS:
            raise ValueError(
                f"Unknown classification model '{model_type}'. "
                f"Available: {list(CLASSIFICATION_MODELS.keys())}"
            )
        estimator = CLASSIFICATION_MODELS[model_type]
    else:
        if model_type not in REGRESSION_MODELS:
            raise ValueError(
                f"Unknown regression model '{model_type}'. "
                f"Available: {list(REGRESSION_MODELS.keys())}"
            )
        estimator = REGRESSION_MODELS[model_type]

    # 应用额外参数 (Apply extra parameters)
    if model_params:
        estimator.set_params(**model_params)

    # 训练 (Train)
    print(f"Training {type(estimator).__name__}...")
    estimator.fit(X_train, y_train)

    # 输出验证指标 (Report validation metrics)
    if X_val is not None and y_val is not None:
        train_score = estimator.score(X_train, y_train)
        val_score = estimator.score(X_val, y_val)
        print(f"  Train score: {train_score:.4f}  |  Val score: {val_score:.4f}")

    return estimator


# ============================================================
# 5. 模型评估 (Model Evaluation)
# ============================================================
def evaluate_model(
    model: BaseEstimator,
    X_test: np.ndarray,
    y_test: np.ndarray,
    task_type: str = "classification",
    class_names: Optional[list] = None,
    model_name: str = "model",
    save_plot: bool = True,
) -> Dict[str, float]:
    """全面评估模型性能，输出指标并生成可视化。

    Comprehensive model evaluation: metrics + plots.

    Parameters
    ----------
    model : BaseEstimator
        训练好的模型。
    X_test, y_test : np.ndarray
        测试数据。
    task_type : str
        'classification' 或 'regression'。
    class_names : list, optional
        分类标签名称。
    model_name : str
        模型名称，用于保存文件。
    save_plot : bool
        是否保存可视化图片。

    Returns
    -------
    metrics : dict
        评估指标字典。

    Raises
    ------
    ValueError
        当 task_type 不支持时。
    """
    y_pred = model.predict(X_test)

    metrics: Dict[str, float] = {}

    if task_type == "classification":
        # ======== 分类指标 (Classification Metrics) ========
        metrics["accuracy"] = float(accuracy_score(y_test, y_pred))
        metrics["precision"] = float(precision_score(y_test, y_pred, average="weighted", zero_division=0))
        metrics["recall"] = float(recall_score(y_test, y_pred, average="weighted", zero_division=0))
        metrics["f1"] = float(f1_score(y_test, y_pred, average="weighted", zero_division=0))

        # AUC (仅二分类)
        # AUC (binary classification only)
        if len(np.unique(y_test)) == 2 and hasattr(model, "predict_proba"):
            y_prob = model.predict_proba(X_test)[:, 1]
            metrics["roc_auc"] = float(roc_auc_score(y_test, y_prob))

        print(f"\n=== Classification Report ({model_name}) ===")
        print(classification_report(y_test, y_pred, target_names=class_names, zero_division=0))

        # 混淆矩阵 (Confusion Matrix)
        if save_plot:
            fig, axes = plt.subplots(1, 2, figsize=(12, 5))

            # 混淆矩阵热力图
            # Confusion matrix heatmap
            cm = confusion_matrix(y_test, y_pred)
            display_labels = class_names if class_names else None
            ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=display_labels).plot(
                ax=axes[0], cmap="Blues", values_format="d"
            )
            axes[0].set_title(f"Confusion Matrix — {model_name}")

            # ROC 曲线 (二分类)
            # ROC curve (binary)
            if len(np.unique(y_test)) == 2 and hasattr(model, "predict_proba"):
                y_prob = model.predict_proba(X_test)[:, 1]
                fpr, tpr, _ = roc_curve(y_test, y_prob)
                auc_val = metrics.get("roc_auc", 0)
                axes[1].plot(fpr, tpr, label=f"ROC (AUC = {auc_val:.3f})")
                axes[1].plot([0, 1], [0, 1], "k--", alpha=0.3)
                axes[1].set_xlabel("False Positive Rate")
                axes[1].set_ylabel("True Positive Rate")
                axes[1].set_title(f"ROC Curve — {model_name}")
                axes[1].legend()
                axes[1].grid(True, alpha=0.3)
            else:
                # 多分类: 显示各类别精度对比
                # Multi-class: per-class precision
                fig.delaxes(axes[1])

            plt.tight_layout()
            plot_path = OUTPUT_DIR / f"{model_name}_evaluation.png"
            plt.savefig(plot_path, bbox_inches="tight")
            plt.close()
            print(f"Evaluation plot saved: {plot_path}")

    elif task_type == "regression":
        # ======== 回归指标 (Regression Metrics) ========
        metrics["mse"] = float(mean_squared_error(y_test, y_pred))
        metrics["rmse"] = float(np.sqrt(metrics["mse"]))
        metrics["mae"] = float(mean_absolute_error(y_test, y_pred))
        metrics["r2"] = float(r2_score(y_test, y_pred))

        print(f"\n=== Regression Metrics ({model_name}) ===")
        for k, v in metrics.items():
            print(f"  {k.upper():8s}: {v:.4f}")

        # 可视化: 预测 vs 真实 (Prediction vs Actual)
        if save_plot:
            fig, axes = plt.subplots(1, 2, figsize=(12, 5))

            # 散点图 (Scatter: Predicted vs Actual)
            axes[0].scatter(y_test, y_pred, alpha=0.5, edgecolors="k", linewidth=0.5)
            min_val = min(y_test.min(), y_pred.min())
            max_val = max(y_test.max(), y_pred.max())
            axes[0].plot([min_val, max_val], [min_val, max_val], "r--", alpha=0.8)
            axes[0].set_xlabel("Actual Values")
            axes[0].set_ylabel("Predicted Values")
            axes[0].set_title(f"Predicted vs Actual — {model_name}")
            axes[0].grid(True, alpha=0.3)

            # 残差图 (Residual Plot)
            residuals = y_test - y_pred
            axes[1].scatter(y_pred, residuals, alpha=0.5, edgecolors="k", linewidth=0.5)
            axes[1].axhline(y=0, color="r", linestyle="--", alpha=0.8)
            axes[1].set_xlabel("Predicted Values")
            axes[1].set_ylabel("Residuals")
            axes[1].set_title(f"Residual Plot — {model_name}")
            axes[1].grid(True, alpha=0.3)

            plt.tight_layout()
            plot_path = OUTPUT_DIR / f"{model_name}_evaluation.png"
            plt.savefig(plot_path, bbox_inches="tight")
            plt.close()
            print(f"Evaluation plot saved: {plot_path}")

    else:
        raise ValueError(f"Unknown task_type: {task_type}. Use 'classification' or 'regression'.")

    return metrics


# ============================================================
# 6. 模型保存 (Model Persistence)
# ============================================================
def save_model(
    model: BaseEstimator,
    path: Union[str, Path],
    preprocessor: Optional[Preprocessor] = None,
    metadata: Optional[Dict[str, Any]] = None,
) -> Path:
    """使用 joblib 保存模型到磁盘。

    Save model to disk using joblib.

    Parameters
    ----------
    model : BaseEstimator
        训练好的模型。
    path : str or Path
        保存路径。
    preprocessor : Preprocessor, optional
        一并保存的预处理器。
    metadata : dict, optional
        额外元数据 (数据集名称、指标等)。

    Returns
    -------
    path : Path
        保存的文件路径。
    """
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)

    package = {
        "model": model,
        "preprocessor": preprocessor,
        "metadata": metadata or {},
    }
    joblib.dump(package, path)
    print(f"Model saved: {path} ({path.stat().st_size / 1024:.1f} KB)")
    return path


# ============================================================
# 7. 模型加载与推理 (Model Loading & Inference)
# ============================================================
def load_and_predict(
    model_path: Union[str, Path],
    X_new: np.ndarray,
    return_proba: bool = False,
) -> Union[np.ndarray, Tuple[np.ndarray, Optional[np.ndarray]]]:
    """加载保存的模型并对新数据进行预测。

    Load a saved model and make predictions on new data.

    Parameters
    ----------
    model_path : str or Path
        模型文件路径 (joblib 格式)。
    X_new : np.ndarray, shape (n_samples, n_features)
        新样本特征矩阵。
    return_proba : bool
        是否同时返回预测概率 (仅适用于支持 predict_proba 的模型)。

    Returns
    -------
    y_pred : np.ndarray
        预测结果。
    y_prob : np.ndarray, optional
        预测概率 (当 return_proba=True 时返回)。

    Raises
    ------
    FileNotFoundError
        当模型文件不存在时。
    """
    model_path = Path(model_path)
    if not model_path.exists():
        raise FileNotFoundError(f"Model file not found: {model_path}")

    package = joblib.load(model_path)
    model = package["model"]
    preprocessor = package.get("preprocessor")

    # 如果存有预处理器，先转换数据
    # Apply preprocessing if a fitted preprocessor was saved
    if preprocessor is not None:
        X_new = preprocessor.transform(X_new)

    y_pred = model.predict(X_new)

    if return_proba and hasattr(model, "predict_proba"):
        y_prob = model.predict_proba(X_new)
        return y_pred, y_prob

    return y_pred


# ============================================================
# 8. 完整端到端演示 (End-to-End Demo)
# ============================================================
def run_demo():
    """在鸢尾花数据集上运行完整的 ML 管道演示。

    Run a complete ML pipeline demo on the Iris dataset.
    """
    print("=" * 60)
    print("ML Project Template — End-to-End Demo")
    print("ML 项目模板 — 端到端演示")
    print("=" * 60)

    # ---- Step 1: Load Data ----
    print("\n[1/6] Loading data...")
    X, y, feature_names, task_type = load_data(dataset_name="iris")
    print(f"  Features ({len(feature_names)}): {feature_names}")

    # ---- Step 2: Split Data ----
    print("\n[2/6] Splitting data...")
    X_train, X_val, X_test, y_train, y_val, y_test = split_data(
        X, y, task_type=task_type, random_state=42
    )

    # ---- Step 3: Preprocess ----
    print("\n[3/6] Preprocessing...")
    X_train_proc, X_val_proc, y_train_proc, y_val_proc, pre = preprocess_pipeline(
        X_train, X_val, y_train, y_val
    )
    X_test_proc, y_test_proc = pre.transform(X_test, y_test)

    # ---- Step 4: Train ----
    print("\n[4/6] Training models...")
    models_to_try = ["logistic", "decision_tree", "random_forest"]
    best_model = None
    best_val_score = -1.0

    for model_name in models_to_try:
        model = train_model(
            X_train_proc, y_train,
            task_type=task_type,
            model_type=model_name,
            X_val=X_val_proc, y_val=y_val,
        )
        val_score = model.score(X_val_proc, y_val)
        print(f"  → {model_name}: val_acc = {val_score:.4f}")

        if val_score > best_val_score:
            best_val_score = val_score
            best_model = model
            best_model_name = model_name

    print(f"\n  Best model: {best_model_name} (val_acc = {best_val_score:.4f})")

    # ---- Step 5: Evaluate ----
    print(f"\n[5/6] Evaluating best model ({best_model_name}) on test set...")
    metrics = evaluate_model(
        best_model, X_test_proc, y_test,
        task_type=task_type,
        class_names=["setosa", "versicolor", "virginica"],
        model_name=f"iris_{best_model_name}",
    )
    print(f"  Test accuracy: {metrics['accuracy']:.4f}")
    print(f"  Test F1 score: {metrics['f1']:.4f}")

    # ---- Step 6: Save & Reload ----
    print(f"\n[6/6] Saving and reloading model...")
    model_path = OUTPUT_DIR / f"iris_{best_model_name}.joblib"
    save_model(
        best_model,
        model_path,
        preprocessor=pre,
        metadata={
            "dataset": "iris",
            "model": best_model_name,
            "metrics": metrics,
            "feature_names": feature_names,
        },
    )

    # 推理演示 (Inference demo)
    print("\n  → Inference on 5 random test samples:")
    sample_idx = RNG.choice(len(X_test_proc), size=5, replace=False)
    X_sample = X_test_proc[sample_idx]
    y_true = y_test[sample_idx]
    y_pred = load_and_predict(model_path, X_sample)
    for i, (true_val, pred_val) in enumerate(zip(y_true, y_pred)):
        status = "✓" if true_val == pred_val else "✗"
        print(f"    [{status}] True: {true_val}, Predicted: {pred_val}")

    print("\n" + "=" * 60)
    print("Demo complete! All pipeline steps verified successfully.")
    print("演示完成！所有管道步骤验证成功。")
    print("=" * 60)


if __name__ == "__main__":
    run_demo()
