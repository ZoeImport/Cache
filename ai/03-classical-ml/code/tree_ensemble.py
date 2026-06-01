"""
03 — 树模型与集成学习配套代码（Tree Models & Ensemble Learning Companion Code）

功能列表 (Features):
  1. compare_trees()            — 对比不同深度决策树的表现
  2. visualize_tree_structure() — 可视化决策树结构（树形图）
  3. compare_rf_vs_tree()       — 随机森林 vs 单棵决策树精度对比
  4. compare_all_models()       — 决策树、随机森林、XGBoost 三者对比
  5. demo_feature_importance()  — 特征重要性展示

依赖: numpy, matplotlib, sklearn, xgboost
运行: python tree_ensemble.py
输出: 终端输出精度对比表; 图片保存至 output/ 目录
"""

import numpy as np
import matplotlib.pyplot as plt
import warnings
import os

from sklearn.datasets import load_iris
from sklearn.model_selection import cross_val_score, train_test_split
from sklearn.tree import DecisionTreeClassifier, plot_tree
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

warnings.filterwarnings("ignore")

# ============================================================
# 全局设置
# ============================================================
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "output")
os.makedirs(OUTPUT_DIR, exist_ok=True)

# 加载 Iris 数据集
iris = load_iris()
X, y = iris.data, iris.target
feature_names = iris.feature_names
target_names = iris.target_names

# 固定随机种子，保证可重复
RANDOM_STATE = 42


# ============================================================
# 1. 决策树深度的影响（对比不同深度）
# ============================================================
def compare_trees():
    """
    对比不同深度（max_depth=1~6）下决策树在 Iris 上的精度。
    展示：过拟合随深度增加的趋势。
    """
    print("=" * 60)
    print("1. 决策树深度对精度的影响 (Effect of Tree Depth)")
    print("=" * 60)

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.3, random_state=RANDOM_STATE
    )

    depths = range(1, 7)
    train_scores = []
    test_scores = []

    for depth in depths:
        tree = DecisionTreeClassifier(max_depth=depth, random_state=RANDOM_STATE)
        tree.fit(X_train, y_train)

        train_acc = accuracy_score(y_train, tree.predict(X_train))
        test_acc = accuracy_score(y_test, tree.predict(X_test))
        train_scores.append(train_acc)
        test_scores.append(test_acc)

        print(f"  max_depth={depth}:  Train Acc = {train_acc:.4f},  Test Acc = {test_acc:.4f}")

    # --- 绘图 ---
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.plot(depths, train_scores, "bo-", label="Train Accuracy")
    ax.plot(depths, test_scores, "rs--", label="Test Accuracy")
    ax.set_xlabel("Max Depth", fontsize=12)
    ax.set_ylabel("Accuracy", fontsize=12)
    ax.set_title("Decision Tree: Accuracy vs Depth (Iris)", fontsize=14)
    ax.set_xticks(depths)
    ax.legend(fontsize=11)
    ax.grid(True, alpha=0.3)
    fig.tight_layout()
    fig.savefig(os.path.join(OUTPUT_DIR, "tree_depth_vs_accuracy.png"), dpi=150)
    plt.close(fig)
    print(f"  [图] 已保存: output/tree_depth_vs_accuracy.png\n")


# ============================================================
# 2. 可视化决策树结构
# ============================================================
def visualize_tree_structure():
    """
    使用 sklearn.tree.plot_tree 可视化一棵训练好的决策树。
    保存树结构图。
    """
    print("=" * 60)
    print("2. 决策树结构可视化 (Tree Structure Visualization)")
    print("=" * 60)

    tree = DecisionTreeClassifier(max_depth=3, random_state=RANDOM_STATE)
    tree.fit(X, y)

    fig, ax = plt.subplots(figsize=(14, 8))
    plot_tree(
        tree,
        feature_names=feature_names,
        class_names=target_names.tolist(),
        filled=True,
        rounded=True,
        fontsize=10,
        ax=ax,
    )
    ax.set_title("Decision Tree Structure (max_depth=3) on Iris", fontsize=14)
    fig.tight_layout()
    fig.savefig(os.path.join(OUTPUT_DIR, "tree_structure.png"), dpi=150)
    plt.close(fig)
    print("  [图] 已保存: output/tree_structure.png\n")

    # 同时打印文本形式的树结构
    print("  树结构文本表示 (Text Representation):")
    print("  " + "-" * 50)
    text_lines = []
    _tree_to_text(tree, feature_names, target_names, text_lines)
    for line in text_lines:
        print("  " + line)
    print()


