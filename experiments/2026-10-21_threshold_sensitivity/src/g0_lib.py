"""Shared utilities for LLM-prior + symbolic-selection G0.

No API key is written to disk. The .env is read for a single process.
"""
from __future__ import annotations

import hashlib
import importlib
import inspect
import itertools
import json
import math
import os
import re
import sys
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import numpy as np
import requests

from applicability import BLACKLIST_TEMPLATES, is_applicable, is_blacklisted, is_text_blacklisted

CATEGORIES = [
    "subtraction",
    "fractions",
    "decimals",
    "negative_numbers",
    "order_of_operations",
    "percentages",
]

ROOT = Path(os.environ.get("SIM_ROOT", Path(__file__).resolve().parents[2])).resolve()
ENV_PATH = ROOT / ".env"
DESCRIPTIONS_PATH = ROOT / "data" / "library" / "malrule_descriptions.json"
REPO_PATH = ROOT / "data" / "external" / "malrulelib_repo"
OLD_G0_PATH = ROOT / "experiments" / "2026-10-20_g0_symbolic"
RUN_DIR = ROOT / "experiments" / "2026-10-20_llm_v4_v5"


def load_env(path: Path = ENV_PATH) -> dict[str, str]:
    values: dict[str, str] = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        if "=" in line and not line.strip().startswith("#"):
            key, value = line.split("=", 1)
            values[key.strip()] = value.strip().strip("\u200b\ufeff").strip()
    return values


def load_descriptions(path: Path = DESCRIPTIONS_PATH) -> list[dict]:
    return json.loads(path.read_text(encoding="utf-8"))


def ensure_imports():
    sys.path.insert(0, str(REPO_PATH))
    sys.path.insert(0, str(OLD_G0_PATH))
    import utils  # noqa: F401
    import g0_active_diagnosis as old  # noqa: F401

    for name in ["ProblemGenerator", "Malrule", "CorrectAlgorithm", "DifficultyLevel"]:
        setattr(old, name, getattr(utils, name))
    return old


# ---------------------------------------------------------------- bank


VALID_OPS = {
    "subtraction": {"subtraction"},
    "fractions": {
        "fraction_addition",
        "fraction_subtraction",
        "fraction_multiplication",
        "fraction_division",
        "fraction_comparison",
        "fraction_ordering",
    },
    "decimals": {
        "comparison",
        "decimal_comparison",
        "multiplication",
        "division",
        "subtraction",
        "mixed",
        "addition",
    },
    "negative_numbers": {
        "negative_subtraction",
        "arithmetic",
        "multiplication",
        "negative_addition",
        "comparison",
        "equation",
        "subtraction",
        "sequential_operations",
        "distributive",
        "multi_step",
        "addition",
        "division",
        "mixed",
    },
    "order_of_operations": {"order_of_operations"},
    "percentages": {
        "percentage_sequential",
        "percentage",
        "percentage_relationship",
        "percentage_conversion",
        "percentage_calculation",
    },
}


def _instantiate(cls, level: int):
    for args in [(), (level,)]:
        try:
            return cls(*args)
        except Exception:
            continue
    return None


def _load_category_classes(category: str):
    old = ensure_imports()
    utils = sys.modules["utils"]
    cat_dir = REPO_PATH / "malrules" / category
    rows = []
    for md in sorted(cat_dir.iterdir()):
        if not (md.is_dir() and (md / "__init__.py").exists()):
            continue
        module_name = f"malrules.{category}.{md.name}"
        module = importlib.import_module(module_name)
        generators, malrules, corrects = [], [], []
        for _, obj in vars(module).items():
            if not (inspect.isclass(obj) and obj.__module__.startswith(module_name)):
                continue
            if issubclass(obj, utils.ProblemGenerator) and not inspect.isabstract(obj):
                generators.append(obj)
            if issubclass(obj, utils.Malrule) and not inspect.isabstract(obj):
                malrules.append(obj)
            if issubclass(obj, utils.CorrectAlgorithm) and not inspect.isabstract(obj):
                corrects.append(obj)
        if generators and malrules:
            rows.append(
                (
                    md.name,
                    generators[0],
                    malrules[0],
                    corrects[0] if corrects else None,
                )
            )
    return rows, old


