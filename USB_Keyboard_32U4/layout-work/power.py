import pcbnew as p
b=p.LoadBoard('layout-work/finished.kicad_pcb');mm=p.FromMM
v=lambda x,y:p.VECTOR2I(mm(x),mm(y))
def trace(net,pts,w=.3,layer=p.F_Cu):
 for a,c in zip(pts,pts[1:]):
  t=p.PCB_TRACK(b);t.SetStart(v(*a));t.SetEnd(v(*c));t.SetWidth(mm(w));t.SetLayer(layer);t.SetNetCode(b.FindNet(net).GetNetCode());b.Add(t)
def via(net,x,y):
 vi=p.PCB_VIA(b);vi.SetPosition(v(x,y));vi.SetWidth(mm(.6));vi.SetDrill(mm(.3));vi.SetViaType(p.VIATYPE_THROUGH);vi.SetLayerPair(p.F_Cu,p.B_Cu);vi.SetNetCode(b.FindNet(net).GetNetCode());b.Add(vi)
trace('VCC',[(120,105.68),(120,105.15),(119.6,104.75),(119.6,103.4),(123.7625,103.4),(125,104.6375)],.2)
via('VCC',119.6,104.4)
trace('VCC',[(114.4401,107.0874),(117.1275,104.4),(119.6,104.4)],.3,p.B_Cu)
# Solid connection on the USB ground pads avoids tiny, starved thermal spokes.
for f in b.GetFootprints():
 if f.GetReference()=='J1':
  for pa in f.Pads():
   if pa.GetNetname()=='GND' and pa.GetNumber()!='SH':pa.SetLocalZoneConnection(p.ZONE_CONNECTION_FULL)
# Short connections from local ground pads to the rear ground plane.
for pts in [[(122.6625,110.2),(123.2,110.7375)],[(112.8375,110.3),(112.8375,111.05)],[(106.1375,113.5),(105.5,112.8625)],[(111.9375,126),(111.9375,126.8)],[(125.3625,113.8),(125.3625,113.0)],[(125.3625,116.4),(126.1,116.4)],[(107.25,116.9),(107.25,117.7)],[(105.55,119.1),(104.7,119.1)],[(108.3625,121.4),(108.9,121.9375)]]:
 trace('GND',pts,.25);via('GND',*pts[-1])
b.BuildConnectivity();p.ZONE_FILLER(b).Fill(b.Zones());p.SaveBoard('layout-work/finished.kicad_pcb',b)
