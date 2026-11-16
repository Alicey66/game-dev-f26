"""Original pixel art generator for Feast or Fiend (requires Pillow only for asset authoring)."""
from PIL import Image,ImageDraw,ImageFont
from pathlib import Path
import random, math
R=random.Random(47)
OUT=Path(__file__).resolve().parent/'art';OUT.mkdir(exist_ok=True)
S=3
C={'grass':'#77c86b','light':'#a0e27e','dark':'#438954','gold':'#f6d56e','cream':'#fff1bb','ink':'#243750','brown':'#8a583a','pink':'#f998aa','blue':'#6fcbdc','red':'#e96e63','leaf':'#389c5d','shade':'#2d6570'}

def save(im,name,scale=3):
 im.resize((im.width*scale,im.height*scale),Image.Resampling.NEAREST).save(OUT/(name+'.png'),optimize=True)
def pix(d,xy,fill):d.rectangle(xy,fill=fill)
def line(d,coords,fill,width=1):d.line(coords,fill=fill,width=width)
def flower(d,x,y,color='#ffefe4'):
 pix(d,(x,y,x+1,y+1),'#256e4f');pix(d,(x,y-2,x+1,y-1),color);pix(d,(x-2,y,x-1,y+1),color);pix(d,(x+2,y,x+3,y+1),color);pix(d,(x,y+2,x+1,y+3),color);pix(d,(x,y,x+1,y+1),'#f9bf55')
def tree(d,x,y,t=0):
 # outlined readable tree, built in 16px units
 pix(d,(x+8,y+15,x+12,y+27),'#523d43');pix(d,(x+9,y+14,x+11,y+27),'#ae7143');
 for xx,yy in [(0,8),(6,1),(13,7),(4,13)]:
  pix(d,(x+xx,y+yy,x+xx+13,y+yy+12),'#235d50')
  pix(d,(x+xx+2,y+yy+1,x+xx+10,y+yy+9),['#49a96b','#68be69','#6dcf74'][t%3]);pix(d,(x+xx+4,y+yy+1,x+xx+7,y+yy+3),'#9fe89b')
def fence(d,x,y,n=4):
 for k in range(n):
  xx=x+k*9;pix(d,(xx,y,xx+2,y+10),'#6c4b53');pix(d,(xx+1,y+1,xx+3,y+8),'#eac07b')
 line(d,(x,y+3,x+9*n,y+3),'#a4754d',2);line(d,(x,y+8,x+9*n,y+8),'#a4754d',2)
def grass(d,x,y,variant):
 pix(d,(x,y,x+15,y+15),['#78c97a','#80d481','#73c877','#8dd883'][variant%4]);
 if variant%3==0:line(d,(x+5,y+11,x+6,y+8),'#44a763');line(d,(x+8,y+12,x+9,y+10),'#409b58')
 if variant%5==0:pix(d,(x+12,y+4,x+13,y+4),'#d4e988')
def path(d,x,y,variant):
 pix(d,(x,y,x+15,y+15),['#e3be84','#dbae75','#e9c68d'][variant%3]);pix(d,(x+3,y+4,x+6,y+4),'#cba16a');pix(d,(x+11,y+11,x+13,y+11),'#f9d9a3')
def water(d,x,y):
 pix(d,(x,y,x+15,y+15),'#3f95ba');line(d,(x+3,y+4,x+10,y+4),'#8ae8e8');line(d,(x+6,y+10,x+14,y+10),'#64bbd7')
def roof(d,x,y,w,h,color):
 pix(d,(x,y,x+w,y+h),'#25364f');pix(d,(x+2,y+2,x+w-2,y+h-2),color)
 for xx in range(x+6,x+w-2,12):line(d,(xx,y+6,xx+5,y+6),'#f8b4a3',2)