def _build_bank_v2(category: str, samples: int, level: int = 5) -> dict:
    rows, old = _load_category_classes(category)
    hyp_rows = [{"local": name, "id": f"{category}.{name}"} for name, _, _, _ in rows]
    hypotheses = []
    for name, _, malrule_cls, _ in rows:
        inst = _instantiate(malrule_cls, level)
        if inst is not None:
            hypotheses.append((name, inst))

    valid_ops = VALID_OPS.get(category)
    items, seen = [], set()
    for name, generator_cls, _, correct_cls in rows:
        generator = _instantiate(generator_cls, level)
        correct_algo = _instantiate(correct_cls, level) if correct_cls else None
        if generator is None or correct_algo is None:
            continue
        generated = 0
        for seed in range(samples * 40):
            if generated >= samples:
                break
            try:
                problem = generator.generate(seed=7000 + seed)
            except Exception:
                continue
            if valid_ops is not None and problem.operation not in valid_ops:
                continue
            key = problem.text.strip()
            if key in seen:
                continue
            seen.add(key)
            try:
                correct = old.normalize(correct_algo.solve(problem).answer)
            except Exception:
                continue
            predictions = {}
            for hyp_name, hyp in hypotheses:
                try:
                    predictions[hyp_name] = old.normalize(hyp.calculate_expected_answer(problem))
                except Exception:
                    continue
            if len(predictions) < 2:
                continue
            answers = sorted(set(list(predictions.values()) + [correct]))
            if len(answers) < 2:
                continue
            template = (problem.metadata or {}).get("template")
            items.append(
                {
                    "text": problem.text,
                    "source": f"{category}.{name}",
                    "operation": problem.operation,
                    "template": template,
                    "predictions": {f"{category}.{k}": v for k, v in predictions.items()},
                    "correct": correct,
                    "answers": answers,
                    "triggers": {
                        f"{category}.{k}": predictions[k] != correct for k in predictions
                    },
                }
            )
            generated += 1
    return {
        "category": category,
        "settings": {"samples_per_malrule": samples, "level": level, "builder": "v2_operation_filtered"},
        "hypotheses": hyp_rows,
        "items": items,
    }


def _build_bank_v3(category: str, samples: int, level: int = 5) -> dict:
    """Operation-filtered bank with per-malrule applicability and no multi-step items."""
    rows, old = _load_category_classes(category)
    hyp_rows = [{"local": name, "id": f"{category}.{name}"} for name, _, _, _ in rows]
    hypotheses = []
    for name, _, malrule_cls, _ in rows:
        inst = _instantiate(malrule_cls, level)
        if inst is not None:
            hypotheses.append((name, inst))

    valid_ops = VALID_OPS.get(category)
    items, seen = [], set()
    for name, generator_cls, _, correct_cls in rows:
        generator = _instantiate(generator_cls, level)
        correct_algo = _instantiate(correct_cls, level) if correct_cls else None
        if generator is None or correct_algo is None:
            continue
        generated = 0
        for seed in range(samples * 40):
            if generated >= samples:
                break
            try:
                problem = generator.generate(seed=7000 + seed)
            except Exception:
                continue
            if valid_ops is not None and problem.operation not in valid_ops:
                continue
            template = (problem.metadata or {}).get("template")
            if is_blacklisted(category, template) or is_text_blacklisted(problem.text):
                continue
            key = problem.text.strip()
            if key in seen:
                continue
            seen.add(key)
            try:
                correct = old.normalize(correct_algo.solve(problem).answer)
            except Exception:
                continue
            predictions = {}
            for hyp_name, hyp in hypotheses:
                try:
                    predictions[hyp_name] = old.normalize(hyp.calculate_expected_answer(problem))
                except Exception:
                    continue
            if len(predictions) < 2:
                continue
            answers = sorted(set(list(predictions.values()) + [correct]))
            if len(answers) < 2:
                continue
            items.append(
                {
                    "text": problem.text,
                    "source": f"{category}.{name}",
                    "operation": problem.operation,
                    "template": template,
                    "operands": list(problem.operands or []),
                    "predictions": {f"{category}.{k}": v for k, v in predictions.items()},
                    "correct": correct,
                    "answers": answers,
                }
            )
            generated += 1

    authored: dict[str, set[str]] = {}
    for name, _, _, _ in rows:
        source = f"{category}.{name}"
        authored[name] = {it["operation"] for it in items if it["source"] == source}

    for item in items:
        applicable = {
            f"{category}.{name}": is_applicable(category, name, item, authored)
            for name, _ in hypotheses
        }
        item["applicable"] = applicable
        item["triggers"] = {
            hid: bool(applicable[hid] and item["predictions"].get(hid, item["correct"]) != item["correct"])
            for hid in applicable
        }

    return {
        "category": category,
        "settings": {
            "samples_per_malrule": samples,
            "level": level,
            "builder": "v3_applicability",
            "blacklist_templates": sorted(BLACKLIST_TEMPLATES),
        },
        "hypotheses": hyp_rows,
        "items": items,
    }


