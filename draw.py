"""NEWS TOWERS - round 5 rebuild for NI21 (Saturday 21 November 2026).

Structure copied from the pixel-measured dissection of NI21's #1
(BEDAH-TOP1-NI21.md): an airy classic newspaper on cream paper.
The date alone is the masthead; three equal leads; ten mini cards in
2 rows x 5; every pictured card has a full 64 px scene with a big
subject, a black slug box inside the scene, a white CONFIRMED /
REPORTED chip, a black location bar, and a red circle badge.
No numbers strip, no tally bar: numbers live in slugs and headlines,
structural counts live in the claims bar.

Content comes ONLY from POOL21 (verified pool for 21 Nov 2026):
13 pictured cards + 27 one-line briefs = 40 stories. The pool holds
no further verified stories, so the page honestly claims 40, not 44.

The News Towers identity survives inside the scenes (a tall lit tower
stands in most scenes) and in the claims bar - the old navy-dark
tower-ribbon page is gone.
"""
import os
import sys

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from mapdata import LAND_POLYS  # noqa: E402

W = H = 1024
PAPER = (245, 241, 224)
RED = (192, 40, 25)
BLACK = (18, 16, 14)
INK = (32, 30, 26)
GREY = (92, 86, 74)
RULE = (120, 112, 96)

FD = os.path.join(HERE, "fonts")
_cache = {}


def F(name, size):
    key = (name, size)
    if key not in _cache:
        _cache[key] = ImageFont.truetype(os.path.join(FD, name), size)
    return _cache[key]


def PF(size):
    return F("PlayfairDisplay-900.ttf", size)


def AB(size):
    return F("Archivo-Bold.ttf", size)


def AM(size):
    return F("Archivo-Medium.ttf", size)


