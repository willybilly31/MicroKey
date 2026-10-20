import pcbnew as p
from pathlib import Path
b=p.LoadBoard('layout-work/original.kicad_pcb')
mm=lambda x:p.FromMM(x)
v=lambda x,y:p.VECTOR2I(mm(x),mm(y))
fs={f.GetReference():f for f in b.GetFootprints()}
placements={
'U1':(116,118,-90),'J1':(117.6,102,180),'J2':(105,106,0),
'R3':(118.4,109.5,-90),'R4':(116.8,109.5,-90),
'R1':(121.2,107.5,0),'R2':(112,107.5,180),
'C3':(121.8,110.2,0),'C8':(113.7,110.3,180),
'C6':(124.5,113.8,0),'C9':(124.5,116.4,0),
'C5':(112.8,126,180),'C4':(107,113.5,180),
'C7':(125,105.5,-90),'R7':(107.6,111.8,0),
'Y1':(106.4,118,90),'C1':(107.5,121.4,180),'C2':(103.7,115.6,0),
'R5':(128.2,111,-90),'D1':(128.2,114.5,90),
'R6':(105,123.5,-90),'D2':(105,127,90)}
# C10 does not exist; C3-C6 bypass the four MCU supply groups.
for ref,(x,y,a) in placements.items():
 f=fs[ref];f.SetPosition(v(x,y));f.SetOrientationDegrees(a)
 f.Value().SetVisible(False)
 t=f.Reference();t.SetTextSize(v(.8,.8));t.SetTextThickness(mm(.12));t.SetTextAngle(p.EDA_ANGLE(0,p.DEGREES_T));t.SetPosition(v(x+1.5,y) if abs(a)==90 else v(x,y-1.3));t.SetVisible(True)
fs['U1'].Reference().SetPosition(v(116,118))
fs['J1'].Reference().SetPosition(v(110.5,100.8))
fs['J2'].Reference().SetPosition(v(105,101.5))
fs['R3'].Reference().SetPosition(v(119.9,109))
fs['R4'].Reference().SetPosition(v(116.8,107.5))
fs['Y1'].Reference().SetPosition(v(104,118.8))
fs['C1'].Reference().SetPosition(v(108.1,122.8))
fs['C4'].Reference().SetPosition(v(107,114.8))
fs['C5'].Reference().SetPosition(v(112.8,127.3))
fs['R1'].Reference().SetPosition(v(121.4,108.8))
# Preserve footprints and their net assignments; discard only degenerate drawing.
for d in list(b.GetDrawings()):b.Remove(d)
for a,c in [((100,99.5),(131,99.5)),((131,99.5),(131,133)),((131,133),(100,133)),((100,133),(100,99.5))]:
 s=p.PCB_SHAPE();s.SetShape(p.SHAPE_T_SEGMENT);s.SetStart(v(*a));s.SetEnd(v(*c));s.SetLayer(p.Edge_Cuts);s.SetWidth(mm(.05));b.Add(s)
settings=b.GetDesignSettings();settings.m_TrackMinWidth=mm(.15);settings.m_MinClearance=mm(.15);settings.m_ViasMinSize=mm(.6);settings.m_MinThroughDrill=mm(.3)
p.SaveBoard('layout-work/placed.kicad_pcb',b)
p.ExportSpecctraDSN(b,'layout-work/placed.dsn')
# Explicitly route USB and oscillator before the general router.
def pad(ref,num):return next(x for x in fs[ref].Pads() if x.GetNumber()==str(num))
def xy(pa):return (p.ToMM(pa.GetPosition().x),p.ToMM(pa.GetPosition().y))
def trace(net,points,width=.2,layer=p.F_Cu):
 for a,c in zip(points,points[1:]):
  if a==c:continue
  t=p.PCB_TRACK(b);t.SetStart(v(*a));t.SetEnd(v(*c));t.SetWidth(mm(width));t.SetLayer(layer);t.SetNetCode(b.FindNet(net).GetNetCode());t.SetLocked(True);b.Add(t)
def link(ref,num,ref2,num2,mid=[]):
 pa=pad(ref,num);pb=pad(ref2,num2);assert pa.GetNetCode()==pb.GetNetCode()
 trace(pa.GetNetname(),[xy(pa)]+mid+[xy(pb)])
link('J1','A6','J1','B6',[(117.85,104.7),(116.85,104.7)])
link('J1','A7','J1','B7',[(117.35,106.65),(118.35,106.65)])
link('J1','B6','R4','1',[(116.85,108.5375)])
link('J1','B7','R3','1',[(118.35,108.5375)])
link('R3','2','U1','3')
link('R4','2','U1','4',[(116.8,110.7),(117.6,111.5)])
link('U1','16','Y1','3',[(109.4,117.2),(108,115.8),(106.65,115.8),(105.55,116.9)])
link('Y1','3','C2','2',[(104.5625,115.9125)])
link('U1','17','Y1','1',[(108.35,118),(107.25,119.1)])
link('Y1','1','C1','2',[(107.25,120.7875)])
# Decoupling and UCAP connections are short local traces.
link('U1','6','C8','1',[(116,111.625),(114.675,110.3)])
link('U1','14','C4','1',[(109.1,115.6),(109.1,114.7375)])
link('U1','24','C5','1',[(112.8,125.1375)])
link('U1','44','C6','1',[(123.4375,114)])
link('U1','42','C9','1',[(122.8,115.6),(123.6,116.4)])
link('U1','2','C3','1',[(119.2,111.2),(120.2,110.2)])
p.SaveBoard('layout-work/placed.kicad_pcb',b)
p.ExportSpecctraDSN(b,'layout-work/placed.dsn')

import json
j=json.load(open("USB_Keyboard_32U4.kicad_pro"))
j["board"]["design_settings"]["rules"]["min_hole_clearance"]=.15
j["board"]["design_settings"]["rules"]["min_clearance"]=.15
Path("layout-work/placed.kicad_pro").write_text(json.dumps(j,indent=2)+"\n")
