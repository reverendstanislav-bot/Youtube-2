# Chicago R15 Smooth Remotion — transition design

Status: REVIEW BUILD SPEC

R15 is a transition/picture-motion correction of the current R14 editorial cut.

Locked:
- same approved source assets;
- same R14 phrase-driven timing;
- same word-level captions;
- same provenance logic;
- same approved AAC bit-for-bit;
- same 1920x1080 / 25 fps / 32,268-frame runtime;
- same Episode-1 textless end screen.

Picture changes only:
- no translate() motion;
- no horizontal pan;
- no vertical pan;
- no shake;
- no whip/slide transitions;
- no zoom-out / zoom-in bouncing;
- adjacent R14 segments using the same source asset are merged into one continuous visual group;
- different source assets transition with a 6-frame (240 ms) full-frame smooth dissolve centered on the original R14 cut;
- same-asset reframes become a slow continuous scale interpolation instead of a hard reframing cut;
- maximum additional reconstruction/concept breathing motion is 0.4% over a group;
- end screen enters with a 10-frame full-frame fade.

Goal: a continuous documentary-film feel without changing story, narration, captions, provenance, or approved audio.
