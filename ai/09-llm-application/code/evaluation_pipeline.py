#!/usr/bin/env python3
"""
Evaluation & Monitoring Pipeline — LLM Output Quality Measurement

A mini evaluation pipeline demonstrating:
1. Evaluation dataset construction (golden dataset)
2. Evaluation metrics: Exact Match, F1, BLEU, ROUGE-L
3. LLM-as-Judge evaluation (simulated using HuggingFace transformers)
4. Comparison report between different models/prompts
5. Per-sample score breakdown

Dependencies: transformers, numpy, nltk (optional for BLEU)
Run: python evaluation_pipeline.py

Author: love-story AI
"""

import json
import math
import re
import sys
from dataclasses import dataclass, field
from typing import Callable
from collections import Counter

import numpy as np

# ============================================================
# Section 1: Evaluation Dataset
# ============================================================

@dataclass
class EvalSample:
    """A single evaluation sample."""
    input: str
    expected: str
    category: str = "general"
    difficulty: str = "medium"


@dataclass
class EvalResult:
    """Evaluation result for a single sample."""
    sample: EvalSample
    prediction: str
    exact_match: float
    f1_score: float
    bleu_score: float
    rouge_l_score: float
    judge_score: float = 0.0
    judge_reason: str = ""


def build_golden_dataset() -> list[EvalSample]:
    """Build a golden evaluation dataset with diverse categories."""
    return [
        # Geography (easy)
        EvalSample(
            input="What is the capital of France?",
            expected="Paris",
            category="geography",
            difficulty="easy",
        ),
        EvalSample(
            input="What is the capital of Japan?",
            expected="Tokyo",
            category="geography",
            difficulty="easy",
        ),
        EvalSample(
            input="Which river is the longest in the world?",
            expected="The Nile River",
            category="geography",
            difficulty="medium",
        ),
        # Science (medium)
        EvalSample(
            input="What is the chemical symbol for water?",
            expected="H2O",
            category="science",
            difficulty="easy",
        ),
        EvalSample(
            input="What planet is known as the Red Planet?",
            expected="Mars",
            category="science",
            difficulty="easy",
        ),
        EvalSample(
            input="What is the speed of light in vacuum?",
            expected="299,792,458 meters per second",
            category="science",
            difficulty="medium",
        ),
        # History (medium)
        EvalSample(
            input="In which year did World War II end?",
            expected="1945",
            category="history",
            difficulty="medium",
        ),
        EvalSample(
            input="Who was the first President of the United States?",
            expected="George Washington",
            category="history",
            difficulty="easy",
        ),
        # Technology (medium)
        EvalSample(
            input="What does CPU stand for?",
            expected="Central Processing Unit",
            category="technology",
            difficulty="easy",
        ),
        EvalSample(
            input="Who co-founded Apple Inc.?",
            expected="Steve Jobs, Steve Wozniak, and Ronald Wayne",
            category="technology",
            difficulty="medium",
        ),
        # Complex QA (hard)
        EvalSample(
            input="Explain the concept of recursion in computer science.",
            expected="Recursion is a programming technique where a function calls itself to solve a problem by breaking it down into smaller subproblems.",
            category="computer science",
            difficulty="hard",
        ),
        EvalSample(
            input="What is the difference between TCP and UDP?",
            expected="TCP is connection-oriented and guarantees reliable delivery, while UDP is connectionless and prioritizes speed over reliability.",
            category="computer science",
            difficulty="hard",
        ),
        # Math (medium)
        EvalSample(
            input="What is the value of Pi to 5 decimal places?",
            expected="3.14159",
            category="mathematics",
            difficulty="medium",
        ),
        # Literature (medium)
        EvalSample(
            input="Who wrote Romeo and Juliet?",
            expected="William Shakespeare",
            category="literature",
            difficulty="easy",
        ),
        EvalSample(
            input="What is the first book of the Bible?",
            expected="Genesis",
            category="religion",
            difficulty="easy",
        ),
    ]


# ============================================================
# Section 2: Mock LLM Implementations
# ============================================================

