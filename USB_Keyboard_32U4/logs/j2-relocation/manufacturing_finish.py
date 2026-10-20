import pcbnew as p,json,math
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]/'layout-work'
b=p.LoadBoard(str(ROOT/'finished.kicad_pcb'));mm=p.FromMM
def vec(x,y):return p.VECTOR2I(mm(x),mm(y))
def xy(v):return(round(p.ToMM(v.x),6),round(p.ToMM(v.y),6))
# Give the USB locating holes a full 0.20 mm copper clearance. Only the four
# overlapping ground contact pad ends change, by 0.01 mm at each end.
usb=next(f for f in b.GetFootprints() if f.GetReference()=='J1')
for a in usb.Pads():
    if a.GetNumber() in ['A1','B12','A12','B1']:a.SetSize(vec(.6,1.13))
for z in b.Zones():z.SetIslandRemovalMode(p.ISLAND_REMOVAL_MODE_ALWAYS)
# Normalize three old diagonal segments whose endpoints differ by 0.1 micron.
for t in list(b.GetTracks()):
    if isinstance(t,p.PCB_VIA):continue
    a,c=xy(t.GetStart()),xy(t.GetEnd());dx=t.GetEnd().x-t.GetStart().x;dy=t.GetEnd().y-t.GetStart().y
    if not(dx and dy and abs(dx)!=abs(dy)):continue
    delta=min(abs(dx),abs(dy));mid=((t.GetStart().x+(delta if dx>0 else -delta))/1e6,(t.GetStart().y+(delta if dy>0 else -delta))/1e6)
    for start,end in [(a,mid),(mid,c)]:
        nt=p.PCB_TRACK(b);nt.SetStart(vec(*start));nt.SetEnd(vec(*end));nt.SetWidth(t.GetWidth());nt.SetLayer(t.GetLayer());nt.SetNetCode(t.GetNetCode());b.Add(nt)
    b.Delete(t)

def bounds(box):return(box.GetLeft(),box.GetTop(),box.GetRight(),box.GetBottom())
def overlap(a,c,margin=0):return not(a[2]+margin<c[0] or c[2]+margin<a[0] or a[3]+margin<c[1] or c[3]+margin<a[1])
fields=[f.Reference() for f in b.GetFootprints() if f.Reference().IsVisible()]
for ref in fields:
    if ref.GetLayer() not in [p.F_SilkS,p.B_SilkS]:continue
    layer=ref.GetLayer();copper=p.F_Cu if layer==p.F_SilkS else p.B_Cu
    fixed=[]
    for f in b.GetFootprints():
        for a in f.Pads():
            if a.IsOnLayer(copper):fixed.append(bounds(a.GetBoundingBox()))
        for g in f.GraphicalItems():
            if g.GetLayer()==layer:fixed.append(bounds(g.GetBoundingBox()))
    others=[bounds(r.GetBoundingBox()) for r in fields if r!=ref and r.GetLayer()==layer]
    old=xy(ref.GetPosition());angle=ref.GetTextAngle().AsDegrees()
    candidates=[]
    for dx in range(-60,61):
        for dy in range(-60,61):
            for rotate in [0,90]:candidates.append((math.hypot(dx,dy)+rotate/90*2,dx,dy,rotate))
    found=False
    for _,dx,dy,rotate in sorted(candidates):
        ref.SetPosition(vec(old[0]+dx*.1,old[1]+dy*.1));ref.SetTextAngle(p.EDA_ANGLE(angle+rotate,p.DEGREES_T));ref.ClearBoundingBoxCache();box=bounds(ref.GetBoundingBox())
        if box[0]<mm(101.9) or box[2]>mm(133.3) or box[1]<mm(99.7) or box[3]>mm(132.8):continue
        if any(overlap(box,c,mm(.17)) for c in fixed+others):continue
        found=True;break
    if not found:raise RuntimeError('No silkscreen position '+ref.GetText())
    print('LABEL',ref.GetText(),old,xy(ref.GetPosition()),flush=True)
b.BuildConnectivity();p.ZONE_FILLER(b).Fill(b.Zones());p.SaveBoard(str(ROOT/'finished.kicad_pcb'),b,True)
print('SAVED',flush=True)

