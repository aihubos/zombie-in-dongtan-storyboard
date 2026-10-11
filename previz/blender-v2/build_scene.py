import bpy, math, json, random
from pathlib import Path
from mathutils import Vector
R=Path(__file__).resolve().parent
PLAN=json.loads((R.parent/'EP01_압축_씬데이터.json').read_text())
FPS=12
bpy.ops.wm.read_factory_settings(use_empty=True)
scene=bpy.context.scene;scene.name='EP01_151_SECONDS'
scene.render.engine='BLENDER_WORKBENCH'
scene.render.resolution_x=1280;scene.render.resolution_y=720;scene.render.resolution_percentage=100
scene.render.fps=FPS;scene.frame_start=1;scene.frame_end=151*FPS
scene.render.image_settings.file_format='PNG';scene.render.image_settings.color_mode='RGB';scene.render.image_settings.compression=15
sh=scene.display.shading;sh.light='STUDIO';sh.color_type='MATERIAL';sh.show_shadows=True;sh.show_cavity=True;sh.cavity_type='BOTH';sh.show_object_outline=True
sh.background_type='WORLD';scene.world=bpy.data.worlds.new('Sunset');scene.world.color=(.29,.21,.27)
scene.view_settings.view_transform='Standard';MAT={}
colors={'stone':(.43,.44,.45),'building':(.32,.36,.40),'glass':(.17,.37,.44),'lake':(.23,.48,.58),'rail':(.73,.75,.76),'wood':(.56,.36,.23),'lily':(.58,.60,.62),'jin':(.99,.81,.38),'skin':(.88,.67,.51),'dark':(.04,.055,.07),'hair':(.14,.065,.03),'zombie':(.38,.44,.38),'pants':(.14,.16,.19),'purple':(.43,.13,.67),'white':(.94,.92,.85),'red':(.73,.045,.04),'green':(.16,.49,.20),'gold':(.94,.63,.15),'teal':(.05,.66,.69),'dog':(.45,.47,.50),'beige':(.70,.61,.46),'orange':(.95,.39,.12)}
for name,c in colors.items():
 m=bpy.data.materials.new(name);m.diffuse_color=(*c,1);MAT[name]=m
exec((R/'primitives.py').read_text(),globals())
def ground(x):return -max(0,min(20,x))*.18
def vis(root,yes,f):
 for ob in [root,*root.children_recursive]:
  if ob.get('_visible')!=int(yes):
   ob.hide_render=not yes;ob.hide_viewport=not yes;ob.keyframe_insert('hide_render',frame=f);ob.keyframe_insert('hide_viewport',frame=f);ob['_visible']=int(yes)
def linkline(o,a,b,r,f):
 a,b=Vector(a),Vector(b);v=b-a;o.location=(a+b)/2;o.rotation_euler=v.to_track_quat('Z','Y').to_euler();o.scale=(r,r,max(.0001,v.length));key(o,f,scale=True)
def line(name,material):return cylinder(name,(0,0,0),(0,0,1),1,material)
def label(name,body,loc,size=.5):
 o=text(name,body,loc,size,'white');o.rotation_euler=(math.pi/2,0,0);return o
# Geography: shop at the upper plaza, ramp descending east, deck and lake below.
cube('Upper plaza',(-9,0,-.22),(22,10,.4),'stone')
o=cube('Ramp',(10,0,-2.0),(20.33,10,.35),'stone');o.rotation_euler.y=math.atan(.18)
cube('Deck',(29,0,-3.82),(18,10,.4),'wood');cube('Lake',(9,-28,-4.25),(115,45,.2),'lake')
for x in range(-18,37,3):
 for y in [-4.8,4.8]:
  cylinder('Rail post',(x,y,ground(x)),(x,y,ground(x)+1),.05,'rail')
  cylinder('Rail top',(x,y,ground(x)+1),(x+3,y,ground(x+3)+1),.06,'rail')
for x in [-15,-8,0,10,20,30]:
 z=ground(x);cube('Shop',(x,8,z+3),(6,5,6),'building');cube('Window',(x,5.46,z+2.4),(5.2,.08,3.5),'glass')
 cube('Awning',(x,4.8,z+4.7),(6,1.4,.15),'orange')
