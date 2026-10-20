import pcbnew as p
b=p.LoadBoard('USB_Keyboard_32U4.kicad_pcb');mm=p.FromMM
v=lambda x,y:p.VECTOR2I(mm(x),mm(y))
original_tracks=list(b.GetTracks())
for t in original_tracks:
 if t.GetNetname()=='GND' and t.GetClass()=='PCB_TRACK':b.RemoveNative(t)
 elif t.GetNetname()=='GND' and t.GetClass()=='PCB_VIA':
  if (t.GetPosition()-v(112.8375,111.05)).EuclideanNorm()<1000:t.SetPosition(v(112.8375,109.55))
  if (t.GetPosition()-v(108.9,121.9375)).EuclideanNorm()<1000:t.SetPosition(v(108.5,122.2))
 elif t.GetNetname()=='VCC' and t.GetClass()=='PCB_TRACK':
  for getter,setter in [(t.GetStart,t.SetStart),(t.GetEnd,t.SetEnd)]:
   pos=getter()
   if abs(p.ToMM(pos.y)-113.3825)<.001 and abs(p.ToMM(pos.x)-115.2)<.001 or abs(p.ToMM(pos.y)-113.3825)<.001 and abs(p.ToMM(pos.x)-119.2)<.001:setter(v(p.ToMM(pos.x),114.4))
def trace(pts):
 for a,c in zip(pts,pts[1:]):
  t=p.PCB_TRACK(b);t.SetStart(v(*a));t.SetEnd(v(*c));t.SetWidth(mm(.25));t.SetLayer(p.F_Cu);t.SetNetCode(b.FindNet('GND').GetNetCode());b.Add(t)
def via(x,y):
 vi=p.PCB_VIA(b);vi.SetPosition(v(x,y));vi.SetWidth(mm(.6));vi.SetDrill(mm(.3));vi.SetViaType(p.VIATYPE_THROUGH);vi.SetLayerPair(p.F_Cu,p.B_Cu);vi.SetNetCode(b.FindNet('GND').GetNetCode());b.Add(vi)
for pts in [[(122.6625,110.2),(123.2,110.7375)],[(112.8375,110.3),(112.8375,109.55)],[(106.1375,113.5),(105.5,112.8625)],[(111.9375,126),(111.9375,126.8)],[(125.3625,113.8),(125.3625,113.0)],[(125.3625,116.4),(126.1,116.4)],[(107.25,116.9),(107.25,117.7)],[(105.55,119.1),(104.7,119.1)],[(108.3625,121.4),(108.5,122.2)]]:trace(pts)
for pts in [[(116.8,112.3375),(116.8,113.8)],[(110.3375,116.4),(109.3,116.4)],[(112,123.6625),(112,124.9)],[(121.6625,114.8),(122.9,114.8)],[(121.6625,121.2),(122.9,121.2)]]:trace(pts);via(*pts[-1])
b.BuildConnectivity();p.ZONE_FILLER(b).Fill(b.Zones());p.SaveBoard('USB_Keyboard_32U4.kicad_pcb',b)
