# USB Keyboard 32U4 PCB layout

Updated the main `USB_Keyboard_32U4.kicad_pcb` using all 22 original footprints and the existing schematic connectivity.

- Two copper layers; rectangular outline: **31 × 33.5 mm**.
- USB-C faces out of the upper board edge. Programming pads remain accessible on the upper left.
- Crystal and its load capacitors sit beside XTAL1/XTAL2. USB series resistors, UCAP capacitor, AREF capacitor and supply bypass capacitors sit near their MCU pins.
- USB data and crystal connections are routed on the front without vias. The remaining connections are routed, with ground pours on both sides and local ground stitching near the MCU and capacitors.
- A roughly 29 × 3 mm band below the components, plus a larger lower-right region, remains available for silkscreen artwork. Small tented stitching vias remain near the board perimeter.
- Programming pads are numbered on the front. Their existing, custom pin mapping is **1 GND, 2 VCC, 3 MOSI/PB2, 4 MISO/PB3, 5 SCK/PB1, 6 RESET**. This differs from conventional AVR ISP header numbering; use the schematic mapping when making a cable or fixture.

## Validation

KiCad 10.0.6 DRC with schematic parity enabled:

- **0 DRC violations** (errors and warnings)
- **0 unconnected items**
- **0 schematic-parity issues**

See `final-drc.rpt`. An independent pin/net comparison also matched all **107 unique PCB pads** to the schematic (`netlist-check.txt`). No DRC exclusions were added. The project retains its existing ignored checks, listed in the report.

Routing uses 0.20 mm signal tracks, with some 0.25–0.30 mm ground/power connections and 0.60 / 0.30 mm through vias. Net-class clearance remains 0.20 mm. The board-wide minimum copper clearance is now 0.15 mm. Minimum copper-to-hole clearance is 0.15 mm because the existing USB-C footprint has approximately 0.194 mm clearance between its locating holes and adjacent pads; the former 0.25 mm rule rejected the footprint itself. Confirm these dimensions with the board fabricator. USB controlled impedance was not verified against a fabrication stackup.

## Existing schematic findings

The schematic was not changed. Its ERC report (`erc.rpt`) contains **26 errors and 11 warnings**: 24 unconnected-pin markers are missing, two power inputs lack an ERC power-output declaration, and there are library/off-grid warnings. PCB DRC passing does not resolve these schematic findings or establish circuit functionality. In particular, the supplied schematic has unused GPIOs and no keyboard switch matrix; this layout implements the supplied controller circuit.

The existing four 100 nF supply capacitors and 27 pF crystal capacitors were retained. Validate the bypass requirements of all MCU supply pins and the crystal's specified load capacitance as part of the circuit review before fabrication.

## Files

- Main edited board: `../USB_Keyboard_32U4.kicad_pcb`
- Updated design rules: `../USB_Keyboard_32U4.kicad_pro`
- Board preview: `board-top.png`
- Original board backup: `original.kicad_pcb`
- Original project backup: `original.kicad_pro`
- Intermediate routing files and scripts are retained here for inspection.

Existing Gerber, drill and production files predate this layout and were **not regenerated**. Export a fresh fabrication set from the updated board after the circuit review and your silkscreen additions.
