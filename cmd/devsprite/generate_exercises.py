"""Generate exercise sprite sheet for male developer character.
Row 0: Idle - sipping coffee (16 frames, front view)
Row 1: Waving - calling for attention (16 frames, front view)
Row 2: Pump-up - "let's do it!" fist pump (16 frames, front view)
Row 3: Chair dips - SIDE VIEW with office chair (16 frames)
Row 4: Standing arm circles - FRONT VIEW (16 frames)
Row 5: Wondering - looking around, no coffee (16 frames, front view)
"""
import math
from PIL import Image

FRAME_W, FRAME_H = 32, 32
NUM_FRAMES = 16
NUM_ANIMS = 18

# Color palette (same as male dev character)
Skin  = (0xF5, 0xD0, 0xA9, 255)
SkinS = (0xD4, 0xA5, 0x74, 255)
SkinH = (0xFF, 0xE0, 0xBD, 255)

Hair  = (0x4A, 0x33, 0x28, 255)
HairH = (0x6B, 0x4A, 0x3A, 255)

Shirt  = (0x2C, 0x3E, 0x50, 255)
ShirtS = (0x1A, 0x25, 0x30, 255)
ShirtH = (0x3D, 0x55, 0x6E, 255)

LogoP = (0xFF, 0x99, 0x33, 255)
LogoS = (0xCC, 0x66, 0x00, 255)
LogoH = (0xFF, 0xBB, 0x77, 255)
LogoO = (0x22, 0x22, 0x22, 255)

Pants  = (0x3B, 0x3B, 0x5C, 255)
PantsS = (0x2A, 0x2A, 0x45, 255)

Shoe  = (0x44, 0x44, 0x44, 255)
ShoeH = (0x66, 0x66, 0x66, 255)

# Office chair colors
ChairSeat  = (0x33, 0x33, 0x33, 255)  # Dark gray fabric
ChairFrame = (0x55, 0x55, 0x55, 255)  # Metal gray
ChairLight = (0x6A, 0x6A, 0x6A, 255)  # Highlight
ChairWheel = (0x22, 0x22, 0x22, 255)  # Black wheels
ChairCush  = (0x44, 0x44, 0x44, 255)  # Cushion mid-tone

O  = (0x22, 0x22, 0x22, 255)
WH = (0xFF, 0xFF, 0xFF, 255)


def px(img, x, y, c):
    """Safe putpixel - only draw within image bounds."""
    if 0 <= x < img.width and 0 <= y < img.height:
        img.putpixel((x, y), c)


# =========================================================================
# IDLE - COFFEE SIP (front view)
# =========================================================================

# Coffee mug colors
MugWhite = (0xEE, 0xEE, 0xE8, 255)
MugShade = (0xCC, 0xCC, 0xC0, 255)
MugDark  = (0xAA, 0xAA, 0x9E, 255)
Coffee   = (0x6B, 0x3A, 0x1A, 255)
Steam1   = (0xDD, 0xDD, 0xDD, 180)
Steam2   = (0xCC, 0xCC, 0xCC, 120)


def draw_coffee_mug(img, ox, oy, mug_x, mug_y):
    """Draw a small coffee mug at given position.
    Mug is ~5px wide, 4px tall.
    """
    # Mug body
    for dy in range(4):
        for dx in range(5):
            c = MugWhite
            if dx == 0:
                c = MugShade
            elif dx == 4:
                c = MugDark
            if dy == 3:
                c = MugShade  # bottom
            px(img, ox + mug_x + dx, oy + mug_y + dy, c)
    # Coffee inside (top row = liquid visible)
    px(img, ox + mug_x + 1, oy + mug_y, Coffee)
    px(img, ox + mug_x + 2, oy + mug_y, Coffee)
    px(img, ox + mug_x + 3, oy + mug_y, Coffee)
    # Handle on right side
    px(img, ox + mug_x + 5, oy + mug_y + 1, MugShade)
    px(img, ox + mug_x + 5, oy + mug_y + 2, MugShade)


def draw_steam(img, ox, oy, mug_x, mug_y, frame):
    """Draw rising steam wisps above the mug, animated."""
    # Two steam wisps that rise and fade
    phase = frame % 8
    # Wisp 1
    w1_x = mug_x + 1
    w1_y = mug_y - 1 - phase // 2
    sway1 = [0, 0, 1, 1, 0, 0, -1, -1][frame % 8]
    if phase < 6:
        alpha = max(40, 180 - phase * 30)
        px(img, ox + w1_x + sway1, oy + w1_y, (*Steam1[:3], alpha))
    # Wisp 2 (offset phase)
    phase2 = (frame + 4) % 8
    w2_x = mug_x + 3
    w2_y = mug_y - 1 - phase2 // 2
    sway2 = [0, -1, -1, 0, 0, 1, 1, 0][frame % 8]
    if phase2 < 6:
        alpha2 = max(40, 180 - phase2 * 30)
        px(img, ox + w2_x + sway2, oy + w2_y, (*Steam2[:3], alpha2))


def draw_idle_arms(img, ox, oy, breath, sip_phase):
    """Draw arms for idle/sipping animation.

    sip_phase:
      0 = both arms down (resting, mug in right hand at side)
      1 = right arm raising mug
      2 = right arm at mouth (sipping)
      3 = right arm lowering mug
    """
    # Left arm always relaxed at side
    for dy in range(3):
        px(img, ox + 7, oy + 17 + breath + dy, ShirtS)
        px(img, ox + 8, oy + 17 + breath + dy, Shirt)
    for dy in range(3):
        px(img, ox + 7, oy + 20 + breath + dy, SkinS)
        px(img, ox + 8, oy + 20 + breath + dy, Skin)

    if sip_phase == 0:
        # Right arm relaxed at side, holding mug at hip level
        for dy in range(3):
            px(img, ox + 23, oy + 17 + breath + dy, Shirt)
            px(img, ox + 24, oy + 17 + breath + dy, ShirtH)
        for dy in range(3):
            px(img, ox + 23, oy + 20 + breath + dy, Skin)
            px(img, ox + 24, oy + 20 + breath + dy, SkinH)
        # Mug at waist level
        draw_coffee_mug(img, ox, oy, 25, 20 + breath)

    elif sip_phase == 1:
        # Right arm rising - elbow out, hand at chest level
        for dy in range(2):
            px(img, ox + 23, oy + 17 + breath + dy, Shirt)
            px(img, ox + 24, oy + 17 + breath + dy, ShirtH)
        # Forearm angled up
        px(img, ox + 23, oy + 19 + breath, Skin)
        px(img, ox + 24, oy + 18 + breath, Skin)
        px(img, ox + 25, oy + 17 + breath, SkinH)
        # Mug at chest level
        draw_coffee_mug(img, ox, oy, 24, 15 + breath)

    elif sip_phase == 2:
        # Right arm at mouth - hand near face
        px(img, ox + 23, oy + 17 + breath, Shirt)
        px(img, ox + 24, oy + 17 + breath, ShirtH)
        # Upper arm out
        px(img, ox + 23, oy + 16 + breath, Skin)
        px(img, ox + 22, oy + 15 + breath, Skin)
        px(img, ox + 21, oy + 14 + breath, SkinH)
        # Mug at mouth level
        draw_coffee_mug(img, ox, oy, 20, 12 + breath)

    elif sip_phase == 3:
        # Right arm lowering - same as phase 1
        for dy in range(2):
            px(img, ox + 23, oy + 17 + breath + dy, Shirt)
            px(img, ox + 24, oy + 17 + breath + dy, ShirtH)
        px(img, ox + 23, oy + 19 + breath, Skin)
        px(img, ox + 24, oy + 18 + breath, Skin)
        px(img, ox + 25, oy + 17 + breath, SkinH)
        draw_coffee_mug(img, ox, oy, 24, 15 + breath)


def draw_coffee_idle_frame(img, ox, oy, frame):
    """Draw one frame of idle coffee sipping.

    16 frames cycle:
      0-3:   idle standing, breathing, mug at side, steam rising
      4:     start raising mug
      5-6:   mug at mouth (sipping)
      7:     lowering mug
      8-15:  idle standing again, breathing, steam
    """
    # Breathing (same curve as original Claude idle)
    breath_curve = [0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0]
    breath = breath_curve[frame]

    # Sip phase mapping
    sip_phases = [0, 0, 0, 0, 1, 2, 2, 3, 0, 0, 0, 0, 0, 0, 0, 0]
    sip = sip_phases[frame]

    # Blink at frames 12-14 (like original)
    blink = frame in (12, 13, 14)

    # Draw body
    draw_hair_front(img, ox, oy + breath)
    draw_head_front(img, ox, oy + breath)

    # Override eyes for blink
    if blink:
        blink_frame = frame - 12  # 0=closing, 1=closed, 2=opening
        eye_y = oy + breath + 11
        # Clear eyes with skin
        for dy in range(2):
            for ex in [13, 14, 17, 18]:
                px(img, ox + ex, eye_y + dy, Skin)
        if blink_frame == 0:
            # Half closed
            px(img, ox + 13, eye_y + 1, O); px(img, ox + 14, eye_y + 1, O)
            px(img, ox + 17, eye_y + 1, O); px(img, ox + 18, eye_y + 1, O)
        elif blink_frame == 1:
            # Fully closed (single line)
            px(img, ox + 13, eye_y + 1, O); px(img, ox + 14, eye_y + 1, O)
            px(img, ox + 17, eye_y + 1, O); px(img, ox + 18, eye_y + 1, O)
        elif blink_frame == 2:
            # Opening (same as half closed)
            px(img, ox + 13, eye_y, WH); px(img, ox + 14, eye_y, WH)
            px(img, ox + 13, eye_y + 1, O); px(img, ox + 14, eye_y + 1, WH)
            px(img, ox + 17, eye_y, WH); px(img, ox + 18, eye_y, WH)
            px(img, ox + 18, eye_y + 1, O); px(img, ox + 17, eye_y + 1, WH)

    # Happy eyes when sipping
    if sip == 2:
        # Closed happy eyes (^_^)
        eye_y = oy + breath + 11
        for dy in range(2):
            for ex in [13, 14, 17, 18]:
                px(img, ox + ex, eye_y + dy, Skin)
        # Draw ^-shaped happy eyes
        px(img, ox + 13, eye_y + 1, O)
        px(img, ox + 14, eye_y, O)
        px(img, ox + 17, eye_y, O)
        px(img, ox + 18, eye_y + 1, O)

    draw_neck_front(img, ox, oy + breath)
    draw_shirt_front(img, ox, oy + breath)
    draw_logo_front(img, ox, oy + breath)
    draw_pants_front(img, ox, oy)
    draw_shoes_front(img, ox, oy)

    # Draw arms with mug
    draw_idle_arms(img, ox, oy, breath, sip)

    # Draw steam when mug is at rest (not sipping)
    if sip == 0:
        draw_steam(img, ox, oy, 25, 20 + breath, frame)


# =========================================================================
# WAVING - calling for attention (front view)
# =========================================================================

