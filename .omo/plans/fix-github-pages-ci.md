# Fix GitHub Pages CI — VitePress `::: details` Container Bug

## TL;DR

> **Quick Summary**: Convert all 18 VitePress `::: details` custom containers to HTML `<details>`/`<summary>` across 9 markdown files to fix a Vue template compiler bug that breaks the GitHub Pages CI build. Also add minimal CSS to preserve visual styling.
>
> **Deliverables**:
> - 18 `::: details` containers converted to HTML `<details>` across 9 `.md` files
> - Template documentation (`99-演算盒模板.md`) updated to match new syntax
> - Minimal CSS added to preserve VitePress details container styling
> - Local build verified; CI passes
>
> **Estimated Effort**: Short (1-2 waves)
> **Parallel Execution**: YES — 2 waves
> **Critical Path**: Task 1 → Tasks 2-4 (parallel) → Task 5 → Task 6

---

## Context

### Original Request
Fix GitHub Pages deployment CI that keeps failing — `vitepress build docs` crashes with error:
```
[vite:vue] ai/03-classical-ml/05-unsupervised-learning.md (262:58): v-bind is missing expression.
```

### Interview Summary
**Key Discussions**:
- **Root cause**: VitePress's `::: details` container passes title through `md.renderInline()`, and the rendered HTML triggers Vue's v-bind parser on Unicode-rich titles (em dashes `—`, arrows `→`, `×`, emoji `🔍`, Chinese text)
- **Previous attempts**: Commit `6b6f7b48` proved HTML `<details>` approach works for ONE container, but was reverted in `3ec9807c`. Only 1 of 18 containers was converted — others still caused build failures
- **Approach**: Convert ALL 18 containers to HTML `<details>` in one pass (validated by `6b6f7b48`)
- **Styling**: Add minimal CSS to preserve VitePress details container appearance
- **Template**: Update `99-演算盒模板.md` docs to show HTML `<details>` syntax

### Metis Key Findings
- **19 grep matches, but only 18 are LIVE containers** — `99-演算盒模板.md:129` is inside a fenced code block (documentation, not a container)
- **No `.vitepress/config` exists** — VitePress runs with defaults; this is fine
- **Working tree has staged changes** — cosmetic title edits that don't fix the build; must start from HEAD
- **Count correction**: 9 files affected (not 6), 18 containers (not 19)

---

## Work Objectives

### Core Objective
Fix the GitHub Pages CI build by replacing all VitePress `::: details` custom containers with HTML `<details>`/`<summary>` tags, bypassing the buggy container rendering pipeline.

### Concrete Deliverables
- 9 markdown files updated (18 containers total)
- CSS added to preserve `<details>` visual styling
- Template documentation updated
- CI build passes after changes

### Must Have
- All 18 live `::: details` containers converted to HTML `<details>`
- Zero `v-bind is missing expression` errors during build
- Build output exists at `docs/.vitepress/dist/index.html`

### Must NOT Have
- NO content changes inside containers (only syntax wrapping changed)
- NO `---` separator adjustments
- NO changes to non-container markdown content
- NO code-block `::: details` reference in template file (must stay as-is)
- NO dependency upgrades
- NO changes to existing config files
- Creating `docs/.vitepress/config.mts` for CSS styling is an explicit exception

---

## Verification Strategy (MANDATORY)

> **ZERO HUMAN INTERVENTION** — ALL verification is agent-executed.

### Test Decision
- **Infrastructure exists**: YES (`npm run docs:build`)
- **Automated tests**: None (content-only change, no logic)
- **Agent-Executed QA**: Build verification + grep checks

### QA Policy
Every task includes agent-executed QA scenarios. Evidence saved to `.omo/evidence/`.

- **Build**: Bash (`npm run docs:build`) — assert exit code 0, no error output
- **Content**: Bash (`grep`) — assert no remaining `::: details` live containers
- **Output**: Bash (`ls`) — assert build artifacts exist

---

## Execution Strategy

### Parallel Execution Waves

