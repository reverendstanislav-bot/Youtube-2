#!/usr/bin/env python3
import argparse
import json
import subprocess
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ORANGE = "0xF28A3A"
CHARCOAL = "0x171A1C"
PAPER = "0xF3EBDD"
BLUE = "0x5F747D"

def ass_time(sec):
    cs = round(float(sec) * 100)
    h = cs // 360000
    cs %= 360000
    m = cs // 6000
    cs %= 6000
    s = cs // 100
    cs %= 100
    return f"{h}:{m:02d}:{s:02d}.{cs:02d}"

def ass_escape(value):
    return str(value).replace("\\", r"\\").replace("{", r"\{").replace("}", r"\}")

def display_word(value, replacements=None):
    token = str(value)
    if replacements and token in replacements:
        return str(replacements[token])
    return token

def _font(size, bold=False):
    name = "DejaVuSans-Bold.ttf" if bold else "DejaVuSans.ttf"
    return ImageFont.truetype(f"/usr/share/fonts/truetype/dejavu/{name}", size)

def _wrap(draw, text, font, max_width):
    words = str(text).split()
    lines=[]
    cur=""
    for word in words:
        test=(cur+" "+word).strip()
        box=draw.textbbox((0,0),test,font=font)
        if cur and box[2]-box[0] > max_width:
            lines.append(cur)
            cur=word
        else:
            cur=test
    if cur:
        lines.append(cur)
    return lines

def _center_lines(draw, lines, y, font, fill, gap=14):
    for line in lines:
        box=draw.textbbox((0,0),line,font=font)
        draw.text(((1080-(box[2]-box[0]))/2,y),line,font=font,fill=fill)
        y += (box[3]-box[1]) + gap
    return y

