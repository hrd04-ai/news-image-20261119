#!/usr/bin/env python3
"""Render the news-image-20261119 front page: Thursday 19 November 2026,
six stories plus a briefs strip. Writes entry.png (1024x1024, < 1 MiB).

Stories, each confirmed in news reports dated 19 November 2026:
  1. Trump, Xi and Putin meet three-way for the first time, in Shenzhen
     on the APEC sidelines (13 outlets incl. CBS, BBC, Japan Times).
  2. Ukraine hits the Crimean (Kerch) Bridge a third time in one week;
     Crimea's Russian-appointed head halted traffic, damage assessed.
  3. The US-Iran exchange of fire spreads across the Gulf: Iran strikes
     Gulf targets after the US hit Qeshm Island; a US base in Kuwait
     and Bahrain were hit too.
  4. Hakeem Jeffries is lined up to be the first Black Speaker of the
     US House (Democrats nominate him; NDTV + 6 outlets).
  5. Pew Research projects Islam passing Christianity as the world's
     largest religion by 2035.
  6. NASA's Voyager 1 becomes the first human-made object to travel
     one light-day from Earth.
Briefs: Anthropic's record stock-market debut; Australia, Canada, Italy
and the UK pressing Israel to let aid into flooded Gaza; Nvidia stopping
H-series chip shipments to mainland China.
"""
import math
import os
import random

from PIL import Image, ImageDraw, ImageFont

CANVAS_W, CANVAS_H = 1024, 1024
PAGE_BG = (247, 243, 232)
TEXT = (20, 20, 20)
ACCENT = (176, 58, 46)
CARD = (255, 253, 246)
MUTED = (96, 90, 78)
OCEAN = (31, 78, 121)
JADE = (18, 110, 105)
TANGERINE = (232, 126, 32)
BRASS = (214, 164, 32)
MIDNIGHT = (24, 42, 84)
PLUM = (94, 60, 140)

FONT_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FONT_REG = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
FONT_SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"


def load_font(path, size):
    return ImageFont.truetype(path, size)


def wrap_text(pen, text, font, max_width):
    """Split text into lines no wider than max_width (pixels)."""
    words = text.split()
    lines = []
    current = ""
    for word in words:
        candidate = (current + " " + word).strip()
        if pen.textlength(candidate, font=font) <= max_width:
            current = candidate
            continue
        if current:
            lines.append(current)
        current = word
    if current:
        lines.append(current)
    return lines


def draw_centered(pen, cx, top, lines, font, fill):
    """Draw lines centred on cx, starting at top; return the next y."""
    y = top
    for line in lines:
        pen.text((cx, y), line, font=font, fill=fill, anchor="ma")
        y += font.size + 4
    return y


# ---------------- pictograms: each draws inside a (w x h) band ----------------
def draw_summit(pen, x0, y0, w, h):
    """Three leaders at a table with three flags behind them."""
    pen.rectangle([x0, y0, x0 + w, y0 + h], fill=MIDNIGHT)
    for i, colour in enumerate((ACCENT, BRASS, OCEAN)):
        fx = x0 + 60 + i * 130
        pen.rectangle([fx, y0 + 14, fx + 54, y0 + 40], fill=colour)
        pen.rectangle([fx + 25, y0 + 14, fx + 29, y0 + 62], fill=(240, 240, 240))
    pen.rectangle([x0 + 30, y0 + 70, x0 + w - 30, y0 + 80], fill=(120, 84, 50))
    pen.rectangle([x0 + 44, y0 + 80, x0 + 54, y0 + h - 4], fill=(96, 66, 38))
    pen.rectangle([x0 + w - 54, y0 + 80, x0 + w - 44, y0 + h - 4], fill=(96, 66, 38))
    for i, skin in enumerate(((232, 190, 150), (210, 170, 130), (232, 190, 150))):
        cx = x0 + 110 + i * 134
        pen.ellipse([cx - 18, y0 + 28, cx + 18, y0 + 64], fill=skin)
        pen.pieslice([cx - 18, y0 + 28, cx + 18, y0 + 52], 180, 360, fill=(60, 60, 60))


