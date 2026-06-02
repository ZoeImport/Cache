# 03 — 树模型与集成学习（Tree Models & Ensemble Learning）

> 树模型（Decision Trees）是机器学习中最直观、最可解释的算法之一。但单棵决策树容易过拟合（overfitting /ˈoʊvərˈfɪtɪŋ/）、不稳定（数据微小变化会导致树结构巨变）。集成学习（Ensemble Learning）通过组合多个弱学习器来构建强学习器，有效解决了这些问题。
> > **时间线**:
> > - **1963**: Vapnik & Chervonenkis 提出 VC 维理论
> > - **1984**: Breiman 等人发表 CART（Classification and Regression Trees）
> > - **1986**: Quinlan 提出 ID3 决策树算法
> > - **1997**: Freund & Schapire 发表 AdaBoost 算法
> - **2001**: Breiman 提出随机森林（Random Forest）
>
> 本章涵盖两大集成范式：**Bagging**（以随机（stochastic /stəˈkæstɪk/）森林为代表）和 **Boosting**（以 GBDT / XGBoost 为代表）。你将看到为什么随机森林能降低方差而不增偏差，以及 XGBoost 为何成为 Kaggle 竞赛和工业界表格数据的常胜将军。
>
> 章节路线：**决策树 → Bagging → 随机森林 → Boosting → GBDT → XGBoost → 树 vs 深度学习**

---

## 1. 决策树（Decision Trees）

### 1.1 树结构

决策树模拟人类做决策的过程：从根节点（Root Node）开始，根据特征值做判断，沿着分支到达内部节点（Internal Nodes），最终到达叶节点（Leaf Nodes），每个叶节点对应一个预测值（分类（classification /ˌklæsɪfɪˈkeɪʃən/）或回归（regression /rɪˈɡreʃən/））。

```
                    [Outlook = Sunny?]
                    /                \
                 Yes                  No
                 /                      \
        [Humidity > 75%?]           [Outlook = Overcast?]
          /          \                 /            \
        Yes           No             Yes             No
        /              \             /                \
    [Play=No]      [Play=Yes]   [Play=Yes]    [Wind = Strong?]
                                                  /          \
                                                Yes           No
                                                /              \
                                           [Play=No]      [Play=Yes]
```

### 1.2 如何选择分裂特征：信息增益 vs Gini 不纯度

决策树的核（kernel /ˈkɜːrnl/）心问题：**在每个节点，选择哪个特征、以什么阈值分裂，能使子节点最"纯"？**

#### 信息增益（Information Gain）

从第 04 章的信息论我们知道，熵（entropy /ˈentrəpi/）（Entropy）衡量不确定性。分裂后子节点的加权熵与父节点熵的差值，就是**信息增益**：

$$IG(D, a) = H(D) - \sum_{v \in Values(a)} \frac{|D_v|}{|D|} H(D_v)$$

其中 $H(D) = -\sum_{k} p_k \log p_k$ 是数据集 $D$ 的熵，$p_k$ 是第 $k$ 类的比例。

**直觉**：信息增益越大，说明这个特征分裂后不确定性降低得越多——即这个特征越重要。

```python
def entropy(labels):
    """计算标签的熵"""
    _, counts = np.unique(labels, return_counts=True)
    probs = counts / counts.sum()
    return -np.sum(probs * np.log2(probs + 1e-10))

def info_gain(data, labels, feature_idx, threshold):
    """计算按某特征阈值分裂的信息增益"""
    parent_entropy = entropy(labels)
    left_mask = data[:, feature_idx] <= threshold
    right_mask = ~left_mask
    n = len(labels)
    n_left, n_right = left_mask.sum(), right_mask.sum()
    if n_left == 0 or n_right == 0:
        return 0
    child_entropy = (n_left / n) * entropy(labels[left_mask]) + \
                    (n_right / n) * entropy(labels[right_mask])
    return parent_entropy - child_entropy
```

#### Gini 不纯度（Gini Impurity）

Gini 不纯度衡量从数据集中**随机抽取两个样本，其类别不一致的概率**：

$$Gini(D) = 1 - \sum_{k} p_k^2$$

- 所有样本属于同一类：$Gini = 0$（最纯）
- 类别均匀分布（$K$ 类）：$Gini = 1 - 1/K$（最不纯）

分裂时选择使**加权 Gini 不纯度最小化**的分裂方式。

**信息增益 vs Gini**：

