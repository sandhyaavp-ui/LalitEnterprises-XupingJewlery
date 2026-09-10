"""One-off: re-encode static/images/about-model.jpg as a right-sized WebP
(with a compressed JPEG fallback for browsers without WebP support).

Original is 1023x1537 or 296KB. Displayed at max ~570px wide (.about-grid
is 1140px max, two equal columns), so 900px wide is plenty even for 2x
retina, and re-encoding at a sane quality cuts the rest.

Run once: venv/Scripts/python.exe scripts/optimize_about_model.py
"""
from PIL import Image

SRC = 'static/images/about-model.jpg'
MAX_WIDTH = 900

img = Image.open(SRC).convert('RGB')
if img.width > MAX_WIDTH:
    ratio = MAX_WIDTH / img.width
    img = img.resize((MAX_WIDTH, round(img.height * ratio)), Image.LANCZOS)

img.save('static/images/about-model.webp', 'WEBP', quality=82)
img.save('static/images/about-model.jpg', 'JPEG', quality=80, optimize=True)

print('about-model.webp:', img.size)
