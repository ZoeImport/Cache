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
  ]
})
