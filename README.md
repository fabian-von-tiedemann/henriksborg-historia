# Henriksborgs Historia
Kort beskrivning av projektet, hur man kör lokalt, hur man bygger och deployar.
## Utveckling
npm install
npm run dev
## Bygg
npm run build

## Sociala delningsbilder & galleri
- `featured_image` i varje sida används för att skapa sociala bilder (1200x630) i `assets/social/` och för OG/Twitter-meta.
- Vid build körs automatiskt:
  - `tools/generate_social_images.py` (kräver Python 3 + Pillow)
  - `tools/build_gallery_json.py` som skapar `assets/gallery.json` från markdown.