def build_bank_cached(category: str, samples: int, force: bool = False) -> dict:
    path = RUN_DIR / f"bank_v3_{category}.json"
    if path.exists() and not force:
        return json.loads(path.read_text(encoding="utf-8"))
    bank = _build_bank_v3(category, samples=samples)
    path.write_text(json.dumps(bank, indent=1, ensure_ascii=False), encoding="utf-8")
    return bank


def build_bank_v4_cached(category: str, samples: int = 100, force: bool = False) -> dict:
    """Expanded bank for the clean template split and formal test."""
    path = RUN_DIR / f"bank_v4_{category}.json"
    if path.exists() and not force:
        return json.loads(path.read_text(encoding="utf-8"))
    bank = _build_bank_v3(category, samples=samples)
    bank["settings"]["builder"] = "v4_applicability_expanded"
    bank["settings"]["samples_per_malrule"] = samples
    path.write_text(json.dumps(bank, indent=1, ensure_ascii=False), encoding="utf-8")
    return bank


# ---------------------------------------------------------------- likelihood model


PAIR_SEP = "|"


def pair_id(a: str, b: str) -> str:
    x, y = sorted([a, b])
    return f"MIXED{PAIR_SEP}{x}{PAIR_SEP}{y}"


@dataclass
class BankModel:
    category: str
    singles: list[str]
    pairs: list[str]
    items: list[dict]
    eps: float = 0.05
    pair_mass: float = 0.10
    correct_mass: float = 0.025
    other_mass: float = 0.025

    def __post_init__(self):
        self.names = list(self.singles) + list(self.pairs) + ["CORRECT", "OTHER"]
        self.index = {h: i for i, h in enumerate(self.names)}
        self.single_idx = np.array([self.index[h] for h in self.singles], dtype=int)
        self.pair_idx = np.array([self.index[h] for h in self.pairs], dtype=int)
        self.correct_idx = self.index["CORRECT"]
        self.other_idx = self.index["OTHER"]
        self.answer_index: list[dict[str, int]] = []
        self.L: list[np.ndarray] = []
        self._build_likelihoods()
        self.L_stack = np.stack(self.L)

    @property
    def n_hypotheses(self) -> int:
        return len(self.names)

    def effective_pred(self, item_idx: int, h: str) -> str:
        item = self.items[item_idx]
        if not item.get("applicable", {}).get(h, True):
            return item["correct"]
        return item["predictions"].get(h, item["correct"])

    def _build_likelihoods(self) -> None:
        o_max = max(len(item["answers"]) for item in self.items)
        for item in self.items:
            answers = list(item["answers"])
            correct = item["correct"]
            if correct not in answers:
                answers.append(correct)
            answers = sorted(set(answers))
            idx = {a: j for j, a in enumerate(answers)}
            n = len(answers)
            L = np.zeros((self.n_hypotheses, o_max), dtype=float)

            for h in self.singles:
                pred = (
                    item["predictions"].get(h, correct)
                    if item.get("applicable", {}).get(h, True)
                    else correct
                )
                j = idx[pred]
                L[self.index[h], :n] = self.eps / max(1, n - 1)
                L[self.index[h], j] = 1.0 - self.eps
            L[self.correct_idx, :n] = self.eps / max(1, n - 1)
            L[self.correct_idx, idx[correct]] = 1.0 - self.eps
            L[self.other_idx, :n] = 1.0 / n

            for p in self.pairs:
                a, b = p.split(PAIR_SEP)[1:]
                L[self.index[p], :n] = 0.5 * (L[self.index[a], :n] + L[self.index[b], :n])

            self.answer_index.append(idx)
            self.L.append(L)

    def prior(self, weights: dict[str, float]) -> np.ndarray:
        post = np.zeros(self.n_hypotheses, dtype=float)
        w = np.array([max(1e-6, weights.get(h, 0.01)) for h in self.singles], dtype=float)
        w = w / w.sum()
        n_pairs = len(self.pairs)
        if n_pairs:
            pw = []
            for a, b in itertools.combinations(self.singles, 2):
                pw.append(weights.get(a, 0.01) * weights.get(b, 0.01))
            pw = np.array(pw, dtype=float)
            pw = pw / max(1e-12, pw.sum())
            post[self.pair_idx] = self.pair_mass * pw
            single_mass = 1.0 - self.pair_mass - self.correct_mass - self.other_mass
        else:
            single_mass = 1.0 - self.correct_mass - self.other_mass
        post[self.single_idx] = single_mass * w
        post[self.correct_idx] = self.correct_mass
        post[self.other_idx] = self.other_mass
        return post

    def update(self, post: np.ndarray, item_idx: int, outcome: str) -> np.ndarray:
        idx = self.answer_index[item_idx]
        if outcome not in idx:
            return post.copy()
        lik = self.L[item_idx][:, idx[outcome]]
        new = post * lik
        total = new.sum()
        if total <= 0 or not np.isfinite(total):
            return post.copy()
        return new / total

    def predictive(self, post: np.ndarray, item_idx: int) -> np.ndarray:
        dist = post @ self.L[item_idx]
        total = dist.sum()
        return dist / total if total > 0 else dist

    @staticmethod
    def entropy(dist: np.ndarray) -> float:
        p = dist[dist > 1e-12]
        return float(-(p * np.log2(p)).sum())

    def select_maxent(self, post: np.ndarray, available: list[int]) -> int:
        Ls = self.L_stack[available]  # (I,H,O)
        dist = np.einsum("h,iho->io", post, Ls)
        dist = dist / np.maximum(1e-12, dist.sum(axis=1, keepdims=True))
        ent = -(np.where(dist > 1e-12, dist * np.log2(np.maximum(dist, 1e-12)), 0.0)).sum(axis=1)
        return available[int(np.argmax(ent))]

    def select_ig(self, post: np.ndarray, available: list[int]) -> int:
        base_h = self.entropy(post)
        best, best_ig = available[0], -1.0
        for i in available:
            dist = self.predictive(post, i)
            exp_h = 0.0
            for o, p in enumerate(dist):
                if p <= 1e-9:
                    continue
                new = post * self.L[i][:, o]
                total = new.sum()
                if total <= 0:
                    continue
                exp_h += p * self.entropy(new / total)
            ig = base_h - exp_h
            if ig > best_ig:
                best, best_ig = i, ig
        return best

    # ------------------------------------------------------------ student models

    def single_outcome(self, item_idx: int, h: str, rng: random.Random, eps: float | None = None) -> str:
        eps = self.eps if eps is None else eps
        item = self.items[item_idx]
        pred = self.effective_pred(item_idx, h)
        if rng.random() < eps:
            choices = [a for a in item["answers"] if a != pred]
            return rng.choice(choices) if choices else pred
        return pred

    def pair_outcome(self, item_idx: int, pair: str, rng: random.Random, eps: float | None = None) -> str:
        a, b = pair.split(PAIR_SEP)[1:]
        chosen = a if rng.random() < 0.5 else b
        return self.single_outcome(item_idx, chosen, rng, eps)

    def slip_outcome(self, item_idx: int, rng: random.Random, eps: float | None = None) -> str:
        eps = self.eps if eps is None else eps
        item = self.items[item_idx]
        if rng.random() >= eps:
            return item["correct"]
        choices = [a for a in item["answers"] if a != item["correct"]]
        return rng.choice(choices) if choices else item["correct"]

    # ------------------------------------------------------------ diagnostics

    def slip_loglik(self, item_idx: int, outcome: str, eps: float | None = None) -> float:
        eps = self.eps if eps is None else eps
        item = self.items[item_idx]
        n = len(self.answer_index[item_idx])
        if outcome == item["correct"]:
            return math.log(max(1e-12, 1.0 - eps))
        return math.log(max(1e-12, eps / max(1, n - 1)))

    def malrule_loglik(self, item_idx: int, h: str, outcome: str) -> float:
        idx = self.answer_index[item_idx]
        if outcome not in idx:
            return math.log(1e-12)
        return math.log(max(1e-12, float(self.L[item_idx][self.index[h], idx[outcome]])))

    def consistent_wrong(self, item_idx: int, h: str, outcome: str) -> bool:
        item = self.items[item_idx]
        if not item.get("applicable", {}).get(h, True):
            return False
        pred = self.effective_pred(item_idx, h)
        return pred != item["correct"] and pred == outcome

    def top_single(self, post: np.ndarray) -> tuple[str, float]:
        probs = post[self.single_idx]
        j = int(np.argmax(probs))
        return self.singles[j], float(probs[j])

    def top_pair(self, post: np.ndarray) -> tuple[str | None, float]:
        if not self.pairs:
            return None, 0.0
        probs = post[self.pair_idx]
        j = int(np.argmax(probs))
        return self.pairs[j], float(probs[j])

    def mass_on_pairs(self, post: np.ndarray) -> float:
        return float(post[self.pair_idx].sum()) if len(self.pair_idx) else 0.0

    def none_mass(self, post: np.ndarray) -> float:
        return float(post[self.correct_idx] + post[self.other_idx])

    def select_targeted(
        self,
        post: np.ndarray,
        available: list[int],
        candidate_kind: str | None = None,
        candidate_id: str | None = None,
    ) -> int:
        """Prefer items that can actually distinguish the leading diagnosis."""
        pair, pp = self.top_pair(post)
        if (
            pair is not None
            and (candidate_kind == "pair" or (pp >= 0.30 and self.mass_on_pairs(post) >= 0.25))
        ):
            a, b = pair.split(PAIR_SEP)[1:]
            diff = [
                i for i in available
                if self.effective_pred(i, a) != self.effective_pred(i, b)
            ]
            if len(diff) >= 3:
                return self.select_maxent(post, diff)
        target = candidate_id if candidate_kind == "single" and candidate_id else self.top_single(post)[0]
        trig = [
            i for i in available
            if self.effective_pred(i, target) != self.items[i]["correct"]
        ]
        if len(trig) >= 3:
            return self.select_maxent(post, trig)
        return self.select_maxent(post, available)

    def stability_candidate(
        self,
        post: np.ndarray,
        history: list[tuple[int, str]],
        top1_threshold: float = 0.8,
        margin_threshold: float = 0.2,
        pair_ceiling: float = 0.15,
        min_consistent_wrong: int = 2,
        lr_threshold: float = 10.0,
        allow_pairs: bool = True,
        check_pairs: bool = True,
        pair_lr_threshold: float = 2.0,
        single_pair_margin: float = -math.log(1.5),
    ) -> tuple[str, str, float] | None:
        """Return (kind, id, confidence) for a stable single or a mixed pair."""
        single, p1 = self.top_single(post)
        probs = post[self.single_idx]
        order = np.argsort(-probs)
        p2 = float(probs[order[1]]) if len(order) > 1 else 0.0
        single_mass = float(probs.sum())
        p1_cond = p1 / single_mass if single_mass > 1e-9 else 0.0
        p2_cond = p2 / single_mass if single_mass > 1e-9 else 0.0
        pm = self.mass_on_pairs(post)
        none_m = self.none_mass(post)

        consistent = sum(
            1 for i, o in history if self.consistent_wrong(i, single, o)
        )
        ll_m = sum(self.malrule_loglik(i, single, o) for i, o in history)
        ll_s = sum(self.slip_loglik(i, o) for i, o in history)
        lr = math.exp(min(50.0, ll_m - ll_s))

        pair, pp = self.top_pair(post)
        ll_pair = None
        if pair is not None and pp >= 0.05:
            ll_pair = sum(self.malrule_loglik(i, pair, o) for i, o in history)

        single_beats_pair = ll_pair is None or (ll_m - ll_pair) >= single_pair_margin
        pair_beats_single = ll_pair is not None and (ll_pair - ll_m) >= math.log(pair_lr_threshold)

        if (
            p1_cond >= top1_threshold
            and (p1_cond - p2_cond) >= margin_threshold
            and single_mass >= 0.40
            and pm <= pair_ceiling
            and none_m <= 0.15
            and consistent >= min_consistent_wrong
            and lr >= lr_threshold
            and single_beats_pair
        ):
            return ("single", single, p1)

        if allow_pairs and check_pairs and self.pairs:
            singles_sorted = np.sort(probs)[::-1]
            top_single_p = float(singles_sorted[0]) if len(singles_sorted) else 0.0
            ca, cb = self.pair_member_counts(history, pair) if pair is not None else (0, 0)
            wrong_obs = sum(1 for i, o in history if o != self.items[i]["correct"])
            pair_beats_slip = pair is not None and ll_pair is not None and (ll_pair - ll_s) >= math.log(10.0)
            if (
                pair is not None
                and pp >= 0.6
                and pm >= 0.5
                and (pp - top_single_p) >= 0.2
                and len(history) >= 2
                and min(ca, cb) >= 1
                and wrong_obs >= 2
                and pair_beats_single
                and pair_beats_slip
            ):
                return ("pair", pair, pp)
        return None

    def no_misconception_candidate(
        self, post: np.ndarray, history: list[tuple[int, str]], threshold: float = 0.8
    ) -> bool:
        single, _ = self.top_single(post)
        return self.none_mass(post) >= threshold and len(history) >= 2

    def single_pair_margin(self, post: np.ndarray, history: list[tuple[int, str]]) -> float:
        """Log-likelihood advantage of the top single over the top pair."""
        single, _ = self.top_single(post)
        pair, pp = self.top_pair(post)
        if pair is None or pp < 0.05:
            return float("inf")
        ll_s = sum(self.malrule_loglik(i, single, o) for i, o in history)
        ll_p = sum(self.malrule_loglik(i, pair, o) for i, o in history)
        return ll_s - ll_p

    def single_single_margin(self, post: np.ndarray, history: list[tuple[int, str]]) -> float:
        """Log-likelihood advantage of the top single over the runner-up single."""
        probs = post[self.single_idx]
        if len(probs) < 2:
            return float("inf")
        order = np.argsort(-probs)
        h1 = self.singles[int(order[0])]
        h2 = self.singles[int(order[1])]
        ll1 = sum(self.malrule_loglik(i, h1, o) for i, o in history)
        ll2 = sum(self.malrule_loglik(i, h2, o) for i, o in history)
        return ll1 - ll2

    def pair_member_counts(self, history: list[tuple[int, str]], pair: str) -> tuple[int, int]:
        a, b = pair.split(PAIR_SEP)[1:]
        ca = sum(1 for i, o in history if self.effective_pred(i, a) == o)
        cb = sum(1 for i, o in history if self.effective_pred(i, b) == o)
        return ca, cb

    def pair_slip_margin(self, history: list[tuple[int, str]], pair: str) -> float:
        return sum(
            self.malrule_loglik(i, pair, o) - self.slip_loglik(i, o)
            for i, o in history
        )


