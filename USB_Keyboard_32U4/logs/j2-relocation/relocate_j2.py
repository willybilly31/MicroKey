import pcbnew as p
import math, heapq, json
from pathlib import Path

ROOT=Path(__file__).resolve().parent
b=p.LoadBoard(str(ROOT/'finished.before-j2.kicad_pcb'))
mm=p.FromMM
def vec(x,y): return p.VECTOR2I(mm(x),mm(y))
def xy(v): return (round(p.ToMM(v.x),6),round(p.ToMM(v.y),6))
fps={f.GetReference():f for f in b.GetFootprints()}
j=fps['J2']
old={a.GetNetname():xy(a.GetPosition()) for a in j.Pads()}
# Remove only programming-connector branches, stopping at shared junctions.
for net in ['PB1','PB2','PB3']:
    for t in list(b.GetTracks()):
        if t.GetNetname()==net: b.Delete(t)
for net in ['GND','VCC','RESET']:
    tracks=[t for t in b.GetTracks() if t.GetNetname()==net and not isinstance(t,p.PCB_VIA) and t.GetLayer()==p.F_Cu]
    anchors={xy(a.GetPosition()) for f in b.GetFootprints() if f!=j for a in f.Pads() if a.GetNetname()==net}
    anchors|={xy(t.GetPosition()) for t in b.GetTracks() if isinstance(t,p.PCB_VIA) and t.GetNetname()==net}
    todo=[old[net]]; removed=[]
    while todo:
        pt=todo.pop()
        if pt!=old[net] and pt in anchors: continue
        adjacent=[t for t in tracks if t not in removed and pt in [xy(t.GetStart()),xy(t.GetEnd())]]
        if pt!=old[net] and len(adjacent)!=1: continue
        for t in adjacent:
            removed.append(t); todo.append(xy(t.GetEnd()) if xy(t.GetStart())==pt else xy(t.GetStart()))
    for t in removed: b.Delete(t)
# The old VCC test-pad via and its branch are no longer needed.
for t in list(b.GetTracks()):
    if t.GetNetname()=='VCC' and ((isinstance(t,p.PCB_VIA) and xy(t.GetPosition())==(109.0089,103.5512)) or
       (t.GetLayer()==p.B_Cu and min(t.GetStart().x,t.GetEnd().x)<mm(113))): b.Delete(t)

j.Flip(j.GetPosition(),p.FLIP_DIRECTION_LEFT_RIGHT)
j.SetPosition(vec(117.6,116.25))
# Bare pogo pads: no stencil apertures.
for a in j.Pads():
    layers=a.GetLayerSet(); layers.RemoveLayer(p.B_Paste); a.SetLayerSet(layers)
    if a.GetNetname()=='GND': a.SetLocalZoneConnection(p.ZONE_CONNECTION_FULL)
    a.BuildEffectiveShapes()
# Keep all existing copper and components inside the rectangular outline.
for d in b.GetDrawings():
    if d.GetLayer()==p.Edge_Cuts:
        a=xy(d.GetStart()); c=xy(d.GetEnd())
        d.SetStart(vec(135.2 if a[0]==131 else a[0],a[1]))
        d.SetEnd(vec(135.2 if c[0]==131 else c[0],c[1]))
for z in b.Zones():
    outline=z.Outline()
    for k in range(outline.OutlineCount()):
        chain=outline.Outline(k)
        for n in range(chain.PointCount()):
            pt=chain.CPoint(n)
            if pt.x==mm(130.5): chain.SetPoint(n,p.VECTOR2I(mm(134.7),pt.y))

p.SaveBoard(str(ROOT/'j2-routing-stage.kicad_pcb'),b,True)
b=p.LoadBoard(str(ROOT/'j2-routing-stage.kicad_pcb'))
j=next(f for f in b.GetFootprints() if f.GetReference()=='J2')

def obstacles(net,layer,extra=0.305):
    out=[]
    items=list(b.GetTracks())+[a for f in b.GetFootprints() for a in f.Pads()]
    for item in items:
        if item.GetNetname()==net or not item.IsOnLayer(layer): continue
        shape=item.GetEffectiveShape(layer)
        box=shape.BBox(); box.Inflate(mm(extra)); out.append((shape,box))
    return out
def clear_segment(a,c,obs,clearance=.305):
    seg=p.SEG(vec(*a),vec(*c))
    lo=(min(a[0],c[0]),min(a[1],c[1])); hi=(max(a[0],c[0]),max(a[1],c[1]))
    for shape,box in obs:
        if box.GetRight()<mm(lo[0]) or box.GetLeft()>mm(hi[0]) or box.GetBottom()<mm(lo[1]) or box.GetTop()>mm(hi[1]): continue
        if shape.Collide(seg,mm(clearance)): return False
    return True
