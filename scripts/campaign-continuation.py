#!/usr/bin/env python3
"""Local/official serial harness. The runners alone schedule actual task work."""
import argparse,json,os,subprocess,sys,time,hashlib,shutil,re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'generators'));sys.path.insert(0,str(ROOT/'scripts'))
from workflow import generate
from probe import command,ENV
from oracle import certify

def closure(g,names):
 by={t['id']:t for t in g['tasks']};out=set()
 def visit(n):
  if n in out:return
  out.add(n)
  for p in by[n]['prerequisites']:visit(p)
 for n in names:visit(n)
 return out

def descendants(g,names):
 out=set(names)
 for t in g['tasks']:
  if any(p in out for p in t['prerequisites']):out.add(t['id'])
 return out

def plan(smoke=False):
 cells=[]
 for tiny,sizes in [(False,[20,100,1000]),(True,[100,1000])]:
  for size in sizes:
   for case in ['noop','leaf','fanout','full']+(['one-percent'] if tiny else [])+(['shared'] if not tiny else []):
    n=50 if case=='noop' else (20 if case=='leaf' else 10 if size<=20 else 5 if size<=100 else 3)
    cells.append({'tiny':tiny,'size':size,'jobs':4,'case':case,'samples':1 if smoke else n})
 for jobs in [1,2]:
  cells.append({'tiny':False,'size':100,'jobs':jobs,'case':'full','samples':1 if smoke else 5})
 cells.append({'tiny':False,'size':20,'jobs':4,'case':'uncached-full','samples':1 if smoke else 10})
 for case in ['target-leaf','target-subgraph','multi-target']:
  cells.append({'tiny':False,'size':20,'jobs':4,'case':case,'samples':1 if smoke else 10})
 return cells

