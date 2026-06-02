# 05 — Your First ML Pipeline / 你的第一个机器学习流水线

> **Goal / 目标**: Run a complete end-to-end ML pipeline without getting lost in math.
> **目的**: 不陷入数学细节，完整跑通一个端到端的机器学习流水线。

We'll build a classifier that identifies **Iris flower species** (setosa, versicolor, virginica) based on 4 measurements. This is the "Hello World" of ML.

我们将训练一个分类（classification /ˌklæsɪfɪˈkeɪʃən/）器，根据 4 个测量值识别 **鸢尾花种类**（setosa、versicolor、virginica）。这是机器学习界的 "Hello World"。

---

## Pipeline Overview / 流水线总览

```
Load Data → EDA → Train/Test Split → Standardize → Train → Predict → Evaluate → Visualize → Save
 加载数据    探索分析    划分训练/测试      标准化      训练     预测      评估      可视化     保存
```

---

## Step 1: Load Data / 加载数据

```python
iris = load_iris()
X = iris.data       # features: 150 samples × 4 columns
y = iris.target     # labels: 0, 1, 2
```

**What's happening? / 这里发生了什么？**

We load the Iris dataset — a built-in dataset in `sklearn`. It contains **150 flowers**, each described by **4 measurements**:
- Sepal length (花萼长度)
- Sepal width (花萼宽度)
- Petal length (花瓣长度)
- Petal width (花瓣宽度)

Each flower is labeled as one of **3 species** (setosa = 0, versicolor = 1, virginica = 2).

我们从 `sklearn` 内置数据集中加载鸢尾花数据。共 **150 朵花**，每朵有 **4 个测量值**，分属 **3 个品种**。

**The data comes ready to use.** No downloading, no cleaning, no missing values — perfect for learning.

**数据拿来即用。** 不需要下载、清洗、处理缺失值——非常适合学习。

---

## Step 2: Exploratory Data Analysis (EDA) / 探索性数据分析

```python
print(X.shape)        # (150, 4)
print(iris.feature_names)
print(iris.target_names)
```

**What's happening? / 这里发生了什么？**

Before building anything, we **look at the data**: How many samples? How many features? Is the data balanced (equal samples per class)?

在建模之前，我们先 **看看数据长什么样**：有多少样本？多少特征？类别分布是否均衡？

> 这就像去菜市场买菜之前先看一下菜长什么样——烂叶子要先摘掉，但 Iris 数据集很干净，我们只需要熟悉一下。

**Why this matters / 为什么重要**: If a dataset has 90% class A and 10% class B, a "model" that always predicts A gets 90% accuracy — but is useless. EDA catches issues like this upfront.

如果数据集 90% 是 A 类、10% 是 B 类，一个"模型"永远猜 A 也能有 90% 准确率——但这毫无用处。EDA 可以在动手之前就发现这类问题。

---

## Step 3: Train / Test Split / 划分训练集和测试集

```python
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)
```

**What's happening? / 这里发生了什么？**

We **split our data** into two parts:
- **Training set (80%)**: The model learns from this.
- **Test set (20%)**: We keep this hidden until the end to see how well the model generalizes.

我们把数据 **分成两份**：
- **训练集 (80%)**：模型从这部分学习。
- **测试集 (20%)**：这部分藏到最后才拿出来，用来检验模型对新数据的泛化能力。

**Why split? / 为什么需要划分？**

Imagine studying for an exam by memorizing the answer key. You'd get 100% on the practice test — but fail the real exam because you never learned the *underlying patterns*.

这就像考试前背答案——模拟考能拿 100 分，但真实考试会一塌糊涂，因为你根本没学会 *背后的规律*。

> 我们把测试集"藏起来"，模拟模型遇到从未见过的新数据时的表现。

**`stratify=y`** ensures the same class ratio in both sets. If the original data is 33% / 33% / 33%, the split preserves that.

**`stratify=y`** 保证训练集和测试集里的类别比例和原始数据一致。

