"""Portable documentation checks; no game references, network, or third-party packages."""
from pathlib import Path
from urllib.parse import unquote, urlsplit
import collections
import json
import re
import sys
import xml.etree.ElementTree as ET
from sync_revision import ROOT, record
from extract_api import mask

errors=[]
def fail(path,message):errors.append(f'{path.relative_to(ROOT)}: {message}')

def fences(text):
    return re.findall(r'^```([^\n]*)\n([\s\S]*?)^```\s*$',text,re.M)

def prose(text):
    return re.sub(r'^```[^\n]*\n[\s\S]*?^```\s*$','',text,flags=re.M)

def anchors(text):
    found=set(re.findall(r'<a\s+id=["\']([^"\']+)',text))
    counts=collections.Counter()
    for heading in re.findall(r'^#{1,6}\s+(.+?)\s*#*$',prose(text),re.M):
        heading=re.sub(r'\[([^\]]+)\]\([^)]*\)',r'\1',heading)
        heading=re.sub(r'<[^>]+>','',heading).lower().replace('`','')
        slug=''.join(c for c in heading if c.isalnum() or c in '_- ')
        slug=slug.replace(' ','-')
        n=counts[slug];counts[slug]+=1
        found.add(slug+(f'-{n}' if n else ''))
    return found

def csharp_contract(code):
    # Remove translated display literals/comments but preserve API structure and numbers.
    structure=re.sub(r'\s+','',mask(code))
    literals=re.findall(r'"((?:\\.|[^"\\])*)"',re.sub(r'//[^\n]*|/\*[\s\S]*?\*/','',code))
    stable=[s for s in literals if (re.fullmatch(r'[A-Za-z0-9_.:/{}<>-]+',s) and
            (any(c in s for c in './_:') or s in {'default','weighted','Default','Weighted','Layered','Branching','LayeredBranching','en','zh-Hans'})) or '{' in s or re.search(r'\d',s)]
    # Format templates can contain translated words, but their placeholder contracts cannot.
    stable=[(tuple(re.findall(r'\{[^{}]+\}',s)),tuple(re.findall(r'\d+',re.sub(r'\{[^{}]+\}','',s))))
            if '{' in s or not re.fullmatch(r'[A-Za-z0-9_.:/{}<>-]+',s) else s for s in stable]
    option_ids=re.findall(r'\b(?:id|sourceCardId|resolverContentId|conditionExpression)\s*=\s*"((?:\\.|[^"\\])*)"',code)
    branch_ids=re.findall(r'\bcase\s+"((?:\\.|[^"\\])*)"',code)
    return structure,stable,option_ids,branch_ids

def json_contract(raw):
    value=json.loads(raw)
    def visit(item):
        if isinstance(item,dict):return {key:('<locale>' if key=='locale' else visit(item[key])) for key in sorted(item)}
        if isinstance(item,list):return [visit(x) for x in item]
        if not isinstance(item,str):return item
        if re.fullmatch(r'[A-Za-z0-9_.:/<>-]+',item) and (any(c in item for c in './_:') or item in {'event','stage','en','zh-Hans'}):return item
        return {'placeholders':re.findall(r'\{[^{}]+\}',item),'numbers':re.findall(r'\d+(?:\.\d+)?',item)}
    return visit(value)

def contains_gameplay_recipe(value):
    # Manifests and locale catalogs are auxiliary data; content rules belong in C#.
    if isinstance(value,dict):
        if {'contentType','richChoices','graphNodes','graphEdges'} & value.keys():return True
        return any(contains_gameplay_recipe(item) for item in value.values())
    if isinstance(value,list):return any(contains_gameplay_recipe(item) for item in value)
    return False

paths=[p for p in ROOT.rglob('*') if p.is_file() and not any(part in {'.git','.local','__pycache__'} for part in p.relative_to(ROOT).parts)]
markdown=[p for p in paths if p.suffix=='.md']
for path in markdown+[ROOT/'llms.txt']:
    data=path.read_text(encoding='utf-8')
    marks=re.findall(r'^```',data,re.M)
    if len(marks)%2:fail(path,'unclosed code fence')
    for kind,code in fences(data):
        if kind.strip()=='json':
            try:
                parsed_json=json.loads(code)
                if contains_gameplay_recipe(parsed_json):
                    fail(path,'gameplay JSON recipe conflicts with the C# authoring policy')
            except ValueError as e:fail(path,f'invalid fenced JSON: {e}')
    for link in re.findall(r'!?\[[^\]]*\]\(([^\n]+?)\)',prose(data)):
        link=link.strip()
        if link.startswith('<'):link=link[1:link.index('>')]
        else:link=link.split(' "',1)[0]
        parsed=urlsplit(link)
        if parsed.scheme or link.startswith('//'):continue
        target=(path.parent/unquote(parsed.path)).resolve() if parsed.path else path
        if not target.is_relative_to(ROOT):fail(path,f'link escapes repository: {link}');continue
        if not target.exists():fail(path,f'missing link: {link}');continue
        if parsed.fragment and target.suffix=='.md' and unquote(parsed.fragment) not in anchors(target.read_text(encoding='utf-8')):
            fail(path,f'missing anchor: {link}')
    if re.search(r'(?i)[A-Z]:[\\/]Users[\\/]|gh[pousr]_[A-Za-z0-9]{20,}|github_pat_',data):
        fail(path,'private path or credential-shaped text')

