# Henriksborg – Eleventy + Decap CMS

Detta repo innehåller en färdig setup för **Eleventy (11ty)** + **Decap CMS** och är redo att driftsättas på **Netlify**.

## Snabbstart lokalt

```bash
npm install
npm run dev      # http://localhost:8080
# eller
npm run build    # bygger till _site/
```

## Struktur

```
src/                # Innehåll (Eleventy input)
  _includes/layouts # Nunjucks-layouter
  pages/            # Markdown-sidor (Jekyll-lik front matter)
assets/             # Bilder, CSS
admin/              # Decap CMS (admin-gränssnitt)
_site/              # (byggd output, ignoreras i git)
tools/              # Manifest + skript för att hämta bilder
```

## Decap CMS (admin)

- Öppna `/admin/` i din driftsatta sajt.
- Konfiguration i `admin/config.yml`. Med standarden `git-gateway` krävs att Netlify Identity är aktiverat i din Netlify site.

## Netlify

- **Build command:** `npm run build`
- **Publish directory:** `_site`

## Mediahantering

- CMS laddar upp till `assets/hsb` och refererar via `/assets/hsb/...`.
- I `tools/` finns `download_hsb_assets_all_http_only.*` och `all_assets_manifest_http_only.csv` för att hämta bilder.
