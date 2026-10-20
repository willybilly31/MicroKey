import pcbnew as p
from pathlib import Path
import math,heapq,json,itertools
ROOT=Path(__file__).resolve().parents[2]/'layout-work'
b=p.LoadBoard(str(ROOT/'finished.before-45-routing.kicad_pcb'))
original=p.LoadBoard(str(ROOT/'finished.before-j2.kicad_pcb'))
original_ids={t.m_Uuid.AsString() for t in original.GetTracks()}
mm=p.FromMM
def vec(pt):return p.VECTOR2I(mm(pt[0]),mm(pt[1]))
def xy(v):return(round(p.ToMM(v.x),6),round(p.ToMM(v.y),6))
def pads():return [a for f in b.GetFootprints() for a in f.Pads()]
def tracks():return list(b.GetTracks())
def isvia(t):return isinstance(t,p.PCB_VIA)
def addtrack(net,a,c,layer,width=.2):
    if a==c:return
    t=p.PCB_TRACK(b);t.SetStart(vec(a));t.SetEnd(vec(c));t.SetWidth(mm(width));t.SetLayer(layer);t.SetNetCode(b.FindNet(net).GetNetCode());b.Add(t)
def addvia(net,pt):
    v=p.PCB_VIA(b);v.SetPosition(vec(pt));v.SetWidth(mm(.6));v.SetDrill(mm(.3));v.SetViaType(p.VIATYPE_THROUGH);v.SetLayerPair(p.F_Cu,p.B_Cu);v.SetNetCode(b.FindNet(net).GetNetCode());b.Add(v);return v
ACTIVE_CLEAR=.305
def obstacles(net,layer,clearance=None):
    if clearance is None:clearance=ACTIVE_CLEAR
    out=[]
    for item in tracks()+pads():
        if item.GetNetname()==net or not item.IsOnLayer(layer):continue
        shape=item.GetEffectiveShape(layer);box=shape.BBox();box.Inflate(mm(clearance));out.append((shape,(box.GetLeft(),box.GetRight(),box.GetTop(),box.GetBottom())))
    return out
def clear(a,c,obs,clearance=None):
    if clearance is None:clearance=ACTIVE_CLEAR
    av=vec(a);cv=vec(c);seg=p.SEG(av,cv)
    left=min(av.x,cv.x);right=max(av.x,cv.x);top=min(av.y,cv.y);bottom=max(av.y,cv.y)
    for shape,box in obs:
        if box[1]<left or box[0]>right or box[3]<top or box[2]>bottom:continue
        if shape.Collide(seg,mm(clearance)):return False
    return True
def via_safe(net,pt,ignore=None):
    for a in pads():
        for layer in [p.F_Cu,p.B_Cu]:
            if a.IsOnLayer(layer) and a.GetEffectiveShape(layer).Collide(vec(pt),mm(.455)):return False
    for layer in [p.F_Cu,p.B_Cu]:
        if not clear(pt,pt,obstacles(net,layer,.505),.505):return False
    for t in tracks():
        if isvia(t) and t!=ignore and math.dist(pt,xy(t.GetPosition()))<.81:return False
    return 100.85<pt[0]<134.35 and 100.35<pt[1]<132.15

def octpaths(a,c):
    ax,ay=mm(a[0]),mm(a[1]);cx,cy=mm(c[0]),mm(c[1]);dx=cx-ax;dy=cy-ay
    if dx==0 or dy==0 or abs(dx)==abs(dy):return [[a,c]]
    d=min(abs(dx),abs(dy));sx=1 if dx>=0 else -1;sy=1 if dy>=0 else -1
    mid1=((ax+sx*d)/1e6,(ay+sy*d)/1e6)
    mid2=((cx-sx*d)/1e6,(cy-sy*d)/1e6)
    return [[a,mid1,c],[a,mid2,c]]
