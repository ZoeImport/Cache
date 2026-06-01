# AI/ML 技术百科全书 — 实施计划

## TL;DR

> **Quick Summary**: 在 love-story 项目的 `/ai/` 目录下创建一套 10 卷 50+ 章的渐进式 AI/ML 技术文档体系（含可运行代码），从零基础到 OpenCode 工具链集成。
>
> **Deliverables**:
> - `/ai/` 目录下的完整文档树（10个子目录，50+个 `.md` 文件）
> - 每章配套的可运行 Python 代码
> - 全局 `requirements.txt` 依赖管理
> - 每章经过 Oracle 事实校对 + Momus 对抗式审查
>
> **Estimated Effort**: XL（预计 50+ 章节书写任务）
> **Parallel Execution**: YES - 10 waves（卷间串行，卷内章节可并行）
> **Critical Path**: 卷1→卷2→卷3→...→卷10（强依赖链）

---

## Context

### Original Request
用户在 love-story 项目中创建一套涵盖神经网络、机器学习、自监督学习、生成式AI、数学推导、模型训练、Agent Harness、Prompt Engineering、工具链集成的完整技术体系。

### Interview Summary
**Key Decisions**:
- **语言**: 中英双语，难翻译术语英文为主+中文注释
- **学习路径**: 从底向上10卷（Python→数学→ML→NN→Transformer→SSL→GenAI→训练→LLM应用→工具链）
- **深度**: 教科书风格（数学推导+理论证明+可运行代码）
- **结构**: `/ai/` 下多文件目录
- **验证**: Oracle 每章校对 + Momus 高精度对抗式审查
- **代码验证**: 每次提交前运行 Python 验证

**Scope OUT**:
- 硬件/GPU编程、非Python框架、生产MLOps、云平台教程、商业产品评测
- 非Transformer架构的全面覆盖（Mamba等仅作补充阅读）

---

## Work Objectives

### Core Objective
在 `/ai/` 目录下创建一套从零基础到 AI 工具链集成的 10 卷渐进式学习体系。

### Concrete Deliverables
- 10 个卷目录，每卷包含 00-index.md + N 个章节 .md 文件 + code/ 子目录
- 全局 requirements.txt + 每卷 requirements-xx.txt
- 50+ 个独立章节文件，每个经过 Oracle + Momus 双重验证
- 每章配套 Python 可运行代码
- `ai/00-README.md` 总入口 + 学习路径图

### Definition of Done
- [ ] 所有 `.py` 文件通过 `python -m py_compile` 语法验证
- [ ] 所有 Mermaid 图表语法正确
- [ ] Oracle 校对报告无 ERR 级问题
- [ ] Momus 审查对每章返回 OKAY
- [ ] 交叉引用完整性检查通过
- [ ] 无伪代码或不可运行代码片段

### Must Have
- 理论概念100%准确（经过 Oracle 逐段验证）
- 所有代码真实可运行
- 每章有 TL;DR、核心概念、正文、代码、参考来源
- 中英双语术语规范

### Must NOT Have (Guardrails)
- 禁止伪代码或不可运行的代码片段
- 禁止虚构的学术引用（每篇引用必须可查证）
- 禁止已定稿卷的未审查修改
- 禁止在已确认的 Scope OUT 范围内展开
- 禁止 torch/TF 等库版本不锁定

---

## Verification Strategy

> **ZERO HUMAN INTERVENTION** - ALL verification is agent-executed. No exceptions.

### QA Pipeline (每章)

```
Write draft → Oracle facts check → Fix ERR/AMB → Momus adversarial review
  → Fix until OKAY → Run all .py files → Write to final path
```

### 每章 QA Scenarios

**Scenario 1: Oracle Fact Verification**
- Tool: Oracle agent
- Steps: Submit full chapter → Oracle checks each formula, each claim → Return ERR/AMB list
- Expected: Zero ERR-level issues. AMB issues all addressed.

**Scenario 2: Momus Adversarial Review**
- Tool: Momus agent
- Steps: Submit chapter file path → Momus scrutinizes clarity, verifiability, completeness
- Expected: Verdict = OKAY (not REJECTED)

**Scenario 3: Python Code Runnable**
- Tool: Bash
- Steps: `cd ai/XX-xxx/code/ && python chapter_YY.py`
- Expected: Runs without error, produces expected output

**Scenario 4: Cross-Reference Check**
- Tool: Bash/grep
- Steps: `grep -r '](\.\./' ai/ | grep -v 'http'` → verify all internal links exist
- Expected: All internal links resolve to existing files

---

## Execution Strategy

### Dependency Chain

```
Vol 1 (Overview+Python)  ← 无依赖
  ↓
Vol 2 (Mathematics)      ← 依赖 Vol 1 Python 基础
  ↓
Vol 3 (Classical ML)     ← 依赖 Vol 2 数学
  ↓
Vol 4 (Neural Networks)   ← 依赖 Vol 3 学习概念
  ↓
Vol 5 (Transformer)       ← 依赖 Vol 4 NN 基础
  ↓
Vol 6 (Self-supervised)   ← 依赖 Vol 5 Transformer
  ↓
Vol 7 (Generative AI)     ← 依赖 Vol 5+6
  ↓
Vol 8 (Model Training)    ← 依赖 Vol 4+7
  ↓
Vol 9 (LLM Applications)  ← 依赖 Vol 7 LLM 部分
  ↓
Vol 10 (Toolchain)        ← 依赖 Vol 9
```

### Parallel Execution Waves

