# AI 教学内容深度改进 — 演算盒补充（Phase 1: Vol 3 + Vol 4）

## TL;DR

> **Quick Summary**: 在 Vol 3（经典ML）和 Vol 4（神经网络）的所有高级数学概念处插入可折叠演算盒（`::: details`），提供手把手代数演算（公式→参数含义→公式来源→手算演示→实际意义），并在目录和章末标记演算位置。
>
> **Deliverables**:
> - 约 13 个 `::: details` 演算盒插入到 Vol 3 + Vol 4 对应章节
> - `📐` 标记添加到章节目录
> - 章末演算盒索引表
> - OC 注释（`!OC:`）从 `03-numpy-and-linalg.md` 中移除
> - 模板文件 `_演算盒模板.md` 作为参考示例
>
> **Estimated Effort**: Medium（约 13 个盒子，每个 30-60 行内容）
> **Parallel Execution**: YES — 3 waves（模板→章节并行→验证）
> **Critical Path**: Template → Chapter 1 → ... → Final Verification

---

## Context

### Original Request
项目 AI 教学内容从 numpy 章节后对概念的详细描述很少，学习者需要补充特征值计算、SVD、PCA、反向传播等知识的手把手演算过程。

### Interview Summary
**Key Discussions**:
- **格式**: `::: details` 可折叠容器（默认折叠），`🔍 完整演算：[概念名] — [场景描述]` 标题
- **结构**: 五段式 — 公式 → 参数含义 → 公式来源 → 手算演示 → 实际意义
- **范围**: Phase 1 = Vol 3（经典ML）+ Vol 4（神经网络）约 13 个演算盒
- **目录标记**: `📐` 在章节标题旁 + 章末演算盒索引表
- **执行顺序**: 按章节顺序推进

**Research Findings**:
- VitePress 原生支持 `::: details` 自定义容器
- MathJax3 已配置完成，`$...$` 和 `$$...$$` 均可正常渲染
- `docs/ai` → `../ai` 符号链接，编辑 `ai/` 目录即可
- OC 注释仅存在于 `03-numpy-and-linalg.md`（5 处）

### Metis Review
**Identified Gaps** (addressed):
- **验证策略未文档化** → 已补充 5 条验证标准到 draft
- **执行分阶段缺失** → 已添加 Phase 1/Phase 2 拆分和阶段切换条件
- **模板先行** → 计划中第一个任务创建模板文件

---

## Work Objectives

### Core Objective
在 Vol 3（经典ML）和 Vol 4（神经网络）共 11 个章节中，对每个涉及高级数学计算的概念插入「演算盒」，提供完整的逐步骤代数演算。

### Concrete Deliverables
- 每个演算盒：1 个 `::: details` 容器块，嵌入对应章节 `.md` 文件中
- 每个受影响章节：`📐` 标记在目录中 + 章末新增"本章演算盒索引"表
- 模板文件：`ai/99-演算盒模板.md`
- OC 注释清除

### Definition of Done
- [ ] `npm run docs:build` → exit code 0
- [ ] 每个受影响的章节至少有一个演算盒
- [ ] `grep -r "!OC:" ai/01-overview/03-numpy-and-linalg.md` → 0 matches
- [ ] `grep "::: details 🔍"` 格式在所有章节中一致

### Must Have
- 每个演算盒包含五段式结构（公式 → 参数含义 → 公式来源 → 手算 → 实际意义）
- 第一次出现的概念（如协方差矩阵）必须有完整的参数含义解释
- 手算使用具体数值，不能用符号推导代替代数运算
- `📐` TOC 标记和章末索引表

### Must NOT Have (Guardrails)
- 不修改 `code/*.py` 文件
- 不修改正文中现有的公式/代码/文字（仅新增演算盒 + 目录标记）
- 不引入章节未定义的新概念
- 不交叉引用其他章节的演算盒（各自独立）
- 不涉及 Vol 5-10（Phase 2 待定）

---

## Verification Strategy

> **ZERO HUMAN INTERVENTION** — ALL verification is agent-executed. No exceptions.

### Test Decision
- **Infrastructure exists**: YES（VitePress + MathJax3）
- **Automated tests**: Tests-after（内容型任务不适合 TDD）
- **Framework**: `npm run docs:build`（构建验证）+ 手动 NumPy 验证（数学正确性）

