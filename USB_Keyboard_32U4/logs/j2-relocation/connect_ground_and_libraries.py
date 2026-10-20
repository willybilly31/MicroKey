from pathlib import Path
src=Path(__file__).with_name('refine_routing.py').read_text().split('# Remove the previous J2 routing')[0]
exec(src)
b=p.LoadBoard(str(ROOT/'finished.kicad_pcb'))
# Restore the MCU ground escape and keep the ISP fanout on its left side.
for t in tracks():
    if t.GetNetname()=='PB2':
        if isvia(t):t.SetPosition(vec((115.0,109.0)))
        else:b.Delete(t)
addtrack('GND',(116.8,111.7209),(115.7367,110.6576),p.F_Cu)
addtrack('GND',(115.7367,110.6576),(115.7367,107.5331),p.F_Cu)
ACTIVE_CLEAR=.255
route('PB2',(112.8,112.3375),(115.0,109.0),p.F_Cu)
route('PB2',(119.485,116.25),(115.0,109.0),p.B_Cu)
lib=ROOT/'MicroKey_Local.pretty';lib.mkdir(exist_ok=True)
for ref,name in [('J1','USB4105_JLC_0p20mm_NPTH_Clearance'),('J2','AVR_ISP_2x3_Pogo_3p23x1p80')]:
    f=next(f for f in b.GetFootprints() if f.GetReference()==ref)
    f.SetFPID(p.LIB_ID('MicroKey_Local',name))
    cp=p.FOOTPRINT(f)
    if cp.GetLayer()==p.B_Cu:cp.Flip(cp.GetPosition(),p.FLIP_DIRECTION_LEFT_RIGHT)
    cp.SetOrientationDegrees(0);cp.SetPosition(vec((0,0)));cp.SetReference('REF**')
    p.PCB_IO_MGR.FindPlugin(p.PCB_IO_MGR.KICAD_SEXP).FootprintSave(str(lib),cp)
(ROOT/'fp-lib-table').write_text('(fp_lib_table\n  (version 7)\n  (lib (name "MicroKey_Local") (type "KiCad") (uri "${KIPRJMOD}/MicroKey_Local.pretty") (options "") (descr "MicroKey manufacturing-adjusted footprints"))\n)\n')
b.BuildConnectivity();p.ZONE_FILLER(b).Fill(b.Zones());p.SaveBoard(str(ROOT/'finished.kicad_pcb'),b,True)
print('SAVED',flush=True)