```
Wave 0 (Setup — 1 task):
└── Task 1: Create directory structure + requirements.txt + README

Wave 1 (Vol 1 Overview — up to 5 parallel tasks):
├── Task 2: 01-intro-to-ai-world.md
├── Task 3: 02-python-quickstart.md
├── Task 4: 03-numpy-and-linalg.md
├── Task 5: 04-visualization.md
└── Task 6: 05-first-ml-pipeline.py
  (All can be parallel — same volume, shared foundation)

Wave 2 (Vol 2 Math — up to 5 parallel):
├── Task 7: 01-linear-algebra.md
├── Task 8: 02-probability.md
├── Task 9: 03-calculus-and-optimization.md
├── Task 10: 04-information-theory.md
└── Task 11: 05-statistics-basics.md

Wave 3 (Vol 3 Classical ML — up to 6 parallel):
├── Task 12: 01-linear-models.md
├── Task 13: 02-model-evaluation.md
├── Task 14: 03-tree-and-ensemble.md
├── Task 15: 04-svm-and-kernel.md
├── Task 16: 05-unsupervised-learning.md
└── Task 17: 06-ml-project-template.py

Wave 4 (Vol 4 Neural Networks — up to 5 parallel):
├── Task 18: 01-perceptron-and-mlp.md
├── Task 19: 02-backpropagation.md
├── Task 20: 03-training-techniques.md
├── Task 21: 04-convolutional-networks.md
└── Task 22: 05-rnn-and-sequence.md

Wave 5 (Vol 5 Transformer — up to 4 parallel):
├── Task 23: 01-attention-mechanism.md
├── Task 24: 02-transformer-architecture.md
├── Task 25: 03-variants-evolution.md
└── Task 26: 04-implement-transformer.py

Wave 6 (Vol 6 SSL — up to 5 parallel):
├── Task 27: 01-pretraining-paradigm.md
├── Task 28: 02-contrastive-learning.md
├── Task 29: 03-masked-modeling.md
├── Task 30: 04-autoregressive-modeling.md
└── Task 31: 05-pretrain-finetune.py

Wave 7 (Vol 7 GenAI — up to 5 parallel):
├── Task 32: 01-vae.md
├── Task 33: 02-gan.md
├── Task 34: 03-diffusion-models.md
├── Task 35: 04-large-language-models.md
└── Task 36: 05-lora-and-finetuning.md

Wave 8 (Vol 8 Training — up to 6 parallel):
├── Task 37: 01-pytorch-deep-dive.md
├── Task 38: 02-training-loop-mastery.md
├── Task 39: 03-distributed-training.md
├── Task 40: 04-data-pipeline.md
├── Task 41: 05-deployment-basics.md
└── Task 42: 06-python-ml-ecosystem.md

Wave 9 (Vol 9 LLM App — up to 5 parallel):
├── Task 43: 01-prompt-engineering.md
├── Task 44: 02-rag.md
├── Task 45: 03-tool-calling.md
├── Task 46: 04-agent-systems.md
└── Task 47: 05-evaluation-and-monitoring.md

Wave 10 (Vol 10 Toolchain — up to 6 parallel):
├── Task 48: 01-ai-coding-assistants.md
├── Task 49: 02-agent-harness-deep-dive.md
├── Task 50: 03-mcp-and-tools.md
├── Task 51: 04-skill-and-prompt-system.md
├── Task 52: 05-build-your-own-tool.md
└── Task 53: 06-conclusion-and-roadmap.md

Wave FINAL (After ALL tasks — 4 parallel reviews, then user okay):
├── Task F1: Plan compliance audit (oracle)
├── Task F2: Code quality review (unspecified-high)
├── Task F3: Real QA — run ALL code (unspecified-high)
└── Task F4: Scope fidelity check (deep)
-> Present results -> Get explicit user okay

Critical Path: Wave 0 → Wave 1 → Wave 2 → ... → Wave 10 → F1-F4 → user okay
```

---

## TODOs

- [x] 1. **项目初始化 — 创建 AI 文档体系骨架**

  **What to do**:
  - 创建 `/ai/` 目录及所有 10 个子卷目录
  - 每个子卷目录创建 `code/` 子目录
  - 创建 `ai/requirements.txt`（全局依赖：torch, transformers, numpy, scipy, scikit-learn, matplotlib, accelerate, wandb, langchain, datasets, httpx）
  - 创建 `ai/00-README.md`（总入口，含学习路径 Mermaid 图、说明、卷索引表）
  - 设置 `.gitignore` 忽略 `__pycache__/`, `*.pyc`, `wandb/`, `.ipynb_checkpoints/`

  **Must NOT do**:
  - 不要安装依赖（由执行代理按需安装）
  - 不要创建任何 .py 或 .md 的内容文件（只创建目录和入口）

  **Recommended Agent Profile**:
  - **Category**: `quick`
    - Reason: 纯文件系统操作，需要快速的目录创建和入口文件生成

  **Parallelization**:
  - **Can Run In Parallel**: NO（独立任务）
  - **Blocks**: 所有后续任务

  **Acceptance Criteria**:
  - [ ] `ai/` 目录存在，包含 10 个子卷目录
  - [ ] 每个子卷目录下有 `code/` 子目录
  - [ ] `ai/requirements.txt` 包含所有必需依赖
  - [ ] `ai/00-README.md` 可读且包含正确的学习路径图

- [x] 2. **Vol 1/Ch 1: AI 世界全景图 — intro-to-ai-world.md**

  **What to do**:
  - 撰写 AI/ML/DL/GenAI/Agent 的概念辨析
  - 整个 AI 领域的"族谱"树形图（Mermaid）
  - 学习路径总地图（Mermaid 流程图）
  - 不同职业路径的推荐策略
  - 中英双语：专业术语首次出现标注英文
  - **写完后**: 提交 Oracle 事实校对 → 修复问题 → 提交 Momus 对抗式审查 → 修复直到 OKAY

  **Must NOT do**:
  - 不要包含任何 Python 代码（这不是教学章）
  - 不要写具体算法细节（这是全景图不是深度教程）

  **Recommended Agent Profile**:
  - **Category**: `writing`
    - Reason: 需要清晰的概念辨析和有感染力的全景描述，重点是写作质量而非技术实现

  **Parallelization**:
  - **Can Run In Parallel**: YES（同 Wave 1 的其他任务）
  - **Parallel Group**: Wave 1（Tasks 2-6）
  - **Blocks**: 无
  - **Blocked By**: Task 1（目录结构）

  **QA Scenarios**:
  ```
  Scenario: 全景图完整性检查
    Tool: Bash (grep + file check)
    Steps:
      1. 检查文件存在: ls ai/01-overview/01-intro-to-ai-world.md
      2. 检查 Mermaid 代码块存在: grep -c '\`\`\`mermaid' ai/01-overview/01-intro-to-ai-world.md
      3. 检查中英双语: 至少找到 3 处 "（英文术语）" 模式
    Expected: 文件存在，≥1 个 Mermaid 图，≥3 处中英术语标注
    Evidence: .omo/evidence/task-2-intro-check.txt
  ```

- [x] 3. **Vol 1/Ch 2: Python 快速入门 — python-quickstart.md**

  **What to do**:
  - Python 环境搭建指引（conda/venv/uv 三种选择）
  - 核心语法速成（20%语法覆盖80%场景）：数据类型、控制流、函数、列表推导、上下文管理器
  - 面向对象编程速览（够用程度）
  - ⚡ 配套代码：`code/python_quickstart.py`
  - **Oracle + Momus 双重验证**

  **Must NOT do**:
  - 不要写完整的 Python 教程（只写 ML 需要的部分）
  - 不要写 Django/Flask/Web 相关内容

  **Recommended Agent Profile**:
  - **Category**: `writing`
    - Reason: 需要精炼提取 Python 的核心子集，写作质量比技术难度更重要

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Blocked By**: Task 1

  **QA Scenarios**:
  ```
  Scenario: Python 代码可运行
    Tool: Bash
    Preconditions: pip install -r requirements.txt
    Steps: python ai/01-overview/code/python_quickstart.py
    Expected: 无报错，输出正确
    Evidence: .omo/evidence/task-3-python-run.txt
  ```