def mock_llm_gpt4_style(input_text: str) -> str:
    """Simulate a strong LLM (GPT-4 style) that answers accurately."""
    dataset = {
        "What is the capital of France?": "Paris",
        "What is the capital of Japan?": "Tokyo",
        "Which river is the longest in the world?": "The Nile River",
        "What is the chemical symbol for water?": "H2O",
        "What planet is known as the Red Planet?": "Mars",
        "What is the speed of light in vacuum?": "Approximately 299,792,458 meters per second",
        "In which year did World War II end?": "1945",
        "Who was the first President of the United States?": "George Washington",
        "What does CPU stand for?": "Central Processing Unit",
        "Who co-founded Apple Inc.?": "Steve Jobs, Steve Wozniak, and Ronald Wayne",
        "Explain the concept of recursion in computer science.": (
            "Recursion is a programming technique where a function calls itself "
            "to solve a problem by breaking it down into smaller subproblems."
        ),
        "What is the difference between TCP and UDP?": (
            "TCP is connection-oriented and guarantees reliable delivery, "
            "while UDP is connectionless and prioritizes speed over reliability."
        ),
        "What is the value of Pi to 5 decimal places?": "3.14159",
        "Who wrote Romeo and Juliet?": "William Shakespeare",
        "What is the first book of the Bible?": "Genesis",
    }
    # Return exact match with minor stylistic variation sometimes
    base = dataset.get(input_text, "I don't have information about that.")
    if "speed of light" in input_text:
        return base  # exact
    return base


def mock_llm_llama_style(input_text: str) -> str:
    """Simulate a weaker LLM that sometimes makes errors or is verbose."""
    answers = {
        "What is the capital of France?": "Paris",
        "What is the capital of Japan?": "Tokyo",
        "Which river is the longest in the world?": "Amazon River",  # WRONG
        "What is the chemical symbol for water?": "H2O",
        "What planet is known as the Red Planet?": "Mars",
        "What is the speed of light in vacuum?": "300,000,000 m/s",  # Approximate
        "In which year did World War II end?": "1945",
        "Who was the first President of the United States?": "George Washington",
        "What does CPU stand for?": "Central Processing Unit",
        "Who co-founded Apple Inc.?": "Steve Jobs",
        "Explain the concept of recursion in computer science.": (
            "Recursion means a function calls itself repeatedly until a base "
            "condition is met."
        ),
        "What is the difference between TCP and UDP?": (
            "TCP is reliable and UDP is fast."
        ),
        "What is the value of Pi to 5 decimal places?": "3.14",  # Not 5 places
        "Who wrote Romeo and Juliet?": "Shakespeare",
        "What is the first book of the Bible?": "Genesis",
    }
    return answers.get(input_text, "I don't know.")


def mock_llm_prompt_v2(input_text: str) -> str:
    """Simulate a prompt-optimized version that uses chain-of-thought style."""
    base = mock_llm_gpt4_style(input_text)
    # Add chain-of-thought prefix for some answers
    if "difference between TCP and UDP" in input_text:
        return "Let me think about this step by step. " + base
    if "recursion" in input_text:
        return "First, let me define the concept. " + base
    return base


# ============================================================
# Section 3: Evaluation Metrics
# ============================================================


def tokenize(text: str) -> list[str]:
    """Simple whitespace + punctuation tokenization."""
    text = text.lower().strip()
    return re.findall(r"\b\w+\b", text)


def compute_exact_match(prediction: str, expected: str) -> float:
    """Exact Match: 1.0 if identical after normalization, else 0.0."""
    p = prediction.strip().lower()
    e = expected.strip().lower()
    return 1.0 if p == e else 0.0


def compute_f1(prediction: str, expected: str) -> float:
    """Token-level F1 score."""
    pred_tokens = tokenize(prediction)
    expected_tokens = tokenize(expected)

    if not pred_tokens and not expected_tokens:
        return 1.0
    if not pred_tokens or not expected_tokens:
        return 0.0

    pred_counter = Counter(pred_tokens)
    expected_counter = Counter(expected_tokens)

    common = sum((pred_counter & expected_counter).values())

    if common == 0:
        return 0.0

    precision = common / len(pred_tokens)
    recall = common / len(expected_tokens)

    if precision + recall == 0:
        return 0.0

    return 2 * precision * recall / (precision + recall)


