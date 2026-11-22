"""NEWS TOWERS - Saturday 21 November 2026 in one page (1024x1024).

Three treatments are built and dueled:
  A - "DUSK TOWERS": deep-navy page, isometric 3D tower strips on every card.
  B - "FLAT WIRE":   cream broadsheet, flat 2D strips, no depth.
  C - "DAWN BLOCKS": slate/teal page, chunky perspective-block strips,
                     masthead and map rearranged.
The duel winner (see README) is written to entry.png; all three renders
are kept in variants/. Facts come only from POOL21 (verified pool):
EU ADOPTED EUR1bn in military aid - never "EUR8bn paid".
"""
import os
import sys

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from mapdata import WORLD  # noqa: E402

W = H = 1024

# ---------------------------------------------------------------- fonts
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


# ---------------------------------------------------------------- data
# n, place, region, headline, deck, tag, source, data label, (lon, lat)
CARDS = [
    (1, "WARSAW, POLAND", "EUROPE",
     "Rutte flies to Warsaw after missiles land",
     "Two missiles and a suspected jet drone came down in the south-east, "
     "a Kh-101 near Nowy Lipowiec. NATO's Rutte calls it a \"grave "
     "violation\"; Tusk calls it a deliberate provocation.",
     "AP - SOFX", "(AP)", "3 WEAPONS CROSS", (21.0, 52.2)),
    (2, "ANTALYA, TURKIYE", "GLOBAL",
     "COP31 runs into overtime with no deal yet",
     "Talks ran past Friday's scheduled close into Saturday. The draft "
     "drops every fossil-fuel reference and the $120bn finance target; "
     "a third draft is due this morning.",
     "Ongoing - AP", "(AP)", "NO DEAL YET", (30.7, 36.9)),
    (3, "NEW YORK", "AMERICAS",
     "Wall Street enters correction as AI rout deepens",
     "The S&P 500 fell about 3.7% on Friday, pushing it into correction "
     "territory. The Nasdaq dropped 5.28% as chip and AI shares plunged.",
     "Friday's close", "(SimpleLife)", "NASDAQ -5.28%", (-74.0, 40.7)),
    (4, "KRYVYI RIH", "EUROPE",
     "Russian strike kills two, injures 42",
     "An overnight strike on Kryvyi Rih kills two and injures 42, four "
     "of them children, the city's military chief says. It was one of "
     "Russia's largest attacks of the war.",
     "City chief says", "(AppiStos)", "2 DEAD - 42 HURT", (33.4, 47.9)),
    (5, "COPENHAGEN", "EUROPE",
     "Denmark exposes 'assassination plot'",
     "Russia 'planned and initiated' a bid to kill a Ukrainian-American "
     "rapper near Copenhagen, Denmark says. The Russian attache is "
     "expelled.",
     "Denmark says - BBC", "(BBC)", "ATTACHE EXPELLED", (12.6, 55.7)),
    (6, "KYIV", "EUROPE",
     "Russia's barrage: 400 drones, 110 missiles",
     "At least eight are dead across Ukraine in the overnight barrage. "
     "The Austrian embassy is hit in Kyiv, and France calls for a UN "
     "Security Council meeting.",
     "Officials' count", "(BBC)", "400 DRONES - 110 MISSILES", (30.5, 50.4)),
    (7, "ODISHA, INDIA", "ASIA",
     "After Akvan: 372,000 moved, no deaths",
     "A day after landfall, no deaths are reported and relief is under "
     "way. The storm weakens to a depression; schools stay shut through "
     "Saturday.",
     "Relief reports", "(Ridhu Times)", "372,000 MOVED", (84.9, 19.3)),
    (8, "BRUSSELS", "EUROPE",
     "EU adopts 1bn euro military aid for Ukraine",
     "Joint buying runs via the Peace Facility. Britain pledges 1,000+ "
     "drones in a 260m pound package alongside the EU deal.",
     "Adopted - EU", "(Reuters)", "EUR 1BN ADOPTED", (4.3, 50.8)),
    (9, "NEW YORK", "AMERICAS",
     "JPMorgan, Visa, Mastercard hit by cyberattack",
     "The banks report incidents at third-party vendors. Their core "
     "payment networks are unaffected, they say.",
     "Banks say", "(Reuters)", "3 NETWORKS HIT", (-73.9, 40.8)),
    (10, "ULAANBAATAR", "ASIA",
     "Mongolia's president resigns",
     "The resignation sets the stage for a snap election. It caps a "
     "week of political turmoil in the capital.",
     "Capital reports", "(Reuters)", "SNAP ELECTION NEXT", (106.9, 47.9)),
    (11, "THE HAGUE", "GLOBAL",
     "Myanmar ruling rattles Israel's Gaza defence",
     "The world court's genocide verdict against Myanmar raises "
     "questions in Jerusalem over its own case, experts say. The "
     "ruling itself came on Thursday.",
     "Experts say", "(BBC)", "GENOCIDE VERDICT", (4.3, 52.1)),
    (12, "JOHANNESBURG", "AFRICA",
     "ANC scrambles after worst result since 1994",
     "The ANC wins 31% of the vote, its worst since 1994. It now races "
     "for coalition deals to stay in government.",
     "Count - BBC", "(BBC)", "ANC 31%", (28.0, -26.2)),
    (13, "WELLINGTON", "OCEANIA",
     "India fight back: 159/1 at stumps, day two",
     "India trail New Zealand by 209 in the first Test after the hosts "
     "made 368. Nicholls made 175 not out for the hosts.",
     "Scorecard - ICC", "(ICC)", "159/1 - DAY TWO", (174.8, -41.3)),
]