def draw_bridge(pen, x0, y0, w, h):
    """Arched bridge over water with a blast on the span."""
    pen.rectangle([x0, y0, x0 + w, y0 + h], fill=(198, 222, 235))
    pen.rectangle([x0, y0 + 62, x0 + w, y0 + h], fill=(52, 110, 150))
    for i in range(5):
        pen.arc([x0 + 10 + i * 96, y0 + 66, x0 + 90 + i * 96, y0 + 92], 180, 360,
                fill=(240, 248, 252), width=3)
    pen.rectangle([x0 + 20, y0 + 44, x0 + w - 20, y0 + 58], fill=(90, 90, 96))
    for i in range(6):
        pen.rectangle([x0 + 40 + i * 72, y0 + 58, x0 + 48 + i * 72, y0 + 66],
                      fill=(70, 70, 76))
    bx, by = x0 + w // 2, y0 + 30
    for angle, length in ((0, 26), (45, 20), (90, 28), (135, 20), (180, 26),
                         (225, 20), (270, 28), (315, 20)):
        ex = bx + int(length * math.cos(math.radians(angle)))
        ey = by + int(length * math.sin(math.radians(angle)))
        pen.line([bx, by, ex, ey], fill=TANGERINE, width=5)
    pen.ellipse([bx - 12, by - 12, bx + 12, by + 12], fill=(255, 214, 64))
    pen.ellipse([bx - 6, by - 6, bx + 6, by + 6], fill=ACCENT)


def draw_gulf(pen, x0, y0, w, h):
    """Night sky, radar dish, sea, and a missile arc with a burst."""
    pen.rectangle([x0, y0, x0 + w, y0 + h], fill=MIDNIGHT)
    for i in range(40):
        random.seed(100 + i)
        pen.point((x0 + random.randint(4, w - 4), y0 + random.randint(4, 40)),
                  fill=(220, 220, 240))
    pen.rectangle([x0, y0 + 68, x0 + w, y0 + h], fill=(28, 88, 120))
    pen.pieslice([x0 + 60, y0 + 34, x0 + 130, y0 + 92], 270, 90, fill=(200, 205, 210))
    pen.line([x0 + 95, y0 + 66, x0 + 95, y0 + 90], fill=(200, 205, 210), width=5)
    pen.arc([x0 + 180, y0 + 6, x0 + 460, y0 + 80], 200, 340, fill=TANGERINE, width=6)
    pen.ellipse([x0 + 430, y0 + 12, x0 + 448, y0 + 30], fill=(255, 214, 64))
    pen.ellipse([x0 + 436, y0 + 18, x0 + 442, y0 + 24], fill=ACCENT)


