#!/usr/bin/env python3
import argparse, math, wave
from pathlib import Path
import numpy as np

SR=48000
DUR=180.0

def lp_noise(rng,n,alpha=0.997):
    x=rng.normal(0,1,n).astype(np.float32)
    y=np.empty_like(x); y[0]=x[0]
    for i in range(1,n):
        y[i]=alpha*y[i-1]+(1-alpha)*x[i]
    y/=max(1e-6,float(np.max(np.abs(y))))
    return y

def write(path,mono):
    mono=np.clip(mono,-.92,.92)
    # subtle stereo width without phasey tricks
    left=mono
    right=np.roll(mono,37)*.985
    st=np.stack([left,right],axis=1)
    pcm=(st*32767).astype(np.int16)
    with wave.open(str(path),"wb") as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes())

def fade_edges(x,sec=4.0):
    n=min(len(x)//2,int(sec*SR))
    if n>1:
        r=np.linspace(0,1,n,dtype=np.float32)
        x[:n]*=r; x[-n:]*=r[::-1]
    return x

def ambient(t,rng):
    n=len(t)
    noise=lp_noise(rng,n,.9982)
    root=0.36*np.sin(2*np.pi*43.0*t)
    fifth=0.19*np.sin(2*np.pi*64.5*t+0.73)
    upper=0.07*np.sin(2*np.pi*86.0*t+1.4)
    slow=(0.60+0.40*np.sin(2*np.pi*0.031*t+0.6))
    x=(root+fifth+upper)*slow + .14*noise
    return fade_edges(.22*x)

def pulse(t,rng):
    n=len(t)
    noise=lp_noise(rng,n,.9965)
    base=.26*np.sin(2*np.pi*52*t)+.12*np.sin(2*np.pi*78*t+.5)
    gate=(np.maximum(0,np.sin(2*np.pi*0.78*t))**6)
    pulse=.22*gate*np.sin(2*np.pi*104*t)
    # sparse metallic transients, deterministic
    clicks=np.zeros(n,dtype=np.float32)
    for sec in np.arange(2.4,DUR,7.8):
        i=int(sec*SR); L=min(int(.11*SR),n-i)
        if L>0:
            tt=np.arange(L,dtype=np.float32)/SR
            clicks[i:i+L]+=0.20*np.sin(2*np.pi*420*tt)*np.exp(-tt*38)
    x=base+.14*noise+pulse+clicks
    return fade_edges(.20*x)

def sky(t,rng):
    n=len(t)
    air=lp_noise(rng,n,.9990)
    low=.24*np.sin(2*np.pi*39*t)+.10*np.sin(2*np.pi*58.5*t+1.0)
    thump=(np.maximum(0,np.sin(2*np.pi*3.15*t))**8)*np.sin(2*np.pi*46*t)
    swell=(0.48+0.52*np.sin(2*np.pi*.018*t-.8))
    x=(low*swell)+.15*air+.10*thump
    return fade_edges(.21*x)

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--out-dir",required=True)
    args=ap.parse_args()
    out=Path(args.out_dir); out.mkdir(parents=True,exist_ok=True)
    t=np.arange(int(DUR*SR),dtype=np.float32)/SR
    rng=np.random.default_rng(497)
    write(out/"ambient_original.wav",ambient(t,rng))
    write(out/"engineering_pulse_original.wav",pulse(t,rng))
    write(out/"sky_tension_original.wav",sky(t,rng))
    print("ORIGINAL_MUSIC_READY",out)

if __name__=="__main__": main()