| 指标 | 公式 | 取值范围 | 偏好 |
|:---|:---|:---:|:---|
| 信息增益 | $H(D) - \sum \frac{n_v}{n} H(D_v)$ | $[0, \log K]$ | 偏向多值特征 |
| Gini 不纯度 | $1 - \sum p_k^2$ | $[0, 1-1/K]$ | 计算更快，通常与信息增益结果相似 |

> **实践建议**：sklearn 的 `DecisionTreeClassifier` 默认使用 `criterion='gini'`。两者在实际应用中差异不大，Gini 计算稍快。

### 1.3 过拟合与剪枝

决策树的一个严重问题是**过拟合**：如果不加限制，树可以不断分裂直到每个叶节点只包含一个样本（训练精度 100%），但泛化能力很差。

**过拟合表现**：
- 树的深度很大
- 叶节点样本数很少
- 训练精度远高于测试精度

**缓解方法**：

| 方法 | 描述 |
|:---|:---|
| **预剪枝（Pre-pruning）** | 在树生长过程中提前停止：限制 `max_depth`、`min_samples_split`、`min_samples_leaf` |
| **后剪枝（Post-pruning）** | 先让树充分生长，再自底向上合并不显著的分支（CCP，Cost-Complexity Pruning） |
| **限制叶节点最小样本数** | 每个叶节点至少包含 $N$ 个样本，防止"记忆"噪声 |

> 详见配套代码 `tree_ensemble.py` 中的 `compare_trees()`，该函数对比了不同深度下决策树在 Iris 数据集上的表现。

---

## 2. 随机森林（Random Forest）

### 2.1 Bagging 原理

**Bagging**（Bootstrap Aggregating）的核心思想：

1. 从原始数据集 $D$ 中**有放回地采样** $N$ 次，生成一个 Bootstrap 样本 $D_i$（大小与原始数据集相同，但约有 $63.2\%$ 的原始样本出现，其余为重复）
2. 在 $D_i$ 上训练一个基学习器（如决策树）
3. 重复 $T$ 次，得到 $T$ 个模型
4. **回归**：取 $T$ 个预测的平均值；**分类**：取 $T$ 个预测的投票结果

```python
def bagging_predict(models, X):
    """Bagging 集成预测"""
    predictions = np.array([model.predict(X) for model in models])
    # 分类：投票（每行是一个样本，每列是一个模型）
    from scipy.stats import mode
    return mode(predictions, axis=0)[0].ravel()
```

### 2.2 为什么 Bagging 能降低方差？

假设 $T$ 个基学习器的方差均为 $\sigma^2$，两两之间的相关系数为 $\rho$，则集成的方差为：

$$\text{Var}(\text{ensemble}) = \rho \sigma^2 + \frac{1 - \rho}{T} \sigma^2$$

- 当 $\rho = 0$（模型完全独立）：方差降至 $\sigma^2 / T$（理想情况，但不可实现）
- 当 $\rho = 1$（模型完全一样）：方差仍为 $\sigma^2$（Bagging 无效果）

决策树对数据扰动敏感，不同 Bootstrap 样本上的树差异很大（$\rho$ 较小），因此方差能有效降低。

**重要性质**：Bagging **不增加偏差**。因为每棵树的偏差相同，平均后偏差不变。

### 2.3 随机森林的特征随机性

随机森林在 Bagging 的基础上增加了一层随机性：**在每个节点分裂时，只考虑特征的一个随机子集**。

- **分类**：通常考虑 $\sqrt{d}$ 个特征（$d$ 为总特征数）
- **回归**：通常考虑 $d/3$ 个特征

这进一步降低了树之间的相关性（$\rho$ 更小），从而更有效地降低方差。

```python
# 随机森林 vs 单棵决策树
rf = RandomForestClassifier(n_estimators=100, max_features='sqrt', random_state=42)
tree = DecisionTreeClassifier(random_state=42)
```

> 详见配套代码 `tree_ensemble.py` 中的 `compare_rf_vs_tree()`，该函数对比了随机森林和单棵决策树在 Iris 上的准确性差异，并展示了特征重要性。

### 2.4 OOB 误差（Out-of-Bag Error）

每个 Bootstrap 样本中，约有 $36.8\%$ 的样本未被抽中，这些样本称为 **OOB 样本**。可以用 OOB 样本评估模型性能，无需单独的验证集：

$$\text{OOB Error} = \frac{1}{N} \sum_{i=1}^N \mathbb{I}(y_i \neq \hat{y}_i^{\text{OOB}})$$