**`random_state=42`** makes the split reproducible. Run it twice, get the same split.
**`random_state=42`** 使划分结果可复现。跑两次，得到一样的划分。

---

## Step 4: Standardize Features / 标准化特征

```python
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)
```

**What's happening? / 这里发生了什么？**

**Standardization** transforms each feature so that it has **mean = 0** and **standard deviation = 1**.

**标准化**将每个特征变换为 **均值 = 0**、**标准差 = 1**。

```
Before:  sepal_length=5.1,  petal_width=0.2  (very different scales)
After:   sepal_length=0.1,  petal_width=-1.2 (comparable scales)
```

**Why standardize? / 为什么需要标准化？**

Many ML models (including Logistic Regression（/rɪˈɡreʃən/）) are sensitive to the **scale** of features. A feature measured in millimeters (like petal width: 0.2 cm) would have tiny numerical values compared to sepal length (5.1 cm). The model might incorrectly treat the larger-numbered feature as "more important."

很多 ML 模型（包括逻辑回归）对特征的 **尺度** 敏感。如果花瓣宽度 0.2 cm，花萼长度 5.1 cm，数值差距很大，模型可能会错误地认为数值大的特征"更重要"。

> Standardization puts all features on an equal playing field. It's like converting currencies to the same unit before comparing prices.

> 标准化把所有特征拉到同一水平线上——就像比较价格前先换算成同一种货币。

**Fit on train, transform on test / 在训练集上拟合，在测试集上变换**:
- `fit_transform(X_train)`: Learn the mean/std from training data **only**.
- `transform(X_test)`: Apply **the same** transformation to test data.

This is *critical*: the test set must be transformed using training-set statistics, not its own. Otherwise you're "cheating" by letting the test set influence preprocessing.

这 *至关重要*：测试集必须用训练集的统计量来变换，而不能用自己的。否则测试集就"作弊"了，因为它影响了预处理。

---

## Step 5: Train Model / 训练模型

```python
model = LogisticRegression(max_iter=200, random_state=42)
model.fit(X_train_scaled, y_train)
```

**What's happening? / 这里发生了什么？**

**Training = finding the best parameters.** The model starts with random parameters and iteratively adjusts them to make better predictions on the training data.

**训练 = 找到最佳参数（parameter /pəˈræmɪtər/）。** 模型从随机（stochastic /stəˈkæstɪk/）参数开始，反复调整，使在训练数据上的预测越来越好。

> Think of tuning a guitar: you don't get the perfect pitch on the first try. You pluck, listen, adjust, pluck again — until each string sounds right.

> 就像调吉他：你不可能一次就调到完美音高。你要拨弦、听音、调整、再拨弦——直到每根弦的音准都对。

**Logistic Regression** is a linear model for classification. It learns a **decision boundary** — a line (or hyperplane) that separates the classes.

**逻辑回归** 是一种用于分类的线性模型。它学习一个 **决策边界**——一条分隔不同类别的直线（或超平面）。

---

## Step 6: Predict / 预测

```python
y_pred = model.predict(X_test_scaled)
```

**What's happening? / 这里发生了什么？**

The trained model takes the **test features** it has never seen and outputs its **best guess** for each one.

训练好的模型拿到 **从未见过的测试特征**，对每个样本输出 **最佳猜测**。

The model also computes **confidence scores** (`predict_proba`) — how sure it is about each prediction.

模型还会计算 **置信度**（`predict_proba`）——对每个预测有多确定。

---

## Step 7: Evaluate / 评估

```python
accuracy = accuracy_score(y_test, y_pred)
print(classification_report(y_test, y_pred))
print(confusion_matrix(y_test, y_pred))
```

**What's happening? / 这里发生了什么？**

We compare the model's predictions (`y_pred`) against the **true labels** (`y_test`) that we kept hidden.

我们拿模型的预测结果（`y_pred`）和之前 **藏起来的真实标签**（`y_test`）做对比。

### Metrics / 评估指标

