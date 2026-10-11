#!/usr/bin/env python3
"""Independent audit: reconstruct graph inputs/outputs and validate raw traces."""
import argparse,json,hashlib,statistics,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'generators'));from workflow import graph

def audit(directory):
 rows=[json.loads(x) for x in (directory/'observations.jsonl').read_text().splitlines()];groups={}
 for row in rows:
  tasks=graph(row['size'])['tasks']
  if row['tiny']:tasks=[{'id':f'tiny-{i:05}','prerequisites':[],'kind':'tiny','output':f'out/tiny-{i:05}.json'} for i in range(row['size'])]
  by={t['id']:t for t in tasks};names=set(by)
  if not row['tiny']:
   for t in tasks:
    if t['output'] is None:t['output']=f'out/{t["id"]}.json'
  if row['case']=='uncached-full':expected=names
  else:
   expected=set(row['mutation']['names']);again=True
   while again:
    again=False
    for t in tasks:
     if t['id'] not in expected and any(p in expected for p in t['prerequisites']):expected.add(t['id']);again=True
  if row['scope'] is not None:expected &=set(row['scope'])
  raw=(directory/(row['id']+'.trace.jsonl')).read_bytes();assert hashlib.sha256(raw).hexdigest()==row['trace_sha256']
  events=[json.loads(x) for x in raw.splitlines()];starts={};done={};active=peak=0
  for e in sorted(events,key=lambda e:e['time_ns']):
   n=e['task'];assert n in expected
   if e['event']=='start':
    assert n not in starts
    for p in by[n]['prerequisites']:
     if p in expected:assert p in done and done[p]<e['time_ns']
    starts[n]=e['time_ns'];active+=1
   else:
    assert e['event']=='complete' and n in starts and n not in done
    done[n]=e['time_ns'];active-=1
   peak=max(peak,active);assert 0<=active<=row['jobs']
  assert active==0 and set(starts)==expected and set(done)==expected
  hashes={};memo={};changed=set(row['mutation']['names'])
  def produce(n):
   if n in memo:return memo[n]
   t=by[n];v={'value':row['mutation']['value'] if n in changed else 1,'records':list(range(32))}
   own=(json.dumps(v,**({} if n in changed else {'indent':2}))+'\n').encode()
   if row['tiny']:
    h=14695981039346656037
    for b in own:h=((h^b)*1099511628211)%2**64
    result=(str(h)+'\n').encode()
   else:
    pieces=[own,*[produce(p) for p in t['prerequisites'] if by[p]['output']]]
    result=(json.dumps({'task':n,'digest':hashlib.sha256(b'\n'.join(pieces)).hexdigest()},sort_keys=True)+'\n').encode()
   memo[n]=result;hashes[n]=hashlib.sha256(result).hexdigest();return result
  for n in row['scope'] if row['scope'] is not None else by:produce(n)
  digest=hashlib.sha256(json.dumps(hashes,sort_keys=True).encode()).hexdigest();assert digest==row['proof']['output_manifest_sha256'], 'reconstructed output mismatch '+row['id']
  m=json.loads((directory/(row['id']+'.metrics.json')).read_text());assert m==row['metrics'] and m['exit_code']==0 and m['wall_ms']>0
  assert peak==row['proof']['peak_concurrency']
  if 'native_cache_hits' in row['proof'] and row['runner']!='nift':
   selected=set(row['scope']) if row['scope'] is not None else names
   assert row['proof']['native_cache_hits']==len(selected)-len(expected)
  if not row['warmup']:
   key=(row['tiny'],row['size'],row['jobs'],row['case'],row['runner']);groups.setdefault(key,[]).append(row)
 declared=json.loads((directory/'plan.json').read_text())
 expected_groups={(c['tiny'],c['size'],c['jobs'],c['case'],r):c['samples'] for c in declared for r in ['nift','turbo','nx']}
 assert set(groups)==set(expected_groups), 'incomplete matrix'
 assert all(len(groups[k])==n for k,n in expected_groups.items()), 'sample count mismatch'
 assert sum(r['warmup'] for r in rows)==len(expected_groups), 'warmup count mismatch'
 summary=[]
 def percentile(x,q):
  x=sorted(x);i=(len(x)-1)*q;lo=int(i);hi=min(lo+1,len(x)-1);return x[lo]+(x[hi]-x[lo])*(i-lo)
 for key,rs in sorted(groups.items()):
  tiny,size,jobs,case,runner=key;item={'tiny':tiny,'size':size,'jobs':jobs,'case':case,'runner':runner,'samples':len(rs)}
  for field in ['wall_ms','cpu_ms','peak_rss_kib']:
   vals=[r['metrics'][field] for r in rs];item[field]={'median':statistics.median(vals),'min':min(vals),'max':max(vals),'p95':percentile(vals,.95) if len(vals)>=20 else None}
  item['executed_tasks']=len(rs[0]['proof']['starts']);item['skipped_or_cache_hit']=size-item['executed_tasks'] if rs[0]['scope'] is None else None
  item['peak_body_concurrency']=max(r['proof']['peak_concurrency'] for r in rs);summary.append(item)
 result={'observations':len(rows),'measured':sum(not r['warmup'] for r in rows),'cells':len(groups),'all_correct':True,'summary':summary}
 (directory/'summary.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({k:v for k,v in result.items() if k!='summary'}));return result
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('directory',type=Path);a=p.parse_args();audit(a.directory)
