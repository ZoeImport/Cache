#!/usr/bin/env python3
"""Add IPA pronunciation annotations to AI/ML markdown files.

Usage: python add_ipa.py
"""

import re
import os
import glob

TERMS = [
    ("backpropagation", "/ˌbækprəpəˈɡeɪʃən/", "反向传播"),
    ("hyperparameter",  "/ˈhaɪpərpəˈræmɪtər/", "超参数"),
    ("classification",  "/ˌklæsɪfɪˈkeɪʃən/", "分类"),
    ("regularization",  "/ˌreɡjələraɪˈzeɪʃən/", "正则化"),
    ("normalization",   "/ˌnɔːrmələˈzeɪʃən/", "归一化"),
    ("reinforcement",   "/ˌriːɪnˈfɔːrsmənt/", "强化"),
    ("underfitting",    "/ˈʌndərˈfɪtɪŋ/", "欠拟合"),
    ("overfitting",     "/ˈoʊvərˈfɪtɪŋ/", "过拟合"),
    ("autoencoder",     "/ˈɔːtoʊənˈkoʊdər/", "自编码器"),
    ("distillation",    "/ˌdɪstɪˈleɪʃən/", "蒸馏"),
    ("convolution",     "/ˌkɒnvəˈluːʃən/", "卷积"),
    ("transformer",     "/trænsˈfɔːrmər/", "变换器"),
    ("stochastic",      "/stəˈkæstɪk/", "随机"),
    ("regression",      "/rɪˈɡreʃən/", "回归"),
    ("embedding",       "/ɪmˈbedɪŋ/", "嵌入"),
    ("perplexity",      "/pərˈpleksəti/", "困惑度"),
    ("diffusion",       "/dɪˈfjuːʒən/", "扩散"),
    ("attention",       "/əˈtenʃən/", "注意力"),
    ("variational",     "/ˌveəriˈeɪʃənl/", "变分"),
    ("momentum",        "/məˈmentəm/", "动量"),
    ("gradient",        "/ˈɡreɪdiənt/", "梯度"),
    ("entropy",         "/ˈentrəpi/", "熵"),
    ("dropout",         "/ˈdrɒpaʊt/", "随机失活"),
    ("pooling",         "/ˈpuːlɪŋ/", "池化"),
    ("sigmoid",         "/ˈsɪɡmɔɪd/", "S型函数"),
    ("softmax",         "/sɒftˈmæks/", "柔性最大值"),
    ("inference",       "/ˈɪnfərəns/", "推理"),
    ("quantize",        "/ˈkwɒntaɪz/", "量化"),
    ("latent",          "/ˈleɪtənt/", "潜在"),
    ("scalar",          "/ˈskeɪlər/", "标量"),
    ("tensor",          "/ˈtensər/", "张量"),
    ("agent",           "/ˈeɪdʒənt/", "智能体"),
    ("encoder",         "/ɪnˈkoʊdər/", "编码器"),
    ("decoder",         "/diːˈkoʊdər/", "解码器"),
    ("parameter",       "/pəˈræmɪtər/", "参数"),
    ("kernel",          "/ˈkɜːrnl/", "核"),
    ("ndarray",         "/ˈen diː ˌæreɪ/", None),
]

SKIP_MULTILINE = re.compile(
    r'```[\s\S]*?```|'
    r'(?<!\$)\$\$(?!\$)[\s\S]*?\$\$|'
    r'<!--[\s\S]*?-->'
)


def _build_occupied(text):
    ranges = []
    for m in re.finditer(r'[\u4e00-\u9fff\w]+[（(]\s*\w+\s*/[^）)]*[）)]', text):
        ranges.append((m.start(), m.end()))
    for m in re.finditer(r'\b[a-zA-Z]+\b[（(]\s*/', text):
        end = text.find('）', m.end())
        if end == -1:
            end = text.find(')', m.end())
        if end == -1:
            end = m.end() + 5
        else:
            end += 1
        ranges.append((m.start(), end))
    ranges.sort()
    merged = []
    for s, e in ranges:
        if merged and s <= merged[-1][1]:
            merged[-1] = (merged[-1][0], max(merged[-1][1], e))
        else:
            merged.append((s, e))
    return merged


