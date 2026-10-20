from pathlib import Path
src=Path(__file__).with_name('refine_routing.py').read_text()
prefix=src.split('# Remove the previous J2 routing')[0]
# Coarser search for the layer crossing reduces search cost in open space.
head,bridge=prefix.split('def route_bridge')
bridge=bridge.replace('n[0]/10,n[1]/10','n[0]/5,n[1]/5').replace('pt[0]*10','pt[0]*5').replace('pt[1]*10','pt[1]*5').replace('end[0]*10','end[0]*5').replace('end[1]*10','end[1]*5').replace('math.dist(a,c)*10','math.dist(a,c)*5').replace('1008<=nn[0]<=1344 and 1003<=nn[1]<=1322','504<=nn[0]<=672 and 502<=nn[1]<=661').replace('n[0]%2==0 and n[1]%2==0 and vf(n)','vf(n)')
exec(head+'def route_bridge'+bridge)
b=p.LoadBoard(str(ROOT/'routing-45-stage.kicad_pcb'))
targets={'PB1':(113.5,113.6),'PB2':(115.7,110.5),'PB3':(111.7,113.6),'VCC':(114.4401,107.0874),'GND':(122.8,112.6),'RESET':(109.0,113.3)}
v=next(t for t in tracks() if isvia(t) and t.GetNetname()=='PB2')
v.SetPosition(vec(targets['PB2']))
for t in tracks():
    if not isvia(t) and t.GetNetname()=='PB2' and t.GetLayer()==p.F_Cu:b.Delete(t)
    elif not isvia(t) and t.GetNetname()=='GND' and {xy(t.GetStart()),xy(t.GetEnd())}=={(112.8375,110.3),(112.8375,111.05)}:b.Delete(t)
    elif t.GetNetname()=='VCC' and (xy(t.GetStart())==(113.4,115.1825) or xy(t.GetEnd())==(113.4,115.1825)):b.Delete(t)
    elif not isvia(t) and t.GetNetname()=='GND' and t.GetLayer()==p.F_Cu and (xy(t.GetStart())==(115.7367,110.6576) or xy(t.GetEnd())==(115.7367,110.6576)):b.Delete(t)
ACTIVE_CLEAR=.255
route('PB2',(112.8,112.3375),targets['PB2'],p.F_Cu)
j=next(f for f in b.GetFootprints() if f.GetReference()=='J2')
for net in ['VCC','PB3','PB1','PB2','RESET','GND']:
    a=next(a for a in j.Pads() if a.GetNetname()==net)
    ACTIVE_CLEAR=.255 if net=='PB2' else .305
    route(net,xy(a.GetPosition()),targets[net],p.B_Cu)
    p.SaveBoard(str(ROOT/'routing-45-progress.kicad_pcb'),b,True)
b.BuildConnectivity();p.ZONE_FILLER(b).Fill(b.Zones());p.SaveBoard(str(ROOT/'finished.kicad_pcb'),b,True)
print('SAVED',flush=True)