# n, city, text, source, (lon, lat)
BRIEFS = [
    (14, "Kathmandu", "Nepal's new leader Balendra Shah faces an India test", "BBC", (85.3, 27.7)),
    (15, "Washington", "US releases more UFO footage filmed in the Middle East", "BBC", (-77.0, 38.9)),
    (16, "Los Angeles", "Hyundai unveils the 2027 Elantra at the auto show", "Fast Company", (-118.2, 34.1)),
    (17, "Cardiff", "Lauren Price beats Kotaskova to become undisputed champion", "BBC", (-3.2, 51.5)),
    (18, "Paris", "Three police are sentenced over the beating of Michel Zecler", "BBC", (2.4, 48.9)),
    (19, "Oxford", "Life, 22 years minimum, for the Thames drowning murder", "BBC", (-1.3, 51.8)),
    (20, "New York", "Nikhil Gupta gets 19+ years over the Sikh murder plot", "BBC", (-74.0, 40.7)),
    (21, "Cincinnati", "Fiona the hippo dies after eating a hat", "AP", (-84.5, 39.1)),
    (22, "Washington", "US sanctions four Iranians over oil revenues", "OFAC", (-77.1, 38.8)),
    (23, "Hormuz", "A tanker is struck and on fire in the Strait of Hormuz", "UKMTO", (56.3, 26.6)),
    (24, "Los Angeles", "A jury convicts the man who started the Palisades Fire", "AP", (-118.3, 34.0)),
    (25, "Frankfurt", "ECB names Boone and Brunnermeier for its Executive Board", "Reuters", (8.7, 50.1)),
    (26, "Buenos Aires", "Argentina's Senate backs a disability framework, 71-0", "AP", (-58.4, -34.6)),
    (27, "Riyadh", "A Saudi coalition intercepts Houthi missiles over Riyadh", "Reuters", (46.7, 24.6)),
    (28, "Barcelona", "A pill is hailed as a breakthrough for pancreatic cancer", "Reuters", (2.2, 41.4)),
    (29, "Gaza", "On World Children's Day, Palestinian children appeal for help", "UN", (34.3, 31.5)),
    (30, "Madrid", "Amnesty says Spanish police used excess force in the strike", "AP", (-3.7, 40.4)),
    (31, "Rome", "Italian workers and students march against Meloni's government", "AFP", (12.5, 41.9)),
    (32, "Jeddah", "Saudi Arabia warns of thunderstorms through Tuesday", "SPA", (39.2, 21.5)),
    (33, "Kuala Lumpur", "Malaysia to send 10,000 Rohingya to Turkey for training", "Reuters", (101.7, 3.1)),
    (34, "Kharkiv", "Ukraine says it has finished a \"Bear Trap\" in the Kharkiv area", "Ukrinform", (36.2, 49.9)),
    (35, "Islamabad", "Pakistan's minerals are worth $8-10 trillion, its minister says", "Reuters", (73.1, 33.7)),
    (36, "Singapore", "US presses Singapore and Malaysia on Iran sanctions", "Reuters", (103.8, 1.35)),
    (37, "Paris", "France seeks a UN council meeting on the Kyiv strikes", "AFP", (2.3, 48.8)),
    (38, "Kyiv", "The war tally: 771 Ukrainians killed, 2,300+ missing", "homevo", (30.6, 50.5)),
    (39, "Ankara", "Turkey welcomes the World Court's Myanmar ruling", "Anadolu", (32.9, 39.9)),
    (40, "Turin", "ATP semis are set: Alcaraz v Shelton, Zverev v Medvedev", "ATP", (7.7, 45.1)),
]

