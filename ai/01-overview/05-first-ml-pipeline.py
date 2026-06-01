"""
First ML Pipeline — 第一个机器学习流水线
===========================================
Complete end-to-end ML pipeline using the Iris dataset.
Runs Logistic Regression: data loading → EDA → training → evaluation → saving.

Run with: python ai/01-overview/05-first-ml-pipeline.py
"""

import warnings
warnings.filterwarnings("ignore")

import numpy as np
import matplotlib
matplotlib.use("Agg")  # Non-interactive backend for headless environments
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap

from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
)
import joblib
import os

# ============================================================
# 0. SETUP — Output directory for plots and models
# ============================================================
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "output")
os.makedirs(OUTPUT_DIR, exist_ok=True)

print("=" * 70)
print("FIRST ML PIPELINE — Iris Classification")
print("=" * 70)

# ============================================================
# 1. LOAD DATA — 加载数据集
# ============================================================
print("\n" + "=" * 70)
print("1. LOAD DATA")
print("=" * 70)

iris = load_iris()
X = iris.data       # Feature matrix: 150 samples × 4 features
y = iris.target     # Target vector: 0, 1, 2 (3 species)

# ============================================================
# 2. EXPLORATORY DATA ANALYSIS (EDA) — 探索性数据分析
# ============================================================
print("\n" + "=" * 70)
print("2. EXPLORATORY DATA ANALYSIS")
print("=" * 70)

print(f"\nDataset shape (rows, columns): {X.shape}")
print(f"Feature names:                {iris.feature_names}")
print(f"Target names:                 {iris.target_names}")
print(f"Target distribution (counts per class):")
for i, name in enumerate(iris.target_names):
    count = sum(y == i)
    print(f"  {i} — {name:12s}: {count} samples")

print(f"\nFirst 5 rows of X:\n{X[:5]}")
print(f"\nFirst 5 targets: {y[:5]}")

# Quick summary statistics
print(f"\nFeature statistics:")
print(f"  mean: {X.mean(axis=0).round(2)}")
print(f"  std:  {X.std(axis=0).round(2)}")

# ============================================================
# 3. TRAIN / TEST SPLIT — 划分训练集和测试集
# ============================================================
print("\n" + "=" * 70)
print("3. TRAIN / TEST SPLIT (80/20 stratified)")
print("=" * 70)

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)
# stratify=y ensures the same class ratio in train and test sets

print(f"Training set:   {X_train.shape[0]} samples")
print(f"Test set:       {X_test.shape[0]} samples")

# ============================================================
# 4. STANDARDIZE FEATURES — 标准化特征
# ============================================================
print("\n" + "=" * 70)
print("4. STANDARDIZE FEATURES (StandardScaler)")
print("=" * 70)

scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# After scaling, each feature has mean ≈ 0 and std ≈ 1
print(f"Mean after scaling (train): {X_train_scaled.mean(axis=0).round(4)}")
print(f"Std  after scaling (train): {X_train_scaled.std(axis=0).round(4)}")

# ============================================================
# 5. TRAIN MODEL — 训练模型
# ============================================================
print("\n" + "=" * 70)
print("5. TRAIN LOGISTIC REGRESSION")
print("=" * 70)

model = LogisticRegression(max_iter=200, random_state=42)
model.fit(X_train_scaled, y_train)
# During fit(), the model finds the optimal coefficients
# that minimize the cross-entropy loss on training data.

print(f"Model coefficients shape: {model.coef_.shape}")
print(f"  (n_classes × n_features)")
print(f"Intercept: {model.intercept_}")

# ============================================================
# 6. PREDICT — 预测
# ============================================================
print("\n" + "=" * 70)
print("6. PREDICT ON TEST SET")
print("=" * 70)

y_pred = model.predict(X_test_scaled)

# Show first 10 predictions vs ground truth
print("\nFirst 10 predictions vs actual:")
for i in range(10):
    pred_name = iris.target_names[y_pred[i]]
    true_name = iris.target_names[y_test[i]]
    match = "✓" if y_pred[i] == y_test[i] else "✗"
    print(f"  [{i}] Predicted: {pred_name:10s} | Actual: {true_name:10s} {match}")

# ============================================================
# 7. EVALUATE — 评估
# ============================================================
print("\n" + "=" * 70)
print("7. EVALUATION")
print("=" * 70)

# Accuracy
acc = accuracy_score(y_test, y_pred)
print(f"\nAccuracy: {acc:.4f}  ({acc * 100:.2f}%)")

# Classification report
print(f"\nClassification Report:")
print(classification_report(y_test, y_pred, target_names=iris.target_names))

# Confusion matrix
cm = confusion_matrix(y_test, y_pred)
print("Confusion Matrix (rows=true, cols=predicted):")
print(cm)

# ============================================================
# 8. VISUALIZE — 可视化
# ============================================================
print("\n" + "=" * 70)
print("8. VISUALIZATION")
print("=" * 70)