def validpath(path,obs):return all(clear(a,c,obs) for a,c in zip(path,path[1:]))
def simplify(path,obs):
    out=[path[0]];k=0
    while k<len(path)-1:
        chosen=None
        for m in range(len(path)-1,k,-1):
            opts=[x for x in octpaths(path[k],path[m]) if validpath(x,obs)]
            if opts:chosen=(m,min(opts,key=lambda x:sum(math.dist(a,c) for a,c in zip(x,x[1:]))));break
        if not chosen:raise RuntimeError('simplify blocked')
        k,pts=chosen;out.extend(pts[1:])
    clean=[]
    for pt in out:
        if clean and pt==clean[-1]:continue
        if len(clean)>1:
            a,c=clean[-2],clean[-1]
            dx1=mm(c[0])-mm(a[0]);dy1=mm(c[1])-mm(a[1]);dx2=mm(pt[0])-mm(c[0]);dy2=mm(pt[1])-mm(c[1])
            if dx1*dy2==dy1*dx2 and dx1*dx2+dy1*dy2>=0:clean.pop()
        clean.append(pt)
    return clean

def route(net,start,end,layer,commit=True):
    obs=obstacles(net,layer)
    def coord(n):return(n[0]/10,n[1]/10)
    def attach(pt,outward):
        found={}
        gx,gy=round(pt[0]*10),round(pt[1]*10)
        for x in range(gx-3,gx+4):
            for y in range(gy-3,gy+4):
                n=(x,y);a,c=(pt,coord(n)) if outward else (coord(n),pt)
                opts=[o for o in octpaths(a,c) if validpath(o,obs)]
                if opts:found[n]=min(opts,key=lambda o:sum(math.dist(a,c) for a,c in zip(o,o[1:])))
        return found
    starts=attach(start,True);goals=attach(end,False)
    if not starts or not goals:raise RuntimeError(f'Endpoint blocked {net} {start} {end}')
    def h(n):return math.hypot(n[0]-end[0]*10,n[1]-end[1]*10)
    q=[];best={};prev={};origin={}
    for n,path in starts.items():
        cost=sum(math.dist(a,c)*10 for a,c in zip(path,path[1:]));best[n]=cost;prev[n]=None;origin[n]=path;heapq.heappush(q,(cost+h(n),cost,n))
    cache={}
    def free(n):
        if n not in cache:cache[n]=clear(coord(n),coord(n),obs)
        return cache[n]
    expansions=0
    while q:
        _,g,n=heapq.heappop(q)
        if g>best.get(n,1e99)+1e-8:continue
        if n in goals:break
        expansions+=1
        if expansions>110000:raise RuntimeError('Search exhausted '+net)
        for dx,dy in [(1,0),(-1,0),(0,1),(0,-1),(1,1),(1,-1),(-1,1),(-1,-1)]:
            nn=(n[0]+dx,n[1]+dy)
            if not(1008<=nn[0]<=1344 and 1003<=nn[1]<=1322):continue
            ng=g+math.hypot(dx,dy)
            if ng>=best.get(nn,1e99)-1e-8 or not free(nn) or not clear(coord(n),coord(nn),obs):continue
            best[nn]=ng;prev[nn]=n;heapq.heappush(q,(ng+h(nn),ng,nn))
    else:raise RuntimeError('No route '+net)
    path=[coord(n)]+goals[n][1:]
    while prev[n] is not None:n=prev[n];path.insert(0,coord(n))
    path=origin[n][:-1]+path
    clean=simplify(path,obs)
    if commit:
        for a,c in zip(clean,clean[1:]):addtrack(net,a,c,layer)
        print('ROUTE',net,b.GetLayerName(layer),clean,flush=True)
    return clean