NUMBERS = [
    ("3", "WEAPONS CROSS INTO POLAND", 1),
    ("42", "INJURED AT KRYVYI RIH", 4),
    ("-5.28%", "NASDAQ, FRIDAY'S CLOSE", 3),
    ("372,000", "MOVED AS AKVAN HIT", 7),
    ("\u20ac1BN", "EU AID ADOPTED", 8),
    ("159/1", "INDIA AT STUMPS", 13),
]

TIMELINE = [
    ("OVERNIGHT", "Kryvyi Rih strike: 2 killed, 42 injured"),
    ("MORNING", "Rutte flies to Warsaw over the missiles"),
    ("MIDDAY", "Antalya: third COP31 draft due"),
    ("AFTERNOON", "Denmark expels the Russian attache"),
    ("EVENING", "Stumps in Wellington: India 159/1"),
]

DATE_CHECK = [
    "LEFT OUT - FIRST REPORTED FRIDAY 20 NOVEMBER:",
    "Kyiv's three bridges hit (20 Nov)",
    "Cyclone Akvan's landfall at Gopalpur (20 Nov)",
    "COP31's scheduled final day, no deal (20 Nov)",
    "Asia's AI sell-off - Taipei -6.2% (20 Nov)",
    "The UK-EU reset deal (20 Nov)",
    "Phillips's 118 in the first innings (20 Nov)",
    "NOT YET HAPPENED - NOT SHOWN:",
    "Any final COP31 text",
    "The ATP semi-final results",
    "BepiColombo's Mercury orbit entry (due today)",
]

REGION_LINE = "EUROPE 16 - ASIA 6 - AMERICAS 8 - MIDEAST 6 - AFRICA 1 - OCEANIA 1 - GLOBAL 2"

REGION_COLORS = {
    "EUROPE": (61, 142, 196),
    "GLOBAL": (150, 108, 199),
    "AMERICAS": (198, 84, 62),
    "ASIA": (64, 166, 120),
    "AFRICA": (217, 164, 65),
    "OCEANIA": (84, 178, 199),
}

HOOK = ("MISSILES LAND IN POLAND  ·  COP31 SLIPS INTO OVERTIME  ·  "
        "WALL STREET FALLS INTO CORRECTION")
FOOTER = ("Every story here happened, or was first reported, on Saturday "
          "21 November 2026. Contested claims are attributed.")
FOOTER2 = "Sources named beside each story - original drawings."


# ---------------------------------------------------------------- helpers
def wrap(d, text, font, maxw):
    words = text.split()
    lines, cur = [], ""
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


def fit_font(d, text, name, size, maxw, floor=10):
    while size > floor and d.textlength(text, font=F(name, size)) > maxw:
        size -= 1
    return F(name, size)


def shade(c, f):
    return tuple(max(0, min(255, int(v * f))) for v in c)


def draw_map(d, box, land, water, pin_colors=True):
    """Equirectangular world from real polygons in mapdata.WORLD."""
    x0, y0, x1, y1 = box
    d.rectangle(box, fill=water)
    for polys in WORLD.values():
        for poly in polys.split("|"):
            pts = []
            for pair in poly.split(","):
                lon, lat = pair.split(":")
                px = x0 + (float(lon) + 180) / 360.0 * (x1 - x0)
                py = y0 + (90 - float(lat)) / 180.0 * (y1 - y0)
                pts.append((px, py))
            if len(pts) > 2:
                d.polygon(pts, fill=land)
    return lambda lon, lat: (x0 + (lon + 180) / 360.0 * (x1 - x0),
                             y0 + (90 - lat) / 180.0 * (y1 - y0))


def pin(d, cx, cy, num, color, dark=(10, 14, 20)):
    r = 9  # Ø18px
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=color,
              outline=(255, 255, 255), width=2)
    t = str(num)
    f = AB(10)
    tw = d.textlength(t, font=f)
    d.text((cx - tw / 2, cy - 6), t, font=f, fill=(255, 255, 255))


def dot(d, cx, cy, color):
    d.ellipse([cx - 2.5, cy - 2.5, cx + 2.5, cy + 2.5], fill=color)


# ---------------------------------------------------------------- strips
def _windows(d, x, y, w, h, cols, rows, lit, seed):
    if w <= 2 or h <= 2:
        return
    rows = max(1, min(rows, int(h / 7)))
    cw, ch = w / cols, h / rows
    pad = 1.2 if ch > 5 else 0.4
    k = seed
    for r in range(rows):
        for c in range(cols):
            k = (k * 1103515245 + 12345) % (2 ** 31)
            if (k >> 8) % 100 < 46:
                d.rectangle([x + c * cw + pad, y + r * ch + pad,
                             x + (c + 1) * cw - pad, y + (r + 1) * ch - pad],
                            fill=lit)