# ------------------------------------------------------------ data
# n, place, region, category, headline, deck, slug, chip, kind, (lon, lat)
CARDS = [
    (1, "WARSAW, POLAND", "EUROPE", "CONFLICT",
     "Rutte flies to Warsaw after missiles land",
     "Two missiles and a suspected jet drone came down in the "
     "south-east, a Kh-101 near Nowy Lipowiec. NATO's Rutte calls it "
     "a \u201cgrave violation\u201d; Tusk calls it a deliberate provocation.",
     "3 WEAPONS CROSS", "CONFIRMED \u2013 AP", "missile", (21.0, 52.2)),
    (2, "ANTALYA", "GLOBAL", "CLIMATE TALKS",
     "COP31 runs into overtime with no deal yet",
     "Talks ran past Friday's scheduled close into Saturday. The draft "
     "drops every fossil-fuel reference and the $120bn finance target; "
     "a third draft is due this morning.",
     "NO DEAL YET", "REPORTED \u2013 AP", "dome", (30.7, 36.9)),
    (3, "NEW YORK", "AMERICAS", "MARKETS",
     "Wall Street enters correction as AI rout deepens",
     "The S&P 500 fell about 3.7% on Friday, pushing it into correction "
     "territory. The Nasdaq dropped 5.28% as chip and AI shares plunged.",
     "NASDAQ -5.28%", "REPORTED \u2013 SIMPLELIFE", "chart", (-74.0, 40.7)),
    (4, "KRYVYI RIH", "EUROPE", "WAR",
     "Russian strike kills two, injures 42",
     "An overnight strike on Kryvyi Rih kills two and injures 42, four "
     "of them children, the city's military chief says.",
     "2 DEAD \u00b7 42 HURT", "CONFIRMED \u2013 APPISTOS", "blast", (33.4, 47.9)),
    (5, "COPENHAGEN", "EUROPE", "SECURITY",
     "Denmark exposes 'assassination plot'",
     "Russia 'planned and initiated' a bid to kill a Ukrainian-American "
     "rapper near Copenhagen, Denmark says.",
     "ATTACHE EXPELLED", "CONFIRMED \u2013 BBC", "target", (12.6, 55.7)),
    (6, "KYIV", "EUROPE", "WAR",
     "Russia's barrage: 400 drones, 110 missiles",
     "At least eight are dead across Ukraine in the overnight barrage. "
     "The Austrian embassy is hit in Kyiv.",
     "400 DRONES", "CONFIRMED \u2013 BBC", "drones", (30.5, 50.4)),
    (7, "ODISHA, INDIA", "ASIA", "STORM",
     "After Akvan: 372,000 moved, no deaths",
     "A day after landfall, no deaths are reported and relief is under "
     "way. The storm weakens to a depression.",
     "372,000 MOVED", "CONFIRMED \u2013 RIDHU TIMES", "cyclone", (84.9, 19.3)),
    (8, "BRUSSELS", "EUROPE", "AID",
     "EU adopts 1bn euro military aid for Ukraine",
     "Joint buying runs via the Peace Facility. Britain pledges 1,000+ "
     "drones in a 260m pound package alongside the EU deal.",
     "\u20ac1BN ADOPTED", "CONFIRMED \u2013 REUTERS", "euro", (4.3, 50.8)),
    (9, "NEW YORK", "AMERICAS", "CYBER",
     "JPMorgan, Visa, Mastercard hit by cyberattack",
     "The banks report incidents at third-party vendors. Their core "
     "payment networks are unaffected, they say.",
     "3 NETWORKS HIT", "CONFIRMED \u2013 REUTERS", "shield", (-73.9, 40.8)),
    (10, "ULAANBAATAR", "ASIA", "POLITICS",
     "Mongolia's president resigns",
     "The resignation sets the stage for a snap election. It caps a "
     "week of political turmoil in the capital.",
     "SNAP ELECTION NEXT", "CONFIRMED \u2013 REUTERS", "flag", (106.9, 47.9)),
    (11, "THE HAGUE", "GLOBAL", "WORLD COURT",
     "Myanmar ruling rattles Israel's Gaza defence",
     "The world court's genocide verdict against Myanmar raises "
     "questions in Jerusalem over its own case, experts say.",
     "GENOCIDE VERDICT", "CONFIRMED \u2013 BBC", "scales", (4.3, 52.1)),
    (12, "JOHANNESBURG", "AFRICA", "ELECTION",
     "ANC scrambles after worst result since 1994",
     "The ANC wins 31% of the vote, its worst since 1994. It now races "
     "for coalition deals to stay in government.",
     "ANC 31%", "CONFIRMED \u2013 BBC", "ballot", (28.0, -26.2)),
    (13, "WELLINGTON", "OCEANIA", "CRICKET",
     "India fight back: 159/1 at stumps, day two",
     "India trail New Zealand by 209 in the first Test after the hosts "
     "made 368. Nicholls made 175 not out for the hosts.",
     "159/1 \u00b7 DAY TWO", "CONFIRMED \u2013 ICC", "cricket", (174.8, -41.3)),
]

# n, lead-in (city), short tail - pool briefs 14-40, cut to one line
BRIEFS = [
    (14, "Kathmandu", "Nepal's new leader Shah faces an India test"),
    (15, "Washington", "US releases more UFO footage from Mideast"),
    (16, "Los Angeles", "Hyundai unveils the 2027 Elantra at the show"),
    (17, "Cardiff", "Price beats Kotaskova, undisputed champion"),
    (18, "Paris", "Three police sentenced over the Zecler beating"),
    (19, "Oxford", "Life, 22 years minimum, for the Thames murder"),
    (20, "New York", "Gupta gets 19+ years over the Sikh murder plot"),
    (21, "Cincinnati", "Fiona the hippo dies after eating a hat"),
    (22, "Washington", "US sanctions four Iranians over oil revenues"),
    (23, "Hormuz", "Tanker struck and on fire in the strait"),
    (24, "Los Angeles", "Jury convicts the Palisades Fire starter"),
    (25, "Frankfurt", "ECB names Boone, Brunnermeier to its Board"),
    (26, "Buenos Aires", "Senate backs a disability framework, 71-0"),
    (27, "Riyadh", "Saudi coalition intercepts Houthi missiles"),
    (28, "Barcelona", "Pill hailed as a pancreatic cancer breakthrough"),
    (29, "Gaza", "Children appeal for help on Children's Day"),
    (30, "Madrid", "Amnesty: police used excess force in the strike"),
    (31, "Rome", "Workers and students march against Meloni"),
    (32, "Jeddah", "Thunderstorms warned through Tuesday"),
    (33, "Kuala Lumpur", "10,000 Rohingya to go to Turkey for training"),
    (34, "Kharkiv", "'Bear Trap' finished in the Kharkiv area"),
    (35, "Islamabad", "Minerals worth $8-10 trillion, minister says"),
    (36, "Singapore", "US presses Singapore, Malaysia on Iran"),
    (37, "Paris", "France seeks a UN meeting on the Kyiv strikes"),
    (38, "Kyiv", "War tally: 771 killed, 2,300+ missing"),
    (39, "Ankara", "Turkey welcomes the World Court's Myanmar ruling"),
    (40, "Turin", "ATP semis: Alcaraz-Shelton, Zverev-Medvedev"),
]