def make_editor_gfx(segment, out_path):
    kind=str(segment.get("gfx_type","")).lower()
    bg=(23,26,28)
    paper=(243,235,221)
    warm=(230,221,200)
    rust=(165,82,53)
    blue=(95,116,125)
    iron=(48,54,58)

    if kind.startswith("court_"):
        im=Image.new("RGB",(1080,1920),warm)
    else:
        im=Image.new("RGB",(1080,1920),bg)
    d=ImageDraw.Draw(im)

    if not kind.startswith("court_"):
        for x in range(80,1080,160):
            d.line((x,130,x,1240),fill=(43,49,52),width=2)
        for y in range(160,1240,160):
            d.line((60,y,1020,y),fill=(43,49,52),width=2)
        d.rectangle((60,120,72,1200),fill=rust)

    if kind=="origin":
        title=_font(62,True); sub=_font(36,False)
        _center_lines(d,["TELEPHONE FIRST"],260,title,paper)
        d.line((220,520,860,520),fill=blue,width=10)
        for x in range(250,851,120):
            d.ellipse((x-13,507,x+13,533),fill=warm)
        _center_lines(d,["UNDERGROUND CONDUITS","BECAME A FREIGHT RAILWAY"],690,sub,warm,24)
        d.line((230,980,850,980),fill=paper,width=8)
        d.line((230,1060,850,1060),fill=paper,width=8)
        d.line((500,985,500,1055),fill=rust,width=6)
        d.text((530,997),"2 FT LATER",font=_font(27,True),fill=rust)

    elif kind=="evidence_uncertain":
        title=_font(48,True); body=_font(34,False); small=_font(27,False)
        _center_lines(d,["WHAT THE EVIDENCE SUPPORTS"],250,title,paper)
        items=["1899 — TELEPHONE FRANCHISE","c.1900 — TUNNEL CONSTRUCTION","FREIGHT RAILWAY CAME AFTER"]
        y=510
        for item in items:
            d.ellipse((150,y+8,174,y+32),fill=rust)
            d.text((205,y),item,font=body,fill=warm)
            y+=120
        d.rounded_rectangle((135,930,945,1160),radius=22,outline=blue,width=4,fill=iron)
        _center_lines(d,["NO VERIFIED EVIDENCE","THAT RAILROAD WAS THE SECRET","PLAN FROM DAY ONE"],965,_font(31,True),paper,12)
        d.text((150,1210),"EDITORIAL EVIDENCE SUMMARY",font=small,fill=blue)

    elif kind=="gauge":
        title=_font(64,True); body=_font(34,False)
        _center_lines(d,["TWO-FOOT GAUGE"],260,title,paper)
        d.line((180,670,900,670),fill=paper,width=12)
        d.line((180,950,900,950),fill=paper,width=12)
        for x in range(220,900,110):
            d.line((x,640,x,980),fill=iron,width=8)
        d.line((540,700,540,920),fill=rust,width=7)
        d.polygon([(540,700),(522,738),(558,738)],fill=rust)
        d.polygon([(540,920),(522,882),(558,882)],fill=rust)
        box=d.textbbox((0,0),"24 IN / 2 FT",font=body)
        d.rectangle((515-(box[2]-box[0])/2,790,565+(box[2]-box[0])/2,850),fill=bg)
        d.text(((1080-(box[2]-box[0]))/2,794),"24 IN / 2 FT",font=body,fill=rust)
        _center_lines(d,["TRACK GAUGE","SCHEMATIC — NOT TO SCALE"],1110,_font(27,False),warm,12)

    elif kind=="obsolescence":
        _center_lines(d,["THE CITY KEPT CHANGING"],260,_font(54,True),paper)
        d.line((180,650,900,650),fill=paper,width=8)
        for x in (260,470,680):
            d.rectangle((x,560,x+130,640),outline=blue,width=6)
            d.ellipse((x+20,625,x+55,660),fill=paper)
            d.ellipse((x+80,625,x+115,660),fill=paper)
        d.line((280,940,800,940),fill=rust,width=8)
        d.line((280,1020,800,1020),fill=rust,width=8)
        _center_lines(d,["SURFACE LOGISTICS EVOLVED","THE TUNNELS REMAINED"],1120,_font(34,True),warm,18)

    elif kind=="network_flood":
        _center_lines(d,["ONE CONNECTED NETWORK"],240,_font(55,True),paper)
        nodes=[(260,570),(540,520),(820,620),(350,830),(650,860),(250,1090),(540,1110),(840,1030)]
        edges=[(0,1),(1,2),(0,3),(1,4),(3,4),(3,5),(4,6),(4,7),(6,7)]
        for a,b in edges:
            d.line((*nodes[a],*nodes[b]),fill=blue,width=18)
        for x,y in nodes:
            d.ellipse((x-28,y-28,x+28,y+28),fill=warm,outline=paper,width=5)
        for a,b in [(0,1),(1,4),(4,6),(6,7)]:
            d.line((*nodes[a],*nodes[b]),fill=rust,width=8)
        _center_lines(d,["BUILT TO MOVE FREIGHT","LATER ABLE TO MOVE WATER"],1240,_font(32,True),warm,14)

    elif kind=="road_compare":
        _center_lines(d,["ORDINARY HIGHWAY TRUCK"],240,_font(46,True),paper)
        d.line((120,560,960,560),fill=paper,width=6)
        d.line((120,640,960,640),fill=paper,width=6)
        d.rectangle((260,470,610,555),outline=warm,width=8)
        d.rectangle((610,510,760,555),outline=warm,width=8)
        d.ellipse((320,535,390,605),fill=iron,outline=paper,width=5)
        d.ellipse((650,535,720,605),fill=iron,outline=paper,width=5)
        d.text((340,710),"NEEDS A ROAD",font=_font(38,True),fill=rust)
        d.line((120,860,960,860),fill=blue,width=3)
        _center_lines(d,["TC-497"],940,_font(60,True),paper)
        d.line((180,1130,900,1130),fill=warm,width=14)
        for x in range(220,900,95):
            d.ellipse((x-28,1100,x+28,1156),fill=iron,outline=paper,width=4)
        _center_lines(d,["BUILT FOR ROADLESS TERRAIN"],1240,_font(34,True),warm)

    elif kind.startswith("terrain_"):
        label=kind.split("_",1)[1].upper()
        _center_lines(d,[label],250,_font(70,True),paper)
        if label=="RIVER":
            d.rectangle((100,690,980,1030),fill=blue)
            for y in range(730,1000,70):
                d.arc((150,y,930,y+90),0,180,fill=paper,width=4)
        elif label=="RIDGE":
            pts=[(80,1080),(300,760),(470,930),(650,610),(1000,1080)]
            d.line(pts,fill=warm,width=20,joint="curve")
            d.line((80,1080,1000,1080),fill=paper,width=5)
        elif label=="SOFT GROUND":
            d.rectangle((100,730,980,1080),fill=(75,75,66))
            for x in range(150,950,120):
                d.ellipse((x,820,x+90,900),outline=warm,width=5)
            d.text((250,1160),"WHEELS SINK • TRACTION FALLS",font=_font(30,True),fill=rust)
        elif label=="DUNES":
            d.arc((80,680,700,1200),185,350,fill=warm,width=20)
            d.arc((420,640,1030,1180),185,350,fill=paper,width=14)
        _center_lines(d,["THE TERRAIN STILL DECIDES"],1240,_font(31,True),rust)

    elif kind=="court_allegation":
        d.rectangle((0,0,1080,26),fill=rust)
        d.text((90,120),"DOCUMENT EXCERPT",font=_font(30,True),fill=rust)
        d.text((90,205),"IN RE CHICAGO FLOOD LITIGATION",font=_font(46,True),fill=(30,32,33))
        d.text((90,275),"ILLINOIS SUPREME COURT • 1997",font=_font(27,True),fill=blue)
        y=470
        lines=_wrap(d,"The complaints alleged that pile driving near the Kinzie Street bridge damaged or weakened the tunnel.",_font(38,False),880)
        y=_center_lines(d,lines,y,_font(38,False),(30,32,33),22)
        d.rounded_rectangle((90,980,990,1160),radius=18,outline=rust,width=5)
        _center_lines(d,["ALLEGATION IN A COMPLAINT","IS NOT A FINAL FINDING"],1020,_font(31,True),rust,14)
        d.text((90,1240),"176 Ill. 2d 179 (1997)",font=_font(27,False),fill=blue)

    elif kind=="court_correction":
        d.rectangle((0,0,1080,26),fill=rust)
        d.text((90,120),"LEGAL HISTORY",font=_font(30,True),fill=rust)
        d.text((90,205),"WHAT THE RECORD SUPPORTS",font=_font(48,True),fill=(30,32,33))
        y=470
        for line in ["PILE DRIVING OCCURRED","DAMAGE WAS ALLEGED","LIABILITY WAS LITIGATED"]:
            d.ellipse((105,y+8,131,y+34),fill=rust)
            d.text((165,y),line,font=_font(35,True),fill=(30,32,33))
            y+=125
        d.line((100,900,980,900),fill=blue,width=4)
        _center_lines(d,["DO NOT REDUCE THAT HISTORY TO","“A CONTRACTOR WAS DEFINITIVELY","FOUND RESPONSIBLE FOR THE FLOOD.”"],980,_font(29,True),(30,32,33),12)
        d.text((90,1240),"SOURCE: IN RE CHICAGO FLOOD LITIGATION",font=_font(24,False),fill=blue)
        d.text((90,1280),"176 Ill. 2d 179 (1997)",font=_font(24,False),fill=blue)

    else:
        raise ValueError(f"Unknown gfx_type: {kind}")

    im.save(out_path,quality=95)
    return Path(out_path)