其中 $\hat{y}_i^{\text{OOB}}$ 是在所有未包含样本 $i$ 的树上投票得到的预测。

---

## 3. GBDT / XGBoost

### 3.1 Boosting vs Bagging

| | Bagging | Boosting |
|:---|:---|:---|
| **训练方式** | 并行训练多个模型 | 串行训练，每个模型纠正前一个的错误 |
| **目标** | 降低方差 | 同时降低偏差和方差 |
| **基学习器** | 强学习器（深树） | 弱学习器（浅树，通常 1-3 层） |
| **样本权重** | 均匀采样 | 动态调整，加大错分样本权重 |

### 3.2 Gradient Boosting 直觉

Gradient（/ˈɡreɪdiənt/） Boosting 的核心思想：**每一棵新树拟合的是前面所有树的残差（Residuals）**。

**逐步推导**：

1. 初始化：$\hat{y}^{(0)} = \bar{y}$（常数预测）
2. 计算残差：$r_i = y_i - \hat{y}_i^{(0)}$
3. 训练一棵树 $h_1(x)$ 拟合残差 $r_i$
4. 更新：$\hat{y}_i^{(1)} = \hat{y}_i^{(0)} + \eta \cdot h_1(x_i)$（$\eta$ 是学习率）
5. 重复：每一步的残差 $r_i = y_i - \hat{y}_i^{(t-1)}$，新树 $h_t$ 拟合这个残差

**为什么叫"Gradient" Boosting？**

残差 $y_i - \hat{y}_i$ 实际上是**均方误差损失函数的负梯度方向**：

$$\frac{\partial}{\partial \hat{y}_i} \frac{1}{2}(y_i - \hat{y}_i)^2 = -(y_i - \hat{y}_i)$$

所以拟合残差 = 沿着负梯度方向更新，等价于**梯度下降**——只不过是在函数空间而非参数（parameter /pəˈræmɪtər/）空间进行的梯度下降。

```python
# 伪代码：Gradient Boosting
def gradient_boosting(X, y, n_estimators=100, lr=0.1):
    models = []
    residual = y.copy()
    for _ in range(n_estimators):
        tree = DecisionTreeRegressor(max_depth=3)
        tree.fit(X, residual)        # 拟合残差
        residual -= lr * tree.predict(X)  # 更新残差
        models.append(tree)
    return models
```

### 3.3 XGBoost 的三大创新

XGBoost（eXtreme Gradient Boosting）是 GBDT 的高效工程实现，在 Kaggle 竞赛中长期占据统治地位。

#### 创新 1：正则化目标函数

传统的 GBDT 只最小化损失函数，XGBoost 加入了模型复杂度惩罚项：

$$\text{Obj} = \sum_{i=1}^n L(y_i, \hat{y}_i) + \sum_{t=1}^T \Omega(f_t)$$

其中 $\Omega(f) = \gamma T + \frac{1}{2}\lambda \sum_{j=1}^T w_j^2$

- $T$：叶节点数（控制树的复杂度）
- $w_j$：叶节点权重值
- $\gamma, \lambda$：正则化（regularization /ˌreɡjələraɪˈzeɪʃən/）超参数（hyperparameter /ˈhaɪpərpəˈræmɪtər/）

这相当于在 GBDT 基础上加了 **L2 正则化**（类似 Ridge Regression），有效防止过拟合。

#### 创新 2：二阶泰勒近似

传统 GBDT 使用一阶梯度（残差），XGBoost 使用**二阶泰勒展开**来近似损失函数：

$$L(y, \hat{y}^{(t)}) \approx L(y, \hat{y}^{(t-1)}) + g_i f_t(x_i) + \frac{1}{2} h_i f_t^2(x_i)$$

其中 $g_i = \partial_{\hat{y}} L(y_i, \hat{y}^{(t-1)})$ 是一阶梯度，$h_i = \partial_{\hat{y}}^2 L(y_i, \hat{y}^{(t-1)})$ 是二阶梯度。

使用二阶信息使优化更精准、收敛更快。

#### 创新 3：近似贪心算法（Approximate Greedy Algorithm）

当数据量很大时，遍历所有可能的分裂点不现实。XGBoost 使用**分位数近似**：

- 将连续特征分桶（如分成 100 个桶）
- 只在桶边界上评估分裂增益
- 支持加权分位数（Weighted Quantile Sketch），使损失大的样本获得更多"注意力（attention /əˈtenʃən/）"

此外，XGBoost 还包含：

