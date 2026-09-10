"""One-off: derive a mobile-sized WebP+JPEG variant of about-model.jpg.

.about-grid goes full-width single-column below 800px (mobile) but
~550px per column above that (desktop two-up) — the original pass only
generated one size (900px, right for desktop), so mobile was
downloading a file sized for a display area 2-3x wider than it actually
renders at. Re-deriving from the already-900px source loses no visible
detail at a 500px target.

Run once: venv/Scripts/python.exe scripts/optimize_about_model.py
"""
from PIL import Image

SRC = 'static/images/about-model.jpg'
MOBILE_WIDTH = 500

img = Image.open(SRC).convert('RGB')
ratio = MOBILE_WIDTH / img.width
img = img.resize((MOBILE_WIDTH, round(img.height * ratio)), Image.LANCZOS)

img.save('static/images/about-model-mobile.webp', 'WEBP', quality=82)
img.save('static/images/about-model-mobile.jpg', 'JPEG', quality=80, optimize=True)

print('about-model-mobile:', img.size)