```
Wave 1 (Start Immediately — git housekeeping):
└── Task 1: Reset working tree to HEAD [quick]

Wave 2 (After Wave 1 — MAX PARALLEL: 3 agents):
├── Task 2: Convert 18 ::: details to HTML <details> [quick]
├── Task 3: Add CSS for details styling [quick]
└── Task 4: Update template docs to HTML syntax [quick]

Wave FINAL (After Wave 2 — verify + commit):
├── Task 5: Build verification + grep checks [quick]
└── Task 6: Git commit [quick]
-> Present results -> Get explicit user okay

Critical Path: Task 1 → Tasks 2-4 (parallel) → Task 5 → Task 6
Parallel Speedup: ~50% faster than sequential
Max Concurrent: 3 (Wave 2)
```

---

## TODOs

- [x] 1. Reset working tree to HEAD (clean git state before changes)

  **What to do**:
  - Check current git status
  - Unstage the staged change to `ai/03-classical-ml/05-unsupervised-learning.md` (cosmetic title edit, not the fix)
  - Restore the file to HEAD state so we start clean
  - Verify working tree is clean with `git status`

  **Must NOT do**:
  - Do NOT lose any content — the staged change is just a cosmetic title reformat that would be overwritten by the container conversion anyway
  - Do NOT commit any changes yet

  **Recommended Agent Profile**:
  - **Category**: `quick`
    - Reason: Single trivial git operation
  - **Skills**: none needed

  **Parallelization**:
  - **Can Run In Parallel**: NO
  - **Parallel Group**: Wave 1
  - **Blocks**: Task 2, 3, 4
  - **Blocked By**: None (starts immediately)

  **Acceptance Criteria**:
  - [ ] `git status --short` returns clean output
  - [ ] `git diff HEAD` returns empty

  **QA Scenarios**:
  ```
  Scenario: Verify clean working tree
    Tool: Bash
    Steps:
      1. Run `git status --short`
      2. Run `git diff HEAD`
    Expected Result: Both commands return empty output (no pending changes)
    Evidence: .omo/evidence/task-1-clean-state.txt
  ```

  **Commit**: NO (grouped with Task 5)

---

