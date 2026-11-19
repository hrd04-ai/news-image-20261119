#!/usr/bin/env python3
"""Draw the news-image-20261119 entry: a newspaper front page summing up
Thursday 19 November 2026 in six stories plus a briefs strip.
Output: entry.png (1024x1024, under 1 MiB).

Six stories, each verified from news reports of 19 November 2026:
  1. Trump, Xi and Putin hold their first three-way summit in Shenzhen
     (APEC sidelines) - reported by 13 outlets incl. CBS, BBC, Japan Times.
  2. Ukraine strikes the Crimean (Kerch) Bridge a third time this week;
     the Russian-appointed head of Crimea halted traffic, damage assessed.
  3. US-Iran fire exchange widens across the Gulf: Iran hits Gulf targets
     after US strikes on Qeshm Island; a US base in Kuwait and Bahrain hit.
  4. Hakeem Jeffries poised to become the first Black Speaker of the US
     House (Democrats nominate him; NDTV + 6 outlets).
  5. Pew Research: Islam set to pass Christianity as the world's largest
     religion by 2035.
  6. NASA's Voyager 1 becomes the first human-made object to travel one
     light-day from Earth.
Briefs strip: Anthropic's record stock-market debut; Australia, Canada,
Italy and the UK urge Israel to let aid reach flooded Gaza; Nvidia halts
H-series chip shipments to mainland China.
"""
import os

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (247, 243, 232)
INK = (20, 20, 20)
RED = (176, 58, 46)
PANEL = (255, 253, 246)
GREY = (96, 90, 78)
BLUE = (31, 78, 121)
TEAL = (18, 110, 105)
ORANGE = (232, 126, 32)
GOLD = (214, 164, 32)
NAVY = (24, 42, 84)
PURPLE = (94, 60, 140)

BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
REG = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SERIFB = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"


def fnt(path, size):
    return ImageFont.truetype(path, size)


def wrap(d, text, font, max_w):
    """Greedy word wrap returning lines that fit max_w."""
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if d.textlength(trial, font=font) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def centred(d, cx, y, lines, font, fill, lead=4):
    for line in lines:
        w = d.textlength(line, font=font)
        d.text((cx - w / 2, y), line, font=font, fill=fill)
        y += font.size + lead
    return y


# ---------------- pictograms (drawn in a 488x96 band) ----------------
def pic_summit(d, x, y, w, h):
    """Three leaders at a table, three flags behind."""
    d.rectangle([x, y, x + w, y + h], fill=NAVY)
    for i, c in enumerate((RED, GOLD, BLUE)):
        fx = x + 60 + i * 130
        d.rectangle([fx, y + 14, fx + 54, y + 40], fill=c)
        d.rectangle([fx + 25, y + 14, fx + 29, y + 62], fill=(240, 240, 240))
    # table
    d.rectangle([x + 30, y + 70, x + w - 30, y + 80], fill=(120, 84, 50))
    d.rectangle([x + 44, y + 80, x + 54, y + h - 4], fill=(96, 66, 38))
    d.rectangle([x + w - 54, y + 80, x + w - 44, y + h - 4], fill=(96, 66, 38))
    # three heads above the table
    for i, c in enumerate(((232, 190, 150), (210, 170, 130), (232, 190, 150))):
        cx = x + 110 + i * 134
        d.ellipse([cx - 18, y + 28, cx + 18, y + 64], fill=c)
        d.pieslice([cx - 18, y + 28, cx + 18, y + 52], 180, 360, fill=(60, 60, 60))


def pic_bridge(d, x, y, w, h):
    """Arched bridge over water, explosion burst on the span."""
    d.rectangle([x, y, x + w, y + h], fill=(198, 222, 235))
    d.rectangle([x, y + 62, x + w, y + h], fill=(52, 110, 150))
    for i in range(5):
        d.arc([x + 10 + i * 96, y + 66, x + 90 + i * 96, y + 92], 180, 360,
              fill=(240, 248, 252), width=3)
    d.rectangle([x + 20, y + 44, x + w - 20, y + 58], fill=(90, 90, 96))
    for i in range(6):
        d.rectangle([x + 40 + i * 72, y + 58, x + 48 + i * 72, y + 66],
                    fill=(70, 70, 76))
    bx, by = x + w // 2, y + 30
    for ang, ln in ((0, 26), (45, 20), (90, 28), (135, 20), (180, 26),
                    (225, 20), (270, 28), (315, 20)):
        import math
        ex = bx + int(ln * math.cos(math.radians(ang)))
        ey = by + int(ln * math.sin(math.radians(ang)))
        d.line([bx, by, ex, ey], fill=ORANGE, width=5)
    d.ellipse([bx - 12, by - 12, bx + 12, by + 12], fill=(255, 214, 64))
    d.ellipse([bx - 6, by - 6, bx + 6, by + 6], fill=RED)


