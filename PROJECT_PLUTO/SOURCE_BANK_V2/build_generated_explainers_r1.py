from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageEnhance, ImageOps

W, H = 3840, 2160
NAVY = (7, 21, 34)
WHITE = (232, 237, 235)
CYAN = (104, 170, 190)
MUTED = (147, 165, 172)
ORANGE = (222, 91, 37)

GEN = Path(r"C:\Users\KK\.codex\generated_images\01a12632-ad0b-71b3-b2ee-75be9adcc1a5")
BANK = Path(r"C:\Users\KK\Desktop\Youtube\Youtube-2\PROJECT_PLUTO\EDITOR_BANK_V2")
OUT = BANK / "17_GENERATED_EXPLANATORY_FRAMES_R1"
OUT.mkdir(parents=True, exist_ok=True)

FONT = Path(r"C:\Windows\Fonts\bahnschrift.ttf")
FONT_BOLD = Path(r"C:\Windows\Fonts\bahnschrift.ttf")

def font(size):
    return ImageFont.truetype(str(FONT), size)

def contain(img, box, pad=0, bg=(9, 22, 34)):
    x0, y0, x1, y1 = box
    bw, bh = x1-x0-2*pad, y1-y0-2*pad
    tmp = ImageOps.contain(img, (bw, bh), Image.Resampling.LANCZOS)
    layer = Image.new("RGB", (x1-x0, y1-y0), bg)
    layer.paste(tmp, ((layer.width-tmp.width)//2, (layer.height-tmp.height)//2))
    return layer

def label(draw, xy, kicker, title, sub=None, accent=CYAN):
    x, y = xy
    draw.rectangle((x, y, x+86, y+9), fill=accent)
    draw.text((x+116, y-20), kicker, font=font(38), fill=MUTED, spacing=4)
    draw.text((x, y+48), title, font=font(62), fill=WHITE)
    if sub:
        draw.text((x, y+126), sub, font=font(34), fill=MUTED)

# GEN-01 — generated explanatory geometry with deterministic factual labels.
im = Image.open(GEN / "exec-286bf5ba-1e5d-4763-bbee-401ca82d9221.png").convert("RGB").resize((W, H), Image.Resampling.LANCZOS)
d = ImageDraw.Draw(im, "RGBA")
d.rectangle((0, 0, W, 245), fill=(4, 14, 25, 218))
label(d, (170, 82), "PROJECT PLUTO // AIRFLOW", "HOW THE TORY RAMJET HEATED AIR")
for x, txt, col in [(310, "AIR INTAKE", CYAN), (1540, "REACTOR CORE", WHITE), (2920, "HEATED AIR / THRUST", ORANGE)]:
    tw = d.textbbox((0,0), txt, font=font(38))[2]
    d.rounded_rectangle((x-26, 1880, x+tw+26, 1950), radius=10, fill=(4,14,25,210), outline=col, width=3)
    d.text((x, 1891), txt, font=font(38), fill=col)
d.text((170, 2040), "EXPLANATORY GRAPHIC // NOT ARCHIVAL FOOTAGE", font=font(27), fill=(135,151,158,255))
im.save(OUT / "GEN-01_TORY_AIRFLOW_EXPLAINER_4K.png", optimize=True)

# GEN-02 — generated blueprint treatment + exact source photograph.
im = Image.open(GEN / "exec-3120ab6d-96d7-4abb-a383-0fb7a552ebf9.png").convert("RGB").resize((W, H), Image.Resampling.LANCZOS)
d = ImageDraw.Draw(im, "RGBA")
photo = Image.open(BANK / "06_EDITOR_READY_PHOTOS_4K_JPEG" / "P002_4K.jpg").convert("L")
photo = ImageEnhance.Contrast(photo).enhance(1.12).convert("RGB")
box = (150, 360, 1515, 1675)
panel = contain(photo, box, pad=16, bg=(5,15,26))
im.paste(panel, (box[0], box[1]))
d = ImageDraw.Draw(im, "RGBA")
d.rectangle(box, outline=(*CYAN, 230), width=5)
d.rectangle((0, 0, W, 255), fill=(4, 14, 25, 220))
label(d, (170, 82), "PROJECT PLUTO // EVIDENCE VS CONCEPT", "WHAT WAS TESTED — AND WHAT WAS NEVER BUILT")
label(d, (170, 1740), "TESTED HARDWARE", "TORY II-C GROUND REACTOR", "AUTHENTIC PROJECT PHOTOGRAPH", CYAN)
label(d, (1775, 1740), "PROPOSED VEHICLE", "SLAM FLIGHT VEHICLE", "CONCEPT ONLY // NEVER BUILT", ORANGE)
d.text((170, 2075), "RIGHT-SIDE AIRFRAME IS A MODERN EXPLANATORY WIREFRAME, NOT ARCHIVAL EVIDENCE", font=font(27), fill=(135,151,158,255))
im.save(OUT / "GEN-02_TESTED_REACTOR_VS_UNBUILT_SLAM_4K.png", optimize=True)

# GEN-03 — generated timeline treatment with exact official pages overlaid.
im = Image.open(GEN / "exec-52215ed1-3bad-463b-b006-c3cbd55b9b26.png").convert("RGB").resize((W, H), Image.Resampling.LANCZOS)
left = Image.open(BANK / "08_EDITOR_READY_OFFICIAL_DOCUMENT_PAGES" / "AEC_PRESIDENT_REPORT_1964__PDFPAGE_067.png").convert("RGB")
right = Image.open(BANK / "01_PRIMARY_EDITOR_BANK" / "PROJECT_PLUTO_REAL_VISUAL_EDITOR_BANK" / "02_PRIMARY_ENGINEERING_REPORT_FIGURES" / "DOC-01__P007__END_OF_PROGRAM_1964_PREFACE.png").convert("RGB")
lb = (112, 180, 1270, 1955)
rb = (2560, 180, 3728, 1955)
im.paste(contain(left, lb, pad=10, bg=(6,16,27)), (lb[0], lb[1]))
im.paste(contain(right, rb, pad=10, bg=(6,16,27)), (rb[0], rb[1]))
d = ImageDraw.Draw(im, "RGBA")
d.rectangle(lb, outline=(*CYAN, 220), width=4)
d.rectangle(rb, outline=(*CYAN, 220), width=4)
d.rounded_rectangle((1370, 600, 2470, 920), radius=18, fill=(4,14,25,225), outline=(*CYAN,230), width=4)
d.rounded_rectangle((1370, 1160, 2470, 1480), radius=18, fill=(4,14,25,225), outline=(*ORANGE,230), width=4)
d.text((1450, 655), "MAY 20, 1964", font=font(72), fill=WHITE)
d.text((1450, 770), "FULL-POWER TORY II-C TEST", font=font(39), fill=CYAN)
d.text((1450, 1215), "JULY 1, 1964", font=font(72), fill=WHITE)
d.text((1450, 1330), "FLIGHT-TEST OBJECTIVE ENDED", font=font(39), fill=ORANGE)
d.text((1420, 2030), "OFFICIAL DOCUMENTS // TWO DATES // ONE DECISION", font=font(31), fill=MUTED)
im.save(OUT / "GEN-03_MAY20_TO_JULY1_DECISION_TIMELINE_4K.png", optimize=True)

print(OUT)