def draw_wave_arms(img, ox, oy, breath, wave_frame):
    """Draw arms for waving animation.

    Left arm stays relaxed at side.
    Right arm waves overhead: up-right, tilted right, up-right, tilted left (back and forth).
    """
    # Left arm relaxed at side
    for dy in range(3):
        px(img, ox + 7, oy + 17 + breath + dy, ShirtS)
        px(img, ox + 8, oy + 17 + breath + dy, Shirt)
    for dy in range(3):
        px(img, ox + 7, oy + 20 + breath + dy, SkinS)
        px(img, ox + 8, oy + 20 + breath + dy, Skin)

    # Right arm waving above head
    # Shoulder pivot
    sx, sy = 23, 17 + breath

    # Wave positions: arm swings back and forth overhead
    # Each position is (elbow_dx, elbow_dy, hand_dx, hand_dy) relative to shoulder
    wave_positions = [
        # Arm up-right (neutral)
        (3, -3, 5, -6),
        (4, -3, 6, -6),
        # Tilted right
        (4, -2, 7, -4),
        (5, -2, 7, -3),
        # Back to center
        (4, -3, 6, -6),
        (3, -3, 5, -6),
        # Tilted left
        (2, -3, 2, -7),
        (1, -3, 1, -7),
        # Back to center
        (2, -3, 3, -6),
        (3, -3, 5, -6),
        # Tilted right
        (4, -2, 7, -4),
        (5, -2, 7, -3),
        # Back to center
        (4, -3, 6, -6),
        (3, -3, 5, -6),
        # Tilted left
        (2, -3, 2, -7),
        (1, -3, 1, -7),
    ]

    edx, edy, hdx, hdy = wave_positions[wave_frame]

    elbow_x = sx + edx
    elbow_y = sy + edy
    hand_x = sx + hdx
    hand_y = sy + hdy

    # Upper arm: shoulder to elbow (shirt colored)
    _draw_thick_arm(img, ox, oy, sx, sy, elbow_x, elbow_y, Shirt, ShirtH)

    # Forearm: elbow to hand (skin colored)
    _draw_thick_arm(img, ox, oy, elbow_x, elbow_y, hand_x, hand_y, Skin, SkinH)

    # Hand (slightly bigger for visibility)
    px(img, ox + hand_x, oy + hand_y, Skin)
    px(img, ox + hand_x + 1, oy + hand_y, SkinH)
    px(img, ox + hand_x, oy + hand_y + 1, SkinH)


def draw_wave_frame(img, ox, oy, frame):
    """Draw one frame of waving animation.

    16 frames: character waves right arm overhead back and forth.
    Slight body bounce to feel energetic.
    """
    # Energetic bounce
    bounce_curve = [0, 0, -1, -1, 0, 0, -1, -1, 0, 0, -1, -1, 0, 0, -1, -1]
    bounce = bounce_curve[frame]

    # Open mouth for calling out on some frames
    calling = frame in (2, 3, 6, 7, 10, 11, 14, 15)

    # Draw body
    draw_hair_front(img, ox, oy + bounce)
    draw_head_front(img, ox, oy + bounce)

    # Override mouth when calling
    if calling:
        mouth_y = oy + bounce + 14
        # Open mouth (small dark oval)
        px(img, ox + 14, mouth_y, O)
        px(img, ox + 15, mouth_y, O)
        px(img, ox + 16, mouth_y, O)

    draw_neck_front(img, ox, oy + bounce)
    draw_shirt_front(img, ox, oy + bounce)
    draw_logo_front(img, ox, oy + bounce)
    draw_pants_front(img, ox, oy)
    draw_shoes_front(img, ox, oy)

    # Draw waving arms
    draw_wave_arms(img, ox, oy, bounce, frame)


# =========================================================================
# OFFICE CHAIR (side view)
# =========================================================================

def draw_office_chair(img, ox, oy):
    """Draw office chair from side view - positioned on right side of frame.
    Chair faces left. Character will be in front of it, facing left.
    """
    # Chair base/pedestal (center pole)
    cx = 22  # chair center x
    # Wheel base (5-star base from side = horizontal bar with wheels)
    for x in range(19, 27):
        px(img, ox + x, oy + 29, ChairFrame)
    # Wheels at ends
    px(img, ox + 18, oy + 29, ChairWheel)
    px(img, ox + 19, oy + 29, ChairWheel)
    px(img, ox + 26, oy + 29, ChairWheel)
    px(img, ox + 27, oy + 29, ChairWheel)

    # Center pole
    for y in range(26, 29):
        px(img, ox + 22, oy + y, ChairFrame)
        px(img, ox + 23, oy + y, ChairLight)

    # Seat cushion (horizontal, side view = thick rectangle)
    for y in range(23, 26):
        for x in range(18, 27):
            c = ChairSeat
            if y == 23:
                c = ChairLight  # top highlight
            elif y == 25:
                c = ChairCush  # bottom shadow
            px(img, ox + x, oy + y, c)

    # Backrest (vertical, on the right side of seat)
    for y in range(14, 24):
        for x in range(25, 28):
            c = ChairSeat
            if x == 25:
                c = ChairCush
            elif x == 27:
                c = ChairLight
            if y == 14:
                c = ChairLight  # top
            px(img, ox + x, oy + y, c)

    # Armrest (small horizontal bar from backrest)
    for x in range(21, 26):
        px(img, ox + x, oy + 19, ChairFrame)
        px(img, ox + x, oy + 20, ChairLight)


# =========================================================================
# SIDE VIEW CHARACTER for dips
# =========================================================================

def draw_side_hair(img, ox, oy):
    """Draw hair from side view."""
    # Top of head
    for x in range(11, 16):
        px(img, ox + x, oy + 6, Hair)
    for x in range(10, 17):
        c = HairH if x >= 15 else Hair
        px(img, ox + x, oy + 7, c)
    for x in range(9, 17):
        c = HairH if x >= 15 else Hair
        px(img, ox + x, oy + 8, c)
    # Back of head hair
    for y in range(9, 13):
        px(img, ox + 15, oy + y, Hair)
        px(img, ox + 16, oy + y, HairH)


def draw_side_head(img, ox, oy):
    """Draw head from side view - facing left."""
    # Head shape (rounder from side)
    for y in range(9, 16):
        left, right = 9, 15
        if y in (9, 15):
            left, right = 10, 14
        if y in (10,):
            left = 9
        for x in range(left, right + 1):
            c = Skin
            if x == left:
                c = SkinS
            elif x == right:
                c = SkinH
            px(img, ox + x, oy + y, c)

    # Eye (side view = one eye visible, facing left)
    px(img, ox + 10, oy + 11, WH)
    px(img, ox + 11, oy + 11, WH)
    px(img, ox + 10, oy + 12, O)  # pupil
    px(img, ox + 11, oy + 12, WH)

    # Nose (small bump on left edge)
    px(img, ox + 8, oy + 12, Skin)
    px(img, ox + 8, oy + 13, SkinS)

    # Mouth
    px(img, ox + 10, oy + 14, SkinS)
    px(img, ox + 11, oy + 14, SkinS)


def draw_side_neck(img, ox, oy):
    px(img, ox + 12, oy + 16, Skin)
    px(img, ox + 13, oy + 16, SkinS)


def draw_side_torso(img, ox, oy):
    """Draw torso from side view (narrower than front view)."""
    for y in range(17, 24):
        left, right = 10, 17
        if y >= 22:
            left, right = 11, 16
        for x in range(left, right + 1):
            c = Shirt
            if x == left:
                c = ShirtS
            elif x == right:
                c = ShirtH
            px(img, ox + x, oy + y, c)

    # Small Claude logo from side (just a hint of orange)
    px(img, ox + 11, oy + 19, LogoP)
    px(img, ox + 12, oy + 19, LogoP)
    px(img, ox + 13, oy + 19, LogoH)
    px(img, ox + 11, oy + 20, LogoS)
    px(img, ox + 12, oy + 20, LogoP)
    px(img, ox + 13, oy + 20, LogoP)


def draw_dip_arms_side(img, ox, oy, dip_offset):
    """Draw arms from side view during dip.
    Arms are BEHIND the character, reaching back to the chair seat.
    Character faces left, chair is to the right.
    The hand grips the chair seat edge (~x=18, y=23).
    """
    # Upper arm (from shoulder going backward/right toward chair)
    shoulder_x = 16
    shoulder_y = 18 + dip_offset

    # Hand position: on chair seat edge (fixed)
    hand_x = 19
    hand_y = 23

    # When at top (dip=0): arm is more horizontal, slightly bent
    # When at bottom (dip=4): arm is straighter, more vertical
    # Interpolate arm through mid point

    mid_x = (shoulder_x + hand_x) // 2
    mid_y = (shoulder_y + hand_y) // 2

    # Draw upper arm (shirt colored) from shoulder to midpoint
    steps = max(abs(mid_x - shoulder_x), abs(mid_y - shoulder_y), 1)
    for i in range(steps + 1):
        t = i / steps
        ax = int(round(shoulder_x + (mid_x - shoulder_x) * t))
        ay = int(round(shoulder_y + (mid_y - shoulder_y) * t))
        px(img, ox + ax, oy + ay, Shirt)
        px(img, ox + ax + 1, oy + ay, ShirtH)

    # Draw forearm (skin colored) from midpoint to hand
    steps = max(abs(hand_x - mid_x), abs(hand_y - mid_y), 1)
    for i in range(steps + 1):
        t = i / steps
        ax = int(round(mid_x + (hand_x - mid_x) * t))
        ay = int(round(mid_y + (hand_y - mid_y) * t))
        px(img, ox + ax, oy + ay, Skin)
        px(img, ox + ax + 1, oy + ay, SkinH)

    # Hand on chair
    px(img, ox + hand_x, oy + hand_y, Skin)
    px(img, ox + hand_x + 1, oy + hand_y, SkinS)


def draw_dip_legs_side(img, ox, oy):
    """Draw legs from side view - extended forward for dip position."""
    # Legs extend to the LEFT (forward) from the body
    # Upper legs (from body going forward-left)
    for y in range(24, 26):
        for x in range(5, 14):
            c = PantsS if x <= 6 else Pants
            px(img, ox + x, oy + y, c)

    # Lower legs (slight bend at knee, angling down to feet)
    for y in range(26, 28):
        for x in range(3, 8):
            c = PantsS if x <= 4 else Pants
            px(img, ox + x, oy + y, c)

    # Feet (on the ground, toes pointing left)
    for x in range(1, 6):
        c = ShoeH if x == 1 else Shoe
        px(img, ox + x, oy + 28, c)
    for x in range(2, 5):
        px(img, ox + x, oy + 29, Shoe)