def route_bridge(net,start,end):
    # Search both copper layers when the bottom pad array blocks a planar path.
    obs={l:obstacles(net,l) for l in [p.F_Cu,p.B_Cu]}
    viaobs=[]
    for a in pads():
        for l in [p.F_Cu,p.B_Cu]:
            if a.IsOnLayer(l):
                shape=a.GetEffectiveShape(l);box=shape.BBox();box.Inflate(mm(.455));viaobs.append((shape,(box.GetLeft(),box.GetRight(),box.GetTop(),box.GetBottom()),.455))
    for t in tracks():
        for l in [p.F_Cu,p.B_Cu]:
            if not t.IsOnLayer(l):continue
            if isvia(t):
                sh=p.SHAPE_CIRCLE(t.GetPosition(),mm(.51));box=sh.BBox();box.Inflate(mm(.305));viaobs.append((sh,(box.GetLeft(),box.GetRight(),box.GetTop(),box.GetBottom()),.305))
            elif t.GetNetname()!=net:
                sh=t.GetEffectiveShape(l);box=sh.BBox();box.Inflate(mm(.505));viaobs.append((sh,(box.GetLeft(),box.GetRight(),box.GetTop(),box.GetBottom()),.505))
    def coord(n):return(n[0]/10,n[1]/10)
    def attach(pt,reverse=False):
        found={};gx,gy=round(pt[0]*10),round(pt[1]*10)
        for x in range(gx-3,gx+4):
            for y in range(gy-3,gy+4):
                n=(x,y,p.B_Cu);a,c=(coord(n),pt) if reverse else (pt,coord(n))
                opts=[o for o in octpaths(a,c) if validpath(o,obs[p.B_Cu])]
                if opts:found[n]=opts[0]
        return found
    starts=attach(start);goals=attach(end,True)
    # The existing goal via is accessible from either layer.
    for n in list(goals):
        opts=[o for o in octpaths(coord(n),end) if validpath(o,obs[p.F_Cu])]
        if opts:goals[(n[0],n[1],p.F_Cu)]=opts[0]
    cache={};vcache={};best={};prev={};orig={};q=[]
    def h(n):return math.hypot(n[0]-end[0]*10,n[1]-end[1]*10)
    for n,path in starts.items():
        g=sum(math.dist(a,c)*10 for a,c in zip(path,path[1:]));best[n]=g;prev[n]=None;orig[n]=path;heapq.heappush(q,(g+h(n),g,n))
    def free(n):
        if n not in cache:cache[n]=clear(coord(n),coord(n),obs[n[2]])
        return cache[n]
    def vf(n):
        key=n[:2]
        if key not in vcache:
            point=vec(coord(n));seg=p.SEG(point,point);ok=True
            for sh,box,margin in viaobs:
                if box[0]<=point.x<=box[1] and box[2]<=point.y<=box[3] and sh.Collide(seg,mm(margin)):
                    ok=False;break
            vcache[key]=ok
        return vcache[key]
    expanded=0
    while q:
        _,g,n=heapq.heappop(q)
        if g>best.get(n,1e99)+1e-8:continue
        if n in goals:break
        expanded+=1
        if expanded>180000:raise RuntimeError('Bridge search exhausted '+net)
        neighbors=[((n[0]+dx,n[1]+dy,n[2]),math.hypot(dx,dy)) for dx,dy in [(1,0),(-1,0),(0,1),(0,-1),(1,1),(1,-1),(-1,1),(-1,-1)]]
        if n[0]%2==0 and n[1]%2==0 and vf(n):neighbors.append(((n[0],n[1],p.F_Cu if n[2]==p.B_Cu else p.B_Cu),35))
        for nn,cost in neighbors:
            if not(1008<=nn[0]<=1344 and 1003<=nn[1]<=1322):continue
            ng=g+cost
            if ng>=best.get(nn,1e99)-1e-8 or not free(nn):continue
            if n[2]==nn[2] and not clear(coord(n),coord(nn),obs[n[2]]):continue
            best[nn]=ng;prev[nn]=n;heapq.heappush(q,(ng+h(nn),ng,nn))
    else:raise RuntimeError('No bridge '+net)
    nodes=[n];tail=goals[n][1:]
    while prev[n] is not None:n=prev[n];nodes.append(n)
    nodes.reverse();layer=p.B_Cu;path=orig[n][:-1];segments=[];vias=[]
    for nn in nodes:
        if nn[2]!=layer:
            path.append(coord(nn));segments.append((layer,simplify(path,obs[layer])));vias.append(coord(nn));path=[coord(nn)];layer=nn[2]
        else:path.append(coord(nn))
    path+=tail;segments.append((layer,simplify(path,obs[layer])))
    assert all(math.dist(a,c)>=.8 for i,a in enumerate(vias) for c in vias[i+1:]),('Bridge vias too close',vias)
    for pt in vias:addvia(net,pt)
    for layer,path in segments:
        for a,c in zip(path,path[1:]):addtrack(net,a,c,layer)
        print('BRIDGE',net,b.GetLayerName(layer),path,flush=True)

# Remove the previous J2 routing and fanout vias, preserving the placed footprint.
for t in tracks():
    if t.m_Uuid.AsString() not in original_ids:b.Delete(t)
