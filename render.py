# render.py — draws entry.png for the make.fun bounty news-image-20261119.
#
# A flat vector newspaper front page for Thursday 19 November 2026, drawn
# from scratch with Pillow (standard library + Pillow locally; the entry
# itself, main.py, only copies the finished PNG). Rendered at 2x and
# downscaled for clean edges. No network, no photos, no external assets:
# every shape, flag and letter is computed here, so no text can come out
# garbled and two runs of main.py write identical bytes.
#
# Stories (researched 19 Nov 2026 ~00:30 UTC, checked against Reuters, AP
# via northjersey/Polygon, NASA/JPL, the European Commission and IMD):
#   1. Shenzhen — Trump, Xi and Putin hold their first trilateral summit.
#   2. GTA VI launches worldwide in a rolling midnight rollout.
#   3. NASA marks Voyager 1 reaching one light-day from Earth.
#   4. Cyclone Akvan strengthens; India moves 200,000 people in Odisha.
#   5. The EU's EUR 45bn Ukraine loan goes to the Coalition of the
#      Willing in Berlin.  Footer: Alaska, Canada, the Bulgaria tanker.

import math
import os

from PIL import Image, ImageDraw, ImageFont

S = 2                      # render scale; final image is 1024 x 1024
W, H = 1024 * S, 1024 * S

NAVY = (20, 33, 61)
NAVY2 = (28, 48, 88)
PAPER = (247, 243, 234)
CARD = (255, 255, 255)
INK = (26, 26, 26)
MUTED = (90, 90, 90)
RED = (180, 35, 24)
GOLD = (201, 162, 39)
GOLD_LT = (232, 197, 90)
SKY = (178, 214, 235)
SEA = (64, 128, 168)
SAND = (233, 205, 150)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"


def font(name, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, name), int(size * S))


F_SERIF = lambda sz: font("DejaVuSerif-Bold.ttf", sz)
F_BOLD = lambda sz: font("DejaVuSans-Bold.ttf", sz)
F_REG = lambda sz: font("DejaVuSans.ttf", sz)

img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img)


def box(x0, y0, x1, y1, fill, outline=None, width=1):
    d.rectangle([x0 * S, y0 * S, x1 * S, y1 * S], fill=fill,
                outline=outline, width=int(width * S))


def text(x, y, s, f, fill, anchor="la"):
    d.text((x * S, y * S), s, font=f, fill=fill, anchor=anchor)


def text_w(s, f):
    return d.textlength(s, font=f) / S


def spaced(x, y, s, f, fill, gap=2):
    """Draw text with extra tracking between letters (small-cap kickers)."""
    cx = x
    for ch in s:
        d.text((cx * S, y * S), ch, font=f, fill=fill)
        cx += text_w(ch, f) + gap
    return cx


def wrap(s, f, max_w):
    """Greedy word wrap; returns a list of lines fitting max_w (1024 units)."""
    lines, cur = [], ""
    for word in s.split(" "):
        trial = (cur + " " + word).strip()
        if text_w(trial, f) <= max_w or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def para(x, y, lines, f, fill, lh):
    for i, line in enumerate(lines):
        text(x, y + i * lh, line, f, fill)
    return y + len(lines) * lh


def fit_one_line(s, f, max_w):
    """Shrink a bold headline until it fits one line; returns (size, font)."""
    size = 26
    while size > 16:
        ff = F_BOLD(size)
        if text_w(s, ff) <= max_w:
            return size, ff
        size -= 1
    return size, F_BOLD(size)


def star_points(cx, cy, r_out, r_in, rot=-90.0):
    pts = []
    for i in range(10):
        r = r_out if i % 2 == 0 else r_in
        a = math.radians(rot + i * 36)
        pts.append(((cx + r * math.cos(a)) * S, (cy + r * math.sin(a)) * S))
    return pts


