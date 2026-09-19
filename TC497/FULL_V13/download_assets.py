#!/usr/bin/env python3
import subprocess
from pathlib import Path

def curl(url, out):
    out=Path(out)
    out.parent.mkdir(parents=True,exist_ok=True)
    subprocess.run(['curl','-fL','--retry','4','--retry-all-errors',url,'-o',str(out)],check=True)

def quoted_url(line):
    if "https://" not in line:
        return None
    parts=line.split("'")
    for part in parts:
        if part.startswith("https://"):
            return part
    return None

def main():
    text=Path('.github/workflows/build_tc497_final_1080.yml').read_text()
    seen={}
    vpairs=[]

    for line in text.splitlines():
        url=quoted_url(line)
        if not url:
            continue
        if '$V4_EXTRA/' in line:
            name=line.split('$V4_EXTRA/',1)[1].split('"',1)[0]
            seen[name]=url
        if '/tmp/tc497master/v5patch/' in line:
            name=line.split('/tmp/tc497master/v5patch/',1)[1].strip().split()[0].strip('"')
            vpairs.append((url,name))

    if len(seen)<39:
        raise SystemExit(f'Expected >=39 unique V4 extras, found {len(seen)}')
    for name,url in sorted(seen.items()):
        curl(url,Path('/tmp/v13/v4extra')/name)

    if len(vpairs)<5:
        raise SystemExit(f'Expected V5 patch assets, found {len(vpairs)}')
    for url,name in vpairs:
        curl(url,Path('/tmp/v13/v5patch')/name)

    text2=Path('.github/workflows/build_tc497_final_v9_1080_surgical.yml').read_text()
    need={'electric_human_v6.png','electric_wheel_v6.png'}
    found={}
    for line in text2.splitlines():
        url=quoted_url(line)
        if not url or '/tmp/work/assets/' not in line:
            continue
        name=line.split('/tmp/work/assets/',1)[1].strip().split()[0].strip('"')
        if name in need:
            found[name]=url
    missing=need-set(found)
    if missing:
        raise SystemExit('Missing V6 URLs: '+','.join(sorted(missing)))
    for name,url in found.items():
        curl(url,Path('/tmp/v13/patch')/name)

    print('downloaded',len(seen),'V4 extras and',len(vpairs)+len(found),'patch assets')

if __name__=='__main__':
    main()
