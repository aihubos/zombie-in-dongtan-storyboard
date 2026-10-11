import bpy
from pathlib import Path
r=Path(__file__).resolve().parent
s=bpy.context.scene
s.sequence_editor_create()
strip=s.sequence_editor.strips.new_sound('EP01 SFX · no BGM',str(r/'EP01_sfx.wav'),channel=1,frame_start=1)
strip.sound.pack()
s.render.use_sequencer=False
s['audio_note']='Packed SFX synced at frame 1; subtitles are composed in assemble.py.'
s.frame_set(1)
bpy.ops.wm.save_as_mainfile(filepath=str(r/'EP01_151초_프리비즈.blend'))
print('FINALIZED',len(s.timeline_markers),s.frame_end,strip.frame_final_duration,strip.sound.packed_file is not None)