### QA Policy
Every task MUST include on-the-fly manual verification by the executor.

---

## Execution Strategy

### Parallel Execution Waves

```
Wave 1 (Foundation):
├── Task 1: Create template file + test build [quick]

Wave 2 (Vol 3 — MAX PARALLEL):
├── Task 2: 01-linear-models — 3 个演算盒 [writing]
├── Task 3: 02-model-evaluation — 0 个（审查后确认）
├── Task 4: 03-tree-and-ensemble — 0 个（审查后确认）
├── Task 5: 04-svm-and-kernel — 2 个演算盒 [writing]
├── Task 6: 05-unsupervised-learning — 3 个演算盒 [writing]
└── Task 7: 06-ml-project-template — 0 个（审查后确认）

Wave 3 (Vol 4 — MAX PARALLEL):
├── Task 8: 01-perceptron-and-mlp — 1 个演算盒 [writing]
├── Task 9: 02-backpropagation — 2 个演算盒 [writing]
├── Task 10: 03-training-techniques — 审查后确认 [writing]
├── Task 11: 04-convolutional-networks — 2 个演算盒 [writing]
└── Task 12: 05-rnn-and-sequence — 审查后确认 [writing]

Wave FINAL:
├── Task F1: OC 注释清除 + 构建验证 [quick]
├── Task F2: 格式一致性检查 [quick]
└── Task F3: 全面审查 [deep]
```

### Agent Dispatch Summary

- **1**: **1** — Task 1 → `quick`
- **2**: **5** — Tasks 2-6 → `writing` / `quick`（审查确认）
- **3**: **5** — Tasks 8-12 → `writing`
- **FINAL**: **3** — F1 → `quick`, F2 → `quick`, F3 → `deep`

---

## TODOs

- [x] 1. **创建演算盒模板 + 测试构建**

  **What to do**:
  - 创建 `ai/99-演算盒模板.md`，包含一个完整的演算盒示例
  - 模板使用五段式结构：📐 公式 → 📖 参数含义 → 📝 公式来源 → ✏️ 手算演示 → 🌍 实际意义
  - 用特征值分解（一个 2×2 矩阵）作为模板示例内容
  - 在模板文件头部说明使用规范（标题格式、何时用、注意事项）
  - 在 VitePress 侧边栏中隐藏此模板文件
  - 运行 `npm run docs:build` 确认 `::: details` + MathJax3 渲染正常

  **Must NOT do**:
  - 不要添加模板之外的额外内容
  - 不要修改任何现有章节文件

  **Recommended Agent Profile**:
  - **Category**: `quick`
    - Reason: 单文件创建 + 构建验证，任务量小
  - **Skills**: []（无需特殊技能）

  **Parallelization**:
  - **Can Run In Parallel**: NO（基础任务）
  - **Blocks**: Tasks 2-12（模板必须先就位）
  - **Blocked By**: None

  **Acceptance Criteria**:
  - [ ] `ai/99-演算盒模板.md` 创建完成，包含 5 段式完整示例
  - [ ] `npm run docs:build` → exit 0, no errors

  **QA Scenarios**:
  ```
  Scenario: Template file exists and follows format
    Tool: Bash
    Steps:
      1. Check file exists: `ls ai/99-演算盒模板.md`
      2. Check 5 sections present: grep for 📐, 📖, 📝, ✏️, 🌍
      3. Build passes: npm run docs:build
    Expected Result: File exists, all 5 sections present, build passes
    Evidence: .omo/evidence/task-1-template-verify.txt
  ```

  **Commit**: YES
  - Message: `docs(ai): add calculation box template + test build`
  - Files: `ai/99-演算盒模板.md`
  - Pre-commit: `npm run docs:build`

