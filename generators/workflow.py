#!/usr/bin/env python3
"""Generate equivalent native runner declarations; never schedule work here."""
import argparse,json,shutil
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def put(root,path,value):
 p=root/path;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(value)
def dump(root,path,value):put(root,path,json.dumps(value,indent=2)+'\n')
def graph(size):
 base=[('generate-schema',[], 'json'),('generate-client',['generate-schema'],'transform'),('lint',[],'check'),('typecheck',['generate-client'],'check'),('unit-test',['generate-client'],'check'),('build-web',['typecheck','lint','unit-test'],'transform'),('build-helper',[],'compile'),('docs',['generate-client'],'transform'),('package',['build-web','build-helper','docs'],'archive'),('integration-test',['package'],'check'),('verify',['integration-test'],'check'),('release-prep',['verify'],'json')]
 tasks=[{'id':n,'prerequisites':d,'kind':k,'input':f'inputs/{n}.json','output':None if k=='check' else f'out/{n}.json'} for n,d,k in base]
 for i in range(size-len(tasks)):
  n=f'asset-{i:05}'; tasks.append({'id':n,'prerequisites':['generate-schema'] if i%2 else [],'kind':'transform','input':f'inputs/{n}.json','output':f'out/{n}.json'})
 return {'schema':1,'tasks':tasks}
def generate(root,size,runner,jobs,checks='receipts',tiny=False):
 root.mkdir(parents=True,exist_ok=True);g=graph(size)
 if tiny:g={'schema':1,'tasks':[{'id':f'tiny-{i:05}','prerequisites':[],'kind':'tiny','input':f'inputs/tiny-{i:05}.json','output':f'out/tiny-{i:05}.json'} for i in range(size)]}
 (root/'out').mkdir(exist_ok=True)
 if tiny:shutil.copy2(ROOT/'work/tiny-body',root/'tiny-body')
 # Receipt track is explicitly different from arbitrary outputless checks.
 if checks=='receipts':
  for t in g['tasks']:
   if t['output'] is None:t['output']=f'out/{t["id"]}.json';t['receipt']=True
 dump(root,'graph.json',g);shutil.copy2(ROOT/'scripts/task_body.py',root/'task_body.py')
 put(root,'.gitignore','node_modules/\n.nx/\n.turbo/\n.nift/\nout/\ntrace.jsonl\nfail-task\n')
 for t in g['tasks']:dump(root,t['input'],{'value':1,'records':list(range(32))})
 package={'name':'workflow','version':'1.0.0','private':True,'packageManager':'npm@9.2.0','scripts':{t['id']:(f'./tiny-body {t["id"]}' if tiny else f'python3 task_body.py {t["id"]}') for t in g['tasks']}}
 dump(root,'package.json',package);dump(root,'package-lock.json',{'name':'workflow','version':'1.0.0','lockfileVersion':3,'requires':True,'packages':{'':{'name':'workflow','version':'1.0.0'}}})
 by={t['id']:t for t in g['tasks']}
 if runner=='turbo':
  dump(root,'turbo.json',{'tasks':{t['id']:{'dependsOn':t['prerequisites'],'inputs':[t['input'],'tiny-body' if tiny else 'task_body.py','graph.json'],'outputs':[t['output']] if t['output'] else [],'cache':bool(t['output'])} for t in g['tasks']}})
 elif runner=='nx':
  dump(root,'nx.json',{'defaultBase':'main','neverConnectToCloud':True,'cacheDirectory':'.nx/cache','parallel':jobs})
  dump(root,'project.json',{'name':'workflow','root':'.','targets':{t['id']:{'executor':'nx:run-commands','options':{'command':(f'./tiny-body {t["id"]}' if tiny else f'python3 task_body.py {t["id"]}')},'dependsOn':t['prerequisites'],'inputs':['{projectRoot}/'+t['input'],'{projectRoot}/tiny-body' if tiny else '{projectRoot}/task_body.py','{projectRoot}/graph.json',{'dependentTasksOutputFiles':'**/*'}],'outputs':['{projectRoot}/'+t['output']] if t['output'] else [],'cache':bool(t['output'])} for t in g['tasks']}})
 elif runner=='nift':
  dump(root,'.nift/config.json',{'config':{'content-dir':'inputs/','content-ext':'.json','output-dir':'out/','output-ext':'.json','default-template':'','build-threads':jobs,'incremental-mode':'hash','minify-exts':[]}})
  dump(root,'.nift/tracked.json',{'tracked':[{'name':t['id'],'title':t['id'],'depends':t['prerequisites'],'build':'tasks/action.f'} for t in g['tasks']]})
  put(root,'tasks/action.f','r := cmd("python3", "task_body.py", getenv("NIFT_HOOK_TARGET")).cwd(getenv("NIFT_HOOK_ROOT")).run()\nif(!r.launched || r.exit_code != 0) { throw error("Task failed: " + r.stderr, "user.task.failed") }\n')
  for t in g['tasks']:dump(root,'inputs/'+t['id']+'.deps.json',{'dependencies':['graph.json','tiny-body' if tiny else 'task_body.py',*[by[x]['output'] for x in t['prerequisites'] if by[x]['output']]]})
  put(root,'tasks/lint.f','r := cmd("python3", "task_body.py", "lint").run()\nif(!r.launched || r.exit_code != 0) { throw error(r.stderr, "user.task.failed") }\n')
 if tiny and runner=='nift':put(root,'tasks/action.f','r := cmd("./tiny-body", getenv("NIFT_HOOK_TARGET")).cwd(getenv("NIFT_HOOK_ROOT")).run()\nif(!r.launched || r.exit_code != 0) { throw error(r.stderr, "user.task.failed") }\n')
 return g
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True);p.add_argument('--size',type=int,default=20);p.add_argument('--runner',choices=['nift','turbo','nx'],required=True);p.add_argument('--jobs',type=int,default=4);p.add_argument('--checks',choices=['receipts','outputless'],default='receipts');a=p.parse_args();generate(a.output,a.size,a.runner,a.jobs,a.checks)
