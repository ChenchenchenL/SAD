"""Run E6-lite: OFAT threshold sensitivity for frozen v5 stability_mixed/maxent.

Pipeline:
  1. load frozen inputs (banks, protocol-valid cases, cached LLM priors);
  2. precompute threshold-independent episode trajectories;
  3. self-checks: (a) default thresholds must reproduce the frozen v5
     stability_mixed/maxent episodes exactly on test and dev; (b) the
     prefix/earliest-fire evaluation must match a direct engine-loop run for
     perturbed configs. If any check fails, no result tables are produced;
  4. OFAT sweep on test (eps=.05 primary, eps=0/.10 secondary) and dev;
  5. LOFO fold ranges (descriptive heterogeneity, not selection);
  6. tables + risk-coverage figure + summary/manifest.

No logic here selects or recommends thresholds.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
import time
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE / "src"))

import e6lite as e6  # noqa: E402
import v5_engine as eng  # noqa: E402
from g0_lib import prior_weights  # noqa: E402

CATEGORIES = ["subtraction", "fractions", "decimals", "negative_numbers",
              "order_of_operations", "percentages"]


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def load_priors(path: Path) -> dict:
    out = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        r = json.loads(line)
        if r.get("http_status") == 200 and r.get("top10"):
            out[r["key"]] = r
    return out


def build_models(bank_dir: Path, prefix: str, eps: float):
    models_np, models_p = {}, {}
    for cat in CATEGORIES:
        bank = load_json(bank_dir / f"{prefix}{cat}.json")
        singles = [h["id"] for h in bank["hypotheses"]]
        models_np[cat] = eng.build_model(cat, bank["items"], singles, with_pairs=False, eps=eps)
        models_p[cat] = eng.build_model(cat, bank["items"], singles, with_pairs=True, eps=eps)
    return models_np, models_p


def case_prior(models_np, models_p, case: dict, priors: dict):
    row = priors.get(case.get("key"))
    if row is None:
        return None
    cat = case["category"]
    top10 = row.get("top10") or []
    singles = models_np[cat].singles
    weights = prior_weights(top10, singles) if top10 else {h: 1.0 / len(singles) for h in singles}
    return models_np[cat].prior(weights), models_p[cat].prior(weights)


def precompute_dataset(cases: list[dict], priors: dict, models_np, models_p,
                       seeds: int, eps: float, max_obs: int):
    trajs = []
    skipped: Counter = Counter()
    for case in cases:
        pr = case_prior(models_np, models_p, case, priors)
        if pr is None:
            skipped["missing_prior"] += 1
            continue
        prior_np, prior_p = pr
        for st in e6.STUDENT_TYPES:
            for seed in range(seeds):
                t = e6.precompute_trajectory(models_p[case["category"]], prior_p, case,
                                             st, seed, eps, max_obs)
                if t is None:
                    skipped[st] += 1
                    continue
                trajs.append(t)
    return trajs, dict(skipped)


def traj_key(t: dict):
    return (t["case_id"], t["student_type"], t["seed"])


def compare_to_frozen(trajs: list[dict], frozen_path: Path) -> dict:
    frozen = load_json(frozen_path)
    ref = {(e["case_id"], e["student_type"], e["seed"]): e
           for e in frozen
           if e.get("rule") == "stability_mixed" and e.get("selection") == "maxent"}
    got = {traj_key(t): e6.evaluate_trajectory(t, e6.Thresholds()) for t in trajs}
    common = sorted(set(ref) & set(got))
    mismatches = []
    for k in common:
        a, b = ref[k], got[k]
        fields = ("terminal_kind", "terminal_id", "n_obs", "n_inquiries", "stopped",
                  "budget_exhausted", "correct", "false_remediation")
        bad = [f for f in fields if a[f] != b[f]]
        if not bad and abs(float(a["terminal_p"]) - float(b["terminal_p"])) > 1e-9:
            bad = ["terminal_p"]
        if bad:
            mismatches.append({"key": list(k), "fields": bad,
                               "frozen": {f: a[f] for f in bad},
                               "got": {f: b[f] for f in bad}})
    return {"n_frozen": len(ref), "n_got": len(got), "n_common": len(common),
            "n_mismatch": len(mismatches), "mismatches": mismatches[:20],
            "pass": len(ref) == len(got) == len(common) and not mismatches}


def direct_loop_check(cases: list[dict], priors: dict, models_np, models_p,
                      traj_map: dict, seeds: int, eps: float, max_obs: int,
                      config_ids: list[str]) -> dict:
    out = {}
    for cid in config_ids:
        th = e6.parse_config_id(cid)
        n_cmp = n_mism = 0
        examples = []
        for case in cases:
            pr = case_prior(models_np, models_p, case, priors)
            if pr is None:
                continue
            _, prior_p = pr
            model = models_p[case["category"]]
            for st in e6.STUDENT_TYPES:
                for seed in range(seeds):
                    slow = e6.run_episode_th(model, prior_p, case, st, th, seed, eps, max_obs)
                    t = traj_map.get((case["case_id"], st, seed))
                    if slow is None or t is None:
                        if (slow is None) != (t is None):
                            n_mism += 1
                            examples.append({"case_id": case["case_id"], "st": st,
                                             "seed": seed, "fields": ["eligibility"],
                                             "slow": None, "fast": None})
                        else:
                            n_cmp += 1
                        continue
                    fast = e6.evaluate_trajectory(t, th, max_obs)
                    n_cmp += 1
                    fields = ("terminal_kind", "terminal_id", "n_obs", "stopped",
                              "budget_exhausted", "correct", "false_remediation")
                    bad = [f for f in fields if slow[f] != fast[f]]
                    if bad:
                        n_mism += 1
                        if len(examples) < 5:
                            examples.append({"case_id": case["case_id"], "st": st,
                                             "seed": seed, "fields": bad,
                                             "slow": {f: slow[f] for f in bad},
                                             "fast": {f: fast[f] for f in bad}})
        out[cid] = {"n_compared": n_cmp, "n_mismatch": n_mism,
                    "pass": n_mism == 0, "examples": examples}
    return out


def run_sweep(trajs: list[dict], family_of_case: dict[str, str], cfg: dict,
              with_lofo: bool) -> dict:
    cb = e6.ClusterBoot(family_of_case, n_boot=cfg["bootstrap"], seed=cfg["bootstrap_seed"])
    by_type: dict[str, list[dict]] = {st: [] for st in e6.STUDENT_TYPES}
    for t in trajs:
        by_type[t["student_type"]].append(t)
    out = {}
    for th in e6.grid_configs():
        eps_by_type = {st: [e6.evaluate_trajectory(t, th, cfg["max_obs"]) for t in rows]
                       for st, rows in by_type.items()}
        entry = {"thresholds": {k: getattr(th, k) for k in e6.GRID_ORDER},
                 "summary": e6.summarize_config(eps_by_type, cb)}
        if with_lofo:
            entry["lofo"] = e6.lofo_ranges(eps_by_type, cb)
        out[th.config_id] = entry
    return out


def deviation_summary(sweep: dict) -> dict:
    """Max |mean(config) - mean(default)| per factor over that factor's grid."""
    default = sweep["default"]["summary"]
    out = {}
    for k in e6.GRID_ORDER:
        configs = [cid for cid in sweep
                   if cid != "default" and cid.split("=")[0] == k]
        if not configs:
            continue
        fac = {}
        for st in e6.STUDENT_TYPES:
            for metric in e6.METRICS:
                base = default[st][metric]["mean"]
                vals = [sweep[cid]["summary"][st][metric]["mean"] for cid in configs]
                fac[f"{st}/{metric}"] = {
                    "default": base,
                    "min": min(vals),
                    "max": max(vals),
                    "max_abs_dev": max(abs(v - base) for v in vals),
                }
        out[k] = fac
    return out