def building(d,x,y,w,h,typ):
 # wood body and brick base
 pix(d,(x+7,y+18,x+w-7,y+h),'#4c6670');pix(d,(x+10,y+20,x+w-10,y+h-3),'#f5d6a4')
 for yy in range(y+31,y+h-2,10):line(d,(x+10,yy,x+w-10,yy),'#e0b47e')
 roof(d,x,y,w,26,{'restaurant':'#e45c67','smith':'#7282b6','shop':'#f0a661'}[typ]);
 for xx in (x+17,x+w-30):
  pix(d,(xx,y+38,xx+15,y+55),'#303f67');pix(d,(xx+2,y+40,xx+13,y+53),'#83dff0');line(d,(xx+8,y+39,xx+8,y+54),'#e5d5b1')
 pix(d,(x+w//2-11,y+h-33,x+w//2+11,y+h),'#364b60');pix(d,(x+w//2-8,y+h-30,x+w//2+8,y+h-1),'#94644c');pix(d,(x+w//2+5,y+h-14,x+w//2+6,y+h-12),'#f2da88');
 pix(d,(x+w//2-32,y+12,x+w//2+32,y+29),'#3b4d66');pix(d,(x+w//2-29,y+14,x+w//2+29,y+26),'#fff1c0')
 # word sign is on UI overlay in game, little icon mark on roof
 for xx in range(x+10,x+w,22):pix(d,(xx,y+4,xx+8,y+5),'#ffb8ba')
def tilemap(scene):
 W,H=320,168;im=Image.new('RGB',(W,H));d=ImageDraw.Draw(im)
 if scene=='town':
  for y in range(0,H,16):
   for x in range(0,W,16):
    if (132<x<194) or (y>104 and 48<x<270) or (y<44 and 117<x<194):path(d,x,y,(x+y)//16)
    else:grass(d,x,y,(x//16*9+y//16*7)%19)
  # central paved market plaza
  pix(d,(105,72,214,121),'#d5ad77');
  for yy in range(77,122,12):
   for xx in range(113+(yy%3)*4,211,21):pix(d,(xx,yy,xx+15,yy+6),'#e6bf85')
  # circular fountain
  d.ellipse((144,85,177,114),fill='#456378',outline='#33445f',width=2);d.ellipse((149,89,173,109),fill='#68c7d7');d.ellipse((155,92,168,107),fill='#b2eeeb');pix(d,(160,84,163,93),'#cde6da')
  building(d,32,10,96,82,'restaurant');building(d,202,10,89,78,'smith')
  fence(d,13,98,10);fence(d,226,104,8)
  for x,y in [(8,5),(290,4),(8,128),(286,124),(258,130),(62,138)]:tree(d,x,y,x%3)
  for x,y in [(12,111),(34,116),(216,142),(262,108),(91,132),(278,97)]:flower(d,x,y)
  pix(d,(132,9,186,27),'#f2d49c');pix(d,(135,12,183,24),'#354f64')
 elif scene=='meadow':
  for y in range(0,H,16):
   for x in range(0,W,16):grass(d,x,y,(x//16*3+y//16*11)%17)
  # river crossing / pond
  for y in range(0,H,16):
   for x in range(240,320,16):
    if (y>60 and x>262) or (y>100 and x>246):water(d,x,y)
  # stepping stones
  for x,y in [(254,107),(266,119),(274,131),(288,143)]:d.ellipse((x-4,y-2,x+8,y+5),fill='#f0e0ac',outline='#708c78')
  for x,y in [(0,3),(14,14),(35,8),(66,0),(89,13),(294,3),(5,112),(32,131),(85,135),(124,143),(181,6)]:tree(d,x,y,(x+y)%3)
  for k in range(25):
   x=R.randrange(18,235);y=R.randrange(23,154)
   flower(d,x,y,('#ffdef0','#ffffce','#d4eafa')[k%3])
  fence(d,103,133,10);fence(d,105,46,7)
  # growing plots
  for x in (111,140,169):
   pix(d,(x,82,x+21,108),'#654b49');pix(d,(x+2,84,x+19,106),'#b88153');
   for j in range(87,105,6):line(d,(x+4,j,x+17,j),'#785849')
 elif scene=='restaurant':
  pix(d,(0,0,W,H),'#9b6b56')
  for y in range(0,H,16):
   for x in range(0,W,16):
    pix(d,(x,y,x+15,y+15),('#dbac70' if (x+y)//16%2 else '#eec58b'))
    line(d,(x,y,x+15,y),'#b88960');line(d,(x,y,x,y+15),'#f9db9f')
  pix(d,(0,0,W,40),'#44566e');pix(d,(0,28,W,40),'#f9df9d');
  # windows with outside greenery
  for x in (18,120,259):
   pix(d,(x,7,x+36,31),'#37495b');pix(d,(x+3,10,x+33,28),'#8bd0d9');pix(d,(x+5,22,x+31,27),'#79c477');line(d,(x+18,9,x+18,29),'#fbe1a9')
  # long counter
  pix(d,(161,44,306,67),'#674b56');pix(d,(166,44,302,62),'#cc856d');pix(d,(166,43,302,47),'#f9c08b')
  for x in [40,96,242]:
   pix(d,(x,89,x+38,109),'#573f50');pix(d,(x+2,85,x+36,103),'#c07c60');pix(d,(x+5,85,x+32,88),'#f2b78c')
   for xx in (x+4,x+30):pix(d,(xx,109,xx+4,114),'#493e48')
  # plant stands & kitchen cooktop
  pix(d,(210,72,282,87),'#5b4854');pix(d,(214,70,279,80),'#f6c78a');
  for x in (223,246):d.ellipse((x,62,x+19,78),fill='#4b5360');d.ellipse((x+2,63,x+17,74),fill='#9cdbe5');d.ellipse((x+6,63,x+13,71),fill='#fff0a6')
  for x,y in [(12,41),(299,42),(12,123),(294,119)]:
   pix(d,(x,y+7,x+11,y+16),'#ad7754');pix(d,(x+1,y,x+12,y+11),'#3d9b68');pix(d,(x+4,y-4,x+9,y+6),'#5ac87e')
  # tapestry
  pix(d,(65,5,99,37),'#b25a6b');pix(d,(68,8,96,34),'#faadd0');pix(d,(78,10,86,28),'#ffe0a7')
 elif scene=='boss':
  for y in range(0,H,16):
   for x in range(0,W,16):path(d,x,y,(x//16+y//16)%3)
  pix(d,(0,0,319,10),'#b55a6d');pix(d,(0,148,319,167),'#b55a6d');pix(d,(0,0,11,167),'#b55a6d');pix(d,(307,0,319,167),'#b55a6d');
  for x,y in [(13,12),(270,13),(15,115),(274,113)]:
   pix(d,(x,y,x+31,y+27),'#6c4865');pix(d,(x+3,y+3,x+28,y+24),'#eb96ae');pix(d,(x+7,y+5,x+24,y+16),'#ffd9cd')
  for x,y in [(40,44),(253,41),(54,114),(248,120)]:
   flower(d,x,y,'#f6b1e1')
  # boss ring
  d.ellipse((113,35,208,132),outline='#e4b19b',width=3);d.ellipse((124,46,197,121),outline='#f7dfbd',width=2)
  for x in range(25,320,40):pix(d,(x,5,x+17,8),'#ffddaa')
 save(im,'bg_'+scene,3)

def sprite(name,scale=3):
 im=Image.new('RGBA',(24,28),(0,0,0,0));d=ImageDraw.Draw(im)
 def rect(a,b,c,d_,color):pix(d,(a,b,c,d_),color)
 # 2px darkest outline for recognizable silhouettes
 if name.startswith('hero'):
  rect(7,3,16,9,'#283e59');rect(8,4,15,10,'#a76e4d');rect(6,4,17,5,'#5d3c56');rect(9,6,11,6,'#283e59');rect(14,6,15,6,'#283e59')
  rect(5,11,18,21,'#283e59');rect(7,12,17,21,'#fff0bb');rect(8,12,15,14,'#f18479');rect(10,15,14,19,'#ffdb95');rect(7,21,10,25,'#474f73');rect(14,21,17,25,'#474f73');rect(6,25,11,27,'#263850');rect(13,25,18,27,'#263850')
  rect(5,13,6,19,'#f0bb8f');rect(18,13,19,19,'#f0bb8f')
  if name=='hero_back':rect(8,4,15,8,'#5e3c4c');rect(9,7,14,9,'#543a4a');rect(7,13,17,18,'#e5b66c')
  if name=='hero_left':rect(8,6,11,6,'#283e59');rect(12,6,16,6,'#a76e4d')
  if name=='hero_right':rect(13,6,16,6,'#283e59');rect(7,6,11,6,'#a76e4d')
 elif name in ('grey','lola','madeline','chester'):
  palette={'grey':('#b9c2cf','#a36b54','#6c778c'),'lola':('#fbb976','#f3b28b','#71bb65'),'madeline':('#b88eca','#e7b39a','#cd6578'),'chester':('#d8b286','#e2ab7c','#7296b4')}
  hair,skin,cloth=palette[name];rect(6,3,18,13,'#2a3e58');rect(8,6,16,12,skin);rect(7,3,17,7,hair);rect(9,9,10,9,'#273e53');rect(14,9,15,9,'#273e53')
  rect(5,13,19,23,'#2b3b54');rect(7,14,17,22,cloth);rect(7,23,10,27,'#39455e');rect(14,23,17,27,'#39455e');rect(4,15,6,21,skin);rect(18,15,20,21,skin)
  if name=='grey':rect(5,4,18,6,'#8b9ea6');rect(11,14,14,21,'#f4e2b2')
  if name=='lola':rect(16,5,20,11,'#d3884e');rect(4,4,7,10,'#d3884e');rect(10,13,15,14,'#f2d76d')
  if name=='madeline':rect(4,5,20,8,'#a66ca7');rect(10,13,15,15,'#f9dcc0')
 elif name in ('carrot','lettuce','broccoli'):
  base={'carrot':'#ed9652','lettuce':'#99d77d','broccoli':'#49b871'}[name]
  rect(5,9,18,24,'#2f5260');rect(7,9,16,21,base)
  if name=='carrot':
   rect(8,7,15,23,'#ed9256');rect(10,3,11,9,'#2e925d');rect(14,4,15,9,'#4fad66');rect(9,12,9,14,'#f9b775')
  elif name=='lettuce':
   rect(4,7,19,19,'#3f9c62');rect(6,5,17,17,'#a6da77');rect(8,3,15,14,'#d2ed93');rect(10,4,11,6,'#f1f9b9')
  else:
   rect(4,5,20,15,'#285f51');rect(5,4,11,15,'#4eaa65');rect(12,3,18,15,'#68c16a');rect(8,2,15,10,'#92d67c');rect(9,15,15,23,'#67995d')
  rect(9,15,10,16,'#24364c');rect(15,15,16,16,'#24364c');rect(8,23,11,26,'#4c5367');rect(15,23,18,26,'#4c5367')
  if name=='carrot':rect(6,19,7,20,'#f7d7a6')
 elif name.startswith('cake'):
  straw=name=='cake_strawberry';rect(2,10,22,25,'#3d405e');rect(4,10,20,22,'#f5d5a9');rect(3,10,21,14,'#fff3d8');rect(5,17,19,20,'#e0a77b');rect(3,12,21,15,'#f7aabe' if straw else '#f8efcc');rect(6,18,8,18,'#3e4358');rect(15,18,17,18,'#3e4358');rect(10,20,14,20,'#c77777');
  for x in [6,12,18]:rect(x,6,x+2,11,'#f2647c' if straw else '#ffefb1')
  rect(8,4,16,7,'#f16b7f' if straw else '#ecd3a4');rect(10,1,14,5,'#7dc367' if straw else '#e6a4b5')
  rect(0,15,3,17,'#fff1cd');rect(21,15,23,17,'#fff1cd');rect(6,25,9,27,'#b66c86');rect(15,25,18,27,'#b66c86')
  if straw:
   for x,y in [(6,12),(18,12),(11,8)]:rect(x,y,x+1,y+2,'#e45e72')
 elif name=='strawberry':
  rect(6,8,17,22,'#315456');rect(7,9,16,21,'#f16e82');rect(8,7,15,10,'#54a961');rect(10,5,13,9,'#4d9457')
  for x,y in [(9,13),(14,13),(12,17)]:rect(x,y,x+1,y+2,'#f9d8b8')
 elif name=='dish':
  d.ellipse((1,14,22,23),fill='#b5e7de',outline='#2b425e',width=2);d.ellipse((5,15,18,20),fill='#74bc6b');rect(8,12,15,16,'#efbd79');rect(10,10,12,15,'#fcdd8d')
 elif name=='heart':
  rect(4,8,9,12,'#e35c72');rect(14,8,19,12,'#e35c72');rect(3,12,20,17,'#ef7c8d');rect(6,18,17,20,'#ef7c8d');rect(9,21,14,23,'#ef7c8d')
 elif name=='coin':
  d.ellipse((3,3,21,23),fill='#df9558',outline='#483e5a',width=2);d.ellipse((5,4,19,20),fill='#ffe084');rect(11,7,13,17,'#ce935c')
 else:rect(5,5,18,21,'#f2c18a')
 save(im,name,3)
for sc in ['town','meadow','restaurant','boss']:tilemap(sc)
for n in ['hero_front','hero_back','hero_left','hero_right','grey','lola','madeline','chester','carrot','lettuce','broccoli','cake','cake_strawberry','strawberry','dish','heart','coin']:sprite(n)
print('Created',len(list(OUT.iterdir())),'PNG assets in',OUT)