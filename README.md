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
<img width="500" height="" alt="image" src="https://github.com/user-attachments/assets/c7c7facc-7d9c-47f0-a5b0-10e1efadb59c" />
<img width="500" height="" alt="image" src="https://github.com/user-attachments/assets/7300a48d-b9ca-4baf-92b3-cf4c0949bc4e" />

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
    </tr>
    <tr>
      <td>D2</td>
      <td>0805</td>
      <td>1</td>
      <td>BLUE</td>
      <td>C2293</td>
      <td>0.62$</td>
    </tr>
    <tr>
      <td>J1</td>
      <td>USB_C_Receptacle_GCT_USB4105-xx-A_16P_TopMnt_Horizontal</td>
      <td>1</td>
      <td>USB_C_Receptacle_USB2.0_16P</td>
      <td>C3020560</td>
      <td>1.31$</td>
    </tr>
    <tr>
      <td>J2</td>
      <td>PinHeader_2x03_P2.54mm_Vertical</td>
      <td>1</td>
      <td>Conn_02x03_Odd_Even</td>
      <td>C5116479</td>
      <td>0.60$</td>
    </tr>
    <tr>
      <td>R1, R2</td>
      <td>0805</td>
      <td>2</td>
      <td>5.1k</td>
      <td>C27834</td>
      <td>0.56$</td>
    </tr>
    <tr>
      <td>R3, R4</td>
      <td>0805</td>
      <td>2</td>
      <td>22</td>
      <td>C17561</td>
      <td>0.46$</td>
    </tr>
    <tr>
      <td>R5, R6, R7</td>
      <td>0805</td>
      <td>3</td>
      <td>1k</td>
      <td>C17513</td>
      <td>0.41$</td>
    </tr>
    <tr>
      <td>U1</td>
      <td>TQFP-44_10x10mm_P0.8mm</td>
      <td>1</td>
      <td>ATmega32U4-A</td>
      <td>C44854</td>
      <td>6.94$</td>
    </tr>
    <tr>
      <td>Y1</td>
      <td>Crystal_SMD_3225-4Pin_3.2x2.5mm</td>
      <td>1</td>
      <td>16mhz</td>
      <td>C70562</td>
      <td>0.55$</td>
    </tr>
  </tbody>
</table>
