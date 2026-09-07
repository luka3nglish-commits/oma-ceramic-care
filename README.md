# OMA Ceramic Coating Care

An animated, interactive ceramic-coating aftercare page for **OMA Auto Detailing**, handed to customers via a printed QR code after a coating job. Brand-matched to the marble-black + emerald business card.

**Live:** https://care.omaautodetailing.com.au

## What's here
- `index.html` — the deployed page. Single self-contained file: fonts, marble texture and logo are all embedded as base64, so it works offline and anywhere. **Generated, do not hand-edit.**
- `template.html` — the real source. Edit this.
- `build.py` — injects the assets from `assets/` into `template.html` and writes `index.html`.
- `assets/` — brand fonts (Anton, Barlow), the emerald marble texture, the white logo.
- `qr/` — printable QR codes (all point to the live URL):
  - `oma-care-card-A6.png` — the print card to hand out (A6, 300dpi).
  - `oma-qr-branded.png` — white-on-black branded QR on its own.
  - `oma-qr-standard.png` — dark-on-white fallback for light print / max scannability.
- `CNAME` — added once DNS is live, to serve on the custom subdomain.

## Editing the page
1. Edit `template.html`.
2. `python build.py` (needs `pillow`).
3. Commit `template.html` and the regenerated `index.html`.

## Custom domain (one-time DNS)
Add this record at the domain registrar for `omaautodetailing.com.au`:

| Type | Host | Value |
|------|------|-------|
| CNAME | `care` | `luka3nglish-commits.github.io` |

Then GitHub issues the HTTPS certificate automatically. If the DNS is on Cloudflare, set the record to **DNS only** (grey cloud) until the certificate issues.
