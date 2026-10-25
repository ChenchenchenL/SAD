"""Extract the three added experiments without altering their saved outputs."""
from collections import Counter, defaultdict
from pathlib import Path
import csv
import hashlib
import json
import math
import numpy as np

ROOT = Path(__file__).resolve().parents[3]
DATA = ROOT / 'results/figures/data'
RUNS = {
    'e1': ROOT / 'experiments/2026-10-21_budget_ablation/runs/20261021T115028Z_budget_ablation_e1',
    'e6': ROOT / 'experiments/2026-10-21_threshold_sensitivity/runs/20261021T120556Z_e6lite',
    'ool': ROOT / 'experiments/2026-10-21_lomo_out_of_library/runs/20261021T120231Z_lomo_eps005',
}


def load(path):
    return json.loads(path.read_text(encoding='utf-8'))


def csv_out(name, rows):
    path = DATA / name
    with path.open('w', encoding='utf-8', newline='') as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def cell_cols(prefix, cell, scale=1):
    return {prefix + suffix: cell[key] * scale for suffix, key in
            (('_mean', 'mean'), ('_ci_low', 'ci_low'), ('_ci_high', 'ci_high'))}


def assert_close(a, b):
    assert math.isclose(a, b, abs_tol=1e-12), (a, b)


def paired_bootstrap(first, second, field, seed=20261026):
    """Independently recompute family-cluster CIs from paired saved records."""
    a = {(r['case_id'], r['seed']): r for r in first}
    b = {(r['case_id'], r['seed']): r for r in second}
    assert a.keys() == b.keys()
    by_case = defaultdict(list)
    family = {}
    for key, row in a.items():
        by_case[key[0]].append(float(row[field]) - float(b[key][field]))
        family[key[0]] = row['family']
    families = sorted(set(family.values()))
    sums = np.array([sum(np.mean(v) for cid, v in by_case.items() if family[cid] == f) for f in families])
    counts = np.array([sum(family[cid] == f for cid in by_case) for f in families])
    draws = np.random.default_rng(seed).integers(0, len(families), (2000, len(families)))
    multiplicities = np.array([np.bincount(d, minlength=len(families)) for d in draws])
    reps = (multiplicities @ sums) / (multiplicities @ counts)
    low, high = np.percentile(reps, [2.5, 97.5])
    return dict(mean=float(sums.sum()/counts.sum()), ci_low=float(low), ci_high=float(high))