- [x] 4. **Vol 1/Ch 3: NumPy 与张量思维 — numpy-and-linalg.md**

  **What to do**:
  - ndarray 基础与向量化计算
  - Broadcasting 机制详解（含可视化解释）
  - 线性代数运算（dot, matmul, svd, eig）
  - ⚡ 配套代码：`code/numpy_basics.py` + `code/linalg_demo.py`
  - 实战：用 NumPy 手写 KNN 分类器
  - **Oracle + Momus 双重验证**

  **Must NOT do**:
  - 不要覆盖 Pandas/DataFrame（那是数据处理不是张量）

  **Recommended Agent Profile**:
  - **Category**: `unspecified-high`
    - Reason: 需要兼顾数学概念解释和代码实现，有一定技术复杂度

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Blocked By**: Task 1

- [x] 5. **Vol 1/Ch 4: 数据可视化入门 — visualization.md**

  **What to do**:
  - Matplotlib 核心 API（figure, axes, subplots）
  - 常见图表类型：折线图、散点图、柱状图、热力图
  - ML 专用可视化：损失曲线、混淆矩阵、ROC曲线、特征分布
  - ⚡ 配套代码：`code/visualization_demo.py`
  - **Oracle + Momus 双重验证**

  **Recommended Agent Profile**:
  - **Category**: `visual-engineering`
    - Reason: 涉及图表生成和可视化布局，需要视觉合理性和代码正确性

  **Parallelization**:
  - **Can Run In Parallel**: YES（Wave 1）
  - **Blocked By**: Task 1

- [x] 6. **Vol 1/Ch 5: 第一个完整 ML 项目 — first-ml-pipeline.py**

  **What to do**:
  - 用 Iris 数据集完成完整 ML 流程
  - 数据加载 → 探索性分析 → 训练/测试分割 → 模型训练 → 评估 → 可视化
  - 不深究原理，只感受完整流程
  - 创建配套 `.md` 引导文件（`05-first-ml-pipeline.md`）解释每一步在做什么
  - **Oracle + Momus 双重验证**

  **Must NOT do**:
  - 不要解释算法原理（这是体验流程不是教学）

  **Recommended Agent Profile**:
  - **Category**: `unspecified-low`
    - Reason: 标准的 sklearn 流程，技术路线明确

  **Parallelization**:
  - **Can Run In Parallel**: YES（Wave 1）
  - **Blocked By**: Task 1

- [x] 7. **Vol 2/Ch 1: 线性代数 — linear-algebra.md**

  **What to do**:
  - 向量与向量空间（几何直观 + 数学定义）
  - 矩阵及其运算：乘法、转置、逆、行列式
  - 特征值与特征向量（PCA的前置理论）
  - 奇异值分解 SVD（推荐系统/降维的理论基础）
  - 矩阵微积分（梯度推导的前置）
  - ⚡ 配套代码：`code/linear_algebra_demo.py`
  - 每次讲解配合 NumPy 代码验证结果
  - **Oracle + Momus 双重验证**

  **Must NOT do**:
  - 不要按数学系标准写完整线性代数（只覆盖 ML 需要的部分）

  **Recommended Agent Profile**:
  - **Category**: `unspecified-high`
    - Reason: 需要精确的数学推导和代码验证，中英双语术语
    - **Skills**: Need `context7_query-docs` for numpy API verification

  **Parallelization**:
  - **Can Run In Parallel**: YES（Wave 2）
  - **Blocked By**: Task 1, Task 3（Python/NumPy 基础）

- [x] 8. **Vol 2/Ch 2: 概率论 — probability.md**

  **What to do**:
  - 概率分布：正态、伯努利、二项、多项分布
  - 条件概率与贝叶斯定理（含完整推导）
  - 最大似然估计 MLE 和最大后验估计 MAP（含推导）
  - 期望、方差、协方差
  - ⚡ 配套代码：`code/probability_demo.py`（scipy.stats 验证每个概念）
  - **Oracle + Momus 双重验证**

  **Recommended Agent Profile**:
  - **Category**: `unspecified-high`
  - **Parallelization**: YES（Wave 2）
  - **Blocked By**: Task 1

- [x] 9. **Vol 2/Ch 3: 微积分与优化 — calculus-and-optimization.md**

  **What to do**:
  - 偏导数与梯度（几何意义可视化）
  - 链式法则（反向传播的核心，详细步骤推导）
  - 梯度下降法原理与证明
  - 常见优化器直觉：SGD → Momentum → Adam
  - ⚡ 配套代码：`code/gradient_descent_demo.py`（手写梯度下降拟合线性回归）
  - **Oracle + Momus 双重验证**

  **Recommended Agent Profile**:
  - **Category**: `unspecified-high`
  - **Parallelization**: YES（Wave 2）
  - **Blocked By**: Task 1

- [x] 10. **Vol 2/Ch 4: 信息论 — information-theory.md**

  **What to do**:
  - 自信息与熵 Entropy（直观理解+数学定义）
  - KL 散度（衡量两个分布的差异）
  - 交叉熵（分类损失函数的由来，完整推导链）
  - 互信息（特征选择的依据）
  - ⚡ 配套代码：`code/information_demo.py`（可视化熵与 KL 散度）
  - **Oracle + Momus 双重验证**

  **Recommended Agent Profile**:
  - **Category**: `unspecified-high`
  - **Parallelization**: YES（Wave 2）
  - **Blocked By**: Task 1

- [x] 11. **Vol 2/Ch 5: 统计学基础 — statistics-basics.md**

  **What to do**:
  - 偏差-方差权衡（过拟合的理论解释，含推导）
  - 参数估计与假设检验基础
  - 置信区间
  - Bootstrap 重采样方法
  - ⚡ 配套代码：`code/statistics_demo.py`
  - **Oracle + Momus 双重验证**

  **Recommended Agent Profile**:
  - **Category**: `unspecified-high`
  - **Parallelization**: YES（Wave 2）
  - **Blocked By**: Task 1

- [ ] 12. **Vol 3/Ch 1: 线性模型 — linear-models.md**

  **What to do**:
  - 线性回归：最小二乘法（◄ 来自 MLE 推导）
  - 逻辑回归：Sigmoid + 交叉熵（◄ 来自信息论）
  - 正则化：L1/Lasso, L2/Ridge
  - 从线性模型引出核心三概念：**参数、损失、梯度**
  - ⚡ 配套代码：`code/linear_models.py`（手写 Linear + Logistic Regression）
  - 📈 可视化损失面、决策边界、正则化效果
  - **Oracle + Momus 双重验证**

  **Must NOT do**:
  - 不要跳过推导直接给公式（这是理解"学习"本质的关键章节）

  **Recommended Agent Profile**:
  - **Category**: `unspecified-high`
    - Reason: 需要从数学公式到代码的完整映射，是 ML 入门最关键章节

  **Parallelization**:
  - **Can Run In Parallel**: YES（Wave 3）
  - **Blocked By**: Task 7（线性代数）, Task 8（概率论MLE）