def strip_iso(d, box, card, sky, ground):
    """A: isometric tower - front face, side face, roof; lit windows."""
    x0, y0, x1, y1 = box
    n, place, region = card[0], card[1], card[2]
    col = REGION_COLORS[region]
    d.rectangle(box, fill=sky)
    # backdrop towers (silhouettes, depth)
    for i, (bx, bh, bf) in enumerate([(0.06, 0.52, 0.55), (0.72, 0.66, 0.45),
                                      (0.86, 0.42, 0.65)]):
        bx0 = x0 + (x1 - x0) * bx
        bw = (x1 - x0) * 0.13
        d.rectangle([bx0, y1 - (y1 - y0) * bh, bx0 + bw, y1],
                    fill=shade(sky, 1.5 if bf < 0.6 else 1.25))
    d.rectangle([x0, y1 - 5, x1, y1], fill=ground)
    # hero tower, isometric: front (left), side (right, darker), roof
    tw = (x1 - x0) * 0.34
    tx = x0 + (x1 - x0) * 0.10
    ty = y0 + 4
    dep = min(tw * 0.42, (y1 - y0) * 0.42)
    front = shade(col, 0.95)
    side = shade(col, 0.55)
    roof = shade(col, 1.3)
    d.polygon([(tx, ty + dep * 0.5), (tx + tw, ty + dep * 0.5),
               (tx + tw + dep, ty), (tx + dep, ty)], fill=roof)
    d.rectangle([tx, ty + dep * 0.5, tx + tw, y1 - 5], fill=front)
    d.polygon([(tx + tw, ty + dep * 0.5), (tx + tw + dep, ty),
               (tx + tw + dep, y1 - 5 - dep * 0.5), (tx + tw, y1 - 5)],
              fill=side)
    _windows(d, tx + 3, ty + dep * 0.5 + 4, tw - 6, (y1 - 5) - ty - dep * 0.5 - 7,
             4, 3, (255, 226, 138), n * 7 + 3)
    _windows(d, tx + tw + 3, ty + 3, dep - 5, (y1 - 5 - dep * 0.5) - ty - 6,
             2, 3, (214, 190, 110), n * 13 + 5)
    # antenna + beacon
    ax = tx + tw * 0.5
    d.line([ax, ty + dep * 0.5, ax, ty - 1], fill=(230, 230, 230), width=2)
    d.ellipse([ax - 2, ty - 3, ax + 2, ty + 1], fill=(255, 80, 70))


def strip_flat(d, box, card, sky, ground):
    """B: flat 2D tower - single face, no depth, flat windows."""
    x0, y0, x1, y1 = box
    n, region = card[0], card[2]
    col = REGION_COLORS[region]
    d.rectangle(box, fill=sky)
    for bx, bh in [(0.05, 0.45), (0.78, 0.6), (0.9, 0.38)]:
        bx0 = x0 + (x1 - x0) * bx
        d.rectangle([bx0, y1 - (y1 - y0) * bh, bx0 + (x1 - x0) * 0.11, y1],
                    fill=shade(sky, 1.18))
    d.rectangle([x0, y1 - 5, x1, y1], fill=ground)
    tw = (x1 - x0) * 0.36
    tx = x0 + (x1 - x0) * 0.10
    d.rectangle([tx, y0 + 5, tx + tw, y1 - 5], fill=col)
    _windows(d, tx + 3, y0 + 9, tw - 6, (y1 - 5) - y0 - 13, 4, 3,
             (255, 240, 190), n * 7 + 3)


def strip_block(d, box, card, sky, ground):
    """C: chunky perspective block - steep side, offset roof slab."""
    x0, y0, x1, y1 = box
    n, region = card[0], card[2]
    col = REGION_COLORS[region]
    d.rectangle(box, fill=sky)
    for bx, bh in [(0.7, 0.5), (0.86, 0.7)]:
        bx0 = x0 + (x1 - x0) * bx
        d.rectangle([bx0, y1 - (y1 - y0) * bh, bx0 + (x1 - x0) * 0.12, y1],
                    fill=shade(sky, 1.3))
    d.rectangle([x0, y1 - 5, x1, y1], fill=ground)
    tw = (x1 - x0) * 0.4
    tx = x0 + (x1 - x0) * 0.08
    ty = y0 + 7
    off = tw * 0.30
    d.polygon([(tx, ty), (tx + tw, ty), (tx + tw + off, ty - 5),
               (tx + off, ty - 5)], fill=shade(col, 1.35))
    d.rectangle([tx, ty, tx + tw, y1 - 5], fill=shade(col, 1.02))
    d.polygon([(tx + tw, ty), (tx + tw + off, ty - 5), (tx + tw + off, y1 - 10),
               (tx + tw, y1 - 5)], fill=shade(col, 0.5))
    _windows(d, tx + 3, ty + 4, tw - 6, (y1 - 5) - ty - 7, 5, 3,
             (190, 245, 235), n * 11 + 7)


