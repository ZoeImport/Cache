# AI/ML 技术百科全书 — v1.1 深度优化方案

> 目标: 将 v1 初稿从「笔记级」提升到「出版级」——每句话有源可查，每个理论有史可依，每个数据真实可验。

---

## 一、三大核心优化维度

### 1️⃣ 理论溯源 (Citation & Provenance)

**原则**: 每个非平凡的理论声明必须标注可查证的原始来源。

| 类型 | 格式 | 示例 |
|:---|:---|:---|
| 原始论文 | `[Author Year]` + 脚注 | `[Vaswani et al. 2017]` |
| 经典教材 | 章节引用 | `[Goodfellow 2016, Ch 6]` |
| 知名博客/课程 | 标注作者 | `[Karpathy 2022, nanoGPT]` |

**需要溯源的关键节点**（每卷抽样）:

**Vol 3 经典ML:**
- 线性回归最小二乘法 → Gauss 1809 / Legendre 1805
- 逻辑回归 → Cox 1958 / Berkson 1944
- SVM → Vapnik 1963 (original) / Cortes & Vapnik 1995 (soft margin)
- 决策树 → Breiman 1984 (CART) / Quinlan 1986 (ID3)
- 随机森林 → Breiman 2001
- AdaBoost → Freund & Schapire 1997
- K-Means → Lloyd 1957 / Forgy 1965
- PCA → Pearson 1901 / Hotelling 1933

**Vol 4 神经网络:**
- 感知机 → Rosenblatt 1958, *Psychological Review*
- MLP + 反向传播 → Rumelhart, Hinton & Williams 1986, *Nature*
- CNN → LeCun 1989 / LeNet-5 1998
- ResNet → He et al. 2015, *Deep Residual Learning*
- LSTM → Hochreiter & Schmidhuber 1997, *Neural Computation*
- Dropout → Srivastava et al. 2014
- Batch Norm → Ioffe & Szegedy 2015
- Adam → Kingma & Ba 2015
- Xavier Init → Glorot & Bengio 2010
- Kaiming Init → He et al. 2015

**Vol 5 Transformer:**
- Attention → Bahdanau et al. 2015 (Neural Machine Translation)
- Transformer → Vaswani et al. 2017, *Attention Is All You Need*
- GPT-1 → Radford et al. 2018
- BERT → Devlin et al. 2019
- GPT-2 → Radford et al. 2019
- GPT-3 → Brown et al. 2020
- LLaMA → Touvron et al. 2023
- FlashAttention → Dao et al. 2022
- RoPE → Su et al. 2021
- Scaling Laws → Kaplan et al. 2020 / Hoffmann et al. 2022 (Chinchilla)

**Vol 6 自监督学习:**
- Word2Vec → Mikolov et al. 2013
- SimCLR → Chen et al. 2020
- MoCo → He et al. 2020
- CLIP → Radford et al. 2021
- BERT → Devlin et al. 2019 (重复但重要)
- MAE → He et al. 2022

**Vol 7 生成式AI:**
- VAE → Kingma & Welling 2014
- GAN → Goodfellow et al. 2014
- DDPM → Ho et al. 2020
- DDIM → Song et al. 2021
- Stable Diffusion → Rombach et al. 2022
- RLHF → Ouyang et al. 2022 (InstructGPT)
- DPO → Rafailov et al. 2023

### 2️⃣ 历史脉络 (Historical Context)

**原则**: 每个核心概念标注「首次出现时间 + 关键里程碑」，形成清晰的技术演进时间线。

**格式示例**:
> **反向传播（Backpropagation）**
> - 1960s: Kelley (1960), Bryson (1961) 提出连续最优控制中的链式法则应用
> - 1970: Seppo Linnainmaa 首次在论文中实现自动微分的反向模式
> - 1986: Rumelhart, Hinton & Williams 发表《Learning representations by back-propagating errors》——引爆第一次神经网络热潮
> - 1989: LeCun 将其应用于手写邮政编码识别（CNN+BP）

**需要编年史的关键线路**:

| 线路 | 起止 | 关键节点数 |
|:---|:---|:---:|
| 神经网络简史 | 1943(McCulloch-Pitts)→2024(LLaMA 3) | ~15 |
| 生成式模型简史 | 2014(GAN)→2022(Stable Diffusion) | ~8 |
| 大语言模型简史 | 2013(Word2Vec)→2024(GPT-4/Gemini) | ~12 |
| 优化器简史 | 1951(SGD)→2020(Lion) | ~8 |
| 计算机视觉简史 | 1989(ConvNet)→2021(ViT) | ~10 |
| 预训练范式简史 | 2013(Word2Vec)→2022(Flan-T5) | ~10 |

### 3️⃣ 核心数据增强 (Empirical Data)

**原则**: 所有性能声明、实验结果、对比数据必须有真实来源或可复现的实验支撑。