def draw_chair_dip_frame(img, ox, oy, frame):
    """Draw one frame of chair dip animation (side view)."""
    # Dip curve: hold at top, lower, hold at bottom, raise, hold
    dip_offsets = [0, 0, 1, 2, 3, 4, 4, 4, 3, 2, 1, 0, 0, 0, 0, 0]
    dip = dip_offsets[frame]

    # Draw chair FIRST (behind/to the right)
    draw_office_chair(img, ox, oy)

    # Draw legs (fixed position - extended forward)
    draw_dip_legs_side(img, ox, oy)

    # Draw upper body shifted down by dip offset
    draw_side_hair(img, ox, oy + dip)
    draw_side_head(img, ox, oy + dip)
    draw_side_neck(img, ox, oy + dip)
    draw_side_torso(img, ox, oy + dip)

    # Draw arms reaching back to chair
    draw_dip_arms_side(img, ox, oy, dip)


# =========================================================================
# ARM CIRCLES (front view - unchanged)
# =========================================================================

def draw_hair_front(img, ox, oy):
    for dx in range(3):
        px(img, ox + 14 + dx, oy + 6, Hair)
    for x in range(11, 21):
        c = HairH if x in (11, 20) else Hair
        px(img, ox + x, oy + 7, c)
    for x in range(10, 22):
        c = HairH if x >= 18 else Hair
        px(img, ox + x, oy + 8, c)
    for x in range(10, 13):
        px(img, ox + x, oy + 9, Hair)
    for x in range(19, 22):
        px(img, ox + x, oy + 9, HairH)


def draw_head_front(img, ox, oy):
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
            px(img, ox + x, oy + y, c)
    px(img, ox + 13, oy + 11, WH); px(img, ox + 14, oy + 11, WH)
    px(img, ox + 13, oy + 12, O);  px(img, ox + 14, oy + 12, WH)
    px(img, ox + 17, oy + 11, WH); px(img, ox + 18, oy + 11, WH)
    px(img, ox + 18, oy + 12, O);  px(img, ox + 17, oy + 12, WH)
    px(img, ox + 14, oy + 14, SkinS)
    px(img, ox + 15, oy + 14, SkinS)
    px(img, ox + 16, oy + 14, SkinS)


def draw_neck_front(img, ox, oy):
    px(img, ox + 15, oy + 16, Skin)
    px(img, ox + 16, oy + 16, Skin)


def draw_shirt_front(img, ox, oy):
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
            px(img, ox + x, oy + y, c)


def draw_logo_front(img, ox, oy):
    lx, ly = ox + 13, oy + 19
    for dy in range(4):
        for dx in range(6):
            c = LogoP
            if dx == 0: c = LogoS
            elif dx == 5: c = LogoH
            if dy == 0: c = LogoH
            elif dy == 3: c = LogoS
            px(img, lx + dx, ly + dy, c)
    px(img, lx + 1, ly + 1, LogoO)
    px(img, lx + 4, ly + 1, LogoO)
    px(img, lx + 1, ly + 4, LogoS)
    px(img, lx + 4, ly + 4, LogoS)


def draw_pants_front(img, ox, oy):
    for y in range(24, 28):
        for x in range(10, 22):
            if y >= 26 and x in (15, 16):
                continue
            c = PantsS if x == 10 else Pants
            px(img, ox + x, oy + y, c)


def draw_shoes_front(img, ox, oy):
    for x in range(9, 15):
        c = ShoeH if x == 9 else Shoe
        px(img, ox + x, oy + 28, c)
        if x <= 13:
            px(img, ox + x, oy + 29, c)
    for x in range(17, 23):
        c = ShoeH if x == 22 else Shoe
        px(img, ox + x, oy + 28, c)
        if x >= 18:
            px(img, ox + x, oy + 29, c)


def _fill_body_segment(img, ox, oy, x1, y1, x2, y2, half_w, fill, shade, highlight):
    """Fill a rotated rectangle from (x1,y1) to (x2,y2) with half_w perpendicular width.

    Used for drawing thick body parts (torso, legs) on diagonal poses.
    Scans every pixel in the bounding box and checks if it falls inside the
    rotated rectangle, producing a solid filled parallelogram.
    """
    body_dx = x2 - x1
    body_dy = y2 - y1
    body_len = math.sqrt(body_dx * body_dx + body_dy * body_dy)
    if body_len < 0.1:
        return
    # Unit vectors along body
    ux, uy = body_dx / body_len, body_dy / body_len
    # Perpendicular (90° CCW): at ~48° body angle, this points lower-right
    px_dir, py_dir = -uy, ux

    # 4 corners of the parallelogram
    corners_x = [
        x1 - half_w * px_dir, x1 + half_w * px_dir,
        x2 + half_w * px_dir, x2 - half_w * px_dir,
    ]
    corners_y = [
        y1 - half_w * py_dir, y1 + half_w * py_dir,
        y2 + half_w * py_dir, y2 - half_w * py_dir,
    ]

    min_px = int(math.floor(min(corners_x))) - 1
    max_px = int(math.ceil(max(corners_x))) + 1
    min_py = int(math.floor(min(corners_y))) - 1
    max_py = int(math.ceil(max(corners_y))) + 1

    for scan_y in range(min_py, max_py + 1):
        for scan_x in range(min_px, max_px + 1):
            vx = scan_x - x1
            vy = scan_y - y1
            along = vx * ux + vy * uy
            perp = vx * px_dir + vy * py_dir
            if -0.7 <= along <= body_len + 0.7 and abs(perp) <= half_w + 0.3:
                c = fill
                if perp < -(half_w - 1.2):
                    c = highlight
                elif perp > (half_w - 1.2):
                    c = shade
                px(img, ox + scan_x, oy + scan_y, c)


def _draw_thick_arm(img, ox, oy, x1, y1, x2, y2, c1, c2):
    """Draw a 2px wide line from (x1,y1) to (x2,y2)."""
    steps = max(abs(x2 - x1), abs(y2 - y1), 1)
    for i in range(steps + 1):
        t = i / steps
        x = int(round(x1 + (x2 - x1) * t))
        y = int(round(y1 + (y2 - y1) * t))
        px(img, ox + x, oy + y, c1)
        if abs(x2 - x1) >= abs(y2 - y1):
            px(img, ox + x, oy + y + 1, c2)
        else:
            px(img, ox + x + 1, oy + y, c2)


def draw_circle_arms(img, ox, oy, frame):
    """Draw arms at positions along a circular path."""
    angle = frame * 2 * math.pi / 16

    l_sx, l_sy = 9, 18
    r_sx, r_sy = 22, 18
    radius = 5

    l_ex = l_sx + int(round(-radius * math.cos(angle)))
    l_ey = l_sy + int(round(-radius * math.sin(angle)))
    r_ex = r_sx + int(round(radius * math.cos(angle)))
    r_ey = r_sy + int(round(-radius * math.sin(angle)))

    l_mx = (l_sx + l_ex) // 2
    l_my = (l_sy + l_ey) // 2
    _draw_thick_arm(img, ox, oy, l_sx, l_sy, l_mx, l_my, ShirtS, Shirt)
    _draw_thick_arm(img, ox, oy, l_mx, l_my, l_ex, l_ey, SkinS, Skin)

    r_mx = (r_sx + r_ex) // 2
    r_my = (r_sy + r_ey) // 2
    _draw_thick_arm(img, ox, oy, r_sx, r_sy, r_mx, r_my, Shirt, ShirtH)
    _draw_thick_arm(img, ox, oy, r_mx, r_my, r_ex, r_ey, Skin, SkinH)


def draw_arm_circle_frame(img, ox, oy, frame):
    """Draw one frame of standing arm circles."""
    bob_curve = [0, 0, 0, 0, -1, -1, 0, 0, 0, 0, 0, 0, -1, -1, 0, 0]
    bob = bob_curve[frame]

    draw_hair_front(img, ox, oy + bob)
    draw_head_front(img, ox, oy + bob)
    draw_neck_front(img, ox, oy + bob)
    draw_shirt_front(img, ox, oy + bob)
    draw_logo_front(img, ox, oy + bob)
    draw_pants_front(img, ox, oy)
    draw_shoes_front(img, ox, oy)
    draw_circle_arms(img, ox, oy + bob, frame)


# =========================================================================
# PUMP-UP - "Let's do it!" fist pump (front view)
# =========================================================================

def draw_pumpup_arms(img, ox, oy, bounce, pump_phase):
    """Draw arms for pump-up animation.

    pump_phase:
      0 = arms at sides (ready stance)
      1 = both arms rising, fists clenching
      2 = right fist pumped overhead (peak)
      3 = arms coming back down
    """
    if pump_phase == 0:
        # Arms at sides, slightly bent (ready stance)
        # Left arm
        for dy in range(3):
            px(img, ox + 7, oy + 17 + bounce + dy, ShirtS)
            px(img, ox + 8, oy + 17 + bounce + dy, Shirt)
        for dy in range(2):
            px(img, ox + 7, oy + 20 + bounce + dy, SkinS)
            px(img, ox + 8, oy + 20 + bounce + dy, Skin)
        # Right arm
        for dy in range(3):
            px(img, ox + 23, oy + 17 + bounce + dy, Shirt)
            px(img, ox + 24, oy + 17 + bounce + dy, ShirtH)
        for dy in range(2):
            px(img, ox + 23, oy + 20 + bounce + dy, Skin)
            px(img, ox + 24, oy + 20 + bounce + dy, SkinH)

    elif pump_phase == 1:
        # Arms rising - elbows out, forearms angling up
        # Left arm bent up
        px(img, ox + 7, oy + 17 + bounce, ShirtS)
        px(img, ox + 8, oy + 17 + bounce, Shirt)
        px(img, ox + 6, oy + 16 + bounce, ShirtS)
        px(img, ox + 7, oy + 16 + bounce, Shirt)
        px(img, ox + 6, oy + 15 + bounce, SkinS)
        px(img, ox + 7, oy + 14 + bounce, Skin)
        # Fist
        px(img, ox + 7, oy + 13 + bounce, Skin)
        px(img, ox + 8, oy + 13 + bounce, SkinH)
        # Right arm bent up
        px(img, ox + 23, oy + 17 + bounce, Shirt)
        px(img, ox + 24, oy + 17 + bounce, ShirtH)
        px(img, ox + 24, oy + 16 + bounce, Shirt)
        px(img, ox + 25, oy + 16 + bounce, ShirtH)
        px(img, ox + 25, oy + 15 + bounce, Skin)
        px(img, ox + 24, oy + 14 + bounce, SkinH)
        # Fist
        px(img, ox + 24, oy + 13 + bounce, Skin)
        px(img, ox + 23, oy + 13 + bounce, SkinS)

    elif pump_phase == 2:
        # Right fist pumped overhead! Left arm bent at side
        # Left arm - fist at chest level
        px(img, ox + 7, oy + 17 + bounce, ShirtS)
        px(img, ox + 8, oy + 17 + bounce, Shirt)
        px(img, ox + 6, oy + 16 + bounce, ShirtS)
        px(img, ox + 7, oy + 15 + bounce, Shirt)
        px(img, ox + 7, oy + 14 + bounce, Skin)
        px(img, ox + 8, oy + 14 + bounce, SkinH)

        # Right arm - FULLY extended overhead
        # Upper arm
        px(img, ox + 23, oy + 17 + bounce, Shirt)
        px(img, ox + 24, oy + 17 + bounce, ShirtH)
        px(img, ox + 24, oy + 16 + bounce, Shirt)
        px(img, ox + 25, oy + 15 + bounce, ShirtH)
        # Forearm going up
        px(img, ox + 25, oy + 14 + bounce, Skin)
        px(img, ox + 25, oy + 13 + bounce, Skin)
        px(img, ox + 25, oy + 12 + bounce, SkinH)
        px(img, ox + 24, oy + 11 + bounce, SkinH)
        # Fist at top
        px(img, ox + 24, oy + 10 + bounce, Skin)
        px(img, ox + 25, oy + 10 + bounce, SkinH)
        px(img, ox + 24, oy + 9 + bounce, Skin)
        px(img, ox + 25, oy + 9 + bounce, SkinH)

    elif pump_phase == 3:
        # Same as phase 1 (coming back down)
        draw_pumpup_arms(img, ox, oy, bounce, 1)