# Ground planes provide the redundant connections below. Remove paths that cross
# VCC or crowd the oscillator; neither component placement nor nets change.
for t in tracks():
    if isvia(t) or t.GetNetname()!='GND':continue
    a,c=xy(t.GetStart()),xy(t.GetEnd())
    if (t.GetLayer()==p.B_Cu and 106<a[1]<108 and 106<c[1]<108) or (a[0]==c[0]==121.92 and {a[1],c[1]}=={100.925,105.105}) or ({a,c}=={(104.9375,113.5),(102.8375,115.6)}):b.Delete(t)

# Move existing ground stitching vias away from every component pad. Their
# short spokes terminate on the refilled ground planes.
for v in list(tracks()):
    if not isvia(v) or v.GetNetname()!='GND':continue
    old=xy(v.GetPosition())
    hit=any(a.GetEffectiveShape(layer).Collide(v.GetPosition(),mm(.455)) for a in pads() for layer in [p.F_Cu,p.B_Cu] if a.IsOnLayer(layer))
    if not hit:continue
    candidates=[]
    for dx in range(-20,21):
        for dy in range(-20,21):
            pt=(round(old[0]+dx*.1,6),round(old[1]+dy*.1,6))
            candidates.append((math.hypot(dx,dy),pt))
    for _,pt in sorted(candidates):
        if via_safe('GND',pt,v):
            v.SetPosition(vec(pt));print('MOVE VIA',old,pt,flush=True);break
    else:raise RuntimeError('No via location '+str(old))

# Escape the ISP signals beyond the MCU pad ends, keeping the annulus clear.
targets={}
for net,x in [('PB1',113.6),('PB2',112.8),('PB3',112)]:
    pad=(x,112.3375)
    candidates=[]
    for y in [113.6,113.7,113.8,111.0,110.9,110.8]:
        for dx in [0,.1,-.1,.2,-.2,.3,-.3,.4,-.4,.5,-.5,.6,-.6]:
            pt=(round(x+dx,6),y)
            candidates.append((math.dist(pad,pt),pt))
    for _,pt in sorted(candidates):
        if not via_safe(net,pt):continue
        obs=obstacles(net,p.F_Cu)
        opts=[o for o in octpaths(pad,pt) if validpath(o,obs)]
        if not opts:continue
        for a,c in zip(opts[0],opts[0][1:]):addtrack(net,a,c,p.F_Cu)
        addvia(net,pt);targets[net]=pt;print('FANOUT',net,pt,flush=True);break
    else:raise RuntimeError('No fanout '+net)

# VCC and ground use remote vias with short traces from the pogo pads.
for net,candidates,anchor in [
    ('VCC',[(113.4,115.1825),(113.2,115.3825),(113.6,114.9825),(114.0,114.5825),(114.4,114.1825)],(115.2,113.3825)),
    ('GND',[(120.1,111.8),(119.8,111.8),(120.1,110.8),(122.8,112.6),(118.0,111.5)],None),
    ('RESET',[(109.0,113.3),(109.0,113.4),(109.0,113.2),(109.0,113.6)],(109.086,113.3))]:
    for pt in candidates:
        if not via_safe(net,pt):continue
        if anchor:
            opts=[o for o in octpaths(anchor,pt) if validpath(o,obstacles(net,p.F_Cu))]
            if not opts:continue
            for a,c in zip(opts[0],opts[0][1:]):addtrack(net,a,c,p.F_Cu)
        addvia(net,pt);targets[net]=pt;print('FANOUT',net,pt,flush=True);break
    else:raise RuntimeError('No remote via '+net)

def save(name):
    b.BuildConnectivity();p.ZONE_FILLER(b).Fill(b.Zones());p.SaveBoard(str(ROOT/name),b,True)
save('routing-45-stage.kicad_pcb')
j=next(f for f in b.GetFootprints() if f.GetReference()=='J2')
for net in ['PB3','PB1','PB2','RESET','VCC','GND']:
    a=next(a for a in j.Pads() if a.GetNetname()==net)
    if net=='PB2':route_bridge(net,xy(a.GetPosition()),targets[net])
    else:route(net,xy(a.GetPosition()),targets[net],p.B_Cu)
save('finished.kicad_pcb')
print('SAVED',flush=True)