STRIP_STYLE = {"A": strip_iso, "B": strip_flat, "C": strip_block}


def draw_card(d, box, card, theme, variant):
    x0, y0, x1, y1 = box
    n, place, region, head, deck, tag, src, label, ll = card
    col = REGION_COLORS[region]
    d.rectangle(box, fill=theme["card"], outline=theme["line"], width=1)
    # strip (top 40% of card)
    sh = int((y1 - y0) * 0.40)
    STRIP_STYLE[variant](d, (x0 + 1, y0 + 1, x1 - 1, y0 + sh), card,
                         theme["sky"], theme["ground"])
    # caption band inside strip bottom: PLACE - DATA LABEL
    band_y = y0 + sh - 15
    d.rectangle([x0 + 1, band_y, x1 - 1, y0 + sh], fill=(14, 24, 38))
    cap = place + "  ·  " + label
    cf = fit_font(d, cap, "Archivo-Bold.ttf", 10, x1 - x0 - 8, 8)
    d.text((x0 + 5, band_y + 3), cap, font=cf, fill=(240, 240, 235))
    # source/certainty tag, top-right over strip
    tf = AB(9)
    tw_ = d.textlength(tag.upper(), font=tf)
    d.rectangle([x1 - tw_ - 9, y0 + 4, x1 - 3, y0 + 17], fill=(14, 24, 38))
    d.text((x1 - tw_ - 6, y0 + 6), tag.upper(), font=tf, fill=(255, 214, 90))
    # headline
    hy = y0 + sh + 5
    hf = AB(14) if (y1 - y0) > 150 else AB(13)
    for ln in wrap(d, head, hf, x1 - x0 - 10)[:2]:
        d.text((x0 + 5, hy), ln, font=hf, fill=theme["head"])
        hy += 16
    # deck (>=2 facts, Archivo Medium 12)
    df = AM(12)
    for ln in wrap(d, deck, df, x1 - x0 - 10)[:4]:
        d.text((x0 + 5, hy + 1), ln, font=df, fill=theme["deck"])
        hy += 14.5
    # source line at card foot
    d.text((x0 + 5, y1 - 14), src, font=AB(9), fill=shade(col, 1.05))


def numbers_row(d, box, theme):
    x0, y0, x1, y1 = box
    d.rectangle(box, fill=theme["band"], outline=theme["line"])
    cw = (x1 - x0) / 6
    for i, (num, lab, cardn) in enumerate(NUMBERS):
        cx = x0 + i * cw
        if i:
            d.line([cx, y0 + 5, cx, y1 - 5], fill=theme["line"], width=1)
        nf = fit_font(d, num, "PlayfairDisplay-900.ttf", 25, cw - 10, 12)
        d.text((cx + 7, y0 + 3), num, font=nf, fill=theme["accent"])
        lf = fit_font(d, lab, "Archivo-Bold.ttf", 9, cw - 10, 7)
        d.text((cx + 7, y0 + 31), lab, font=lf, fill=theme["bandtxt"])
        d.text((cx + 7, y0 + 43), "CARD %d" % cardn, font=AB(8),
               fill=theme["bandtxt"])


def timeline_row(d, box, theme):
    x0, y0, x1, y1 = box
    d.rectangle(box, fill=theme["band"], outline=theme["line"])
    cw = (x1 - x0) / 5
    d.line([x0 + 8, y0 + 13, x1 - 8, y0 + 13], fill=theme["accent"], width=2)
    for i, (slot, ev) in enumerate(TIMELINE):
        cx = x0 + i * cw
        d.ellipse([cx + 8, y0 + 9, cx + 16, y0 + 17], fill=theme["accent"])
        d.text((cx + 20, y0 + 5), slot, font=AB(10), fill=theme["bandtxt"])
        ef = AM(10)
        yy = y0 + 22
        for ln in wrap(d, ev, ef, cw - 12)[:2]:
            d.text((cx + 8, yy), ln, font=ef, fill=theme["bandtxt"])
            yy += 12


def briefs_block(d, box, theme, two_col=False):
    x0, y0, x1, y1 = box
    d.text((x0, y0), "ALSO ON THE PAGE - 27 BRIEFS", font=AB(11),
           fill=theme["head"])
    yy = y0 + 17
    bf = AM(10)
    for (n, city, text, src, ll) in BRIEFS:
        line = "%d. %s - %s (%s)" % (n, city, text, src)
        f = fit_font(d, line, "Archivo-Medium.ttf", 10, x1 - x0 - 2, 8)
        d.text((x0, yy), line, font=f, fill=theme["deck"])
        yy += 11.6
    return yy