**数据来源策略**:
- 论文原文表格 → 提取关键数字
- 官方 Leaderboard → Papers With Code, Eval Harness
- 自行运行验证 → 小规模复现
- 标注置信度 → "据 [paper] 报道 85.3%" vs "笔者实测 84.2%"

**需要补充数据的章节**:

| 章节 | 需要的数据类型 | 数据来源 |
|:---|:---|:---|
| 3.1 线性模型 | 在 benchmark 上的性能对比 | sklearn docs / UCI |
| 3.3 树模型 | RF vs GBDT vs XGBoost 精度/速度 | 自行运行或官方 |
| 4.2 反向传播 | 训练收敛曲线、梯度范数变化 | ✅ 已有代码生成 |
| 4.4 CNN | ResNet 在 CIFAR-10/ImageNet 的精度 | ✅ 已有 CIFAR-10 结果(70.96%) |
| 5.2 Transformer | 不同配置下的 Perplexity 对比 | nanoGPT 实验 |
| 5.4 nanoGPT | 训练损失曲线、生成样本 | ✅ 已有 (3.36→1.38) |
| 6.1 对比学习 | SimCLR 在 CIFAR-10 的 k-NN accuracy | 自行运行或原文 |
| 7.1 VAE | 重构质量 (MSE/SSIM)、潜在空间插值 | ✅ 已有 MNIST 结果 |
| 7.2 GAN | 生成样本质量 (FID/IS)、训练稳定性 | 需自行运行 |
| 7.3 扩散模型 | 采样速度 (DDPM vs DDIM) | 论文数据 |
| 7.4 LLM | 不同模型在 benchmark 上的对比 | Eval Harness / Open LLM Leaderboard |
| 7.5 LoRA | 可训练参数对比（全量 vs LoRA） | ✅ 已有 |

---

## 二、批量机械性任务

### B1. 代码块运行输出补充（Vol 1-3）
**方式**: 逐章运行配套 .py，截取 stdout 嵌入 .md
**涉及**: `01-overview`(4章) + `02-mathematics`(5章) + `03-classical-ml`(6章) + `04-neural-networks`(2章) = 17章
**格式**:
```text
运行输出:
Epoch 10/10: Loss=0.023, Acc=97.5%
```

### B2. 缺失代码文件创建
| 卷 | 缺失文件 | 优先级 |
|:---|:---|:---:|
| Vol 5 | `transformer_block.py`（补充独立运行脚本） | P1 |
| Vol 8 | `data_pipeline.py`, `distributed_demo.py`, `ecosystem_overview.py`（补全） | P1 |
| Vol 9 | `rag_system.py` | P1 |
| Vol 10 | 6 个 .py（按 md 描述编写） | P1 |

### B3. IPA 音标批量标注
**工具**: 用 Python 脚本自动识别首次出现的术语，插入 IPA
**术语表**: 约 60-80 个核心术语
**脚本逻辑**: 扫描每个 .md → 首次出现 → 插入 `术语（/ipa/，中文）`

### B4. Matplotlib 白框验证
**范围**: 所有已生成的 .png
**修复**: 重新运行含中文标签的代码，确认无 glyph 警告

---

## 三、执行策略

### Phase 1: 批量机械任务（并行）
- B1 代码输出补充 → 逐个运行 .py 截取输出
- B4 白框验证 → 重新生成可疑图片
- B2 缺失代码 → 按优先级补齐

### Phase 2: 深度优化（逐章进行）
- 1️⃣ 理论溯源 → 为关键声明添加引用
- 2️⃣ 历史脉络 → 插入技术编年史时间线
- 3️⃣ 核心数据 → 补充实验数据和 benchmark

### Phase 3: 最终验证
- 交叉引用完整检查
- 术语一致性审计
- IPA 标注正确性检查

---

## 四、预估工作量

| 项目 | 估计时间 | 并行度 |
|:---|:---:|:---:|
| B1 代码输出嵌入 | 3-4h | 多章并行 |
| B2 缺失代码 | 2-3h | 并行 |
| B3 IPA 标注 | 1-2h | 可半自动 |
| B4 白框验证 | 0.5h | 快速 |
| Phase 2 深度优化 | 8-12h | 逐卷 |
| Phase 3 最终验证 | 1-2h | 自动+人工 |
| **总计** | **~20h** | |

---

## 五、参考文献（格式示例）

每章末尾增加参考文献列表，格式：
```markdown
## 参考文献
1. Rumelhart, D.E., Hinton, G.E. & Williams, R.J. (1986). Learning representations by back-propagating errors. *Nature*, 323(6088), 533-536.
2. LeCun, Y. et al. (1989). Backpropagation applied to handwritten zip code recognition. *Neural Computation*, 1(4), 541-551.
```

---

**方案已就绪。等你确认优先级和范围后开始执行。**
