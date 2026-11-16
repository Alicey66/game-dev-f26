"""Feast or Fiend: The Last Spoon — a complete small offline RPG vertical slice.
Copyright (c) 2026 Feast or Fiend contributors. Original code and procedural pixel art.
No external runtime dependencies: Python 3.10+ with Tkinter (ships with standard Windows Python).
"""
from __future__ import annotations
import base64, io, json, math, os, random, sys, time, tkinter as tk, zipfile
from pathlib import Path

TITLE='FEAST OR FIEND  |  THE LAST SPOON'
WIDTH,HEIGHT=960,600
WORLD_H=504
BG='#192f49'; GOLD='#ffe0a0'; CREAM='#fff4d5'; MUTED='#a9c8c7'; MINT='#79e4b1'
HERE=Path(__file__).resolve().parent
ASSETS=(Path(getattr(sys,'_MEIPASS',HERE))/'art') if getattr(sys,'frozen',False) else (HERE/'art')
SAVE=Path.home()/'.feast_or_fiend_demo_save.json'
R=random.Random(12)

def clamp(x,a,b):return max(a,min(b,x))
def dist(a,b):return math.hypot(a[0]-b[0],a[1]-b[1])

class Game:
 def __init__(self,root):
  self.root=root;root.title(TITLE);root.resizable(False,False);root.configure(bg=BG)
  self.canvas=tk.Canvas(root,width=WIDTH,height=HEIGHT,background=BG,highlightthickness=0)
  self.canvas.pack();self.img={}
  for p in ASSETS.glob('*.png'):
   try:self.img[p.stem]=tk.PhotoImage(file=str(p))
   except tk.TclError:pass
  if 'bg_town' not in self.img:
   pack=Path(getattr(sys,'_MEIPASS',HERE))/'artpack.b64' if getattr(sys,'frozen',False) else HERE/'artpack.b64'
   if pack.exists():
    try:
     with zipfile.ZipFile(io.BytesIO(base64.b64decode(pack.read_text(encoding='ascii')))) as z:
      for fname in z.namelist():
       if fname.endswith('.png'):
        data=base64.b64encode(z.read(fname)).decode('ascii')
        self.img[Path(fname).stem]=tk.PhotoImage(data=data)
    except (OSError,ValueError,zipfile.BadZipFile,tk.TclError) as e:
     raise RuntimeError('Cannot load bundled pixel-art assets: '+str(e)) from e
  for icon_name in ('heart','coin'):
   if icon_name in self.img:self.img[icon_name+'_small']=self.img[icon_name].subsample(3,3)
  self.keys=set();self.modal=None;self.modal_options=[];self.modal_callback=None
  self.scene='town';self.x=510.;self.y=395.;self.face='front';self.walking=0
  self.coins=1;self.hp=6;self.max_hp=6;self.seed={'carrot':0,'lettuce':0,'broccoli':0}
  self.inventory={'carrot':0,'lettuce':0,'broccoli':0,'strawberry':0}
  self.recipes=['Water'];self.plots=[{'crop':None,'ready':0} for _ in range(3)]
  self.sales=0;self.renown=0;self.upgrades=0;self.boss_wins=0;self.boss_mode='ADAPTIVE';self.boss_changed=False
  self.quest=0;self.help_seen=False;self.boss_unlocked=False;self.boss_hp=12;self.boss_attack_at=0
  self.boss_next_action='';self.boss_warning=None;self.boss_bullets=[];self.boss_x=480.;self.boss_y=220.
  self.monsters=[];self.started=time.monotonic();self.last=self.started;self.attack_at=0;self.invuln_until=0
  self.hit_fx=[];self.notice='';self.notice_until=0;self.particles=[];self.dialogue_queue=[]
  self.entry_msg='';self.tick_count=0;self.sound=True
  root.bind('<KeyPress>',self.key_down);root.bind('<KeyRelease>',self.key_up)
  self.canvas.bind('<Button-1>',self.click)
  if SAVE.exists():
   try:self.load()
   except (OSError,ValueError,KeyError,TypeError):pass
  self.spawn_monsters();self.root.after(50,self.run)
  self.show_intro()

 def load(self):
  d=json.loads(SAVE.read_text(encoding='utf8'))
  for k in ['scene','x','y','coins','hp','max_hp','seed','inventory','recipes','plots','sales','renown','upgrades','boss_wins','boss_mode','boss_changed','quest','boss_unlocked']:
   if k in d:setattr(self,k,d[k])
  # don't load into the middle of an active fight
  if self.scene=='boss':self.scene='town';self.x=870;self.y=365
  if self.scene not in ['town','meadow','restaurant']:self.scene='town'
  self.hp=max(1,int(self.hp));self.x=float(self.x);self.y=float(self.y)

 def save(self):
  data={k:getattr(self,k) for k in ['scene','x','y','coins','hp','max_hp','seed','inventory','recipes','plots','sales','renown','upgrades','boss_wins','boss_mode','boss_changed','quest','boss_unlocked']}
  SAVE.write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf8')
  self.toast('Progress saved!  Your little restaurant is safe.')

 def toast(self,s,seconds=3):self.notice=s;self.notice_until=time.monotonic()+seconds
 def dialogue(self,title,body,choices=None,callback=None):
  self.modal=('dialogue',title,body);self.modal_options=choices or ['Continue  ↵'];self.modal_callback=callback;self.keys.clear()
 def show_intro(self):
  self.dialogue('THE LAST SPOON  •  PROLOGUE',
  'A dusty little restaurant. One pot, one table... and a bucket of water.\n\nGrandpa left you a note:  "Pot on the stove. Water in the barrel. Food in the wild. Don\'t starve."\n\nWelcome to SEASONING TOWN.  Your restaurant story begins today.',
  ['Open the doors!  ↵'],lambda i:self.toast('WASD / arrows: move   •   E: interact   •   J: attack   •   Q: journal',6))

 def spawn_monsters(self):
  self.monsters=[{'type':'carrot','x':220.,'y':170.,'hp':2,'alive':True,'respawn':0,'phase':.2},
   {'type':'lettuce','x':720.,'y':195.,'hp':2,'alive':True,'respawn':0,'phase':2.4},
   {'type':'broccoli','x':660.,'y':370.,'hp':3,'alive':True,'respawn':0,'phase':1.0},
   {'type':'carrot','x':380.,'y':420.,'hp':2,'alive':True,'respawn':0,'phase':3.0}]

 def key_down(self,event):
  k=event.keysym.lower();fresh=k not in self.keys;self.keys.add(k)
  if not fresh:return
  if self.modal:
   if k in ('return','space','e'):
    self.resolve_modal(0)
   elif k in ('escape','backspace'):self.resolve_modal(-1)
   elif k.isdigit() and 1<=int(k)<=len(self.modal_options):self.resolve_modal(int(k)-1)
   elif k in ('up','w','down','s'):
    self.modal_selected=(getattr(self,'modal_selected',0)+(1 if k in ('down','s') else -1))%len(self.modal_options)
   return
  if k=='j':self.attack()
  elif k=='e':self.interact()
  elif k=='k':self.feed()
  elif k=='q':self.journal()
  elif k=='tab':self.inventory_menu()
  elif k=='f5':self.save()
  elif k=='escape':self.pause_menu()
  elif k=='t' and self.scene=='boss':self.boss_mode='SCRIPTED' if self.boss_mode=='ADAPTIVE' else 'ADAPTIVE';self.toast('Boss policy: '+self.boss_mode)
  elif k=='m':self.sound=not self.sound;self.toast('Sound cues: '+('on' if self.sound else 'off'))
 def key_up(self,event):self.keys.discard(event.keysym.lower())
 def resolve_modal(self,i):
  cb=self.modal_callback;self.modal=None;self.modal_callback=None;self.modal_selected=0
  if i>=0 and cb:cb(i)
 def click(self,event):
  x,y=event.x,event.y
  if self.modal:
   count=min(len(self.modal_options),4)
   top=305 if count>=4 else 340 if count==3 else 380
   if 200<x<760 and top<=y<top+count*37:
    i=int((y-top)/37)
    if 0<=i<count:self.resolve_modal(i)
   return
  if y>=531:
   if x<185:self.interact()
   elif x<363:self.attack()
   elif x<548:self.journal()
   elif x<747:self.inventory_menu()
   else:self.pause_menu()

 def set_scene(self,scene,x,y):
  self.scene=scene;self.x=x;self.y=y;self.keys.clear()
  if scene=='boss':
   self.boss_hp=12 if not self.boss_changed else 17;self.boss_attack_at=time.monotonic()+2
   self.boss_x=480.;self.boss_y=225.;self.boss_warning=None;self.boss_bullets=[]
   self.dialogue('BOSS ENCOUNTER  •  LADY CAKE',
    '"Oh? A chef. You want to feed me a strawberry? Darling, I could use a new look!"\n\nJ: attack  •  K: offer a strawberry  •  T: compare boss policies\nDodge her telegraphed attacks and survive!', ['Let them eat cake!'])
  elif scene=='meadow':self.toast('WILDFLAVOR MEADOW  •  J to strike  •  E to plant or harvest',4)
  elif scene=='restaurant':self.toast('THE LAST SPOON  •  Cook at the pot. Serve at the counter.',4)
  elif scene=='town':self.toast('SEASONING TOWN  •  A new day smells like adventure.',4)
  self.save()

 def current_object(self):
  p=(self.x,self.y);targets=[]
  if self.scene=='town':
   for name,x,y in [('Grey',720,325),('Lola',475,382),('Madeline',586,340),('Chester',375,370),('Restaurant',240,280)]:targets.append((dist(p,(x,y)),name))
  elif self.scene=='restaurant':
   for name,x,y in [('Cookpot',740,250),('Counter',460,320),('Upgrade',700,385),('Door',480,465)]:targets.append((dist(p,(x,y)),name))
  elif self.scene=='meadow':
   for i,x in enumerate([365,452,539]):targets.append((dist(p,(x,320)),'Plot'+str(i)))
  if not targets:return None
  d,name=min(targets);return name if d<93 else None

 def interact(self):
  name=self.current_object()
  if not name:
   self.toast('Get closer to a character, door, garden plot, or station.');return
  if name=='Restaurant':self.set_scene('restaurant',470,443)
  elif name=='Door':self.set_scene('town',245,329)
  elif name=='Grey':
   if self.sales:
    self.dialogue('GREY  •  THE POTSMITH','"I can smell it. Finally, something other than boiled water! Your grandpa... well, his cooking had personality."')
   else:self.dialogue('GREY  •  THE POTSMITH','"You\'re the new kid? That pot is old enough to sell as an antique. Don\'t cry, I\'ll fix it.\n\nOh right. You can only serve water."')
  elif name=='Lola':
   self.dialogue('LOLA  •  THE GARDENER','"Seeds? From monsters? What a strange world! Plant them in the beds to the west.\n\nThe secret is not to stare. Carrots get shy."')
  elif name=='Madeline':
   self.dialogue('MAYOR MADELINE','"This town once had seventeen beautiful smells on one street. Now, there\'s just your bucket of water.\n\nDon\'t lose hope, dear. Even water is a flavor."')
  elif name=='Chester':
   self.dialogue('CHESTER  •  YOUR FIRST CUSTOMER','"Still here? Good. I\'ll be back tomorrow.\n\nYour grandpa once held a town-wide food tasting. Everyone remembered it... for two days."')
  elif name=='Cookpot':self.cook_menu()
  elif name=='Counter':self.serve()
  elif name=='Upgrade':self.upgrade()
  elif name.startswith('Plot'):self.plant(int(name[-1]))

 def plant(self,i):
  plot=self.plots[i];now=time.time()
  if plot['crop']:
   if now>=plot['ready']:
    c=plot['crop'];self.inventory[c]+=3;plot['crop']=None;plot['ready']=0
    self.renown+=1;self.toast('HARVEST!  +3 '+c.title()+'  •  Your garden is thriving!',4)
    self.burst([365,452,539][i],307,'#ffe3ac')
    if self.quest==1:self.quest=2;self.toast('QUEST COMPLETE!  Now cook a dish at The Last Spoon!',5)
    self.save()
   else:self.toast('Growing...  '+str(math.ceil(plot['ready']-now))+'s until harvest.')
  else:
   available=[k for k,v in self.seed.items() if v>0]
   if not available:self.toast('No seeds yet!  Hunt the living vegetables with J.');return
   opts=[c.title()+' seed  (you own '+str(self.seed[c])+')' for c in available]
   self.dialogue('PLANT A SEED','The little garden smells of sunshine and fresh soil. What will you grow?',opts,lambda n:self.do_plant(i,available[n]))

 def do_plant(self,i,crop):
  if self.seed[crop]<=0:return
  self.seed[crop]-=1;self.plots[i]={'crop':crop,'ready':time.time()+12};self.toast(crop.title()+' planted!  Return in 12 seconds.',4)
  if self.quest==0:self.quest=1
  self.save()

 def cook_menu(self):
  options=['Garden Salad  ·  2 Lettuce  →  8 coins', 'Carrot Soup  ·  2 Carrot  →  9 coins', 'Forest Stew  ·  1 Carrot + 1 Broccoli  →  14 coins','Cancel']
  self.dialogue('THE PRIMORDIAL COOKPOT','"What you feed a pot... the pot remembers."\n\nTry recipes and build the menu. Ingredients come from your adventures and harvests.',options,lambda i:self.cook(i))
 def cook(self,i):
  if i>=3:return
  recipes=[('Garden Salad',{'lettuce':2},8),('Carrot Soup',{'carrot':2},9),('Forest Stew',{'carrot':1,'broccoli':1},14)]
  name,req,price=recipes[i]
  missing=[f'{k} x{n}' for k,n in req.items() if self.inventory[k]<n]
  if missing:self.dialogue('NOT ENOUGH INGREDIENTS','You still need: '+', '.join(missing)+'.\n\nExplore the meadow and grow more ingredients.');return
  for k,n in req.items():self.inventory[k]-=n
  if name not in self.recipes:self.recipes.append(name);self.renown+=2
  self.inventory['dish_'+str(i)]=self.inventory.get('dish_'+str(i),0)+1
  self.toast('NEW DISH!  '+name+'  •  Bring it to the serving counter!',5)
  if self.quest<=2:self.quest=3
  self.burst(740,215,'#ffe4ae');self.save()

 def serve(self):
  dishes=[('Garden Salad',0,8),('Carrot Soup',1,9),('Forest Stew',2,14)]
  have=[(n,i,c) for n,i,c in dishes if self.inventory.get('dish_'+str(i),0)>0]
  if not have:
   self.dialogue('COUNTER  •  FIRST CUSTOMER','A customer taps a spoon on the table.\n\n"Anything to eat?"\n\nYou offer water. The customer smiles politely.\n\nEarn some money by cooking a real dish!', ['Serve water  (+1 coin)'],lambda i:self.serve_water());return
  names=[f'Serve {n}  •  +{c} coins' for n,i,c in have]
  self.dialogue('READY TO SERVE!','The aroma fills the room. Which dish will you put on the menu?',names,lambda ix:self.sell_dish(have[ix]))
 def serve_water(self):
  self.coins+=1;self.toast('You served water. +1 coin. A humble beginning!');self.save()
 def sell_dish(self,chosen):
  name,i,c=chosen;key='dish_'+str(i)
  if self.inventory.get(key,0)<1:return
  self.inventory[key]-=1;self.coins+=c;self.sales+=1;self.renown+=2
  self.toast('SOLD!  '+name+'  +'+str(c)+' coins  ★ Reputation +2',5)
  if self.sales>=2 and not self.boss_unlocked:
   self.boss_unlocked=True;self.inventory['strawberry']+=1;self.quest=4
   self.dialogue('A MYSTERIOUS RECIPE',
    'A recipe begins to glow. New words appear on the back:\n\n"The finest flavors hide in the most dangerous places."\n\nBOSS ARENA UNLOCKED!  Exit town on the RIGHT.\nA strawberry has appeared in your pantry.  Try feeding it to Lady Cake!')
  self.save()
 def upgrade(self):
  cost=15+self.upgrades*12
  self.dialogue('RENOVATE  •  THE LAST SPOON',f'Bigger tables, warmer lights, and more hungry customers!\n\nUpgrade cost: {cost} coins\nYour purse: {self.coins} coins\nCurrent restaurant level: {self.upgrades+1}',[f'Upgrade  ·  {cost} coins','Maybe later'],lambda i:self.buy_upgrade(i,cost))
 def buy_upgrade(self,i,cost):
  if i:return
  if self.coins<cost:self.toast('Not enough coins. Serve more food first!');return
  self.coins-=cost;self.upgrades+=1;self.renown+=5;self.toast('RESTAURANT LEVEL '+str(self.upgrades+1)+'!  The town is talking!',5);self.save()

 def attack(self):
  now=time.monotonic()
  if now<self.attack_at:return
  self.attack_at=now+.32
  ox,oy=self.x,self.y-18;self.hit_fx.append([ox,oy,now+.18])
  if self.scene=='meadow':
   for m in self.monsters:
    if m['alive'] and dist((self.x,self.y),(m['x'],m['y']))<83:
     m['hp']-=1;self.burst(m['x'],m['y']-20,'#fff4c6',7)
     if m['hp']<=0:
      m['alive']=False;m['respawn']=now+7
      typ=m['type'];self.seed[typ]+=1;self.inventory[typ]+=1
      self.coins+=2;self.toast('+'+typ.title()+'  +1 seed  +2 coins!  Try the garden plots.',4)
      if self.quest==0:self.quest=1
      self.save()
     break
  elif self.scene=='boss':
   if dist((self.x,self.y),(self.boss_x,self.boss_y))<108:
    self.boss_hp-=1;self.burst(self.boss_x,self.boss_y-32,'#fff0bf',10)
    if self.boss_hp<=0:self.win_boss()

 def feed(self):
  if self.scene!='boss':self.toast('K: offer ingredients to a boss during an encounter.');return
  if self.inventory.get('strawberry',0)<=0:self.toast('No strawberries!  Earn one from the restaurant or buy in town.');return
  if dist((self.x,self.y),(self.boss_x,self.boss_y))>170:self.toast('Get closer to Lady Cake to offer her the strawberry.');return
  if self.boss_changed:self.toast('Lady Cake has already transformed!');return
  self.inventory['strawberry']-=1;self.boss_changed=True;self.boss_hp+=5;self.burst(self.boss_x,self.boss_y-40,'#f57fa5',22)
  self.dialogue('A SWEET TRANSFORMATION!','"Strawberry?! I\'m beautiful! Mr. Tea, look!"\n\nLADY CAKE → STRAWBERRY CAKE\nNew frosting. Faster attacks. Rare recipe reward.\n\nThe boss adapts to the ingredient you offered.')

 def win_boss(self):
  self.boss_wins+=1;self.coins+=25;self.renown+=12
  recipe='Strawberry Cake' if self.boss_changed else 'Cake'
  if recipe not in self.recipes:self.recipes.append(recipe)
  self.quest=5;self.hp=self.max_hp;self.burst(self.boss_x,self.boss_y-40,'#fdf1b3',30)
  mode=self.boss_mode
  self.dialogue('BOSS DEFEATED  ★  '+recipe.upper(),
   f'Victory!  +25 coins  +12 reputation\n\nNEW RECIPE: {recipe}\nBoss decision mode: {mode}\n\nThe Last Spoon has a new signature dish.\n\nYou have completed the playable demo!\nKeep exploring, cooking, and upgrading your restaurant.', ['Back to Seasoning Town'],lambda i:self.set_scene('town',865,365))
  self.save()

 def boss_agent(self,now):
  # Two genuine, comparable local decision policies. This is a bounded offline game agent,
  # not a hosted LLM; no hidden API cost, no network access and no ability to edit world state.
  if self.boss_mode=='SCRIPTED':
   seq=['fan','charge','fan','rest'];act=seq[(self.tick_count//36)%len(seq)]
  else:
   d=dist((self.x,self.y),(self.boss_x,self.boss_y))
   if d<100:act='shockwave'
   elif d>260:act='charge'
   elif self.boss_changed and R.random()<.58:act='fan'
   else:act='fan' if R.random()<.58 else 'charge'
  self.boss_next_action=act
  if act=='rest':self.boss_attack_at=now+.9;return
  self.boss_warning={'act':act,'at':now+.6,'tx':self.x,'ty':self.y}
  self.boss_attack_at=now+(1.75 if self.boss_changed else 2.05)

 def update_boss(self,dt,now):
  if self.boss_warning and now>=self.boss_warning['at']:
   a=self.boss_warning;act=a['act'];self.boss_warning=None
   if act=='shockwave':
    if dist((self.x,self.y),(self.boss_x,self.boss_y))<150:self.damage(1)
    self.burst(self.boss_x,self.boss_y,'#ffcaad',17)
   elif act=='charge':
    if dist((self.x,self.y),(a['tx'],a['ty']))<70:self.damage(1)
    self.boss_x=clamp(a['tx'],65,890);self.boss_y=clamp(a['ty'],65,450)
    self.burst(self.boss_x,self.boss_y,'#f8b9d3',12)
   elif act=='fan':
    dx=self.x-self.boss_x;dy=self.y-self.boss_y;l=max(1,math.hypot(dx,dy));angle=math.atan2(dy,dx)
    for da in [-.48,-.24,0,.24,.48]:
     a2=angle+da;self.boss_bullets.append({'x':self.boss_x,'y':self.boss_y-30,'dx':math.cos(a2)*205,'dy':math.sin(a2)*205,'life':2.3})
  if not self.boss_warning and now>=self.boss_attack_at:self.boss_agent(now)
  keep=[]
  for b in self.boss_bullets:
   b['x']+=b['dx']*dt;b['y']+=b['dy']*dt;b['life']-=dt
   if dist((self.x,self.y-13),(b['x'],b['y']))<26:self.damage(1);b['life']=0
   if b['life']>0 and 30<b['x']<940 and 20<b['y']<485:keep.append(b)
  self.boss_bullets=keep

 def damage(self,n):
  now=time.monotonic()
  if now<self.invuln_until:return
  self.hp-=n;self.invuln_until=now+1.05;self.burst(self.x,self.y-20,'#ff8086',12)
  if self.hp<=0:
   self.hp=self.max_hp;self.coins=max(0,self.coins-3)
   self.dialogue('YOU FAINTED!','Grey dragged you back to town and patched you up.\n\n"Didn\'t I tell you not to die? I have pots to repair."\n\nYou lost 3 coins, but kept your ingredients and progress.', ['Try again'],lambda i:self.set_scene('town',845,360))

 def burst(self,x,y,color,n=9):
  now=time.monotonic()
  for _ in range(n):
   a=R.random()*math.tau;s=R.uniform(20,85)
   self.particles.append([x,y,math.cos(a)*s,math.sin(a)*s,now+R.uniform(.3,.65),color])

 def journal(self):
  stage=['Catch a vegetable monster in Wildflavor Meadow (LEFT from town).',
         'Plant a seed in the garden plots. Wait 12 seconds.',
         'Harvest your crops, then visit the pot inside your restaurant.',
         'Sell two cooked dishes at your serving counter.',
         'Fight Lady Cake in the boss arena (RIGHT from town). Try K to feed!',
         'DEMO COMPLETE! Keep growing the restaurant and try the scripted boss.']
  text='CURRENT QUEST\n'+stage[clamp(self.quest,0,5)]+'\n\nDISCOVERED RECIPES\n'+', '.join(self.recipes)+'\n\nRESTAURANT LEVEL  '+str(self.upgrades+1)+'     •     REPUTATION  '+str(self.renown)+'\nBOSS VICTORIES  '+str(self.boss_wins)+'\n\nCharacters and story are inspired by your original Seasoning Town design.'
  self.dialogue('ADVENTURE JOURNAL  ★',text,['Close'])
 def inventory_menu(self):
  text='YOUR BACKPACK\n\n'+ '     '.join(k.title()+': '+str(v) for k,v in self.inventory.items() if v>0 and not k.startswith('dish'))
  text+='\n\nSEEDS\n'+'     '.join(k.title()+': '+str(v) for k,v in self.seed.items())
  text+='\n\nPREPARED DISHES\n'+'     '.join(str(k[5:])+': '+str(v) for k,v in self.inventory.items() if k.startswith('dish') and v>0)
  text+='\n\nCoins: '+str(self.coins)+'   •   F5 to save'
  self.dialogue('INVENTORY  •  YOUR BAG',text,['Close'])
 def pause_menu(self):
  self.dialogue('PAUSED  •  TAKE A BREATH','THE LAST SPOON IS YOURS.\n\nWASD / ARROWS    Move       E    Interact / Cook / Plant\nJ    Swing spoon       K    Offer strawberry to boss\nQ    Journal           TAB  Inventory\nT    Compare boss AI   F5   Save      ESC  Pause', ['Return to adventure','Save game','Quit game'],lambda i:self.pause_action(i))
 def pause_action(self,i):
  if i==1:self.save()
  elif i==2:self.save();self.root.destroy()

 def update(self,dt,now):
  self.tick_count+=1;dx=dy=0
  if 'a' in self.keys or 'left' in self.keys:dx-=1
  if 'd' in self.keys or 'right' in self.keys:dx+=1
  if 'w' in self.keys or 'up' in self.keys:dy-=1
  if 's' in self.keys or 'down' in self.keys:dy+=1
  if dx or dy:
   mag=math.hypot(dx,dy);speed=190
   xx=self.x+dx/mag*speed*dt;yy=self.y+dy/mag*speed*dt
   self.x=clamp(xx,8,953);self.y=clamp(yy,50,480)
   self.walking+=dt
   if abs(dx)>abs(dy):self.face='right' if dx>0 else 'left'
   else:self.face='front' if dy>0 else 'back'
  if self.scene=='town':
   if self.x<22 and self.y>315:self.set_scene('meadow',930,365)
   elif self.x>937 and self.y>260:
    if not self.boss_unlocked:self.x=921;self.toast('The Cake Garden is locked. Serve 2 dishes to find the recipe map!')
    else:self.set_scene('boss',105,390)
  elif self.scene=='meadow' and self.x>940:self.set_scene('town',52,375)
  elif self.scene=='boss' and self.x<15:self.set_scene('town',905,365)
  if self.scene=='meadow':
   for m in self.monsters:
    if not m['alive'] and now>m['respawn']:m['alive']=True;m['hp']=3 if m['type']=='broccoli' else 2
    if m['alive']:
     m['phase']+=dt
     m['x']+=math.sin(m['phase']*1.1)*9*dt
     m['y']+=math.cos(m['phase']*.9)*8*dt
     if dist((self.x,self.y),(m['x'],m['y']))<34:self.damage(1)
  elif self.scene=='boss':self.update_boss(dt,now)
  self.hit_fx=[h for h in self.hit_fx if h[2]>now]
  self.particles=[p for p in self.particles if p[4]>now]

 def rounded(self,x1,y1,x2,y2,fill,outline=None,r=9,width=2,tag='ui'):
  self.canvas.create_rectangle(x1+r,y1,x2-r,y2,fill=fill,outline='',tags=tag)
  self.canvas.create_rectangle(x1,y1+r,x2,y2-r,fill=fill,outline='',tags=tag)
  self.canvas.create_arc(x1,y1,x1+r*2,y1+r*2,start=90,extent=90,fill=fill,outline='',tags=tag)
  self.canvas.create_arc(x2-r*2,y1,x2,y1+r*2,start=0,extent=90,fill=fill,outline='',tags=tag)
  self.canvas.create_arc(x1,y2-r*2,x1+r*2,y2,start=180,extent=90,fill=fill,outline='',tags=tag)
  self.canvas.create_arc(x2-r*2,y2-r*2,x2,y2,start=270,extent=90,fill=fill,outline='',tags=tag)
  if outline:self.canvas.create_rectangle(x1+2,y1+2,x2-2,y2-2,outline=outline,width=width,tags=tag)
 def text(self,x,y,s,size=12,fill=CREAM,weight='bold',anchor='nw',tag='ui',width=None):
  self.canvas.create_text(x,y,text=s,font=('Consolas',size,weight),fill=fill,anchor=anchor,tags=tag,width=width)
 def image(self,name,x,y,tag='world'):
  if name in self.img:self.canvas.create_image(int(x),int(y),image=self.img[name],anchor='s',tags=tag)
 def render(self,now):
  c=self.canvas;c.delete('all')
  self.image('bg_'+self.scene,0,0) if False else None
  c.create_image(0,0,image=self.img['bg_'+self.scene],anchor='nw',tags='world')
  if self.scene=='town':
   self.text(237,80,'THE LAST SPOON',13,BG,anchor='center',tag='world')
   self.text(743,77,'GREY\'S SHOP',12,BG,anchor='center',tag='world')
   self.image('grey',720,344);self.image('lola',475,399);self.image('madeline',586,360);self.image('chester',375,388)
   self.render_marker(240,284,'E  ENTER');self.render_marker(28,370,'← MEADOW')
   self.render_marker(919,370,'BOSS →' if self.boss_unlocked else 'LOCKED →')
  elif self.scene=='meadow':
   self.render_marker(916,370,'TOWN →')
   for i,plot in enumerate(self.plots):
    x=[365,452,539][i]
    if plot['crop']:
     progress=clamp((time.time()-plot['ready']+12)/12,0,1)
     if progress>=1:self.image(plot['crop'] if plot['crop'] in self.img else 'broccoli',x,313)
     else:
      c.create_line(x,325,x,313-progress*14,fill='#42ac65',width=5,tags='world');c.create_oval(x-7,308,x+7,321,fill='#8ade78',outline='#376f59',width=2,tags='world')
     self.text(x,265,'READY!' if progress>=1 else str(math.ceil(plot['ready']-time.time()))+'s',10,MINT,anchor='center',tag='world')
    else:
     self.text(x,265,'PLOT '+str(i+1),10,GOLD,anchor='center',tag='world')
   for m in self.monsters:
    if not m['alive']:continue
    self.image(m['type'],m['x'],m['y']+math.sin(now*4+m['phase'])*2)
    c.create_rectangle(m['x']-18,m['y']-61,m['x']+18,m['y']-56,fill='#293b52',outline='#fff1c0',tags='world')
    c.create_rectangle(m['x']-16,m['y']-60,m['x']-16+(32*m['hp']/(3 if m['type']=='broccoli' else 2)),m['y']-57,fill='#fd8d84',outline='',tags='world')
  elif self.scene=='restaurant':
   self.text(747,137,'COOKING STATION',12,BG,anchor='center',tag='world')
   self.text(457,210,'SERVE HERE',13,BG,anchor='center',tag='world')
   self.render_marker(740,270,'E  COOK');self.render_marker(458,327,'E  SERVE');self.render_marker(702,400,'E  UPGRADE');self.render_marker(476,463,'E  EXIT')
   for i in range(self.upgrades):
    x=78+i*65
    self.canvas.create_oval(x,50,x+18,67,fill='#ffe59b',outline='#f28e95',width=3,tags='world')
   if self.sales>0:self.image('dish',100,108)
  elif self.scene=='boss':
   self.image('cake_strawberry' if self.boss_changed else 'cake',self.boss_x,self.boss_y)
   c.create_rectangle(297,32,661,57,fill='#27334f',outline='#ffdbad',width=3,tags='world')
   c.create_rectangle(302,37,302+354*max(0,self.boss_hp)/(17 if self.boss_changed else 12),52,fill='#f883a0' if self.boss_changed else '#f6b36f',outline='',tags='world')
   self.text(480,13,'LADY CAKE  •  '+self.boss_mode,12,CREAM,anchor='center',tag='world')
   self.render_marker(53,359,'← ESCAPE')
   if self.boss_warning:
    warning=self.boss_warning;act=warning['act'];target=(warning['tx'],warning['ty'])
    if act=='shockwave':c.create_oval(self.boss_x-150,self.boss_y-150,self.boss_x+150,self.boss_y+150,outline='#ed6283',width=5,dash=(10,8),tags='world')
    elif act=='charge':c.create_oval(target[0]-56,target[1]-56,target[0]+56,target[1]+56,outline='#e96b7a',width=4,dash=(6,5),tags='world')
    else:c.create_line(self.boss_x,self.boss_y,target[0],target[1],fill='#ef8ca0',dash=(4,6),width=4,tags='world')
   for b in self.boss_bullets:c.create_oval(b['x']-9,b['y']-9,b['x']+9,b['y']+9,fill='#fff0ce',outline='#db5d87',width=3,tags='world')
   self.text(480,475,'K  OFFER STRAWBERRY     •     T  CHANGE BOSS POLICY',12,CREAM,anchor='center',tag='world')
  if self.hp>0 and (now>=self.invuln_until or (self.tick_count//3)%2==0):self.image('hero_'+self.face,self.x,self.y+math.sin(self.walking*13)*1.6)
  for x,y,ending in self.hit_fx:
   if ending>now:
    c.create_arc(x-42,y-40,x+42,y+44,start=30,extent=120,style='arc',outline='#fff2bf',width=7,tags='world')
  for x,y,vx,vy,expire,color in self.particles:
   rem=max(0,expire-now);xx=x+vx*(.6-rem);yy=y+vy*(.6-rem)
   c.create_rectangle(xx-3,yy-3,xx+3,yy+3,fill=color,outline='',tags='world')
  self.render_hud()
  if now<self.notice_until:self.rounded(145,456,815,493,'#213d52','#f8d294',7,2,'notification');self.text(480,474,self.notice,12,CREAM,anchor='center',tag='notification',width=630)
  if self.modal:self.render_modal()

 def render_marker(self,x,y,s):
  w=max(83,len(s)*8+16)
  self.rounded(x-w/2,y-19,x+w/2,y+7,'#293f56','#f0ce8a',5,1,'world')
  self.text(x,y-13,s,10,CREAM,anchor='n',tag='world')

 def render_hud(self):
  c=self.canvas
  c.create_rectangle(0,504,960,600,fill='#203952',outline='#f4c98a',width=3,tags='ui')
  c.create_rectangle(0,507,960,513,fill='#325c65',outline='',tags='ui')
  self.text(25,519,'THE LAST SPOON',14,'#ffe4ad');self.text(25,540,'SEASONING TOWN  /  '+self.scene.upper(),9,'#9adbc0')
  for i in range(self.max_hp):self.image('heart_small',277+i*30,546,'ui') if i<self.hp else self.text(277+i*30,531,'♡',24,'#7299a3')
  self.image('coin_small',483,555,'ui');self.text(510,532,str(self.coins),15,GOLD)
  self.text(598,520,'★  '+str(self.renown)+' RENOWN',13,'#ffcb8b')
  self.text(598,541,'LV '+str(self.upgrades+1)+' RESTAURANT',10,MUTED)
  # clickable footer controls
  for x,y,w,s in [(16,569,166,'E  INTERACT'),(192,569,160,'J  ATTACK'),(362,569,177,'Q  QUESTS'),(550,569,185,'TAB  BAG'),(747,569,196,'ESC  MENU')]:
   c.create_rectangle(x,y,x+w,y+23,fill='#385771',outline='#5b8c89',width=1,tags='ui')
   self.text(x+w/2,y+5,s,10,CREAM,anchor='n')
  self.text(957,18,'FEAST  OR  FIEND',12,'#fff0bb',anchor='ne',tag='ui')

 def render_modal(self):
  c=self.canvas;c.create_rectangle(0,0,960,504,fill='#0c2032',stipple='gray50',outline='',tags='modal')
  self.rounded(150,100,810,488,'#243c54','#ffd69b',14,3,'modal')
  c.create_rectangle(169,119,792,163,fill='#416d72',outline='#7db69a',width=2,tags='modal')
  self.text(185,128,self.modal[1],17,'#fff0c8',tag='modal')
  option_count=min(len(self.modal_options),4)
  option_top=305 if option_count>=4 else 340 if option_count==3 else 380
  approx_lines=sum(max(1,math.ceil(len(line)/64)) for line in self.modal[2].split('\n'))
  body_size=11 if approx_lines>=9 else 12
  self.text(188,175,self.modal[2],body_size,'#ecf5dc',tag='modal',width=590)
  self.modal_selected=getattr(self,'modal_selected',0)
  for i,s in enumerate(self.modal_options[:4]):
   yy=option_top+i*37
   color='#527d70' if self.modal_selected==i else '#324c65'
   c.create_rectangle(200,yy,760,yy+32,fill=color,outline='#a6c7a8',width=2,tags='modal')
   self.text(218,yy+8,str(i+1)+'. '+s,11,CREAM,tag='modal')
  self.text(481,475,'ENTER to continue   •   1–4 choose   •   ESC close',10,'#a9c8c7',anchor='center',tag='modal')

 def run(self):
  now=time.monotonic();dt=min(.07,now-self.last);self.last=now
  if not self.modal:self.update(dt,now)
  self.render(now)
  self.root.after(33,self.run)

def main():
 root=tk.Tk()
 try:
  game=Game(root);root.protocol('WM_DELETE_WINDOW',lambda:(game.save(),root.destroy()))
  root.mainloop()
 except tk.TclError as e:
  print('GUI error:',e)
  raise

if __name__=='__main__':main()