import bpy,json,sys,time
from pathlib import Path
R=Path(__file__).resolve().parent
scene=bpy.context.scene
data=json.loads((R/'frame_manifest.json').read_text())
preview='preview' in sys.argv
selected=[next(x for x in data if x['shot']==n and x['cut']==c) for n,c in [(1,1),(4,1),(4,4),(7,3),(8,1),(11,2),(12,4),(13,4),(15,3),(16,5),(18,2),(19,3),(20,3),(22,4)]] if preview else data
dest=R/('preview' if preview else 'frames');dest.mkdir(exist_ok=True)
started=time.time()
for k,item in enumerate(selected):
 f=item['frame'];out=dest/f'{f:04}.png'
 if out.exists() and not preview:continue
 scene.frame_set(f);scene.camera=bpy.data.objects[item['camera']];scene.render.filepath=str(out)
 bpy.ops.render.render(write_still=True)
 if k%36==0 or k==len(selected)-1:
  status=dict(state='rendered' if k==len(selected)-1 else 'rendering',frame=f,completed=k+1,total=len(selected),elapsed=round(time.time()-started,1))
  (R/('preview-status.json' if preview else 'render-status.json')).write_text(json.dumps(status));print('PROGRESS',status,flush=True)
