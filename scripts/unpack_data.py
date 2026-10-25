"""Verify and unpack losslessly compressed publication records."""
from __future__ import annotations
import gzip
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def unpack():
    manifest = json.loads((ROOT / 'reproduction_data/manifest.json').read_text(encoding='utf-8'))
    count = 0
    for row in manifest['files']:
        if not row['gzip']:
            continue
        source = (ROOT / row['stored_path']).resolve()
        target = (ROOT / row['path']).resolve()
        if not source.is_relative_to(ROOT) or not target.is_relative_to(ROOT):
            raise ValueError('Archive path leaves the repository')
        raw = gzip.decompress(source.read_bytes())
        if hashlib.sha256(raw).hexdigest() != row['published_sha256']:
            raise ValueError(f'Checksum mismatch: {row["stored_path"]}')
        if target.exists() and target.read_bytes() != raw:
            raise FileExistsError(f'Refusing to overwrite modified data: {row["path"]}')
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(raw)
        count += 1
    print(f'PASS: {count} compressed records verified and unpacked')


if __name__ == '__main__':
    unpack()
