#!/usr/bin/env python3
import json,sys,subprocess,shutil
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'scripts'));sys.path.insert(0,str(ROOT/'generators'))
from workflow import generate
from probe import command,ENV
from oracle import certify
rows=[]
for runner in ['nift','turbo','nx']:
 r=ROOT/'work'/('features-'+runner);shutil.rmtree(r,ignore_errors=True);g=generate(r,20,runner,4)
 if runner!='nift':(r/'node_modules').symlink_to(ROOT/'work/tools/node_modules')
 p=subprocess.run(command(runner,g),cwd=r,env=ENV,capture_output=True,text=True,timeout=1800);assert p.returncode==0
 (r/'trace.jsonl').unlink(missing_ok=True);(r/'out/asset-00000.json').unlink()
 p=subprocess.run(command(runner,g),cwd=r,env=ENV,capture_output=True,text=True,timeout=1800);assert p.returncode==0
 proof=certify(r,['asset-00000'] if runner=='nift' else [],4);rows.append({'runner':runner,'case':'missing-output','mechanism':'rebuild' if runner=='nift' else 'cache-restore','proof':proof})
 (ROOT/'investigation'/f'{runner}-restore.log').write_text(p.stdout+p.stderr)
# Genuine outputless checks in a mixed native task DAG, not synthetic receipts.
for runner in ['nift','turbo','nx']:
 r=ROOT/'work'/('checks-'+runner);shutil.rmtree(r,ignore_errors=True);g=generate(r,20,runner,4,'outputless')
 if runner!='nift':(r/'node_modules').symlink_to(ROOT/'work/tools/node_modules')
 for iteration in range(2 if runner!='nift' else 1):
  (r/'trace.jsonl').unlink(missing_ok=True);p=subprocess.run(command(runner,g),cwd=r,env=ENV,capture_output=True,text=True,timeout=1800)
  events=[json.loads(x) for x in (r/'trace.jsonl').read_text().splitlines()] if (r/'trace.jsonl').exists() else []
  starts=[e['task'] for e in events if e['event']=='start'];done=[e['task'] for e in events if e['event']=='complete']
  if runner!='nift':
   expected=[t['id'] for t in g['tasks']] if iteration==0 else [t['id'] for t in g['tasks'] if t['kind']=='check']
   certify(r,expected,4);assert p.returncode==0
  else:assert p.returncode!=0 and 'custom build did not produce the tracked output file' in p.stderr
  rows.append({'runner':runner,'case':'outputless','iteration':iteration,'exit_code':p.returncode,'starts':starts,'completions':done,'native_dag_supported':runner!='nift'})
  (ROOT/'investigation'/f'{runner}-outputless-{iteration}.log').write_text(p.stdout+p.stderr)
 if runner=='nift':
  (r/'trace.jsonl').unlink(missing_ok=True);p=subprocess.run([str(ROOT/'work/nift-source/nift'),'tasks/lint.f'],cwd=r,env=ENV,capture_output=True,text=True);assert p.returncode==0
  rows.append({'runner':runner,'case':'direct-f-outputless-check','exit_code':p.returncode})
(ROOT/'investigation/feature-probes.json').write_text(json.dumps(rows,indent=2)+'\n')
print('Certified feature probes:',len(rows))