def draw_pumpup_frame(img, ox, oy, frame):
    """Draw one frame of pump-up animation.

    16 frames:
      0-2:   ready stance, slight crouch
      3-4:   arms rising
      5-8:   fist pump overhead (hold at peak, energetic bounce)
      9-10:  arms lowering
      11-12: second pump rising
      13-15: fist pump again + hold
    """
    # Bounce curve - energetic vertical motion
    bounce_curve = [0, 0, 0, -1, -1, -2, -2, -1, -2, -1, 0, -1, -1, -2, -2, -1]
    bounce = bounce_curve[frame]

    # Pump phase mapping
    pump_phases = [0, 0, 0, 1, 1, 2, 2, 2, 2, 3, 0, 1, 1, 2, 2, 2]
    pump = pump_phases[frame]

    # Open mouth when pumping (excited!)
    excited = pump == 2

    # Draw body
    draw_hair_front(img, ox, oy + bounce)
    draw_head_front(img, ox, oy + bounce)

    # Override mouth when excited
    if excited:
        mouth_y = oy + bounce + 14
        # Big open smile
        px(img, ox + 14, mouth_y, O)
        px(img, ox + 15, mouth_y, O)
        px(img, ox + 16, mouth_y, O)
        px(img, ox + 17, mouth_y, O)

    draw_neck_front(img, ox, oy + bounce)
    draw_shirt_front(img, ox, oy + bounce)
    draw_logo_front(img, ox, oy + bounce)
    draw_pants_front(img, ox, oy)
    draw_shoes_front(img, ox, oy)

    # Draw pump-up arms
    draw_pumpup_arms(img, ox, oy, bounce, pump)


# =========================================================================
# WONDERING - looking around, no coffee (front view)
# =========================================================================

def draw_wondering_arms(img, ox, oy, breath):
    """Draw both arms relaxed at sides (no coffee mug)."""
    # Left arm relaxed at side
    for dy in range(3):
        px(img, ox + 7, oy + 17 + breath + dy, ShirtS)
        px(img, ox + 8, oy + 17 + breath + dy, Shirt)
    for dy in range(3):
        px(img, ox + 7, oy + 20 + breath + dy, SkinS)
        px(img, ox + 8, oy + 20 + breath + dy, Skin)

    # Right arm relaxed at side (mirrored, no mug)
    for dy in range(3):
        px(img, ox + 23, oy + 17 + breath + dy, Shirt)
        px(img, ox + 24, oy + 17 + breath + dy, ShirtH)
    for dy in range(3):
        px(img, ox + 23, oy + 20 + breath + dy, Skin)
        px(img, ox + 24, oy + 20 + breath + dy, SkinH)


def draw_wondering_frame(img, ox, oy, frame):
    """Draw one frame of wondering/looking around animation.

    16 frames cycle:
      0-3:   looking left
      4-7:   looking center
      8-11:  looking right
      12-15: looking center (with blink at 12-14)
    """
    # Breathing (same curve as coffee sip)
    breath_curve = [0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0]
    breath = breath_curve[frame]

    # Eye direction: -1 = left, 0 = center, 1 = right
    eye_dir_map = [-1, -1, -1, -1, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0]
    eye_dir = eye_dir_map[frame]

    # Blink at frames 12-14
    blink = frame in (12, 13, 14)

    # Draw body
    draw_hair_front(img, ox, oy + breath)
    draw_head_front(img, ox, oy + breath)

    # Override eyes for look direction
    if eye_dir != 0 and not blink:
        eye_y = oy + breath + 11
        # Clear default eyes
        for dy in range(2):
            for ex in [13, 14, 17, 18]:
                px(img, ox + ex, eye_y + dy, Skin)
        if eye_dir == -1:
            # Looking left: pupils shifted left
            px(img, ox + 13, eye_y, WH); px(img, ox + 14, eye_y, WH)
            px(img, ox + 13, eye_y + 1, O); px(img, ox + 14, eye_y + 1, WH)
            px(img, ox + 17, eye_y, WH); px(img, ox + 18, eye_y, WH)
            px(img, ox + 17, eye_y + 1, O); px(img, ox + 18, eye_y + 1, WH)
        else:
            # Looking right: pupils shifted right
            px(img, ox + 13, eye_y, WH); px(img, ox + 14, eye_y, WH)
            px(img, ox + 13, eye_y + 1, WH); px(img, ox + 14, eye_y + 1, O)
            px(img, ox + 17, eye_y, WH); px(img, ox + 18, eye_y, WH)
            px(img, ox + 17, eye_y + 1, WH); px(img, ox + 18, eye_y + 1, O)

    # Override eyes for blink
    if blink:
        blink_frame = frame - 12  # 0=closing, 1=closed, 2=opening
        eye_y = oy + breath + 11
        # Clear eyes with skin
        for dy in range(2):
            for ex in [13, 14, 17, 18]:
                px(img, ox + ex, eye_y + dy, Skin)
        if blink_frame == 0:
            px(img, ox + 13, eye_y + 1, O); px(img, ox + 14, eye_y + 1, O)
            px(img, ox + 17, eye_y + 1, O); px(img, ox + 18, eye_y + 1, O)
        elif blink_frame == 1:
            px(img, ox + 13, eye_y + 1, O); px(img, ox + 14, eye_y + 1, O)
            px(img, ox + 17, eye_y + 1, O); px(img, ox + 18, eye_y + 1, O)
        elif blink_frame == 2:
            px(img, ox + 13, eye_y, WH); px(img, ox + 14, eye_y, WH)
            px(img, ox + 13, eye_y + 1, O); px(img, ox + 14, eye_y + 1, WH)
            px(img, ox + 17, eye_y, WH); px(img, ox + 18, eye_y, WH)
            px(img, ox + 18, eye_y + 1, O); px(img, ox + 17, eye_y + 1, WH)

    draw_neck_front(img, ox, oy + breath)
    draw_shirt_front(img, ox, oy + breath)
    draw_logo_front(img, ox, oy + breath)
    draw_pants_front(img, ox, oy)
    draw_shoes_front(img, ox, oy)

    # Draw arms (both relaxed, no coffee)
    draw_wondering_arms(img, ox, oy, breath)


# =========================================================================
# SEATED HELPERS (shared by new seated exercises, rows 6-11)
# Character sits IN the chair (unlike Chair Dips where they're off it)
# SEAT_DX shifts character right so body is against the chair backrest.
# =========================================================================

SEAT_DX = 6


def draw_seated_legs(img, ox, oy):
    """Draw legs for seated-in-chair pose (side view).
    Thighs on seat, lower legs hanging down.
    """
    for y in range(23, 25):
        for x in range(10, 19):
            c = PantsS if x <= 11 else Pants
            px(img, ox + x, oy + y, c)
    for y in range(25, 28):
        for x in range(10, 13):
            c = PantsS if x == 10 else Pants
            px(img, ox + x, oy + y, c)
    for x in range(9, 13):
        c = ShoeH if x == 9 else Shoe
        px(img, ox + x, oy + 28, c)
    for x in range(9, 12):
        px(img, ox + x, oy + 29, Shoe)


def draw_seated_arms_resting(img, ox, oy, breath=0):
    """Draw arms resting on lap/thighs for seated pose (side view)."""
    shoulder_x, shoulder_y = 16, 18 + breath
    for dy in range(3):
        px(img, ox + shoulder_x, oy + shoulder_y + dy, Shirt)
        px(img, ox + shoulder_x + 1, oy + shoulder_y + dy, ShirtH)
    px(img, ox + 15, oy + 21 + breath, Skin)
    px(img, ox + 14, oy + 22 + breath, Skin)
    px(img, ox + 13, oy + 22 + breath, SkinH)
    px(img, ox + 12, oy + 23, Skin)
    px(img, ox + 13, oy + 23, SkinH)


# =========================================================================
# ROW 6: KNEE RAISES (seated, side view)
# =========================================================================

def draw_knee_raise_frame(img, ox, oy, frame):
    """Seated knee raises - thigh rotates forward 60-90° from vertical."""
    cx = ox + SEAT_DX
    raise_curve = [0, 1, 2, 3, 4, 4, 3, 2, 1, 0, 0, 0, 0, 0, 0, 0]
    knee_lift = raise_curve[frame]

    draw_office_chair(img, ox, oy)

    if knee_lift > 0:
        # 1. Resting leg (behind everything, still seated)
        draw_seated_legs(img, cx, oy)

        # 2. Upper body (middle layer)
        draw_side_hair(img, cx, oy)
        draw_side_head(img, cx, oy)
        draw_side_neck(img, cx, oy)
        draw_side_torso(img, cx, oy)
        draw_seated_arms_resting(img, cx, oy)

        # 3. Raised leg (front layer — drawn last to appear in front)
        # Hip joint at front-bottom of torso
        hip_x = cx + 13
        hip_y = oy + 23

        # Knee moves FORWARD (left) and UP as lift increases
        # Shorter thigh to match seated proportions
        knee_x = [0, cx + 10, cx + 8, cx + 7, cx + 6][knee_lift]
        knee_y = [0, oy + 22, oy + 21, oy + 20, oy + 20][knee_lift]

        # Thigh (hip to knee) - filled parallelogram
        _fill_body_segment(img, 0, 0,
                           float(hip_x), float(hip_y),
                           float(knee_x), float(knee_y),
                           1.8, Pants, PantsS, PantsS)

        # Lower leg hangs straight down from knee - 3px wide
        for dy in range(4):
            px(img, knee_x - 1, knee_y + 1 + dy, Pants)
            px(img, knee_x, knee_y + 1 + dy, Pants)
            px(img, knee_x + 1, knee_y + 1 + dy, PantsS)

        # Foot at bottom of lower leg
        foot_y = knee_y + 5
        px(img, knee_x - 1, foot_y, ShoeH)
        px(img, knee_x, foot_y, Shoe)
        px(img, knee_x - 1, foot_y + 1, Shoe)
        px(img, knee_x, foot_y + 1, Shoe)
    else:
        # Resting: legs first, then body on top
        draw_seated_legs(img, cx, oy)
        draw_side_hair(img, cx, oy)
        draw_side_head(img, cx, oy)
        draw_side_neck(img, cx, oy)
        draw_side_torso(img, cx, oy)
        draw_seated_arms_resting(img, cx, oy)


