from pathlib import Path
import json,hashlib,shutil,datetime,argparse
from PIL import Image
p=argparse.ArgumentParser();p.add_argument("--asset",required=True);p.add_argument("--source",required=True);a=p.parse_args()
r=Path(r"C:\YOUTUBE\Youtube 2\VIDEO 10\IMAGEGEN_FULL_FILM_R2");f=r/"GENERATION_QUEUE_ASSEMBLY_R4.json";q=json.loads(f.read_text());x=next(x for x in q if x["asset_id"]==a.asset);source=Path(a.source);dest=r/x["output"]
assert source.is_file();assert not dest.exists();im=Image.open(source);assert im.width>im.height and abs(im.width/im.height-16/9)<.03
shutil.copy2(source,dest);x.update(status="GENERATED",qc="PENDING_VISUAL_QC",source_generated_path=str(source),sha256=hashlib.sha256(dest.read_bytes()).hexdigest(),generated_at_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),generated_prompt=x["prompt"],generated_references=x["references"])
tmp=f.with_suffix(".tmp");tmp.write_text(json.dumps(q,indent=2));tmp.replace(f)
print(a.asset+" saved "+str(sum(z["status"]=="GENERATED" for z in q))+"/150")
