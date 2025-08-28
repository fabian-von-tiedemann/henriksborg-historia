#!/usr/bin/env python3
"""
Generate 1200x630 social share images from featured images defined in markdown front matter.
Requires: pillow (pip install pillow)
"""
import re
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
PAGES = ROOT / "src" / "pages"
ASSETS = ROOT / "assets"
OUT_DIR = ASSETS / "social"
OUT_DIR.mkdir(parents=True, exist_ok=True)

FRONT_RE = re.compile(r"^---[\s\S]*?---", re.MULTILINE)
FEATURE_RE = re.compile(r"featured_image:\s*(?P<path>\S+)")
TITLE_RE = re.compile(r"title:\s*\"?(?P<title>.+?)\"?$", re.MULTILINE)

def parse_front_matter(text: str):
    m = FRONT_RE.search(text)
    if not m:
        return {}
    block = m.group(0)
    fm = {}
    m2 = FEATURE_RE.search(block)
    if m2:
        fm['featured_image'] = m2.group('path').strip()
    m3 = TITLE_RE.search(block)
    if m3:
        fm['title'] = m3.group('title').strip('"')
    return fm

def generate_social(src_path: Path, out_path: Path):
    try:
        with Image.open(src_path) as img:
            # letterbox to 1200x630
            target_w, target_h = 1200, 630
            img_ratio = img.width / img.height
            target_ratio = target_w / target_h
            if img_ratio > target_ratio:
                # too wide -> fit height
                new_h = target_h
                new_w = int(new_h * img_ratio)
            else:
                new_w = target_w
                new_h = int(new_w / img_ratio)
            resized = img.resize((new_w, new_h), Image.LANCZOS)
            canvas = Image.new('RGB', (target_w, target_h), (0,0,0))
            off_x = (target_w - new_w) // 2
            off_y = (target_h - new_h) // 2
            canvas.paste(resized, (off_x, off_y))
            out_path.parent.mkdir(parents=True, exist_ok=True)
            canvas.save(out_path, format='JPEG', quality=85)
            return True
    except Exception as e:
        print(f"Failed {src_path}: {e}")
        return False

def main():
    generated = 0
    for md in PAGES.glob("*_local_assets.md"):
        text = md.read_text(encoding='utf-8')
        fm = parse_front_matter(text)
        if not fm.get('featured_image'):
            continue
        src_rel = fm['featured_image'].lstrip('/')
        src = ROOT / src_rel
        if not src.exists():
            print(f"Missing: {src}")
            continue
        # output path mirrors permalink if present
        out_name = md.stem.replace('_local_assets','') + '.jpg'
        out = OUT_DIR / out_name
        if generate_social(src, out):
            generated += 1
            print(f"Wrote {out}")
    print(f"Generated {generated} social images in {OUT_DIR}")

if __name__ == "__main__":
    main()