def _tree_to_text(tree, feature_names, class_names, lines, node=0, depth=0):
    """递归输出树结构的文本表示"""
    indent = "  " * depth
    n_samples = tree.tree_.n_node_samples[node]
    value = tree.tree_.value[node][0]
    class_idx = np.argmax(value)
    class_name = class_names[class_idx]

    if tree.tree_.children_left[node] == tree.tree_.children_right[node]:
        # 叶节点
        lines.append(f"{indent}├── Leaf: class={class_name}, samples={n_samples}, "
                      f"distribution={value.astype(int)}")
    else:
        feature = feature_names[tree.tree_.feature[node]]
        threshold = tree.tree_.threshold[node]
        impurity = tree.tree_.impurity[node]
        lines.append(f"{indent}├── [{feature} <= {threshold:.2f}] "
                      f"gini={impurity:.3f}, samples={n_samples}, "
                      f"distribution={value.astype(int)}")
        _tree_to_text(tree, feature_names, class_names, lines,
                       tree.tree_.children_left[node], depth + 1)
        _tree_to_text(tree, feature_names, class_names, lines,
                       tree.tree_.children_right[node], depth + 1)


# ============================================================
# 3. 随机森林 vs 单棵决策树
# ============================================================
def compare_rf_vs_tree():
    """
    对比随机森林和单棵决策树的交叉验证精度，
    以及随机森林的 OOB 误差。
    """
    print("=" * 60)
    print("3. 随机森林 vs 单棵决策树 (RF vs Single Tree)")
    print("=" * 60)

    # 交叉验证
    tree = DecisionTreeClassifier(random_state=RANDOM_STATE)
    rf = RandomForestClassifier(n_estimators=100, random_state=RANDOM_STATE)

    tree_cv = cross_val_score(tree, X, y, cv=5)
    rf_cv = cross_val_score(rf, X, y, cv=5)

    print(f"  单棵决策树 CV Accuracy: {tree_cv.mean():.4f} ± {tree_cv.std():.4f}")
    print(f"  随机森林    CV Accuracy: {rf_cv.mean():.4f} ± {rf_cv.std():.4f}")
    print(f"  精度提升: +{(rf_cv.mean() - tree_cv.mean()) * 100:.2f}%")
    print()

    # OOB 误差
    rf_oob = RandomForestClassifier(
        n_estimators=200, oob_score=True, random_state=RANDOM_STATE
    )
    rf_oob.fit(X, y)
    print(f"  随机森林 OOB Score: {rf_oob.oob_score_:.4f}")
    print(f"  这与 5 折 CV 精度 {rf_cv.mean():.4f} 非常接近")
    print()

    # --- 绘图：RF 精度随 n_estimators 变化 ---
    n_range = [1, 5, 10, 20, 50, 100, 200, 500]
    rf_scores = []
    for n in n_range:
        rf = RandomForestClassifier(n_estimators=n, random_state=RANDOM_STATE)
        scores = cross_val_score(rf, X, y, cv=5)
        rf_scores.append(scores.mean())

    fig, ax = plt.subplots(figsize=(8, 5))
    ax.plot(n_range, rf_scores, "go-", label="Random Forest CV Accuracy")
    ax.axhline(y=tree_cv.mean(), color="r", linestyle="--",
               label=f"Single Tree (CV={tree_cv.mean():.3f})")
    ax.set_xlabel("Number of Trees (n_estimators)", fontsize=12)
    ax.set_ylabel("CV Accuracy", fontsize=12)
    ax.set_title("Random Forest: Accuracy vs Number of Trees", fontsize=14)
    ax.set_xscale("log")
    ax.set_xticks(n_range)
    ax.get_xaxis().set_major_formatter(plt.ScalarFormatter())
    ax.legend(fontsize=11)
    ax.grid(True, alpha=0.3)
    fig.tight_layout()
    fig.savefig(os.path.join(OUTPUT_DIR, "rf_accuracy_vs_ntrees.png"), dpi=150)
    plt.close(fig)
    print(f"  [图] 已保存: output/rf_accuracy_vs_ntrees.png\n")


