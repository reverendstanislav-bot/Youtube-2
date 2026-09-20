#!/usr/bin/env python3
import argparse, json, re
from pathlib import Path

KEYWORDS=[
 "subtitle","caption","srt","ass","vtt","transcript","word_level","word level",
 "final_upload","final upload","upload master","master","ffmpeg","remotion",
 "premiere","resolve","voiceover","voice over","narration","burn","timing","sync"
]
TEXT_EXT={".md",".txt",".json",".csv",".srt",".ass",".vtt",".sbv",".py",".js",".jsx",".ts",".tsx",".ps1",".sh",".yaml",".yml"}

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--root",required=True)
    ap.add_argument("--report",required=True)
    ap.add_argument("--index",required=True)
    a=ap.parse_args()
    root=Path(a.root)
    rows=[]; matches=[]
    for p in sorted(root.rglob("*")):
        if not p.is_file() or p.suffix.lower() not in TEXT_EXT: continue
        rel=str(p.relative_to(root))
        size=p.stat().st_size
        rows.append({"path":rel,"size_bytes":size})
        if size>8_000_000: continue
        try: txt=p.read_text(encoding="utf-8",errors="replace")
        except: continue
        low=txt.lower()
        hit=[k for k in KEYWORDS if k in low]
        if hit:
            excerpts=[]
            lines=txt.splitlines()
            rx=re.compile("|".join(re.escape(k) for k in hit),re.I)
            for i,line in enumerate(lines):
                if rx.search(line):
                    clean=line.strip()
                    if clean:
                        excerpts.append({"line":i+1,"text":clean[:500]})
                    if len(excerpts)>=12: break
            matches.append({"path":rel,"size_bytes":size,"keywords":hit,"excerpts":excerpts})
    Path(a.index).write_text(json.dumps({"files":rows,"keyword_matches":matches},ensure_ascii=False,indent=2),encoding="utf-8")
    important=sorted(matches,key=lambda m:(0 if re.search(r"(subtitle|caption|transcript|final|upload|master)",m["path"],re.I) else 1,m["path"].lower()))
    out=["# Chicago source text/build/subtitle audit","",f"- Extracted text/project files: **{len(rows)}**",f"- Files with relevant keyword matches: **{len(matches)}**",""]
    out += ["## Relevant files and excerpts",""]
    for m in important[:120]:
        out.append(f"### \`{m['path']}\`")
        out.append("Keywords: "+", ".join(m["keywords"]))
        for e in m["excerpts"][:8]:
            out.append(f"- L{e['line']}: {e['text']}")
        out.append("")
    Path(a.report).write_text("\n".join(out),encoding="utf-8")
if __name__=="__main__": main()
