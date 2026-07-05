import sys
from fpdf import FPDF

FONTS = sys.argv[1]
OUT = sys.argv[2]


def hx(s):
    s = s.lstrip("#")
    return tuple(int(s[i:i + 2], 16) for i in (0, 2, 4))


SKY_TOP = hx("9fdcf2")
SKY_MID = hx("bfe9f0")
SKY_BOT = hx("d7f1ea")
SAND = hx("f7e7b4")
GRASS = hx("8ed18b")
GRASS_DARK = hx("6fbf72")
CREAM = hx("fdf6e3")
CREAM_EDGE = hx("e7d4ab")
INK = hx("6b5743")
INK_SOFT = hx("9a866d")
BROWN_TEXT = hx("5a4836")
PINK = hx("f4a8bd")
GREEN = hx("8fce9a")
TEAL = hx("4fc3c7")
WOOD = hx("9a6537")
WOOD_DARK = hx("5e3c1d")
WOOD_BORDER = hx("432a13")
GOLD = hx("ffd24d")
GOLD_DEEP = hx("ef9f23")
WHITE = (255, 255, 255)

DAYS = [
    {
        "pill": "DAY 1 · 7 JULY",
        "num": "1",
        "sub": "ESPORTS DAY",
        "title": "Opening & Brawl Stars",
        "hours": "10 AM – 5 PM",
        "accent": PINK,
        "events": [
            ("Great Game Week Opening Ceremony", "The festival officially begins!", "10 AM – 11 AM"),
            ("Brawl Stars Tournament", "Opening matches all the way to the winner announcement", "11:30 AM – 5 PM"),
        ],
        "host": "Hosted by APU Game Dev Club × APU Esports Club",
    },
    {
        "pill": "DAY 2 · 8 JULY",
        "num": "2",
        "sub": "BOARD GAMES DAY",
        "title": "Tabletop Takeover",
        "hours": "10 AM – 5 PM",
        "accent": GREEN,
        "events": [
            ("Warhammer 40,000 Painting & Play Session", "Paint your own miniature, then take it to the battlefield", "10 AM – 4 PM"),
            ("Board Game Showcase & Sale", "Try out tabletop favourites and take one home", "10 AM – 4 PM"),
        ],
        "host": "Hosted by APU Game Dev Club × APU Board Game Club",
    },
    {
        "pill": "DAY 3 · 9 JULY",
        "num": "3",
        "sub": "GAME DEV DAY",
        "title": "Create & Celebrate",
        "hours": "10 AM – 6 PM",
        "accent": GOLD_DEEP,
        "events": [
            ("GGJ 2026 Pitching", "Great Game Jam teams pitch their creations to the judges", "10 AM – 12 PM"),
            ("Student Game Showcase", "Play games made by APU students, all day long", "10 AM – 5 PM"),
            ("Portfolio Review", "Get your work reviewed by industry professionals", "12 PM – 4 PM"),
            ("Industry Talks", "Hear from folks working in the games industry", "1 PM – 5:30 PM"),
            ("Closing & Award Ceremony", "Winners crowned and the festival wraps up", "5:30 PM – 6 PM"),
        ],
        "host": "Hosted by APU Game Dev Club × Great Game Jam",
    },
]

pdf = FPDF(orientation="P", unit="mm", format="A4")
pdf.set_auto_page_break(False)
pdf.set_title("APU Great Game Week 2026 – E-Handbook")
pdf.set_author("APU Game Dev Club × APU Esports Club × APU Board Game Club")
pdf.add_font("Fredoka", "", f"{FONTS}/fredoka-500.ttf")
pdf.add_font("Fredoka", "B", f"{FONTS}/fredoka-700.ttf")
pdf.add_font("FredokaSB", "", f"{FONTS}/fredoka-600.ttf")
pdf.add_font("Quicksand", "", f"{FONTS}/quicksand-500.ttf")
pdf.add_font("Quicksand", "B", f"{FONTS}/quicksand-700.ttf")
pdf.add_page()

W, H = 210, 297


def lerp(a, b, t):
    return tuple(round(a[i] + (b[i] - a[i]) * t) for i in range(3))


def vgrad(x, y, w, h, c1, c2, steps=40):
    band = h / steps
    for i in range(steps):
        pdf.set_fill_color(*lerp(c1, c2, i / (steps - 1)))
        pdf.rect(x, y + i * band, w, band + 0.05, style="F")


def rrect(x, y, w, h, r, fill=None, stroke=None, lw=0.5):
    style = ""
    if fill:
        pdf.set_fill_color(*fill)
        style += "F"
    if stroke:
        pdf.set_draw_color(*stroke)
        pdf.set_line_width(lw)
        style += "D"
    pdf.rect(x, y, w, h, style=style, round_corners=True, corner_radius=r)


