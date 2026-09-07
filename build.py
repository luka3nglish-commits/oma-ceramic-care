#!/usr/bin/env python
"""Inject base64 brand assets (fonts, marble, logo) into template.html -> index.html.
Re-run after editing template.html.  Assets are read from the job tmp dir + OMA asset folders."""
import base64, os
from PIL import Image
from io import BytesIO

ROOT = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.join(ROOT, "assets")     # self-contained: fonts, marble, logo
LOGO = os.path.join(ASSETS, "logo.png")

def b64_file(path, mime):
    with open(path, "rb") as f:
        return "data:%s;base64,%s" % (mime, base64.b64encode(f.read()).decode())

def b64_logo(path, width=480):
    im = Image.open(path).convert("RGBA")
    h = round(im.height * width / im.width)
    im = im.resize((width, h), Image.LANCZOS)
    buf = BytesIO(); im.save(buf, "PNG", optimize=True)
    return "data:image/png;base64," + base64.b64encode(buf.getvalue()).decode()

subs = {
    "__ANTON__":      b64_file(os.path.join(ASSETS,"Anton.woff2"), "font/woff2"),
    "__BAR_MED__":    b64_file(os.path.join(ASSETS,"Barlow-Medium.woff2"), "font/woff2"),
    "__BAR_SB__":     b64_file(os.path.join(ASSETS,"Barlow-SemiBold.woff2"), "font/woff2"),
    "__BAR_BOLD__":   b64_file(os.path.join(ASSETS,"Barlow-Bold.woff2"), "font/woff2"),
    "__MARBLE_AMB__": b64_file(os.path.join(ASSETS,"marble_ambient.jpg"), "image/jpeg"),
    "__LOGO__":       b64_logo(LOGO),
}

with open(os.path.join(ROOT,"template.html"), encoding="utf-8") as f:
    html = f.read()
for k,v in subs.items():
    html = html.replace(k,v)

out = os.path.join(ROOT,"index.html")
with open(out,"w",encoding="utf-8") as f:
    f.write(html)
print("wrote", out, round(len(html)/1024,1), "KB")
missing=[k for k in subs if k in html]
print("unresolved placeholders:", missing or "none")