def draw_escape(value):
    return (
        str(value)
        .replace("\\", "\\\\")
        .replace(":", "\\:")
        .replace("'", "\\'")
        .replace("%", "\\%")
    )

def is_sentence_end(token):
    return str(token).rstrip('"”').endswith((".", "!", "?"))

def normalize_words(words):
    out=[]
    i=0
    while i < len(words):
        cur=dict(words[i])
        token=str(cur.get("w",""))
        if i+1 < len(words):
            nxt=dict(words[i+1])
            nxt_token=str(nxt.get("w",""))
            if token=="turn" and nxt_token=="-o":
                cur["w"]="LeTourneau"
                cur["short_e"]=nxt["short_e"]
                out.append(cur); i+=2; continue
            if nxt_token.startswith("-") and token:
                cur["w"]=token+nxt_token
                cur["short_e"]=nxt["short_e"]
                out.append(cur); i+=2; continue
        out.append(cur); i+=1
    return out

def caption_groups(words):
    words=normalize_words(words)
    groups = []
    buf = []

    def flush():
        nonlocal buf
        if buf:
            groups.append(buf)
            buf = []

    for word in words:
        if buf and float(word["short_s"]) - float(buf[-1]["short_e"]) > 0.36:
            flush()
        buf.append(word)
        chars = sum(len(str(x["w"])) + 1 for x in buf)
        if len(buf) >= 5 or chars >= 29 or is_sentence_end(word["w"]):
            flush()

    flush()
    return groups

