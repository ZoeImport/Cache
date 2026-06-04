import { defineConfig } from 'vitepress'

export default defineConfig({
  base: '/Cache/',
  title: 'Cache 知识库',
  description: 'AI/ML 技术百科 · Arch Linux 实战 · 周易与奇门遁甲',
  ignoreDeadLinks: true,
  srcExclude: ['**/.venv/**'],
  markdown: {
    math: true
  },
  head: [
    ['style', {}, `
details {
  position: relative;
  border-left: 3px solid var(--vp-c-brand-1);
  background: var(--vp-c-bg-soft);
  border-radius: 8px;
  padding: 16px 20px;
  margin: 16px 0;
}
details summary {
  cursor: pointer;
  font-weight: 600;
  margin-bottom: 8px;
}
details[open] summary {
  margin-bottom: 16px;
}
`]
  ],
  themeConfig: {
    sidebar: [
      {
        text: '📘 AI/ML 技术百科全书',
        items: [
          { text: '📖 术语表', link: '/ai/00-GLOSSARY' },
          {
            text: '卷1: AI全景图 + Python',
            collapsed: false,
            items: [
              { text: '第1章: AI世界全景图', link: '/ai/01-overview/01-intro-to-ai-world' },
              { text: '第2章: Python快速入门', link: '/ai/01-overview/02-python-quickstart' },
              { text: '第3章: NumPy与张量思维', link: '/ai/01-overview/03-numpy-and-linalg' },
              { text: '第4章: 数据可视化入门', link: '/ai/01-overview/04-visualization' },
              { text: '第5章: 第一个ML项目', link: '/ai/01-overview/05-first-ml-pipeline' }
            ]
          },
          {
            text: '卷2: 数学基础',
            collapsed: false,
            items: [
              { text: '第1章: 线性代数', link: '/ai/02-mathematics/01-linear-algebra' },
              { text: '第2章: 概率论', link: '/ai/02-mathematics/02-probability' },
              { text: '第3章: 微积分与优化', link: '/ai/02-mathematics/03-calculus-and-optimization' },
              { text: '第4章: 信息论', link: '/ai/02-mathematics/04-information-theory' },
              { text: '第5章: 统计学基础', link: '/ai/02-mathematics/05-statistics-basics' }
            ]
          },
          {
            text: '卷3: 经典机器学习',
            collapsed: false,
            items: [
              { text: '第1章: 线性模型', link: '/ai/03-classical-ml/01-linear-models' },
              { text: '第2章: 模型评估', link: '/ai/03-classical-ml/02-model-evaluation' },
              { text: '第3章: 树模型与集成', link: '/ai/03-classical-ml/03-tree-and-ensemble' },
              { text: '第4章: SVM与核方法', link: '/ai/03-classical-ml/04-svm-and-kernel' },
              { text: '第5章: 无监督学习', link: '/ai/03-classical-ml/05-unsupervised-learning' },
              { text: '第6章: ML项目模板', link: '/ai/03-classical-ml/06-ml-project-template' }
            ]
          },
          {
            text: '卷4: 神经网络',
            collapsed: false,
            items: [
              { text: '第1章: 感知机与MLP', link: '/ai/04-neural-networks/01-perceptron-and-mlp' },
              { text: '第2章: 反向传播', link: '/ai/04-neural-networks/02-backpropagation' },
              { text: '第3章: 训练技巧', link: '/ai/04-neural-networks/03-training-techniques' },
              { text: '第4章: 卷积网络', link: '/ai/04-neural-networks/04-convolutional-networks' },
              { text: '第5章: RNN与序列模型', link: '/ai/04-neural-networks/05-rnn-and-sequence' }
            ]
          },
          {
            text: '卷5: Transformer',
            collapsed: false,
            items: [
              { text: '第1章: 注意力机制', link: '/ai/05-transformer/01-attention-mechanism' },
              { text: '第2章: Transformer架构', link: '/ai/05-transformer/02-transformer-architecture' },
              { text: '第3章: 变体与演进', link: '/ai/05-transformer/03-variants-evolution' },
              { text: '第4章: 动手实现Transformer', link: '/ai/05-transformer/04-implement-transformer' }
            ]
          },
          {
            text: '卷6: 自监督学习',
            collapsed: false,
            items: [
              { text: '第1章: 预训练范式', link: '/ai/06-self-supervised/01-pretraining-paradigm' },
              { text: '第2章: 对比学习', link: '/ai/06-self-supervised/02-contrastive-learning' },
              { text: '第3章: 掩码建模', link: '/ai/06-self-supervised/03-masked-modeling' },
              { text: '第4章: 自回归建模', link: '/ai/06-self-supervised/04-autoregressive-modeling' },
              { text: '第5章: 预训练与微调', link: '/ai/06-self-supervised/05-pretrain-finetune' }
            ]
          },
          {
            text: '卷7: 生成式AI/LLM',
            collapsed: false,
            items: [
              { text: '第1章: 变分自编码器(VAE)', link: '/ai/07-generative-ai/01-vae' },
              { text: '第2章: 生成对抗网络(GAN)', link: '/ai/07-generative-ai/02-gan' },
              { text: '第3章: 扩散模型', link: '/ai/07-generative-ai/03-diffusion-models' },
              { text: '第4章: 大语言模型', link: '/ai/07-generative-ai/04-large-language-models' },
              { text: '第5章: LoRA与微调', link: '/ai/07-generative-ai/05-lora-and-finetuning' }
            ]
          },
          {
            text: '卷8: 模型训练工程',
            collapsed: false,
            items: [
              { text: '第1章: PyTorch深入', link: '/ai/08-model-training/01-pytorch-deep-dive' },
              { text: '第2章: 训练循环精通', link: '/ai/08-model-training/02-training-loop-mastery' },
              { text: '第3章: 分布式训练', link: '/ai/08-model-training/03-distributed-training' },
              { text: '第4章: 数据管道', link: '/ai/08-model-training/04-data-pipeline' },
              { text: '第5章: 部署基础', link: '/ai/08-model-training/05-deployment-basics' },
              { text: '第6章: Python ML生态', link: '/ai/08-model-training/06-python-ml-ecosystem' }
            ]
          },
          {
            text: '卷9: LLM应用开发',
            collapsed: false,
            items: [
              { text: '第1章: 提示工程', link: '/ai/09-llm-application/01-prompt-engineering' },
              { text: '第2章: RAG', link: '/ai/09-llm-application/02-rag' },
              { text: '第3章: 工具调用', link: '/ai/09-llm-application/03-tool-calling' },
              { text: '第4章: 智能体系统', link: '/ai/09-llm-application/04-agent-systems' },
              { text: '第5章: 评估与监控', link: '/ai/09-llm-application/05-evaluation-and-monitoring' }
            ]
          },
          {
            text: '卷10: 工具链集成',
            collapsed: false,
            items: [
              { text: '第1章: AI编程助手', link: '/ai/10-toolchain-integration/01-ai-coding-assistants' },
              { text: '第2章: Agent Harness深入', link: '/ai/10-toolchain-integration/02-agent-harness-deep-dive' },
              { text: '第3章: MCP与工具', link: '/ai/10-toolchain-integration/03-mcp-and-tools' },
              { text: '第4章: 技能与提示系统', link: '/ai/10-toolchain-integration/04-skill-and-prompt-system' },
              { text: '第5章: 构建自己的工具', link: '/ai/10-toolchain-integration/05-build-your-own-tool' },
              { text: '第6章: 总结与路线图', link: '/ai/10-toolchain-integration/06-conclusion-and-roadmap' }
            ]
          }
        ]
      },
      {
        text: '🐧 Arch Linux',
        items: [
          { text: '安装与配置', link: '/archlinux/' }
        ]
      },
      {
        text: '☯ 周易 & 奇门遁甲',
        items: [
          { text: '奇门遁甲', link: '/qimen/' }
        ]
      }
    ]
  }
})
