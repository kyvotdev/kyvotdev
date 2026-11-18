from PIL import Image, ImageDraw, ImageFont
from pathlib import Path
import math
root = Path(__file__).resolve().parent
fontpath = '/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf'
def font(n): return ImageFont.truetype(fontpath,n)
frames=[]
commands=['> architect backend systems', '> craft frontend experiences', '> break assumptions. find vulnerabilities.']
for n in range(110):
    im=Image.new('RGB',(1200,420),'#050505'); d=ImageDraw.Draw(im)
    for x in range(0,1200,40): d.line((x,0,x,420),fill='#101010')
    for y in range(0,420,40): d.line((0,y,1200,y),fill='#101010')
    d.rounded_rectangle((28,24,1172,396),radius=16,fill='#090909',outline='#333333',width=1)
    d.line((28,66,1172,66),fill='#292929')
    for x,c in [(51,'#eeeeee'),(71,'#777777'),(91,'#333333')]: d.ellipse((x,41,x+8,49),fill=c)
    d.text((118,36),'SYSTEM / DEVELOPER PROFILE',font=font(13),fill='#888888')
    d.text((1030,36),'VOL. 001',font=font(13),fill='#888888')
    d.text((68,92),'BUILD. BREAK.',font=font(66),fill='#ffffff')
    d.text((68,172),'UNDERSTAND.',font=font(66),fill='#ffffff')
    index=min(n//34,2); t=n%34 if n<102 else 34
    line=commands[index][:int(t/24*len(commands[index]))]
    d.text((72,281),line+('▌' if n%12<7 else ''),font=font(21),fill='#bcbcbc')
    d.text((72,352),'BACKEND  /  FRONTEND  /  PENTEST',font=font(14),fill='#777777')
    for k in range(28):
        h=int(4+16*(.5+.5*math.sin(n*.22+k*.65)))
        d.rectangle((967+k*5,366-h,969+k*5,366),fill='#cccccc' if k%3==0 else '#555555')
    frames.append(im)
frames[0].save(root/'hero.gif',save_all=True,append_images=frames[1:],duration=65,loop=0,optimize=True)