def vgrad(x0, y0, x1, y1, top, bottom):
    """Vertical gradient, drawn as horizontal bands."""
    h = int((y1 - y0) * S)
    for i in range(h):
        t = i / max(h - 1, 1)
        c = tuple(int(top[k] + (bottom[k] - top[k]) * t) for k in range(3))
        d.line([(x0 * S, (y0 * S) + i), (x1 * S, (y0 * S) + i)], fill=c)


def flag_us(x, y, w, h):
    box(x, y, x + w, y + h, (255, 255, 255))
    for i in range(13):
        if i % 2 == 0:
            box(x, y + i * h / 13, x + w, y + (i + 1) * h / 13, (178, 34, 52))
    cw, ch = w * 0.4, h * 7 / 13
    box(x, y, x + cw, y + ch, (60, 59, 110))
    for r in range(5):
        for c in range(6):
            px = x + cw * (c + 0.5) / 6
            py = y + ch * (r + 0.5) / 5
            d.ellipse([(px - 1.1) * S, (py - 1.1) * S,
                       (px + 1.1) * S, (py + 1.1) * S], fill=(255, 255, 255))


def flag_cn(x, y, w, h):
    box(x, y, x + w, y + h, (222, 41, 16))
    cx, cy = x + w * 0.22, y + h * 0.28
    d.polygon(star_points(cx, cy, h * 0.16, h * 0.065), fill=(255, 222, 0))
    for sx, sy in [(0.52, 0.14), (0.66, 0.26), (0.66, 0.48), (0.52, 0.60)]:
        d.polygon(star_points(x + w * sx, y + h * sy, h * 0.055, h * 0.022),
                  fill=(255, 222, 0))


def flag_ru(x, y, w, h):
    box(x, y, x + w, y + h / 3, (255, 255, 255))
    box(x, y + h / 3, x + w, y + 2 * h / 3, (0, 57, 166))
    box(x, y + 2 * h / 3, x + w, y + h, (213, 0, 50))


def flag_on_pole(x, y, w, h, draw_flag):
    d.line([(x + w / 2) * S, y * S, (x + w / 2) * S, (y + h + 26) * S],
           fill=(60, 60, 60), width=int(2 * S))
    d.ellipse([(x + w / 2 - 2.5) * S, (y - 2.5) * S,
               (x + w / 2 + 2.5) * S, (y + 2.5) * S], fill=GOLD)
    draw_flag(x, y, w, h)


# ---------------------------------------------------------------- masthead
box(0, 0, 1024, 112, NAVY)
kicker = "THURSDAY  •  THE WORLD'S NEWS IN ONE IMAGE"
kw = sum(text_w(ch, F_BOLD(19)) + 2 for ch in kicker) - 2
spaced((1024 - kw) / 2, 16, kicker, F_BOLD(19), GOLD_LT, gap=2)
date = "19 NOVEMBER 2026"
text(512, 40, date, F_SERIF(58), (255, 255, 255), anchor="ma")
box(0, 112, 1024, 116, GOLD)

# ---------------------------------------------------------------- lead: Shenzhen
LX0, LY0, LX1, LY1 = 16, 124, 1008, 452
box(LX0, LY0, LX1, LY1, CARD, outline=NAVY, width=2)
AX0, AY0, AX1, AY1 = LX0, LY0, 470, LY1          # art on the left
vgrad(AX0, AY0, AX1, AY1, (214, 232, 244), SKY)
d.ellipse([(AX1 - 118) * S, (AY0 + 26) * S, (AX1 - 48) * S, (AY0 + 96) * S],
          fill=(250, 224, 140))
# Shenzhen skyline silhouettes
skyline = [(0, 210, 46, 130), (52, 240, 40, 170), (98, 190, 52, 120),
           (156, 250, 38, 200), (200, 170, 46, 90), (252, 230, 40, 150),
           (298, 200, 48, 110), (352, 250, 44, 190), (402, 220, 52, 140)]
for bx, by, bw, bh in skyline:
    box(AX0 + bx, AY1 - bh, AX0 + bx + bw, AY1 - 58, NAVY2)