label('Lakmong','LAKMONG',(-8,5.3,5.1),.68)
for x in [-12,-4,24,33]:
 z=ground(x);cube('Bench',(x,3,z+.5),(2,.55,.15),'wood')
 for dx in [-.7,.7]:cube('Bench leg',(x+dx,3,z+.25),(.09,.4,.5),'dark')
for x in [-14,0,12,25,34]:
 z=ground(x);cylinder('Lamp',(x,3.8,z),(x,3.8,z+3.8),.07,'dark');sphere('Lamp bulb',(x,3.8,z+3.9),(.26,.26,.22),'gold')
cube('Planter',(-2,2.7,.4),(3,1,.8),'wood');sphere('Shrub',(-2,2.7,1.0),(1.5,.55,.5),'green')
# Closed-door shelter; father is intentionally absent from the scene graph.
cube('Shelter floor',(-48,0,-.2),(10,9,.35),'wood');cube('Shelter wall',(-48,3,2),(10,.25,4),'building')
cube('Closed bedroom door',(-46,2.8,1.3),(1.35,.1,2.6),'wood');label('Door label','DAD RESTING',(-46,2.72,2.8),.22)
cube('Table',(-49,1,.65),(2.2,1,.12),'white');cube('Empty medicine',(-49.5,1,.85),(.45,.23,.3),'red')
therm=cube('Thermometer',(-48.6,.65,.8),(.60,.12,.10),'white');label('Temperature','39.4 C',(-48.6,.57,.91),.16)
# Pharmacy stage has no wall between the camera and the performers.
cube('Pharmacy floor',(-29,0,-.18),(9,8,.3),'white');cube('Pharmacy shelf',(-29,2,1.2),(7,.45,2.4),'wood')
for i in range(12):cube('Medicine box',(-32+(i%6)*1.1,1.7,.6+(i//6)*1.1),(.35,.25,.55),'white' if i%2 else 'teal')
label('Pharmacy sign','PHARMACY',(-29,1.65,2.9),.6)
# News stage and anchor are physically separate from the family.
cube('News floor',(-70,0,-.2),(12,8,.3),'dark');cube('News backdrop',(-70,3,2),(11,.2,4),'glass')
cube('News desk',(-70,0,.5),(3,1,1),'white');label('News title','DONGTAN  /  BREAKING NEWS',(-70,2.8,2.8),.45)
anchor=person('ANCHOR','lily',1.8);anchor['root'].location=(-70,.65,0)
lily=person('LILY','lily',1.63);jin=person('JIN','jin',1.22)
# Distinctive wardrobe and rounded child head; low-poly blocking, not facial likeness.
jin['head'].scale.x*=1.15;jin['head'].scale.z*=.95
for side in ['L','R']:
 for suffix in ['thigh_'+side,'shin_'+side]:
  ob=bpy.data.objects.get('JIN_'+suffix);ob.data.materials.clear();ob.data.materials.append(MAT['beige'])
for z in [.80,.90,1.0,1.1,1.2]:cube('Lily shirt stripe',(0,-.125,z),(.27,.025,.035),'white',lily['root'])
sphere('Lily long hair',(0,.10,1.35),(.18,.14,.32),'hair',lily['root'])
bag=cube('Medicine crossbody bag',(.25,-.09,.80),(.30,.16,.27),'dark',lily['root'])
cylinder('Bag strap',(-.22,-.16,1.35),(.27,-.16,.87),.018,'dark',lily['root'])
pack=cube('Dinosaur backpack',(0,.18,.75),(.31,.19,.38),'green',jin['root'])
for z in [.62,.75,.88]:sphere('Backpack spine',(0,.31,z),(.06,.055,.055),'gold',jin['root'])
# Luna: narrow greyhound body, long legs, folded ears, teal harness.
dog=empty('LUNA');sphere('Luna body',(0,0,.34),(.16,.29,.19),'dog',dog)
sphere('Luna neck',(0,-.19,.49),(.10,.12,.21),'dog',dog);sphere('Luna head',(0,-.27,.64),(.095,.12,.10),'dog',dog)
sphere('Luna muzzle',(0,-.38,.61),(.055,.13,.05),'dog',dog)
for side in [-1,1]:
 sphere('Folded ear',(side*.07,-.20,.70),(.055,.085,.025),'dark',dog)
 sphere('Dog eye',(side*.07,-.33,.66),(.014,.016,.014),'dark',dog)
 for y in [-.18,.17]:cylinder('Luna leg',(side*.105,y,.30),(side*.11,y-.03,0),.022,'dog',dog)
cylinder('Tail',(0,.25,.40),(.04,.53,.30),.018,'dog',dog)
cylinder('Harness',(0,-.18,.56),(0,-.28,.29),.025,'teal',dog)
for side in [-1,1]:cylinder('Harness Y',(0,-.18,.56),(side*.145,-.12,.28),.019,'teal',dog)
# Props.
sign=empty('SIGN');cube('White sign',(0,0,.85),(1.3,.1,1.6),'orange',sign);cube('Sign face',(0,-.06,.85),(1.12,.04,1.40),'white',sign)
for x in [-.53,.53]:cylinder('Sign leg',(x,-.35,0),(x,0,1.65),.04,'dark',sign)
phone=cube('PHONE',(0,0,0),(.16,.045,.29),'dark');cube('Phone screen',(0,-.026,0),(.13,.01,.23),'teal',phone)
medicine=empty('MEDICINE');cube('Medicine A',(-.12,0,0),(.21,.14,.32),'white',medicine);cube('Medicine B',(.12,0,0),(.21,.14,.32),'red',medicine)
watch=empty('PURPLE_JESTER_WATCH');sphere('Purple watch strap',(0,0,0),(.10,.06,.07),'purple',watch);sphere('Watch face',(0,-.05,.035),(.074,.028,.063),'white',watch);sphere('Red nose button',(0,-.083,.035),(.022,.018,.023),'red',watch)
roulette=empty('CRAZY_SLOT_PHYSICAL_POPUP');sphere('Ivory face',(0,0,0),(.24,.17,.28),'white',roulette)
for side in [-1,1]:
 sphere('Jester eye',(side*.08,-.15,.09),(.03,.025,.045),'dark',roulette)
 o=sphere('Purple hat',(side*.19,0,.25),(.14,.12,.24),'purple',roulette);o.rotation_euler.y=side*.6
 sphere('Hat bell',(side*.29,0,.38),(.052,.05,.055),'gold',roulette)
sphere('Jester red nose',(0,-.19,.02),(.055,.035,.05),'red',roulette)
cube('Mouth slot',(0,-.165,-.12),(.25,.04,.16),'dark',roulette);cylinder('Brass handle',(0,0,-.26),(0,0,-.7),.035,'gold',roulette)
digits={}
for char in '123456789?':
 d=text('SLOT_'+char,char,(0,-.196,-.17),.145,'gold',roulette);d.rotation_euler=(math.pi/2,0,0);digits[char]=d
# Wearable red/gold armor follows the articulated character.
armor=empty('JIN_SUIT',parent=jin['root']);sphere('Red chest',(0,0,.77),(.19,.13,.25),'red',armor)
sphere('Gold chest',(0,-.118,.82),(.12,.025,.12),'gold',armor)
suit_parts=[armor]
for side in ['L','R']:
 arm,fore,leg,knee=jin['limbs'][side]
 for parent,loc,scale in [(arm,(0,0,-.10),(.065,.065,.13)),(fore,(0,0,-.11),(.065,.065,.13)),(leg,(0,0,-.15),(.079,.075,.17)),(knee,(0,0,-.14),(.07,.07,.15))]:
  ob=sphere('Armor plate',loc,scale,'red',parent);suit_parts.append(ob)
spiders=[]
for i,(side,z) in enumerate([(-1,.95),(1,.95),(-1,.68),(1,.68)]):
 pivot=empty('Spider leg pivot '+str(i),(side*.12,.22,z),armor)
 cylinder('Gold mech inner',(0,0,0),(side*.4,.13,.35 if z>.8 else -.15),.036,'gold',pivot)
 cylinder('Gold mech outer',(side*.4,.13,.35 if z>.8 else -.15),(side*.67,-.20,.08 if z>.8 else -.49),.029,'gold',pivot)
 sphere('Mechanical joint',(side*.4,.13,.35 if z>.8 else -.15),(.05,.05,.05),'dark',pivot);spiders.append(pivot)
shards=[sphere('Armor fragment '+str(i),(0,0,0),(.05,.04,.09),'gold' if i%2 else 'red') for i in range(14)]
web=line('WEB_SHOT','white');zipline=line('WEB_ZIPLINE','white');net=empty('WEB_NET')
for y in [-4,-3,-2,-1,0,1,2,3,4]:cylinder('Web vertical',(2,y,ground(2)+.1),(2,y,ground(2)+2.3),.018,'white',net)
for z in [.1,.5,.9,1.3,1.7,2.1]:cylinder('Web horizontal',(2,-4,ground(2)+z),(2,4,ground(2)+z),.018,'white',net)
tangle=empty('TANGLED_WEB',parent=jin['root'])
for i in range(7):cylinder('Tangled silk',(-.27,-.23,.3+i*.09),(.27,-.23,.6+i*.045),.014,'white',tangle)
zombies=[person('ZOMBIE_%02d'%i,'zombie',1.67+(i%3)*.07) for i in range(16)]
frames=[];cutidx=0;start=0
for no,job in enumerate(PLAN['scenes'],1):
 print('BUILD',no,flush=True);elapsed=0
 for ci,c in enumerate(job['cuts']):
  cutidx+=1;first=round((start+elapsed)*FPS)+1;elapsed+=c['sec'];last=round((start+elapsed)*FPS)
  cd=bpy.data.cameras.new('Lens_%03d'%cutidx);cam=bpy.data.objects.new('CAM_%03d_S%02d'%(cutidx,no),cd);scene.collection.objects.link(cam);cd.lens=42;cd.clip_start=.02;cd.clip_end=240
  marker=scene.timeline_markers.new('S%02d C%02d %s'%(no,ci+1,c['move']),frame=first);marker.camera=cam
  for f in range(first,last+1):
   t=(f-1)/FPS;u=(t-start)/job['duration'];v=(f-first)/max(1,last-first)
   x=-3.;z=0.;mode='idle'
   if no==4:x=-48 if ci<3 else -29
   if no==5:x=-6+u*2;mode='walk'
   if no==7:x=-6+u*3;mode='run' if u<.7 else 'idle'
   if no==17:x=-2+max(0,u-.5)*12;z=1.1-.115*x if u>.5 else 0
   if no==18:x=4+u*20;z=1.1-.115*x
   if no>=19:x=25;z=-3.6
   if no==19:z=(-1.66*(1-min(1,u*4))+-3.6*min(1,u*4))
   jl=Vector((x,-.8,z));ll=Vector((x-.55,.45,z))
   if no in [17,18]:ll=jl+Vector((-.30,.40,-.05))
   if no==10:ll=Vector((x+.25,-.1,z-.25))
   if no==20:ll=jl+Vector((-.35,.10,0))
   animate_person(jin,f,jl,'magic' if no in [11,12,15,16,17,18,22] else ('hug' if no==20 else mode),t*10)
   animate_person(lily,f,ll,'brace' if no in [10,14] else ('hug' if no in [17,18,20] else mode),t*10+1)
   if no==13:jin['root'].location.z+=.12*math.sin(u*math.pi);key(jin['root'],f)
   family=no>=4
   vis(jin['root'],family,f);vis(lily['root'],family,f);vis(dog,family,f)
   dog.location=ll+Vector((0,-.24,.95)) if 7<=no<=19 else jl+Vector((.25,-.75,0))
   if no in [10,11,12]:dog.location=jl+Vector((0,-.22,.30))
   dog.rotation_euler=(0,0,-math.pi/2);key(dog,f)
   watch.location=jl+Vector((.16,-.29,.84));watch.rotation_euler.z=-.15;key(watch,f);vis(watch,family,f)
   active_suit=13<=no<=18 or (no==19 and u<.45)
   for ob in suit_parts:vis(ob,active_suit,f)
   for i,p in enumerate(spiders):p.rotation_euler.y=math.sin(t*2+i)*.12;p.keyframe_insert('rotation_euler',frame=f)
   vis(tangle,no==15 and u<.55,f)
   pop=no in [11,12,13,14,22];vis(roulette,pop,f)
   roulette.location=watch.location+Vector((0,-.15,.28+(.35*min(1,u*3) if no in [11,22] else .35)))
   roulette.scale=(1,1,1) if no not in [11,22] else (max(.04,min(1,u*4)),)*3;key(roulette,f,scale=True)
   digit='7' if no in [13,14] else str(int(t*15)%9+1)
   if no==12:digit='5' if u<.2 else '6' if u<.4 else '7' if u<.55 else '8' if u<.68 else '7'
   if no==22:digit='?'
   for val,ob in digits.items():vis(ob,pop and val==digit,f)
   sign.location=(-4,1,0) if no<10 else (-.2,0,0)
   sign.rotation_euler=(0,math.pi/2*min(1,max(0,(u-.15)*4)) if no==5 else math.pi/2 if 6<=no<10 else 0,0)
   if no==10:sign.location.x=-4+min(1,u*2)*3.8
   if no>=16:sign.rotation_euler.y=math.pi/2
   key(sign,f);vis(sign,5<=no<=18,f)
   phone.location=ll+Vector((0,-.2,1.2))
   if no==9:
    p=max(0,min(1,(u-.2)*2));phone.location=ll+Vector(((-9-ll.x)*p,(3-ll.y)*p,1.2+math.sin(p*math.pi)*1.8-.6*p))
   if no>9:phone.location=(-9,3,.6)
   key(phone,f);vis(phone,9<=no<=18,f)
   medicine.location=ll+Vector((.18,-.27,.95));key(medicine,f);vis(medicine,no in [4,20],f)
   vis(net,16<=no<=20,f);net.scale=(1,1,max(.01,min(1,u*3))) if no==16 else (1,1,1);key(net,f,scale=True)
   vis(web,no in [15,16,17],f);linkline(web,jl+Vector((.2,-.35,.93)),(25,-.35,.1) if no!=16 else (2,-4+8*u,1.5),.02,f)
   vis(zipline,17<=no<=19,f);linkline(zipline,(-2,-.8,2.65),(25,-.8,-.45),.028,f)
   for i,o in enumerate(shards):
    vis(o,no in [13,19],f);a=i*2.4+t*4;r=.7*(1-u) if no==13 else .3+u*.6
    o.location=jl+Vector((math.cos(a)*r,math.sin(a)*r,.35+(i%5)*.22));o.scale=(.05*(1-u*.7),.04,.07);key(o,f,scale=True)
   for i,p in enumerate(zombies):
    side=-1 if i<8 else 1;j=i%8;zx=-11+j*.8 if side<0 else 7+j*.8;zy=(j%3-1)*1.1
    if 6<=no<=15:
     progress=min(1,(no-6+u)/8);zx=(-11+6*progress-j*.42) if side<0 else (7-5*progress+j*.40)
    if no>=9 and side<0:zx=-9+(j%3)*.45;zy=2.4+(j//3)*.5
    if 16<=no<=20:zx=2.45+(j//3)*.6;zy=(j%3-1)*1.1
    if no>=21:zx=32+j*.7-(u*2 if no==22 else 0);zy=(j%3-1)*1.1
    animate_person(p,f,(zx,zy,ground(zx)),'zombie' if no>=6 else 'walk',t*(10 if no>=6 else 3)+i,math.pi/2 if side<0 else -math.pi/2)
    vis(p['root'],no in [1,2,3] or 6<=no<=22,f)
   # Subject-led cameras. Wide group framing takes priority over tiny inserts.
   txt=c['txt'];fr=c['frame'];target=jl+Vector((-.15,.25,1.0));subject='family'
   if fr in ['클로즈업','빅 클로즈업','익스트림 클로즈업','인서트','미디엄 클로즈업']:
    if '릴리' in txt:target=ll+Vector((0,-.05,1.42));subject='face'
    else:target=jl+Vector((0,-.05,1.08));subject='face'
    if any(k in txt for k in ['슬롯','숫자','피에로']):target=roulette.location.copy();subject='slot'
    if any(k in txt for k in ['손목','버튼','시계']):target=watch.location.copy();subject='watch'
    if '간판' in txt:target=sign.location+Vector((0,0,.8));subject='sign'
    if '휴대폰' in txt:target=phone.location.copy();subject='phone'
   if no==1:
    target=Vector((-70,0,1.3)) if ci<2 else zombies[8]['root'].location+Vector((0,0,1.0));subject='news' if ci<2 else 'crowd'
   if no in [2,3,6]:target=zombies[8]['root'].location+Vector((0,0,1));subject='crowd'
   if no==8:target=Vector((-1,0,1));subject='geography'
   if no==4 and ci==0:target=Vector((-48,.7,1.2));subject='shelter'
   if no==12:target=roulette.location.copy();subject='slot'
   if no==13:target=jl+Vector((0,0,.85));subject='transform'
   if no==16 and ci>=3:target=Vector((2,0,.8));subject='net'
   if no in [17,18]:target=(jl+ll)/2+Vector((0,0,.85));subject='escape'
   if no==21:target=Vector((33,0,-2.5));subject='crowd'
   if no==22:target=roulette.location.copy();subject='slot'
   dist={'익스트림 와이드':20,'와이드':11,'미디엄 와이드':8,'풀샷':6,'쓰리샷':6.5,'투샷':5,'미디엄':4,'미디엄 클로즈업':2.6,'클로즈업':1.8,'빅 클로즈업':1.3,'익스트림 클로즈업':1,'인서트':1.1}.get(fr,6)
   if subject in ['geography','crowd','net']:dist=max(dist,10)
   if subject in ['escape','transform','shelter']:dist=max(dist,5.5)
   if subject=='slot':dist=2.2 if no==22 else 1.65
   if subject=='watch':dist=1.0
   if subject=='news':dist=7
   az=-1.35;el=.18
   if c['angle'] in ['하이 앵글','탑다운']:el=.65 if c['angle']=='하이 앵글' else 1.2
   if subject=='geography':el=1.15;dist=17
   if subject in ['slot','watch']:az=-math.pi/2;el=.08
   move=c['move']
   if '아크' in move or '헬릭스' in move:az+=(v-.5)*.7
   if '인' in move:dist*=1.15-.25*v
   if '아웃' in move:dist*=.90+.30*v
   if '크레인' in move:el+=(v-.5)*.25
   pos=target+Vector((math.cos(az)*math.cos(el)*dist,math.sin(az)*math.cos(el)*dist,math.sin(el)*dist))
   if '핸드헬드' in move:pos+=Vector((.025*math.sin(t*25),0,.025*math.cos(t*30)))
   cam.location=pos;cam.rotation_euler=(target-pos).to_track_quat('-Z','Y').to_euler();key(cam,f)
   frames.append(dict(frame=f,shot=no,cut=ci+1,cut_global=cutidx,time=t,camera=cam.name,move=move,angle=c['angle'],framing=fr,description=txt,dialogue=job['dialogue']))
 start+=job['duration']
for action in bpy.data.actions:
 for layer in action.layers:
  for strip in layer.strips:
   for slot in action.slots:
    bag=strip.channelbag(slot)
    if bag:
     for curve in bag.fcurves:
      for pt in curve.keyframe_points:pt.interpolation='CONSTANT' if curve.data_path.startswith('hide_') else 'LINEAR'
scene.frame_set(1);scene.camera=bpy.data.objects[frames[0]['camera']]
scene['duration_seconds']=151;scene['story']='Medicine mission; Jin suit 7; Lily and Luna zipline; father off-screen';scene['cuts']=cutidx
(R/'frame_manifest.json').write_text(json.dumps(frames,ensure_ascii=False))
bpy.ops.wm.save_as_mainfile(filepath=str(R/'EP01_151초_프리비즈.blend'))
print('SAVED',len(frames),'frames',cutidx,'cuts',len(scene.objects),'objects',flush=True)
