#!/usr/bin/env python3
"""G0 feasibility check for active malrule diagnosis on MalRuleLib.

Usage:
  python g0_active_diagnosis.py --repo ./data/external/malrulelib_repo --category subtraction

Writes a JSON summary next to this script (or to --out).
No LLM, no GPU; all diagnosis is symbolic.
"""
import argparse
import importlib
import inspect
import json
import math
import random
import sys
from collections import Counter
from pathlib import Path


def load_classes(module_name):
    module = importlib.import_module(module_name)
    generators, malrules, corrects = [], [], []
    for name, obj in vars(module).items():
        if not (inspect.isclass(obj) and obj.__module__.startswith(module_name)):
            continue
        if issubclass(obj, ProblemGenerator) and not inspect.isabstract(obj):
            generators.append(obj)
        if issubclass(obj, Malrule) and not inspect.isabstract(obj):
            malrules.append(obj)
        if issubclass(obj, CorrectAlgorithm) and not inspect.isabstract(obj):
            corrects.append(obj)
    return (generators[0] if generators else None,
            malrules[0] if malrules else None,
            corrects[0] if corrects else None)


def instantiate(cls, level=5):
    for args in [(), (level,), (level, DifficultyLevel.MEDIUM)]:
        try:
            return cls(*args)
        except Exception:
            continue
    return None


def normalize(answer):
    text = str(answer).strip().replace(",", "")
    try:
        value = float(text)
        return str(int(value)) if value == int(value) else str(round(value, 6))
    except Exception:
        return text.lower()


def build_bank(repo, category, samples_per_malrule=30, level=5):
    rows = []
    cat_dir = Path(repo) / "malrules" / category
    for md in sorted(cat_dir.iterdir()):
        if not (md.is_dir() and (md / "__init__.py").exists()):
            continue
        generator_cls, malrule_cls, correct_cls = load_classes(f"malrules.{category}.{md.name}")
        if generator_cls and malrule_cls:
            rows.append((md.name, generator_cls, malrule_cls, correct_cls))

    hypotheses = []
    for name, _, malrule_cls, _ in rows:
        instance = instantiate(malrule_cls, level)
        if instance is not None:
            hypotheses.append((name, instance))

    items, seen = [], set()
    for name, generator_cls, _, correct_cls in rows:
        generator = instantiate(generator_cls, level)
        correct_algo = instantiate(correct_cls, level) if correct_cls else None
        if generator is None:
            continue
        generated = 0
        for seed in range(samples_per_malrule * 20):
            if generated >= samples_per_malrule:
                break
            try:
                problem = generator.generate(seed=5000 + seed)
            except Exception:
                continue
            key = problem.text.strip()
            if key in seen:
                continue
            seen.add(key)
            predictions = {}
            for hyp_name, hyp in hypotheses:
                try:
                    predictions[hyp_name] = normalize(hyp.calculate_expected_answer(problem))
                except Exception:
                    pass
            correct = None
            if correct_algo is not None:
                try:
                    correct = normalize(correct_algo.solve(problem).answer)
                except Exception:
                    pass
            if correct is None or len(predictions) < 2:
                continue
            answers = sorted(set(list(predictions.values()) + [correct]))
            items.append({
                "text": problem.text,
                "source_malrule": name,
                "predictions": predictions,
                "correct": correct,
                "answers": answers,
                "triggers": {h: predictions[h] != correct for h in predictions},
            })
            generated += 1
    return hypotheses, items


def likelihood(item, hypothesis, outcome, eps):
    if hypothesis == "OTHER":
        return 1.0 / max(1, len(item["answers"]))
    if hypothesis == "CORRECT" or hypothesis not in item["predictions"]:
        # A malrule that does not apply to this item is assumed to fall back
        # to the correct procedure; this matches how the simulated student
        # answers non-triggering items and keeps the likelihood consistent.
        predicted = item["correct"]
    else:
        predicted = item["predictions"][hypothesis]
    if predicted == outcome:
        return 1.0 - eps
    return eps / max(1, len(item["answers"]) - 1)


def update(posterior, item, outcome, eps):
    updated = {h: posterior[h] * likelihood(item, h, outcome, eps) for h in posterior}
    total = sum(updated.values())
    if total <= 0:
        return posterior
    return {h: v / total for h, v in updated.items()}


def entropy(posterior):
    return -sum(v * math.log(v + 1e-12, 2) for v in posterior.values() if v > 0)


def expected_information_gain(posterior, item, eps):
    outcomes = item["answers"]
    probs = {o: 0.0 for o in outcomes}
    for h, p in posterior.items():
        for o in outcomes:
            probs[o] += p * likelihood(item, h, o, eps)
    total = sum(probs.values())
    probs = {o: v / total for o, v in probs.items() if v > 0}
    expected_entropy = sum(
        p * entropy(update(posterior, item, o, eps)) for o, p in probs.items()
    )
    return entropy(posterior) - expected_entropy


