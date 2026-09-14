#!/usr/bin/env python3
"""Archive the CURRENT period before writing a new one.
Copies meta + each investor's latest[] into history/<window_end>.json and prepends an entry to history/index.json.
Skips silently if the period has no views (nothing worth archiving) or is already archived.
Run this FIRST in every update, before touching data.json.
"""
import json, os

d = json.load(open("data.json", encoding="utf-8"))
m = d["meta"]
total = sum(len(iv.get("latest", [])) for iv in d["investors"])
fname = f"{m['window_end']}.json"
path = os.path.join("history", fname)

if total == 0:
    print("current period has no views; nothing archived"); raise SystemExit(0)
if os.path.exists(path):
    print(f"{path} already exists; nothing archived"); raise SystemExit(0)

snap = {
    "meta": {k: m.get(k) for k in ("title", "last_updated", "window_start", "window_end", "period_summary")},
    "investors": [{"id": iv["id"], "name": iv["name"], "firm": iv.get("firm", ""), "latest": iv.get("latest", [])} for iv in d["investors"]],
}
json.dump(snap, open(path, "w", encoding="utf-8"), ensure_ascii=False, indent=2)

idx_path = os.path.join("history", "index.json")
idx = json.load(open(idx_path, encoding="utf-8")) if os.path.exists(idx_path) else []
idx = [e for e in idx if e.get("file") != fname]
idx.insert(0, {"file": fname, "window_start": m["window_start"], "window_end": m["window_end"], "period_summary": m.get("period_summary", "")})
json.dump(idx, open(idx_path, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
print(f"archived {total} views to {path}")
