#!/usr/bin/env python3
import os,json,subprocess,sys,time,shutil
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'generators'));sys.path.insert(0,str(ROOT/'scripts'))
from workflow import generate
from oracle import certify
ENV=dict(os.environ,NX_DAEMON='false',NX_NO_CLOUD='true',TURBO_TELEMETRY_DISABLED='1',DO_NOT_TRACK='1',NX_TASKS_RUNNER_DYNAMIC_OUTPUT='false')
def command(runner,g,jobs=4,target=None,force=False):
 names=target or [t['id'] for t in g['tasks']]
 if runner=='nift':return [str(ROOT/'work/nift-source/nift'),'build',*(['--all'] if force else names if target else [])]
 if runner=='turbo':return [str(ROOT/'work/tools/node_modules/.bin/turbo'),'run',*names,f'--concurrency={jobs}','--cache=local:' if force else '--cache=local:rw','--continue=dependencies-successful','--output-logs=errors-only']
 return [str(ROOT/'work/tools/node_modules/.bin/nx'),'run-many','--projects=workflow','--targets='+','.join(names),f'--parallel={jobs}','--outputStyle=static',*(['--skip-nx-cache'] if force else [])]
def invoke(r,runner,g,label,expected,jobs=4,target=None,force=False,failed=None):
 (r/'trace.jsonl').unlink(missing_ok=True);start=time.monotonic();args=command(runner,g,jobs,target,force)
 if label=='recovery' and runner=='nift':args=[str(ROOT/'work/nift-source/nift'),'build','--repair']
 p=subprocess.run(args,cwd=r,env=ENV,capture_output=True,text=True,timeout=1800);wall=time.monotonic()-start
 (r/(label+'.log')).write_text(p.stdout+p.stderr);print(runner,label,p.returncode,round(wall,3),flush=True)
 if p.returncode and not failed:raise RuntimeError((p.stdout+p.stderr)[-3500:])
 assert (p.returncode!=0)==bool(failed)
 result=certify(r,expected,jobs,failed);result.update(exit_code=p.returncode,wall_seconds=wall,label=label,runner=runner);return result
def main():
 results=[]
 for runner in ['nift','turbo','nx']:
  r=ROOT/'work'/('probe-'+runner);shutil.rmtree(r,ignore_errors=True);g=generate(r,20,runner,4);names=[t['id'] for t in g['tasks']]
  if runner!='nift' and not (r/'node_modules').exists():(r/'node_modules').symlink_to(ROOT/'work/tools/node_modules')
  results.append(invoke(r,runner,g,'full',names))
  results.append(invoke(r,runner,g,'noop',[]))
  p=r/'inputs/asset-00000.json';v=json.loads(p.read_text());v['value']=2;p.write_text(json.dumps(v)+'\n')
  results.append(invoke(r,runner,g,'leaf',['asset-00000']))
  p=r/'inputs/generate-schema.json';v=json.loads(p.read_text());v['value']=2;p.write_text(json.dumps(v)+'\n')
  dirty={'generate-schema'}
  for t in g['tasks']:
   if any(x in dirty for x in t['prerequisites']):dirty.add(t['id'])
  results.append(invoke(r,runner,g,'shared',dirty))
  results.append(invoke(r,runner,g,'target-forced',['asset-00000'],target=['asset-00000'],force=(runner!='nift')))
  (r/'fail-task').write_text('generate-schema')
  permitted=set(names)-dirty|{'generate-schema'}
  results.append(invoke(r,runner,g,'failure',permitted,force=True,failed='generate-schema'))
  (r/'fail-task').unlink()
  results.append(invoke(r,runner,g,'recovery',names,force=True))
 (ROOT/'investigation/initial-probe.json').write_text(json.dumps(results,indent=2)+'\n')
if __name__=='__main__':main()