def predictive_entropy(posterior, item, eps):
    probs = {o: 0.0 for o in item["answers"]}
    for h, p in posterior.items():
        for o in item["answers"]:
            probs[o] += p * likelihood(item, h, o, eps)
    total = sum(probs.values())
    probs = {o: v / total for o, v in probs.items() if v > 0}
    return entropy(probs)


def simulate(hypotheses, items, policy, k, eps, trials, seed):
    random.seed(seed)
    hyp_names = [h for h, _ in hypotheses] + ["CORRECT", "OTHER"]
    acc, ent, detected = [], [], []
    for true_name, _ in hypotheses:
        triggering = [i for i, it in enumerate(items) if it["triggers"].get(true_name, False)]
        if not triggering:
            continue
        for _ in range(trials):
            posterior = {h: 1.0 / len(hyp_names) for h in hyp_names}
            first = random.choice(triggering)
            item = items[first]
            outcome = item["predictions"][true_name]
            if random.random() < eps:
                alternatives = [a for a in item["answers"] if a != outcome]
                outcome = random.choice(alternatives or item["answers"])
            posterior = update(posterior, item, outcome, eps)
            available = [i for i in range(len(items)) if i != first]
            for _ in range(k):
                if policy == "random":
                    idx = random.choice(available)
                elif policy == "fixed":
                    idx = available[0]
                elif policy == "maxent":
                    idx = max(available, key=lambda j: predictive_entropy(posterior, items[j], eps))
                elif policy == "ig":
                    idx = max(available, key=lambda j: expected_information_gain(posterior, items[j], eps))
                else:
                    raise ValueError(policy)
                item = items[idx]
                available.remove(idx)
                outcome = item["predictions"].get(true_name, item["correct"])
                if random.random() < eps:
                    alternatives = [a for a in item["answers"] if a != outcome]
                    outcome = random.choice(alternatives or item["answers"])
                posterior = update(posterior, item, outcome, eps)
            best = max(posterior, key=posterior.get)
            acc.append(best == true_name)
            ent.append(entropy(posterior))
            detected.append(best in ("CORRECT", "OTHER"))
    n = len(acc)
    return {
        "top1": sum(acc) / n if n else None,
        "entropy": sum(ent) / n if n else None,
        "correct_or_other_rate": sum(detected) / n if n else None,
        "n": n,
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", required=True, help="Path to the malrulelib repository")
    parser.add_argument("--category", default="subtraction")
    parser.add_argument("--samples", type=int, default=30, help="unique problems per malrule")
    parser.add_argument("--trials", type=int, default=40)
    parser.add_argument("--eps", type=float, default=0.05)
    parser.add_argument("--seed", type=int, default=0)
    parser.add_argument("--out", default=None)
    args = parser.parse_args()

    sys.path.insert(0, str(Path(args.repo).resolve()))
    import utils
    for name in ["ProblemGenerator", "Malrule", "CorrectAlgorithm", "DifficultyLevel"]:
        globals()[name] = getattr(utils, name)
    hypotheses, items = build_bank(args.repo, args.category, args.samples)
    summary = {
        "category": args.category,
        "n_hypotheses": len(hypotheses),
        "hypotheses": [h for h, _ in hypotheses],
        "n_items": len(items),
        "applicability": dict(sorted(Counter(len(it["predictions"]) for it in items).items())),
        "distinct_answers": dict(sorted(Counter(len(it["answers"]) for it in items).items())),
        "triggering_items": {h: sum(1 for it in items if it["triggers"].get(h, False)) for h, _ in hypotheses},
        "policies": {},
        "settings": {"samples": args.samples, "trials": args.trials, "eps": args.eps, "seed": args.seed},
    }
    for policy in ["random", "fixed", "maxent", "ig"]:
        summary["policies"][policy] = {}
        for k in [1, 2, 3, 4, 5]:
            summary["policies"][policy][k] = simulate(
                hypotheses, items, policy, k, args.eps, args.trials, args.seed
            )

    output = Path(args.out) if args.out else Path(__file__).with_name(f"g0_{args.category}.json")
    output.write_text(json.dumps(summary, indent=2, ensure_ascii=False), encoding="utf-8")
    print(json.dumps({k: summary[k] for k in ["category", "n_hypotheses", "n_items", "applicability", "distinct_answers"]}, ensure_ascii=False))
    for policy, results in summary["policies"].items():
        line = ", ".join(f"k={k}: top1={v['top1']:.3f} H={v['entropy']:.3f}" for k, v in results.items())
        print(f"{policy}: {line}")
    print(f"wrote {output}")


if __name__ == "__main__":
    main()