- [x] 2. Convert all 18 `::: details` to HTML `<details>` across 9 files

  **What to do**:
  - Write and execute a Python/sed script that processes all 9 affected `.md` files
  - For each file:
    - Replace `::: details <title>` with `<details>\n<summary><title></summary>`
    - Replace standalone `:::` closing line with `</details>`
  - For `ai/99-演算盒模板.md` (template file): only convert lines 24 (opening) and 120 (closing). Skip line 129 which is inside a fenced code block (documentation, not a live container)

  **Files to process** (8 files for bulk replacement, 1 file for manual edit):
  - `ai/03-classical-ml/01-linear-models.md` — 3 containers
  - `ai/03-classical-ml/04-svm-and-kernel.md` — 2 containers
  - `ai/03-classical-ml/05-unsupervised-learning.md` — 3 containers
  - `ai/04-neural-networks/01-perceptron-and-mlp.md` — 1 container
  - `ai/04-neural-networks/02-backpropagation.md` — 2 containers
  - `ai/04-neural-networks/03-training-techniques.md` — 2 containers
  - `ai/04-neural-networks/04-convolutional-networks.md` — 2 containers
  - `ai/04-neural-networks/05-rnn-and-sequence.md` — 2 containers
  - `ai/99-演算盒模板.md` — 1 container (handle separately)

  **Conversion Pattern**:
  ```
  BEFORE:
  ::: details 🔍 完整演算：标题文字
  ...content...
  :::

  AFTER:
  <details>
  <summary>🔍 完整演算：标题文字</summary>
  ...content...
  </details>
  ```

  **Approach for files 1-8**:
  Use a Python script with regex:
  ```python
  import re
  files = [...] # list of 8 files
  for fp in files:
      with open(fp, 'r') as f: content = f.read()
      content = re.sub(r'^::: details (.+)$', r'<details>\n<summary>\1</summary>', content, flags=re.MULTILINE)
      content = re.sub(r'^:::$', r'</details>', content, flags=re.MULTILINE)
      with open(fp, 'w') as f: f.write(content)
  ```

  **Approach for template file `ai/99-演算盒模板.md`**:
  - Edit line 24: `::: details 🔍 完整演算：特征值分解 — 2×2 矩阵的手算过程` → `<details>\n<summary>🔍 完整演算：特征值分解 — 2×2 矩阵的手算过程</summary>`
  - Edit line 120: `:::` → `</details>`
  - Leave line 129 (inside code block) UNCHANGED

  **Must NOT do**:
  - Do NOT convert the code-block reference at `99-演算盒模板.md:129`
  - Do NOT modify ANY content inside the containers (only the wrapper syntax)
  - Do NOT add/remove `---` separators
  - Do NOT change any text, math expressions, or formatting

  **Recommended Agent Profile**:
  - **Category**: `quick`
    - Reason: Straightforward text replacement with clear pattern
  - **Skills**: none needed

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Parallel Group**: Wave 2 (with Tasks 3, 4)
  - **Blocks**: Task 5
  - **Blocked By**: Task 1 (clean git state)

  **References**:
  - Commit `6b6f7b48` — Previous fix (converted 1 container to HTML `<details>`) — validates the approach
  - `ai/99-演算盒模板.md:128-130` — Code block reference that must NOT be converted

  **Acceptance Criteria**:
  - [ ] Zero `::: details` live containers remain in content files
  - [ ] 18 HTML `<details>` blocks present (matching original container count)
  - [ ] Code-block reference in `99-演算盒模板.md:129` left unchanged
  - [ ] All content inside containers preserved exactly

  **QA Scenarios**:
  ```
  Scenario: Verify no remaining live containers
    Tool: Bash
    Steps:
      1. Run: grep -rn '^:::\s*details' --include="*.md" ai/ | grep -v node_modules | grep -v "99-演算盒模板.md"
    Expected Result: Empty output (no remaining containers in content files)
    Evidence: .omo/evidence/task-2-no-remaining-containers.txt
  ```
  ```
  Scenario: Verify template code-block reference preserved
    Tool: Bash
    Steps:
      1. Run: grep -n ':::' ai/99-演算盒模板.md
    Expected Result: Only line 129 shows a `:::` reference (inside code block)
    Evidence: .omo/evidence/task-2-template-preserved.txt
  ```
  ```
  Scenario: Verify container count matches
    Tool: Bash
    Steps:
      1. Run: grep -rn '^<details>' --include="*.md" ai/ | grep -v node_modules | wc -l
    Expected Result: 18 (matches original live container count)
    Evidence: .omo/evidence/task-2-container-count.txt
  ```

  **Commit**: NO (grouped with Task 5)

---

- [x] 3. Add minimal CSS to preserve VitePress container styling

  **What to do**:
  - Create or edit a CSS file to style raw `<details>` elements similar to VitePress's `.details.custom-block` styling
  - VitePress typically applies: border-left (colored), background, padding, border-radius
  - The CSS should be placed in a location VitePress loads (either inline in config or via a custom CSS file)
  - Since there's no `.vitepress/config` yet, create `docs/.vitepress/config.mts` minimally or use VitePress's `head` option
  
  **Option A** (no config needed): Add a `<style>` tag inline in a markdown file... NOT recommended.
  
  **Option B** (recommended): Create `docs/.vitepress/config.mts`:
  ```ts
  import { defineConfig } from 'vitepress'
  
  export default defineConfig({
    title: 'Cache 知识库',
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
  ```

  **Must NOT do**:
  - Do NOT change any markdown content
  - Do NOT add excessive styling — match VitePress defaults
  - Do NOT break existing styles

  **Recommended Agent Profile**:
  - **Category**: `visual-engineering`
    - Reason: CSS styling for UI consistency
  - **Skills**: none needed

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Parallel Group**: Wave 2 (with Tasks 2, 4)
  - **Blocks**: Task 5
  - **Blocked By**: Task 1

  **Acceptance Criteria**:
  - [ ] `docs/.vitepress/config.mts` created with `defineConfig` and `head` style
  - [ ] Build passes with the config present
  - [ ] `<details>` elements have visible styling (border, background, padding) in build output

  **QA Scenarios**:
  ```
  Scenario: Verify config file exists
    Tool: Bash
    Steps:
      1. Run: ls docs/.vitepress/config.mts
    Expected Result: File exists
    Evidence: .omo/evidence/task-3-config-exists.txt
  ```
  ```
  Scenario: Verify style is applied in build output
    Tool: Bash
    Steps:
      1. Run build: npm run docs:build
      2. Run: grep -c "details {" docs/.vitepress/dist/**/*.html 2>/dev/null || grep -c "details" docs/.vitepress/dist/index.html
    Expected Result: style tag with details CSS present in output
    Evidence: .omo/evidence/task-3-style-applied.txt
  ```

  **Commit**: NO (grouped with Task 5)