def date_check_block(d, box, theme):
    """Two-column DATE CHECK: dated discards left, not-yet right."""
    x0, y0, x1, y1 = box
    d.rectangle(box, outline=(198, 60, 50), width=2)
    d.rectangle([x0, y0, x1, y0 + 18], fill=(198, 60, 50))
    d.text((x0 + 6, y0 + 4), "DATE CHECK - NOT SATURDAY'S NEWS",
           font=AB(10), fill=(255, 255, 255))
    mid = (x0 + x1) / 2
    for cx, items in ((x0, DATE_CHECK[:7]), (mid + 4, DATE_CHECK[7:])):
        yy = y0 + 23
        for ln in items:
            if ln.endswith(":"):
                f, fill = AB(9), theme["head"]
            else:
                f, fill = AM(10), theme["deck"]
            for wln in wrap(d, ln, f, (x1 - x0) / 2 - 12):
                d.text((cx + 5, yy), wln, font=f, fill=fill)
                yy += 11


def map_panel(d, box, theme, legend_fill):
    x0, y0, x1, y1 = box
    d.text((x0, y0), "WHERE IT HAPPENED", font=AB(11), fill=theme["head"])
    proj = draw_map(d, (x0, y0 + 16, x1, y1 - 26), theme["land"],
                    theme["water"])
    for b in BRIEFS:
        px, py = proj(b[4][0], b[4][1])
        dot(d, px, py, (240, 200, 90))
    for c in CARDS:
        px, py = proj(c[8][0], c[8][1])
        pin(d, px, py, c[0], REGION_COLORS[c[2]])
    lf = fit_font(d, "Numbered pins = the 13 pictured cards. Small dots "
                  "= the 27 briefs.", "Archivo-Medium.ttf", 9, x1 - x0, 7)
    d.text((x0, y1 - 22),
           "Numbered pins = the 13 pictured cards. Small dots = the 27 "
           "briefs.", font=lf, fill=legend_fill)
    rf = fit_font(d, REGION_LINE, "Archivo-Bold.ttf", 8, x1 - x0, 7)
    d.text((x0, y1 - 11), REGION_LINE, font=rf, fill=legend_fill)


# ---------------------------------------------------------------- themes
THEMES = {
    "A": dict(bg=(9, 17, 29), card=(17, 29, 45), line=(52, 74, 102),
              head=(245, 242, 230), deck=(205, 214, 226),
              band=(13, 26, 42), bandtxt=(220, 228, 238),
              accent=(240, 193, 75), sky=(26, 46, 70), ground=(8, 14, 22),
              land=(56, 84, 64), water=(18, 34, 54),
              hook=(176, 44, 36), legend=(190, 200, 214)),
    "B": dict(bg=(243, 238, 226), card=(250, 247, 238), line=(60, 55, 48),
              head=(20, 18, 16), deck=(52, 48, 44),
              band=(238, 232, 216), bandtxt=(30, 28, 26),
              accent=(176, 44, 36), sky=(216, 207, 184), ground=(122, 112, 96),
              land=(168, 158, 128), water=(198, 208, 208),
              hook=(176, 44, 36), legend=(70, 64, 56)),
    "C": dict(bg=(13, 30, 34), card=(20, 44, 48), line=(46, 92, 96),
              head=(238, 246, 242), deck=(196, 220, 214),
              band=(10, 26, 30), bandtxt=(210, 232, 226),
              accent=(94, 209, 196), sky=(24, 54, 58), ground=(8, 20, 22),
              land=(48, 88, 76), water=(16, 38, 44),
              hook=(12, 84, 80), legend=(190, 214, 206)),
}


def draw_card2(d, box, card, theme, variant, strip_h, lead=False):
    x0, y0, x1, y1 = box
    n, place, region, head, deck, tag, src, label, ll = card
    col = REGION_COLORS[region]
    d.rectangle(box, fill=theme["card"], outline=theme["line"], width=1)
    STRIP_STYLE[variant](d, (x0 + 1, y0 + 1, x1 - 1, y0 + strip_h), card,
                         theme["sky"], theme["ground"])
    band_y = y0 + strip_h - 15
    d.rectangle([x0 + 1, band_y, x1 - 1, y0 + strip_h], fill=(14, 24, 38))
    cap = place + "  ·  " + label
    cf = fit_font(d, cap, "Archivo-Bold.ttf", 10, x1 - x0 - 46, 8)
    d.text((x0 + 5, band_y + 3), cap, font=cf, fill=(240, 240, 235))
    sf = AB(9)
    sw = d.textlength(src, font=sf)
    d.text((x1 - sw - 5, band_y + 3), src, font=sf, fill=(255, 214, 90))
    tf = AB(9)
    tw_ = d.textlength(tag.upper(), font=tf)
    d.rectangle([x1 - tw_ - 9, y0 + 4, x1 - 3, y0 + 17], fill=(14, 24, 38))
    d.text((x1 - tw_ - 6, y0 + 6), tag.upper(), font=tf, fill=(255, 214, 90))
    hy = y0 + strip_h + 5
    hf = AB(15) if lead else AB(13)
    step = 17 if lead else 14
    for ln in wrap(d, head, hf, x1 - x0 - 10)[:2]:
        d.text((x0 + 5, hy), ln, font=hf, fill=theme["head"])
        hy += step
    df = AM(12)
    maxl = 3 if lead else 4
    for ln in wrap(d, deck, df, x1 - x0 - 10)[:maxl]:
        d.text((x0 + 5, hy + 1), ln, font=df, fill=theme["deck"])
        hy += 13


