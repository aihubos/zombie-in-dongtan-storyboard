def mat(o,m):o.data.materials.append(MAT[m]);return o

def cube(name,loc,scale,m,parent=None):
 bpy.ops.mesh.primitive_cube_add(size=1,location=loc);o=bpy.context.object;o.name=name;o.scale=scale;mat(o,m)
 if parent:o.parent=parent
 return o

def sphere(name,loc,scale,m,parent=None):
 bpy.ops.mesh.primitive_uv_sphere_add(segments=12,ring_count=8,radius=1,location=loc);o=bpy.context.object;o.name=name;o.scale=scale;mat(o,m)
 if parent:o.parent=parent
 return o

def empty(name,loc=(0,0,0),parent=None):
 o=bpy.data.objects.new(name,None);scene.collection.objects.link(o);o.location=loc
 if parent:o.parent=parent
 return o

def cylinder(name,a,b,r,m,parent=None):
 a=Vector(a);b=Vector(b);d=b-a
 bpy.ops.mesh.primitive_cylinder_add(vertices=10,radius=r,depth=d.length,location=(a+b)/2);o=bpy.context.object;o.name=name;o.rotation_euler=d.to_track_quat('Z','Y').to_euler();mat(o,m)
 if parent:o.parent=parent
 return o

def text(name,body,loc,size,m,parent=None):
 d=bpy.data.curves.new(name,'FONT');d.body=body;d.align_x='CENTER';d.size=size;d.extrude=.002
 o=bpy.data.objects.new(name,d);scene.collection.objects.link(o);o.location=loc;mat(o,m)
 if parent:o.parent=parent
 return o

def key(o,f,rotation=True,scale=False):
 o.keyframe_insert('location',frame=f)
 if rotation:o.keyframe_insert('rotation_euler',frame=f)
 if scale:o.keyframe_insert('scale',frame=f)

def person(name,color,h):
 root=empty('CHAR_'+name);s=h/1.8
 torso=sphere(name+'_torso',(0,0,1.13*s),(.23*s,.14*s,.36*s),color,root)
 head=sphere(name+'_head',(0,0,1.62*s),(.17*s,.15*s,.21*s),'skin' if color!='zombie' else 'zombie',root)
 sphere(name+'_hair',(0,.025*s,1.76*s),(.175*s,.145*s,.10*s),'hair',root)
 for x in [-.059,.059]:sphere(name+'_eye',(x*s,-.139*s,1.65*s),(.021*s,.016*s,.022*s),'dark',root)
 # a tiny nose marks facing direction
 sphere(name+'_nose',(0,-.165*s,1.59*s),(.035*s,.045*s,.036*s),'skin' if color!='zombie' else 'zombie',root)
 limbs={}
 for side,sgn in [('L',-1),('R',1)]:
  arm=empty(name+'_arm_'+side,(sgn*.27*s,0,1.38*s),root)
  cylinder(name+'_upperarm_'+side,(0,0,0),(0,0,-.29*s),.067*s,color,arm)
  fore=empty(name+'_elbow_'+side,(0,0,-.29*s),arm)
  cylinder(name+'_forearm_'+side,(0,0,0),(0,0,-.27*s),.057*s,color,fore)
  sphere(name+'_hand_'+side,(0,0,-.3*s),(.075*s,.063*s,.08*s),'skin' if color!='zombie' else 'zombie',fore)
  leg=empty(name+'_hip_'+side,(sgn*.105*s,0,.88*s),root)
  cylinder(name+'_thigh_'+side,(0,0,0),(0,0,-.4*s),.09*s,'pants',leg)
  knee=empty(name+'_knee_'+side,(0,0,-.4*s),leg)
  cylinder(name+'_shin_'+side,(0,0,0),(0,0,-.38*s),.074*s,'pants',knee)
  cube(name+'_shoe_'+side,(0,-.055*s,-.42*s),(.18*s,.30*s,.11*s),'dark',knee)
  limbs[side]=(arm,fore,leg,knee)
 return {'root':root,'limbs':limbs,'s':s,'head':head}

def animate_person(p,f,loc,mode='idle',phase=0,face=-math.pi/2):
 r=p['root'];r.location=loc;r.rotation_euler=(0,0,face)
 if mode=='run':r.location.z+=.065*abs(math.sin(phase));r.rotation_euler.x=.12
 if mode=='sit':r.location.z-=.38
 key(r,f)
 for side,sgn in [('L',1),('R',-1)]:
  a,e,l,k=p['limbs'][side];a.rotation_euler=(0,0,0);e.rotation_euler=(0,0,0);l.rotation_euler=(0,0,0);k.rotation_euler=(0,0,0)
  if mode in ['walk','run']:
   v=math.sin(phase)*sgn;strength=.8 if mode=='run' else .36
   l.rotation_euler.x=v*strength;k.rotation_euler.x=max(0,-v)*.9
   a.rotation_euler.x=-v*strength;e.rotation_euler.x=-.6 if mode=='run' else -.16
  elif mode=='sit':l.rotation_euler.x=-1.40;k.rotation_euler.x=.45;a.rotation_euler.x=-.7;e.rotation_euler.x=-.4
  elif mode=='magic':a.rotation_euler.x=-1.30-(.16 if side=='R' else 0);a.rotation_euler.y=sgn*.20;e.rotation_euler.x=-.25
  elif mode=='brace':a.rotation_euler.x=-1.3;e.rotation_euler.x=-.3
  elif mode=='hug':a.rotation_euler.x=-1.0;a.rotation_euler.y=sgn*.8
  elif mode=='zombie':a.rotation_euler.x=-1.1+math.sin(phase)*.15;l.rotation_euler.x=math.sin(phase)*sgn*.65;k.rotation_euler.x=max(0,-math.sin(phase)*sgn)*.7
  for ob in [a,e,l,k]:ob.keyframe_insert('rotation_euler',frame=f)