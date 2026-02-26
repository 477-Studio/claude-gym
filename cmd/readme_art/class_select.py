#!/usr/bin/env python3
"""Generate a pixel-art 'SELECT YOUR CLASS' menu for the README."""

from PIL import Image, ImageDraw, ImageFont
import os

SCALE = 2
W, H = 460, 370

# Retro palette
BG = (18, 14, 28)
BORDER = (120, 100, 160)
BORDER_HI = (180, 160, 220)
BORDER_DARK = (60, 50, 80)
TITLE_COLOR = (255, 220, 60)
LABEL_A = (255, 90, 70)
LABEL_B = (90, 200, 255)
LABEL_C = (80, 200, 100)
TEXT = (200, 195, 210)
DIM = (160, 155, 175)
ACCENT = (255, 170, 50)
SELECT = (60, 220, 90)
DIVIDER = (60, 50, 80)

# Tag colors
TAG_MUST_BG = (180, 40, 30)
TAG_MUST_FG = (255, 255, 255)
TAG_SHOULD_BG = (30, 110, 170)
TAG_SHOULD_FG = (255, 255, 255)
TAG_DONT_BG = (55, 55, 65)
TAG_DONT_FG = (140, 140, 150)

img = Image.new("RGB", (W, H), BG)
draw = ImageDraw.Draw(img)

font_path = None
for p in [
    "/System/Library/Fonts/Menlo.ttc",
    "/System/Library/Fonts/Monaco.dfont",
    "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf",
]:
    if os.path.exists(p):
        font_path = p
        break

if font_path:
    font_sm = ImageFont.truetype(font_path, 11)
    font_md = ImageFont.truetype(font_path, 13)
    font_tag = ImageFont.truetype(font_path, 10)
    font_title = ImageFont.truetype(font_path, 16)
else:
    font_sm = ImageFont.load_default()
    font_md = font_sm
    font_tag = font_sm
    font_title = font_sm


def draw_border(x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], outline=BORDER_DARK)
    draw.rectangle([x + 2, y + 2, x + w - 2, y + h - 2], outline=BORDER)
    draw.line([(x + 2, y + 2), (x + w - 2, y + 2)], fill=BORDER_HI)
    draw.line([(x + 2, y + 2), (x + 2, y + h - 2)], fill=BORDER_HI)
    draw.line([(x + 3, y + h - 2), (x + w - 2, y + h - 2)], fill=BORDER_DARK)
    draw.line([(x + w - 2, y + 3), (x + w - 2, y + h - 2)], fill=BORDER_DARK)
    for corner in [(x+1, y+1), (x+w-1, y+1), (x+1, y+h-1), (x+w-1, y+h-1)]:
        img.putpixel(corner, BORDER)


def draw_divider(y):
    for x in range(20, W - 20, 6):
        draw.line([(x, y), (x + 3, y)], fill=DIVIDER)


def draw_selector(x, y):
    for i in range(5):
        draw.line([(x + i, y - i + 4), (x + i, y + i - 4)], fill=SELECT)


def draw_star(cx, cy, color):
    pts = [(cx, cy-2), (cx-1, cy-1), (cx+1, cy-1),
           (cx-2, cy), (cx, cy), (cx+2, cy),
           (cx-1, cy+1), (cx+1, cy+1), (cx, cy+2)]
    for px, py in pts:
        if 0 <= px < W and 0 <= py < H:
            img.putpixel((px, py), color)


def draw_tag(x, y, text, bg, fg):
    """Draw a pill-shaped tag badge."""
    tw = int(draw.textlength(text, font=font_tag))
    pad_x, pad_y = 5, 2
    tag_w = tw + pad_x * 2
    tag_h = 12 + pad_y
    # Background with 1px border radius feel
    draw.rectangle([x + 1, y, x + tag_w - 1, y + tag_h], fill=bg)
    draw.rectangle([x, y + 1, x + tag_w, y + tag_h - 1], fill=bg)
    # Text centered
    draw.text((x + pad_x, y + pad_y), text, fill=fg, font=font_tag)
    return tag_w


# ============================================================
# MAIN BORDER
# ============================================================
draw_border(6, 6, W - 12, H - 12)

# ============================================================
# TITLE
# ============================================================
title = "IS THIS FOR ME?"
tw = draw.textlength(title, font=font_title)
tx = (W - tw) // 2
draw.text((tx, 16), title, fill=TITLE_COLOR, font=font_title)
draw_star(int(tx - 12), 24, TITLE_COLOR)
draw_star(int(tx + tw + 12), 24, TITLE_COLOR)
draw.line([(20, 36), (W - 20, 36)], fill=BORDER)

# ============================================================
# CLASS A: THE BROKEN VETERAN — MUST USE
# ============================================================
ya = 46

draw_selector(16, ya + 8)
draw.text((30, ya), "[A]", fill=LABEL_A, font=font_md)
draw.rectangle([56, ya + 1, 60, ya + 11], fill=LABEL_A)
draw.text((62, ya), "THE BROKEN VETERAN", fill=LABEL_A, font=font_md)

# MUST USE tag
tag_x = 62 + int(draw.textlength("THE BROKEN VETERAN", font=font_md)) + 8
draw_tag(tag_x, ya, "MUST USE", TAG_MUST_BG, TAG_MUST_FG)

