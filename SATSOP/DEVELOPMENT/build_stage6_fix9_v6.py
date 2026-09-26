from pathlib import Path
import hashlib, json, subprocess

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "STAGE_6" / "FINAL28_V5"
OUT = ROOT / "STAGE_6" / "FIX9_V6"
OUT.mkdir(parents=True, exist_ok=True)

def run(name, vf, source=None):
    out=OUT/name
    cmd=["ffmpeg","-y"]
    cmd += (["-i",str(source)] if source else ["-f","lavfi","-i","color=c=0x161b1d:s=1344x752:r=1"])
    cmd += ["-vf",vf,"-frames:v","1",str(out)]
    subprocess.run(cmd,check=True,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
    return {"filename":name,"size_bytes":out.stat().st_size,"sha256":hashlib.sha256(out.read_bytes()).hexdigest()}

grid=",".join([f"drawbox=x=0:y={y}:w=1344:h=1:c=0x202628:t=fill" for y in range(0,752,32)])
recs=[]

f=[grid]
for i,x in enumerate([120,420,720,1020]):
    f += [f"drawbox=x={x}:y=230:w=190:h=290:c=0x2d3436:t=fill",f"drawbox=x={x}:y=230:w=190:h=5:c=0x687779:t=fill",f"drawbox=x={x}:y=515:w=190:h=5:c=0x687779:t=fill"]
    if i<3: f += [f"drawbox=x={x+210}:y=371:w=65:h=8:c=0xf28a3a:t=fill"]
recs.append(run("SAT-GEN022_FIX_GFX.png",",".join(f)))

recs.append(run("SAT-GEN043_FIX_GFX.png",grid+",drawbox=x=160:y=500:w=380:h=110:c=0x687779:t=fill,drawbox=x=790:y=350:w=380:h=260:c=0x796349:t=fill,drawbox=x=610:y=220:w=110:h=420:c=0x1f2527:t=fill,drawbox=x=642:y=390:w=46:h=60:c=0xf28a3a:t=fill"))
recs.append(run("SAT-GEN046_FIX_GFX.png",grid+",drawbox=x=170:y=180:w=350:h=430:c=0x687779:t=fill,drawbox=x=170:y=180:w=350:h=140:c=0xf28a3a:t=fill,drawbox=x=760:y=340:w=350:h=270:c=0xd2c9b2:t=fill,drawbox=x=600:y=150:w=5:h=490:c=0x414b4d:t=fill"))

f=[grid,"drawbox=x=670:y=120:w=5:h=520:c=0xf28a3a:t=fill"]
for r in range(4):
    for c in range(5): f += [f"drawbox=x={100+c*100}:y={170+r*105}:w=75:h=75:c=0x687779:t=fill"]
for r in range(2):
    for c in range(2): f += [f"drawbox=x={930+c*100}:y={380+r*105}:w=75:h=75:c=0xd2c9b2:t=fill"]
recs.append(run("SAT-GEN050_FIX_GFX.png",",".join(f)))

vf=grid+",drawbox=x=100:y=576:w=480:h=8:c=0xf2f2ed:t=fill,drawbox=x=760:y=576:w=480:h=8:c=0xf2f2ed:t=fill,drawbox=x=150:y=410:w=95:h=170:c=0x687779:t=fill,drawbox=x=280:y=340:w=95:h=240:c=0x687779:t=fill,drawbox=x=410:y=450:w=95:h=130:c=0x687779:t=fill,drawbox=x=850:y=500:w=300:h=8:c=0xd2c9b2:t=fill,drawbox=x=850:y=500:w=8:h=80:c=0xd2c9b2:t=fill,drawbox=x=1142:y=500:w=8:h=80:c=0xd2c9b2:t=fill"
recs.append(run("SAT-GEN053_FIX_GFX.png",vf))

vf=grid+",drawbox=x=120:y=385:w=1100:h=70:c=0x687779:t=fill"
for x in [190,430,720,980]: vf += f",drawbox=x={x}:y=220:w=150:h=130:c=0xd2c9b2:t=fill,drawbox=x={x+72}:y=350:w=7:h=35:c=0xf28a3a:t=fill"
recs.append(run("SAT-GEN064_FIX_GFX.png",vf))

manifest={"status":"6 deterministic GFX fixes built; 3 Higgsfield replacements tracked separately","technical":{"width":1344,"height":752,"format":"PNG"},"files":recs}
(OUT/"FIX9_V6_DETERMINISTIC_MANIFEST.json").write_text(json.dumps(manifest,indent=2),encoding="utf-8")
