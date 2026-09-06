from pathlib import Path
from html.parser import HTMLParser
import requests, json, subprocess
P=Path(__file__).resolve().parents[1]
class Text(HTMLParser):
    def __init__(self):super().__init__();self.skip=0;self.parts=[]
    def handle_starttag(self,t,a):
        if t in ['script','style']:self.skip+=1
        if t in ['p','br','div','h1','h2','h3']:self.parts.append('\n')
    def handle_endtag(self,t):
        if t in ['script','style']:self.skip=max(0,self.skip-1)
    def handle_data(self,d):
        if not self.skip:self.parts.append(d)
u='https://www.odbms.org/blog/2017/08/big-data-at-ups-interview-with-jack-levis/'
r=requests.get(u,timeout=40);r.raise_for_status();p=Text();p.feed(r.text)
out='\n'.join(x.strip() for x in ''.join(p.parts).splitlines() if x.strip())
assert '200,000' in out and 'Gettysburg' in out
(P/'research/evidence_odbms.txt').write_text(out,encoding='utf-8')
(P/'research/evidence_odbms.html').write_text(r.text,encoding='utf-8')
s=P/'src/citations/sources.py'
cmd=['python3',str(s),'--ledger',str(P/'research/ledger.json')]
for q in ['The ORION savings of 100 million miles and $300 million to $400 million annually is in addition to the savings from PFT.','Research into ORION began in 2003, and the first model was field tested in 2008 in Gettysburg, Pennsylvania.']:
    subprocess.run(cmd+['quote','1','--text',q,'--from',str(P/'research/evidence_odbms.txt')],check=True)
print('ODBMS evidence saved:',len(out))