# ---------------------------------------------------------------- LLM prior


SYSTEM_PROMPT = (
    "You are an expert mathematics education diagnostician. You infer the procedural "
    "misconception that best explains a student's final answer. You distinguish stable "
    "misconceptions from one-off slips and from mixtures of two misconceptions. You never "
    "claim to see work that is not shown. Follow the output schema exactly."
)


def build_library_text(descriptions: list[dict], max_desc_chars: int = 520) -> str:
    lines = []
    for d in descriptions:
        desc = d["description"].replace("\n", " ").strip()
        if len(desc) > max_desc_chars:
            desc = desc[:max_desc_chars].rstrip() + "..."
        lines.append(f"- {d['module']} | {d['human_name']}: {desc}")
    return "\n".join(lines)


def build_prior_prompt(problem: str, answer: str, correct: str, category: str, library: str) -> str:
    return f"""A student solved the problem below and produced the final answer shown.
Their reasoning is not visible.

PROBLEM:
{problem}

CORRECT ANSWER:
{correct}

STUDENT FINAL ANSWER:
{answer}

DOMAIN: {category}

MISCONCEPTION LIBRARY ({library.count(chr(10)) + 1} entries; identifier | name: description):
{library}

Rank the 10 misconceptions from the library that most plausibly explain the student's answer.
Consider the arithmetic relationship between the operands, the correct answer, and the student's answer.
Include every plausible candidate whose predicted error pattern is consistent with the answer, even if
another candidate seems more likely. The problem is from the {category} domain, but do not ignore a
cross-domain candidate if it fits. Also state whether the evidence looks more like one stable
misconception or a mixture of two.
Use only identifiers from the library. Do not solve the problem.
Return strict JSON:
{{"top10": ["id1", "id2", "... up to 10"], "stable_or_mixed": "stable|mixed|slip|unsure", "confidence": 0.0, "reason": "one sentence"}}"""