box(AX0, AY1 - 58, AX1, AY1, NAVY)               # stage band
# three flags on the stage
flag_on_pole(AX0 + 52, AY1 - 128, 62, 42, flag_us)
flag_on_pole(AX0 + 196, AY1 - 128, 62, 42, flag_cn)
flag_on_pole(AX0 + 340, AY1 - 128, 62, 42, flag_ru)
text(AX0 + 227, AY1 - 46, "SHENZHEN", F_BOLD(15), (255, 255, 255), anchor="ma")

TX = 492
text(TX, LY0 + 18, "SHENZHEN  •  DIPLOMACY", F_BOLD(19), RED)
head = wrap("TRUMP, XI AND PUTIN MEET IN SHENZHEN", F_BOLD(40), 1008 - TX - 18)
y = para(TX, LY0 + 48, head, F_BOLD(40), NAVY, 47)
deck = wrap("The first trilateral summit of the three leaders — nuclear "
            "arms and the Iran war on the agenda at the APEC meeting in "
            "China.", F_REG(20), 1008 - TX - 18)
y = para(TX, y + 10, deck, F_REG(20), INK, 27)
text(TX, y + 12, "2:30 p.m. local time  •  Kylin Villa", F_BOLD(17), MUTED)

# ---------------------------------------------------------------- row 2
RY0, RY1 = 468, 676
panels2 = [(16, 496), (512, 992)]
for i, (px0, px1) in enumerate(panels2):
    box(px0, RY0, px1, RY1, CARD, outline=NAVY, width=2)

# GTA VI panel (left)
px0, px1 = panels2[0]
vgrad(px0, RY0, px1, RY0 + 92, (255, 122, 89), (198, 52, 140))
d.ellipse([(px0 + 384) * S, (RY0 + 10) * S, (px0 + 444) * S, (RY0 + 70) * S],
          fill=(255, 214, 130))
# palm silhouettes: curved trunk, smooth drooping fronds (bezier)
def bezier(p0, p1, p2, n=12):
    pts = []
    for i in range(n + 1):
        t = i / n
        x = (1 - t) ** 2 * p0[0] + 2 * (1 - t) * t * p1[0] + t * t * p2[0]
        y = (1 - t) ** 2 * p0[1] + 2 * (1 - t) * t * p1[1] + t * t * p2[1]
        pts.append((x * S, y * S))
    return pts

for px in (px0 + 36, px0 + 424):
    crown_x, crown_y = px + 6, RY0 + 92 - 56
    d.line([(px) * S, (RY0 + 92) * S, crown_x * S, crown_y * S],
           fill=(40, 20, 40), width=int(4 * S))
    for dxf, dyf in [(-34, -14), (-24, -28), (-6, -34), (14, -28), (30, -12)]:
        d.line(bezier((crown_x, crown_y),
                      (crown_x + dxf * 0.6, crown_y + dyf * 0.4 - 8),
                      (crown_x + dxf, crown_y + dyf + 10)),
               fill=(40, 20, 40), width=int(3 * S))
box(px0, RY0 + 78, px1, RY0 + 92, (30, 16, 34))
text(px0 + 150, RY0 + 18, "VI", F_SERIF(56), (255, 255, 255), anchor="ma")
ty = RY0 + 104
text(px0 + 14, ty, "CULTURE  •  VIDEO GAMES", F_BOLD(16), RED)
size, hf = fit_one_line("GTA VI IS OUT — VICE CITY OPENS", F_BOLD(26),
                        px1 - px0 - 28)
text(px0 + 14, ty + 24, "GTA VI IS OUT — VICE CITY OPENS", hf, NAVY)
deck = wrap("A rolling midnight launch from New Zealand — 13 years after "
            "GTA V, with about 16 million pre-orders.", F_REG(17),
            px1 - px0 - 28)
para(px0 + 14, ty + 24 + 32, deck, F_REG(17), INK, 21)

# Voyager panel (right)
px0, px1 = panels2[1]
box(px0, RY0, px1, RY0 + 92, (10, 16, 38))
stars = [(24, 18), (70, 44), (120, 14), (180, 52), (240, 22), (300, 40),
         (360, 16), (410, 58), (450, 26), (150, 70), (330, 72), (60, 70)]
