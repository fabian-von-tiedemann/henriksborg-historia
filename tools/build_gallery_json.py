#!/usr/bin/env python3
import re
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAGES = ROOT / "src" / "pages"
OUT = ROOT / "assets" / "gallery.json"

IMG_RE = re.compile(r"!\[(?P<alt>[^\]]*)\]\((?P<src>[^\)]+)\)")
EM_RE = re.compile(r"^\*([^*]+)\*\s*$")

def extract_entries(md_path: Path):
    entries = []
    lines = md_path.read_text(encoding="utf-8").splitlines()
    i = 0
    while i < len(lines):
        line = lines[i]
        m = IMG_RE.search(line)
        if m:
            src = m.group("src").strip()
            alt = m.group("alt").strip()
            caption = ""
            # Prefer italic on same line (after our earlier merge) or next line
            after = line[m.end():].strip()
            mm = EM_RE.match(after) if after else None
            if mm:
                caption = mm.group(1).strip()
            elif i + 1 < len(lines):
                mm2 = EM_RE.match(lines[i+1].strip())
                if mm2:
                    caption = mm2.group(1).strip()
                    i += 1
            entries.append({
                "src": src,
                "alt": alt,
                "caption": caption,
                "page": md_path.name,
            })
        i += 1
    return entries

def main():
    all_entries = []
    for md in sorted(PAGES.glob("*_local_assets.md")):
        all_entries.extend(extract_entries(md))
    OUT.write_text(json.dumps(all_entries, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Wrote {len(all_entries)} entries to {OUT}")

if __name__ == "__main__":
    main()


