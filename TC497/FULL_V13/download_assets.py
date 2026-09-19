#!/usr/bin/env python3
import re, subprocess
from pathlib import Path

def curl(url, out):
    out=Path(out)
    out.parent.mkdir(parents=True,exist_ok=True)
    subprocess.run(['curl','-fL','--retry','4','--retry-all-errors',url,'-o',str(out)],check=True)

def main():
    text=Path('.github/workflows/build_tc497_final_1080.yml').read_text()

    # V4_EXTRA assets.
    pattern=re.compile(r"'(https://d8j0ntlcm91z4\.cloudfront\.net/[^']+)'\s+-o\s+"\$V4_EXTRA/([^"]+)"",re.S)
    pairs=pattern.findall(text)
    seen={name:url for url,name in pairs}
    if len(seen)<39:
        raise SystemExit(f'Expected >=39 unique V4 extras, found {len(seen)}')
    for name,url in sorted(seen.items()):
        curl(url,Path('/tmp/v13/v4extra')/name)

    # Five retained V5/V6 correction assets.
    pattern2=re.compile(r"'(https://d8j0ntlcm91z4\.cloudfront\.net/[^']+)'\s+-o\s+/tmp/tc497master/v5patch/([^\s]+)",re.S)
    vpairs=pattern2.findall(text)
    if len(vpairs)<5:
        raise SystemExit(f'Expected V5 patch assets, found {len(vpairs)}')
    for url,name in vpairs:
        curl(url,Path('/tmp/v13/v5patch')/name)

    # Two corrected V6 Electric Wheel assets.
    text2=Path('.github/workflows/build_tc497_final_v9_1080_surgical.yml').read_text()
    for name in ['electric_human_v6.png','electric_wheel_v6.png']:
        pat=re.compile(r"'(https://d8j0ntlcm91z4\.cloudfront\.net/[^']+)'\s+-o\s+/tmp/work/assets/"+re.escape(name),re.S)
        m=pat.search(text2)
        if not m:
            raise SystemExit('Missing '+name+' URL')
        curl(m.group(1),Path('/tmp/v13/patch')/name)

    print('downloaded',len(seen),'V4 extras and',len(vpairs)+2,'patch assets')

if __name__=='__main__':
    main()