# ============================================================
# 4. 三模型对比：决策树 vs 随机森林 vs XGBoost
# ============================================================
def compare_all_models():
    """
    在 Iris 数据集上对比 DecisionTree、RandomForest、XGBoost 的精度。

    注意：需要安装 xgboost (pip install xgboost)。
    """
    print("=" * 60)
    print("4. 三模型精度对比 (DT vs RF vs XGBoost)")
    print("=" * 60)

    try:
        from xgboost import XGBClassifier
    except ImportError:
        print("  [SKIP] xgboost 未安装，跳过 XGBoost 对比。")
        print("  安装: pip install xgboost")
        print()
        return

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.3, random_state=RANDOM_STATE
    )

    models = {
        "DecisionTree (max_depth=3)": DecisionTreeClassifier(
            max_depth=3, random_state=RANDOM_STATE
        ),
        "DecisionTree (full)": DecisionTreeClassifier(
            random_state=RANDOM_STATE
        ),
        "RandomForest (100 trees)": RandomForestClassifier(
            n_estimators=100, random_state=RANDOM_STATE
        ),
        "XGBoost (default)": XGBClassifier(
            n_estimators=100, eval_metric="logloss", random_state=RANDOM_STATE,
            verbosity=0
        ),
        "XGBoost (tuned)": XGBClassifier(
            n_estimators=100, max_depth=3, learning_rate=0.1,
            reg_lambda=1.0, subsample=0.8, colsample_bytree=0.8,
            eval_metric="logloss", random_state=RANDOM_STATE, verbosity=0
        ),
    }

    print(f"  {'Model':<28} {'Train Acc':>10} {'Test Acc':>10} {'CV Acc':>10}")
    print("  " + "-" * 60)

    results = []
    for name, model in models.items():
        model.fit(X_train, y_train)
        train_acc = accuracy_score(y_train, model.predict(X_train))
        test_acc = accuracy_score(y_test, model.predict(X_test))
        cv_scores = cross_val_score(model, X, y, cv=5)
        cv_mean = cv_scores.mean()
        results.append((name, train_acc, test_acc, cv_mean))
        print(f"  {name:<28} {train_acc:>10.4f} {test_acc:>10.4f} {cv_mean:>10.4f}")

    print()

    # --- 绘图：条形图对比 ---
    names = [r[0] for r in results]
    test_accs = [r[2] for r in results]
    cv_accs = [r[3] for r in results]

    fig, ax = plt.subplots(figsize=(10, 6))
    x = np.arange(len(names))
    width = 0.35
    bars1 = ax.bar(x - width / 2, test_accs, width, label="Test Accuracy", color="steelblue")
    bars2 = ax.bar(x + width / 2, cv_accs, width, label="CV Accuracy (5-fold)", color="coral")
    ax.set_ylabel("Accuracy", fontsize=12)
    ax.set_title("Model Comparison: Decision Tree vs Random Forest vs XGBoost", fontsize=14)
    ax.set_xticks(x)
    ax.set_xticklabels(names, rotation=20, ha="right", fontsize=10)
    ax.legend(fontsize=11)
    ax.set_ylim([0.8, 1.05])
    ax.grid(True, axis="y", alpha=0.3)

    # 在柱上标注数值
    for bar in bars1:
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() - 0.015,
                f"{bar.get_height():.3f}", ha="center", va="top", fontsize=9, color="white", fontweight="bold")
    for bar in bars2:
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.003,
                f"{bar.get_height():.3f}", ha="center", va="bottom", fontsize=9, color="darkred")

    fig.tight_layout()
    fig.savefig(os.path.join(OUTPUT_DIR, "model_comparison.png"), dpi=150)
    plt.close(fig)
    print(f"  [图] 已保存: output/model_comparison.png\n")


# ============================================================
# 5. 特征重要性展示
# ============================================================
def demo_feature_importance():
    """
    展示决策树、随机森林、XGBoost 的特征重要性排序。
    """
    print("=" * 60)
    print("5. 特征重要性 (Feature Importance)")
    print("=" * 60)

    try:
        from xgboost import XGBClassifier
        has_xgb = True
    except ImportError:
        has_xgb = False

    models = {
        "DecisionTree": DecisionTreeClassifier(random_state=RANDOM_STATE),
        "RandomForest": RandomForestClassifier(n_estimators=100, random_state=RANDOM_STATE),
    }
    if has_xgb:
        models["XGBoost"] = XGBClassifier(
            n_estimators=100, eval_metric="logloss", random_state=RANDOM_STATE, verbosity=0
        )

    fig, axes = plt.subplots(1, len(models), figsize=(5 * len(models), 5))
    if len(models) == 1:
        axes = [axes]

    for ax, (name, model) in zip(axes, models.items()):
        model.fit(X, y)
        importances = model.feature_importances_
        sorted_idx = np.argsort(importances)[::-1]

        ax.bar(range(len(feature_names)), importances[sorted_idx], color="teal", alpha=0.8)
        ax.set_xticks(range(len(feature_names)))
        ax.set_xticklabels([feature_names[i] for i in sorted_idx], rotation=15, fontsize=9)
        ax.set_title(f"{name}\nFeature Importance", fontsize=12)
        ax.set_ylabel("Importance", fontsize=10)
        ax.grid(True, axis="y", alpha=0.3)

        # 标注数值
        for i, v in enumerate(importances[sorted_idx]):
            ax.text(i, v + 0.02, f"{v:.3f}", ha="center", va="bottom", fontsize=8)

        # 打印
        print(f"  {name} Feature Importance:")
        for i in sorted_idx:
            print(f"    {feature_names[i]:<25} {importances[i]:.4f}")
        print()

    fig.tight_layout()
    fig.savefig(os.path.join(OUTPUT_DIR, "feature_importance.png"), dpi=150)
    plt.close(fig)
    print(f"  [图] 已保存: output/feature_importance.png\n")


# ============================================================
# 主函数
# ============================================================
if __name__ == "__main__":
    print()
    print("🌳  树模型与集成学习配套代码运行中 ...")
    print("   Tree Models & Ensemble Learning — Companion Code")
    print()

    compare_trees()
    visualize_tree_structure()
    compare_rf_vs_tree()
    compare_all_models()
    demo_feature_importance()

    print("=" * 60)
    print("✅ 全部演示完成! 图片保存至: code/output/")
    print("   All demos complete! Images saved to: code/output/")
    print("=" * 60)