- [x] 2. **Vol 3 Ch 1 线性模型 — 3 个演算盒**

  **What to do**:
  在 `ai/03-classical-ml/01-linear-models.md` 中插入以下演算盒：

  **Box A — 正规方程手算**（§1.3 后）：
  - 构建一个 4×2 小数据集（如 4 个样本，2 个特征）
  - 手算：设计矩阵 X → XᵀX → (XᵀX)⁻¹ → Xᵀy → w* = (XᵀX)⁻¹Xᵀy
  - 参数含义解释：w（权重）、X（设计矩阵）、y（目标向量）
  - 公式来源：从 MSE 损失 ∂L/∂w = 0 推导出正规方程
  - 实际意义：闭式解 vs 梯度下降的取舍场景

  **Box B — 梯度下降手算**（§1.4 后）：
  - 用同一小数据集，展示 3 步梯度下降迭代
  - 手算：预测值 → 残差 → 梯度 → w 更新（每步展示参数变化）
  - 参数含义：η（学习率）、∇L（梯度方向）
  - 实际意义：为什么梯度下降在大数据/高维特征时优于闭式解

  **Box C — 逻辑回归梯度手算**（§2.3 后）：
  - 单样本 x=[2, -1]，标签 y=1，初始 w=[0.5, -0.3], b=0
  - 手算：z = w·x + b → σ(z) → 交叉熵损失 → ∂L/∂w → 权重更新
  - 参数含义：σ(z)（Sigmoid 输出，代表概率 P(y=1|x)）
  - 公式来源：交叉熵损失的链式导数展开
  - 实际意义：为什么交叉熵 + Sigmoid 的梯度形式与线性回归相同

  **Must NOT do**:
  - 不修改现有正文
  - 不修改 code/*.py

  **References**:
  - `ai/99-演算盒模板.md` — 格式参考
  - 当前文件 §1.3、§1.4、§2.3 — 插入位置前的上下文
  - `03-classical-ml/code/linear_models.py` — 用于验证数学正确性的 NumPy 脚本

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Parallel Group**: Wave 2（with Tasks 5, 6）
  - **Blocked By**: Task 1（模板）

  **Acceptance Criteria**:
  - [ ] Box A 完整：正规方程完整手算 + 参数解释 + 实际意义
  - [ ] Box B 完整：梯度下降 3 步迭代至少展示 w₁, w₂, b 的变化
  - [ ] Box C 完整：逻辑回归单样本完整链式手算
  - [ ] `📐` 标记添加到 §1.3、§1.4、§2.3 的目录条目
  - [ ] 章末新增"本章演算盒索引"表

  **QA Scenarios**:
  ```
  Scenario: Build passes with new boxes
    Tool: Bash
    Steps:
      1. npm run docs:build
    Expected Result: exit 0
    Evidence: .omo/evidence/task-2-build.txt

  Scenario: Boxes exist in chapter
    Tool: Bash
    Steps:
      1. grep -c "::: details 🔍" ai/03-classical-ml/01-linear-models.md
    Expected Result: 3 boxes
    Evidence: .omo/evidence/task-2-box-count.txt
  ```

  **Commit**: YES（groups with Task 5, 6）
  - Message: `docs(ai): add 3 calculation boxes for linear models chapter`
  - Files: `ai/03-classical-ml/01-linear-models.md`
  - Pre-commit: `npm run docs:build`

- [x] 3. **Vol 3 Ch 2 模型评估 — 审查确认无需演算盒**

  **What to do**:
  - 快速审查 `ai/03-classical-ml/02-model-evaluation.md`，确认无高级数学计算需要演算盒
  - 如有发现，添加演算盒（当前预期：无需）

  **Parallelization**:
  - **Can Run In Parallel**: YES（Wave 2）

  **Acceptance Criteria**:
  - [ ] 审查完成，确认 0 个演算盒需要
  - [ ] 如无需要，在文件末尾添加注释 `<!-- 演算盒审查完成: 无需 -->`

- [x] 4. **Vol 3 Ch 3 树模型与集成 — 审查确认无需演算盒**

  **What to do**:
  - 快速审查 `ai/03-classical-ml/03-tree-and-ensemble.md`
  - 当前预期：树模型基于不纯度/信息增益，无高级线性代数计算，无需演算盒

  **Parallelization**:
  - **Can Run In Parallel**: YES（Wave 2）

  **Acceptance Criteria**:
  - [ ] 审查完成，确认 0 个演算盒需要
  - [ ] 如无需要，在文件末尾添加注释 `<!-- 演算盒审查完成: 无需 -->`

- [x] 5. **Vol 3 Ch 4 SVM 与核方法 — 2 个演算盒**

  **What to do**:
  在 `ai/03-classical-ml/04-svm-and-kernel.md` 中插入以下演算盒：

  **Box A — 拉格朗日对偶推导**（§2 后）：
  - 4 个样本（2 个 +1, 2 个 -1），展示从原始问题到对偶问题的转化
  - 手算：原始目标 → 拉格朗日函数 → 对 w,b 求偏导 → 回代 → 对偶目标
  - 参数含义：αᵢ（拉格朗日乘子）、K(xᵢ, xⱼ)（核矩阵元素）
  - 公式来源：原始目标 min ½||w||² 受约束 yᵢ(w·xᵢ+b) ≥ 1

  **Box B — RBF 核手算**（§3.4 后）：
  - 2 个点 x₁=[1,2], x₂=[4,6]，分别用 γ=0.1 和 γ=1.0 计算核值
  - 手算：||x₁ − x₂||² → -γ·d² → exp(...) → 核值
  - 参数含义：γ（核宽度参数，控制影响范围）
  - 实际意义：γ 小→平滑边界，γ 大→过拟合

  **References**:
  - `ai/99-演算盒模板.md`

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Parallel Group**: Wave 2（with Tasks 2, 6）
  - **Blocked By**: Task 1

  **Acceptance Criteria**:
  - [ ] Box A 完整：4 样本对偶推导手算
  - [ ] Box B 完整：RBF 核值计算（两个 γ 值对比）
  - [ ] `📐` 标记添加 + 章末索引表

  **QA Scenarios**:
  ```
  Scenario: Build passes
    Tool: Bash
    Steps: npm run docs:build
    Expected Result: exit 0
    Evidence: .omo/evidence/task-5-build.txt

  Scenario: 2 boxes in chapter
    Tool: Bash
    Steps: grep -c "::: details 🔍" ai/03-classical-ml/04-svm-and-kernel.md
    Expected Result: 2
    Evidence: .omo/evidence/task-5-box-count.txt
  ```

  **Commit**: YES（groups with Tasks 2, 6）

- [x] 6. **Vol 3 Ch 5 无监督学习 — 3 个演算盒**

  **What to do**:
  在 `ai/03-classical-ml/05-unsupervised-learning.md` 中插入以下演算盒：

  **Box A — 协方差矩阵手算**（§2.2 前，首次出现！）：
  - 4×3 数据集（4 样本，3 特征），一步步手算
  - 手算：中心化（每列减均值）→ 外积求和 → 除以 (n−1)
  - **参数含义完整解释**：每个元素 Cᵢⱼ 表示特征 i 和 j 的协方差
  - **公式来源**：Var(X) = E[(X−μ)(X−μ)ᵀ]
  - **实际意义**：协方差矩阵是对角化的基础（它告诉 PCA 哪些方向方差最大）

  **Box B — PCA via SVD 手算**（§2.3 后）：
  - 4×2 数据集降维到 1D
  - 手算：中心化 → SVD（UΣVᵀ）→ 取 V 的第一列为主成分 → 投影 Z = U₁σ₁
  - 参数含义：U（左奇异向量，样本在主成分上的方向）、Σ（奇异值，方差大小）、Vᵀ（右奇异向量，主成分方向）
  - **公式来源**：X = UΣVᵀ，其中 XᵀX 的特征分解 = VΣ²Vᵀ

  **Box C — 保留方差比例手算**（§2.5 后）：
  - 用 Box B 中的 σ₁, σ₂ 计算 r₁ = σ₁²/(σ₁²+σ₂²), r₂ = σ₂²/(σ₁²+σ₂²)
  - 实际意义：决定保留多少主成分（常用阈值 95%）

  **References**:
  - `ai/99-演算盒模板.md`

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Parallel Group**: Wave 2（with Tasks 2, 5）
  - **Blocked By**: Task 1

  **Acceptance Criteria**:
  - [ ] Box A 完整：协方差矩阵首次出现，参数含义必须详述
  - [ ] Box B 完整：PCA via SVD 完整手算
  - [ ] Box C 完整：方差比例计算
  - [ ] `📐` 标记 + 章末索引表

  **QA Scenarios**:
  ```
  Scenario: Build passes
    Tool: Bash
    Steps: npm run docs:build
    Expected Result: exit 0
    Evidence: .omo/evidence/task-6-build.txt

  Scenario: 3 boxes in chapter
    Tool: Bash
    Steps: grep -c "::: details 🔍" ai/03-classical-ml/05-unsupervised-learning.md
    Expected Result: 3
    Evidence: .omo/evidence/task-6-box-count.txt
  ```

  **Commit**: YES（groups with Tasks 2, 5）

- [x] 7. **Vol 3 Ch 6 ML 项目模板 — 审查确认无需演算盒**

  **What to do**:
  - 快速审查 `ai/03-classical-ml/06-ml-project-template.md`
  - 当前预期：流程/模板章节，无高级数学计算

  **Parallelization**:
  - **Can Run In Parallel**: YES（Wave 2）

  **Acceptance Criteria**:
  - [ ] 审查完成
  - [ ] 文件末尾注释 `<!-- 演算盒审查完成: 无需 -->`

- [x] 8. **Vol 4 Ch 1 感知机与 MLP — 1 个演算盒**

  **What to do**:
  在 `ai/04-neural-networks/01-perceptron-and-mlp.md` §3.1 后插入：

  **Box A — MLP 前向传播手算**：
  - 极简网络 2→2→1（2 输入 → 2 隐藏 → 1 输出），1 个样本 x=[1, -1]
  - 手算：z¹ = W¹·x + b¹ → h¹ = ReLU(z¹) → z² = W²·h¹ + b² → ŷ = σ(z²)
  - 每一步展示矩阵乘法的逐元素计算
  - 参数含义：W⁽ˡ⁾（权重矩阵）、b⁽ˡ⁾（偏置向量）、z⁽ˡ⁾（线性输出）、a⁽ˡ⁾（激活值）
  - 公式来源：逐层变换 a⁽ˡ⁾ = σ(W⁽ˡ⁾a⁽ˡ⁻¹⁾ + b⁽ˡ⁾)

  **References**: `ai/99-演算盒模板.md`

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Parallel Group**: Wave 3
  - **Blocked By**: Task 1

  **Acceptance Criteria**:
  - [ ] 1 个完整演算盒
  - [ ] `📐` 标记 + 章末索引表

  **Commit**: YES（groups with Tasks 9, 11）

- [x] 9. **Vol 4 Ch 2 反向传播 — 2 个演算盒**

  **What to do**:
  在 `ai/04-neural-networks/02-backpropagation.md` 中插入：

  **Box A — 单神经元梯度计算**（§1.2 后）：
  - 单神经元：w=2, b=1, x=3, y=0
  - 手算完整链式：z = wx+b → a = σ(z) → L = ½(a−y)² → ∂L/∂w
  - 参数含义：δ（误差信号）、∂L/∂w（权重梯度）

  **Box B — 2 层网络反向传播手算**（§2 结束后，**最高优先级**）：
  - 极简网络 2→2→1，1 个样本 x=[0.5, -0.3], y=1
  - 手算展示完整过程：
    - 前向：z¹ = W¹·x+b¹ → h¹ = tanh(z¹) → z² = W²·h¹+b² → ŷ = σ(z²) → L
    - 反向：δ² = ŷ−y → ∂L/∂W² = h¹ᵀ·δ² → δ¹ = (δ²·W²ᵀ) ⊙ tanh'(z¹) → ∂L/∂W¹ = xᵀ·δ¹
  - 关键：用一个表格展示【梯度信号流向】从输出到输入的逐层传递

  **References**: `ai/99-演算盒模板.md`

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Parallel Group**: Wave 3（with Tasks 8, 11）
  - **Blocked By**: Task 1

  **Acceptance Criteria**:
  - [ ] Box A 完整：单神经元链式展示
  - [ ] Box B 完整：2 层网络完整数值前向+反向
  - [ ] `📐` 标记 + 章末索引表

  **QA Scenarios**:
  ```
  Scenario: Build passes
    Tool: Bash
    Steps: npm run docs:build
    Expected Result: exit 0
    Evidence: .omo/evidence/task-9-build.txt

  Scenario: 2 boxes in chapter
    Tool: Bash
    Steps: grep -c "::: details 🔍" ai/04-neural-networks/02-backpropagation.md
    Expected Result: 2
    Evidence: .omo/evidence/task-9-box-count.txt
  ```

  **Commit**: YES（groups with Tasks 8, 11）

- [x] 10. **Vol 4 Ch 3 训练技巧 — 审查确认**

  **What to do**:
  - 审查 `ai/04-neural-networks/03-training-techniques.md`
  - 关注意义：是否有优化器公式（动量、Adam）需要手算
  - 如果发现需要，添加对应演算盒

  **Parallelization**:
  - **Can Run In Parallel**: YES（Wave 3）

  **Acceptance Criteria**:
  - [ ] 审查完成，按需添加演算盒

- [x] 11. **Vol 4 Ch 4 卷积网络 — 2 个演算盒**

  **What to do**:
  在 `ai/04-neural-networks/04-convolutional-networks.md` 中插入：

  **Box A — 卷积核手算**（§1 后）：
  - 3×3 核在 5×5 输入上滑动（无填充，步长 1）
  - 手算：核在左上角 → 逐元素乘 → 求和 → 输出特征图第一个值
  - 参数含义：K（卷积核/滤波器）、S（输出特征图）、stride（步长）、padding（填充）
  - 实际意义：卷积核 → 边缘检测 → 高层次特征提取

  **Box B — 输出尺寸公式验证**（§1.3 后）：
  - 用多个参数组合验证 W_out = ⌊(W_in + 2p − k)/s + 1⌋
  - 如：28×28 输入，3×3 核，步长 1，无填充 → 26×26

  **References**: `ai/99-演算盒模板.md`

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Parallel Group**: Wave 3（with Tasks 8, 9）
  - **Blocked By**: Task 1

  **Acceptance Criteria**:
  - [ ] 2 个完整演算盒
  - [ ] `📐` 标记 + 章末索引表

  **Commit**: YES（groups with Tasks 8, 9）

- [x] 12. **Vol 4 Ch 5 RNN 与序列 — 审查确认**

  **What to do**:
  - 审查 `ai/04-neural-networks/05-rnn-and-sequence.md`
  - 关注意义：是否有 BPTT、梯度消失等需要手算演示

  **Parallelization**:
  - **Can Run In Parallel**: YES（Wave 3）

  **Acceptance Criteria**:
  - [ ] 审查完成，按需添加演算盒

---

## Final Verification Wave (MANDATORY)

- [x] F1. **OC 注释清除 + 构建验证** — `quick`
  - 从 `ai/01-overview/03-numpy-and-linalg.md` 移除所有 5 处 `!OC:` 注释
  - 运行 `npm run docs:build` 确认无错误
  - Output: `Build [PASS/FAIL] | OC 注释 [N removed]`

- [x] F2. **格式一致性检查** — `quick`
  - `grep "::: details 🔍"` 检查所有任务文件，确认标题格式一致
  - 检查每个受影响章节的 `📐` 标记和索引表是否存在
  - Output: `Format [N/N consistent] | TOC [N/N marked]`

- [x] F3. **全面审查** — `deep`
  从用户视角审查所有演算盒：
  - 每个五段式是否完整？
  - 手算步骤是否每一步都清晰可追踪？
  - 参数含义是否解释清楚？
  - 第一次出现的概念是否有完整说明？
  Output: 逐章审查报告

---

## Commit Strategy

- **1-7**: `docs(ai): add calculation boxes for Vol 3 classic ML chapters`
- **8-12**: `docs(ai): add calculation boxes for Vol 4 neural network chapters`

---

## Success Criteria

### Verification Commands
```bash
npm run docs:build           # Expected: exit 0, no errors
grep -r "!OC:" ai/01-overview/03-numpy-and-linalg.md  # Expected: 0 matches
grep "::: details 🔍" ai/03-classical-ml/*.md  # Expected: 8 matches
grep "::: details 🔍" ai/04-neural-networks/*.md  # Expected: 5 matches
```

### Final Checklist
- [ ] Build passes: `npm run docs:build` → exit 0
- [ ] All 5 OC comments removed from `03-numpy-and-linalg.md`
- [ ] Vol 3: 8 calculation boxes across 6 chapters
- [ ] Vol 4: 5 calculation boxes across 5 chapters
- [ ] All boxes follow the 5-section format
- [ ] All affected chapters have `📐` TOC markers and index tables