def addtrack(net,a,c,layer):
    t=p.PCB_TRACK(b); t.SetStart(vec(*a)); t.SetEnd(vec(*c)); t.SetWidth(mm(.2)); t.SetLayer(layer); t.SetNetCode(b.FindNet(net).GetNetCode()); b.Add(t)
def via(net,pt):
    v=p.PCB_VIA(b); v.SetPosition(vec(*pt)); v.SetWidth(mm(.6)); v.SetDrill(mm(.3)); v.SetViaType(p.VIATYPE_THROUGH); v.SetLayerPair(p.F_Cu,p.B_Cu); v.SetNetCode(b.FindNet(net).GetNetCode()); b.Add(v)

# Short front fanouts at the original MCU pins; all long J2 routes are on B.Cu.
targets={}
for net,x in [('PB3',112),('PB2',112.8),('PB1',113.6)]:
    pad=(x,112.3375)
    found=False
    for y in ([112.0,112.1,112.2,113.4] if net=='PB2' else [113.4,113.5,113.3,113.6,113.2,112.8]):
        pt=(x,y)
        if clear_segment(pt,pt,obstacles(net,p.F_Cu,.505),.505) and clear_segment(pt,pt,obstacles(net,p.B_Cu,.505),.505) and clear_segment(pad,pt,obstacles(net,p.F_Cu)):
            addtrack(net,pad,pt,p.F_Cu); via(net,pt); targets[net]=pt; found=True; break
    if not found: raise RuntimeError('No safe fanout '+net)
targets['GND']=(120.1,113.71)
assert clear_segment(targets['GND'],targets['GND'],obstacles('GND',p.F_Cu,.505),.505), 'GND via collision'
via('GND',targets['GND'])
targets['VCC']=(115.2,113.3825)
assert clear_segment(targets['VCC'],targets['VCC'],obstacles('VCC',p.F_Cu,.505),.505), 'VCC via collision'
via('VCC',targets['VCC'])
targets['RESET']=(109.7781,114.8)
if not clear_segment(targets['RESET'],targets['RESET'],obstacles('RESET',p.F_Cu,.505),.505):
    raise RuntimeError('RESET via collision')
via('RESET',targets['RESET'])

def route(net,start,end):
    obs=obstacles(net,p.B_Cu)
    # 0.1 mm grid, exact endpoints connected by short clearance-checked segments.
    step=.1
    def coord(n): return (n[0]*step,n[1]*step)
    def snap(pt): return (round(pt[0]/step),round(pt[1]/step))
    s=snap(start); goal=snap(end)
    cache={}
    def free(n):
        if n not in cache: cache[n]=clear_segment(coord(n),coord(n),obs)
        return cache[n]
    def h(n): return math.hypot(n[0]-goal[0],n[1]-goal[1])
    q=[(h(s),0,s)]; best={s:0}; prev={}
    while q:
        _,g,n=heapq.heappop(q)
        if g>best.get(n,1e9): continue
        if n==goal: break
        for dx,dy in [(1,0),(-1,0),(0,1),(0,-1),(1,1),(1,-1),(-1,1),(-1,-1)]:
            nxt=(n[0]+dx,n[1]+dy)
            if not (1020<=nxt[0]<=1320 and 1005<=nxt[1]<=1315): continue
            ng=g+math.hypot(dx,dy)
            if ng>=best.get(nxt,1e9) or not free(nxt): continue
            if not clear_segment(coord(n),coord(nxt),obs): continue
            best[nxt]=ng; prev[nxt]=n; heapq.heappush(q,(ng+h(nxt),ng,nxt))
    else: raise RuntimeError('No path '+net)
    path=[end,coord(goal)]; n=goal
    while n!=s: n=prev[n]; path.append(coord(n))
    path.append(start); path.reverse()
    # Remove grid stair steps where a straight segment has the same clearance.
    clean=[path[0]]; k=0
    while k<len(path)-1:
        m=len(path)-1
        while m>k+1 and not clear_segment(path[k],path[m],obs): m-=1
        if not clear_segment(path[k],path[m],obs): raise RuntimeError('Endpoint blocked '+net)
        clean.append(path[m]); k=m
    for a,c in zip(clean,clean[1:]):
        if a!=c: addtrack(net,a,c,p.B_Cu)
    print(net,clean,flush=True)

for net in ['PB3','PB1','PB2','RESET','VCC','GND']:
    pad=next(a for a in j.Pads() if a.GetNetname()==net)
    route(net,xy(pad.GetPosition()),targets[net])

b.BuildConnectivity()
p.ZONE_FILLER(b).Fill(b.Zones())
p.SaveBoard(str(ROOT/'finished.kicad_pcb'),b,True)
print('Saved',flush=True)