def call_anthropic(
    api_key: str,
    base_url: str,
    model: str,
    system: str,
    user: str,
    max_tokens: int = 900,
    retries: int = 2,
) -> dict:
    payload = {
        "model": model,
        "system": system,
        "max_tokens": max_tokens,
        "messages": [{"role": "user", "content": user}],
    }
    last = None
    for attempt in range(retries + 1):
        try:
            response = requests.post(
                f"{base_url.rstrip('/')}/v1/messages",
                headers={
                    "Authorization": f"Bearer {api_key}",
                    "anthropic-version": "2023-06-01",
                    "Content-Type": "application/json",
                },
                json=payload,
                timeout=240,
            )
            body = response.text
            try:
                parsed = response.json()
            except Exception:
                parsed = {}
            text = "".join(
                block.get("text", "")
                for block in (parsed.get("content") or [])
                if block.get("type") == "text"
            )
            result = {
                "http_status": response.status_code,
                "text": text,
                "usage": parsed.get("usage") or {},
                "raw": body[:30000],
                "model": parsed.get("model"),
                "stop_reason": parsed.get("stop_reason"),
                "attempt": attempt,
            }
            if response.status_code == 200 and text:
                return result
            last = result
            if response.status_code in (400, 401, 403, 404):
                return result
        except Exception as exc:
            last = {"http_status": -1, "text": "", "usage": {}, "raw": repr(exc), "model": None, "stop_reason": None, "attempt": attempt}
        time.sleep(2 + attempt * 3)
    return last or {"http_status": -1, "text": "", "usage": {}, "raw": "", "model": None, "stop_reason": None, "attempt": retries}