def shadow(x, y, w, h, r, dy=1.6, op=0.10):
    with pdf.local_context(fill_opacity=op):
        rrect(x, y + dy, w, h, r, fill=(0, 0, 0))


def center_text(cx, y, txt, family, style, size, color, shadow_color=None):
    pdf.set_font(family, style, size)
    tw = pdf.get_string_width(txt)
    if shadow_color:
        pdf.set_text_color(*shadow_color)
        pdf.text(cx - tw / 2, y + 0.45, txt)
    pdf.set_text_color(*color)
    pdf.text(cx - tw / 2, y, txt)


def pill(cx_or_x, y, txt, bg, fg, size=10, pad=4.5, h=8, family="FredokaSB", style="", centered=True, border=True):
    pdf.set_font(family, style, size)
    tw = pdf.get_string_width(txt)
    w = tw + pad * 2
    x = cx_or_x - w / 2 if centered else cx_or_x
    shadow(x, y, w, h, h / 2, dy=1.1, op=0.08)
    rrect(x, y, w, h, h / 2, fill=bg)
    if border:
        with pdf.local_context(stroke_opacity=0.55):
            rrect(x, y, w, h, h / 2, stroke=WHITE, lw=0.8)
    pdf.set_text_color(*fg)
    pdf.text(x + pad, y + h / 2 + size * 0.123, txt)
    return w


def cloud(cx, cy, s=1.0, op=0.9):
    with pdf.local_context(fill_opacity=op):
        pdf.set_fill_color(*WHITE)
        for dx, dy, d in ((0, 0, 9), (6, -2.5, 11), (13, 0, 9), (5, 2, 10)):
            pdf.ellipse(cx + dx * s, cy + dy * s, d * s, d * s * 0.82, style="F")


vgrad(0, 0, W, 150, SKY_TOP, SKY_MID)
vgrad(0, 150, W, H - 150, SKY_MID, SKY_BOT)

with pdf.local_context(fill_opacity=0.25):
    pdf.set_fill_color(*GOLD)
    pdf.ellipse(160, 2, 30, 30, style="F")
pdf.set_fill_color(*GOLD)
pdf.ellipse(164, 6, 22, 22, style="F")
pdf.set_fill_color(*hx("fff4c2"))
pdf.ellipse(168, 9, 8, 8, style="F")

cloud(16, 22, 1.0, 0.85)
cloud(38, 48, 0.55, 0.7)
cloud(158, 52, 0.7, 0.7)

pdf.set_fill_color(*GRASS)
pdf.ellipse(-40, 262, 290, 80, style="F")
pdf.set_fill_color(*GRASS_DARK)
pdf.ellipse(-40, 266.5, 290, 80, style="F")
pdf.set_fill_color(*SAND)
pdf.ellipse(-40, 269, 290, 80, style="F")
pdf.rect(0, 288, W, 9, style="F")

sx, sy, sw, sh = 43, 10, 124, 34
shadow(sx, sy, sw, sh, 6, dy=2, op=0.14)
rrect(sx, sy, sw, sh, 6, fill=WOOD, stroke=WOOD_BORDER, lw=2)
with pdf.local_context(fill_opacity=0.10):
    pdf.set_fill_color(0, 0, 0)
    for px in range(int(sx + 9), int(sx + sw - 4), 10):
        pdf.rect(px, sy + 1.5, 0.8, sh - 3, style="F")
    pdf.rect(sx + 2, sy + sh * 0.55, sw - 4, sh * 0.42, style="F")
for bx in (sx + 7, sx + sw - 9):
    pdf.set_fill_color(*hx("2a1808"))
    pdf.ellipse(bx, sy + sh - 7, 2.6, 2.6, style="F")
    pdf.set_fill_color(*hx("8a6a4a"))
    pdf.ellipse(bx + 0.5, sy + sh - 6.5, 1, 1, style="F")

center_text(W / 2, sy + 12, "Great Game Week", "FredokaSB", "", 14.5, GOLD, GOLD_DEEP)
center_text(W / 2, sy + 26, "E-Handbook 2026", "Fredoka", "B", 25, GOLD, GOLD_DEEP)

pdf.set_font("FredokaSB", "", 10)
w1 = pdf.get_string_width("7–9 July 2026") + 9
w2 = pdf.get_string_width("APU Campus · Level 3") + 9
gap = 6
start = W / 2 - (w1 + w2 + gap) / 2
pill(start, 50, "7–9 July 2026", GREEN, WHITE, size=10, centered=False)
pill(start + w1 + gap, 50, "APU Campus · Level 3", TEAL, WHITE, size=10, centered=False)

