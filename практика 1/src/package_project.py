from pathlib import Path
import subprocess,sys,json,re,zipfile,hashlib
from PIL import Image,ImageOps,ImageDraw
P=Path(__file__).resolve().parents[1]
required=['README.md','Практическая_работа_1.md','Практическая_работа_1_Проектирование_ИС.pptx','Практическая_работа_1_Проектирование_ИС.pdf','research/case_selection.md','research/case_analysis.md','research/sources.md']+[f'docs/{x}.md' for x in ['architecture','lifecycle','use_case_specification','digital_technology_proposal','questions','speaker_notes']]+[f'diagrams/{x}.puml' for x in ['as_is','to_be','use_case','architecture','lifecycle','future_technology']]+[f'diagrams/rendered/{x}.png' for x in ['as_is','to_be','use_case','architecture','lifecycle','gantt','future_technology']]+['diagrams/gantt.csv']
for p in required:assert (P/p).is_file() and (P/p).stat().st_size>0,p
report=(P/'Практическая_работа_1.md').read_text(encoding='utf-8')
headings=re.findall(r'^## (\d+)\. (.*)$',report,re.M)
assert [int(h[0]) for h in headings]==list(range(1,18)),headings
for x in P.rglob('*.md'):
    for link in re.findall(r'\]\(([^)]+)\)',x.read_text(encoding='utf-8')):
        if not link.startswith(('https://','http://','#','mailto:')):assert (x.parent/link).exists(),(x,link)
for x in [P/'Практическая_работа_1.md',*list((P/'docs').glob('*.md')),*list((P/'research').glob('*.md'))]:
    if re.search(r'\[\d+\]',x.read_text(encoding='utf-8')):
        subprocess.run(['python3',str(P/'src/citations/sources.py'),'--ledger',str(P/'research/ledger.json'),'render','--replace-in',str(x)],check=True,capture_output=True)
    result=subprocess.run(['python3',str(P/'src/citations/sources.py'),'--ledger',str(P/'research/ledger.json'),'verify',str(x),'--evidence'],capture_output=True,text=True)
    assert result.returncode==0,(x,result.stdout,result.stderr)
# Контактный лист экспортов для финальной визуальной проверки.
imgs=sorted((P/'diagrams/rendered').glob('*.png'));sheet=Image.new('RGB',(1800,3*740),'#e1e6eb');draw=ImageDraw.Draw(sheet)
for i,f in enumerate(imgs):
    im=Image.open(f).convert('RGB');im.thumbnail((570,675));xx=(i%3)*600+(600-im.width)//2;yy=(i//3)*740+42;sheet.paste(im,(xx,yy));draw.text(((i%3)*600+14,(i//3)*740+12),f.stem,fill='#20364d')
sheet.save(P/'preview/diagrams_contact.jpg',quality=94)
assert len(imgs)==9
v=json.loads((P/'docs/verification.json').read_text());assert not v['shape_boundary_errors'] and v['slides']==v['pdf_pages']==15
manifest={'required_artifacts_verified':len(required),'report_sections':len(headings),'diagram_pngs':len(imgs),'slides':v['slides'],'speaker_words':v['speaker_words'],'sha256':{f:hashlib.sha256((P/f).read_bytes()).hexdigest() for f in required}}
(P/'docs/delivery_manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
archive=P.with_suffix('.zip')
files=sorted(f for f in P.rglob('*') if f.is_file() and '__pycache__' not in f.parts and f.name!='.DS_Store')
with zipfile.ZipFile(archive,'w',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
    for f in files:z.write(f,Path(P.name)/f.relative_to(P))
with zipfile.ZipFile(archive) as z:assert z.testzip() is None and len(z.namelist())==len(files)
print(json.dumps({'archive':str(archive),'archive_files':len(files),'bytes':archive.stat().st_size,**{k:val for k,val in manifest.items() if k!='sha256'}},ensure_ascii=False,indent=2))
