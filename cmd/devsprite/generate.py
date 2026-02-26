"""Generate pixel art developer character with Claude logo t-shirt."""
from PIL import Image

W, H = 32, 32

# Color palette
Skin  = (0xF5, 0xD0, 0xA9, 255)
SkinS = (0xD4, 0xA5, 0x74, 255)  # shadow
SkinH = (0xFF, 0xE0, 0xBD, 255)  # highlight

Hair  = (0x4A, 0x33, 0x28, 255)
HairH = (0x6B, 0x4A, 0x3A, 255)

Shirt  = (0x2C, 0x3E, 0x50, 255)  # navy
ShirtS = (0x1A, 0x25, 0x30, 255)
ShirtH = (0x3D, 0x55, 0x6E, 255)

LogoP = (0xFF, 0x99, 0x33, 255)   # Claude orange
LogoS = (0xCC, 0x66, 0x00, 255)
LogoH = (0xFF, 0xBB, 0x77, 255)
LogoO = (0x22, 0x22, 0x22, 255)

Pants  = (0x3B, 0x3B, 0x5C, 255)
PantsS = (0x2A, 0x2A, 0x45, 255)

Shoe  = (0x44, 0x44, 0x44, 255)
ShoeH = (0x66, 0x66, 0x66, 255)

O = (0x22, 0x22, 0x22, 255)  # dark outline
WH = (0xFF, 0xFF, 0xFF, 255)  # white

img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
px = img.putpixel


def rect(x1, y1, x2, y2, c):
    for y in range(y1, y2 + 1):
        for x in range(x1, x2 + 1):
            px((x, y), c)


def draw_developer():
    # === HAIR (y=6-9) ===
    # Top tuft
    for dx in range(3):
        px((14 + dx, 6), Hair)
    # Main hair
    for x in range(11, 21):
        c = HairH if x in (11, 20) else Hair
        px((x, 7), c)
    for x in range(10, 22):
        c = HairH if x >= 18 else Hair
        px((x, 8), c)
    # Hair sides (forehead visible in middle)
    for x in range(10, 13):
        px((x, 9), Hair)
    for x in range(19, 22):
        px((x, 9), HairH)

    # === HEAD / FACE (y=9-15) ===
    for y in range(9, 16):
        left, right = 10, 21
        if y in (9, 15):
            left, right = 11, 20
        for x in range(left, right + 1):
            c = Skin
            if x == left:
                c = SkinS
            elif x == right:
                c = SkinH
            px((x, y), c)

    # Eyes (white + pupil)
    px((13, 11), WH); px((14, 11), WH)
    px((13, 12), O);  px((14, 12), WH)
    px((17, 11), WH); px((18, 11), WH)
    px((18, 12), O);  px((17, 12), WH)

    # Smile
    px((14, 14), SkinS); px((15, 14), SkinS); px((16, 14), SkinS)

    # === NECK (y=16) ===
    px((15, 16), Skin); px((16, 16), Skin)

    # === T-SHIRT (y=17-23) ===
    for y in range(17, 24):
        left, right = 9, 22
        if y >= 22:
            left, right = 10, 21
        for x in range(left, right + 1):
            c = Shirt
            if x <= left + 1:
                c = ShirtS
            elif x >= right - 1:
                c = ShirtH
            px((x, y), c)

    # Claude logo on shirt (6x4 mini blob with eyes + legs)
    lx, ly = 13, 19
    for dy in range(4):
        for dx in range(6):
            c = LogoP
            if dx == 0: c = LogoS
            elif dx == 5: c = LogoH
            if dy == 0: c = LogoH
            elif dy == 3: c = LogoS
            px((lx + dx, ly + dy), c)
    # Logo eyes
    px((lx + 1, ly + 1), LogoO)
    px((lx + 4, ly + 1), LogoO)
    # Logo tiny legs
    px((lx + 1, ly + 4), LogoS)
    px((lx + 4, ly + 4), LogoS)

    # === ARMS ===
    # Left arm (shirt shoulder + skin forearm)
    for dy in range(3):
        px((7, 17 + dy), ShirtS); px((8, 17 + dy), Shirt)
    for dy in range(3):
        px((7, 20 + dy), SkinS); px((8, 20 + dy), Skin)

    # Right arm
    for dy in range(3):
        px((23, 17 + dy), Shirt); px((24, 17 + dy), ShirtH)
    for dy in range(3):
        px((23, 20 + dy), Skin); px((24, 20 + dy), SkinH)

    # === PANTS (y=24-27) ===
    for y in range(24, 28):
        for x in range(10, 22):
            if y >= 26 and x in (15, 16):
                continue  # leg gap
            c = PantsS if x == 10 else Pants
            px((x, y), c)

    # === SHOES (y=28-29) ===
    for x in range(9, 15):
        c = ShoeH if x == 9 else Shoe
        px((x, 28), c)
        if x <= 13:
            px((x, 29), c)
    for x in range(17, 23):
        c = ShoeH if x == 22 else Shoe
        px((x, 28), c)
        if x >= 18:
            px((x, 29), c)


draw_developer()

import os
os.makedirs("assets/developer", exist_ok=True)

# Save at 1x (original 32x32)
img.save("assets/developer/dev_character.png")

# Also save a 8x scaled version for easy viewing
scaled = img.resize((W * 8, H * 8), Image.NEAREST)
scaled.save("assets/developer/dev_character_preview.png")

print("Generated assets/developer/dev_character.png (32x32)")
print("Generated assets/developer/dev_character_preview.png (256x256 preview)")