def main():
    summaries = {k: load(run / 'outputs/summary.json') for k, run in RUNS.items()}
    e1, e6, ool = (summaries[k] for k in ('e1', 'e6', 'ool'))
    # Identical default-SM observations use one bootstrap across all displays.
    original_path = ROOT / 'experiments/2026-10-20_llm_v4_v5/v5/out/test_category_eps05_corrected_episodes.json'
    primary_path = ROOT / 'experiments/2026-10-20_llm_v4_v5/v5/out/final_audit/diagnosis_audit.json'
    original = [e for e in load(original_path)
                if e['rule'] == 'stability_mixed' and e['selection'] == 'maxent']
    primary = load(primary_path)['table']['stability_mixed_maxent']
    key = lambda e: (e['case_id'], e['student_type'], e['seed'])
    original_by_key = {key(e): e for e in original}
    compared = {}
    for label, records in [('E1', [e for e in load(RUNS['e1'] / 'outputs/episodes.json') if e['arm'] == 'sm_b6']),
                           ('E6', load(RUNS['e6'] / 'outputs/episodes_default_test.json'))]:
        assert set(map(key, records)) == set(original_by_key)
        for e in records:
            for field in ('terminal_kind','terminal_id','n_obs','stopped','correct','false_remediation'):
                assert e[field] == original_by_key[key(e)][field], (label,key(e),field)
        compared[label] = len(records)
    recomputed = {}
    for st, metric, field in [('slip','false','false_remediation'),('stable','correct','correct'),
                              ('stable','correct_stop','correct_stop'),('stable','n_inquiries','n_inquiries'),
                              ('slip','n_inquiries','n_inquiries')]:
        group = [dict(e, correct_stop=int(e['correct'] and e['stopped'])) for e in original if e['student_type']==st]
        zeros = [dict(e, **{field:0}) for e in group]
        computed = paired_bootstrap(group, zeros, field, seed=20261026)
        for name in ('mean','ci_low','ci_high'):
            assert_close(computed[name], primary[st][metric][name])
        recomputed[st+'/'+metric] = computed
    harmonization = dict(bootstrap_seed=20261026, n_resamples=2000, unit='36 template families',
                         default_episode_matches=compared, recomputed=recomputed,
                         scope='Only default-SM marginal CIs in the E6 display are harmonized; raw outputs and paired contrasts remain unchanged.',
                         sources={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest()
                                  for p in (original_path, primary_path, RUNS['e6'] / 'outputs/summary.json')})
    (ROOT/'docs/default_sm_ci_harmonization_2026-10-22.json').write_text(
        json.dumps(harmonization,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    arms = [('A', 'fixed_k3'), ('B', 'fixed_k3_gate'), ("C'", 'sm_b3'), ('C', 'sm_b6')]
    rows = []
    for label, arm in arms:
        rec = e1['aggregates'][arm]
        row = dict(arm_label=label, arm=arm, cap=6 if arm == 'sm_b6' else 3)
        for st, metric in [('slip', 'false'), ('stable', 'correct'), ('stable', 'n_inquiries'),
                           ('slip', 'n_inquiries'), ('stable', 'none'), ('slip', 'none'),
                           ('stable', 'abstain'), ('slip', 'abstain')]:
            row.update(cell_cols(f'{st}_{metric}', rec[st][metric], 1 if metric == 'n_inquiries' else 100))
        rows.append(row)
    csv_out('e1_four_arms.csv', rows)
    contrasts = []
    for contrast, rec in e1['e1_contrasts'].items():
        for st, metric in [('slip', 'false'), ('stable', 'correct'), ('stable', 'n_inquiries'), ('slip', 'n_inquiries')]:
            contrasts.append(dict(contrast=contrast, student_type=st, metric=metric,
                                  **cell_cols('difference', rec[st][metric], 1 if metric == 'n_inquiries' else 100)))
    for st, metric in [('slip', 'false'), ('stable', 'correct'), ('stable', 'n_inquiries'), ('slip', 'n_inquiries')]:
        c = e1['cap_contrasts']['sm_b3 - sm_b6'][st][metric]
        inv = dict(mean=-c['mean'], ci_low=-c['ci_high'], ci_high=-c['ci_low'])
        contrasts.append(dict(contrast='sm_b6 - sm_b3', student_type=st, metric=metric,
                              **cell_cols('difference', inv, 1 if metric == 'n_inquiries' else 100)))
    csv_out('e1_component_contrasts.csv', contrasts)

    sweep = e6['sweep']['test_eps0.05']
    default = sweep['default']['summary']
    factor_rows, range_rows = [], []
    for factor, values in e6['protocol']['grids'].items():
        subset = []
        for value in values:
            if value == e6['protocol']['swept'][factor]:
                config = 'default'
            else:
                config = next(k for k, r in sweep.items()
                              if k.startswith(factor + '=') and
                              (r['thresholds'][factor] == value or
                               (value == 'off' and r['thresholds'][factor] is None)))
            rec = sweep[config]['summary']
            row = dict(factor=factor, value=value, config=config)
            for st, metric in [('slip', 'false'), ('stable', 'correct'), ('stable', 'correct_stop'),
                               ('stable', 'n_inquiries'), ('slip', 'n_inquiries')]:
                scale = 1 if metric == 'n_inquiries' else 100
                prefix = f'{st}_{metric}'
                cell = primary[st][metric] if config == 'default' else rec[st][metric]
                assert_close(cell['mean'], rec[st][metric]['mean'])
                row.update(cell_cols(prefix, cell, scale))
                row[prefix + '_delta'] = (rec[st][metric]['mean'] - default[st][metric]['mean']) * scale
            subset.append(row)
        factor_rows.extend(subset)
        row = dict(factor=factor)
        for metric in ('slip_false', 'stable_correct', 'stable_n_inquiries'):
            deltas = [r[metric + '_delta'] for r in subset]
            row.update({metric + '_delta_min': min(deltas), metric + '_delta_max': max(deltas)})
        range_rows.append(row)
    csv_out('e6_threshold_sweep.csv', factor_rows)
    csv_out('e6_threshold_ranges.csv', range_rows)

    table = []
    for st in ('stable_ool', 'slip_ool'):
        for arm in ('posterior_only', 'posterior_plus_E', 'stability_mixed_reference'):
            rec = ool['aggregates'][arm][st]
            row = dict(student_type=st, arm=arm)
            row.update(cell_cols('false_commit', rec['false_commit'], 100))
            row.update(none=rec['none']['mean'] * 100, abstain=rec['abstain']['mean'] * 100,
                       n_inquiries=rec['n_inquiries']['mean'])
            table.append(row)
    csv_out('ool_false_commit.csv', table)

    # Recompute primary point estimates and event counts from saved episodes.
    checks = []
    for kind in ('e1', 'ool'):
        episodes = load(RUNS[kind] / 'outputs/episodes.json')
        groups = defaultdict(list)
        for episode in episodes:
            groups[episode['arm'], episode['student_type']].append(episode)
        for (arm, st), group in groups.items():
            assert len(group) == 435 and len({e['case_id'] for e in group}) == 87
            assert len({(e['case_id'], e['seed']) for e in group}) == 435
            for metric, field in ([('correct', 'correct'), ('false', 'false_remediation')]
                                  if kind == 'e1' else [('false_commit', 'false_commit')]):
                assert_close(sum(float(e[field]) for e in group) / len(group), summaries[kind]['aggregates'][arm][st][metric]['mean'])
            assert_close(sum(e['n_inquiries'] for e in group) / len(group), summaries[kind]['aggregates'][arm][st]['n_inquiries']['mean'])
        checks.append(f'{kind}: primary means and 435 paired observations per arm/type verified')
        if kind == 'e1':
            for contrast, saved in e1['e1_contrasts'].items():
                first, second = contrast.split(' - ')
                for st, metric, field in [('slip','false','false_remediation'), ('stable','correct','correct')]:
                    computed = paired_bootstrap(groups[first,st], groups[second,st], field)
                    for key in computed:
                        assert_close(computed[key], saved[st][metric][key])
            checks.append('E1: all eight primary paired mean/CI comparisons independently recomputed')
        if kind == 'ool':
            for st in ('stable_ool','slip_ool'):
                computed = paired_bootstrap(groups['posterior_plus_E',st], groups['posterior_only',st], 'false_commit')
                saved = ool['contrasts']['posterior_plus_E - posterior_only/' + st]['false_commit']
                for key in computed:
                    assert_close(computed[key], saved[key])
            checks.append('OOL: two primary gate contrasts independently recomputed with family bootstrap')
            post_stops = [e for e in groups['posterior_only', 'stable_ool'] if e['terminal_kind'] == 'single']
            zero = [e for e in post_stops if e['gate']['consistent_wrong'] == 0]
            residual = [e for e in groups['stability_mixed_reference', 'stable_ool'] if e['false_commit']]
            mechanism = dict(n_posterior_stops=len(post_stops), n_E_zero=len(zero),
                             E_zero_targets=dict(Counter(e['terminal_id'] for e in zero)),
                             residual_stable_errors=len(residual),
                             residual_pairs=dict(Counter(e['removed_rule'] + ' -> ' + str(e['terminal_id']) for e in residual)),
                             noisy_pair_mixed_errors=sum(e['false_pair_mixed'] for e in groups['stability_mixed_reference', 'slip_ool']))
            assert mechanism['n_posterior_stops'] == 195 and mechanism['n_E_zero'] == 170
            assert mechanism['residual_stable_errors'] == 30
            for e in episodes:
                assert e['false_commit'] == (e['terminal_kind'] in ('single', 'pair', 'mixed'))
            checks.append('OOL scoring and counterfactual E=0 count verified from raw records')

    # This is a local sensitivity envelope, not an independent threshold choice.
    assert len(sweep) == 31
    assert e6['protocol']['threshold_selection_from_test'] is False
    for rec in e6['checks'].values():
        if isinstance(rec, dict) and 'pass' in rec:
            assert rec['pass']
    checks.append('E6 contains 31 unique configurations; no threshold selection; saved reproduction checks pass')
    source_paths = [run / 'outputs/summary.json' for run in RUNS.values()]
    source_paths += [RUNS[k] / 'outputs/episodes.json' for k in ('e1', 'ool')]
    source_paths += [RUNS['e6'] / 'outputs/episodes_default_test.json']
    report = dict(checks=checks, mechanism=mechanism,
                  sources={str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest() for p in source_paths},
                  extraction_only=True, raw_experiments_changed=False,
                  interpretation=dict(e1='four-arm nested comparison, not a full 2x2 factorial',
                                      stopping_contrast="Cprime minus B at cap=3", budget_contrast='C minus Cprime',
                                      ool_noisy='removed stable rule plus noise, not correct-program slip',
                                      e6='local OFAT; no independent risk certification'))
    (ROOT / 'docs/three_experiments_integration_audit_2026-10-21.json').write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(dict(checks=checks, mechanism=mechanism), ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
