#!/usr/bin/env python3
import sys,json,shutil,time
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'scripts'));sys.path.insert(0,str(ROOT/'generators'))
from probe import invoke
from workflow import generate
results=[]
for tiny,size in [(False,100),(False,1000),(True,100),(True,1000)]:
 for runner in ['nift','turbo','nx']:
  r=ROOT/'work'/f'feasibility-{tiny}-{size}-{runner}';shutil.rmtree(r,ignore_errors=True);g=generate(r,size,runner,4,tiny=tiny);names=[t['id'] for t in g['tasks']]
  if runner!='nift':(r/'node_modules').symlink_to(ROOT/'work/tools/node_modules')
  try:
   for label,expected in [('full',names),('noop',[])]:
    v=invoke(r,runner,g,label,expected);v.update(size=size,tiny=tiny);results.append(v)
  except Exception as e:
   (ROOT/'investigation/feasibility-error.txt').write_text(str(e));raise
  (ROOT/'investigation/feasibility.json').write_text(json.dumps(results,indent=2)+'\n')
