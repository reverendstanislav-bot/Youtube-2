#!/usr/bin/env python3
import argparse, json, re
from collections import Counter, defaultdict
from pathlib import Path

MEDIA_VIDEO={".mp4",".mov",".mkv",".avi",".m4v",".webm"}
MEDIA_AUDIO={".wav",".mp3",".aac",".m4a",".flac",".ogg"}
SUBS={".srt",".ass",".vtt",".sbv",".ttml"}
TEXT={".md",".txt",".json",".csv",".py",".js",".jsx",".ts",".tsx",".ps1",".sh",".yaml",".yml"}
ARCH={".zip",".rar",".7z",".tar",".gz"}

def parse_slt(path):
    lines=Path(path).read_text(encoding="utf-8",errors="replace").splitlines()
    recs=[]; cur={}
    started=False
    for line in lines:
        if line.startswith("----------"):
            started=True; cur={}
            continue
        if not started: 
            continue
        if not line.strip():
            if cur.get("Path"):
                recs.append(cur)
            cur={}
            continue
        if " = " in line:
            k,v=line.split(" = ",1); cur[k]=v
    if cur.get("Path"): recs.append(cur)
    out=[]
    for r in recs:
        p=r.get("Path","")
        attrs=r.get("Attributes","")
        is_dir=("D" in attrs and not r.get("Size")) or p.endswith("/") or p.endswith("\\")
        try: size=int(r.get("Size","0") or 0)
        except: size=0
        out.append({"path":p,"size_bytes":size,"is_dir":is_dir,"packed_size":r.get("Packed Size")})
    return out

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--slt",required=True)
    ap.add_argument("--out",required=True)
    ap.add_argument("--summary",required=True)
    a=ap.parse_args()
    recs=parse_slt(a.slt)
    files=[r for r in recs if not r["is_dir"]]
    ext=Counter()
    groups=defaultdict(list)
    for r in files:
        e=Path(r["path"]).suffix.lower()
        ext[e or "<none>"]+=1
        if e in MEDIA_VIDEO: groups["video"].append(r)
        if e in MEDIA_AUDIO: groups["audio"].append(r)
        if e in SUBS: groups["subtitles"].append(r)
        if e in TEXT: groups["text_project"].append(r)
        if e in ARCH: groups["archives"].append(r)
    def top(xs,n=100): return sorted(xs,key=lambda x:x["size_bytes"],reverse=True)[:n]
    name_terms=re.compile(r"(final|upload|master|review|export|subtitle|caption|transcript|voice|vo\b|timeline|premiere|resolve|remotion|ffmpeg|render)",re.I)
    interesting=[r for r in files if name_terms.search(r["path"])]
    data={
      "total_entries":len(recs),
      "file_count":len(files),
      "directory_count":len(recs)-len(files),
      "unpacked_total_bytes":sum(r["size_bytes"] for r in files),
      "extensions":dict(ext.most_common()),
      "video_files":top(groups["video"],200),
      "audio_files":top(groups["audio"],200),
      "subtitle_files":top(groups["subtitles"],200),
      "project_text_files":top(groups["text_project"],500),
      "nested_archives":top(groups["archives"],100),
      "interesting_name_matches":top(interesting,300),
      "largest_files":top(files,100)
    }
    Path(a.out).write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding="utf-8")
    lines=[
      "# Chicago canonical source archive — content audit","",
      f"- Files: **{data['file_count']}**",
      f"- Directories: **{data['directory_count']}**",
      f"- Unpacked payload represented by archive listing: **{data['unpacked_total_bytes']:,} bytes**","",
      "## Key project assets","",
      f"- Video files: **{len(groups['video'])}**",
      f"- Audio files: **{len(groups['audio'])}**",
      f"- Subtitle files (.srt/.ass/.vtt/...): **{len(groups['subtitles'])}**",
      f"- Project/text/script files: **{len(groups['text_project'])}**",
      f"- Nested archives: **{len(groups['archives'])}**","",
      "## Largest video candidates",""
    ]
    for r in top(groups["video"],30):
        lines.append(f"- \`{r['path']}\` — {r['size_bytes']:,} bytes")
    lines += ["","## Subtitle files",""]
    if groups["subtitles"]:
        for r in sorted(groups["subtitles"],key=lambda x:x["path"].lower())[:100]:
            lines.append(f"- \`{r['path']}\` — {r['size_bytes']:,} bytes")
    else: lines.append("- No standalone subtitle files found by extension.")
    lines += ["","## Names relevant to final/export/subtitle/transcript/build",""]
    for r in sorted(interesting,key=lambda x:x["path"].lower())[:200]:
        lines.append(f"- \`{r['path']}\` — {r['size_bytes']:,} bytes")
    lines += ["","Full machine-readable inventory: \`SOURCE_INVENTORY.json\`."]
    Path(a.summary).write_text("\n".join(lines)+"\n",encoding="utf-8")
if __name__=="__main__": main()