stats_a = [
    ("Age", "30+"),
    ("Got children", "yes"),
    ("Body status", "back pain, neck crunches"),
]
for i, (key, val) in enumerate(stats_a):
    sy = ya + 20 + i * 15
    draw.line([(36, ya + 16), (36, sy + 6)], fill=DIM)
    draw.line([(36, sy + 6), (42, sy + 6)], fill=DIM)
    draw.text((46, sy), key, fill=DIM, font=font_sm)
    vx = 210
    draw.text((vx, sy), val, fill=TEXT, font=font_sm)

vy = ya + 20 + len(stats_a) * 15 + 4
draw.line([(36, vy - 10), (36, vy + 6)], fill=DIM)
draw.text((36, vy + 2), "└►", fill=ACCENT, font=font_sm)
draw.text((58, vy), "VERDICT:", fill=ACCENT, font=font_md)
draw.text((140, vy), "you need this yesterday", fill=LABEL_A, font=font_md)

# ============================================================
# DIVIDER
# ============================================================
d1y = vy + 22
draw_divider(d1y)

# ============================================================
# CLASS B: THE OPTIMIST — SHOULD USE
# ============================================================
yb = d1y + 10

draw.text((30, yb), "[B]", fill=LABEL_B, font=font_md)
draw.rectangle([56, yb + 1, 60, yb + 11], fill=LABEL_B)
draw.text((62, yb), "THE TICKING CLOCK", fill=LABEL_B, font=font_md)

tag_x = 62 + int(draw.textlength("THE TICKING CLOCK", font=font_md)) + 8
draw_tag(tag_x, yb, "SHOULD USE", TAG_SHOULD_BG, TAG_SHOULD_FG)

stats_b = [
    ("Age", "25-30"),
    ("Got children", "not yet"),
    ("Body status", "fine (for now)"),
]
for i, (key, val) in enumerate(stats_b):
    sy = yb + 20 + i * 15
    draw.line([(36, yb + 16), (36, sy + 6)], fill=DIM)
    draw.line([(36, sy + 6), (42, sy + 6)], fill=DIM)
    draw.text((46, sy), key, fill=DIM, font=font_sm)
    vx = 210
    draw.text((vx, sy), val, fill=TEXT, font=font_sm)

vy2 = yb + 20 + len(stats_b) * 15 + 4
draw.line([(36, vy2 - 10), (36, vy2 + 6)], fill=DIM)
draw.text((36, vy2 + 2), "└►", fill=ACCENT, font=font_sm)
draw.text((58, vy2), "VERDICT:", fill=ACCENT, font=font_md)
draw.text((140, vy2), "install now, thank yourself", fill=LABEL_B, font=font_md)
draw.text((140, vy2 + 14), "in 6 months", fill=LABEL_B, font=font_md)

# ============================================================
# DIVIDER
# ============================================================
d2y = vy2 + 32
draw_divider(d2y)

# ============================================================
# CLASS C: THE TOURIST — DON'T USE
# ============================================================
yc = d2y + 10

draw.text((30, yc), "[C]", fill=LABEL_C, font=font_md)
draw.rectangle([56, yc + 1, 60, yc + 11], fill=LABEL_C)
draw.text((62, yc), "THE YOUNG BLOKE", fill=LABEL_C, font=font_md)

tag_x = 62 + int(draw.textlength("THE YOUNG BLOKE", font=font_md)) + 8
draw_tag(tag_x, yc, "DON'T USE", TAG_DONT_BG, TAG_DONT_FG)

stats_c = [
    ("Age", "< 25"),
    ("Got children", "lol no"),
    ("Body status", "runs 5km at dawn"),
]
for i, (key, val) in enumerate(stats_c):
    sy = yc + 20 + i * 15
    draw.line([(36, yc + 16), (36, sy + 6)], fill=DIM)
    draw.line([(36, sy + 6), (42, sy + 6)], fill=DIM)
    draw.text((46, sy), key, fill=DIM, font=font_sm)
    vx = 210
    draw.text((vx, sy), val, fill=TEXT, font=font_sm)

vy3 = yc + 20 + len(stats_c) * 15 + 4
draw.line([(36, vy3 - 10), (36, vy3 + 6)], fill=DIM)
draw.text((36, vy3 + 2), "└►", fill=ACCENT, font=font_sm)
draw.text((58, vy3), "VERDICT:", fill=ACCENT, font=font_md)
draw.text((140, vy3), "why are you even here?", fill=LABEL_C, font=font_md)

# ============================================================
# BOTTOM CONTROLS
# ============================================================
ctrl_y = H - 24
ctrl_text = "▲▼ to select    ENTER to continue"
cw = draw.textlength(ctrl_text, font=font_sm)
draw.text(((W - cw) // 2, ctrl_y), ctrl_text, fill=DIM, font=font_sm)

# ============================================================
# OUTPUT
# ============================================================
scaled = img.resize((W * SCALE, H * SCALE), Image.NEAREST)
out_path = "assets/class_select.png"
scaled.save(out_path)
print(f"Generated {out_path} ({W * SCALE}x{H * SCALE})")
