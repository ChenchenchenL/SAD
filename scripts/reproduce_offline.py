"""Rebuild statistics and source CSVs without network or API calls."""
from __future__ import annotations
import json
import math
import os
from pathlib import Path
import subprocess
import sys
from unpack_data import unpack

ROOT = Path(__file__).resolve().parents[1]
V5 = ROOT / 'experiments/2026-10-20_llm_v4_v5/v5'


def compare(a, b, path='root'):
    if isinstance(a, dict):
        assert isinstance(b, dict) and set(a) == set(b), path
        for key in a:
            compare(a[key], b[key], f'{path}/{key}')
    elif isinstance(a, list):
        assert isinstance(b, list) and len(a) == len(b), path
        for i, (x, y) in enumerate(zip(a, b)):
            compare(x, y, f'{path}/{i}')
    elif isinstance(a, (int, float)) and not isinstance(a, bool):
        assert math.isclose(a, b, rel_tol=1e-10, abs_tol=1e-12), path
    else:
        assert a == b, path


def run(relative):
    env = os.environ.copy()
    env['SIM_ROOT'] = str(ROOT)
    p = subprocess.run([sys.executable, str(ROOT / relative)], cwd=ROOT,
                       env=env, capture_output=True, text=True, encoding='utf-8')
    log = ROOT / 'verification' / (Path(relative).stem + '.log')
    log.parent.mkdir(exist_ok=True)
    log.write_text(p.stdout + p.stderr, encoding='utf-8')
    if p.returncode:
        print(p.stdout[-2000:])
        print(p.stderr[-3000:])
        raise RuntimeError(f'Failed: {relative}')
    print(f'PASS: {relative}')


def main():
    (ROOT / 'results/figures/qa').mkdir(parents=True, exist_ok=True)
    unpack()
    targets = ['diagnosis_audit.json', 'feedback_audit.json']
    expected = {f: json.loads((V5 / 'out/final_audit' / f).read_text(encoding='utf-8')) for f in targets}
    run('experiments/2026-10-20_llm_v4_v5/v5/regression_checks.py')
    for name in ['final_audit_v5.py', 'feedback_audit_v5.py']:
        run(f'experiments/2026-10-20_llm_v4_v5/v5/{name}')
    for f in targets:
        actual = json.loads((V5 / 'out/final_audit' / f).read_text(encoding='utf-8'))
        compare(expected[f], actual, f)
        print(f'PASS: archived and regenerated {f} match')
    run('results/figures/scripts/extract_source_data.py')
    run('results/figures/scripts/extract_extension_data.py')
    run('results/figures/scripts/audit_three_experiments_sources.py')
    result = {'status': 'PASS', 'network_calls': 0, 'python': sys.version.split()[0],
              'checks': ['information-boundary regression', 'main diagnosis audit',
                         'feedback audit', 'archived-vs-regenerated statistics',
                         'source CSV extraction', 'extension source/CI audit']}
    (ROOT / 'verification/offline_result.json').write_text(json.dumps(result, indent=2) + '\n', encoding='utf-8')
    print('PASS: offline reproduction completed; no LLM requests were made')


if __name__ == '__main__':
    main()
