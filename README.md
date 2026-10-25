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
<img width="400" height="" alt="image" src="https://github.com/user-attachments/assets/8937f32b-8cab-42db-bf8b-957710ce60cd" /> <img width="400" height="" alt="image" src="https://github.com/user-attachments/assets/b14e7902-8f1f-4ab5-bcbf-9a17d45cb079" />



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
      <td>C1, C2</td>
      <td>0603</td>
      <td>2</td>
      <td>27pF</td>
      <td>C1656</td>
      <td>0.60$</td>
      <td><a href="https://www.lcsc.com/product-detail/C1656.html">C1656</a></td>
    </tr>
    <tr>
      <td>C10, C3, C4, C5, C6, C9</td>
      <td>0603</td>
      <td>6</td>
      <td>100nF</td>
      <td>C1591</td>
      <td>0.28$</td>
      <td><a href="https://www.lcsc.com/product-detail/C1591.html">C1591</a></td>
    </tr>
    <tr>
      <td>C7</td>
      <td>0603</td>
      <td>1</td>
      <td>10uF</td>
      <td>C19702</td>
      <td>0.40$</td>
      <td><a href="https://www.lcsc.com/product-detail/C19702.html">C19702</a></td>
    </tr>
    <tr>
      <td>C8</td>
      <td>0603</td>
      <td>1</td>
      <td>1uF</td>
      <td>C15849</td>
      <td>0.87$</td>
      <td><a href="https://www.lcsc.com/product-detail/C15849.html">C15849</a></td>
    </tr>
    <tr>
      <td>D1</td>
      <td>0603</td>
      <td>1</td>
      <td>RED</td>
      <td>C2286</td>
      <td>0.0076$</td>
      <td><a href="https://www.lcsc.com/product-detail/C2286.html">C2286</a></td>
    </tr>
    <tr>
      <td>D2</td>
      <td>0603</td>
      <td>1</td>
      <td>BLUE</td>
      <td>C965807</td>
      <td>0.0043$</td>
      <td><a href="https://www.lcsc.com/product-detail/C965807.html">C965807</a></td>
    </tr>
    <tr>
      <td>J1</td>
      <td>GCT_USB4105-GF-A</td>
      <td>1</td>
      <td>USB_C_Receptacle_USB2.0_16P</td>
      <td>C3020560</td>
      <td>1.31$</td>
      <td><a href="https://www.lcsc.com/product-detail/C3020560.html">C3020560</a></td>
    </tr>
    <tr>
      <td>J2</td>
      <td>AVR_ISP_2x3_Pogo_3p23x1p80</td>
      <td>1</td>
      <td>Conn_02x03_Odd_Even</td>
      <td></td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <td>R1, R2</td>
      <td>0603</td>
      <td>2</td>
      <td>5.1k</td>
      <td>C23186</td>
      <td>0.12$</td>
      <td><a href="https://www.lcsc.com/product-detail/C23186.html">C23186</a></td>
    </tr>
    <tr>
      <td>R3, R4</td>
      <td>0603</td>
      <td>2</td>
      <td>22</td>
      <td>C23345</td>
      <td>0.0018$</td>
      <td><a href="https://www.lcsc.com/product-detail/C23345.html">C23345</a></td>
    </tr>
    <tr>
      <td>R5, R6</td>
      <td>0603</td>
      <td>2</td>
      <td>1k</td>
      <td>C21190</td>
      <td>0.06$</td>
      <td><a href="https://www.lcsc.com/product-detail/C21190.html">C21190</a></td>
    </tr>
    <tr>
      <td>R7, R8</td>
      <td>0603</td>
      <td>2</td>
      <td>10k</td>
      <td>C25804</td>
      <td>0.09$</td>
      <td><a href="https://www.lcsc.com/product-detail/C25804.html">C25804</a></td>
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
      <td>16MHz</td>
      <td>C70562</td>
      <td>0.55$</td>
      <td><a href="https://www.lcsc.com/product-detail/C70562.html">C70562</a></td>
    </tr>
  </tbody>
</table>