def timeline_compact(d, box, theme):
    x0, y0, x1, y1 = box
    d.rectangle(box, fill=theme["band"], outline=theme["line"])
    cw = (x1 - x0) / 5
    d.line([x0 + 10, y0 + 10, x1 - 10, y0 + 10], fill=theme["accent"],
           width=2)
    shorts = ["Kryvyi Rih: 2 dead, 42 hurt", "Rutte flies to Warsaw",
              "Antalya: 3rd COP31 draft due", "Denmark expels attache",
              "Wellington: India 159/1"]
    for i, (slot, ev) in enumerate(TIMELINE):
        cx = x0 + i * cw
        d.ellipse([cx + 8, y0 + 6, cx + 15, y0 + 13], fill=theme["accent"])
        d.text((cx + 19, y0 + 3), slot, font=AB(10), fill=theme["bandtxt"])
        f = fit_font(d, shorts[i], "Archivo-Medium.ttf", 10, cw - 12, 8)
        d.text((cx + 8, y0 + 19), shorts[i], font=f, fill=theme["bandtxt"])


def briefs_col(d, box, items, theme):
    x0, y0, x1, y1 = box
    yy = y0
    for (n, city, text, src, ll) in items:
        line = "%d. %s - %s (%s)" % (n, city, text, src)
        f = AM(10)
        for ln in wrap(d, line, f, x1 - x0 - 2)[:2]:
            d.text((x0, yy), ln, font=f, fill=theme["deck"])
            yy += 10.6
    return yy


def bottom_zone(d, y0, theme, variant):
    # col1: map + footer (narrower, so brief columns get one-line width)
    map_panel(d, (8, y0, 300, y0 + 222), theme, theme["legend"])
    fy = y0 + 230
    for ln in wrap(d, FOOTER, AM(9), 292):
        d.text((8, fy), ln, font=AM(9), fill=theme["legend"])
        fy += 11
    d.text((8, fy + 1), FOOTER2, font=AM(9), fill=theme["legend"])
    # briefs header + three columns (9 each - keeps every brief >=10px
    # and inside the zone; two columns overflowed into DATE CHECK)
    d.text((308, y0), "ALSO ON THE PAGE - 27 BRIEFS", font=AB(11),
           fill=theme["head"])
    briefs_col(d, (308, y0 + 16, 540, 1020), BRIEFS[:9], theme)
    briefs_col(d, (548, y0 + 16, 780, 1020), BRIEFS[9:18], theme)
    briefs_col(d, (788, y0 + 16, 1016, 1020), BRIEFS[18:], theme)
    date_check_block(d, (308, y0 + 214, 1016, 1020), theme)


def masthead(d, theme, variant):
    if variant == "B":
        t = "NEWS TOWERS"
        f = fit_font(d, t, "PlayfairDisplay-900.ttf", 54, 700)
        tw = d.textlength(t, font=f)
        d.text(((1024 - tw) / 2, 2), t, font=f, fill=theme["head"])
        d.line([8, 58, 1016, 58], fill=theme["head"], width=3)
        d.line([8, 62, 1016, 62], fill=theme["head"], width=1)
        d.text((8, 40), "SATURDAY 21 NOVEMBER 2026", font=AB(11),
               fill=theme["head"])
        k = "40 STORIES - 7 REGIONS"
        d.text((1016 - d.textlength(k, font=AB(11)), 40), k, font=AB(11),
               fill=theme["head"])
    elif variant == "C":
        t = "NEWS TOWERS"
        f = fit_font(d, t, "PlayfairDisplay-900.ttf", 50, 700)
        tw = d.textlength(t, font=f)
        d.text(((1024 - tw) / 2, 0), t, font=f, fill=theme["accent"])
        s = "SATURDAY 21 NOVEMBER 2026  ·  40 STORIES - 7 REGIONS"
        sf = AB(10)
        d.text(((1024 - d.textlength(s, font=sf)) / 2, 56), s, font=sf,
               fill=theme["head"])
    else:
        t = "NEWS TOWERS"
        f = fit_font(d, t, "PlayfairDisplay-900.ttf", 58, 640)
        d.text((8, 0), t, font=f, fill=theme["head"])
        d.text((700, 8), "SATURDAY 21 NOVEMBER 2026", font=AB(13),
               fill=theme["head"])
        d.text((700, 28), "40 STORIES - 7 REGIONS", font=AB(11),
               fill=theme["accent"])
        d.text((700, 44), "EVERY ONE DATED SATURDAY", font=AM(10),
               fill=theme["deck"])