try:
    value=record()
    saved=ROOT/'docs/revision.json'
    if not saved.exists() or json.loads(saved.read_text(encoding='utf-8'))!=value:fail(saved,'bilingual revision hashes are stale')
    api_file=ROOT/'docs/api-surface.json'
    if json.loads(api_file.read_text(encoding='utf-8'))['api']!=value['reviewedApi']:
        fail(api_file,'API version differs from the reviewed revision; review references and update the baseline')
    for pair in value['pairs']:
        zh,en=ROOT/pair['zh-CN'],ROOT/pair['en']
        if zh.suffix=='.json':
            if json_contract(zh.read_text(encoding='utf-8'))!=json_contract(en.read_text(encoding='utf-8')):
                fail(en,'JSON keys, IDs, numbers or placeholders differ in paired file')
            continue
        if zh.suffix=='.md':
            a=[c for kind,c in fences(zh.read_text(encoding='utf-8')) if kind.strip()=='csharp']
            b=[c for kind,c in fences(en.read_text(encoding='utf-8')) if kind.strip()=='csharp']
        else:a=[zh.read_text(encoding='utf-8')];b=[en.read_text(encoding='utf-8')]
        if len(a)!=len(b):fail(en,'C# fence count differs between languages');continue
        for index,(left,right) in enumerate(zip(a,b),1):
            if csharp_contract(left)!=csharp_contract(right):fail(en,f'C# contract differs in fragment {index}')
        if zh.suffix=='.md':
            left_json=[c for kind,c in fences(zh.read_text(encoding='utf-8')) if kind.strip()=='json']
            right_json=[c for kind,c in fences(en.read_text(encoding='utf-8')) if kind.strip()=='json']
            if len(left_json)!=len(right_json):fail(en,'JSON fence count differs between languages')
            else:
                for index,(left,right) in enumerate(zip(left_json,right_json),1):
                    if json_contract(left)!=json_contract(right):fail(en,f'JSON keys, IDs, numbers or placeholders differ in fragment {index}')
    capability_file=ROOT/'docs/capabilities.json'
    capability=json.loads(capability_file.read_text(encoding='utf-8'))
    api=json.loads(api_file.read_text(encoding='utf-8'))
    if capability['reviewedApi']!=value['reviewedApi'] or capability['guideRevision']!=value['guideRevision']:
        fail(capability_file,'capability version differs from reviewed revision')
    ids=set()
    for item in capability['capabilities']:
        if item['id'] in ids:fail(capability_file,'duplicate capability: '+item['id'])
        ids.add(item['id'])
        if item['status'] not in {'available','partial','backend-only'}:fail(capability_file,'unknown status: '+item['id'])
        for name in item['apiTypes']:
            if name not in api['types']:fail(capability_file,'type absent from declaration index: '+name)
        for lang in ['en','zh-CN']:
            if not (ROOT/item['docs'][lang]).is_file():fail(capability_file,'missing route: '+item['docs'][lang])
            if not item['boundary'][lang].strip():fail(capability_file,'missing boundary: '+item['id'])
    for lang,locale in [('zh-CN','zh-Hans'),('en','en')]:
        catalog_path=ROOT/f'templates/{lang}/localization.json'
        catalog=json.loads(catalog_path.read_text(encoding='utf-8'))
        if catalog.get('locale')!=locale:fail(catalog_path,'incorrect locale')
        entries=catalog.get('entries',[])
        keys=[item['key'] for item in entries]
        if len(keys)!=len(set(key.casefold() for key in keys)):fail(catalog_path,'duplicate localization key')
        if any(not re.fullmatch(r'[a-z0-9_.]+',key) for key in keys):fail(catalog_path,'non-semantic localization key')
        known=set(keys)
        for snippet in (ROOT/f'templates/{lang}').glob('*.cs.txt'):
            code=snippet.read_text(encoding='utf-8')
            used=re.findall(r'ModText\.(?:Get|Format)\(\s*(?:ModEntry\.PackageId|context\.PackageId),\s*"([^"\n]+)"',code)
            used+=re.findall(r'ModUi\.(?:Text|Button|HostButton)\(\s*"[^"\n]+",\s*"([^"\n]+)"',code)
            for key in used:
                if key not in known:fail(catalog_path,f'missing key {key} used by {snippet.name}')
except (ValueError,KeyError,json.JSONDecodeError) as e:errors.append(str(e))

for path in paths:
    if path.suffix=='.svg':
        try:
            svg=ET.fromstring(path.read_text(encoding='utf-8'))
            if not svg.tag.endswith('svg') or 'viewBox' not in svg.attrib:fail(path,'SVG needs root viewBox')
            if any(e.tag.endswith('script') for e in svg.iter()):fail(path,'SVG contains executable script')
        except ET.ParseError as e:fail(path,f'invalid SVG: {e}')
    if path.suffix.lower() in {'.dll','.pdb','.exe','.zip','.unity','.asset','.meta','.log','.user'}:
        fail(path,'forbidden documentation release artifact')
    if any(part in {'bin','obj','Library','Temp','.tmode-sdk','.snapshots','Installed','Builds'} for part in path.relative_to(ROOT).parts):
        fail(path,'generated or private directory in release tree')
    if path.suffix=='.json':
        try:json.loads(path.read_text(encoding='utf-8'))
        except (ValueError,UnicodeError) as e:fail(path,f'invalid JSON: {e}')

if errors:
    print('\n'.join(errors));sys.exit(1)
print(f'PASS {len(markdown)} Markdown files: local links, anchors, fences, bilingual C#/JSON contracts, revision hashes')
print(f'PASS {len(capability["capabilities"])} capability routes: versions, statuses, bilingual boundaries and indexed types')
print('PASS JSON/SVG syntax and release artifact boundaries')
print('Boundary: no external-link, C# compiler, gameplay, UI, or online-publishing verification.')