- [ ] 13. **Vol 3/Ch 2: 模型评估与验证 — model-evaluation.md**

  **What to do**:
  - 过拟合 vs 欠拟合：核心直觉 + 可视化
  - 训练/验证/测试集划分原则
  - K-Fold 交叉验证
  - 偏差-方差权衡（用实际数据可视化）
  - 学习曲线（诊断模型状态的工具）
  - ⚡ 配套代码：`code/model_evaluation.py`（学习曲线可视化）
  - **Oracle + Momus 双重验证**

  **Recommended Agent Profile**:
  - **Category**: `unspecified-high`
  - **Parallelization**: YES（Wave 3）
  - **Blocked By**: Task 12（线性模型）

- [ ] 14. **Vol 3/Ch 3: 树模型与集成学习 — tree-and-ensemble.md**

  **What to do**:
  - 决策树：信息增益、基尼系数（◄ 来自信息论）
  - 随机森林：Bagging 思想
  - GBDT / XGBoost：Boosting 思想
  - 为什么树模型在表格数据上仍然最好
  - ⚡ 配套代码：`code/tree_ensemble.py`（sklearn 完整分类任务）
  - **Oracle + Momus 双重验证**

  **Recommended Agent Profile**:
  - **Category**: `unspecified-low`
    - Reason: 标准 sklearn API 调用，技术路线确定

  **Parallelization**:
  - **Can Run In Parallel**: YES（Wave 3）
  - **Blocked By**: Task 12（线性模型作为前置概念）

- [ ] 15. **Vol 3/Ch 4: SVM 与核方法 — svm-and-kernel.md**

  **What to do**:
  - 最大间隔分类器（几何直观 + 数学推导）
  - 对偶问题（简要推导）
  - 核技巧 Kernel Trick（关键洞察：隐式高维映射）
  - 常见核函数：RBF、多项式
  - ⚡ 配套代码：`code/svm_demo.py`（可视化核函数效果）
  - **Oracle + Momus 双重验证**

  **Recommended Agent Profile**:
  - **Category**: `unspecified-high`
    - Reason: 对偶问题和核技巧需要清晰的数学解释和可视化

  **Parallelization**:
  - **Can Run In Parallel**: YES（Wave 3）
  - **Blocked By**: Task 12

- [ ] 16. **Vol 3/Ch 5: 无监督学习 — unsupervised-learning.md**

  **What to do**:
  - K-Means 聚类（EM 思想的雏形）
  - PCA（◄ 来自 SVD 的理论基础）
  - t-SNE 与 UMAP（高维数据可视化）
  - 高斯混合模型 GMM
  - ⚡ 配套代码：`code/unsupervised_demo.py`（PCA 降维 + 可视化）
  - **Oracle + Momus 双重验证**

  **Recommended Agent Profile**:
  - **Category**: `unspecified-high`
  - **Parallelization**: YES（Wave 3）
  - **Blocked By**: Task 7（SVD 数学基础）, Task 12

- [ ] 17. **Vol 3/Ch 6: ML 项目模板 — ml-project-template.py**

  **What to do**:
  - 创建可复用的完整 ML 项目模板
  - 涵盖：数据加载 → 预处理 → 训练 → 调参 → 评估 → 保存
  - 可复用到未来任何 ML 任务
  - 创建配套 `.md` 解释文件（`06-ml-project-template.md`）
  - **Oracle + Momus 双重验证**

  **Recommended Agent Profile**:
  - **Category**: `unspecified-low`
    - Reason: 标准工程模板，不需创新

  **Parallelization**:
  - **Can Run In Parallel**: YES（Wave 3）
  - **Blocked By**: Task 12-16（整合前三卷的知识）

- [ ] 18. **Vol 4/Ch 1: 感知机与 MLP — perceptron-and-mlp.md**

  **What to do**:
  - 感知机：历史上第一个学习算法
  - 多层感知机 MLP：为什么需要"深"
  - 激活函数：Sigmoid/Tanh/ReLU/GELU/SwiGLU（数学定义+导数+可视化对比）
  - 万能近似定理（理解为什么神经网络可以拟合任何函数）
  - ⚡ 配套代码：`code/perceptron_mlp.py`（NumPy 手写 MLP 前向传播）
  - **Oracle + Momus 双重验证**

  **Recommended Agent Profile**:
  - **Category**: `deep`
    - Reason: 神经网络的数学基础，需要从感知机收敛证明到万能近似定理的完整论证链

  **Parallelization**:
  - **Can Run In Parallel**: YES（Wave 4）
  - **Blocked By**: Task 7（线性代数）, Task 9（微积分）

- [ ] 19. **Vol 4/Ch 2: 反向传播 — backpropagation.md** ⭐

  **What to do**:
  - 计算图：Autograd 的底层原理
  - 链式法则的递归应用（完整推导 + 数值验证）
  - 全连接层的反向传播：手算 + 代码
  - 梯度消失与梯度爆炸
  - ⚡ 配套代码：`code/backpropagation.py`（NumPy 手写反向传播 + 梯度检验）
  - 📈 可视化：计算图、梯度流
  - **Oracle + Momus 双重验证**

  **Must NOT do**:
  - 不要跳过中间推导步骤（这是整个深度学习最核心的算法）

  **Recommended Agent Profile**:
  - **Category**: `ultrabrain`
    - Reason: 反向传播是整个深度学习的核心引擎，推导必须精确无误，每一步都需要验证。需要最高的推理质量

  **Parallelization**:
  - **Can Run In Parallel**: YES（Wave 4）
  - **Blocked By**: Task 18

- [ ] 20. **Vol 4/Ch 3: 训练技巧 — training-techniques.md**

  **What to do**:
  - 权重初始化：Xavier → Kaiming → LLaMA 的 init 方案
  - 优化器进化史：SGD → Momentum → Adam → AdamW（每个的数学原理）
  - 学习率调度：Warmup / Cosine / Linear
  - Normalization：Batch Norm / Layer Norm / RMS Norm
  - Dropout / 权重衰减 / 标签平滑
  - ⚡ 配套代码：`code/training_techniques.py`（PyTorch 训练第一个分类网络）
  - **Oracle + Momus 双重验证**

  **Recommended Agent Profile**:
  - **Category**: `unspecified-high`
  - **Parallelization**: YES（Wave 4）
  - **Blocked By**: Task 18, Task 19（需要反向传播理解优化器）

- [ ] 21. **Vol 4/Ch 4: 卷积神经网络 — convolutional-networks.md**

  **What to do**:
  - 卷积运算的数学定义（连续→离散）
  - 为什么 CNN 适合图像：平移不变性 + 局部连接 + 参数共享
  - 池化、步长、填充
  - 经典架构演进：LeNet → AlexNet → VGG → ResNet
  - 现代 CNN：EfficientNet、ConvNeXt
  - ⚡ 配套代码：`code/cnn_cifar10.py`（PyTorch 实现 ResNet 训练 CIFAR-10）
  - **Oracle + Momus 双重验证**

  **Recommended Agent Profile**:
  - **Category**: `unspecified-high`
    - Reason: 需要从数学卷积到架构演进的完整覆盖

  **Parallelization**:
  - **Can Run In Parallel**: YES（Wave 4）
  - **Blocked By**: Task 18（MLP 基础）