def fmt(x, d=3) -> str:
    if x is None or (isinstance(x, float) and not np.isfinite(x)):
        return "—"
    return f"{x:.{d}f}"


def ci_str(c: dict) -> str:
    return f"{c['mean']:.3f} [{c['ci_low']:.3f}, {c['ci_high']:.3f}]"


def build_tables(sweep: dict, cfg: dict, dataset_label: str, with_lofo: bool) -> str:
    lines = [f"# E6-lite OFAT sweep — {dataset_label}", ""]
    lines.append("Sensitivity analysis only: no threshold is selected here. "
                 "Default = frozen v5 pre-registered values "
                 "(u1=.80, margin=.20, S=.40, P=.20, N=.15, E=2, LR=10, pair_guard=1.5). "
                 "Family-cluster means with 95% bootstrap CI.")
    lines.append("")
    default = sweep["default"]["summary"]
    for k in e6.GRID_ORDER:
        d = e6.DEFAULTS[k]
        lines.append(f"## {k} (default {d})")
        lines.append("")
        lines.append("| value | slip false | slip none | slip abstain | slip inq | stable correct | stable correct-stop | stable inq | mixed false | mixed commit | slip J5 |")
        lines.append("|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|")
        rows = [(str(v), sweep[_cfg_id_for(k, v)])
                for v in e6.GRIDS[k] if _cfg_id_for(k, v) in sweep]
        seen = set()
        for label, entry in rows:
            if label in seen:
                continue
            seen.add(label)
            s = entry["summary"]
            mark = " **(frozen)**" if entry is sweep["default"] else ""
            lines.append("| {label}{mark} | {sf} | {sn} | {sa} | {si} | {sc} | {scs} | {sci} | {mf} | {md} | {sj} |".format(
                label=label, mark=mark,
                sf=ci_str(s["slip"]["false"]), sn=fmt(s["slip"]["none"]["mean"]),
                sa=fmt(s["slip"]["abstain"]["mean"]), si=fmt(s["slip"]["n_inquiries"]["mean"], 2),
                sc=ci_str(s["stable"]["correct"]), scs=fmt(s["stable"]["correct_stop"]["mean"]),
                sci=fmt(s["stable"]["n_inquiries"]["mean"], 2),
                mf=fmt(s["mixed"]["false"]["mean"]), md=fmt(s["mixed"]["diagnosed"]["mean"]),
                sj=fmt(s["slip"]["J5"]["mean"], 2)))
        lines.append("")
    if with_lofo:
        lines.append("## LOFO fold ranges at the frozen default (descriptive only)")
        lines.append("")
        lines.append("| student type | metric | fold min | fold max | fold range | n folds |")
        lines.append("|---|---|---:|---:|---:|---:|")
        lofo = sweep["default"]["lofo"]
        for st in e6.STUDENT_TYPES:
            for metric, v in lofo.get(st, {}).items():
                lines.append(f"| {st} | {metric} | {fmt(v['min'])} | {fmt(v['max'])} | {fmt(v['range'])} | {v['n_folds']} |")
        lines.append("")
    return "\n".join(lines)


