#!/usr/bin/env python3
import json,sys,subprocess,shutil,hashlib
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'scripts'));sys.path.insert(0,str(ROOT/'generators'))
from workflow import generate
from probe import command,ENV
rows=[]
for runner in ['nift','turbo','nx']:
 r=ROOT/'work'/('environment-'+runner);shutil.rmtree(r,ignore_errors=True);g=generate(r,20,runner,4)
 body=r/'task_body.py';s=body.read_text();s=s.replace("data=json.loads(inputs[0]);", "if t['id']=='asset-00000':inputs.append(os.environ.get('TASK_PROBE','').encode())\n data=json.loads(inputs[0]);");body.write_text(s)
 if runner!='nift':(r/'node_modules').symlink_to(ROOT/'work/tools/node_modules')
 if runner=='turbo':
  p=r/'turbo.json';v=json.loads(p.read_text());v['tasks']['asset-00000']['env']=['TASK_PROBE'];p.write_text(json.dumps(v))
 if runner=='nx':
  p=r/'project.json';v=json.loads(p.read_text());v['targets']['asset-00000']['inputs'].append({'env':'TASK_PROBE'});p.write_text(json.dumps(v))
 for value in ['A','B']:
  (r/'trace.jsonl').unlink(missing_ok=True);p=subprocess.run(command(runner,g),cwd=r,env=dict(ENV,TASK_PROBE=value),capture_output=True,text=True,timeout=1800);assert p.returncode==0
  events=[json.loads(x) for x in (r/'trace.jsonl').read_text().splitlines()] if (r/'trace.jsonl').exists() else []
  digest=hashlib.sha256((r/'inputs/asset-00000.json').read_bytes()+b'\n'+value.encode()).hexdigest()
  actual=json.loads((r/'out/asset-00000.json').read_text())['digest'];starts=[e['task'] for e in events if e['event']=='start']
  rows.append({'runner':runner,'value':value,'starts':starts,'output_matches_environment':actual==digest,'declared_env_input':runner!='nift','exit_code':p.returncode})
  if value=='B':assert (actual==digest)==(runner!='nift');assert set(starts)==({'asset-00000'} if runner!='nift' else set())
Path('investigation/environment-probes.json').write_text(json.dumps(rows,indent=2)+'\n');print('Environment probes certified: Nx/Turbo declarations invalidate; Nift runtime read alone does not')