- [ ] 22. **Vol 4/Ch 5: RNN 与序列模型 — rnn-and-sequence.md**

  **What to do**:
  - RNN 循环计算图 + BPTT
  - LSTM：门控机制解决长期依赖（完整推导）
  - GRU：LSTM 的简化
  - 编码器-解码器架构
  - RNN 的局限 → 引出 Attention（为下一卷做铺垫）
  - ⚡ 配套代码：`code/rnn_lstm.py`（PyTorch LSTM 文本生成）
  - **Oracle + Momus 双重验证**

  **Recommended Agent Profile**:
  - **Category**: `unspecified-high`
  - **Parallelization**: YES（Wave 4）
  - **Blocked By**: Task 18, Task 19

- [ ] 23. **Vol 5/Ch 1: 注意力机制 — attention-mechanism.md** ⭐

  **What to do**:
  - Query / Key / Value 的直观理解（从检索系统类比）
  - 缩放点积注意力完整推导：Attention(Q,K,V) = softmax(QK^T/√d)V
  - 注意力权重的可视化解释
  - 从 RNN+Attention 到纯注意力的演进
  - ⚡ 配套代码：`code/attention_mechanism.py`（NumPy 手写注意力 + 权重热力图）
  - **Oracle + Momus 双重验证**

  **Recommended Agent Profile**:
  - **Category**: `ultrabrain`
    - Reason: 注意力机制是 Transformer 的核心创新，QKV 的直觉和数学需要最高精度

  **Parallelization**:
  - **Can Run In Parallel**: YES（Wave 5）
  - **Blocked By**: Task 22（RNN 的局限是注意力机制的动机）

- [ ] 24. **Vol 5/Ch 2: Transformer 完整架构 — transformer-architecture.md** ⭐

  **What to do**:
  - Encoder-Decoder 总览架构图（Mermaid）
  - Encoder Block：Multi-Head Attention → Add&Norm → FFN
  - Multi-Head Attention 拆分（为什么需要多头）
  - 位置编码：Sinusoidal → RoPE → ALiBi
  - Masked Self-Attention（为什么解码器不能看未来）
  - Cross-Attention（编码器→解码器的桥梁）
  - 残差连接与 Layer Normalization 的作用
  - ⚡ 配套代码：`code/transformer_block.py`（逐组件实现 Transformer Block）
  - **Oracle + Momus 双重验证**

  **Recommended Agent Profile**:
  - **Category**: `ultrabrain`
    - Reason: 整个体系最关键的一章，架构图、每个组件的数学、代码实现都需要极致精度

  **Parallelization**:
  - **Can Run In Parallel**: YES（Wave 5）
  - **Blocked By**: Task 23（注意力机制）

- [ ] 25. **Vol 5/Ch 3: Transformer 进化史 — variants-evolution.md**

  **What to do**:
  - Decoder-only 分支：GPT-1/2/3 → ChatGPT → LLaMA
  - Encoder-only 分支：BERT
  - Encoder-Decoder 分支：T5 / BART
  - 高效 Transformer：FlashAttention, 稀疏注意力, 滑动窗口
  - 后 Transformer 时代：Mamba（SSM）、xLSTM（简要对比）
  - ⚡ 配套代码：`code/transformer_family.py`（HuggingFace 加载不同架构）
  - **Oracle + Momus 双重验证**

  **Recommended Agent Profile**:
  - **Category**: `writing`
    - Reason: 以综述和对比分析为主，需要清晰的分类叙述

  **Parallelization**:
  - **Can Run In Parallel**: YES（Wave 5）
  - **Blocked By**: Task 24

- [ ] 26. **Vol 5/Ch 4: 从零实现 nanoGPT — implement-transformer.py**

  **What to do**:
  - 逐组件实现微型 GPT（参考 Andrej Karpathy 的 nanoGPT 风格）
  - 每一行代码对应上一章的一个组件概念
  - 完整的训练循环 + 生成 Shakespeare 风格文本
  - 创建详细的注释解释每段代码的作用
  - ⚡ 创建配套引导文件 `04-implement-transformer.md`
  - **Oracle + Momus 双重验证**

  **Recommended Agent Profile**:
  - **Category**: `deep`
    - Reason: 需要从零构建完整可运行的 GPT 训练，编码质量和注释质量都需要高水准

  **Parallelization**:
  - **Can Run In Parallel**: YES（Wave 5）
  - **Blocked By**: Task 24（必须先理解架构才能实现）

- [ ] 27. **Vol 6/Ch 0: 预训练范式总览 — pretraining-paradigm.md**

  **What to do**:
  - 标注数据的瓶颈 → SSL 的动机
  - 监督 vs 无监督 vs 自监督 vs 半监督（四象限对比图）
  - 预训练-微调范式详解
  - 为什么预训练有效（表示学习的理论解释）
  - 从 Word2Vec → BERT → GPT 的历史脉络
  - **Oracle + Momus 双重验证**

  **Recommended Agent Profile**:
  - **Category**: `writing`
  - **Parallelization**: YES（Wave 6）
  - **Blocked By**: Task 24（Transformer 是 SSL 的架构基础）, Task 25

- [ ] 28. **Vol 6/Ch 1: 对比学习 — contrastive-learning.md**

  **What to do**:
  - 核心思想：拉近正样本、推远负样本
  - SimCLR 完整架构：数据增强 → Encoder → Projection Head → Contrastive Loss
  - InfoNCE Loss 推导（◄ 来自互信息）
  - MoCo：动量编码器
  - CLIP：图文对比学习的里程碑
  - ⚡ 配套代码：`code/contrastive_learning.py`（SimCLR 风格实现）
  - **Oracle + Momus 双重验证**

  **Recommended Agent Profile**:
  - **Category**: `deep`
  - **Parallelization**: YES（Wave 6）
  - **Blocked By**: Task 27

- [ ] 29. **Vol 6/Ch 2: 掩码建模 — masked-modeling.md**

  **What to do**:
  - BERT：Masked Language Model
  - MAE：Masked Autoencoder（图像版掩码）
  - 为什么"填空"能学到语义（理论解释）
  - 对比 MLM vs Autoregressive
  - ⚡ 配套代码：`code/masked_modeling.py`（迷你 BERT 掩码预测）
  - **Oracle + Momus 双重验证**

  **Recommended Agent Profile**:
  - **Category**: `unspecified-high`
  - **Parallelization**: YES（Wave 6）
  - **Blocked By**: Task 27

