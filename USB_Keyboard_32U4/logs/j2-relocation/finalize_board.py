import pcbnew as p,json,math
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]/'layout-work'
path=ROOT/'finished.kicad_pcb'
b=p.LoadBoard(str(path));mm=p.FromMM
def vec(x,y):return p.VECTOR2I(mm(x),mm(y))
def xy(v):return(round(p.ToMM(v.x),6),round(p.ToMM(v.y),6))
for d in b.GetDrawings():
    if d.GetLayer()!=p.Edge_Cuts:continue
    for setter,getter in [(d.SetStart,d.GetStart),(d.SetEnd,d.GetEnd)]:
        x,y=xy(getter());setter(vec(101.7 if x==100 else 133.5 if x==135.2 else x,y))
for t in b.GetTracks():
    if isinstance(t,p.PCB_VIA) and t.GetPosition().x==mm(101.2):t.SetPosition(vec(102.65,p.ToMM(t.GetPosition().y)))
# Make reference lettering meet the fabricator's legibility guidance.
for f in b.GetFootprints():
    ref=f.Reference();ref.SetTextSize(vec(1,1));ref.SetTextThickness(mm(.15))
    for g in f.GraphicalItems():
        if isinstance(g,p.PCB_SHAPE) and g.GetLayer() in [p.F_SilkS,p.B_SilkS] and g.GetWidth()<mm(.15):g.SetWidth(mm(.15))
b.BuildConnectivity();p.ZONE_FILLER(b).Fill(b.Zones());p.SaveBoard(str(path),b,True)
# Keep existing net clearances and conservative board-edge clearance, strengthen
# the explicit manufacturing minima without using premium via processing.
pro=ROOT/'finished.kicad_pro';data=json.loads(pro.read_text());rules=data['board']['design_settings']['rules']
rules.update(min_hole_clearance=.2,min_hole_to_hole=.25,min_via_annular_width=.15,min_via_diameter=.6,min_through_hole_diameter=.3,min_silk_clearance=.15,min_text_height=1.0,min_text_thickness=.15)
pro.write_text(json.dumps(data,indent=2)+'\n')
print('Narrowed to 31.8 x 33.5 mm; USB and J2 center X=117.6',flush=True)