def compute_bleu(prediction: str, expected: str, max_n: int = 4) -> float:
    """Simplified BLEU score (no brevity penalty shortcut for demo)."""
    pred_tokens = tokenize(prediction)
    expected_tokens = tokenize(expected)

    if not pred_tokens or not expected_tokens:
        return 0.0

    # Brevity penalty
    bp = min(1.0, math.exp(1 - len(expected_tokens) / max(len(pred_tokens), 1)))

    precisions = []
    for n in range(1, min(max_n, 4) + 1):
        pred_ngrams = Counter(
            tuple(pred_tokens[i:i + n]) for i in range(len(pred_tokens) - n + 1)
        )
        expected_ngrams = Counter(
            tuple(expected_tokens[i:i + n]) for i in range(len(expected_tokens) - n + 1)
        )

        if not pred_ngrams:
            precisions.append(0.0)
            continue

        matches = sum((pred_ngrams & expected_ngrams).values())
        total = sum(pred_ngrams.values())

        precisions.append(matches / max(total, 1))

    # Geometric mean of precisions
    if any(p == 0 for p in precisions):
        return 0.0

    geo_mean = math.exp(sum(math.log(p) for p in precisions) / len(precisions))
    return bp * geo_mean


def compute_rouge_l(prediction: str, expected: str) -> float:
    """ROUGE-L: F-score based on longest common subsequence."""
    pred_tokens = tokenize(prediction)
    expected_tokens = tokenize(expected)

    # LCS length using dynamic programming
    m, n = len(pred_tokens), len(expected_tokens)
    dp = [[0] * (n + 1) for _ in range(m + 1)]

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if pred_tokens[i - 1] == expected_tokens[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
            else:
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])

    lcs = dp[m][n]

    if lcs == 0:
        return 0.0

    precision = lcs / max(m, 1)
    recall = lcs / max(n, 1)

    if precision + recall == 0:
        return 0.0

    return 2 * precision * recall / (precision + recall)


# ============================================================
# Section 4: LLM-as-Judge (simulated)
# ============================================================


def llm_judge(input_text: str, prediction: str, expected: str) -> tuple[float, str]:
    """Simulate LLM-as-Judge using rule-based scoring with detailed reasoning.

    In production, this would call GPT-4 / Claude with a structured rubric prompt.
    Here we simulate the judge's behavior based on metric signals.
    """
    em = compute_exact_match(prediction, expected)
    f1 = compute_f1(prediction, expected)
    rouge = compute_rouge_l(prediction, expected)

    # Base score from existing metrics
    base_score = 0.3 * em + 0.4 * f1 + 0.3 * rouge

    # Simulated judge reasoning
    if em == 1.0:
        reason = "The answer exactly matches the expected response. Excellent factual accuracy."
        return 5.0, reason

    if f1 >= 0.8:
        reason = (
            f"The answer is highly accurate (F1={f1:.2f}). "
            "It captures the core information with minor differences in phrasing."
        )
        score = min(5.0, 3.0 + base_score * 2)
        return round(score, 1), reason

    if f1 >= 0.5:
        reason = (
            f"The answer is partially correct (F1={f1:.2f}). "
            "It contains relevant information but misses some key details."
        )
        score = 1.5 + base_score * 2
        return round(score, 1), reason

    reason = (
        f"The answer has low overlap with expected (F1={f1:.2f}). "
        "It may be incorrect, incomplete, or addressing a different aspect."
    )
    score = max(1.0, base_score * 3)
    return round(score, 1), reason


# ============================================================
# Section 5: Evaluation Runner
# ============================================================


def evaluate_model(
    model_fn: Callable[[str], str],
    dataset: list[EvalSample],
    model_name: str,
) -> list[EvalResult]:
    """Run full evaluation of a model against the dataset."""
    results = []
    for sample in dataset:
        prediction = model_fn(sample.input)

        em = compute_exact_match(prediction, sample.expected)
        f1 = compute_f1(prediction, sample.expected)
        bleu = compute_bleu(prediction, sample.expected)
        rouge = compute_rouge_l(prediction, sample.expected)
        judge_score, judge_reason = llm_judge(
            sample.input, prediction, sample.expected
        )

        results.append(EvalResult(
            sample=sample,
            prediction=prediction,
            exact_match=em,
            f1_score=round(f1, 4),
            bleu_score=round(bleu, 4),
            rouge_l_score=round(rouge, 4),
            judge_score=judge_score,
            judge_reason=judge_reason,
        ))

    return results


