"""Extract selected public declarations from an authorized MiniHero source tree.

This is a declaration index, not a C# compiler or a semantics generator. It writes
no method bodies, private members, absolute source paths, or game assemblies.
"""
from pathlib import Path
import argparse
import hashlib
import json
import re

ROOT = Path(__file__).resolve().parents[1]
TYPES = {
    'MiniHeroModApi', 'MiniHeroMod', 'MiniHeroModAttribute', 'IModRegistrar', 'ModRegistrarExtensions',
    'ModText', 'ModAssets', 'ModPresentation', 'IModPresentationContent',
    'ModMusicTheme', 'ModConfig', 'ModConfigDefinition',
    'GameContentModule', 'TreasureContent', 'IMultipleVariantEffect',
    'CharacterContent', 'TreasurePoolDefinition', 'TraitContent', 'MoveContent',
    'EnemyContent', 'EnemyTraitContent', 'EnemyTraitEvent', 'EnemyTraitDamageEvent',
    'StageContent', 'AdventureContent', 'AdventureStepDefinition',
    'AdventureDifficultyDefinition', 'StageDefinition', 'GameRuleEvent',
    'ITreasureRuntime', 'TreasureStatsEvent', 'BeforeHealingEvent', 'AfterHealingEvent',
    'StageEnteredEvent', 'ColumnClearedEvent', 'BeforeMoveResolvedEvent',
    'AfterMoveResolvedEvent', 'EnemyKilledEvent', 'BeforeItemEffectEvent',
    'ItemUsedEvent', 'ItemContent', 'EventContent', 'ContentCards'
}

def mask(source):
    # Preserve offsets while hiding braces and comment markers within literals.
    pattern = r'//[^\n]*|/\*[\s\S]*?\*/|@"(?:""|[^"])*"|"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\''
    return re.sub(pattern, lambda m: ''.join('\n' if c == '\n' else ' ' for c in m[0]), source)

def closing(masked, start, left='{', right='}'):
    depth=0
    for i in range(start,len(masked)):
        if masked[i]==left: depth+=1
        elif masked[i]==right:
            depth-=1
            if depth==0:return i
    raise ValueError('Unbalanced source declaration')

def clean(value):
    value=re.sub(r'//[^\n]*|/\*[\s\S]*?\*/','',value)
    return re.sub(r'\s+',' ',value).strip()

def members(source, masked, start, end, interface):
    result=[]; i=start+1
    while i<end:
        while i<end and masked[i].isspace():i+=1
        if i>=end:break
        if masked[i]=='[':
            i=closing(masked,i,'[',']')+1;continue
        begin=i; paren=0; bracket=0
        while i<end:
            c=masked[i]
            if c=='(':paren+=1
            elif c==')':paren-=1
            elif c=='[':bracket+=1
            elif c==']':bracket-=1
            if not paren and not bracket and (c in '{;' or masked[i:i+2]=='=>'):break
            i+=1
        header=source[begin:i]; head=clean(header)
        visible=interface or bool(re.match(r'public\b',head))
        if masked[i:i+2]=='=>':
            # Skip expression bodies, including initializers with nested braces.
            j=i+2; level=0
            while j<end:
                if masked[j] in '{([':level+=1
                elif masked[j] in '})]':level-=1
                elif masked[j]==';' and level==0:break
                j+=1
            if visible:result.append(head+';' if '(' in head else head+' { get; }')
            i=j+1
        elif masked[i]=='{':
            j=closing(masked,i)
            if visible and not re.search(r'\b(class|struct|enum|interface)\b',head):
                if '(' in head:result.append(head+';')
                else:
                    access=clean(source[i+1:j])
                    accessors=re.findall(r'(?:(?:private|protected|internal)\s+)?(?:get|set)\s*;',access)
                    result.append(head+' { '+(' '.join(accessors) if accessors else 'get;')+' }')
            i=j+1
            # Skip a property initializer after its accessor block.
            while i<end and masked[i].isspace():i+=1
            if i<end and masked[i]=='=':
                while i<end and masked[i]!=';':i+=1
                i+=1
        else:
            if visible:result.append(head+';')
            i+=1
    return result