- [ ] 30. **Vol 6/Ch 3: 自回归建模 — autoregressive-modeling.md**

  **What to do**:
  - 自回归语言模型的核心：next token prediction
  - GPT 系列：为什么自回归能学到世界知识
  - Scaling Laws（缩放定律）：Loss 随参数/数据/算力的幂律关系
  - 涌现能力（Emergent Abilities）
  - ⚡ 配套代码：`code/autoregressive_demo.py`（GPT-2 推理代码解读）
  - **Oracle + Momus 双重验证**

  **Recommended Agent Profile**:
  - **Category**: `unspecified-high`
  - **Parallelization**: YES（Wave 6）
  - **Blocked By**: Task 27

- [ ] 31. **Vol 6/Ch 4: 预训练-微调流程 — pretrain-finetune.py**

  **What to do**:
  - 使用 HuggingFace Transformers 生态系统
  - 加载预训练模型 → 在自定义数据集上微调 → 评估
  - 完整的训练脚本 + 配置文件
  - ⚡ 创建配套引导文件 `05-pretrain-finetune.md`
  - **Oracle + Momus 双重验证**

  **Recommended Agent Profile**:
  - **Category**: `unspecified-low`
  - **Parallelization**: YES（Wave 6）
  - **Blocked By**: Task 27

- [ ] 32. **Vol 7/Ch 1: VAE — vae.md**

  **What to do**:
  - 自编码器的局限 → 需要概率生成
  - 潜在变量模型（Latent Variable Model）的直觉
  - 变分下界 ELBO 的完整推导 ⭐
  - 重参数化技巧（Reparameterization Trick）
  - VAE 损失函数：Reconstruction + KL 的直觉
  - VQ-VAE：离散潜在空间
  - ⚡ 配套代码：`code/vae.py`（VAE 生成 MNIST，潜在空间可视化）
  - **Oracle + Momus 双重验证**

  **Recommended Agent Profile**:
  - **Category**: `ultrabrain`
    - Reason: ELBO 推导需要极高的数学精度，是理解扩散模型的前置知识

  **Parallelization**:
  - **Can Run In Parallel**: YES（Wave 7）
  - **Blocked By**: Task 8（概率论）, Task 19（反向传播理解梯度）

- [ ] 33. **Vol 7/Ch 2: GAN — gan.md**

  **What to do**:
  - 对抗训练框架：生成器 vs 判别器
  - 极小极大博弈的数学形式
  - 模式崩溃（Mode Collapse）的原因
  - 条件 GAN / CycleGAN / StyleGAN
  - ⚡ 配套代码：`code/gan.py`（GAN 训练 + 稳定性技巧）
  - **Oracle + Momus 双重验证**

  **Recommended Agent Profile**:
  - **Category**: `unspecified-high`
  - **Parallelization**: YES（Wave 7）
  - **Blocked By**: Task 18（NN 基础）

- [ ] 34. **Vol 7/Ch 3: 扩散模型 — diffusion-models.md** ⭐

  **What to do**:
  - 前向扩散过程：逐步加噪的数学定义
  - 反向去噪过程：学习去噪的数学推导
  - DDPM 完整推导：从 ELBO 到简化损失 ⭐
  - DDIM：加速采样
  - 潜在扩散模型（LDM / Stable Diffusion）
  - Classifier-Free Guidance
  - ⚡ 配套代码：`code/diffusion_demo.py`（迷你扩散模型 + 采样可视化）
  - **Oracle + Momus 双重验证**

  **Recommended Agent Profile**:
  - **Category**: `ultrabrain`
    - Reason: DDPM 的数学推导极为复杂，每一步都必须精确

  **Parallelization**:
  - **Can Run In Parallel**: YES（Wave 7）
  - **Blocked By**: Task 32（VAE 的变分推导是扩散模型的前置）

- [ ] 35. **Vol 7/Ch 4: 大语言模型 — large-language-models.md** ⭐⭐

  **What to do**:
  - **第一部分：预训练**
    - 数据收集与清洗（CommonCrawl、去重、质量过滤）
    - Tokenization：BPE / SentencePiece / TikToken
    - 训练稳定性：损失尖峰、梯度问题
  - **第二部分：对齐（Alignment）**
    - Instruction Tuning：指令数据的构建
    - RLHF 完整框架：SFT → Reward Model → PPO ⭐
    - DPO：更简单的替代方案
  - **第三部分：推理增强**
    - Chain-of-Thought / Tree-of-Thought
    - RAG（检索增强生成的概念引出）
    - Long-Context 技术
  - **第四部分：LLM 系统架构**
    - KV Cache
    - Speculative Decoding
    - 量化：GPTQ / AWQ / GGUF
    - 推理框架：vLLM / TensorRT-LLM
  - ⚡ 配套代码：`code/llm_inference.py`（HuggingFace 加载并推理 LLM） + `code/rlhf_pipeline_demo.py`（简化 RLHF 流程）
  - **Oracle + Momus 双重验证**

  **Recommended Agent Profile**:
  - **Category**: `ultrabrain`
    - Reason: 这是整个体系中最重要且最复杂的一章，涉及预训练/RLHF/推理优化等多个高难度子领域

  **Parallelization**:
  - **Can Run In Parallel**: NO（超长单章，需要连续写完四个部分）
  - **Blocked By**: Task 24（Transformer）, Task 30（Scaling Laws 等前置概念）
  - **Note**: 这一章可能超长，如果超过 3000 行，拆分为 `04a-pretraining.md`, `04b-alignment.md`, `04c-inference.md`

- [ ] 36. **Vol 7/Ch 5: 高效微调 — lora-and-finetuning.md**

  **What to do**:
  - 全量微调 vs 参数高效微调（对比分析）
  - LoRA 的数学原理：低秩近似
  - QLoRA：结合量化的 4-bit 微调
  - Adapter / Prefix Tuning
  - ⚡ 配套代码：`code/lora_finetuning.py`（使用 PEFT 库微调 LLM）
  - **Oracle + Momus 双重验证**

  **Recommended Agent Profile**:
  - **Category**: `unspecified-high`
  - **Parallelization**: YES（Wave 7）
  - **Blocked By**: Task 35（需要 LLM 基础理解）

- [ ] 37. **Vol 8/Ch 1: PyTorch 深入 — pytorch-deep-dive.md**

  **What to do**:
  - Tensor 底层机制：Storage / Stride
  - Autograd 引擎：计算图 + 梯度累积
  - nn.Module 体系：构建自定义层/网络
  - torch.utils.data：Dataset / DataLoader / Sampler
  - torch.compile：JIT 编译加速
  - ⚡ 配套代码：`code/pytorch_deep_dive.py`（手写简化版 Autograd 引擎）
  - **Oracle + Momus 双重验证**

  **Recommended Agent Profile**:
  - **Category**: `unspecified-high`
  - **Parallelization**: YES（Wave 8）
  - **Blocked By**: Task 18（理解自动微分需要先懂反向传播）

