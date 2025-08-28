#!/usr/bin/env python3
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAGES_DIR = ROOT / "src" / "pages"

IMG_PATTERN = re.compile(r"^!\[[^\n\]]*\]\([^\n\)]+\)\s*$")
ITALIC_PATTERN = re.compile(r"^\*[^\n]*\*\s*$")

def fix_file(path: Path) -> bool:
    original = path.read_text(encoding="utf-8")
    lines = original.splitlines()
    changed = False

    new_lines = []
    i = 0
    while i < len(lines):
        line = lines[i]
        # Detect image line
        if IMG_PATTERN.match(line):
            # Look ahead: optional single blank line then italic
            if i + 1 < len(lines) and lines[i + 1].strip() == "" and i + 2 < len(lines) and ITALIC_PATTERN.match(lines[i + 2].strip()):
                # Merge into same paragraph: image + space + italic
                merged = f"{line} {lines[i + 2].strip()}"
                new_lines.append(merged)
                i += 3
                changed = True
                continue
            elif i + 1 < len(lines) and ITALIC_PATTERN.match(lines[i + 1].strip()):
                # Already adjacent; keep but ensure same paragraph
                merged = f"{line} {lines[i + 1].strip()}"
                new_lines.append(merged)
                i += 2
                changed = True
                continue
        new_lines.append(line)
        i += 1

    if changed:
        path.write_text("\n".join(new_lines) + "\n", encoding="utf-8")
    return changed


def main():
    any_changed = False
    for md in PAGES_DIR.glob("*_local_assets.md"):
        if fix_file(md):
            print(f"Fixed: {md}")
            any_changed = True
    if not any_changed:
        print("No caption spacing issues found.")

if __name__ == "__main__":
    main()


