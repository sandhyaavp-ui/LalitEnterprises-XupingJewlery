"""One-off generator for the site's Open Graph / Twitter Card banner image.

Run once locally (not part of the request/response path):
    venv/Scripts/python.exe scripts/generate_og_banner.py
Writes static/images/og-banner.jpg (1200x630).
"""
import math
from PIL import Image, ImageDraw, ImageFont

W, H = 1200, 630

ESPRESSO_TOP = (61, 40, 23)      # #3D2817
ESPRESSO_BOTTOM = (74, 50, 32)   # #4A3220
GOLD = (212, 175, 55)            # #D4AF37
GOLD_BRIGHT = (230, 200, 102)    # #E6C866
GOLD_DIM = (166, 132, 42)        # #A6842A
CREAM = (245, 237, 224)          # #F5EDE0
CREAM_MUTED = (196, 173, 143)    # #C4AD8F

FAVICON_YELLOW = (253, 226, 112)

FONT_DIR = r'C:\Users\vikas\AppData\Local\Temp\claude\E--xuping-site\29775262-50f1-486d-8975-4d4365e52ad9\scratchpad\ogfonts'
font_title = ImageFont.truetype(FONT_DIR + r'\PlayfairDisplay-Bold.ttf', 74)
font_sub = ImageFont.truetype(FONT_DIR + r'\Inter-SemiBold.ttf', 30)
font_cta = ImageFont.truetype(FONT_DIR + r'\Inter-SemiBold.ttf', 26)
font_url = ImageFont.truetype(FONT_DIR + r'\Inter-Regular.ttf', 22)

# --- background gradient ---
img = Image.new('RGB', (W, H), ESPRESSO_TOP)
for y in range(H):
    t = y / (H - 1)
    r = round(ESPRESSO_TOP[0] + (ESPRESSO_BOTTOM[0] - ESPRESSO_TOP[0]) * t)
    g = round(ESPRESSO_TOP[1] + (ESPRESSO_BOTTOM[1] - ESPRESSO_TOP[1]) * t)
    b = round(ESPRESSO_TOP[2] + (ESPRESSO_BOTTOM[2] - ESPRESSO_TOP[2]) * t)
    ImageDraw.Draw(img).line([(0, y), (W, y)], fill=(r, g, b))

draw = ImageDraw.Draw(img)

# thin inset gold frame
draw.rectangle([28, 28, W - 29, H - 29], outline=GOLD_DIM, width=2)

# --- logo badge (circle) ---
badge_cx, badge_cy, badge_r = 225, H // 2, 150
draw.ellipse(
    [badge_cx - badge_r, badge_cy - badge_r, badge_cx + badge_r, badge_cy + badge_r],
    fill=(69, 48, 34), outline=GOLD, width=4,
)

# cut the navy "le" monogram out of the yellow favicon square and paste it
# into the badge, recolouring it to fit the espresso/gold theme instead of
# the placeholder favicon's own yellow background.
favicon = Image.open('static/images/favicon.png').convert('RGBA')
data = favicon.getdata()
new_data = []
for px in data:
    r, g, b = px[0], px[1], px[2]
    dist = math.dist((r, g, b), FAVICON_YELLOW)
    if dist < 60:
        new_data.append((0, 0, 0, 0))
    else:
        # recolour the navy monogram to brand gold
        new_data.append((GOLD_BRIGHT[0], GOLD_BRIGHT[1], GOLD_BRIGHT[2], 255))
favicon.putdata(new_data)

logo_size = 250
favicon_small = favicon.resize((logo_size, logo_size), Image.LANCZOS)
img.paste(
    favicon_small,
    (badge_cx - logo_size // 2, badge_cy - logo_size // 2),
    favicon_small,
)

# --- text block ---
text_x = 460

draw.text((text_x, 165), 'Lalit Enterprises', font=font_title, fill=GOLD_BRIGHT)
draw.text(
    (text_x, 268),
    'Authentic Xuping Jewellery — Wholesale Prices',
    font=font_sub, fill=CREAM,
)

# CTA pill
cta_text = 'Enquire Now on WhatsApp'
bbox = draw.textbbox((0, 0), cta_text, font=font_cta)
cta_w = bbox[2] - bbox[0]
pad_x, pad_y = 28, 16
pill_x0, pill_y0 = text_x, 340
pill_x1, pill_y1 = pill_x0 + cta_w + pad_x * 2, pill_y0 + (bbox[3] - bbox[1]) + pad_y * 2
draw.rounded_rectangle([pill_x0, pill_y0, pill_x1, pill_y1], radius=28, outline=GOLD, width=2)
draw.text((pill_x0 + pad_x, pill_y0 + pad_y - bbox[1]), cta_text, font=font_cta, fill=GOLD_BRIGHT)

# footer line: reseller/MOQ note + url
draw.text(
    (text_x, pill_y1 + 36),
    'For resellers & retailers across India',
    font=font_url, fill=CREAM_MUTED,
)
url_text = 'lalitenterprise.in'
bbox_u = draw.textbbox((0, 0), url_text, font=font_url)
draw.text((W - 60 - (bbox_u[2] - bbox_u[0]), H - 60), url_text, font=font_url, fill=CREAM_MUTED)

img.save('static/images/og-banner.jpg', quality=92)
print('wrote static/images/og-banner.jpg', img.size)
