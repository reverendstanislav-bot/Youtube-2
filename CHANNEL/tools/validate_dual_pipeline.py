#!/usr/bin/env python3
"""Dependency-free validation of declared HIA dual pipeline; does NOT inspect Windows installations."""
import json
import sys
from pathlib import Path

def validate(config, registry):
    errors = []
    if config.get("schema") != "HIA_DUAL_PIPELINE_CONFIG_V1": errors.append("unknown config schema")
    if registry.get("schema") != "HIA_DUAL_PIPELINE_SKILLS_V1": errors.append("unknown registry schema")
    names = registry.get("explicitly_named_skills", [])
    if not isinstance(names, list) or not all(isinstance(n,str) and n.strip() for n in names):
        errors.append("invalid skill name list")
    elif len(names) != len(set(names)): errors.append("duplicate skill names")
    if registry.get("explicitly_named_count") != len(names): errors.append("explicit named count mismatch")
    if registry.get("owner_reported_total") != len(names)+registry.get("unnamed_claimed_skills_count", -999):
        errors.append("declared count mismatch")
    if config.get("available_routes") != ["resolve","remotion"]: errors.append("unexpected engines")
    if config.get("default_engine") != "episode_current_lock": errors.append("must preserve episode engine")
    for key in ("auto_render","auto_generate","auto_tts","auto_download","publish","shorts","subtitles","generated_video"):
        if config.get(key) is not False: errors.append(f"unsafe flag: {key}")
    if registry.get("verification", {}).get("codex_local") != "NOT_VERIFIED_FROM_GITHUB":
        errors.append("local installation cannot be verified here")
    if registry.get("verification", {}).get("antigravity_local") != "NOT_VERIFIED_FROM_GITHUB":
        errors.append("local installation cannot be verified here")
    return {"result":"FAIL" if errors else "PASS_CONFIGURATION_ONLY","errors":errors,
            "named_skills":len(names),"owner_reported":registry.get("owner_reported_total"),
            "local_installation_verified":False,"production_authorized":False}

def main():
    try:
        cfgpath=Path(sys.argv[1]) if len(sys.argv)>1 else Path(__file__).resolve().parents[1]/"OPERATIONS/DUAL_PIPELINE_CONFIG.json"
        cfg=json.loads(cfgpath.read_text(encoding="utf-8-sig"))
        reg=json.loads((cfgpath.parent/"SKILL_REGISTRY.json").read_text(encoding="utf-8-sig"))
        result=validate(cfg,reg)
    except (ValueError,OSError,TypeError) as exc:
        result={"result":"FAIL","errors":[str(exc)]}
    print(json.dumps(result,ensure_ascii=False,indent=2))
    return 1 if result["result"]=="FAIL" else 0
if __name__=="__main__":
    raise SystemExit(main())