def run(args):
 output=args.output.resolve();output.mkdir(parents=True,exist_ok=True);cells=plan(args.smoke)
 if args.cell is not None:cells=[cells[args.cell]]
 (output/'plan.json').write_text(json.dumps(cells,indent=2)+'\n')
 rows=[json.loads(x) for x in (output/'observations.jsonl').read_text().splitlines()];seq=len(rows)
 for localci,c in enumerate(cells):
  if localci<27:continue
  ci=args.cell if args.cell is not None else localci
  fixtures={};graphs={}
  for runner in ['nift','turbo','nx']:
   r=ROOT/'work'/f'campaign-{c["tiny"]}-{c["size"]}-{c["jobs"]}-{runner}'
   # Reuse prepared successful state; creation/setup never enters timing.
   g=generate(r,c['size'],runner,c['jobs'],tiny=c['tiny']);graphs[runner]=g;fixtures[runner]=r
   if runner!='nift' and not (r/'node_modules').exists():(r/'node_modules').symlink_to(ROOT/'work/tools/node_modules')
   p=subprocess.run(command(runner,g,c['jobs']),cwd=r,env=ENV,capture_output=True,text=True,timeout=1800)
   if p.returncode:raise RuntimeError('bootstrap failed '+runner+' '+p.stderr[-2000:])
   trace=[json.loads(x) for x in (r/'trace.jsonl').read_text().splitlines()] if (r/'trace.jsonl').exists() else []
   # Bootstrap output equality is checked below after clearing cumulative trace.
   (r/'trace.jsonl').unlink(missing_ok=True);certify(r,[],c['jobs'])
  for roundno in range(c['samples']+1):
   order=['nift','turbo','nx'];offset=(roundno+ci)%3;order=order[offset:]+order[:offset]
   for runner in order:
    r=fixtures[runner];g=graphs[runner];names=[t['id'] for t in g['tasks']];target=None;force=c['case']=='uncached-full'
    case=c['case'];dirty=set();scope=None;changed=[]
    if case in ['leaf','fanout','one-percent','shared','full','target-leaf','target-subgraph','multi-target']:
     if case=='full':changed=names
     elif case=='shared':changed=['generate-schema']
     elif case=='target-subgraph':changed=['generate-schema'];target=['release-prep'];scope=closure(g,target)
     elif case=='multi-target':changed=['asset-00000','asset-00002'];target=changed
     elif case in ['fanout','one-percent']:changed=[t['id'] for t in g['tasks'] if t['id'].startswith(('asset-','tiny-'))][:max(1,c['size']//(100 if case=='one-percent' else 10))]
     else:changed=[names[0] if c['tiny'] else 'asset-00000'];target=changed if case=='target-leaf' else None
     for n in changed:
      p=r/'inputs'/f'{n}.json';v=json.loads(p.read_text());v['value']+=1+(100000*(ci+1) if roundno==0 else 0);p.write_text(json.dumps(v)+'\n')
     dirty=descendants(g,changed)
     if scope is not None:dirty &= scope
    expected=set(names) if force else dirty
    if target and scope is None:scope=closure(g,target)
    # Selected targets are dirty for all runners; Nift force semantics do not
    # add extra clean work in these cases.
    (r/'trace.jsonl').unlink(missing_ok=True);seq+=1;stem=f'{seq:06}';metric=output/(stem+'.metrics.json')
    args0=command(runner,g,c['jobs'],target,force)
    with (output/(stem+'.stdout')).open('w') as out,(output/(stem+'.stderr')).open('w') as err:
     p=subprocess.run([str(ROOT/'work/measure'),str(metric),*args0],cwd=r,env=ENV,stdout=out,stderr=err,timeout=1800)
    if p.returncode:raise RuntimeError('measured command failed '+runner+' '+stem)
    proof=certify(r,expected,c['jobs'],scope=scope)
    selected=scope if scope is not None else set(names)
    skipped=len(selected)-len(expected)
    text=re.sub(r'\x1b\[[0-9;]*m','',(output/(stem+'.stdout')).read_text())
    cache_match=re.search(r'Cached:\s+(\d+) cached,\s+(\d+) total',text) if runner=='turbo' else re.search(r'Cache:\s+(\d+)/(\d+) hit',text) if runner=='nx' else None
    if runner!='nift':
     if runner=='nx' and force:
      assert skipped==0 and 'Cache:' in text and 'Skipped (--skip-nx-cache)' in text,'missing explicit disabled-cache receipt'
     else:
      assert cache_match and int(cache_match.group(1))==skipped and int(cache_match.group(2))==len(selected),'native cache summary mismatch'
    proof['not_executed']=sorted(selected-expected);proof['blocked']=[]
    proof['skip_mechanism']='tracked clean-state validation' if runner=='nift' else 'native local task-cache hit'
    proof['native_cache_hits']=int(cache_match.group(1)) if cache_match else 0 if runner=='nx' and force else None
    events=(r/'trace.jsonl').read_text() if (r/'trace.jsonl').exists() else '';(output/(stem+'.trace.jsonl')).write_text(events)
    hashes=proof.pop('output_hashes');proof['output_manifest_sha256']=hashlib.sha256(json.dumps(hashes,sort_keys=True).encode()).hexdigest()
    row={'id':stem,**c,'runner':runner,'cell_index':ci,'mutation':{'names':changed,'value':100000*(ci+1)+2+roundno if changed else None},'scope':sorted(scope) if scope is not None else None,'round':roundno,'warmup':roundno==0,'order':order,'command':args0,'metrics':json.loads(metric.read_text()),'proof':proof,'trace_sha256':hashlib.sha256(events.encode()).hexdigest()}
    rows.append(row)
    with (output/'observations.jsonl').open('a') as f:f.write(json.dumps(row,separators=(',',':'))+'\n')
    print(f'{localci+1}/{len(cells)} {case} {c["size"]} {runner} round {roundno} {row["metrics"]["wall_ms"]:.1f}ms tasks={len(expected)}',flush=True)
   if case=='target-subgraph':
    # Restore a globally coherent baseline outside timing: unselected schema
    # consumers intentionally remain stale after targeted execution.
    for runner in order:
     p=subprocess.run(command(runner,graphs[runner],c['jobs']),cwd=fixtures[runner],env=ENV,capture_output=True,timeout=1800)
     if p.returncode:raise RuntimeError('target baseline repair failed')
 (output/'complete.json').write_text(json.dumps({'observations':len(rows),'cells':len(cells),'all_correct':True},indent=2)+'\n')
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--output',required=True,type=Path);p.add_argument('--smoke',action='store_true');p.add_argument('--cell',type=int);a=p.parse_args();run(a)