def find_first_in_text(text, term_en, term_zh, occupied):
    def in_skip(p):
        for s, e in occupied:
            if s <= p < e:
                return True
        return False

    segments = []
    pos = 0
    for m in SKIP_MULTILINE.finditer(text):
        if m.start() > pos:
            segments.append((pos, m.start()))
        pos = m.end()
    if pos < len(text):
        segments.append((pos, len(text)))

    best = None

    for seg_start, seg_end in segments:
        seg_text = text[seg_start:seg_end]
        lines = seg_text.split('\n')
        line_offsets = []
        cum = seg_start
        for line in lines:
            if line.strip() and not line.strip().startswith('#'):
                line_offsets.append((cum, cum + len(line)))
            cum += len(line) + 1

        for ls, le in line_offsets:
            sub = text[ls:le]
            if not sub.strip():
                continue
            inline_skips = [(m.start() + ls, m.end() + ls)
                           for m in re.finditer(r'`[^`]*`|\$[^$]*\$', sub)]

            def not_skipped(p):
                if any(s <= p < e for s, e in inline_skips):
                    return False
                if in_skip(p):
                    return False
                return True

            if term_zh is not None:
                search_from = ls
                while True:
                    zh_idx = text.find(term_zh, search_from, le)
                    if zh_idx == -1:
                        break
                    abs_pos = zh_idx
                    if not_skipped(abs_pos):
                        ahead = text[abs_pos + len(term_zh):abs_pos + len(term_zh) + len(term_en) + 5]
                        if not re.match(r'[（(]\s*' + re.escape(term_en) + r'\s*/', ahead, re.IGNORECASE):
                            cand = (abs_pos, abs_pos + len(term_zh), term_zh, True)
                            if best is None or abs_pos < best[0]:
                                best = cand
                            break
                    search_from = abs_pos + 1
                    if search_from >= le:
                        break

            en_pat = r'(?<![a-zA-Z])' + re.escape(term_en) + r'(?![a-zA-Z])'
            for m_en in re.finditer(en_pat, sub, re.IGNORECASE):
                abs_pos = ls + m_en.start()
                if not_skipped(abs_pos):
                    after = text[abs_pos + len(m_en.group()):abs_pos + len(m_en.group()) + 3]
                    if re.match(r'[（(]\s*/', after) or after.startswith(' /'):
                        continue
                    cand = (abs_pos, abs_pos + len(m_en.group()), m_en.group(), False)
                    if best is None or abs_pos < best[0]:
                        best = cand

    return best


def make_annotation(matched_text, term_en, ipa, is_chinese):
    if is_chinese:
        return f'{matched_text}（{term_en} {ipa}）'
    else:
        return f'{matched_text}（{ipa}）'


def _has_term_annotation(text, term_en, term_zh):
    """Check if the file already has an IPA annotation for this specific term."""
    if term_zh:
        pat = re.escape(term_zh) + r'[（(]' + re.escape(term_en) + r'\s*/'
        if re.search(pat, text, re.IGNORECASE):
            return True
    pat = r'(?<![a-zA-Z])' + re.escape(term_en) + r'(?![a-zA-Z])[（(]/'
    if re.search(pat, text, re.IGNORECASE):
        return True
    return False


def annotate_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        text = f.read()
    original = text
    occupied = _build_occupied(text)

    for term_en, ipa, term_zh in TERMS:
        if _has_term_annotation(text, term_en, term_zh):
            continue
        result = find_first_in_text(text, term_en, term_zh, occupied)
        if result is None:
            continue
        start, end, matched, is_chinese = result
        annotation = make_annotation(matched, term_en, ipa, is_chinese)
        text = text[:start] + annotation + text[end:]
        shift = len(annotation) - (end - start)
        occupied = [(s + shift if s >= end else s, e + shift if e >= end else e)
                    for s, e in occupied]
        occupied.append((start, start + len(annotation)))
        occupied.sort()

    if text != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(text)
        return True
    return False


def main():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    targets = []

    for i in range(1, 11):
        targets.extend(glob.glob(os.path.join(base_dir, f'{i:02d}-*', '*.md')))

    readme = os.path.join(base_dir, '00-README.md')
    if os.path.exists(readme):
        targets.append(readme)

    glossary = os.path.join(base_dir, '00-GLOSSARY.md')
    targets = [f for f in targets if f != glossary]
    targets.sort()

    print(f"Found {len(targets)} target files to process.")
    modified = 0
    for fp in targets:
        rel = os.path.relpath(fp, base_dir)
        try:
            if annotate_file(fp):
                print(f"  \u2713 {rel}")
                modified += 1
            else:
                print(f"  - {rel} (no changes)")
        except Exception as e:
            print(f"  \u2717 {rel} \u2014 ERROR: {e}")

    print(f"\nDone. {modified} files modified.")


if __name__ == '__main__':
    main()
