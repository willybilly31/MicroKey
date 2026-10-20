import json,math
from PIL import Image,ImageDraw
from pathlib import Path
r=Path(__file__).resolve().parents[2]/'layout-work'
d=json.loads((r/'bottom-preview-data.json').read_text())
im=Image.new('RGB',(1100,1100),'#111b26');draw=ImageDraw.Draw(im)
def pt(x,y):return((x-98)*27,(y-96)*27)
draw.rectangle([pt(101.7,99.5),pt(133.5,133)],outline='white',width=3)
colors={'GND':'#568eaf','VCC':'#ed776b','PB1':'#dc9f4d','PB2':'#b7de71','PB3':'#66dbb6','RESET':'#c18ced'}
for x,y,x1,y1,w,net,via in d['tracks']:
    c=colors.get(net,'#5a718c')
    if via:
        a,b=pt(x,y); draw.ellipse((a-w*13.5,b-w*13.5,a+w*13.5,b+w*13.5),fill=c);draw.ellipse((a-3,b-3,a+3,b+3),fill='#111b26')
    else: draw.line([pt(x,y),pt(x1,y1)],fill=c,width=max(2,round(w*27)))
for ref,num,x,y,w,h,ang,net in d['pads']:
    theta=math.radians(-ang)
    pts=[pt(x+u*math.cos(theta)-v*math.sin(theta),y+u*math.sin(theta)+v*math.cos(theta)) for u,v in [(-w/2,-h/2),(w/2,-h/2),(w/2,h/2),(-w/2,h/2)]]
    draw.polygon(pts,fill=colors.get(net,'#5a718c'))
    if ref=='J2':draw.text(pt(x-1.0,y-.2),f'{num} {net}',fill='black')
draw.text((55,30),'BOTTOM COPPER — viewed through board from front',fill='white')
draw.text((55,1060),'J2 centered at (117.60, 116.25) mm | Outline 31.80 x 33.50 mm',fill='white')
im.save(r/'finished-bottom-preview.png')