- [ ] 38. **Vol 8/Ch 2: 训练循环精通 — training-loop-mastery.md**

  **What to do**:
  - 标准训练循环模板（可复用于任何项目）
  - 断点续训：Checkpoint 保存/恢复
  - 梯度累积：模拟更大 Batch Size
  - 梯度裁剪：防止梯度爆炸
  - 混合精度训练 AMP
  - 实验跟踪：WandB / TensorBoard
  - ⚡ 配套代码：`code/trainer_class.py`（完整训练器类）
  - **Oracle + Momus 双重验证**

  **Recommended Agent Profile**:
  - **Category**: `unspecified-high`
  - **Parallelization**: YES（Wave 8）
  - **Blocked By**: Task 37

- [ ] 39. **Vol 8/Ch 3: 分布式训练 — distributed-training.md**

  **What to do**:
  - 数据并行 DDP：原理与实现
  - 模型并行：Tensor Parallel + Pipeline Parallel
  - FSDP：Fully Sharded Data Parallel
  - DeepSpeed ZeRO 三阶段
  - ⚡ 配套代码：`code/distributed_demo.py`（单机多卡 DDP 脚本）
  - **Oracle + Momus 双重验证**

  **Recommended Agent Profile**:
  - **Category**: `deep`
  - **Parallelization**: YES（Wave 8）
  - **Blocked By**: Task 37

- [ ] 40. **Vol 8/Ch 4: 数据管线工程 — data-pipeline.md**

  **What to do**:
  - 大规模数据加载优化
  - WebDataset / Mosaic 流式加载
  - 数据增强：torchvision / albumentations
  - 数据集格式：HuggingFace Datasets / Arrow
  - ⚡ 配套代码：`code/data_pipeline.py`（高性能数据加载实现）
  - **Oracle + Momus 双重验证**

  **Recommended Agent Profile**:
  - **Category**: `unspecified-high`
  - **Parallelization**: YES（Wave 8）
  - **Blocked By**: Task 37

- [ ] 41. **Vol 8/Ch 5: 模型部署基础 — deployment-basics.md**

  **What to do**:
  - 模型导出：TorchScript / ONNX
  - 推理服务：FastAPI + Triton
  - INT8 / INT4 量化
  - Docker 容器化
  - ⚡ 配套代码：`code/serve_model.py`（完整推理 API）
  - **Oracle + Momus 双重验证**

  **Recommended Agent Profile**:
  - **Category**: `unspecified-high`
  - **Parallelization**: YES（Wave 8）
  - **Blocked By**: Task 37

- [ ] 42. **Vol 8/Ch 6: Python ML 生态全景 — python-ml-ecosystem.md**

  **What to do**:
  - HuggingFace Transformers / Datasets / PEFT
  - PyTorch Lightning / Accelerate
  - Weights & Biases 实验管理
  - LangChain / LlamaIndex
  - vLLM / Ollama / llama.cpp
  - ⚡ 配套代码：`code/ecosystem_overview.py`（各框架快速体验脚本）
  - **Oracle + Momus 双重验证**

  **Recommended Agent Profile**:
  - **Category**: `writing`
  - **Parallelization**: YES（Wave 8）
  - **Blocked By**: Task 37

- [ ] 43. **Vol 9/Ch 1: Prompt Engineering — prompt-engineering.md**

  **What to do**:
  - 基础模式：角色/指令/格式/示例
  - Few-Shot / Zero-Shot Prompting
  - Chain-of-Thought（思维链）原理解析 ⭐
  - 结构化 Prompt：XML / JSON 模板
  - System Prompt 设计原则
  - Prompt 优化：DSPy 框架
  - 反注入与安全
  - ⚡ 配套代码：`code/prompt_patterns.py`（Prompt 模板库 + A/B 测试）
  - **Oracle + Momus 双重验证**

  **Recommended Agent Profile**:
  - **Category**: `writing`
  - **Parallelization**: YES（Wave 9）
  - **Blocked By**: Task 35（LLM 基础理解）

- [ ] 44. **Vol 9/Ch 2: RAG — rag.md**

  **What to do**:
  - 为什么需要 RAG：知识截止、幻觉、私有数据
  - RAG 三件套：索引 → 检索 → 生成
  - 向量数据库：Chroma / Pinecone / Qdrant
  - 文本分割策略 Chunking
  - Embedding 模型选择
  - 高级 RAG：HyDE / RAPTOR / Self-RAG
  - 多模态 RAG
  - ⚡ 配套代码：`code/rag_system.py`（从零构建完整 RAG 系统）
  - **Oracle + Momus 双重验证**

  **Recommended Agent Profile**:
  - **Category**: `deep`
  - **Parallelization**: YES（Wave 9）
  - **Blocked By**: Task 35（需要 LLM 理解）

- [ ] 45. **Vol 9/Ch 3: Function Calling — tool-calling.md**

  **What to do**:
  - Tool Calling 协议：OpenAI / Anthropic 格式详解
  - 工具定义 Schema：参数、描述、返回值
  - 从自然语言到 API 调用的全流程
  - 并行工具调用
  - ⚡ 配套代码：`code/tool_calling.py`（构建 Calculator+Search+Code 工具集）
  - **Oracle + Momus 双重验证**

  **Recommended Agent Profile**:
  - **Category**: `unspecified-high`
  - **Parallelization**: YES（Wave 9）
  - **Blocked By**: Task 35

- [ ] 46. **Vol 9/Ch 4: Agent 系统 — agent-systems.md** ⭐

  **What to do**:
  - Agent = LLM + 工具 + 循环（核心公式）
  - ReAct 循环：Reasoning + Acting 完整流程 ⭐
  - Agent 记忆管理：短期/长期/持久化
  - 任务规划：Plan-and-Execute
  - 框架实践：
    - LangChain Agent
    - LangGraph：图式 Agent 编排
    - AutoGen：多 Agent 对话
    - CrewAI：角色式 Agent 协作
  - ⚡ 配套代码：`code/agent_framework.py`（从零实现 Mini Agent Framework）
  - 📈 图：ReAct 循环流程图
  - **Oracle + Momus 双重验证**

  **Recommended Agent Profile**:
  - **Category**: `deep`
    - Reason: Agent 系统是多组件整合的复杂系统，需要从原理到框架实现的全覆盖

  **Parallelization**:
  - **Can Run In Parallel**: YES（Wave 9）
  - **Blocked By**: Task 43, Task 45（需要 Prompt + Tool Calling）

- [ ] 47. **Vol 9/Ch 5: LLM 评估与监控 — evaluation-and-monitoring.md**

  **What to do**:
  - 评估指标：准确率/相关性/安全性
  - 评估数据集构建
  - LLM-as-Judge 评估方法
  - LangSmith / LangFuse 监控
  - ⚡ 配套代码：`code/evaluation_pipeline.py`（自动化评估管线）
  - **Oracle + Momus 双重验证**

  **Recommended Agent Profile**:
  - **Category**: `unspecified-high`
  - **Parallelization**: YES（Wave 9）
  - **Blocked By**: Task 35

