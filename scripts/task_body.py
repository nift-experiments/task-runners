#!/usr/bin/env python3
"""Identical task work, no cache or selection logic. Trace writes are atomic."""
import hashlib,json,os,sys,time,subprocess,tarfile,io,tempfile
from pathlib import Path
root=Path.cwd();g=json.loads((root/'graph.json').read_text());by={t['id']:t for t in g['tasks']};t=by[sys.argv[1]]
def event(kind):
 line=json.dumps({'task':t['id'],'event':kind,'time_ns':time.monotonic_ns(),'pid':os.getpid()})+'\n'
 fd=os.open(root/'trace.jsonl',os.O_CREAT|os.O_WRONLY|os.O_APPEND,0o600);os.write(fd,line.encode());os.close(fd)
event('start')
try:
 if (root/'fail-task').exists() and (root/'fail-task').read_text().strip()==t['id']:raise RuntimeError('injected prerequisite failure')
 inputs=[(root/t['input']).read_bytes()]
 for n in t['prerequisites']:
  out=by[n]['output']
  if out:inputs.append((root/out).read_bytes())
 data=json.loads(inputs[0]); records=data['records'];assert sum(records)==sum(range(len(records)))
 digest=hashlib.sha256(b'\n'.join(inputs)).hexdigest()
 # Deterministic controlled work: JSON processing, text transform, checks,
 # one actual native helper compilation, and deterministic archive validation.
 if t['kind']=='transform':assert ' '.join(str(x) for x in records).split()==[str(x) for x in records]
 if t['kind']=='compile':
  with tempfile.TemporaryDirectory(prefix='task-helper-') as tmp:
   out=Path(tmp)
   src=out/'helper.c';src.write_text('int main(void){return 0;}\n')
   subprocess.run(['cc','-O2','-o',str(out/'helper'),str(src)],check=True,capture_output=True)
   subprocess.run([str(out/'helper')],check=True)
 if t['kind']=='archive':
  buff=io.BytesIO()
  with tarfile.open(fileobj=buff,mode='w') as tar:
   for i,b in enumerate(inputs):
    info=tarfile.TarInfo(f'input-{i}.json');info.size=len(b);info.mtime=0;info.mode=0o644;tar.addfile(info,io.BytesIO(b))
  with tarfile.open(fileobj=io.BytesIO(buff.getvalue())) as tar:assert len(tar.getmembers())==len(inputs)
 if t['output']:
  p=root/t['output'];p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps({'task':t['id'],'digest':digest},sort_keys=True)+'\n')
 event('complete')
except Exception as e:
 event('fail');print(f'{t["id"]}: {e}',file=sys.stderr);sys.exit(7)