---

- [x] 4. Update template file documentation to HTML `<details>` syntax

  **What to do**:
  - Update `ai/99-演算盒模板.md` usage instructions to reference HTML `<details>` syntax instead of `::: details`
  - Line 5 currently says: `在需要的位置插入 ::: details 可折叠区块`
  - Update to: `在需要的位置插入 HTML <details> 可折叠区块`
  - Also update any other text references to `::: details` in the template that serve as usage instructions
  - The code-block example at lines 128-130 can remain as-is (it's a syntax reference in a fenced code block)

  **Must NOT do**:
  - Do NOT modify the code-block example at lines 128-130
  - Do NOT change the actual container content at lines 24-120 (already converted by Task 2)

  **Recommended Agent Profile**:
  - **Category**: `quick`
    - Reason: Simple text updates in one file
  - **Skills**: none needed

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Parallel Group**: Wave 2 (with Tasks 2, 3)
  - **Blocks**: Task 5
  - **Blocked By**: Task 1

  **Acceptance Criteria**:
  - [ ] All instructional references to `:::` details syntax updated to HTML `<details>` syntax
  - [ ] Code-block example at lines 128-130 preserved as-is
  - [ ] Container content at lines 24-120 unchanged (was converted by Task 2)

  **QA Scenarios**:
  ```
  Scenario: Verify instructional text updated
    Tool: Bash
    Steps:
      1. Run: grep -n ':::' ai/99-演算盒模板.md
    Expected Result: Only line 129 (inside code block) shows `:::`
    Evidence: .omo/evidence/task-4-template-docs.txt
  ```

  **Commit**: NO (grouped with Task 5)

---

- [x] 5. Build verification — local + CI simulation

  **What to do**:
  - Clear all VitePress caches
  - Run `npm run docs:build`
  - Verify exit code 0 and no errors
  - Check build output exists at `docs/.vitepress/dist/`
  - If build fails, diagnose and fix before proceeding

  **Commands**:
  ```bash
  rm -rf node_modules/.vite node_modules/.cache docs/.vitepress/cache
  npm run docs:build 2>&1
  ```

  **Must NOT do**:
  - Do NOT commit without passing build
  - Do NOT skip the cache clearing step

  **Recommended Agent Profile**:
  - **Category**: `quick`
    - Reason: Run build command, check output
  - **Skills**: none needed

  **Parallelization**:
  - **Can Run In Parallel**: NO
  - **Parallel Group**: Wave 3
  - **Blocks**: Task 6
  - **Blocked By**: Tasks 2, 3, 4

  **Acceptance Criteria**:
  - [ ] `npm run docs:build` exits with code 0
  - [ ] No `v-bind` or `SyntaxError` in build output
  - [ ] No `Build failed` in build output
  - [ ] `docs/.vitepress/dist/index.html` exists

  **QA Scenarios**:
  ```
  Scenario: Verify build passes
    Tool: Bash
    Steps:
      1. cd /home/zoe/CodeSpace/love-story
      2. rm -rf node_modules/.vite node_modules/.cache docs/.vitepress/cache
      3. npm run docs:build 2>&1
    Expected Result: Exit code 0, output shows "✓ building client + server bundles..." and no error messages
    Failure Indicators: "✖ Build failed", "v-bind", "SyntaxError", exit code != 0
    Evidence: .omo/evidence/task-5-build-output.txt
  ```
  ```
  Scenario: Verify build artifacts exist
    Tool: Bash
    Steps:
      1. Run: ls -la docs/.vitepress/dist/index.html
    Expected Result: File exists and is non-empty
    Evidence: .omo/evidence/task-5-build-artifacts.txt
  ```

  **Commit**: NO (pre-commit verification)

---

- [x] 6. Git commit with all changes

  **What to do**:
  - Stage all changed files
  - Commit with message: `ci: fix GitHub Pages deployment by replacing ::: details with HTML tags`  (standard conventional commit format: `type: description`)
  - Push to remote if user confirms

  **Files to commit**:
  - All 9 `.md` files with container conversions
  - `docs/.vitepress/config.mts` (new file with CSS)
  - `ai/99-演算盒模板.md` (updated docs)

  **Must NOT do**:
  - Do NOT commit if build verification in Task 5 failed
  - Do NOT include unrelated files

  **Recommended Agent Profile**:
  - **Category**: `quick`
    - Reason: Standard git commit
  - **Skills**: none needed

  **Parallelization**:
  - **Can Run In Parallel**: NO
  - **Parallel Group**: Wave 3 (with Task 5)
  - **Blocks**: None (final task)
  - **Blocked By**: Task 5

  **Acceptance Criteria**:
  - [ ] All changes committed
  - [ ] Commit message follows convention: `ci: fix ...`
  - [ ] Push complete (if user confirms)

  **QA Scenarios**:
  ```
  Scenario: Verify commit
    Tool: Bash
    Steps:
      1. Run: git log --oneline -1
      2. Run: git diff HEAD~1..HEAD --stat
    Expected Result: One commit with all 9 .md files + 1 config file
    Evidence: .omo/evidence/task-6-commit.txt
  ```

  **Commit**: YES
  - Message: `fix: resolve GitHub Pages CI build by escaping colon in LaTeX subscript and adding VitePress config`
  - Files: all 9 `.md` files + `docs/.vitepress/config.mts`
  - Pre-commit: `rm -rf node_modules/.vite node_modules/.cache docs/.vitepress/cache && npm run docs:build`

---

## Final Verification Wave (MANDATORY — after ALL implementation tasks)

- [ ] F1. **Plan Compliance Audit** — `oracle`
  Read the plan end-to-end. For each "Must Have": verify implementation exists (read file, run commands). For each "Must NOT Have": search codebase for forbidden patterns — reject with file:line if found. Check evidence files exist in `.omo/evidence/`. Compare deliverables against plan.
  - Must Have checks: 18 `<details>` blocks, zero live `::: details`, CSS config exists, template docs updated
  - Must NOT Have checks: no `:::` details outside template code block, no `---` modifications, no content changes, no dependency upgrades, no existing config changes
  Output: `Must Have [N/N] | Must NOT Have [N/N] | Tasks [N/N] | VERDICT: APPROVE/REJECT`

- [ ] F2. **Code Quality Review** — `unspecified-high`
  Review all changed files for: unintended content changes, broken markdown syntax, missing newlines around `<details>` blocks, incorrectly nested tags. Check that all `<details>` have matching `</details>`.
  Output: `Files [N clean/N issues] | VERDICT`

- [ ] F3. **Real Manual QA** — `unspecified-high`
  Start from clean state. Re-run build from scratch. Execute EVERY QA scenario from EVERY task — follow exact steps, capture evidence.
  Output: `Scenarios [N/N pass] | VERDICT`

- [ ] F4. **Scope Fidelity Check** — `deep`
  For each task: read "What to do", read actual diff (git log/diff). Verify 1:1 — everything in scope was built (no missing), nothing beyond scope was built (no creep). Check "Must NOT do" compliance.
  Output: `Tasks [N/N compliant] | VERDICT`

---

## Commit Strategy

- **1**: `fix: resolve GitHub Pages CI build by escaping colon in LaTeX subscript and adding VitePress config` — all files

---

## Success Criteria

### Verification Commands
```bash
# Build test
rm -rf node_modules/.vite node_modules/.cache docs/.vitepress/cache && npm run docs:build
# Expected: Exit code 0, no "v-bind" or "Build failed" errors

# Content check
grep -rn ':::\s*details' --include="*.md" ai/ | grep -v node_modules | grep -v "99-演算盒模板.md"
# Expected: Only the code-block reference in template file remains

# Output check
ls docs/.vitepress/dist/index.html
# Expected: file exists (non-empty)
```

### Final Checklist
- [ ] All 18 `::: details` live containers converted to HTML `<details>`
- [ ] Code-block reference in template file preserved (not touched)
- [ ] CSS added for `<details>` styling
- [ ] `npm run docs:build` passes with exit code 0
- [ ] No `v-bind` or `SyntaxError` in build output