# =========================================================================
# ROW 7: SPINAL TWIST (seated, side view -> front view -> side view)
# =========================================================================

def draw_spinal_twist_frame(img, ox, oy, frame):
    """Seated spinal twist - character rotates from side to front view and back."""
    cx = ox + SEAT_DX      # side view character origin
    fx = cx - 4             # front view origin (align body centers)

    # View state: 0=side, 1=transition (wider), 2=front
    # Slower: long holds in side and front positions
    view_map = [0, 0, 0, 0, 1, 2, 2, 2, 2, 2, 1, 0, 0, 0, 0, 0]
    view = view_map[frame]

    draw_office_chair(img, ox, oy)
    draw_seated_legs(img, cx, oy)

    if view == 2:
        # Front view (twisted to face viewer)
        draw_hair_front(img, fx, oy)
        draw_head_front(img, fx, oy)
        draw_neck_front(img, fx, oy)
        draw_shirt_front(img, fx, oy)
        draw_logo_front(img, fx, oy)
        # Front view arms at sides
        for dy in range(3):
            px(img, fx + 7, oy + 17 + dy, ShirtS)
            px(img, fx + 8, oy + 17 + dy, Shirt)
        for dy in range(2):
            px(img, fx + 7, oy + 20 + dy, SkinS)
            px(img, fx + 8, oy + 20 + dy, Skin)
        for dy in range(3):
            px(img, fx + 23, oy + 17 + dy, Shirt)
            px(img, fx + 24, oy + 17 + dy, ShirtH)
        for dy in range(2):
            px(img, fx + 23, oy + 20 + dy, Skin)
            px(img, fx + 24, oy + 20 + dy, SkinH)
    elif view == 1:
        # Transition: slightly wider torso (between side and front)
        draw_side_hair(img, cx, oy)
        draw_side_head(img, cx, oy)
        draw_side_neck(img, cx, oy)
        for y in range(17, 24):
            left, right = 9, 18  # 1px wider each side than normal (10, 17)
            if y >= 22:
                left, right = 10, 17
            for x in range(left, right + 1):
                c = Shirt
                if x == left:
                    c = ShirtS
                elif x == right:
                    c = ShirtH
                px(img, cx + x, oy + y, c)
        px(img, cx + 11, oy + 19, LogoP)
        px(img, cx + 12, oy + 19, LogoP)
        px(img, cx + 13, oy + 19, LogoH)
        px(img, cx + 11, oy + 20, LogoS)
        px(img, cx + 12, oy + 20, LogoP)
        px(img, cx + 13, oy + 20, LogoP)
        draw_seated_arms_resting(img, cx, oy)
    else:
        # Side view (resting)
        draw_side_hair(img, cx, oy)
        draw_side_head(img, cx, oy)
        draw_side_neck(img, cx, oy)
        draw_side_torso(img, cx, oy)
        draw_seated_arms_resting(img, cx, oy)


# =========================================================================
# ROW 8: GLUTE SQUEEZE (seated, side view)
# =========================================================================

def draw_glute_squeeze_frame(img, ox, oy, frame):
    """Seated glute squeeze - nearly static, 1px posture shift."""
    cx = ox + SEAT_DX
    # One rep: up, hold, down
    squeeze_curve = [0, 0, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 0, 0, 0]
    squeeze = squeeze_curve[frame]

    draw_office_chair(img, ox, oy)
    draw_seated_legs(img, cx, oy)
    draw_side_hair(img, cx, oy + squeeze)
    draw_side_head(img, cx, oy + squeeze)
    draw_side_neck(img, cx, oy + squeeze)
    draw_side_torso(img, cx, oy + squeeze)
    draw_seated_arms_resting(img, cx, oy, squeeze)


# =========================================================================
# ROW 9: SHOULDER ROLLS (seated, side view)
# =========================================================================

def draw_shoulder_rolls_frame(img, ox, oy, frame):
    """Seated shoulder rolls - shoulder area orbits in circular motion."""
    cx = ox + SEAT_DX
    angle = frame * 2 * math.pi / 16
    sdx = int(round(1.5 * math.cos(angle)))
    sdy = int(round(1.5 * math.sin(angle)))

    draw_office_chair(img, ox, oy)
    draw_seated_legs(img, cx, oy)
    draw_side_hair(img, cx, oy)
    draw_side_head(img, cx, oy)
    draw_side_neck(img, cx, oy)

    # Torso with shoulder shift in upper portion
    for y in range(17, 24):
        base_left, base_right = 10, 17
        if y >= 22:
            base_left, base_right = 11, 16
        dx_offset = sdx if y <= 19 else 0
        dy_offset = sdy if y <= 19 else 0
        for x in range(base_left + dx_offset, base_right + 1 + dx_offset):
            c = Shirt
            if x == base_left + dx_offset:
                c = ShirtS
            elif x == base_right + dx_offset:
                c = ShirtH
            px(img, cx + x, oy + y + dy_offset, c)

    px(img, cx + 11, oy + 19, LogoP)
    px(img, cx + 12, oy + 19, LogoP)
    px(img, cx + 13, oy + 19, LogoH)
    px(img, cx + 11, oy + 20, LogoS)
    px(img, cx + 12, oy + 20, LogoP)
    px(img, cx + 13, oy + 20, LogoP)

    # Arm follows shoulder shift
    shoulder_x = 16 + sdx
    shoulder_y = 18 + sdy
    for dy in range(3):
        px(img, cx + shoulder_x, oy + shoulder_y + dy, Shirt)
        px(img, cx + shoulder_x + 1, oy + shoulder_y + dy, ShirtH)
    px(img, cx + 15 + sdx, oy + 21 + sdy, Skin)
    px(img, cx + 14, oy + 22, Skin)
    px(img, cx + 13, oy + 22, SkinH)
    px(img, cx + 12, oy + 23, Skin)
    px(img, cx + 13, oy + 23, SkinH)


# =========================================================================
# ROW 10: LEG EXTENSIONS (seated, side view)
# =========================================================================

def draw_leg_extension_frame(img, ox, oy, frame):
    """Seated leg extensions - lower leg extends to horizontal."""
    cx = ox + SEAT_DX
    ext_curve = [0, 1, 2, 3, 4, 5, 5, 4, 3, 2, 1, 0, 0, 0, 0, 0]
    ext = ext_curve[frame]

    draw_office_chair(img, ox, oy)

    # Thighs on seat
    for y in range(23, 25):
        for x in range(10, 19):
            c = PantsS if x <= 11 else Pants
            px(img, cx + x, oy + y, c)

    if ext > 0:
        # Lower leg extending - longer reach, perfectly horizontal at max
        # Knee at seat edge, foot interpolates from hanging to horizontal
        knee_x = cx + 10
        knee_y = oy + 25
        # At max (ext=5): foot 7px left of knee, same height = straight
        foot_x = int(round(knee_x - ext * 7 / 5))
        foot_y = int(round(oy + 28 - ext * 3 / 5))

        steps = max(abs(foot_x - knee_x), abs(foot_y - knee_y), 1)
        for i in range(steps + 1):
            t = i / steps
            lx = int(round(knee_x + (foot_x - knee_x) * t))
            ly = int(round(knee_y + (foot_y - knee_y) * t))
            px(img, lx, ly - 1, Pants)
            px(img, lx, ly, Pants)
            px(img, lx, ly + 1, PantsS)

        # Thick foot
        px(img, foot_x - 1, foot_y - 1, ShoeH)
        px(img, foot_x, foot_y - 1, Shoe)
        px(img, foot_x - 1, foot_y, Shoe)
        px(img, foot_x, foot_y, Shoe)
    else:
        draw_seated_legs(img, cx, oy)

    # Upper body
    draw_side_hair(img, cx, oy)
    draw_side_head(img, cx, oy)
    draw_side_neck(img, cx, oy)
    draw_side_torso(img, cx, oy)
    draw_seated_arms_resting(img, cx, oy)


# =========================================================================
# ROW 11: NECK STRETCH (front view, standing)
# Head tilts side to side with hand on head
# =========================================================================

def draw_neck_stretch_frame(img, ox, oy, frame):
    """Front view neck stretch - head tilts with hand assist."""
    # One side only: tilt left, hold, return
    tilt_curve = [0, 0, -1, -2, -2, -2, -2, -2, -2, -2, -1, 0, 0, 0, 0, 0]
    tilt = tilt_curve[frame]

    # Head tilts, body stays centered
    draw_hair_front(img, ox + tilt, oy)
    draw_head_front(img, ox + tilt, oy)

    # Closed relaxed eyes during hold
    if abs(tilt) == 2:
        eye_y = oy + 11
        for dy in range(2):
            for ex in [13, 14, 17, 18]:
                px(img, ox + tilt + ex, eye_y + dy, Skin)
        px(img, ox + tilt + 13, eye_y + 1, SkinS)
        px(img, ox + tilt + 14, eye_y + 1, SkinS)
        px(img, ox + tilt + 17, eye_y + 1, SkinS)
        px(img, ox + tilt + 18, eye_y + 1, SkinS)

    draw_neck_front(img, ox, oy)
    draw_shirt_front(img, ox, oy)
    draw_logo_front(img, ox, oy)
    draw_pants_front(img, ox, oy)
    draw_shoes_front(img, ox, oy)

    if tilt < 0:
        # Tilting left: LEFT arm up to left side of head, right arm at side
        for dy in range(3):
            px(img, ox + 23, oy + 17 + dy, Shirt)
            px(img, ox + 24, oy + 17 + dy, ShirtH)
        for dy in range(3):
            px(img, ox + 23, oy + 20 + dy, Skin)
            px(img, ox + 24, oy + 20 + dy, SkinH)
        # Left arm up to left side of tilted head
        px(img, ox + 7, oy + 17, ShirtS)
        px(img, ox + 8, oy + 17, Shirt)
        px(img, ox + 8, oy + 16, Shirt)
        px(img, ox + 9, oy + 15, Skin)
        px(img, ox + 10, oy + 14, Skin)
        px(img, ox + 11, oy + 13, SkinS)
        px(img, ox + tilt + 11, oy + 11, SkinS)
        px(img, ox + tilt + 10, oy + 11, Skin)
    elif tilt > 0:
        # Tilting right: RIGHT arm up to right side of head, left arm at side
        for dy in range(3):
            px(img, ox + 7, oy + 17 + dy, ShirtS)
            px(img, ox + 8, oy + 17 + dy, Shirt)
        for dy in range(3):
            px(img, ox + 7, oy + 20 + dy, SkinS)
            px(img, ox + 8, oy + 20 + dy, Skin)
        # Right arm up to right side of tilted head
        px(img, ox + 23, oy + 17, Shirt)
        px(img, ox + 24, oy + 17, ShirtH)
        px(img, ox + 23, oy + 16, Shirt)
        px(img, ox + 22, oy + 15, Skin)
        px(img, ox + 21, oy + 14, Skin)
        px(img, ox + 20, oy + 13, SkinH)
        px(img, ox + tilt + 20, oy + 11, Skin)
        px(img, ox + tilt + 21, oy + 11, SkinH)
    else:
        # Both arms at sides
        for dy in range(3):
            px(img, ox + 7, oy + 17 + dy, ShirtS)
            px(img, ox + 8, oy + 17 + dy, Shirt)
        for dy in range(3):
            px(img, ox + 7, oy + 20 + dy, SkinS)
            px(img, ox + 8, oy + 20 + dy, Skin)
        for dy in range(3):
            px(img, ox + 23, oy + 17 + dy, Shirt)
            px(img, ox + 24, oy + 17 + dy, ShirtH)
        for dy in range(3):
            px(img, ox + 23, oy + 20 + dy, Skin)
            px(img, ox + 24, oy + 20 + dy, SkinH)