center_text(W / 2, 64.5, "APU GAME DEV CLUB × APU ESPORTS CLUB × APU BOARD GAME CLUB", "Quicksand", "B", 8, INK_SOFT)
center_text(W / 2, 69.5, "“Celebrating the culture and love of games”", "Quicksand", "", 9, INK_SOFT)


def day_card(y0, d):
    x, w = 14, 182
    n = len(d["events"])
    rows_y = y0 + 20
    row_h = 10.5
    h = 20 + n * row_h + 8

    shadow(x, y0, w, h, 5)
    rrect(x, y0, w, h, 5, fill=CREAM)
    pdf.set_dash_pattern(dash=1.2, gap=1.4)
    rrect(x + 3, y0 + 3, w - 6, h - 6, 3.5, stroke=CREAM_EDGE, lw=0.7)
    pdf.set_dash_pattern()

    pill(x + 8, y0 - 4, d["pill"], d["accent"], WHITE, size=9, pad=4, h=7.6, centered=False)

    bx, by, bd = x + 8, y0 + 5, 13
    pdf.set_fill_color(*WHITE)
    pdf.ellipse(bx, by, bd, bd, style="F")
    pdf.set_dash_pattern(dash=1, gap=1.2)
    pdf.set_draw_color(*d["accent"])
    pdf.set_line_width(0.9)
    pdf.ellipse(bx, by, bd, bd, style="D")
    pdf.set_dash_pattern()
    center_text(bx + bd / 2, by + bd / 2 + 1.8, d["num"], "Fredoka", "B", 15, d["accent"])

    pdf.set_font("FredokaSB", "", 8)
    pdf.set_text_color(*d["accent"])
    pdf.text(x + 25, y0 + 10, d["sub"])
    pdf.set_font("FredokaSB", "", 14.5)
    pdf.set_text_color(*INK)
    pdf.text(x + 25, y0 + 16.5, d["title"])

    pdf.set_font("FredokaSB", "", 8.5)
    hw = pdf.get_string_width(d["hours"]) + 8
    pill(x + w - 8 - hw, y0 + 8, d["hours"], GREEN, WHITE, size=8.5, pad=4, h=7, centered=False)

    for i, (name, desc, time) in enumerate(d["events"]):
        ry = rows_y + i * row_h
        if i > 0:
            pdf.set_dash_pattern(dash=1.2, gap=1.4)
            pdf.set_draw_color(*CREAM_EDGE)
            pdf.set_line_width(0.6)
            pdf.line(x + 8, ry - 2.4, x + w - 8, ry - 2.4)
            pdf.set_dash_pattern()

        pdf.set_fill_color(*d["accent"])
        pdf.set_draw_color(*WHITE)
        pdf.set_line_width(0.8)
        pdf.ellipse(x + 8.4, ry + 0.2, 3.6, 3.6, style="DF")

        pdf.set_font("Quicksand", "B", 10.5)
        pdf.set_text_color(*BROWN_TEXT)
        pdf.text(x + 15, ry + 3.2, name)
        pdf.set_font("Quicksand", "", 8)
        pdf.set_text_color(*INK_SOFT)
        pdf.text(x + 15, ry + 7, desc)

        pdf.set_font("FredokaSB", "", 8.5)
        tw = pdf.get_string_width(time) + 8
        pill(x + w - 8 - tw, ry - 0.8, time, TEAL, WHITE, size=8.5, pad=4, h=6.6, centered=False)

    pdf.set_font("Quicksand", "B", 8)
    pdf.set_text_color(*INK_SOFT)
    pdf.text(x + 8, y0 + h - 4, d["host"])
    return y0 + h


y = 77
for d in DAYS:
    y = day_card(y, d) + 6.5

pdf.set_font("Quicksand", "B", 8.5)
tip = "Times may shift a smidge on the day – the GGW booth always knows best!"
tw = pdf.get_string_width(tip) + 12
fx = W / 2 - tw / 2
fy = min(y + 1, 270)
shadow(fx, fy, tw, 9, 4.5, dy=1.2, op=0.08)
with pdf.local_context(fill_opacity=0.95):
    rrect(fx, fy, tw, 9, 4.5, fill=WHITE)
pdf.set_text_color(*INK_SOFT)
pdf.text(fx + 6, fy + 5.8, tip)

center_text(W / 2, 293.5, "APU GREAT GAME WEEK 2026", "Fredoka", "B", 9, WOOD_DARK)

pdf.output(OUT)
print("wrote", OUT)