- [ ] 48. **Vol 10/Ch 1: AI 编程助手内部机制 — ai-coding-assistants.md** ⭐

  **What to do**:
  - 自动补全 vs Chat vs Agent 三种模式
  - TabNine / Copilot 时代的架构演变
  - OpenCode / ClaudeCode / Cursor 的架构对比
  - LSP（语言服务器协议）与 AI 补全的结合
  - 上下文管理：项目理解 + 文件索引
  - ⚡ 配套代码：`code/coding_assistant_analysis.md`（框架对比分析笔记）
  - **Oracle + Momus 双重验证**

  **⚠️ Special Note**: 本章涉及 OpenCode 自身机制的分析。Oracle 和 Momus 可能不掌握 OpenCode 内部细节。需要额外的外部文档验证（查阅 OpenCode 的 AGENTS.md 和公开发布的资料）

  **Recommended Agent Profile**:
  - **Category**: `writing`
  - **Parallelization**: YES（Wave 10）
  - **Blocked By**: Task 46（需要 Agent 系统理解）

- [ ] 49. **Vol 10/Ch 2: Agent Harness 架构 — agent-harness-deep-dive.md**

  **What to do**:
  - 调度系统：任务规划 → 子代理分配
  - 工具系统：Tool Calling 与 MCP 协议
  - 技能系统：动态技能加载与注入
  - 记忆系统：对话历史 + 文件状态
  - 权限系统：文件操作/命令执行沙箱
  - 异常处理与恢复机制
  - 📈 图：Harness 架构全景图
  - **Oracle + Momus 双重验证**

  **⚠️ Special Note**: 同第48章，需要外部验证。

  **Recommended Agent Profile**:
  - **Category**: `deep`
  - **Parallelization**: YES（Wave 10）
  - **Blocked By**: Task 48

- [ ] 50. **Vol 10/Ch 3: MCP 协议与工具生态 — mcp-and-tools.md**

  **What to do**:
  - Model Context Protocol (MCP) 详解
  - 工具定义与注册机制
  - 如何开发自定义 MCP 服务器
  - 常见 MCP 实践：SSH / Docker / 数据库
  - ⚡ 配套代码：`code/custom_mcp_server.py`（构建自定义 MCP 工具）
  - **Oracle + Momus 双重验证**

  **Recommended Agent Profile**:
  - **Category**: `unspecified-high`
  - **Parallelization**: YES（Wave 10）
  - **Blocked By**: Task 48

- [ ] 51. **Vol 10/Ch 4: 技能系统与 Prompt 架构 — skill-and-prompt-system.md**

  **What to do**:
  - 技能（Skill）的设计模式
  - 系统 Prompt 的层级结构
  - 上下文窗口最优利用策略
  - 多 Agent 协作的工作流设计
  - ⚡ 配套代码：`code/custom_skill.py`（编写并加载自定义 Skill）
  - **Oracle + Momus 双重验证**

  **Recommended Agent Profile**:
  - **Category**: `writing`
  - **Parallelization**: YES（Wave 10）
  - **Blocked By**: Task 48

- [ ] 52. **Vol 10/Ch 5: 毕业项目 — build-your-own-tool.md** ⭐⭐

  **What to do**:
  - 终极目标：综合运用前九卷所有知识
  - **Part A: 核心引擎**
    - LLM 调用封装（支持多 Provider）
    - 上下文管理（文件感知 + 历史管理）
    - Agent 循环
  - **Part B: 工具系统**
    - 文件读写 / 命令执行 / 搜索工具
    - MCP 协议兼容
  - **Part C: Skill 系统**
    - 动态 Prompt 注入
    - 可插拔技能加载
  - **Part D: IDE 集成**
    - 与 VS Code / 终端的集成
    - 与 OpenCode/ClaudeCode 的互操作
  - ⚡ 全部代码在 `code/build_your_own/` 目录下
  - **Oracle + Momus 双重验证**

  **Recommended Agent Profile**:
  - **Category**: `ultrabrain`
    - Reason: 综合应用前 9 卷所有知识，需要理解 LLM、Agent、工具链的完整链路

  **Parallelization**:
  - **Can Run In Parallel**: NO（Part A→B→C→D 有依赖关系）
  - **Blocked By**: Task 46, Task 49-51

- [ ] 53. **Vol 10/Ch 6: 持续成长路线图 — conclusion-and-roadmap.md**

  **What to do**:
  - 学习路径总结（回顾 10 卷的思维导图）
  - 进阶方向：研究 / 工程 / 产品三条路径
  - 推荐读物与资源列表（论文/书籍/课程/博客）
  - 如何持续跟进前沿（Twitter/ArXiv/会议/社区）
  - **Oracle + Momus 双重验证**

  **Recommended Agent Profile**:
  - **Category**: `writing`
  - **Parallelization**: YES（Wave 10）
  - **Blocked By**: Task 35（需要 LLM 理解）, Task 46（需要 Agent 理解）
---

## Final Verification Wave

> 4 review agents run in PARALLEL. ALL must APPROVE. Present consolidated results to user and get explicit "okay" before completing.

- [ ] F1. **Plan Compliance Audit** — `oracle`
  Read the plan end-to-end. For each "Must Have": verify implementation exists (read file). For each "Must NOT Have": search for forbidden patterns — reject with file:line if found. Check evidence files exist. Compare deliverables against plan.
  Output: `Must Have [N/N] | Must NOT Have [N/N] | Tasks [N/N] | VERDICT: APPROVE/REJECT`

- [ ] F2. **Code Quality Review** — `unspecified-high`
  Run `python -m py_compile` on all .py files. Review for: bare-except, unused imports, hardcoded paths, print() in library code. Check AI slop: excessive comments, over-abstraction, generic names.
  Output: `Compile [PASS/FAIL] | Files [N clean/N issues] | VERDICT`

- [ ] F3. **Real Manual QA** — `unspecified-high`
  Start from clean venv. Execute ALL code from ALL chapters. Test cross-chapter integration. Save to `.omo/evidence/final-qa/`.
  Output: `Scripts [N/N pass] | Integration [N/N] | VERDICT`

- [ ] F4. **Scope Fidelity Check** — `deep`
  For each task: read "What to do", read actual output. Verify 1:1 — everything in spec was built (no missing), nothing beyond spec was built (no creep). Check "Must NOT do" compliance.
  Output: `Tasks [N/N compliant] | Unaccounted [CLEAN/N files] | VERDICT`

---

## Commit Strategy

- **Wave commits**: One commit per wave (one volume)
- **Message pattern**: `docs(ai): [volume name] - [chapter count] chapters`
- **Pre-commit**: Run all .py files in the wave's volume

---

## Success Criteria

### Final Checklist
- [ ] All "Must Have" present in `/ai/`
- [ ] All "Must NOT Have" absent
- [ ] Every chapter has Oracle + Momus approval record
- [ ] All Python scripts runnable
- [ ] All internal links resolve
- [ ] Mermaid diagrams render correctly