# ============================================================
# Section 6: Report Generation
# ============================================================


def print_section(title: str, char: str = "=") -> None:
    """Print a section header."""
    print(f"\n{char * 70}")
    print(f"  {title}")
    print(f"{char * 70}")


def generate_report(results: list[EvalResult], model_name: str) -> dict:
    """Generate and print evaluation report."""
    n = len(results)
    if n == 0:
        return {}

    # Aggregate metrics
    avg_em = np.mean([r.exact_match for r in results])
    avg_f1 = np.mean([r.f1_score for r in results])
    avg_bleu = np.mean([r.bleu_score for r in results])
    avg_rouge = np.mean([r.rouge_l_score for r in results])
    avg_judge = np.mean([r.judge_score for r in results])

    # Per-category breakdown
    categories = {}
    for r in results:
        cat = r.sample.category
        if cat not in categories:
            categories[cat] = []
        categories[cat].append(r)

    report = {
        "model_name": model_name,
        "samples": n,
        "avg_exact_match": round(avg_em, 4),
        "avg_f1": round(avg_f1, 4),
        "avg_bleu": round(avg_bleu, 4),
        "avg_rouge_l": round(avg_rouge, 4),
        "avg_judge_score": round(avg_judge, 2),
        "categories": {},
    }

    # ==================== Overall Summary ====================
    print_section(f"Evaluation Report: {model_name}")
    print(f"  Total samples: {n}")
    print(f"  {'Metric':<25} {'Score':<10} {'Interpretation'}")
    print(f"  {'-'*25} {'-'*10} {'-'*30}")
    print(
        f"  {'Exact Match':<25} {avg_em:<10.4f} "
        f"{'Perfect match rate' if avg_em > 0.5 else 'Low exact match rate'}"
    )
    print(
        f"  {'F1 Score (token)':<25} {avg_f1:<10.4f} "
        f"{'Good token overlap' if avg_f1 > 0.7 else 'Moderate token overlap'}"
    )
    print(
        f"  {'BLEU Score':<25} {avg_bleu:<10.4f} "
        f"{'Good n-gram overlap' if avg_bleu > 0.5 else 'Low n-gram overlap'}"
    )
    print(
        f"  {'ROUGE-L Score':<25} {avg_rouge:<10.4f} "
        f"{'Good structure match' if avg_rouge > 0.7 else 'Moderate structure match'}"
    )
    print(f"  {'LLM-as-Judge Score':<25} {avg_judge:<10.2f} {'Out of 5.0'}")
    print(f"  {'-'*65}")

    # ==================== Per-Category Breakdown ====================
    print_section("Per-Category Breakdown", "-")
    print(f"  {'Category':<20} {'Samples':<8} {'EM':<8} {'F1':<8} {'BLEU':<8} {'Judge':<8}")
    print(f"  {'-'*20} {'-'*8} {'-'*8} {'-'*8} {'-'*8} {'-'*8}")
    for cat, cat_results in sorted(categories.items()):
        cat_em = np.mean([r.exact_match for r in cat_results])
        cat_f1 = np.mean([r.f1_score for r in cat_results])
        cat_bleu = np.mean([r.bleu_score for r in cat_results])
        cat_judge = np.mean([r.judge_score for r in cat_results])
        print(
            f"  {cat:<20} {len(cat_results):<8} "
            f"{cat_em:<8.3f} {cat_f1:<8.3f} {cat_bleu:<8.3f} {cat_judge:<8.2f}"
        )

        report["categories"][cat] = {
            "samples": len(cat_results),
            "avg_exact_match": round(cat_em, 4),
            "avg_f1": round(cat_f1, 4),
            "avg_bleu": round(cat_bleu, 4),
            "avg_judge_score": round(cat_judge, 2),
        }

    return report


