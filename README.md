# MicroKey
ATmega32U4-AU based micro controller with the sole purpose of emulating keyboard and mouse input. This project was made for Hack Club forge. The idea came to me when i was playing with my Esp32-S3 and thought the keyboard emulation with HID was cool, but the form factor of the Esp32 was too big and i also wanted to make my own devboard and thought this would be simple.

## Hardware
- ATmega32U4-AU
- Power Led
- User input Led
- USB C receptacle
- 16mhz Crystal
- Generic 2x3 header for bootloader

## Features
- HID emulation with the ATmega32U4-AU
- User input light

## Screenshots
<img width="1070" height="828" alt="image" src="https://github.com/user-attachments/assets/22445e1e-da64-4234-ac21-65aa100e095a" />
<img width="1133" height="828" alt="image" src="https://github.com/user-attachments/assets/441bcd1e-0bcd-4bbe-9117-377fcea1ce32" />


## BOM 
﻿<table>
  <thead>
    <tr>
      <th>Designator</th>
      <th>Footprint</th>
      <th>Quantity</th>
      <th>Value</th>
      <th>LCSC Part #</th>
      <th>Minimum Price</th>
      <th>LCSC Link</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>D1</td>
      <td>0805</td>
      <td>1</td>
      <td>RED</td>
      <td>C2295</td>
      <td>0.58$</td>
      <td><a href="https://www.lcsc.com/product-detail/C2295.html">C2295</a></td>
    </tr>
    <tr>
      <td>D2</td>
      <td>0805</td>
      <td>1</td>
      <td>BLUE</td>
      <td>C2293</td>
      <td>0.62$</td>
      <td><a href="https://www.lcsc.com/product-detail/C2293.html">C2293</a></td>
    </tr>
    <tr>
      <td>J1</td>
      <td>USB_C_Receptacle_GCT_USB4105-xx-A_16P_TopMnt_Horizontal</td>
      <td>1</td>
      <td>USB_C_Receptacle_USB2.0_16P</td>
      <td>C3020560</td>
      <td>1.31$</td>
      <td><a href="https://www.lcsc.com/product-detail/C3020560.html">C3020560</a></td>
    </tr>
    <tr>
      <td>J2</td>
      <td>PinHeader_2x03_P2.54mm_Vertical</td>
      <td>1</td>
      <td>Conn_02x03_Odd_Even</td>
      <td>C5116479</td>
      <td>0.60$</td>
      <td><a href="https://www.lcsc.com/product-detail/C5116479.html">C5116479</a></td>
    </tr>
    <tr>
      <td>R1, R2</td>
      <td>0805</td>
      <td>2</td>
      <td>5.1k</td>
      <td>C27834</td>
      <td>0.56$</td>
      <td><a href="https://www.lcsc.com/product-detail/C27834.html">C27834</a></td>
    </tr>
    <tr>
      <td>R3, R4</td>
      <td>0805</td>
      <td>2</td>
      <td>22</td>
      <td>C17561</td>
      <td>0.46$</td>
      <td><a href="https://www.lcsc.com/product-detail/C17561.html">C17561</a></td>
    </tr>
    <tr>
      <td>R5, R6, R7</td>
      <td>0805</td>
      <td>3</td>
      <td>1k</td>
      <td>C17513</td>
      <td>0.41$</td>
      <td><a href="https://www.lcsc.com/product-detail/C17513.html">C17513</a></td>
    </tr>
    <tr>
      <td>U1</td>
      <td>TQFP-44_10x10mm_P0.8mm</td>
      <td>1</td>
      <td>ATmega32U4-A</td>
      <td>C44854</td>
      <td>6.94$</td>
      <td><a href="https://www.lcsc.com/product-detail/C44854.html">C44854</a></td>
    </tr>
    <tr>
      <td>Y1</td>
      <td>Crystal_SMD_3225-4Pin_3.2x2.5mm</td>
      <td>1</td>
      <td>16mhz</td>
      <td>C70562</td>
      <td>0.55$</td>
      <td><a href="https://www.lcsc.com/product-detail/C70562.html">C70562</a></td>
    </tr>
  </tbody>
</table>