| 特性 | 作用 |
|:---|:---|
| **列采样（Column Subsampling）** | 类似随机森林，降低过拟合 |
| **Shrinkage（学习率）** | 每棵树贡献乘以 $\eta$，留更多空间给后续树 |
| **并行化** | 在特征级别并行（树本身仍是串行的） |
| **处理缺失值** | 自动学习缺失值的最佳分裂方向 |

```python
# XGBoost 使用示例
model = XGBClassifier(n_estimators=100, max_depth=3, learning_rate=0.1,
                      reg_lambda=1.0, subsample=0.8, colsample_bytree=0.8,
                      eval_metric='logloss', random_state=42)
model.fit(X_train, y_train)
```

> 详见配套代码 `tree_ensemble.py` 中的 `compare_all_models()`，该函数在 Iris 数据集上对比了决策树、随机森林和 XGBoost 的精度。

---

## 4. 什么时候树模型打败深度学习？

虽然深度学习在图像、文本、语音等领域取得了巨大成功，但在许多场景下，树模型（尤其是 GBDT / XGBoost / LightGBM）仍然是最优选择：

### 4.1 树模型的优势

| 场景 | 为什么树模型更好 |
|:---|:---|
| **表格数据（Tabular Data）** | 表格数据通常包含混合类型（数值 + 类别），树模型天然处理非线性关系和特征交互 |
| **小样本数据** | 深度学习需要大量数据，树模型在几百到几万样本上就能表现很好 |
| **可解释性** | 特征重要性、SHAP 值、树结构可视化——树模型的决策过程透明可解释 |
| **训练效率** | 在 CPU 上即可快速训练，不需要 GPU |
| **无需特征缩放** | 树模型基于阈值分裂，不受特征尺度影响 |

### 4.2 典型的"树模型优先"场景

```
Kaggle 表格数据竞赛 → 90% 以上冠军方案使用 XGBoost / LightGBM / CatBoost
金融风控评分卡  → 逻辑回归（可解释性）或 GBDT（精度）
推荐系统 CTR 预估 → 深度学习（大规模）或 GBDT（中小规模）
医疗诊断辅助   → 树模型（可解释性要求高）
工业传感器异常检测 → 孤立森林（Isolation Forest，基于树的异常检测）
```

### 4.3 什么时候换深度学习？

- 数据量极大（百万级以上）
- 数据具有空间结构（图像、视频）
- 数据具有时序依赖（文本、语音、时间序列长程依赖）
- 需要端到端表示学习（无需手动特征工程）

---

## 总结

```
决策树 (Decision Tree)
  ├─ 单个模型，可解释但易过拟合
  ├─ 分裂标准：信息增益 / Gini 不纯度
  └─ 剪枝控制复杂度

随机森林 (Random Forest)
  ├─ Bagging + 特征随机性
  ├─ 降低方差，不增偏差
  ├─ OOB 误差天然验证
  └─ 适合中等规模表格数据

GBDT / XGBoost
  ├─ Boosting：串行纠正残差
  ├─ XGBoost：二阶梯度 + 正则化 + 近似分裂
  ├─ 精度通常最高（Kaggle 之王）
  └─ 适合结构化/表格数据
```

| 模型 | 偏差 | 方差 | 可解释性 | 训练速度 | 精度 |
|:---|:---:|:---:|:---:|:---:|:---:|
| 单棵决策树 | 低 | **高** | ★★★★★ | ★★★★★ | ★★★ |
| 随机森林 | 低 | 中 | ★★★★ | ★★★ | ★★★★ |
| XGBoost | **更低** | 中 | ★★★ | ★★★ | ★★★★★ |

> 下一章，我们将进入**无监督学习**的世界，探索聚类（K-Means, DBSCAN）和降维（PCA, t-SNE）的核心思想与实战。

## 参考文献 (References)

1. **Breiman, L. et al.** (1984). *Classification and Regression Trees*. Wadsworth. — CART 算法。
2. **Quinlan, J. R.** (1986). Induction of decision trees. *Machine Learning*, 1(1), 81–106. — ID3 算法。
3. **Freund, Y. & Schapire, R. E.** (1997). A decision-theoretic generalization of on-line learning and an application to boosting. *JCSS*, 55(1), 119–139. — AdaBoost 算法。
4. **Breiman, L.** (2001). Random forests. *Machine Learning*, 45(1), 5–32. — 随机森林。
5. **Chen, T. & Guestrin, C.** (2016). XGBoost: A scalable tree boosting system. *KDD*, 785–794. — XGBoost。