| Metric / 指标 | Chinese / 中文 | What it tells us / 告诉我们什么 |
|---|---|---|
| **Accuracy** | 准确率 | Overall: what fraction did we get right? 总体来看，猜对了多少？ |
| **Precision** | 精确率 | When the model says "class A", how often is it right? 模型说是 A 类时，正确率多高？ |
| **Recall** | 召回率 | Of all actual class A samples, how many did the model catch? 实际是 A 类的样本中，模型找出了多少？ |
| **F1-score** | F1 分数 | Harmonic mean of precision & recall. 精确率和召回率的调和平均。 |

### Confusion Matrix / 混淆矩阵

```
              Predicted:
              Setosa  Versicolor  Virginica
Actual:
  Setosa        10         0          0
  Versicolor     0         9          1
  Virginica      0         0         10
```

- **Diagonal** (左上到右下): Correct predictions — this is what we want.
- **Off-diagonal**: Mistakes — where the model got confused.

- **对角线**：预测正确——这是我们想要的。
- **非对角线**：预测错误——模型在这里搞混了。

> A confusion matrix shows *what kinds of mistakes* the model makes. Two models with the same accuracy can make very different errors.

> 混淆矩阵展示了模型犯了 *什么类型的错误*。两个准确率相同的模型，犯的错误可能完全不同。

---

## Step 8: Visualize / 可视化

```python
sns.heatmap(cm, annot=True, fmt="d", cmap="Blues")
```

**What's happening? / 这里发生了什么？**

A picture is worth a thousand numbers. We generate:
- **Confusion matrix heatmap**: Makes the numbers above instantly readable.
- **Decision boundary plot**: Shows how the model separates classes in 2D space.

一张图胜过一千个数字。我们生成了：
- **混淆矩阵热力图**：让上面的数字一目了然。
- **决策边界图**：展示模型在二维空间中是如何分隔类别的。

---

## Step 9: Save Model / 保存模型

```python
joblib.dump(model, "iris_logistic_regression.joblib")
```

**What's happening? / 这里发生了什么？**

Training is done. We **serialize** the trained model to disk so we can:
- Load it later without retraining.
- Deploy it in a web app or API.
- Share it with teammates.

训练完成了。我们把训练好的模型 **保存到磁盘**，以后可以：
- 直接加载，无需重新训练。
- 部署到 Web 应用或 API 中。
- 分享给团队成员。

---

## Summary / 总结

| Step | What you did | Why it matters |
|---|---|---|
| 1. Load Data | `load_iris()` | Get data into Python |
| 2. EDA | `print(X.shape, ...)` | Understand what you're working with |
| 3. Split | `train_test_split()` | Prevent overfitting（/ˈoʊvərˈfɪtɪŋ/） by holding out test data |
| 4. Standardize | `StandardScaler()` | Put all features on the same scale |
| 5. Train | `model.fit()` | Learn patterns from training data |
| 6. Predict | `model.predict()` | Apply learned patterns to new data |
| 7. Evaluate | `accuracy_score()`, `confusion_matrix()` | Quantify how well the model performs |
| 8. Visualize | `sns.heatmap()` | Spot patterns and errors visually |
| 9. Save | `joblib.dump()` | Persist the model for future use |

**This is the ML pipeline.** The exact same pattern — with different datasets, different models, different parameters — applies to 80% of real-world ML problems. Master this flow, and you have the foundation for everything else.

**这就是 ML 流水线。** 同样的模式——换不同的数据集、不同的模型、不同的参数——可以应用到 80% 的真实 ML 问题中。掌握了这个流程，你就有了后续学习的所有基础。

> "First, learn the rhythm. The improvisation comes later."
> "先学会节奏，再谈即兴发挥。"

---

## Run It / 运行

```bash
# Make sure you're in the project root
python ai/01-overview/05-first-ml-pipeline.py
```

Expected output: console logs + two PNG files in `ai/01-overview/output/`.

预期输出：控制台日志 + `ai/01-overview/output/` 目录下的两张 PNG 图片。