for sx, sy in stars:
    r = 1.6 if (sx + sy) % 3 else 2.4
    d.ellipse([(px0 + sx - r) * S, (RY0 + sy - r) * S,
               (px0 + sx + r) * S, (RY0 + sy + r) * S], fill=(255, 255, 255))
# gold dish (bowl) + signal arcs, text clear of the arcs
dx, dy = px0 + 110, RY0 + 44
d.pieslice([(dx - 52) * S, (dy - 34) * S, (dx + 52) * S, (dy + 34) * S],
           0, 180, fill=(212, 175, 55))
d.line([(dx - 52) * S, dy * S, (dx + 52) * S, dy * S],
       fill=(212, 175, 55), width=int(3 * S))
d.line([(dx) * S, (dy + 32) * S, (dx) * S, (RY0 + 92) * S],
       fill=(212, 175, 55), width=int(3 * S))
# feed horn above the bowl, held by two thin supports from the rim
d.ellipse([(dx - 4) * S, (dy - 30) * S, (dx + 4) * S, (dy - 22) * S],
          fill=(212, 175, 55))
d.line([(dx - 48) * S, (dy - 2) * S, (dx - 3) * S, (dy - 24) * S],
       fill=(212, 175, 55), width=int(2 * S))
d.line([(dx + 48) * S, (dy - 2) * S, (dx + 3) * S, (dy - 24) * S],
       fill=(212, 175, 55), width=int(2 * S))
for r in (52, 70):
    d.arc([(dx - r) * S, (dy - 26 - r) * S, (dx + r) * S, (dy - 26 + r) * S],
          -62, 62, fill=GOLD_LT, width=int(2 * S))
text(px0 + 330, RY0 + 34, "1 LIGHT-DAY", F_BOLD(20), GOLD_LT, anchor="ma")
ty = RY0 + 104
text(px0 + 14, ty, "SPACE  •  NASA", F_BOLD(16), RED)
size, hf = fit_one_line("VOYAGER 1, ONE LIGHT-DAY AWAY", F_BOLD(26),
                        px1 - px0 - 28)
text(px0 + 14, ty + 24, "VOYAGER 1, ONE LIGHT-DAY AWAY", hf, NAVY)
deck = wrap("NASA marks the 1977 probe's milestone: 16 billion miles out, "
            "a radio signal now takes a day to reach it.", F_REG(17),
            px1 - px0 - 28)
para(px0 + 14, ty + 24 + 32, deck, F_REG(17), INK, 21)

# ---------------------------------------------------------------- row 3
TY0, TY1 = 692, 892
panels3 = [(16, 336), (352, 672), (688, 1008)]
for px0, px1 in panels3:
    box(px0, TY0, px1, TY1, CARD, outline=NAVY, width=2)

# Cyclone Akvan
px0, px1 = panels3[0]
box(px0, TY0, px1, TY0 + 72, (186, 224, 238))
d.polygon([(px0) * S, TY0 * S, (px0 + 66) * S, TY0 * S,
           (px0 + 82) * S, (TY0 + 36) * S, (px0 + 66) * S, (TY0 + 72) * S,
           (px0) * S, (TY0 + 72) * S], fill=(96, 168, 96))
cx, cy = px0 + 200, TY0 + 36
for r in (10, 20, 30, 40):
    d.arc([(cx - r) * S, (cy - r) * S, (cx + r) * S, (cy + r) * S],
          r * 9, 200 + r * 9, fill=(255, 255, 255), width=int(3 * S))
d.ellipse([(cx - 6) * S, (cy - 6) * S, (cx + 6) * S, (cy + 6) * S],
          fill=NAVY)