def _match_id(value: str, valid: list[str]) -> str | None:
    value = str(value).strip().strip("\"'").strip()
    if value in valid:
        return value
    hits = [v for v in valid if value and (value == v.split(".")[-1] or v.endswith("." + value))]
    return hits[0] if len(hits) == 1 else None


def parse_prior(text: str, valid_ids: list[str]) -> dict:
    match = re.search(r"\{.*\}", text, re.S)
    if not match:
        return {"top10": [], "stable_or_mixed": None, "confidence": None, "reason": None, "parsed": False}
    try:
        obj = json.loads(match.group(0))
    except Exception:
        return {"top10": [], "stable_or_mixed": None, "confidence": None, "reason": None, "parsed": False}

    raw = obj.get("top10") or obj.get("ranking") or obj.get("top3") or []
    if isinstance(raw, dict):
        raw = [k for k, _ in sorted(raw.items(), key=lambda kv: -float(kv[1]))]
    top10 = []
    for value in raw:
        hid = _match_id(value, valid_ids)
        if hid and hid not in top10:
            top10.append(hid)
    return {
        "top10": top10[:10],
        "stable_or_mixed": obj.get("stable_or_mixed"),
        "confidence": obj.get("confidence"),
        "reason": obj.get("reason"),
        "parsed": bool(top10),
    }


def prior_weights(top10: list[str], singles: list[str], floor: float = 0.01) -> dict[str, float]:
    rank = {h: i + 1 for i, h in enumerate(top10)}
    return {h: (1.0 / rank[h] if h in rank else floor) for h in singles}


def estimated_cost_usd(usage: dict, input_rate: float = 0.28, output_rate: float = 0.42) -> float:
    # Conservative public DeepSeek-style rates; actual proxy billing may differ.
    inp = usage.get("input_tokens") or 0
    out = usage.get("output_tokens") or 0
    return inp / 1e6 * input_rate + out / 1e6 * output_rate


def stable_key(problem: str, answer: str) -> str:
    return hashlib.sha256(f"{problem}\n---\n{answer}".encode("utf-8")).hexdigest()[:20]