# =========================================================================
# STANDING/ACTIVE EXERCISE HELPERS (rows 12-17)
# =========================================================================

# Desk wood colors
DeskTop      = (0x8B, 0x6B, 0x4A, 255)
DeskLeg      = (0x6B, 0x4E, 0x37, 255)
DeskHighlight = (0xA8, 0x85, 0x60, 255)

# Wall colors
WallColor     = (0x9E, 0x9E, 0xA8, 255)
WallShade     = (0x85, 0x85, 0x90, 255)
WallHighlight = (0xB5, 0xB5, 0xBE, 255)


def draw_wall_side(img, ox, oy):
    """Draw vertical wall band on right side (x=27-30, full height)."""
    for y in range(0, 32):
        px(img, ox + 27, oy + y, WallShade)
        px(img, ox + 28, oy + y, WallColor)
        px(img, ox + 29, oy + y, WallColor)
        px(img, ox + 30, oy + y, WallHighlight)


def draw_side_standing_legs(img, ox, oy):
    """Draw side-view standing legs (facing left)."""
    # Upper legs / thighs
    for y in range(24, 27):
        for x in range(11, 15):
            c = PantsS if x == 11 else Pants
            px(img, ox + x, oy + y, c)
    # Lower legs
    for y in range(27, 29):
        for x in range(10, 14):
            c = PantsS if x == 10 else Pants
            px(img, ox + x, oy + y, c)
    # Feet (pointing left)
    for x in range(8, 14):
        c = ShoeH if x == 8 else Shoe
        px(img, ox + x, oy + 29, c)


# =========================================================================
# ROW 12: DESK PUSH-UPS (side view, facing right, diagonal body)
# Character faces right. Body forms one straight line from feet to head
# at ~45 degrees. Hands on desk edge. Arms bend/extend during push-up.
# =========================================================================

def draw_desk_pushup_frame(img, ox, oy, frame):
    """Desk push-up: side view facing right, full-scale body proportions.

    Entire body (head, shoulders, hips, knees, ankles) aligned in one
    straight diagonal line. Hands on desk front edge. No hip bend.
    Top: arms straight, chest away. Bottom: elbows ~90 degrees.
    Body proportions match original standing character (~24px total).
    """
    # One rep: down, hold, up
    dip_curve = [0, 0, 1, 2, 3, 4, 4, 4, 4, 4, 3, 2, 1, 0, 0, 0]
    dip = dip_curve[frame]

    # --- DESK (right side of frame, tabletop at y=16) ---
    for x in range(22, 31):
        c = DeskHighlight if x >= 29 else DeskTop
        px(img, ox + x, oy + 16, c)
        px(img, ox + x, oy + 17, DeskTop)
    for y in range(18, 30):
        px(img, ox + 22, oy + y, DeskLeg)
        px(img, ox + 23, oy + y, DeskHighlight if y == 18 else DeskLeg)
    for y in range(18, 30):
        px(img, ox + 29, oy + y, DeskLeg)
        px(img, ox + 30, oy + y, DeskHighlight if y == 18 else DeskLeg)

    # --- BODY GEOMETRY ---
    # Body angle: 48 deg at top -> 35 deg at bottom
    angle = math.radians(48.0 - dip * 13.0 / 4.0)
    cos_a, sin_a = math.cos(angle), math.sin(angle)

    # Foot anchor (shifted left to fit longer body)
    fx, fy = 1.0, 29.0

    def bp(dist):
        """Body point at given distance from feet along diagonal."""
        return (int(round(fx + dist * cos_a)),
                int(round(fy - dist * sin_a)))

    # Proportional body points matching original character scale
    ankle = bp(1)       # just above feet
    knee = bp(6)        # 5px shin
    hip = bp(11)        # 5px thigh
    shoulder = bp(18)   # 7px torso
    neck = bp(19)       # 1px neck

    # --- FEET (flat on ground) ---
    for x in range(0, 5):
        c = ShoeH if x == 0 else Shoe
        px(img, ox + x, oy + 29, c)
    px(img, ox + 1, oy + 28, Shoe)
    px(img, ox + 2, oy + 28, Shoe)
    px(img, ox + 3, oy + 28, ShoeH)

    # --- LEGS: filled parallelograms matching seated side-view thickness ---
    # Use float body points for accurate segment filling
    ankle_f = (fx + 1 * cos_a, fy - 1 * sin_a)
    knee_f = (fx + 6 * cos_a, fy - 6 * sin_a)
    hip_f = (fx + 11 * cos_a, fy - 11 * sin_a)
    shoulder_f = (fx + 18 * cos_a, fy - 18 * sin_a)

    # Calf (ankle to knee): half_w=2.0 (~4-5px wide, visible calf shape)
    _fill_body_segment(img, ox, oy,
                       ankle_f[0], ankle_f[1], knee_f[0], knee_f[1],
                       2.0, Pants, PantsS, PantsS)
    # Thigh (knee to hip): half_w=2.8 (~6px wide, matching seated upper leg)
    _fill_body_segment(img, ox, oy,
                       knee_f[0], knee_f[1], hip_f[0], hip_f[1],
                       2.8, Pants, PantsS, PantsS)

    # --- TORSO: filled parallelogram matching original 8px side-view width ---
    _fill_body_segment(img, ox, oy,
                       hip_f[0], hip_f[1], shoulder_f[0], shoulder_f[1],
                       4.0, Shirt, ShirtS, ShirtH)

    # Claude logo on torso face (using perpendicular offsets)
    perp_x, perp_y = -sin_a, cos_a
    logo1 = bp(14)
    logo2 = bp(15)
    for lpt in [logo1, logo2]:
        lx, ly = lpt
        for j in range(-1, 2):
            px_x = int(round(lx + j * perp_x))
            px_y = int(round(ly + j * perp_y))
            if lpt == logo1:
                c = LogoH if j >= 1 else LogoP
            else:
                c = LogoP if j >= 0 else LogoS
            px(img, ox + px_x, oy + px_y, c)

    # --- NECK ---
    px(img, ox + neck[0], oy + neck[1], Skin)
    px(img, ox + neck[0] + 1, oy + neck[1], SkinH)

    # --- HEAD (7x7 facing right, matching original character head) ---
    hc = bp(22)  # head center: 3px beyond neck
    hx, hy = hc
    # 7px head shape with rounded corners
    for dy in range(-3, 4):
        if abs(dy) == 3:
            xr = range(-2, 3)   # 5px at top/bottom rows
        else:
            xr = range(-3, 4)   # 7px middle rows
        for dx in xr:
            c = Skin
            if dx <= -2:
                c = SkinS
            elif dx >= 2:
                c = SkinH
            px(img, ox + hx + dx, oy + hy + dy, c)

    # Hair (3px fringe on top, back-of-head on left)
    for dx in range(-1, 2):
        px(img, ox + hx + dx, oy + hy - 5, Hair)
    for dx in range(-2, 3):
        c = HairH if dx >= 1 else Hair
        px(img, ox + hx + dx, oy + hy - 4, c)
    for dx in range(-2, 3):
        c = HairH if dx >= 1 else Hair
        px(img, ox + hx + dx, oy + hy - 3, c)
    # Back-of-head hair (left side since facing right)
    for dy in range(-2, 1):
        px(img, ox + hx - 3, oy + hy + dy, Hair)
        px(img, ox + hx - 4, oy + hy + dy, HairH)

    # Eye (right side, facing right)
    px(img, ox + hx + 1, oy + hy - 1, WH)
    px(img, ox + hx + 2, oy + hy - 1, WH)
    px(img, ox + hx + 2, oy + hy, O)   # pupil
    px(img, ox + hx + 1, oy + hy, WH)
    # Nose (bump beyond right edge)
    px(img, ox + hx + 4, oy + hy, Skin)
    px(img, ox + hx + 4, oy + hy + 1, SkinH)
    # Mouth
    px(img, ox + hx + 1, oy + hy + 2, SkinS)
    px(img, ox + hx + 2, oy + hy + 2, SkinS)

    # --- ARMS (shoulder to desk) ---
    sx, sy = shoulder
    hand_x, hand_y = 22, 16  # on desk front edge

    # Elbow bends downward with dip
    elbow_x = (sx + hand_x) // 2 + 1
    elbow_y = (sy + hand_y) // 2 + dip * 3 // 4

    # Upper arm (shirt)
    _draw_thick_arm(img, ox, oy, sx, sy, elbow_x, elbow_y, Shirt, ShirtH)
    # Forearm (skin)
    _draw_thick_arm(img, ox, oy, elbow_x, elbow_y, hand_x, hand_y, Skin, SkinH)
    # Hand on desk edge
    px(img, ox + hand_x, oy + hand_y, Skin)
    px(img, ox + hand_x, oy + hand_y - 1, SkinH)
    px(img, ox + hand_x - 1, oy + hand_y, SkinS)


# =========================================================================
# ROW 13: BODYWEIGHT SQUATS (front view)
# =========================================================================

