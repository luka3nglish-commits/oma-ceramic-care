#!/usr/bin/env python
"""Print-ready ceramic-care business cards (front+back) + QR codes.
85x55mm @300dpi with 3mm bleed. All QR targets = the live care page."""
import os
from PIL import Image, ImageDraw, ImageFont
import qrcode
from qrcode.constants import ERROR_CORRECT_H
from qrcode.image.styledpil import StyledPilImage
from qrcode.image.styles.moduledrawers.pil import RoundedModuleDrawer
from qrcode.image.styles.colormasks import SolidFillColorMask
import cv2, numpy as np

URL="https://care.omaautodetailing.com.au"
ROOT=os.path.dirname(os.path.abspath(__file__))
OUT=os.path.join(ROOT,"qr"); os.makedirs(OUT,exist_ok=True)
A=os.path.join(ROOT,"assets"); LOGO=os.path.join(A,"logo.png"); MARBLE=os.path.join(A,"marble.jpg")
FD=r"C:\Users\luka3\OMA-stickers\fonts"
ANTON=os.path.join(FD,"Anton-Regular.ttf"); BAR_B=os.path.join(FD,"Barlow-Bold.ttf"); BAR_M=os.path.join(FD,"Barlow-Medium.ttf")
EM=(47,211,154); DARK=(6,9,8); WHITE=(244,248,246); MIST=(174,187,181)
det=cv2.QRCodeDetector(); DPI=300
def mm(x): return round(x/25.4*DPI)
BW,BH=mm(91),mm(61); TRIMX,TRIMY=mm(3),mm(3); TW,TH=mm(85),mm(55); SAFE=mm(4)
def font(f,s): return ImageFont.truetype(f,s)
def spaced(draw,txt,f,fill,y,cx,tr):
    ws=[]
    for ch in txt:
        bb=draw.textbbox((0,0),ch,font=f); ws.append(bb[2]-bb[0]+tr)
    tot=sum(ws)-tr; x=cx-tot//2
    for ch,w in zip(txt,ws): draw.text((x,y),ch,font=f,fill=fill); x+=w