def _cfg_id_for(factor: str, value) -> str:
    if value == e6.DEFAULTS[factor]:
        return "default"
    return f"{factor}={'off' if value is None else value}"


def build_figure(sweep: dict, out_png: Path, out_pdf: Path) -> None:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    factors = [k for k in e6.GRID_ORDER]
    colors = plt.get_cmap("tab10")
    fig, axes = plt.subplots(2, 2, figsize=(11.5, 9.0))

    ax = axes[0][0]
    for fi, k in enumerate(factors):
        xs, ys = [], []
        for v in e6.GRIDS[k]:
            entry = sweep.get(_cfg_id_for(k, v))
            if entry is None:
                continue
            s = entry["summary"]
            xs.append(s["stable"]["correct"]["mean"])
            ys.append(s["slip"]["false"]["mean"])
        if xs:
            ax.plot(xs, ys, "-o", ms=4, lw=1.2, color=colors(fi), label=k, alpha=0.85)
    d = sweep["default"]["summary"]
    ax.scatter([d["stable"]["correct"]["mean"]], [d["slip"]["false"]["mean"]],
               marker="*", s=260, color="black", zorder=5, label="frozen default")
    ax.set_xlabel("stable correct (family-cluster mean)")
    ax.set_ylabel("slip false remediation")
    ax.set_title("Risk-coverage: each line = one threshold factor's grid")
    ax.legend(fontsize=8, loc="best")

    panels = [(axes[0][1], "slip", "false", "slip false remediation"),
              (axes[1][0], "stable", "correct", "stable correct"),
              (axes[1][1], "slip", "n_inquiries", "slip additional inquiries")]
    for ax, st, metric, title in panels:
        for fi, k in enumerate(factors):
            xs, ys = [], []
            for gi, v in enumerate(e6.GRIDS[k]):
                entry = sweep.get(_cfg_id_for(k, v))
                if entry is None:
                    continue
                xs.append(gi)
                ys.append(entry["summary"][st][metric]["mean"])
            if xs:
                ax.plot(xs, ys, "-o", ms=4, lw=1.2, color=colors(fi), label=k, alpha=0.85)
        ax.set_xlabel("grid position (low -> high within factor)")
        ax.set_ylabel(title)
        ax.set_title(title)
        ax.legend(fontsize=8, loc="best")
    fig.suptitle("E6-lite threshold sensitivity (frozen v5 stability_mixed/maxent, protocol-valid test set)", fontsize=12)
    fig.tight_layout(rect=(0, 0, 1, 0.97))
    fig.savefig(out_png, dpi=200)
    fig.savefig(out_pdf)
    plt.close(fig)


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    h.update(path.read_bytes())
    return h.hexdigest()


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", default=str(HERE / "config.json"))
    ap.add_argument("--run-name", default="e6lite")
    args = ap.parse_args()
    cfg = load_json(Path(args.config))
    ts = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    run_dir = HERE / "runs" / f"{ts}_{args.run_name}"
    out_dir = run_dir / "outputs"
    out_dir.mkdir(parents=True, exist_ok=True)

    t_start = time.time()
    cfg_path = Path(args.config)
    input_files = {
        "config": cfg_path,
        "banks": [Path(cfg["bank_dir"]) / f"{cfg['bank_prefix']}{c}.json" for c in CATEGORIES],
        "test_cases": Path(cfg["test_cases"]),
        "test_priors": Path(cfg["test_priors"]),
        "dev_cases": Path(cfg["dev_cases"]),
        "dev_priors": Path(cfg["dev_priors"]),
        "frozen_test_episodes": Path(cfg["frozen_test_episodes"]),
        "frozen_dev_episodes": Path(cfg["frozen_dev_episodes"]),
    }
    manifest = {"generated_at": ts, "sha256": {}}
    for name, p in input_files.items():
        files = p if isinstance(p, list) else [p]
        for f in files:
            manifest["sha256"][f"{name}:{f.name}"] = sha256(f)
    for code in sorted((HERE / "src").glob("*.py")) + [Path(__file__)]:
        manifest["sha256"][f"code:{code.name}"] = sha256(code)
    (run_dir / "manifest.json").write_text(json.dumps(manifest, indent=1), encoding="utf-8")
    (run_dir / "config.snapshot.json").write_text(json.dumps(cfg, indent=1), encoding="utf-8")

    test_cases = load_json(HERE / cfg["test_cases"])
    dev_cases = load_json(HERE / cfg["dev_cases"])
    test_priors = load_priors(HERE / cfg["test_priors"])
    dev_priors = load_priors(HERE / cfg["dev_priors"])

    datasets = {}
    # primary test (eps .05, 5 seeds)
    models_np, models_p = build_models(HERE / cfg["bank_dir"], cfg["bank_prefix"], cfg["eps_primary"])
    trajs, skipped = precompute_dataset(test_cases, test_priors, models_np, models_p,
                                        cfg["test_seeds"], cfg["eps_primary"], cfg["max_obs"])
    datasets["test_eps0.05"] = {"trajs": trajs, "skipped": skipped,
                                "models": (models_np, models_p), "seeds": cfg["test_seeds"],
                                "eps": cfg["eps_primary"], "cases": test_cases, "priors": test_priors}
    # dev (eps .05, 3 seeds, matching the frozen dev run)
    trajs_dev, skipped_dev = precompute_dataset(dev_cases, dev_priors, models_np, models_p,
                                                cfg["dev_seeds"], cfg["eps_primary"], cfg["max_obs"])
    datasets["dev_eps0.05"] = {"trajs": trajs_dev, "skipped": skipped_dev,
                               "models": (models_np, models_p), "seeds": cfg["dev_seeds"],
                               "eps": cfg["eps_primary"], "cases": dev_cases, "priors": dev_priors}
    # secondary test noise levels
    for eps in cfg["eps_secondary"]:
        m_np, m_p = build_models(HERE / cfg["bank_dir"], cfg["bank_prefix"], eps)
        trajs_e, skipped_e = precompute_dataset(test_cases, test_priors, m_np, m_p,
                                                cfg["test_seeds"], eps, cfg["max_obs"])
        datasets[f"test_eps{eps:.2f}"] = {"trajs": trajs_e, "skipped": skipped_e,
                                          "models": (m_np, m_p), "seeds": cfg["test_seeds"],
                                          "eps": eps, "cases": test_cases, "priors": test_priors}

    traj_map = {traj_key(t): t for t in datasets["test_eps0.05"]["trajs"]}
    m_np, m_p = datasets["test_eps0.05"]["models"]
    checks = {
        "frozen_test_episodes_default_config": compare_to_frozen(
            datasets["test_eps0.05"]["trajs"], HERE / cfg["frozen_test_episodes"]),
        "frozen_dev_episodes_default_config": compare_to_frozen(
            datasets["dev_eps0.05"]["trajs"], HERE / cfg["frozen_dev_episodes"]),
        "direct_loop_vs_prefix": direct_loop_check(
            test_cases, test_priors, m_np, m_p, traj_map,
            cfg["test_seeds"], cfg["eps_primary"], cfg["max_obs"], cfg["direct_check_configs"]),
    }
    all_ok = (checks["frozen_test_episodes_default_config"]["pass"]
              and checks["frozen_dev_episodes_default_config"]["pass"]
              and all(v["pass"] for v in checks["direct_loop_vs_prefix"].values()))

    status = {
        "run": str(run_dir), "timestamp": ts, "checks_pass": all_ok,
        "checks": checks, "elapsed_s": round(time.time() - t_start, 1),
    }
    if not all_ok:
        (out_dir / "status.json").write_text(json.dumps(status, indent=1), encoding="utf-8")
        print("SELF-CHECK FAILED - no result tables produced.", json.dumps(status)[:2000])
        sys.exit(1)

    sweep = {}
    data_info = {}
    for ds_name, ds in datasets.items():
        family_of_case = {t["case_id"]: t["family"] for t in ds["trajs"]}
        with_lofo = ds_name.startswith("test")
        sweep[ds_name] = run_sweep(ds["trajs"], family_of_case, cfg, with_lofo)
        data_info[ds_name] = {
            "n_cases": len({t["case_id"] for t in ds["trajs"]}),
            "n_families": len(set(family_of_case.values())),
            "n_trajectories": len(ds["trajs"]),
            "n_seeds": ds["seeds"],
            "eps": ds["eps"],
            "skipped": ds["skipped"],
        }
        print(f"swept {ds_name}: {data_info[ds_name]}")

    deviations = {ds: deviation_summary(sweep[ds]) for ds in sweep}

    # default-config episodes for audit
    default_episodes = [e6.evaluate_trajectory(t, e6.Thresholds(), cfg["max_obs"])
                        for t in datasets["test_eps0.05"]["trajs"]]
    (out_dir / "episodes_default_test.json").write_text(
        json.dumps(default_episodes, ensure_ascii=False), encoding="utf-8")

    tables = [build_tables(sweep["test_eps0.05"], cfg, "test eps=0.05 (primary)", with_lofo=True), ""]
    tables += [build_tables(sweep["dev_eps0.05"], cfg, "dev eps=0.05 (20 cases, 11 families - power limited)", with_lofo=False), ""]
    for eps in cfg["eps_secondary"]:
        tables += [build_tables(sweep[f"test_eps{eps:.2f}"], cfg, f"test eps={eps:.2f} (secondary)", with_lofo=False), ""]
    (out_dir / "tables.md").write_text("\n".join(tables), encoding="utf-8")

    build_figure(sweep["test_eps0.05"], out_dir / "risk_coverage.png", out_dir / "risk_coverage.pdf")

    summary = {
        "experiment": "e6lite_threshold_sensitivity",
        "timestamp": ts,
        "protocol": {
            "purpose": "one-factor-at-a-time threshold sensitivity of the frozen v5 stability_mixed/maxent rule",
            "threshold_selection_from_test": False,
            "threshold_selection_from_dev": False,
            "claim_allowed": "threshold insensitivity / stable plateau only; NOT a risk certification",
            "swept": e6.DEFAULTS,
            "grids": e6.GRIDS,
            "fixed_internal_constants": e6.FIXED,
        },
        "data": data_info,
        "checks": checks,
        "sweep": sweep,
        "deviations": deviations,
    }
    (out_dir / "summary.json").write_text(json.dumps(summary, indent=1, ensure_ascii=False), encoding="utf-8")
    status["outputs"] = sorted(p.name for p in out_dir.iterdir())
    (out_dir / "status.json").write_text(json.dumps(status, indent=1), encoding="utf-8")
    print(f"DONE in {round(time.time() - t_start, 1)}s -> {out_dir}")


if __name__ == "__main__":
    main()
