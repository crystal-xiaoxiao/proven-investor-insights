#!/usr/bin/env python3
"""Validate data.json before commit. Exit 1 on any problem so the routine never pushes a broken page.
Usage: python3 scripts/validate.py [--strict]   (--strict also requires every latest item to have a working-looking https URL)
"""
import json, re, sys
from datetime import date, timedelta

strict = "--strict" in sys.argv
errs = []

try:
    d = json.load(open("data.json", encoding="utf-8"))
except Exception as e:
    print(f"data.json is not valid JSON: {e}"); sys.exit(1)

m = d.get("meta", {})
for k in ("title", "last_updated", "window_start", "window_end", "period_summary"):
    if not m.get(k): errs.append(f"meta.{k} missing")

iso = re.compile(r"^\d{4}-\d{2}-\d{2}$")
for k in ("last_updated", "window_start", "window_end"):
    if m.get(k) and not iso.match(m[k]): errs.append(f"meta.{k} must be YYYY-MM-DD")

try:
    ws, we, lu = (date.fromisoformat(m[k]) for k in ("window_start", "window_end", "last_updated"))
    if we < ws: errs.append("window_end before window_start")
    if lu < we: errs.append("last_updated earlier than window_end")
    if (we - ws).days > 21: errs.append("observation window longer than 21 days")
except Exception:
    pass

ids = set()
for iv in d.get("investors", []):
    n = iv.get("name", "?")
    if not iv.get("id"): errs.append(f"{n}: id missing")
    if iv.get("id") in ids: errs.append(f"{n}: duplicate id")
    ids.add(iv.get("id"))
    for i, v in enumerate(iv.get("latest", [])):
        tag = f"{n}.latest[{i}]"
        if not v.get("headline"): errs.append(f"{tag}: headline missing")
        if not v.get("date") or not iso.match(v["date"]): errs.append(f"{tag}: date missing or not YYYY-MM-DD")
        else:
            try:
                dd = date.fromisoformat(v["date"])
                if dd < ws - timedelta(days=3) or dd > we + timedelta(days=3):
                    errs.append(f"{tag}: date {v['date']} outside window {ws}..{we}")
            except Exception: pass
        if not v.get("url"): errs.append(f"{tag}: url missing (every view needs a source)")
        elif strict and not v["url"].startswith("https://"): errs.append(f"{tag}: url must be https")
        if not v.get("source_label"): errs.append(f"{tag}: source_label missing")
        if not v.get("points"): errs.append(f"{tag}: points missing (what did they actually say?)")
    for t in iv.get("track_record", []):
        if t.get("wave") not in {w["id"] for w in d.get("waves", [])}:
            errs.append(f"{n}: track_record wave '{t.get('wave')}' not in waves")

if len(d.get("investors", [])) != 10:
    errs.append(f"expected 10 investors, found {len(d.get('investors', []))}")

if errs:
    print("data.json validation FAILED:"); [print(" -", e) for e in errs]; sys.exit(1)
total = sum(len(iv.get("latest", [])) for iv in d["investors"])
print(f"data.json OK — {total} views across {len(d['investors'])} investors, window {m['window_start']}..{m['window_end']}")
