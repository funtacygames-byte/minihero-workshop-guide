"""Record a reviewed bilingual revision. Hashes detect edits, not translation quality."""
from pathlib import Path
import argparse
import hashlib
import json

ROOT = Path(__file__).resolve().parents[1]

def digest(path):
    # Git may normalize line endings; checks must survive a Windows/Linux checkout.
    data = path.read_text(encoding='utf-8').replace('\r\n', '\n')
    return hashlib.sha256(data.encode('utf-8')).hexdigest()

def pairs():
    result = []
    for source_dir, target_dir in [('docs/zh-CN', 'docs/en'), ('templates/zh-CN', 'templates/en')]:
        for source in sorted((ROOT/source_dir).rglob('*')):
            if not source.is_file(): continue
            target = ROOT/target_dir/source.relative_to(ROOT/source_dir)
            if not target.is_file(): raise ValueError(f'Missing English counterpart: {target.relative_to(ROOT)}')
            result.append({'zh-CN': source.relative_to(ROOT).as_posix(), 'en': target.relative_to(ROOT).as_posix(),
                           'sourceHash': digest(source), 'translationHash': digest(target)})
        source_names = {p.relative_to(ROOT/source_dir).as_posix() for p in (ROOT/source_dir).rglob('*') if p.is_file()}
        target_names = {p.relative_to(ROOT/target_dir).as_posix() for p in (ROOT/target_dir).rglob('*') if p.is_file()}
        if source_names != target_names: raise ValueError(f'Unpaired files: {sorted(source_names ^ target_names)}')
    for source_name, target_name in [('README.zh-CN.md','README.md'),('templates/README.zh-CN.md','templates/README.md')]:
        result.append({'zh-CN':source_name,'en':target_name,'sourceHash':digest(ROOT/source_name),
                       'translationHash':digest(ROOT/target_name)})
    return result

def record():
    return {'guideRevision':2, 'reviewedApi':'1.8.0', 'reviewDate':'2026-10-14',
            'status':'local-reviewed-draft', 'hashAlgorithm':'SHA-256, UTF-8 with LF line endings',
            'meaningReview':'AI-assisted bilingual review; independent reader trial pending',
            'pairs':pairs()}

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--write',action='store_true',help='Record hashes only after reviewing both languages')
    args=parser.parse_args()
    value=record(); path=ROOT/'docs/revision.json'
    if args.write:
        path.write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
        print(f'Recorded {len(value["pairs"])} reviewed language pairs. Hashes do not certify meaning.')
    elif not path.exists() or json.loads(path.read_text(encoding='utf-8'))!=value:
        raise SystemExit('Revision record is missing or stale. Review edits, then run --write.')
    else: print(f'PASS revision record: {len(value["pairs"])} pairs')

if __name__=='__main__':main()