DAYPARTS = [
    ("OVERNIGHT", "Kryvyi Rih strike: two killed, 42 injured"),
    ("MORNING", "Rutte flies to Warsaw over the missiles"),
    ("MIDDAY", "Antalya: third COP31 draft due after talks"),
    ("AFTERNOON", "Denmark expels the Russian attache"),
    ("EVENING", "Stumps in Wellington: India 159/1"),
]

REGION_COLORS = {
    "EUROPE": (61, 122, 196),
    "GLOBAL": (150, 108, 199),
    "AMERICAS": (214, 92, 56),
    "ASIA": (46, 150, 105),
    "AFRICA": (222, 158, 44),
    "OCEANIA": (52, 160, 190),
}
CONTINENTS = [("EUROPE", "EUROPE"), ("ASIA", "ASIA"),
              ("AMERICAS", "AMERICAS"), ("AFRICA", "AFRICA"),
              ("OCEANIA", "OCEANIA"), ("GLOBAL", "WORLDWIDE")]

SKIES = [(247, 214, 176), (186, 222, 242), (250, 226, 186),
         (252, 214, 182), (196, 230, 240), (182, 216, 246),
         (204, 234, 230), (250, 232, 182), (190, 226, 248),
         (246, 224, 196), (206, 230, 242), (252, 234, 190),
         (196, 232, 214)]


# ------------------------------------------------------------ helpers
def wrap(d, text, font, maxw):
    words, lines, cur = text.split(), [], ""
    for w_ in words:
        t = (cur + " " + w_).strip()
        if d.textlength(t, font=font) <= maxw or not cur:
            cur = t
        else:
            lines.append(cur)
            cur = w_
    if cur:
        lines.append(cur)
    return lines


def fit_text(d, text, font, maxw):
    """Cut (never wrap) until text fits maxw."""
    if d.textlength(text, font=font) <= maxw:
        return text
    while text and d.textlength(text + "\u2026", font=font) > maxw:
        text = text.rsplit(" ", 1)[0] if " " in text else text[:-1]
    return text + "\u2026"