def marble_bg(dk):
    m=Image.open(MARBLE).convert("RGB"); r=m.width/m.height; tr=BW/BH
    if r>tr: nw=int(m.height*tr); m=m.crop(((m.width-nw)//2,0,(m.width-nw)//2+nw,m.height))
    else: nh=int(m.width/tr); m=m.crop((0,(m.height-nh)//2,m.width,(m.height-nh)//2+nh))
    return Image.blend(m.resize((BW,BH),Image.LANCZOS),Image.new("RGB",(BW,BH),(0,0,0)),dk)
def chip(d):
    c=Image.new("RGBA",(d,d),(0,0,0,0)); cd=ImageDraw.Draw(c)
    cd.rounded_rectangle([0,0,d-1,d-1],radius=int(d*0.26),fill=DARK+(255,))
    cd.rounded_rectangle([1,1,d-2,d-2],radius=int(d*0.26),outline=EM+(230,),width=max(2,d//60))
    lg=Image.open(LOGO).convert("RGBA"); lw=int(d*0.66); lh=round(lg.height*lw/lg.width)
    c.alpha_composite(lg.resize((lw,lh),Image.LANCZOS),((d-lw)//2,(d-lh)//2)); return c
def qr_tile(size):
    qr=qrcode.QRCode(error_correction=ERROR_CORRECT_H,box_size=40,border=3); qr.add_data(URL); qr.make(fit=True)
    im=qr.make_image(image_factory=StyledPilImage,module_drawer=RoundedModuleDrawer(),
        color_mask=SolidFillColorMask(front_color=WHITE,back_color=DARK)).convert("RGBA").resize((size,size),Image.LANCZOS)
    d=int(size*0.19); im.alpha_composite(chip(d),((size-d)//2,(size-d)//2))
    pad=int(size*0.06); t=Image.new("RGBA",(size+2*pad,)*2,(0,0,0,0)); td=ImageDraw.Draw(t)
    td.rounded_rectangle([0,0,size+2*pad-1,size+2*pad-1],radius=int(size*0.09),fill=DARK+(255,),outline=EM+(150,),width=4)
    t.alpha_composite(im,(pad,pad)); return t
def bracket(dr,x,y,hx,hy,L,w): dr.line([(x,y),(x+hx*L,y)],fill=EM,width=w); dr.line([(x,y),(x,y+hy*L)],fill=EM,width=w)

# BACK
back=marble_bg(0.55).convert("RGBA"); dr=ImageDraw.Draw(back)
qsz=mm(40); tile=qr_tile(qsz); tx=TRIMX+SAFE+mm(1); ty=(BH-tile.height)//2
back.alpha_composite(tile,(tx,ty))
rcx=(tx+tile.width+mm(4)+(TRIMX+TW-SAFE))//2
spaced(dr,"SCAN FOR YOUR",font(BAR_B,28),EM,ty+mm(3),rcx,5)
af=font(ANTON,60)
for i,l in enumerate(["CERAMIC","CARE GUIDE"]):
    w=dr.textlength(l,font=af); dr.text((rcx-w/2,ty+mm(8)+i*60),l,font=af,fill=WHITE)
spaced(dr,"POINT YOUR CAMERA",font(BAR_M,22),MIST,ty+mm(8)+2*60+mm(3),rcx,2)
nf=font(ANTON,44); num="0490 793 033"; w=dr.textlength(num,font=nf); dr.text((rcx-w/2,ty+tile.height-mm(12)),num,font=nf,fill=WHITE)
spaced(dr,"@OMA.AUTODETAILING",font(BAR_B,20),EM,ty+tile.height-mm(4),rcx,3)
back.convert("RGB").save(os.path.join(OUT,"oma-card-BACK.png"),dpi=(DPI,DPI))

# FRONT (fixed layout)
front=marble_bg(0.42).convert("RGBA"); dr=ImageDraw.Draw(front); cx=BW//2
top=mm(6)+TRIMY; lg=Image.open(LOGO).convert("RGBA"); lw=mm(20); lh=round(lg.height*lw/lg.width)
front.alpha_composite(lg.resize((lw,lh),Image.LANCZOS),(cx-lw//2,top))
ey=top+lh+mm(2); spaced(dr,"CERAMIC COATED",font(BAR_B,26),EM,ey,cx,7)
hy=ey+mm(6); af=font(ANTON,64)
for i,l in enumerate(["AFTERCARE","GUIDE"]):
    w=dr.textlength(l,font=af); dr.text((cx-w/2,hy+i*62),l,font=af,fill=WHITE)
spaced(dr,"OMA AUTO DETAILING . LOCKYER VALLEY QLD",font(BAR_M,19),MIST,BH-TRIMY-mm(6),cx,1)
for x,y,hx,hy2 in [(TRIMX+SAFE,TRIMY+SAFE,1,1),(BW-TRIMX-SAFE,TRIMY+SAFE,-1,1),(TRIMX+SAFE,BH-TRIMY-SAFE,1,-1),(BW-TRIMX-SAFE,BH-TRIMY-SAFE,-1,-1)]:
    bracket(dr,x,y,hx,hy2,mm(5),4)
front.convert("RGB").save(os.path.join(OUT,"oma-card-FRONT.png"),dpi=(DPI,DPI))

# standalone QR
qr_tile(mm(50)).convert("RGB").save(os.path.join(OUT,"oma-qr-branded.png"))
sqr=qrcode.QRCode(error_correction=ERROR_CORRECT_H,box_size=40,border=4); sqr.add_data(URL); sqr.make(fit=True)
std=sqr.make_image(image_factory=StyledPilImage,module_drawer=RoundedModuleDrawer(),
    color_mask=SolidFillColorMask(front_color=(9,17,14),back_color=(255,255,255))).convert("RGBA")
sd=int(std.size[0]*0.18); std.alpha_composite(chip(sd),((std.size[0]-sd)//2,(std.size[1]-sd)//2))
std.convert("RGB").save(os.path.join(OUT,"oma-qr-standard.png"))

# preview + verify
def guide(im):
    im=im.copy(); d=ImageDraw.Draw(im); d.rectangle([TRIMX,TRIMY,BW-TRIMX,BH-TRIMY],outline=(255,80,110),width=2); return im
gap=40; prev=Image.new("RGB",(BW*2+gap,BH+96),(20,22,21)); pd=ImageDraw.Draw(prev)
prev.paste(guide(front.convert("RGB")),(0,60)); prev.paste(guide(back.convert("RGB")),(BW+gap,60))
lf=font(BAR_B,28); pd.text((10,18),"FRONT",font=lf,fill=(255,255,255)); pd.text((BW+gap+10,18),"BACK (QR)",font=lf,fill=(255,255,255))
pd.text((10,BH+66),"red line = trim (85x55mm). art bleeds past it. print double-sided.",font=font(BAR_M,20),fill=MIST)
prev.save(os.path.join(OUT,"oma-card-PREVIEW.png"))
def decode(im,inv=True):
    a=np.array(im.convert("RGB").resize((900,int(900*im.height/im.width)),Image.LANCZOS))[:,:,::-1].copy()
    if inv:a=255-a
    v,_,_=det.detectAndDecode(a); return v
rb=decode(back); rs=decode(std.convert("RGB"),inv=False)
print("QR",round(qsz/DPI*25.4,1),"mm | BACK:",repr(rb),"| STD:",repr(rs),"|","PASS" if rb==URL and rs==URL else "FAIL")
