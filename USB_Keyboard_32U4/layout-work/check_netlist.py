import re,collections,json
from pathlib import Path
import pcbnew as p
def parse(s):
 tokens=re.findall(r'"(?:\\.|[^"\\])*"|[^\s()]+|[()]',s); stack=[];result=None
 for t in tokens:
  if t=='(':
   a=[]
   if stack:stack[-1].append(a)
   stack.append(a)
  elif t==')':result=stack.pop()
  else:stack[-1].append(json.loads(t) if t.startswith('"') else t)
 return result
def child(a,k):return next(x for x in a if isinstance(x,list) and x[0]==k)
n=parse(Path('layout-work/schematic.net').read_text());expected={}
for net in child(n,'nets')[1:]:
 name=child(net,'name')[1]
 for node in [x for x in net if isinstance(x,list) and x[0]=='node']:
  expected[(child(node,'ref')[1],child(node,'pin')[1])]=name
b=p.LoadBoard('layout-work/placed.kicad_pcb');actual={}
for f in b.GetFootprints():
 for pa in f.Pads():
  if pa.GetNumber():actual[(f.GetReference(),pa.GetNumber())]=pa.GetNetname()
errors=[]
for key,val in expected.items():
 if key not in actual or actual[key]!=val:errors.append((key,val,actual.get(key)))
for key,val in actual.items():
 if key not in expected:errors.append((key,'absent from schematic',val))
print('Compared',len(expected),'schematic pins with',len(actual),'unique PCB pads. Mismatches:',errors)
Path('layout-work/netlist-check.txt').write_text(f'Compared {len(expected)} schematic pins with {len(actual)} unique PCB pads.\nMismatches: {errors}\n')
assert not errors
