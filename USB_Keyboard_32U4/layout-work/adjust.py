import pcbnew as p
b=p.LoadBoard('layout-work/finished.kicad_pcb');mm=p.FromMM
v=lambda x,y:p.VECTOR2I(mm(x),mm(y))
f=next(f for f in b.GetFootprints() if f.GetReference()=='C2')
old=[(pa.GetPosition(),pa.GetNetCode()) for pa in f.Pads()]
f.SetPosition(v(103.7,115.05));f.Reference().SetPosition(v(103.2,113.7))
for (pos,net),pa in zip(old,f.Pads()):
 t=p.PCB_TRACK(b);t.SetStart(pos);t.SetEnd(pa.GetPosition());t.SetWidth(mm(.2));t.SetLayer(p.F_Cu);t.SetNetCode(net);b.Add(t)
for f in b.GetFootprints():
 if f.GetReference()=='C3':f.Reference().SetPosition(v(123.9,110.1))
b.BuildConnectivity();p.ZONE_FILLER(b).Fill(b.Zones());p.SaveBoard('layout-work/finished.kicad_pcb',b)