def balanced_split(group):
    if len(group) <= 3:
        return len(group)
    total = sum(len(str(x["w"])) + 1 for x in group)
    best_score = 10**9
    best_index = len(group)
    for i in range(1, len(group)):
        left = sum(len(str(x["w"])) + 1 for x in group[:i])
        right = total - left
        score = abs(left - right)
        if score < best_score:
            best_score = score
            best_index = i
    return best_index

def make_ass(words, out_path, duration, fps, replacements=None):
    header = """[Script Info]
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920
WrapStyle: 2
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name,Fontname,Fontsize,PrimaryColour,SecondaryColour,OutlineColour,BackColour,Bold,Italic,Underline,StrikeOut,ScaleX,ScaleY,Spacing,Angle,BorderStyle,Outline,Shadow,Alignment,MarginL,MarginR,MarginV,Encoding
Style: Cap,DejaVu Sans,66,&H00FFFFFF,&H00FFFFFF,&H00101416,&H90000000,-1,0,0,0,100,100,0,0,1,4.6,1.5,2,104,104,315,1

[Events]
Format: Layer,Start,End,Style,Name,MarginL,MarginR,MarginV,Effect,Text
"""
    raw=[]

    for group in caption_groups(words):
        visible_chars = sum(len(str(x["w"])) + 1 for x in group)
        split = balanced_split(group) if visible_chars > 21 else len(group)

        for active_index, active_word in enumerate(group):
            parts = []
            for index, item in enumerate(group):
                token = ass_escape(display_word(item["w"], replacements))
                if index == active_index:
                    token = r"{\c&H003A8AF2&}" + token + r"{\c&HFFFFFF&}"
                parts.append(token)

            if split < len(parts):
                rendered = " ".join(parts[:split]) + r"\N" + " ".join(parts[split:])
            else:
                rendered = " ".join(parts)

            start = float(active_word["short_s"])
            if active_index + 1 < len(group):
                provisional_end = float(group[active_index + 1]["short_s"])
            else:
                provisional_end = float(active_word["short_e"]) + 0.08
            raw.append({"start":start,"end":provisional_end,"text":rendered})

    events=[]
    for i,event in enumerate(raw):
        start=event["start"]
        next_start=raw[i+1]["start"] if i+1 < len(raw) else float(duration)
        # Zero-duration transcript tokens sometimes share the next token's start.
        # Skip them rather than creating an overlapping subtitle event.
        if next_start <= start + 0.001 and i+1 < len(raw):
            continue
        end=min(float(event["end"]),float(next_start),float(duration))
        if end <= start:
            continue
        events.append(
            f"Dialogue: 0,{ass_time(start)},{ass_time(end)},Cap,,0,0,0,,{event['text']}"
        )

    Path(out_path).write_text(header + "\n".join(events) + "\n", encoding="utf-8")