# 8a. Confusion matrix heatmap
plt.figure(figsize=(6, 5))
plt.imshow(cm, interpolation="nearest", cmap="Blues")
plt.colorbar(shrink=0.8)
for i in range(cm.shape[0]):
    for j in range(cm.shape[1]):
        plt.text(j, i, str(cm[i, j]), ha="center", va="center", fontsize=14)
plt.title("Confusion Matrix — Iris Logistic Regression")
plt.xlabel("Predicted Label")
plt.ylabel("True Label")
plt.xticks(ticks=range(len(iris.target_names)), labels=iris.target_names)
plt.yticks(ticks=range(len(iris.target_names)), labels=iris.target_names)
confusion_path = os.path.join(OUTPUT_DIR, "confusion_matrix.png")
plt.tight_layout()
plt.savefig(confusion_path, dpi=150)
plt.close()
print(f"  Confusion matrix saved to: {confusion_path}")

# 8b. Decision boundary for 2 selected features (petal length × petal width)
#     This gives a visual sense of what the model learned.
plt.figure(figsize=(8, 6))

# Use only petal length (feature 2) and petal width (feature 3) for 2D viz
X_vis = X_train[:, 2:4]  # petal_length, petal_width
vis_scaler = StandardScaler()
X_vis_scaled = vis_scaler.fit_transform(X_vis)  # separate scaler for 2D viz

# Train a quick model on just these 2 features for visualization
model_vis = LogisticRegression(max_iter=200, random_state=42)
model_vis.fit(X_vis_scaled, y_train)

# Create a mesh grid
x_min, x_max = X_vis_scaled[:, 0].min() - 1, X_vis_scaled[:, 0].max() + 1
y_min, y_max = X_vis_scaled[:, 1].min() - 1, X_vis_scaled[:, 1].max() + 1
xx, yy = np.meshgrid(np.linspace(x_min, x_max, 200), np.linspace(y_min, y_max, 200))

# Predict on mesh grid
Z = model_vis.predict(np.c_[xx.ravel(), yy.ravel()])
Z = Z.reshape(xx.shape)

# Plot decision boundary
cmap_light = ListedColormap(["#FFAAAA", "#AAFFAA", "#AAAAFF"])
cmap_bold = ListedColormap(["#FF0000", "#00AA00", "#0000FF"])
plt.contourf(xx, yy, Z, alpha=0.3, cmap=cmap_light)

# Plot training points
scatter = plt.scatter(
    X_vis_scaled[:, 0],
    X_vis_scaled[:, 1],
    c=y_train,
    cmap=cmap_bold,
    edgecolor="black",
    s=40,
)
plt.xlabel("Petal Length (standardized)")
plt.ylabel("Petal Width (standardized)")
plt.title("Decision Boundary (Petal Length × Petal Width)")
plt.colorbar(scatter, ticks=[0, 1, 2], label="Species")
decision_path = os.path.join(OUTPUT_DIR, "decision_boundary.png")
plt.tight_layout()
plt.savefig(decision_path, dpi=150)
plt.close()
print(f"  Decision boundary saved to: {decision_path}")

# ============================================================
# 9. SAVE MODEL — 保存模型
# ============================================================
print("\n" + "=" * 70)
print("9. SAVE MODEL")
print("=" * 70)

model_path = os.path.join(OUTPUT_DIR, "iris_logistic_regression.joblib")
joblib.dump(model, model_path)
print(f"  Model saved to: {model_path}")

# Also save the scaler for future use (new data needs the same scaling)
scaler_path = os.path.join(OUTPUT_DIR, "scaler.joblib")
joblib.dump(scaler, scaler_path)
print(f"  Scaler saved to: {scaler_path}")

# ============================================================
# 10. LOAD & VERIFY — 加载并验证保存的模型
# ============================================================
print("\n" + "=" * 70)
print("10. LOAD SAVED MODEL & VERIFY")
print("=" * 70)

loaded_model = joblib.load(model_path)
loaded_scaler = joblib.load(scaler_path)

# Predict on a single new sample
sample = X_test[0:1]
sample_scaled = loaded_scaler.transform(sample)
pred = loaded_model.predict(sample_scaled)
pred_proba = loaded_model.predict_proba(sample_scaled)

print(f"\nSingle sample (row 0 of test set):")
print(f"  Raw features:        {sample[0].round(2)}")
print(f"  Predicted class:     {iris.target_names[pred[0]]}")
print(f"  Confidence (proba):  {pred_proba[0].round(4)}")
print(f"  Actual class:        {iris.target_names[y_test[0]]}")

# ============================================================
# SUMMARY
# ============================================================
print("\n" + "=" * 70)
print("PIPELINE COMPLETE ✓")
print("=" * 70)
print(f"\nOutput files:")
print(f"  {confusion_path}")
print(f"  {decision_path}")
print(f"  {model_path}")
print(f"  {scaler_path}")
print(f"\nKey takeaway: This pipeline went from raw data to a saved, ")
print(f"evaluated model in ~9 steps. The same pattern applies to ")
print(f"any classification problem — swap the dataset and tune the model.")
