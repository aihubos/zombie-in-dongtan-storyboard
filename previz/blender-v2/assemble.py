from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import json,subprocess,numpy as np,wave
R=Path(__file__).resolve().parent
plan=json.loads((R.parent/'EP01_압축_씬데이터.json').read_text());frames=json.loads((R/'frame_manifest.json').read_text())
FONT='/System/Library/Fonts/AppleSDGothicNeo.ttc'
small=ImageFont.truetype(FONT,20);body=ImageFont.truetype(FONT,28);large=ImageFont.truetype(FONT,42)
def wrap(d,text,font,width):
 lines=[];line=''
 for c in text:
  if d.textlength(line+c,font=font)>width:lines.append(line);line=''
  line+=c
 if line:lines.append(line)
 return lines
def overlay(im,item):
 im=im.convert('RGB');d=ImageDraw.Draw(im);n=item['shot'];job=plan['scenes'][n-1]
 a,b=map(int,job['start'].split(':'));u=(item['time']-60*a-b)/job['duration']
 d.rectangle((0,0,1280,74),fill=(16,24,34));d.text((24,9),'좀비 인 동탄  EP.01  |  아빠의 약 · 7번이 나왔다',font=body,fill='white')
 d.text((24,46),f"BLENDER 동작·카메라 프리비즈  ·  S{n:02} C{item['cut']:02}  ·  {item['move']} / {item['angle']} / {item['framing']}",font=small,fill=(139,206,235))
 d.text((1130,15),f"{int(item['time'])//60:02}:{int(item['time'])%60:02}",font=body,fill='white')
 d.rectangle((0,602,1280,720),fill=(16,24,34))
 desc=item['description'].split('[추가 콘티:')[0]
 for i,line in enumerate(wrap(d,desc,small,1230)[:1]):d.text((24,611),line,font=small,fill=(170,190,202))
 dialogue=[l.strip() for l in job['dialogue'].split('\n') if l.strip() and not l.startswith('없음')]
 line=dialogue[min(len(dialogue)-1,int(u*len(dialogue)))] if dialogue else '릴리 · 회색  /  서진 · 노랑·빨강  /  루나 · 회색·청록  /  아빠는 은신처에'
 for i,ln in enumerate(wrap(d,line,body,1230)[:2]):d.text(((1280-d.textlength(ln,font=body))/2,643+i*31),ln,font=body,fill=(248,248,245))
 if n==1 and item['cut']>=3:d.text((25,95),'CCTV · 동탄 상가',font=body,fill='white')
 if n==2 and item['cut'] in [2,3]:
  d.rounded_rectangle((310,160,970,465),20,fill=(238,241,244));d.text((350,192),'긴급재난문자',font=large,fill=(25,33,42));d.text((350,280),'동탄 일대 외출을 자제하시고',font=body,fill=(25,33,42));d.text((350,328),'큰 소리를 내지 마십시오.',font=body,fill=(163,33,40))
 if n==2 and item['cut']==5:
  d.rectangle((0,74,1280,602),fill=(16,24,34));d.text((445,240),'좀비 인 동탄',font=large,fill='white');d.text((445,320),'EP.01 · 사흘 뒤',font=body,fill=(152,208,231))
 if n==4 and item['cut']==1:d.text((30,95),'닫힌 방문 너머 아빠의 기침 · 39.4℃ · 빈 해열제',font=body,fill='white',stroke_width=1,stroke_fill='black')
 if n==22 and item['cut']==5:
  d.rectangle((0,74,1280,602),fill=(8,11,18));d.text((455,270),'다음 화에 계속',font=large,fill='white')
 d.rectangle((0,716,int(1280*item['time']/151),719),fill=(89,173,235))
 return im
# Keep dialogue as Korean captions. No new voice or BGM is introduced.
def tc(t):
 ms=round(t*1000);return f'{ms//3600000:02}:{ms//60000%60:02}:{ms//1000%60:02},{ms%1000:03}'
srt=[]
for job in plan['scenes']:
 a,b=map(int,job['start'].split(':'));start=60*a+b;lines=[l for l in job['dialogue'].split('\n') if l and not l.startswith('없음')]
 for i,line in enumerate(lines):srt.append(f'{len(srt)+1}\n{tc(start+i*job["duration"]/len(lines))} --> {tc(start+(i+1)*job["duration"]/len(lines))}\n{line}\n')
