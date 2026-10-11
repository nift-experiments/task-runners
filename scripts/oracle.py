#!/usr/bin/env python3
"""Independent graph traversal, task event ordering and output calculation."""
import hashlib,json
from pathlib import Path
def certify(root,expected,jobs,failed=None,scope=None):
 g=json.loads((root/'graph.json').read_text());by={t['id']:t for t in g['tasks']};events=[json.loads(x) for x in (root/'trace.jsonl').read_text().splitlines()] if (root/'trace.jsonl').exists() else []
 starts=[e['task'] for e in events if e['event']=='start'];done={e['task']:e['time_ns'] for e in events if e['event']=='complete'};fails=[e['task'] for e in events if e['event']=='fail']
 assert len(starts)==len(set(starts)), 'duplicate task starts'
 assert set(starts)==set(expected),(set(starts)-set(expected),set(expected)-set(starts))
 assert set(done)==set(expected)-({failed} if failed else set()), 'completion mismatch'
 assert fails==([failed] if failed else []), 'failure mismatch'
 active=peak=0
 for e in sorted(events,key=lambda e:e['time_ns']):
  active+=1 if e['event']=='start' else -1;peak=max(peak,active);assert 0<=active<=jobs
  if e['event']=='start':
   for p in by[e['task']]['prerequisites']:
    if p in expected:assert p in done and done[p]<e['time_ns'],'prerequisite order violated'
 assert active==0
 hashes={}
 def output(n):
  t=by[n];pieces=[(root/t['input']).read_bytes()]
  for p in t['prerequisites']:
   if by[p]['output']:pieces.append(output(p))
  if t['kind']=='tiny':
   h=14695981039346656037
   for byte in pieces[0]:h=((h^byte)*1099511628211)&((1<<64)-1)
   result=(str(h)+'\n').encode()
  else:result=(json.dumps({'task':n,'digest':hashlib.sha256(b'\n'.join(pieces)).hexdigest()},sort_keys=True)+'\n').encode()
  if t['output'] and n!=failed:
   actual=(root/t['output']).read_bytes();assert actual==result, f'output differs: {n}';hashes[n]=hashlib.sha256(actual).hexdigest()
  return result
 invalid={failed} if failed else set()
 changed=True
 while changed:
  changed=False
  for t in g['tasks']:
   if t['id'] not in invalid and any(p in invalid for p in t['prerequisites']):invalid.add(t['id']);changed=True
 for n in (scope if scope is not None else by):
  if n not in invalid:output(n)
 return {'starts':starts,'complete':sorted(done),'failed':fails,'peak_concurrency':peak,'output_hashes':hashes}
