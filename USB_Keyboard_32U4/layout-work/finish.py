import pcbnew as p
import sys,json
from pathlib import Path
b=p.LoadBoard('layout-work/placed.kicad_pcb')
mm=p.FromMM
v=lambda x,y:p.VECTOR2I(mm(x),mm(y))
if not p.ImportSpecctraSES(b,sys.argv[1]):raise RuntimeError('SES import failed')
print('Imported tracks:',len(list(b.GetTracks())))
for layer in [p.F_Cu,p.B_Cu]:
 z=p.ZONE(b);z.SetLayer(layer);z.SetNetCode(b.FindNet('GND').GetNetCode());z.SetLocalClearance(mm(.2));z.SetMinThickness(mm(.2));z.SetThermalReliefGap(mm(.25));z.SetThermalReliefSpokeWidth(mm(.25));z.SetPadConnection(p.ZONE_CONNECTION_THERMAL);z.SetIslandRemovalMode(p.ISLAND_REMOVAL_MODE_ALWAYS)
 outline=z.Outline();outline.NewOutline()
 for x,y in [(100.5,100),(130.5,100),(130.5,132.5),(100.5,132.5)]:outline.Append(mm(x),mm(y))
 b.Add(z)
# Ground stitching at perimeter and beside sensitive supply/clock ground returns.
for x,y in [(101.2,101.2),(129.8,101.2),(101.2,131.8),(129.8,131.8),(115,131.8),(129.8,119),(101.2,119)]:
 vi=p.PCB_VIA(b);vi.SetPosition(v(x,y));vi.SetWidth(mm(.6));vi.SetDrill(mm(.3));vi.SetViaType(p.VIATYPE_THROUGH);vi.SetLayerPair(p.F_Cu,p.B_Cu);vi.SetNetCode(b.FindNet('GND').GetNetCode());b.Add(vi)
b.BuildConnectivity();p.ZONE_FILLER(b).Fill(b.Zones())
p.SaveBoard('layout-work/finished.kicad_pcb',b)
Path('layout-work/finished.kicad_pro').write_text(Path('layout-work/placed.kicad_pro').read_text())
print('Saved finished PCB')