(R/'EP01_대사.srt').write_text('\n'.join(srt))
rate=48000;mix=np.zeros((151*rate,2),dtype=np.float32);events=[]
def source(name):
 raw=subprocess.check_output(['ffmpeg','-v','error','-i',str(R/'audio'/name),'-f','f32le','-ac','2','-ar',str(rate),'-'])
 return np.frombuffer(raw,dtype='<f4').reshape(-1,2).copy()
def add(name,start,gain=.4,trim=True):
 snd=source(name);peak=float(np.max(np.abs(snd)))
 if trim:
  onset=np.where(np.max(np.abs(snd),axis=1)>max(.015,peak*.08))[0]
  if len(onset):snd=snd[max(0,int(onset[0])-240):]
 snd*=gain/max(.1,peak);fade=min(len(snd)//2,2400);snd[:fade]*=np.linspace(0,1,fade)[:,None];snd[-fade:]*=np.linspace(1,0,fade)[:,None]
 offset=int(start*rate);length=min(len(snd),len(mix)-offset)
 if length>0:mix[offset:offset+length]+=snd[:length]
 events.append(dict(file=name,start=start,gain=gain,seconds=length/rate))
for t in range(13,149,7):add('lakeside.wav',t,.055,False)
for name,t,g in [('cough.wav',20.2,.22),('sign-crash.wav',29,.6),('phone-alarm.wav',54.6,.4),('phone-alarm.wav',57.2,.3),('roulette.wav',67.5,.4),('roulette.wav',74,.4),('sign-crash.wav',62,.32),('suit-assemble.wav',80.5,.6),('suit-assemble.wav',84,.4),('sign-crash.wav',89,.35),('web-zip.wav',94.5,.35),('web-zip.wav',98,.45),('web-zip.wav',102,.5),('web-zip.wav',105,.45),('web-zip.wav',110,.42),('web-zip.wav',115,.5),('web-zip.wav',119,.45),('suit-assemble.wav',125,.35),('roulette.wav',144.3,.45)]:add(name,t,g)
for t in [6,34,37,40,43,47,50,58,65,90,146]:add('running.wav',t,.26)
# The sign crash's one-second silence is intentional; the cliffhanger cuts abruptly.
mix[int(30.5*rate):int(31.5*rate)]=0;mix[int(149*rate):]=0
peak=float(np.max(np.abs(mix)));mix*=min(1,.88/max(.001,peak))
with wave.open(str(R/'EP01_sfx.wav'),'wb') as w:w.setnchannels(2);w.setsampwidth(2);w.setframerate(rate);w.writeframes((mix*32767).astype('<i2').tobytes())
(R/'audio_timeline.json').write_text(json.dumps(dict(events=events,peak_before_gain=peak,peak_after_gain=float(np.max(np.abs(mix))),bgm=False,dialogue='Korean subtitles',listening_review='not_performed'),ensure_ascii=False,indent=2))
cmd=['ffmpeg','-y','-v','error','-f','rawvideo','-pix_fmt','rgb24','-s','1280x720','-r','12','-i','-','-i',str(R/'EP01_sfx.wav'),'-map','0:v','-map','1:a','-c:v','libx264','-preset','fast','-crf','22','-pix_fmt','yuv420p','-r','24','-c:a','aac','-b:a','160k','-t','151','-movflags','+faststart',str(R/'EP01_블렌더_프리비즈_v2.mp4')]
p=subprocess.Popen(cmd,stdin=subprocess.PIPE)
try:
 for i,item in enumerate(frames):
  with Image.open(R/'frames'/f'{item["frame"]:04}.png') as im:out=overlay(im,item)
  p.stdin.write(out.tobytes())
  if i%120==0:print('ENCODE',i,len(frames),flush=True)
finally:p.stdin.close()
if p.wait()!=0:raise RuntimeError('FFmpeg encoding failed')
samples=[]
for no in range(1,23):
 group=[x for x in frames if x['shot']==no];item=group[len(group)//2]
 with Image.open(R/'frames'/f'{item["frame"]:04}.png') as im:img=overlay(im,item)
 img.save(R/f'S{no:02}.jpg',quality=88);samples.append(img.resize((320,180)))
contact=Image.new('RGB',(1280,6*180),(16,24,34))
for i,im in enumerate(samples):contact.paste(im,((i%4)*320,(i//4)*180))
contact.save(R/'EP01_전체장면.jpg',quality=90)
print('COMPLETE',flush=True)