def draw_squat_frame(img, ox, oy, frame):
    """Front view squats - body drops, knees spread outward."""
    squat_curve = [0, 0, 1, 2, 3, 4, 5, 5, 4, 3, 2, 1, 0, 0, 0, 0]
    depth = squat_curve[frame]

    # Upper body drops with squat
    draw_hair_front(img, ox, oy + depth)
    draw_head_front(img, ox, oy + depth)
    draw_neck_front(img, ox, oy + depth)
    draw_shirt_front(img, ox, oy + depth)
    draw_logo_front(img, ox, oy + depth)

    # Arms out front for balance
    if depth > 0:
        for dy in range(2):
            px(img, ox + 6, oy + 18 + depth + dy, ShirtS)
            px(img, ox + 7, oy + 18 + depth + dy, Shirt)
        px(img, ox + 5, oy + 19 + depth, SkinS)
        px(img, ox + 4, oy + 19 + depth, Skin)
        for dy in range(2):
            px(img, ox + 24, oy + 18 + depth + dy, Shirt)
            px(img, ox + 25, oy + 18 + depth + dy, ShirtH)
        px(img, ox + 26, oy + 19 + depth, Skin)
        px(img, ox + 27, oy + 19 + depth, SkinH)
    else:
        # Arms at sides
        for dy in range(3):
            px(img, ox + 7, oy + 17 + dy, ShirtS)
            px(img, ox + 8, oy + 17 + dy, Shirt)
        for dy in range(3):
            px(img, ox + 7, oy + 20 + dy, SkinS)
            px(img, ox + 8, oy + 20 + dy, Skin)
        for dy in range(3):
            px(img, ox + 23, oy + 17 + dy, Shirt)
            px(img, ox + 24, oy + 17 + dy, ShirtH)
        for dy in range(3):
            px(img, ox + 23, oy + 20 + dy, Skin)
            px(img, ox + 24, oy + 20 + dy, SkinH)

    # Custom legs - knees spread outward as depth increases
    knee_spread = depth // 2  # 0-2 pixels outward

    # Left leg
    for y in range(24 + depth, 28):
        left_x = 10 - knee_spread
        for x in range(left_x, left_x + 4):
            c = PantsS if x == left_x else Pants
            px(img, ox + x, oy + y, c)

    # Right leg
    for y in range(24 + depth, 28):
        right_x = 18 + knee_spread
        for x in range(right_x, right_x + 4):
            c = Pants if x == right_x + 3 else Pants
            if x == right_x:
                c = PantsS
            px(img, ox + x, oy + y, c)

    # Feet - widen with squat
    for x in range(8 - knee_spread, 14 - knee_spread):
        c = ShoeH if x == 8 - knee_spread else Shoe
        px(img, ox + x, oy + 28, c)
        if x <= 12 - knee_spread:
            px(img, ox + x, oy + 29, c)
    for x in range(18 + knee_spread, 24 + knee_spread):
        c = ShoeH if x == 23 + knee_spread else Shoe
        px(img, ox + x, oy + 28, c)
        if x >= 19 + knee_spread:
            px(img, ox + x, oy + 29, c)


# =========================================================================
# ROW 14: STANDING CALF RAISES (front view)
# =========================================================================

def draw_calf_raise_frame(img, ox, oy, frame):
    """Front view calf raises - heels lift, toes stay on ground."""
    # One rep: up, hold, down
    lift_curve = [0, 0, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1, 0, 0, 0]
    lift = lift_curve[frame]

    # Upper body lifts
    draw_hair_front(img, ox, oy - lift)
    draw_head_front(img, ox, oy - lift)
    draw_neck_front(img, ox, oy - lift)
    draw_shirt_front(img, ox, oy - lift)
    draw_logo_front(img, ox, oy - lift)

    # Arms at sides (lift with body)
    for dy in range(3):
        px(img, ox + 7, oy - lift + 17 + dy, ShirtS)
        px(img, ox + 8, oy - lift + 17 + dy, Shirt)
    for dy in range(3):
        px(img, ox + 7, oy - lift + 20 + dy, SkinS)
        px(img, ox + 8, oy - lift + 20 + dy, Skin)
    for dy in range(3):
        px(img, ox + 23, oy - lift + 17 + dy, Shirt)
        px(img, ox + 24, oy - lift + 17 + dy, ShirtH)
    for dy in range(3):
        px(img, ox + 23, oy - lift + 20 + dy, Skin)
        px(img, ox + 24, oy - lift + 20 + dy, SkinH)

    # Legs stretch from lifted body down to grounded feet
    # Top of legs lifts with body, bottom stays near ground
    for y in range(24 - lift, 28):
        for x in range(10, 22):
            if y >= 26 and x in (15, 16):
                continue  # gap between legs in lower portion
            c = PantsS if x == 10 else Pants
            px(img, ox + x, oy + y, c)

    # Feet - toes always at ground (y=29), heels lift when raised
    if lift > 0:
        # Tiptoe: narrow toes at ground level
        for x in range(11, 14):
            px(img, ox + x, oy + 29, Shoe)
        for x in range(18, 21):
            px(img, ox + x, oy + 29, Shoe)
        # Ankle area at y=28 (connects legs to toes)
        for x in range(10, 14):
            px(img, ox + x, oy + 28, Shoe)
        for x in range(18, 22):
            px(img, ox + x, oy + 28, Shoe)
    else:
        draw_shoes_front(img, ox, oy)


# =========================================================================
# ROW 15: WALL SIT (side view)
# =========================================================================

WALL_DX = 8  # Shift character right so back touches wall


def draw_wall_sit_frame(img, ox, oy, frame):
    """Side view wall sit - slides from standing to squat against wall."""
    # One rep: slide down, hold, slide up
    squat_curve = [0, 0, 1, 2, 3, 4, 4, 4, 4, 4, 4, 3, 2, 1, 0, 0]
    squat = squat_curve[frame]
    body_drop = min(squat, 2)  # body drops at most 2px
    cx = ox + WALL_DX

    # Draw wall first (behind everything)
    draw_wall_side(img, ox, oy)

    # Upper body slides down wall
    draw_side_hair(img, cx, oy + body_drop)
    draw_side_head(img, cx, oy + body_drop)
    draw_side_neck(img, cx, oy + body_drop)
    draw_side_torso(img, cx, oy + body_drop)

    # Arms on thighs
    shoulder_x, shoulder_y = 16, 18 + body_drop
    for dy in range(3):
        px(img, cx + shoulder_x, oy + shoulder_y + dy, Shirt)
        px(img, cx + shoulder_x + 1, oy + shoulder_y + dy, ShirtH)
    px(img, cx + 15, oy + 21 + body_drop, Skin)
    px(img, cx + 14, oy + 22 + body_drop, Skin)
    px(img, cx + 13, oy + 23 + body_drop, SkinH)

    if squat == 0:
        # Standing legs
        draw_side_standing_legs(img, cx, oy)
    else:
        # Legs transition: knees push forward as squat deepens
        hip_y = 23 + body_drop
        knee_fwd = squat + 1  # how far forward knee extends (2-5)
        knee_x = 11 - knee_fwd

        # Thighs (from hip extending forward, increasingly horizontal)
        for y in range(hip_y, hip_y + 2):
            for x in range(knee_x, 14):
                c = PantsS if x == knee_x else Pants
                px(img, cx + x, oy + y, c)

        # Lower legs (vertical from knee to ground)
        for y in range(hip_y + 2, 29):
            for x in range(knee_x - 1, knee_x + 2):
                c = PantsS if x == knee_x - 1 else Pants
                px(img, cx + x, oy + y, c)

        # Feet flat on ground
        for x in range(knee_x - 2, knee_x + 2):
            c = ShoeH if x == knee_x - 2 else Shoe
            px(img, cx + x, oy + 29, c)


# =========================================================================
# ROW 16: STANDING TORSO ROTATION (front <-> side)
# =========================================================================

def _draw_side_upper_body_right(img, ox, oy):
    """Draw side-view upper body facing RIGHT by mirroring the left-facing view."""
    temp = Image.new("RGBA", (32, 32), (0, 0, 0, 0))
    draw_side_hair(temp, 0, 0)
    draw_side_head(temp, 0, 0)
    draw_side_neck(temp, 0, 0)
    draw_side_torso(temp, 0, 0)
    # Include arm
    for dy in range(3):
        px(temp, 16, 18 + dy, Shirt)
        px(temp, 17, 18 + dy, ShirtH)
    px(temp, 15, 21, Skin)
    px(temp, 14, 22, Skin)
    px(temp, 13, 22, SkinH)
    temp = temp.transpose(Image.FLIP_LEFT_RIGHT)
    for y in range(32):
        for x in range(32):
            c = temp.getpixel((x, y))
            if c[3] > 0:
                px(img, ox + x, oy + y, c)


def _draw_side_upper_body_right_wide(img, ox, oy):
    """Draw wider transition torso facing RIGHT (mirrored)."""
    temp = Image.new("RGBA", (32, 32), (0, 0, 0, 0))
    draw_side_hair(temp, 0, 0)
    draw_side_head(temp, 0, 0)
    draw_side_neck(temp, 0, 0)
    for y in range(17, 24):
        left, right = 9, 18
        if y >= 22:
            left, right = 10, 17
        for x in range(left, right + 1):
            c = Shirt
            if x == left:
                c = ShirtS
            elif x == right:
                c = ShirtH
            px(temp, x, y, c)
    px(temp, 11, 19, LogoP)
    px(temp, 12, 19, LogoP)
    px(temp, 13, 19, LogoH)
    px(temp, 11, 20, LogoS)
    px(temp, 12, 20, LogoP)
    px(temp, 13, 20, LogoP)
    for dy in range(3):
        px(temp, 16, 18 + dy, Shirt)
        px(temp, 17, 18 + dy, ShirtH)
    px(temp, 15, 21, Skin)
    px(temp, 14, 22, SkinH)
    temp = temp.transpose(Image.FLIP_LEFT_RIGHT)
    for y in range(32):
        for x in range(32):
            c = temp.getpixel((x, y))
            if c[3] > 0:
                px(img, ox + x, oy + y, c)


def draw_torso_rotation_frame(img, ox, oy, frame):
    """Standing torso rotation - one left, one right."""
    # 0=front, 1=trans-left, 2=side-left, 3=trans-right, 4=side-right
    view_map = [0, 0, 1, 2, 2, 1, 0, 0, 0, 3, 4, 4, 4, 3, 0, 0]
    view = view_map[frame]

    # Legs always front-view standing (fixed, don't rotate)
    draw_pants_front(img, ox, oy)
    draw_shoes_front(img, ox, oy)

    if view == 2:
        # Side view facing LEFT
        sx = ox + 4
        draw_side_hair(img, sx, oy)
        draw_side_head(img, sx, oy)
        draw_side_neck(img, sx, oy)
        draw_side_torso(img, sx, oy)
        shoulder_x, shoulder_y = 16, 18
        for dy in range(3):
            px(img, sx + shoulder_x, oy + shoulder_y + dy, Shirt)
            px(img, sx + shoulder_x + 1, oy + shoulder_y + dy, ShirtH)
        px(img, sx + 15, oy + 21, Skin)
        px(img, sx + 14, oy + 22, Skin)
        px(img, sx + 13, oy + 22, SkinH)
    elif view == 4:
        # Side view facing RIGHT (mirrored)
        _draw_side_upper_body_right(img, ox - 4, oy)
    elif view == 1:
        # Transition to left: wider side-view torso
        sx = ox + 4
        draw_side_hair(img, sx, oy)
        draw_side_head(img, sx, oy)
        draw_side_neck(img, sx, oy)
        for y in range(17, 24):
            left, right = 9, 18
            if y >= 22:
                left, right = 10, 17
            for x in range(left, right + 1):
                c = Shirt
                if x == left:
                    c = ShirtS
                elif x == right:
                    c = ShirtH
                px(img, sx + x, oy + y, c)
        px(img, sx + 11, oy + 19, LogoP)
        px(img, sx + 12, oy + 19, LogoP)
        px(img, sx + 13, oy + 19, LogoH)
        px(img, sx + 11, oy + 20, LogoS)
        px(img, sx + 12, oy + 20, LogoP)
        px(img, sx + 13, oy + 20, LogoP)
        for dy in range(3):
            px(img, sx + 16, oy + 18 + dy, Shirt)
            px(img, sx + 17, oy + 18 + dy, ShirtH)
        px(img, sx + 15, oy + 21, Skin)
        px(img, sx + 14, oy + 22, SkinH)
    elif view == 3:
        # Transition to right (mirrored wider torso)
        _draw_side_upper_body_right_wide(img, ox - 4, oy)
    else:
        # Front view (resting)
        draw_hair_front(img, ox, oy)
        draw_head_front(img, ox, oy)
        draw_neck_front(img, ox, oy)
        draw_shirt_front(img, ox, oy)
        draw_logo_front(img, ox, oy)
        # Front view arms at sides
        for dy in range(3):
            px(img, ox + 7, oy + 17 + dy, ShirtS)
            px(img, ox + 8, oy + 17 + dy, Shirt)
        for dy in range(3):
            px(img, ox + 7, oy + 20 + dy, SkinS)
            px(img, ox + 8, oy + 20 + dy, Skin)
        for dy in range(3):
            px(img, ox + 23, oy + 17 + dy, Shirt)
            px(img, ox + 24, oy + 17 + dy, ShirtH)
        for dy in range(3):
            px(img, ox + 23, oy + 20 + dy, Skin)
            px(img, ox + 24, oy + 20 + dy, SkinH)