def extract(game):
    base=game/'Assets/Game/脚本'; found={}; hashes={}
    # Sources are scanned read-only; only selected declarations are retained.
    for path in sorted(base.rglob('*.cs')):
        source=path.read_text(encoding='utf-8-sig'); masked=mask(source)
        matches=list(re.finditer(r'\bpublic\s+(?:(?:abstract|sealed|static|partial)\s+)*(class|interface)\s+(\w+)[^{]*\{',masked))
        for match in matches:
            kind,name=match[1],match[2]
            if name not in TYPES:continue
            start=match.end()-1; end=closing(masked,start)
            relative=path.relative_to(game).as_posix()
            hashes[relative]=hashlib.sha256(path.read_bytes()).hexdigest()
            if name in found:raise ValueError('Duplicate selected type: '+name)
            found[name]={'declaration':clean(source[match.start():start]),'members':members(source,masked,start,end,kind=='interface'),'source':relative}
    missing=TYPES-set(found)
    if missing:raise ValueError('Missing public declarations: '+', '.join(sorted(missing)))
    version=re.search(r'public const string Version\s*=\s*"([^"]+)"', '\n'.join(found['MiniHeroModApi']['members']))
    if not version:raise ValueError('Missing API version declaration')
    return {'api':version[1],'reviewDate':'2026-10-13','extraction':'selected source declarations; inherited members listed under their defining base','sources':hashes,'types':dict(sorted(found.items()))}

def render(data,lang):
    zh=lang=='zh-CN'; other='en' if zh else 'zh-CN'
    lines=['# 公开 API 声明索引' if zh else '# Public API declaration index','',f'[{"English" if zh else "简体中文"}](../../{other}/reference/api-surface.md) · [{"目录" if zh else "Index"}](../README.md)','',
        ('教程修订 2' if zh else 'Guide revision 2')+f' · API {data["api"]} · 2026-10-13','',
        '从当前授权工程只读提取的选定公开声明，不包含方法实现；它不是完整 SDK 文档。继承成员在定义它的基类下查询。默认值与调用语义须同时查对应[规则参考](../README.md#reference)。维护者可使用[提取工具](../../../tools/extract_api.py)重新生成。' if zh else 'Selected public declarations extracted read-only from the authorized source, without implementations. This is not the entire SDK. Look up inherited members under their defining base and use the [rule references](../README.md#reference) for defaults and semantics. Maintainers can regenerate it with the [extractor](../../../tools/extract_api.py).','']
    lines += ['| Type | Type | Type |','| --- | --- | --- |']
    names=list(data['types'])
    for index in range(0,len(names),3):
        cells=[f'[{name}](#{name.lower()})' for name in names[index:index+3]]
        lines.append('| '+' | '.join(cells+['']*(3-len(cells)))+' |')
    lines.append('')
    for name,item in data['types'].items():
        lines += ['## '+name,'','```csharp',item['declaration'],'{']+['    '+m for m in item['members']]+['}','```','']
    return '\n'.join(lines)

def main():
    p=argparse.ArgumentParser();p.add_argument('--source-root',type=Path,required=True);p.add_argument('--check',action='store_true')
    args=p.parse_args();data=extract(args.source_root.resolve())
    outputs={ROOT/'docs/api-surface.json':json.dumps(data,ensure_ascii=False,indent=2)+'\n'}
    for lang in ['en','zh-CN']:outputs[ROOT/f'docs/{lang}/reference/api-surface.md']=render(data,lang)
    for path,text in outputs.items():
        if args.check:
            if not path.exists() or path.read_text(encoding='utf-8')!=text:raise SystemExit('API reference drift: '+str(path.relative_to(ROOT)))
        else:path.write_text(text,encoding='utf-8')
    print(f'{len(data["types"])} selected types; {sum(len(v["members"]) for v in data["types"].values())} declarations; '+('current' if args.check else 'written'))

if __name__=='__main__':main()