def render(variant):
    theme = THEMES[variant]
    img = Image.new("RGB", (W, H), theme["bg"])
    d = ImageDraw.Draw(img)
    masthead(d, theme, variant)
    # deck line
    deck = ("Missiles land in Poland - COP31 slips into overtime - "
            "Wall Street falls into correction - Denmark exposes a plot")
    df = fit_font(d, deck, "Archivo-Medium.ttf", 12, 1008, 10)
    d.text((8, 68), deck, font=df, fill=theme["accent"])
    # hook band
    d.rectangle([8, 86, 1016, 110], fill=theme["hook"])
    hf = fit_font(d, HOOK, "Archivo-Bold.ttf", 13, 990, 10)
    hw = d.textlength(HOOK, font=hf)
    d.text(((1024 - hw) / 2, 92), HOOK, font=hf, fill=(255, 255, 255))
    # numbers + timeline
    numbers_row(d, (8, 114, 1016, 166), theme)
    timeline_compact(d, (8, 170, 1016, 204), theme)
    # cards
    if variant == "C":
        # full-width horizontal lead card
        c = CARDS[0]
        box = (8, 208, 1016, 304)
        d.rectangle(box, fill=theme["card"], outline=theme["line"])
        STRIP_STYLE["C"](d, (9, 209, 330, 303), c, theme["sky"],
                          theme["ground"])
        d.rectangle([9, 288, 330, 303], fill=(14, 24, 38))
        d.text((13, 291), c[1] + "  ·  " + c[7], font=AB(10),
               fill=(240, 240, 235))
        hy = 216
        for ln in wrap(d, c[3], AB(17), 660)[:2]:
            d.text((342, hy), ln, font=AB(17), fill=theme["head"])
            hy += 20
        for ln in wrap(d, c[4], AM(12), 660)[:3]:
            d.text((342, hy + 2), ln, font=AM(12), fill=theme["deck"])
            hy += 14.5
        d.text((342, 284), c[5].upper() + "  " + c[6], font=AB(10),
               fill=theme["accent"])
        rest = CARDS[1:]
        rows = [(308, 426), (430, 548), (552, 670)]
        idx = 0
        for (ry0, ry1) in rows:
            for k in range(4):
                if idx >= len(rest):
                    break
                cx0 = 8 + k * 253
                draw_card2(d, (cx0, ry0, cx0 + 245, ry1), rest[idx],
                           theme, variant, 32)
                idx += 1
        bottom_zone(d, 678, theme, variant)
    else:
        draw_card2(d, (8, 208, 508, 326), CARDS[0], theme, variant, 42,
                   lead=True)
        draw_card2(d, (516, 208, 1016, 326), CARDS[1], theme, variant, 42,
                   lead=True)
        rest = CARDS[2:]
        rows = [(330, 448), (452, 570), (574, 692)]
        idx = 0
        for (ry0, ry1) in rows:
            for k in range(4):
                if idx >= len(rest):
                    break
                cx0 = 8 + k * 253
                draw_card2(d, (cx0, ry0, cx0 + 245, ry1), rest[idx],
                           theme, variant, 32)
                idx += 1
        bottom_zone(d, 700, theme, variant)
    return img


WINNER = "A"


def _compressed(img):
    """Palette-quantize to the 100-160 KB tie-break window (deterministic)."""
    import io
    for colors in (256, 192, 128, 96, 64):
        q = img.quantize(colors=colors, method=Image.MEDIANCUT,
                         dither=Image.FLOYDSTEINBERG)
        buf = io.BytesIO()
        q.save(buf, format="PNG", optimize=True)
        if buf.tell() <= 160_000:
            return q
    return q


def main():
    os.makedirs(os.path.join(HERE, "variants"), exist_ok=True)
    for v in ("A", "B", "C"):
        render(v).save(os.path.join(HERE, "variants",
                                    "variant-%s.png" % v))
    _compressed(render(WINNER)).save(os.path.join(HERE, "entry.png"),
                                     optimize=True)
    print("winner:", WINNER)


if __name__ == "__main__":
    main()
