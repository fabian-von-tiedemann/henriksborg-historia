#!/usr/bin/env python3
import re
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAGES = ROOT / "src" / "pages"
OUT = ROOT / "assets" / "gallery.json"

IMG_RE = re.compile(r"!\[(?P<alt>[^\]]*)\]\((?P<src>[^\)]+)\)")
EM_RE = re.compile(r"^\*([^*]+)\*\s*$")

def parse_front_matter(lines):
    title = None
    permalink = None
    if lines and lines[0].strip() == '---':
        for i in range(1, len(lines)):
            line = lines[i]
            if line.strip() == '---':
                break
            if line.startswith('title:'):
                title = line.split(':', 1)[1].strip().strip('"')
            if line.startswith('permalink:'):
                permalink = line.split(':', 1)[1].strip()
    return title, permalink


def extract_entries(md_path: Path):
    entries = []
    text = md_path.read_text(encoding="utf-8")
    lines = text.splitlines()
    page_title, page_permalink = parse_front_matter(lines)
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
                "page_title": page_title,
                "permalink": page_permalink,
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