def print_per_sample(results: list[EvalResult], model_name: str) -> None:
    """Print detailed per-sample evaluation."""
    print_section(f"Per-Sample Scores: {model_name}", "-")
    header = f"  {'#':<4} {'Category':<16} {'Difficulty':<10} {'EM':<6} {'F1':<6} {'BLEU':<6} {'ROUGE-L':<6} {'Judge':<6}"
    print(header)
    print(f"  {'-'*len(header)}")
    for i, r in enumerate(results):
        print(
            f"  {i+1:<4} {r.sample.category:<16} {r.sample.difficulty:<10} "
            f"{r.exact_match:<6.2f} {r.f1_score:<6.3f} {r.bleu_score:<6.3f} "
            f"{r.rouge_l_score:<6.3f} {r.judge_score:<6.1f}"
        )


def print_worst_samples(results: list[EvalResult], model_name: str, top_k: int = 3) -> None:
    """Print the lowest-scoring samples."""
    sorted_results = sorted(results, key=lambda r: r.judge_score)
    print_section(f"Lowest Scoring Samples: {model_name}", "-")
    for r in sorted_results[:top_k]:
        print(f"\n  Input:    {r.sample.input}")
        print(f"  Expected: {r.sample.expected}")
        print(f"  Got:      {r.prediction}")
        print(f"  F1:       {r.f1_score:.3f}  |  Judge: {r.judge_score:.1f}/5.0")
        print(f"  Reason:   {r.judge_reason}")


def compare_models(reports: list[dict]) -> None:
    """Print comparison table across different models."""
    print_section("Model Comparison Summary")
    header = f"  {'Model':<25} {'EM':<8} {'F1':<8} {'BLEU':<8} {'ROUGE-L':<8} {'Judge':<8}"
    print(header)
    print(f"  {'-'*len(header)}")
    for report in reports:
        print(
            f"  {report['model_name']:<25} "
            f"{report['avg_exact_match']:<8.3f} "
            f"{report['avg_f1']:<8.3f} "
            f"{report['avg_bleu']:<8.3f} "
            f"{report['avg_rouge_l']:<8.3f} "
            f"{report['avg_judge_score']:<8.2f}"
        )

    # Best model
    best = max(reports, key=lambda r: r["avg_judge_score"])
    print(f"\n  >> Best overall: {best['model_name']} (Judge: {best['avg_judge_score']:.2f}/5.0)")


# ============================================================
# Section 7: Main Pipeline
# ============================================================


def main():
    print("=" * 70)
    print("  LLM Evaluation Pipeline Demo")
    print("=" * 70)

    # Step 1: Build dataset
    print_section("Step 1: Building Evaluation Dataset")
    dataset = build_golden_dataset()
    print(f"  Dataset size: {len(dataset)} samples")
    categories = set(s.category for s in dataset)
    print(f"  Categories: {', '.join(sorted(categories))}")
    difficulties = set(s.difficulty for s in dataset)
    print(f"  Difficulties: {', '.join(sorted(difficulties))}")

    # Step 2: Evaluate models
    models = [
        ("GPT-4 (Strong LLM)", mock_llm_gpt4_style),
        ("Llama-3 (Weak LLM)", mock_llm_llama_style),
        ("GPT-4 + Prompt v2 (Optimized)", mock_llm_prompt_v2),
    ]

    all_reports = []
    all_results = []

    for model_name, model_fn in models:
        print_section(f"Step 2: Evaluating {model_name}")
        results = evaluate_model(model_fn, dataset, model_name)
        report = generate_report(results, model_name)
        print_per_sample(results, model_name)
        print_worst_samples(results, model_name)
        all_reports.append(report)
        all_results.append(results)

    # Step 3: Compare models
    print_section("Step 3: Cross-Model Comparison")
    compare_models(all_reports)

    # Step 4: Summary statistics
    print_section("Step 4: Key Takeaways")
    for report in all_reports:
        name = report["model_name"]
        em = report["avg_exact_match"]
        f1 = report["avg_f1"]
        judge = report["avg_judge_score"]
        print(f"  {name:<25} — EM={em:.2%}, F1={f1:.3f}, Judge Score={judge:.2f}/5.0")

    print(f"\n{'=' * 70}")
    print("  Evaluation complete. Run `python evaluation_pipeline.py` to re-run.")
    print(f"{'=' * 70}")


if __name__ == "__main__":
    main()