def draw_speaker(pen, x0, y0, w, h):
    """Capitol dome on columns, gavel at lower right."""
    pen.rectangle([x0, y0, x0 + w, y0 + h], fill=(232, 226, 210))
    pen.pieslice([x0 + w // 2 - 90, y0 + 6, x0 + w // 2 + 90, y0 + 96], 180, 360,
                 fill=(120, 130, 140))
    pen.rectangle([x0 + w // 2 - 96, y0 + 52, x0 + w // 2 + 96, y0 + 62],
                  fill=(100, 110, 120))
    pen.rectangle([x0 + w // 2 - 6, y0 - 2, x0 + w // 2 + 6, y0 + 12], fill=BRASS)
    for i in range(5):
        cx = x0 + w // 2 - 80 + i * 40
        pen.rectangle([cx - 7, y0 + 62, cx + 7, y0 + 88], fill=(240, 238, 228))
    pen.rectangle([x0 + w // 2 - 96, y0 + 88, x0 + w // 2 + 96, y0 + h - 2],
                  fill=(100, 110, 120))
    pen.rectangle([x0 + w - 118, y0 + 62, x0 + w - 58, y0 + 76], fill=(96, 66, 38))
    pen.line([x0 + w - 88, y0 + 76, x0 + w - 58, y0 + 92], fill=(120, 84, 50),
             width=5)


def draw_faith(pen, x0, y0, w, h):
    """Two bars: the second overtakes the first by 2035."""
    pen.rectangle([x0, y0, x0 + w, y0 + h], fill=(244, 238, 226))
    pen.line([x0 + 40, y0 + h - 18, x0 + w - 30, y0 + h - 18], fill=MUTED, width=2)
    pen.line([x0 + 40, y0 + 10, x0 + 40, y0 + h - 18], fill=MUTED, width=2)
    pen.rectangle([x0 + 90, y0 + 26, x0 + 190, y0 + h - 18], fill=OCEAN)
    pen.rectangle([x0 + 230, y0 + 12, x0 + 330, y0 + h - 18], fill=JADE)
    pen.text((x0 + 96, y0 + h - 44), "NOW", font=load_font(FONT_BOLD, 15),
             fill=(255, 255, 255))
    pen.text((x0 + 236, y0 + h - 44), "2035", font=load_font(FONT_BOLD, 15),
             fill=(255, 255, 255))
    pen.text((x0 + 346, y0 + 8), "ISLAM", font=load_font(FONT_BOLD, 17), fill=JADE)
    pen.text((x0 + 346, y0 + 30), "PASSES", font=load_font(FONT_BOLD, 17), fill=JADE)
    pen.text((x0 + 346, y0 + 52), "No. 1", font=load_font(FONT_BOLD, 17), fill=JADE)


def draw_voyager(pen, x0, y0, w, h):
    """Spacecraft with dish; a dotted curve runs out to a bright star."""
    pen.rectangle([x0, y0, x0 + w, y0 + h], fill=(12, 16, 34))
    for i in range(46):
        random.seed(200 + i)
        pen.point((x0 + random.randint(4, w - 4), y0 + random.randint(4, h - 4)),
                  fill=(220, 220, 240))
    x_start, y_start = x0 + 185, y0 + 56
    x_end, y_end = x0 + w - 88, y0 + 22
    for i in range(13):
        t = i / 12.0
        px = int(x_start + (x_end - x_start) * t)
        py = int(y_start + (y_end - y_start) * t - 26 * math.sin(math.pi * t))
        pen.ellipse([px - 3, py - 3, px + 3, py + 3], fill=BRASS)
    pen.ellipse([x0 + w - 96, y0 + 8, x0 + w - 72, y0 + 32], fill=(255, 240, 180))
    pen.rectangle([x0 + 40, y0 + 44, x0 + 130, y0 + 66], fill=(200, 205, 210))
    pen.pieslice([x0 + 120, y0 + 30, x0 + 180, y0 + 80], 270, 90, fill=(230, 232, 235))
    pen.line([x0 + 40, y0 + 55, x0 + 16, y0 + 55], fill=(160, 165, 170), width=4)
    pen.text((x0 + 200, y0 + 72), "1 LIGHT-DAY", font=load_font(FONT_BOLD, 18),
             fill=(255, 255, 255))


PANELS = [
    {"kicker": "SUMMIT OF THREE", "pic": draw_summit, "colour": MIDNIGHT,
     "head": "Trump, Xi & Putin meet in Shenzhen",
     "sub": "First three-way summit of the US, China and Russia leaders \u00b7 APEC sidelines"},
    {"kicker": "BRIDGE HIT AGAIN", "pic": draw_bridge, "colour": OCEAN,
     "head": "Ukraine strikes Crimean Bridge a 3rd time this week",
     "sub": "Traffic halted as damage is assessed \u00b7 Kerch Strait"},
    {"kicker": "GULF IN FLAMES", "pic": draw_gulf, "colour": ACCENT,
     "head": "US\u2013Iran fire exchange widens across the Gulf",
     "sub": "Iran hits Gulf targets after the US strike on Qeshm Island"},
    {"kicker": "A FIRST FOR THE HOUSE", "pic": draw_speaker, "colour": PLUM,
     "head": "Jeffries poised to be first Black Speaker",
     "sub": "Democrats nominate Hakeem Jeffries \u00b7 Washington"},
    {"kicker": "FAITH IN 2035", "pic": draw_faith, "colour": JADE,
     "head": "Islam set to pass Christianity as No. 1 faith",
     "sub": "Pew Research projection \u00b7 world demographics"},
    {"kicker": "ONE LIGHT-DAY OUT", "pic": draw_voyager, "colour": MIDNIGHT,
     "head": "Voyager 1 reaches one light-day from Earth",
     "sub": "First human-made object to travel so far \u00b7 NASA"},
]

BRIEFS = [
    "Anthropic's stock-market debut raises a record sum",
    "Australia, Canada, Italy & UK: let aid reach flooded Gaza",
    "Nvidia halts H-series chip shipments to China",
]


def render():
    page = Image.new("RGB", (CANVAS_W, CANVAS_H), PAGE_BG)
    pen = ImageDraw.Draw(page)

    # ---- masthead ----
    pen.rectangle([0, 0, CANVAS_W, 118], fill=TEXT)
    pen.text((512, 14), "THE WORLD IN ONE DAY", font=load_font(FONT_SERIF, 54),
             fill=PAGE_BG, anchor="ma")
    pen.text((512, 76), "THURSDAY 19 NOVEMBER 2026",
             font=load_font(FONT_BOLD, 26), fill=BRASS, anchor="ma")
    pen.line([16, 126, CANVAS_W - 16, 126], fill=ACCENT, width=4)

    # ---- story grid: 2 columns x 3 rows ----
    margin, top = 16, 140
    cell_w, cell_h = 488, 246
    gap_x, gap_y = 16, 12
    head_font = load_font(FONT_BOLD, 25)
    sub_font = load_font(FONT_REG, 17)
    kick_font = load_font(FONT_BOLD, 15)
    for idx, panel in enumerate(PANELS):
        col, row = idx % 2, idx // 2
        x = margin + col * (cell_w + gap_x)
        y = top + row * (cell_h + gap_y)
        pen.rectangle([x, y, x + cell_w, y + cell_h], fill=CARD,
                      outline=(200, 192, 172))
        pen.rectangle([x, y, x + cell_w, y + 26], fill=panel["colour"])
        pen.text((x + 10, y + 4), panel["kicker"], font=kick_font,
                 fill=(255, 255, 255))
        panel["pic"](pen, x + 8, y + 34, cell_w - 16, 92)
        hy = y + 136
        for line in wrap_text(pen, panel["head"], head_font, cell_w - 24)[:2]:
            pen.text((x + 12, hy), line, font=head_font, fill=TEXT)
            hy += 30
        for line in wrap_text(pen, panel["sub"], sub_font, cell_w - 24)[:2]:
            pen.text((x + 12, hy + 2), line, font=sub_font, fill=MUTED)
            hy += 22

    # ---- briefs strip ----
    fy = top + 3 * cell_h + 2 * gap_y + 4
    pen.rectangle([margin, fy, CANVAS_W - margin, fy + 78], fill=(238, 232, 214),
                  outline=(200, 192, 172))
    pen.text((margin + 10, fy + 8), "ALSO IN BRIEF", font=load_font(FONT_BOLD, 16),
             fill=ACCENT)
    brief_font = load_font(FONT_REG, 16)
    by = fy + 30
    for item in BRIEFS:
        pen.text((margin + 10, by), "\u2022  " + item, font=brief_font, fill=TEXT)
        by += 20
    pen.text((512, CANVAS_H - 22),
             "Six stories, one day \u2014 drawn from the news of 19 November 2026",
             font=load_font(FONT_REG, 14), fill=MUTED, anchor="ma")

    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
    page.save(out, "PNG", optimize=True)
    print("wrote", out, os.path.getsize(out), "bytes")


if __name__ == "__main__":
    render()
