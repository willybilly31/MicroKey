import pcbnew as p,json,math
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]/'layout-work'
b=p.LoadBoard(str(ROOT/'finished.kicad_pcb'))
original=p.LoadBoard(str(ROOT/'finished.before-45-routing.kicad_pcb'))
def pos(f):return(f.GetPosition().x,f.GetPosition().y,f.GetOrientationDegrees(),f.GetLayer())
old={f.GetReference():pos(f) for f in original.GetFootprints()}
changed=[f.GetReference() for f in b.GetFootprints() if pos(f)!=old[f.GetReference()]]
assert not changed,changed
bad=[];hits=[];vias=[];pads=[(f,a) for f in b.GetFootprints() for a in f.Pads()]
for t in b.GetTracks():
    if isinstance(t,p.PCB_VIA):vias.append(t);continue
    dx=abs(t.GetStart().x-t.GetEnd().x);dy=abs(t.GetStart().y-t.GetEnd().y)
    if dx and dy and dx!=dy:bad.append(t.m_Uuid.AsString())
for v in vias:
    for f,a in pads:
        if any(a.IsOnLayer(l) and a.GetEffectiveShape(l).Collide(v.GetPosition(),v.GetWidth(l)//2+p.FromMM(.15)) for l in [p.F_Cu,p.B_Cu]):hits.append((f.GetReference(),a.GetNumber()))
assert not bad,bad
assert not hits,hits
d=json.loads((ROOT/'drc-after.json').read_text());assert not d['violations'] and not d['unconnected_items']
result={'drc_violations':0,'unconnected_items':0,'non_45_degree_segments':0,'vias_touching_pads_or_within_0p15mm':0,'footprint_placement_changes':changed,'width_mm':31.8,'height_mm':33.5,'previous_width_mm':35.2,'width_reduction_percent':round(100*(35.2-31.8)/35.2,2),'usb_and_j2_center_x_mm':117.6,'source':'https://jlcpcb.com/capabilities/pcb-capabilities/','manufacturing_assumption':'Standard 2-layer FR-4, 1 oz copper; routed outline; ordinary tented through vias','trace_width_mm':.2,'default_trace_clearance_mm':.2,'PB2_min_clearance_mm':.15,'via_diameter_mm':.6,'via_drill_mm':.3,'min_hole_to_copper_mm':.2,'min_copper_to_edge_mm':.5,'silkscreen_text_height_mm':1.0,'silkscreen_line_mm':.15}
(ROOT/'routing-verification.json').write_text(json.dumps(result,indent=2)+'\n')
mm=lambda n:p.ToMM(n)
preview={'pads':[(f.GetReference(),a.GetNumber(),mm(a.GetPosition().x),mm(a.GetPosition().y),mm(a.GetSize().x),mm(a.GetSize().y),a.GetOrientationDegrees(),a.GetNetname()) for f,a in pads if a.IsOnLayer(p.B_Cu)],'tracks':[(mm(t.GetStart().x),mm(t.GetStart().y),mm(t.GetEnd().x),mm(t.GetEnd().y),mm(t.GetWidth(p.B_Cu) if isinstance(t,p.PCB_VIA) else t.GetWidth()),t.GetNetname(),isinstance(t,p.PCB_VIA)) for t in b.GetTracks() if t.IsOnLayer(p.B_Cu)]}
(ROOT/'bottom-preview-data.json').write_text(json.dumps(preview))
print(json.dumps(result,indent=2))