# =========================================================================
# ROW 17: REVERSE LUNGES (side view)
# =========================================================================

def draw_reverse_lunge_frame(img, ox, oy, frame):
    """Side view reverse lunges - proper form.

    - Front knee at ~90°, stacked above ankle (not past toes)
    - Back knee hovers near ground, pointing down
    - Back foot on toes only
    - Torso stays vertical throughout
    - Hips move straight down
    """
    lunge_curve = [0, 0, 1, 2, 3, 4, 4, 3, 2, 1, 0, 0, 0, 0, 0, 0]
    depth = lunge_curve[frame]

    if depth == 0:
        # Standing position - standard side-view character
        draw_side_standing_legs(img, ox, oy)
        draw_side_hair(img, ox, oy)
        draw_side_head(img, ox, oy)
        draw_side_neck(img, ox, oy)
        draw_side_torso(img, ox, oy)
        # Arm relaxed at side
        for dy in range(3):
            px(img, ox + 16, oy + 18 + dy, Shirt)
            px(img, ox + 17, oy + 18 + dy, ShirtH)
        px(img, ox + 15, oy + 21, Skin)
        px(img, ox + 14, oy + 22, SkinH)
        return

    # --- LUNGE POSITION (depth 1-4) ---
    # Hips drop straight down
    body_drop = [0, 0, 1, 2, 3][depth]
    hip_y = 23 + body_drop

    # Front knee: above ankle, approaches 90° at max depth
    front_foot_cx = 10  # foot center (fixed on ground)
    front_knee_x = [0, 11, 11, 10, 10][depth]
    front_knee_y = hip_y + (1 if depth <= 2 else 0)

    # Back knee & foot positions per depth (carefully tuned)
    bk_x = [0, 15, 16, 18, 19][depth]
    bk_y = [0, 26, 27, 28, 28][depth]
    bf_x = [0, 16, 18, 20, 22][depth]

    # ---- DRAW ORDER: back leg, front leg, upper body ----

    # BACK THIGH: hip to back knee (diagonal, filled parallelogram)
    _fill_body_segment(img, ox, oy,
                       14.0, float(hip_y),
                       float(bk_x), float(bk_y),
                       1.8, Pants, PantsS, PantsS)
    # BACK SHIN: knee to foot (filled parallelogram)
    _fill_body_segment(img, ox, oy,
                       float(bk_x), float(bk_y),
                       float(bf_x), 29.0,
                       1.2, Pants, PantsS, PantsS)
    # Back foot: on toes only (2px)
    px(img, ox + bf_x, oy + 29, Shoe)
    px(img, ox + bf_x + 1, oy + 29, ShoeH)

    # FRONT THIGH: roughly horizontal block from knee to hip
    for y in range(front_knee_y - 1, front_knee_y + 1):
        for x in range(front_knee_x - 1, 14):
            c = PantsS if x == front_knee_x - 1 else Pants
            px(img, ox + x, oy + y, c)
    # FRONT SHIN: vertical from below knee to ground
    for y in range(front_knee_y + 1, 29):
        for x in range(front_foot_cx - 1, front_foot_cx + 2):
            c = PantsS if x == front_foot_cx - 1 else Pants
            px(img, ox + x, oy + y, c)
    # Front foot: flat on ground (pointing left)
    for x in range(front_foot_cx - 2, front_foot_cx + 3):
        c = ShoeH if x == front_foot_cx - 2 else Shoe
        px(img, ox + x, oy + 29, c)
    px(img, ox + front_foot_cx - 1, oy + 28, Shoe)
    px(img, ox + front_foot_cx, oy + 28, Shoe)

    # UPPER BODY: stays vertical, drops with body_drop
    draw_side_hair(img, ox, oy + body_drop)
    draw_side_head(img, ox, oy + body_drop)
    draw_side_neck(img, ox, oy + body_drop)
    draw_side_torso(img, ox, oy + body_drop)

    # Arm relaxed at side
    for dy in range(4):
        px(img, ox + 16, oy + 18 + body_drop + dy, Shirt)
        px(img, ox + 17, oy + 18 + body_drop + dy, ShirtH)
    # Hand just below torso
    px(img, ox + 15, oy + 24 + body_drop, Skin)
    px(img, ox + 14, oy + 24 + body_drop, SkinH)


# =========================================================================
# GENERATE
# =========================================================================

def main():
    sheet_w = FRAME_W * NUM_FRAMES
    sheet_h = FRAME_H * NUM_ANIMS
    sheet = Image.new("RGBA", (sheet_w, sheet_h), (0, 0, 0, 0))

    # Row 0: Idle coffee sip
    for frame in range(NUM_FRAMES):
        draw_coffee_idle_frame(sheet, frame * FRAME_W, 0, frame)

    # Row 1: Waving (call to exercise)
    for frame in range(NUM_FRAMES):
        draw_wave_frame(sheet, frame * FRAME_W, FRAME_H, frame)

    # Row 2: Pump-up "let's do it!" fist pump
    for frame in range(NUM_FRAMES):
        draw_pumpup_frame(sheet, frame * FRAME_W, FRAME_H * 2, frame)

    # Row 3: Chair dips
    for frame in range(NUM_FRAMES):
        draw_chair_dip_frame(sheet, frame * FRAME_W, FRAME_H * 3, frame)

    # Row 4: Arm circles
    for frame in range(NUM_FRAMES):
        draw_arm_circle_frame(sheet, frame * FRAME_W, FRAME_H * 4, frame)

    # Row 5: Wondering (looking around, no coffee)
    for frame in range(NUM_FRAMES):
        draw_wondering_frame(sheet, frame * FRAME_W, FRAME_H * 5, frame)

    # Row 6: Knee Raises
    for frame in range(NUM_FRAMES):
        draw_knee_raise_frame(sheet, frame * FRAME_W, FRAME_H * 6, frame)

    # Row 7: Spinal Twist
    for frame in range(NUM_FRAMES):
        draw_spinal_twist_frame(sheet, frame * FRAME_W, FRAME_H * 7, frame)

    # Row 8: Glute Squeeze
    for frame in range(NUM_FRAMES):
        draw_glute_squeeze_frame(sheet, frame * FRAME_W, FRAME_H * 8, frame)

    # Row 9: Shoulder Rolls
    for frame in range(NUM_FRAMES):
        draw_shoulder_rolls_frame(sheet, frame * FRAME_W, FRAME_H * 9, frame)

    # Row 10: Leg Extensions
    for frame in range(NUM_FRAMES):
        draw_leg_extension_frame(sheet, frame * FRAME_W, FRAME_H * 10, frame)

    # Row 11: Neck Stretch
    for frame in range(NUM_FRAMES):
        draw_neck_stretch_frame(sheet, frame * FRAME_W, FRAME_H * 11, frame)

    # Row 12: Desk Push-Ups
    for frame in range(NUM_FRAMES):
        draw_desk_pushup_frame(sheet, frame * FRAME_W, FRAME_H * 12, frame)

    # Row 13: Bodyweight Squats
    for frame in range(NUM_FRAMES):
        draw_squat_frame(sheet, frame * FRAME_W, FRAME_H * 13, frame)

    # Row 14: Calf Raises
    for frame in range(NUM_FRAMES):
        draw_calf_raise_frame(sheet, frame * FRAME_W, FRAME_H * 14, frame)

    # Row 15: Wall Sit
    for frame in range(NUM_FRAMES):
        draw_wall_sit_frame(sheet, frame * FRAME_W, FRAME_H * 15, frame)

    # Row 16: Torso Rotation
    for frame in range(NUM_FRAMES):
        draw_torso_rotation_frame(sheet, frame * FRAME_W, FRAME_H * 16, frame)

    # Row 17: Reverse Lunges
    for frame in range(NUM_FRAMES):
        draw_reverse_lunge_frame(sheet, frame * FRAME_W, FRAME_H * 17, frame)

    import os
    os.makedirs("assets/developer", exist_ok=True)

    sheet.save("assets/developer/exercise_spritesheet.png")
    print(f"Generated exercise_spritesheet.png ({sheet_w}x{sheet_h})")

    preview = sheet.resize((sheet_w * 4, sheet_h * 4), Image.NEAREST)
    preview.save("assets/developer/exercise_spritesheet_preview.png")
    print(f"Generated exercise_spritesheet_preview.png ({sheet_w*4}x{sheet_h*4})")

    # Key frame previews
    anim_names = [
        "coffee_idle", "waving", "pump_up", "chair_dips", "arm_circles", "wondering",
        "knee_raises", "spinal_twist", "glute_squeeze", "shoulder_rolls", "leg_extensions", "neck_stretch",
        "desk_pushups", "squats", "calf_raises", "wall_sit", "torso_rotation", "reverse_lunges",
    ]
    for anim in range(NUM_ANIMS):
        anim_name = anim_names[anim]
        for frame in [0, 4, 5, 6, 8, 12]:
            region = sheet.crop((
                frame * FRAME_W,
                anim * FRAME_H,
                (frame + 1) * FRAME_W,
                (anim + 1) * FRAME_H,
            ))
            scaled = region.resize((FRAME_W * 8, FRAME_H * 8), Image.NEAREST)
            scaled.save(f"assets/developer/{anim_name}_f{frame:02d}_preview.png")
    print("Generated key frame previews (8x scale)")


if __name__ == "__main__":
    main()