def build(plan, mapping, asset_dir, audio_source, output, qc_dir):
    short = next(x for x in mapping["shorts"] if x["id"] == plan["id"])
    fps = int(plan["fps"])
    duration = float(short["duration_sec"])

    qc_dir = Path(qc_dir)
    qc_dir.mkdir(parents=True, exist_ok=True)
    ass_path = qc_dir / f"{plan['id']}.ass"
    make_ass(
        short["source_words"],
        ass_path,
        duration,
        fps,
        plan.get("caption_replacements", {}),
    )

    inputs = []
    filters = []
    video_labels = []

    for index, segment in enumerate(plan["segments"]):
        segment_duration = float(segment["out_end"]) - float(segment["out_start"])
        is_vertical_gfx = bool(segment.get("gfx_type"))
        if is_vertical_gfx:
            gfx_dir = qc_dir / "editor_gfx"
            gfx_dir.mkdir(parents=True, exist_ok=True)
            asset = make_editor_gfx(
                segment,
                gfx_dir / f"{plan['id']}_{index:02d}_{segment['gfx_type']}.png",
            )
        else:
            asset = Path(asset_dir) / segment["asset"]
            if not asset.exists():
                raise FileNotFoundError(asset)

        inputs += [
            "-loop", "1",
            "-framerate", str(fps),
            "-t", f"{segment_duration:.3f}",
            "-i", str(asset),
        ]

        # Clean-source vertical composition.
        # GFX are authored directly at 1080x1920.
        focal = float(segment.get("x", 0.5))
        x_expr = f"(iw-ow)*{focal:.3f}"
        fit = str(segment.get("fit", "crop")).lower()

        motion = str(segment.get("motion", "static")).lower()
        if is_vertical_gfx:
            base_picture = "scale=1080:1920:flags=lanczos"
        elif fit == "contain":
            base_picture = (
                "scale=1080:1920:force_original_aspect_ratio=decrease:flags=lanczos,"
                "pad=1080:1920:(ow-iw)/2:(oh-ih)/2:color=0x171A1C"
            )
        else:
            base_picture = (
                f"crop=ih*9/16:ih:x='{x_expr}':y=0,"
                "scale=1080:1920:flags=lanczos"
            )
        if motion == "push":
            # ~1.2% total push across the segment. No x/y travel.
            frames = max(1, round(segment_duration * fps))
            step = 0.012 / frames
            base_picture += (
                f",zoompan=z='min(zoom+{step:.8f},1.012)':"
                "x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':"
                f"d=1:s=1080x1920:fps={fps}"
            )

        vf = (
            base_picture
            + ",drawbox=x=0:y=1380:w=1080:h=540:color=0x171A1C@0.48:t=fill"
            + ",drawbox=x=0:y=1680:w=1080:h=240:color=0x171A1C@0.88:t=fill"
            + f",drawbox=x=54:y=1374:w=972:h=4:color={ORANGE}:t=fill"
        )

        provenance = draw_escape(segment.get("provenance", ""))
        if provenance:
            vf += (
                f",drawtext=font='DejaVu Sans':text='{provenance}':"
                "x=w-text_w-42:y=74:fontsize=19:fontcolor=0xF3EBDD:"
                "borderw=2:bordercolor=black@0.72"
            )

        metric = draw_escape(segment.get("metric", ""))

        if metric:
            vf += (
                f",drawtext=font='DejaVu Sans':text='{metric}':"
                f"x=54:y=1286:fontsize=42:fontcolor={PAPER}:"
                "borderw=3:bordercolor=black@0.82"
            )

        if index == 0:
            title_1 = draw_escape(plan["title_lines"][0])
            title_2 = draw_escape(plan["title_lines"][1])
            vf += (
                f",drawtext=font='DejaVu Sans':text='{title_1}':"
                f"x=(w-text_w)/2:y=150:fontsize=44:fontcolor={PAPER}:"
                "borderw=4:bordercolor=black@0.90:enable='between(t,0,2.6)',"
                f"drawtext=font='DejaVu Sans':text='{title_2}':"
                f"x=(w-text_w)/2:y=202:fontsize=44:fontcolor={PAPER}:"
                "borderw=4:bordercolor=black@0.90:enable='between(t,0,2.6)'"
            )

        filters.append(f"[{index}:v]{vf},fps={fps},setsar=1[v{index}]")
        video_labels.append(f"[v{index}]")

    filters.append(
        "".join(video_labels)
        + f"concat=n={len(video_labels)}:v=1:a=0[vcat]"
    )

    ass_filter_path = str(ass_path).replace(":", r"\:")
    filters.append(f"[vcat]ass='{ass_filter_path}'[vout]")

    # Exact locked long-form audio excerpt.
    inputs += [
        "-ss", f"{float(short['source_in_sec']):.3f}",
        "-t", f"{duration:.3f}",
        "-i", audio_source,
    ]
    audio_input_index = len(plan["segments"])

    command = [
        "ffmpeg", "-y", "-loglevel", "error",
        *inputs,
        "-filter_complex", ";".join(filters),
        "-map", "[vout]",
        "-map", f"{audio_input_index}:a:0",
        "-c:v", "libx264",
        "-preset", "veryfast",
        "-crf", "17",
        "-pix_fmt", "yuv420p",
        "-r", str(fps),
        "-c:a", "aac",
        "-b:a", "192k",
        "-ar", "48000",
        "-ac", "2",
        "-movflags", "+faststart",
        output,
    ]
    subprocess.run(command, check=True)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--plan", required=True)
    parser.add_argument("--map", required=True)
    parser.add_argument("--asset-dir", required=True)
    parser.add_argument("--audio-source", required=True)
    parser.add_argument("--out", required=True)
    parser.add_argument("--qc", required=True)
    args = parser.parse_args()

    plan = json.loads(Path(args.plan).read_text(encoding="utf-8"))
    mapping = json.loads(Path(args.map).read_text(encoding="utf-8"))

    Path(args.out).parent.mkdir(parents=True, exist_ok=True)
    build(plan, mapping, args.asset_dir, args.audio_source, args.out, args.qc)

if __name__ == "__main__":
    main()
