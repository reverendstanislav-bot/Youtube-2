#!/usr/bin/env python3
import argparse
from pathlib import Path

BASE = '&H00DDEBF3&'
RECON = '&H00708ED8&'
GOLD = '&H008EC5E0&'
BLUE = '&H00B6A89A&'

PATCHES = [
    {
        'segment_start': 261.533333,
        'visual_start': 261.771,
        'end': 269.100000,
        'label': 'RECONSTRUCTION',
        'color': RECON,
        'file': 'p1.ass',
    },
    {
        'segment_start': 295.966667,
        'visual_start': 295.972,
        'end': 300.866667,
        'label': 'DOCUMENT • U.S. PATENT',
        'color': GOLD,
        'file': 'p2.ass',
    },
    {
        'segment_start': 474.500000,
        'visual_start': 474.502,
        'end': 480.166667,
        'label': 'ARCHIVE • TC-497',
        'color': BLUE,
        'file': 'p3.ass',
    },
]

def ass_to_sec(x):
    h, m, s = x.split(':')
    return int(h) * 3600 + int(m) * 60 + float(s)

def sec_to_ass(t):
    t = max(0.0, float(t))
    h = int(t // 3600)
    t -= h * 3600
    m = int(t // 60)
    t -= m * 60
    return f'{h}:{m:02d}:{t:05.2f}'

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--source-ass', required=True)
    ap.add_argument('--out-dir', required=True)
    args = ap.parse_args()

    src = Path(args.source_ass).read_text(encoding='utf-8', errors='replace')
    head, sep, events = src.partition('[Events]')
    if not sep:
        raise SystemExit('ASS has no [Events] section')

    fmt = 'Format: Layer,Start,End,Style,Name,MarginL,MarginR,MarginV,Effect,Text'
    parsed = []
    for line in events.splitlines():
        if line.startswith('Format:'):
            fmt = line
            continue
        if not line.startswith('Dialogue:'):
            continue
        p = line.split(',', 9)
        if len(p) < 10:
            continue
        parsed.append(p)

    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    for patch in PATCHES:
        seg = patch['segment_start']
        ps = patch['visual_start']
        pe = patch['end']
        lines = []

        for p in parsed:
            if p[3] != 'CapV10':
                continue
            s = ass_to_sec(p[1])
            e = ass_to_sec(p[2])
            a = max(s, ps)
            b = min(e, pe)
            if b <= a:
                continue
            q = p.copy()
            q[1] = sec_to_ass(a - seg)
            q[2] = sec_to_ass(b - seg)
            lines.append(','.join(q))

        label_start = (ps - seg) + 0.18
        label_end = min(pe - seg, (ps - seg) + 2.65)
        lines.append(
            f"Dialogue: 115,{sec_to_ass(label_start)},{sec_to_ass(label_end)},"
            f"SourceV10,,0,0,0,,{{\\c{patch['color']}}}{patch['label']}{{\\c{BASE}}}"
        )

        out = head + '[Events]\n' + fmt + '\n' + '\n'.join(lines) + '\n'
        (out_dir / patch['file']).write_text(out, encoding='utf-8')
        print(patch['file'], len(lines))

if __name__ == '__main__':
    main()