def tower(d, x, ybase, w, h, body, win=(255, 226, 138)):
    """The News Towers motif: one tall lit tower inside a scene."""
    d.rectangle([x, ybase - h, x + w, ybase], fill=body)
    d.polygon([(x - 2, ybase - h), (x + w + 2, ybase - h),
               (x + w - 3, ybase - h - 5), (x + 3, ybase - h - 5)],
              fill=tuple(min(255, int(v * 1.25)) for v in body))
    cols = max(2, int(w // 9))
    rows = max(3, int(h // 11))
    cw, ch = w / cols, h / rows
    for r in range(rows):
        for c in range(cols):
            if (r * 7 + c * 3) % 3 != 0:
                d.rectangle([x + c * cw + 1.6, ybase - h + r * ch + 2,
                             x + (c + 1) * cw - 1.6,
                             ybase - h + (r + 1) * ch - 2], fill=win)


# ------------------------------------------------------------ scenes
def scene(d, box, card):
    """Flat bright scene, 64 px tall, <=3 large elements, big subject."""
    x0, y0, x1, y1 = box
    n, kind = card[0], card[8]
    sky = SKIES[n - 1]
    d.rectangle(box, fill=sky)
    ground = tuple(int(v * 0.88) for v in sky)
    d.rectangle([x0, y1 - 9, x1, y1], fill=ground)
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2 + 3
    dark = (38, 44, 66)
    if kind == "missile":
        tower(d, x1 - 34, y1 - 9, 24, 46, (96, 110, 150))
        d.polygon([(x0 + 18, y1 - 16), (x0 + 62, y0 + 14),
                   (x0 + 74, y0 + 24), (x0 + 30, y1 - 8)], fill=dark)
        d.polygon([(x0 + 62, y0 + 14), (x0 + 84, y0 + 8),
                   (x0 + 74, y0 + 24)], fill=RED)
        d.polygon([(x0 + 18, y1 - 16), (x0 + 6, y1 - 6),
                   (x0 + 30, y1 - 8)], fill=(240, 150, 60))
    elif kind == "dome":
        d.rectangle([cx - 52, y1 - 30, cx + 52, y1 - 9], fill=(240, 244, 248))
        d.pieslice([cx - 40, y1 - 62, cx + 40, y1 - 6], 180, 360,
                   fill=(64, 150, 120))
        d.rectangle([cx - 3, y0 + 4, cx + 3, y0 + 14], fill=dark)
        for i in range(-2, 3):
            d.rectangle([cx + i * 18 - 3, y1 - 26, cx + i * 18 + 3, y1 - 10],
                        fill=dark)
    elif kind == "chart":
        tower(d, x0 + 10, y1 - 9, 20, 38, (110, 130, 170))
        tower(d, x0 + 34, y1 - 9, 20, 48, (84, 104, 150))
        pts = [(x0 + 66, y0 + 14), (x0 + 96, y0 + 22), (x0 + 122, y0 + 18),
               (x0 + 150, y0 + 38), (x1 - 14, y0 + 50)]
        d.line(pts, fill=RED, width=5, joint="curve")
        d.polygon([(x1 - 14, y0 + 50), (x1 - 28, y0 + 46),
                   (x1 - 18, y0 + 36)], fill=RED)
    elif kind == "blast":
        tower(d, x1 - 32, y1 - 9, 22, 42, (104, 112, 140))
        import math
        pts = []
        for i in range(16):
            ang = i * math.pi / 8
            r = 26 if i % 2 == 0 else 12
            pts.append((cx - 22 + r * math.cos(ang), cy + r * math.sin(ang)))
        d.polygon(pts, fill=(240, 120, 40))
        d.ellipse([cx - 33, cy - 11, cx - 11, cy + 11], fill=(250, 200, 70))
    elif kind == "target":
        tower(d, x0 + 10, y1 - 9, 22, 44, (96, 118, 158))
        for r, col in ((24, RED), (17, (250, 250, 248)), (10, RED)):
            d.ellipse([cx + 16 - r, cy - r, cx + 16 + r, cy + r], fill=col)
        d.ellipse([cx + 13, cy - 3, cx + 19, cy + 3], fill=dark)
    elif kind == "drones":
        for dx, dy, s in ((-38, -12, 1.0), (26, -4, 0.8)):
            bx, by = cx + dx, cy + dy
            d.rectangle([bx - 16 * s, by - 5 * s, bx + 16 * s, by + 5 * s],
                        fill=dark)
            for sx in (-20, 20):
                d.line([bx + sx * s - 7, by - 10 * s, bx + sx * s + 7,
                        by - 10 * s], fill=dark, width=3)
            d.line([bx, by + 5 * s, bx, by + 12 * s], fill=dark, width=2)
        tower(d, x1 - 30, y1 - 9, 20, 36, (110, 124, 160))
    elif kind == "cyclone":
        for r, col in ((26, (70, 150, 190)), (19, (110, 180, 214)),
                       (12, (160, 210, 232)), (6, (240, 248, 250))):
            d.ellipse([cx - 30 - r, cy - r, cx - 30 + r, cy + r], fill=col)
        tower(d, x1 - 34, y1 - 9, 24, 44, (90, 130, 140))
    elif kind == "euro":
        d.ellipse([cx - 40, cy - 27, cx + 14, cy + 27], fill=(52, 92, 170))
        t = "\u20ac"
        f = PF(44)
        tw = d.textlength(t, font=f)
        d.text((cx - 13 - tw / 2, cy - 26), t, font=f, fill=(255, 224, 90))
        tower(d, x1 - 32, y1 - 9, 22, 46, (100, 116, 156))
    elif kind == "shield":
        d.polygon([(cx - 8, y0 + 8), (cx + 22, y0 + 16), (cx + 22, y1 - 24),
                   (cx - 8, y1 - 12), (cx - 38, y1 - 24), (cx - 38, y0 + 16)],
                  fill=(52, 110, 170))
        d.rectangle([cx - 20, cy - 2, cx + 4, cy + 16], fill=(250, 250, 248))
        d.rectangle([cx - 15, cy - 10, cx - 1, cy - 1], outline=(250, 250, 248),
                      width=3)
        tower(d, x0 + 8, y1 - 9, 20, 40, (104, 122, 158))
    elif kind == "flag":
        tower(d, x1 - 34, y1 - 9, 24, 48, (110, 120, 150))
        d.rectangle([x0 + 30, y0 + 8, x0 + 34, y1 - 9], fill=dark)
        d.polygon([(x0 + 34, y0 + 9), (x0 + 76, y0 + 16), (x0 + 34, y0 + 26)],
                  fill=RED)
        d.rectangle([x0 + 16, y1 - 16, x0 + 88, y1 - 9], fill=dark)
    elif kind == "scales":
        d.rectangle([cx - 3, y0 + 12, cx + 3, y1 - 12], fill=dark)
        d.rectangle([cx - 42, y0 + 14, cx + 42, y0 + 19], fill=dark)
        for sx in (-42, 42):
            d.line([cx + sx, y0 + 19, cx + sx - 10, y1 - 20], fill=dark, width=2)
            d.line([cx + sx, y0 + 19, cx + sx + 10, y1 - 20], fill=dark, width=2)
            d.arc([cx + sx - 13, y1 - 26, cx + sx + 13, y1 - 8], 0, 180,
                  fill=dark, width=3)
        d.rectangle([cx - 16, y1 - 13, cx + 16, y1 - 9], fill=dark)
    elif kind == "ballot":
        d.rectangle([cx - 46, y1 - 34, cx + 8, y1 - 9], fill=(250, 250, 248),
                    outline=dark, width=2)
        d.rectangle([cx - 38, y1 - 27, cx, y1 - 22], fill=dark)
        t = "31%"
        f = PF(30)
        d.text((cx - 38, y1 - 22), "", font=f, fill=RED)
        tw = d.textlength(t, font=f)
        d.text((cx + 20, cy - 18), t, font=f, fill=RED)
        tower(d, x1 - 30, y1 - 9, 20, 40, (120, 110, 140))
    elif kind == "cricket":
        d.polygon([(x0 + 26, y1 - 12), (x0 + 62, y0 + 12), (x0 + 72, y0 + 18),
                   (x0 + 38, y1 - 6)], fill=(196, 140, 70))
        d.ellipse([x0 + 66, y0 + 26, x0 + 88, y0 + 48], fill=RED)
        for i in range(3):
            d.rectangle([x1 - 52 + i * 12, y1 - 38, x1 - 48 + i * 12, y1 - 9],
                        fill=(240, 230, 190), outline=dark, width=1)
        d.rectangle([x1 - 54, y1 - 38, x1 - 14, y1 - 34], fill=dark)


# ------------------------------------------------------------ cards
def draw_card(d, x, y, w, card, lead=False):
    n, place, region, cat, head, deck, slug, chip, kind, ll = card
    # scene 64 px
    scene(d, (x, y, x + w, y + 64), card)
    sf = AB(10 if lead else 9)
    # slug: black box top-left INSIDE scene
    sw = d.textlength(slug, font=sf)
    d.rectangle([x + 4, y + 4, x + 8 + sw, y + 19], fill=BLACK)
    d.text((x + 6, y + 6), slug, font=sf, fill=(255, 255, 255))
    # chip: white, black border, top-right INSIDE scene
    cf = AB(9 if lead else 8)
    cw_ = d.textlength(chip, font=cf)
    if x + 12 + sw + cw_ + 10 > x + w:  # shrink slug font if crowded
        sf = AB(8)
        sw = d.textlength(slug, font=sf)
        d.rectangle([x + 4, y + 4, x + 8 + sw, y + 19], fill=BLACK)
        d.text((x + 6, y + 7), slug, font=sf, fill=(255, 255, 255))
    d.rectangle([x + w - cw_ - 10, y + 4, x + w - 4, y + 19],
                fill=(255, 255, 255), outline=BLACK, width=1)
    d.text((x + w - cw_ - 7, y + 6), chip, font=cf, fill=BLACK)
    # black location bar, full card width
    by = y + 64
    d.rectangle([x, by, x + w, by + 19], fill=BLACK)
    lf = AB(11)
    loc = fit_text(d, place, lf, w - 10)
    d.text((x + 5, by + 4), loc, font=lf, fill=(255, 255, 255))
    # badge row: red filled circle + region . category in red caps
    ry = by + 23
    d.ellipse([x + 1, ry, x + 21, ry + 20], fill=RED)
    nf = AB(11)
    t = str(n)
    d.text((x + 11 - d.textlength(t, font=nf) / 2, ry + 4), t, font=nf,
           fill=(255, 255, 255))
    bf = AB(12)
    lab = fit_text(d, region + " \u00b7 " + cat, bf, w - 28)
    d.text((x + 26, ry + 4), lab, font=bf, fill=RED)
    # headline serif bold (shrink a step if it would pass 2 lines)
    hy = ry + 24
    hsize = 20 if lead else 15
    while True:
        hf = PF(hsize)
        hlines = wrap(d, head, hf, w - 4)
        if len(hlines) <= 2 or hsize <= 12:
            break
        hsize -= 1
    hstep = 22 if lead else 17
    for ln in hlines[:2]:
        d.text((x + 1, hy), ln, font=hf, fill=BLACK)
        hy += hstep
    # deck sans, <=3 lines (lead) / <=2 (mini), then the card body
    # stays empty on purpose - the whitespace is the design
    df = AM(11 if lead else 10)
    dstep = 13 if lead else 12
    maxl = 3
    for ln in wrap(d, deck, df, w - 4)[:maxl]:
        d.text((x + 1, hy + 1), ln, font=df, fill=INK)
        hy += dstep


# ------------------------------------------------------------ map
def build_dotmap(box):
    """Dot-matrix world: a dot wherever a land polygon covers the grid."""
    x0, y0, x1, y1 = box
    polys = []
    for pts in LAND_POLYS:
        pts = [(float(lo), float(la)) for lo, la in pts]
        los = [p[0] for p in pts]
        las = [p[1] for p in pts]
        polys.append((pts, min(los), max(los), min(las), max(las)))

    def inside(lon, lat, pts):
        c = False
        j = len(pts) - 1
        for i in range(len(pts)):
            xi, yi = pts[i]
            xj, yj = pts[j]
            if ((yi > lat) != (yj > lat)) and \
               (lon < (xj - xi) * (lat - yi) / (yj - yi) + xi):
                c = not c
            j = i
        return c

    step = 4.5
    dots = []
    lat_top, lat_bot = 84.0, -58.0
    gy = y0 + 2
    while gy < y1 - 2:
        lat = lat_top - (gy - y0) / (y1 - y0) * (lat_top - lat_bot)
        gx = x0 + 2
        while gx < x1 - 2:
            lon = -180 + (gx - x0) / (x1 - x0) * 360
            for pts, mnlo, mxlo, mnla, mxla in polys:
                if mnlo <= lon <= mxlo and mnla <= lat <= mxla and \
                        inside(lon, lat, pts):
                    dots.append((gx, gy))
                    break
            gx += step
        gy += step

    def proj(lon, lat):
        return (x0 + (lon + 180) / 360.0 * (x1 - x0),
                y0 + (lat_top - lat) / (lat_top - lat_bot) * (y1 - y0))
    return dots, proj


# ------------------------------------------------------------ page
def render():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    MX = 14
    CW = W - 2 * MX  # 996

    # ---- claims bar
    d.text((MX, 7), "NEWS TOWERS", font=AB(13), fill=RED)
    right = "40 STORIES \u00b7 13 DRAWN \u00b7 6 CONTINENTS \u00b7 ALL FROM 21 NOVEMBER"
    rf = AB(11)
    d.text((W - MX - d.textlength(right, font=rf), 8), right, font=rf,
           fill=BLACK)
    d.rectangle([MX, 27, W - MX, 29], fill=RED)

    # ---- masthead: THE DATE ONLY, serif title case, natural width
    title = "Saturday 21 November 2026"
    size = 80
    while size > 70 and d.textlength(title, font=PF(size)) > CW - 40:
        size -= 2
    tf = PF(size)
    tw = d.textlength(title, font=tf)
    d.text(((W - tw) / 2, 36), title, font=tf, fill=BLACK)

    # ---- day-parts bar
    py = 108
    d.rectangle([MX, py, MX + 118, py + 54], fill=RED)
    for i, ln in enumerate(("THE DAY", "IN PARTS")):
        f = AB(13)
        d.text((MX + 59 - d.textlength(ln, font=f) / 2, py + 9 + i * 17),
               ln, font=f, fill=(255, 255, 255))
    segw = (CW - 124) / 5
    for i, (lab, head) in enumerate(DAYPARTS):
        sx = MX + 124 + i * segw
        if i:
            d.line([sx, py + 4, sx, py + 50], fill=RULE, width=1)
        d.text((sx + 8, py + 3), lab, font=AB(10), fill=RED)
        for j, ln in enumerate(wrap(d, head, AM(11), segw - 14)[:2]):
            d.text((sx + 8, py + 19 + j * 13), ln, font=AM(11), fill=INK)
    d.line([MX, py + 58, W - MX, py + 58], fill=RULE, width=1)

    # ---- three equal leads
    ly = 176
    lw = (CW - 16) / 3
    for i in range(3):
        draw_card(d, MX + i * (lw + 8), ly, lw, CARDS[i], lead=True)

    # ---- ten minis, 2 rows x 5
    mw = (CW - 32) / 5
    for r in range(2):
        for c in range(5):
            draw_card(d, MX + c * (mw + 8), 366 + r * 178, mw,
                      CARDS[3 + r * 5 + c])

    # ---- section headers
    hy = 728
    d.text((MX, hy), "WHERE IT HAPPENED", font=AB(13), fill=BLACK)
    hdr = "ALSO ON SATURDAY 21 NOVEMBER"
    d.text((430, hy), hdr, font=AB(13), fill=BLACK)
    d.line([MX, hy + 18, W - MX, hy + 18], fill=RULE, width=1)

    # ---- map (bottom-left, ~40% width)
    mapbox = (MX, 752, 414, 882)
    dots, proj = build_dotmap(mapbox)
    for (gx, gy) in dots:
        d.ellipse([gx - 1.8, gy - 1.8, gx + 1.8, gy + 1.8], fill=(186, 172, 138))
    for card in CARDS:
        px, py2 = proj(card[9][0], card[9][1])
        col = REGION_COLORS[card[2]]
        r = 8
        d.ellipse([px - r, py2 - r, px + r, py2 + r], fill=col,
                  outline=(255, 255, 255), width=1)
        t = str(card[0])
        f = AB(9)
        d.text((px - d.textlength(t, font=f) / 2, py2 - 5), t, font=f,
               fill=(255, 255, 255))
    # continent colour legend
    lx = MX
    ly2 = 888
    for key, lab in CONTINENTS:
        d.ellipse([lx, ly2 + 1, lx + 8, ly2 + 9], fill=REGION_COLORS[key])
        f = AB(9)
        d.text((lx + 11, ly2), lab, font=f, fill=INK)
        lx += 11 + d.textlength(lab, font=f) + 10

    # ---- briefs: 27 hard one-liners, 2 columns, pitch 10.5
    bx = [430, 722]
    bw = [284, 288]
    nf, lf2, tf2 = AB(10), AB(10), AM(10)
    for ci, chunk in enumerate((BRIEFS[:14], BRIEFS[14:])):
        yy = 752
        for (n, city, tail) in chunk:
            num = str(n)
            d.text((bx[ci], yy), num, font=nf, fill=RED)
            leadin = city + ":"
            x2 = bx[ci] + d.textlength(num, font=nf) + 4
            d.text((x2, yy), leadin, font=lf2, fill=BLACK)
            x3 = x2 + d.textlength(leadin, font=lf2) + 4
            tail = fit_text(d, tail, tf2, bx[ci] + bw[ci] - x3)
            d.text((x3, yy), tail, font=tf2, fill=INK)
            yy += 10.5

    # ---- DATE CHECK (climaxku two-section form + Unverified clause)
    dy = 910
    d.rectangle([MX, dy, W - MX, 984], outline=RED, width=2)
    d.rectangle([MX, dy, MX + 104, dy + 20], fill=RED)
    d.text((MX + 8, dy + 4), "DATE CHECK", font=AB(11), fill=(255, 255, 255))
    colw = 432
    d.text((MX + 116, dy + 4), "LEFT OUT \u2013 FRIDAY 20 NOVEMBER'S NEWS",
           font=AB(10), fill=RED)
    d.text((MX + 116 + colw + 16, dy + 4), "NOT YET HAPPENED \u2013 NOT SHOWN",
           font=AB(10), fill=RED)
    disc = ("Kyiv's three bridges hit (20 Nov) \u00b7 Cyclone Akvan's landfall "
            "at Gopalpur (20 Nov) \u00b7 COP31's final day, no deal (20 Nov) "
            "\u00b7 Asia's AI sell-off, Taipei -6.2% (20 Nov) \u00b7 UK-EU reset "
            "deal (20 Nov) \u00b7 Phillips's 118, first innings (20 Nov)")
    notyet = ("Any final COP31 text \u00b7 the ATP semi-final results \u00b7 "
              "BepiColombo's entry into orbit around Mercury (due today)")
    for j, ln in enumerate(wrap(d, disc, AM(10), colw - 8)[:3]):
        d.text((MX + 116, dy + 23 + j * 12), ln, font=AM(10), fill=INK)
    for j, ln in enumerate(wrap(d, notyet, AM(10), colw - 8)[:3]):
        d.text((MX + 116 + colw + 16, dy + 23 + j * 12), ln, font=AM(10),
               fill=INK)
    unv = ("Unverified: Denmark's assassination-plot claim is Denmark's "
           "account only \u2013 Russia's side is not in the reports, so it "
           "is shown as a claim, not as fact.")
    d.text((MX + 116, dy + 62), fit_text(d, unv, AM(10), CW - 124),
           font=AM(10), fill=INK)

    # ---- footer, one line
    foot = ("Every story here happened, or was first reported, on Saturday "
            "21 November 2026 \u00b7 Sources: AP \u00b7 BBC \u00b7 Reuters \u00b7 ICC "
            "\u00b7 SimpleLife \u00b7 AppiStos \u00b7 Ridhu Times \u00b7 Original drawings")
    ff = AM(9)
    foot = fit_text(d, foot, ff, CW)
    d.text((MX, 994), foot, font=ff, fill=GREY)
    return img


def _compressed(img):
    """Palette-quantize into the fleet's lean size range (deterministic)."""
    import io
    q = None
    for colors in (256, 192, 128, 96):
        q = img.quantize(colors=colors, method=Image.MEDIANCUT,
                         dither=Image.FLOYDSTEINBERG)
        buf = io.BytesIO()
        q.save(buf, format="PNG", optimize=True)
        if buf.tell() <= 170_000:
            return q
    return q


def main():
    img = render()
    _compressed(img).save(os.path.join(HERE, "entry.png"), optimize=True)
    img.resize((300, 300), Image.LANCZOS).save(
        os.path.join(HERE, "entry-300.png"), optimize=True)
    print("rendered entry.png + entry-300.png")


if __name__ == "__main__":
    main()