def pic_gulf(d, x, y, w, h):
    """Missile arc over a radar dish and sea."""
    d.rectangle([x, y, x + w, y + h], fill=(24, 42, 84))
    for i in range(40):
        import random
        random.seed(100 + i)
        sx = x + random.randint(4, w - 4)
        sy = y + random.randint(4, 40)
        d.point((sx, sy), fill=(220, 220, 240))
    # sea
    d.rectangle([x, y + 68, x + w, y + h], fill=(28, 88, 120))
    # radar dish
    d.pieslice([x + 60, y + 34, x + 130, y + 92], 270, 90, fill=(200, 205, 210))
    d.line([x + 95, y + 66, x + 95, y + 90], fill=(200, 205, 210), width=5)
    # missile arc
    d.arc([x + 180, y + 6, x + 460, y + 80], 200, 340, fill=ORANGE, width=6)
    d.ellipse([x + 430, y + 12, x + 448, y + 30], fill=(255, 214, 64))
    d.ellipse([x + 436, y + 18, x + 442, y + 24], fill=RED)


def pic_speaker(d, x, y, w, h):
    """Capitol dome with a gavel."""
    d.rectangle([x, y, x + w, y + h], fill=(232, 226, 210))
    # dome
    d.pieslice([x + w // 2 - 90, y + 6, x + w // 2 + 90, y + 96], 180, 360,
               fill=(120, 130, 140))
    d.rectangle([x + w // 2 - 96, y + 52, x + w // 2 + 96, y + 62],
                fill=(100, 110, 120))
    d.rectangle([x + w // 2 - 6, y - 2, x + w // 2 + 6, y + 12], fill=GOLD)
    # columns
    for i in range(5):
        cx = x + w // 2 - 80 + i * 40
        d.rectangle([cx - 7, y + 62, cx + 7, y + 88], fill=(240, 238, 228))
    d.rectangle([x + w // 2 - 96, y + 88, x + w // 2 + 96, y + h - 2],
                fill=(100, 110, 120))
    # gavel, bottom right
    d.rectangle([x + w - 118, y + 62, x + w - 58, y + 76], fill=(96, 66, 38))
    d.line([x + w - 88, y + 76, x + w - 58, y + 92], fill=(120, 84, 50),
           width=5)


def pic_faith(d, x, y, w, h):
    """Two rising bars, the second overtaking the first by 2035."""
    d.rectangle([x, y, x + w, y + h], fill=(244, 238, 226))
    d.line([x + 40, y + h - 18, x + w - 30, y + h - 18], fill=GREY, width=2)
    d.line([x + 40, y + 10, x + 40, y + h - 18], fill=GREY, width=2)
    # bar 1 (Christianity) tall but flat-topped
    d.rectangle([x + 90, y + 26, x + 190, y + h - 18], fill=BLUE)
    # bar 2 (Islam) overtakes
    d.rectangle([x + 230, y + 12, x + 330, y + h - 18], fill=TEAL)
    d.text((x + 96, y + h - 44), "NOW", font=fnt(BOLD, 15), fill=(255, 255, 255))
    d.text((x + 236, y + h - 44), "2035", font=fnt(BOLD, 15),
           fill=(255, 255, 255))
    d.text((x + 346, y + 8), "ISLAM", font=fnt(BOLD, 17), fill=TEAL)
    d.text((x + 346, y + 30), "PASSES", font=fnt(BOLD, 17), fill=TEAL)
    d.text((x + 346, y + 52), "No. 1", font=fnt(BOLD, 17), fill=TEAL)


def pic_voyager(d, x, y, w, h):
    """Spacecraft with dish, a long dashed arc marking one light-day."""
    d.rectangle([x, y, x + w, y + h], fill=(12, 16, 34))
    for i in range(46):
        import random
        random.seed(200 + i)
        sx = x + random.randint(4, w - 4)
        sy = y + random.randint(4, h - 4)
        d.point((sx, sy), fill=(220, 220, 240))
    # dashed curve from the spacecraft up to a bright star (all in-bounds)
    import math
    x0, y0 = x + 185, y + 56
    x1, y1 = x + w - 88, y + 22
    for i in range(13):
        t = i / 12.0
        px = int(x0 + (x1 - x0) * t)
        py = int(y0 + (y1 - y0) * t - 26 * math.sin(math.pi * t))
        d.ellipse([px - 3, py - 3, px + 3, py + 3], fill=GOLD)
    d.ellipse([x + w - 96, y + 8, x + w - 72, y + 32], fill=(255, 240, 180))
    # spacecraft body + dish
    d.rectangle([x + 40, y + 44, x + 130, y + 66], fill=(200, 205, 210))
    d.pieslice([x + 120, y + 30, x + 180, y + 80], 270, 90, fill=(230, 232, 235))
    d.line([x + 40, y + 55, x + 16, y + 55], fill=(160, 165, 170), width=4)
    d.text((x + 200, y + 72), "1 LIGHT-DAY", font=fnt(BOLD, 18),
           fill=(255, 255, 255))


STORIES = [
    ("SUMMIT OF THREE", pic_summit, NAVY,
     "Trump, Xi & Putin meet in Shenzhen",
     "First three-way summit of the US, China and Russia leaders \u00b7 APEC sidelines"),
    ("BRIDGE HIT AGAIN", pic_bridge, BLUE,
     "Ukraine strikes Crimean Bridge a 3rd time this week",
     "Traffic halted as damage is assessed \u00b7 Kerch Strait"),
    ("GULF IN FLAMES", pic_gulf, RED,
     "US\u2013Iran fire exchange widens across the Gulf",
     "Iran hits Gulf targets after the US strike on Qeshm Island"),
    ("A FIRST FOR THE HOUSE", pic_speaker, PURPLE,
     "Jeffries poised to be first Black Speaker",
     "Democrats nominate Hakeem Jeffries \u00b7 Washington"),
    ("FAITH IN 2035", pic_faith, TEAL,
     "Islam set to pass Christianity as No. 1 faith",
     "Pew Research projection \u00b7 world demographics"),
    ("ONE LIGHT-DAY OUT", pic_voyager, NAVY,
     "Voyager 1 reaches one light-day from Earth",
     "First human-made object to travel so far \u00b7 NASA"),
]

BRIEFS = [
    "Anthropic's stock-market debut raises a record sum",
    "Australia, Canada, Italy & UK: let aid reach flooded Gaza",
    "Nvidia halts H-series chip shipments to China",
]


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # ---- masthead ----
    d.rectangle([0, 0, W, 118], fill=INK)
    d.text((512, 14), "THE WORLD IN ONE DAY", font=fnt(SERIFB, 54),
           fill=(247, 243, 232), anchor="ma")
    d.text((512, 76), "THURSDAY 19 NOVEMBER 2026",
           font=fnt(BOLD, 26), fill=GOLD, anchor="ma")
    d.line([16, 126, W - 16, 126], fill=RED, width=4)

    # ---- panels: 2 cols x 3 rows ----
    mx, my = 16, 140
    pw, ph = 488, 246
    gx, gy = 16, 12
    hf = fnt(BOLD, 25)
    sf = fnt(REG, 17)
    kf = fnt(BOLD, 15)
    for i, (kicker, pic, accent, head, sub) in enumerate(STORIES):
        col, row = i % 2, i // 2
        x = mx + col * (pw + gx)
        y = my + row * (ph + gy)
        d.rectangle([x, y, x + pw, y + ph], fill=PANEL, outline=(200, 192, 172))
        d.rectangle([x, y, x + pw, y + 26], fill=accent)
        d.text((x + 10, y + 4), kicker, font=kf, fill=(255, 255, 255))
        pic(d, x + 8, y + 34, pw - 16, 92)
        hy = y + 136
        lines = wrap(d, head, hf, pw - 24)
        for line in lines[:2]:
            d.text((x + 12, hy), line, font=hf, fill=INK)
            hy += 30
        sub_lines = wrap(d, sub, sf, pw - 24)
        for line in sub_lines[:2]:
            d.text((x + 12, hy + 2), line, font=sf, fill=GREY)
            hy += 22

    # ---- briefs strip ----
    fy = my + 3 * ph + 2 * gy + 4
    d.rectangle([mx, fy, W - mx, fy + 78], fill=(238, 232, 214),
                outline=(200, 192, 172))
    d.text((mx + 10, fy + 8), "ALSO IN BRIEF", font=fnt(BOLD, 16), fill=RED)
    bf = fnt(REG, 16)
    by = fy + 30
    for b in BRIEFS:
        d.text((mx + 10, by), "\u2022  " + b, font=bf, fill=INK)
        by += 20
    d.text((512, H - 22), "Six stories, one day \u2014 drawn from the news of 19 November 2026",
           font=fnt(REG, 14), fill=GREY, anchor="ma")

    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
    img.save(out, "PNG", optimize=True)
    print("wrote", out, os.path.getsize(out), "bytes")


if __name__ == "__main__":
    main()
