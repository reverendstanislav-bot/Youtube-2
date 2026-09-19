#!/usr/bin/env python3
import argparse, math, random, struct, wave
from pathlib import Path

SR=48000
DUR=55.0

def env(t):
    fi=min(1.0,t/4.0)
    fo=min(1.0,max(0.0,(DUR-t)/8.0))
    return fi*fo

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--output",required=True)
    args=ap.parse_args()
    Path(args.output).parent.mkdir(parents=True,exist_ok=True)
    rng=random.Random(4977)
    noise=0.0
    freqs=[55.0,82.5,110.0,164.81,220.0]
    amps=[0.21,0.15,0.095,0.045,0.025]
    bells=[(8.0,329.63),(23.0,440.0),(38.0,329.63)]
    with wave.open(args.output,"wb") as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
        frames=bytearray()
        for i in range(int(DUR*SR)):
            t=i/SR
            e=env(t)
            drift=0.78+0.22*math.sin(2*math.pi*0.021*t+0.4)
            s=0.0
            for k,(f,a) in enumerate(zip(freqs,amps)):
                s += a*math.sin(2*math.pi*f*t + k*0.71)
            noise=0.9986*noise+0.0014*rng.uniform(-1,1)
            s=(s*drift + 0.10*noise)
            for bt,bf in bells:
                dt=t-bt
                if 0<=dt<2.8:
                    s += 0.045*math.sin(2*math.pi*bf*dt)*math.exp(-dt*2.2)
            s*=0.42*e
            l=max(-0.9,min(0.9,s))
            r=max(-0.9,min(0.9,s*0.985 + 0.008*math.sin(2*math.pi*0.13*t)))
            frames += struct.pack("<hh",int(l*32767),int(r*32767))
            if len(frames)>=SR*4:
                w.writeframes(frames); frames.clear()
        if frames: w.writeframes(frames)
    print("OUTRO_MUSIC_READY",args.output)

if __name__=="__main__":
    main()