text(px0 + 14, TY0 + 82, "WEATHER  •  BAY OF BENGAL", F_BOLD(14), RED)
head = wrap("CYCLONE AKVAN BEARS DOWN ON INDIA", F_BOLD(22), px1 - px0 - 28)
y = para(px0 + 14, TY0 + 104, head, F_BOLD(22), NAVY, 26)
deck = wrap("Very severe now; 200,000 to move in Odisha; landfall Friday, "
            "winds 145 km/h.", F_REG(14), px1 - px0 - 28)
para(px0 + 14, y + 4, deck, F_REG(14), INK, 19)

# EU Ukraine loan
px0, px1 = panels3[1]
box(px0, TY0, px1, TY0 + 72, (0, 51, 153))
cx, cy = px0 + 62, TY0 + 36
for k in range(12):
    a = math.radians(k * 30 - 90)
    sx, sy = cx + 26 * math.cos(a), cy + 26 * math.sin(a)
    d.polygon(star_points(sx, sy, 4.5, 1.8), fill=(255, 204, 0))
text(px0 + 112, TY0 + 22, "€45bn", F_BOLD(26), (255, 255, 255))
text(px0 + 14, TY0 + 82, "EUROPE  •  UKRAINE", F_BOLD(14), RED)
head = wrap("EU'S €45BN UKRAINE LOAN GOES TO BERLIN", F_BOLD(22),
            px1 - px0 - 28)
y = para(px0 + 14, TY0 + 104, head, F_BOLD(22), NAVY, 26)
deck = wrap("The Coalition of the Willing meets today on the loan: €20bn "
            "budgets, €25bn arms.", F_REG(14), px1 - px0 - 28)
para(px0 + 14, y + 4, deck, F_REG(14), INK, 19)

# Saudi Arabia / Gulf
px0, px1 = panels3[2]
vgrad(px0, TY0, px1, TY0 + 72, (250, 226, 170), (233, 196, 130))
d.ellipse([(px0 + 240) * S, (TY0 + 8) * S, (px0 + 284) * S, (TY0 + 52) * S],
          fill=(255, 240, 180))
# two dune ridges, clipped to the art band by construction
d.polygon([(px0) * S, (TY0 + 72) * S, (px0) * S, (TY0 + 52) * S,
           (px0 + 60) * S, (TY0 + 40) * S, (px0 + 130) * S, (TY0 + 46) * S,
           (px0 + 200) * S, (TY0 + 60) * S, (px0 + 220) * S, (TY0 + 72) * S],
          fill=(206, 158, 92))
d.polygon([(px0 + 120) * S, (TY0 + 72) * S, (px0 + 130) * S, (TY0 + 56) * S,
           (px0 + 200) * S, (TY0 + 48) * S, (px0 + 270) * S, (TY0 + 56) * S,
           (px1) * S, (TY0 + 66) * S, (px1) * S, (TY0 + 72) * S],
          fill=(188, 140, 78))
text(px0 + 14, TY0 + 82, "THE GULF  •  SAUDI ARABIA", F_BOLD(14), RED)
head = wrap("SAUDI ARABIA: DANGER HAS PASSED", F_BOLD(22), px1 - px0 - 28)
y = para(px0 + 14, TY0 + 104, head, F_BOLD(22), NAVY, 26)
deck = wrap("Riyadh lifts alerts in three southern cities as the Gulf stays "
            "on guard.", F_REG(14), px1 - px0 - 28)
para(px0 + 14, y + 4, deck, F_REG(14), INK, 19)

# ---------------------------------------------------------------- footer
box(0, 908, 1024, 1008, NAVY)
text(16, 924, "ALSO TODAY:", F_BOLD(16), GOLD_LT)
f1 = ("Peltola nears a Senate win in Alaska   •   Canada's Carney "
      "recalibrates China ties")
f2 = ("LPG tanker that sank off Bulgaria was hit by projectiles, "
      "officials say")
text(16, 948, f1, F_REG(16), (255, 255, 255))
text(16, 972, f2, F_REG(16), (255, 255, 255))

out = img.resize((1024, 1024), Image.LANCZOS)
out.save("entry.png", optimize=True)
print("wrote entry.png", out.size)
