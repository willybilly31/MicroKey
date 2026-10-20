import pcbnew as p
b=p.LoadBoard('USB_Keyboard_32U4.kicad_pcb');mm=p.FromMM
v=lambda x,y:p.VECTOR2I(mm(x),mm(y))
for t in b.GetTracks():
 if t.GetNetname()!='GND':continue
 for getter,setter in [(t.GetStart,t.SetStart),(t.GetEnd,t.SetEnd)]:
  po=getter()
  for a,c in [((122.9,121.2),(122.7,121.2)),((109.3,116.4),(109.4,116.3))]:
   if (po-v(*a)).EuclideanNorm()<1000:setter(v(*c))
for f in b.GetFootprints():
 if f.GetReference()=='R1':f.Reference().SetPosition(v(123.4,107.5))
# Identify the custom programming pad numbering without using the artwork strip.
for n,x,y in [(1,100.8,103.46),(2,109.3,103.46),(3,100.8,106),(4,109.3,106),(5,100.8,108.54),(6,109.3,108.54)]:
 t=p.PCB_TEXT(b);t.SetText(str(n));t.SetPosition(v(x,y));t.SetTextSize(v(.8,.8));t.SetTextThickness(mm(.12));t.SetLayer(p.F_SilkS);b.Add(t)
b.BuildConnectivity();p.ZONE_FILLER(b).Fill(b.Zones());p.SaveBoard('USB_Keyboard_32U4.kicad_pcb',b)
