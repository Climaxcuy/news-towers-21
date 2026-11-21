# main.py — NEWS TOWERS (variant H, news-image-20261121).
# Composites the final 1024x1024 page: a Pillow dusk sky + masthead, the
# Three.js city render (scene.png, made by shoot.mjs) with a razor-sharp
# Pillow headline panel bolted onto each hero tower, then the numbers strip,
# the UTC timeline, the street-level briefs band, the DATE CHECK box and the
# footer. Writes /output/entry.png (and refreshes the committed entry.png).
# Deterministic, no network. If the scene assets are missing it falls back
# to copying the committed entry.png, so the entry contract always holds.

import json
import math
import os
import random
import shutil
import sys

from PIL import Image, ImageDraw, ImageFilter, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import stories as S

ASSETS = os.path.join(HERE, "..", "..", "makefun-news-image-20all", "assets")
FONTS = os.path.join(ASSETS, "fonts")
W = H = 1024
BAND_Y = 118            # city band top on the page
BAND_H = 522            # city band height (scene is rendered at 2x)

CREAM = (253, 246, 227)
PAPER = (248, 242, 223)
INK = (23, 18, 8)
FACT = (58, 52, 40)
GOLD = (255, 179, 71)
DIM = (184, 168, 136)
DARK = (12, 9, 24)


def font(name, size):
    return ImageFont.truetype(os.path.join(FONTS, name), int(size))


F = {
    "kicker": font("Archivo-Bold.ttf", 12),
    "date": font("PlayfairDisplay-900.ttf", 57),
    "deck": font("Archivo-Medium.ttf", 13),
    "kick2": font("Archivo-Bold.ttf", 10),
    "p_num": font("Archivo-Bold.ttf", 11),
    "p_place": font("Archivo-Bold.ttf", 11),
    "p_head": font("Archivo-Bold.ttf", 15),
    "p_fact": font("Archivo-Medium.ttf", 11),
    "p_fact_s": font("Archivo-Medium.ttf", 10),
    "p_data": font("Archivo-Bold.ttf", 10),
    "p_tag": font("Archivo-Bold.ttf", 9),
    "num_big": font("Archivo-Bold.ttf", 21),
    "num_cap": font("Archivo-Medium.ttf", 9),
    "tl_lab": font("Archivo-Bold.ttf", 10),
    "tl_txt": font("Archivo-Medium.ttf", 10),
    "br_head": font("Archivo-Bold.ttf", 12),
    "br_reg": font("Archivo-Medium.ttf", 9),
    "br_num": font("Archivo-Bold.ttf", 10),
    "br_txt": font("Archivo-Medium.ttf", 10),
    "dc": font("Archivo-Medium.ttf", 9),
    "dc_lab": font("Archivo-Bold.ttf", 10),
    "foot": font("Archivo-Medium.ttf", 9),
}


def wrap(draw, text, fnt, maxw):
    """Greedy word wrap by pixel width."""
    words, lines, cur = text.split(), [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= maxw or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def tracked(draw, xy, text, fnt, fill, tracking=2):
    """Draw text with letter tracking; returns the end x."""
    x, y = xy
    for ch in text:
        draw.text((x, y), ch, font=fnt, fill=fill)
        x += draw.textlength(ch, font=fnt) + tracking
    return x


def vgrad(w, h, stops):
    """Vertical gradient from (y, color) stops."""
    strip = Image.new("RGB", (1, h))
    px = strip.load()
    for y in range(h):
        for i in range(len(stops) - 1):
            y0, c0 = stops[i]
            y1, c1 = stops[i + 1]
            if y0 <= y <= y1:
                t = 0 if y1 == y0 else (y - y0) / (y1 - y0)
                px[0, y] = tuple(int(c0[k] + (c1[k] - c0[k]) * t) for k in range(3))
                break
        else:
            px[0, y] = stops[-1][1]
    return strip.resize((w, h))


def radial_glow(size, color, peak=200):
    """Small radial-gradient sprite (bright centre fading out)."""
    s = 60
    img = Image.new("RGBA", (s, s), (0, 0, 0, 0))
    px = img.load()
    for yy in range(s):
        for xx in range(s):
            d = math.hypot(xx - s / 2, yy - s / 2) / (s / 2)
            a = max(0.0, 1.0 - d) ** 1.8
            px[xx, yy] = (color[0], color[1], color[2], int(peak * a))
    return img.resize((size, size), Image.BILINEAR)


def dotted_world(base, x0, y0, w, h):
    """Faint dotted world map (from the shared mapdata polygons) in the sky."""
    sys.path.insert(0, ASSETS)
    import mapdata_literal
    mask = Image.new("L", (w, h), 0)
    md = ImageDraw.Draw(mask)
    for rings in mapdata_literal.WORLD.values():
        for ring in rings.split("|"):
            pts = []
            for pair in ring.split(","):
                lon, lat = pair.split(":")
                mx = (float(lon) + 180) / 360 * w
                my = (85 - float(lat)) / 145 * h
                pts.append((mx, my))
            if len(pts) > 2:
                md.polygon(pts, fill=255)
    px = mask.load()
    dots = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    dd = ImageDraw.Draw(dots)
    for gy in range(0, h, 3):
        for gx in range(0, w, 3):
            if px[gx, gy] > 0:
                dd.ellipse([x0 + gx - 1, y0 + gy - 1, x0 + gx + 1, y0 + gy + 1],
                           fill=(255, 214, 150, 88))
    base.alpha_composite(dots)


def sky():
    img = vgrad(W, H, [
        (0, (6, 8, 24)), (150, (19, 16, 56)), (300, (51, 32, 92)),
        (430, (107, 50, 96)), (520, (179, 90, 65)), (600, (224, 138, 76)),
        (700, (24, 16, 44)), (1024, (10, 8, 22)),
    ]).convert("RGBA")
    # low sun glow behind the skyline
    glow = radial_glow(430, (255, 150, 70), peak=150)
    img.alpha_composite(glow, (770 - 215, 415 - 215))
    sun = radial_glow(120, (255, 196, 110), peak=235)
    img.alpha_composite(sun, (770 - 60, 415 - 60))
    # stars
    rng = random.Random(7)
    st = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    sd = ImageDraw.Draw(st)
    for _ in range(210):
        x, y = rng.uniform(0, W), rng.uniform(0, 290)
        r = rng.choice([1, 1, 1, 2])
        sd.ellipse([x - r, y - r, x + r, y + r],
                   fill=(255, 244, 214, rng.randint(36, 150)))
    img.alpha_composite(st)
    dotted_world(img, 800, 26, 212, 96)
    return img


def masthead(img):
    d = ImageDraw.Draw(img)
    tracked(d, (28, 14), "NEWS TOWERS - THE DAY AS A CITY - A 3D NEWS DIORAMA",
            F["kicker"], (255, 226, 160), tracking=2)
    d.text((28, 30), "Saturday 21 November 2026", font=F["date"], fill=CREAM)
    d.text((28, 96), S.MASTHEAD_DECK, font=F["deck"], fill=(232, 217, 176))
    d.rectangle([28, 114, 996, 116], fill=GOLD)


def panel(img, card, cx, top, pw):
    """One headline panel bolted onto a tower's front face.

    Layout: region-coloured top bar; kicker row with number chip and
    PLACE - REGION; headline; the two facts; a bottom row with the data
    chip. The source/certainty tag is placed by a fallback chain — full
    tag in the kicker, shortened tag in the kicker, full tag beside the
    data chip, shortened tag beside the data chip, else a second kicker
    line — so attribution is never dropped and never collides.
    """
    d = ImageDraw.Draw(img)
    inner = pw - 18
    col = S.REGION_COLORS[card["region"]]
    head_lines = wrap(d, card["headline"], F["p_head"], inner)
    fact_font, fact_lh = F["p_fact"], 14
    fact_lines = [wrap(d, f, fact_font, inner) for f in card["facts"]]
    total_fact = sum(len(x) for x in fact_lines)
    if total_fact > 5:
        fact_font, fact_lh = F["p_fact_s"], 13
        fact_lines = [wrap(d, f, fact_font, inner) for f in card["facts"]]
        total_fact = sum(len(x) for x in fact_lines)
    # --- tag placement chain ---
    place_str = card["place"] + " · " + card["region"]
    place_w = d.textlength(place_str, font=F["p_place"])
    tag_full, tag_short = card["tag"], card["tag"].split(" - ")[0]
    chip_w = d.textlength(card["data"], font=F["p_data"]) + 12
    kick_avail = inner - 22 - place_w          # room right of place in kicker
    data_avail = inner - chip_w - 6            # room right of the data chip
    tag_where, tag_text = None, tag_short
    for where, txt in (("kicker", tag_full), ("kicker", tag_short),
                       ("data", tag_full), ("data", tag_short)):
        avail = kick_avail if where == "kicker" else data_avail
        if d.textlength(txt, font=F["p_tag"]) <= avail:
            tag_where, tag_text = where, txt
            break
    if tag_where is None:
        tag_where = "line2"
    extra = 12 if tag_where == "line2" else 0
    ph = 7 + 15 + extra + 3 + len(head_lines) * 18 + 3 + total_fact * fact_lh + 4 + 15 + 7
    x0, y0 = int(cx - pw / 2), int(top)
    x1, y1 = x0 + pw, y0 + ph
    # soft shadow
    sh = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ImageDraw.Draw(sh).rounded_rectangle([x0 + 3, y0 + 5, x1 + 3, y1 + 5],
                                         radius=8, fill=(0, 0, 0, 120))
    img.alpha_composite(sh.filter(ImageFilter.GaussianBlur(3)))
    d = ImageDraw.Draw(img)
    d.rounded_rectangle([x0, y0, x1, y1], radius=8, fill=col)
    d.rounded_rectangle([x0, y0 + 5, x1, y1], radius=8, fill=PAPER)
    d.rectangle([x0, y0 + 5, x1, y0 + 9], fill=PAPER)
    # kicker row: number chip + place - region [+ tag]
    cy = y0 + 7
    d.rounded_rectangle([x0 + 9, cy, x0 + 26, cy + 15], radius=3, fill=col)
    nw = d.textlength(str(card["n"]), font=F["p_num"])
    d.text((x0 + 17.5 - nw / 2, cy + 2), str(card["n"]), font=F["p_num"],
           fill=(255, 255, 255))
    d.text((x0 + 31, cy + 2), place_str, font=F["p_place"], fill=col)
    if tag_where == "kicker":
        tw = d.textlength(tag_text, font=F["p_tag"])
        d.text((x1 - 9 - tw, cy + 3), tag_text, font=F["p_tag"], fill=(107, 98, 82))
    elif tag_where == "line2":
        d.text((x0 + 31, cy + 14), tag_text, font=F["p_tag"], fill=(107, 98, 82))
    # headline
    hy = cy + 18 + extra
    for ln in head_lines:
        d.text((x0 + 9, hy), ln, font=F["p_head"], fill=INK)
        hy += 18
    hy += 3
    for lines in fact_lines:
        for ln in lines:
            d.text((x0 + 9, hy), ln, font=fact_font, fill=FACT)
            hy += fact_lh
    # data row: data chip [+ tag]
    dy = y1 - 22
    d.rounded_rectangle([x0 + 9, dy, x0 + 9 + chip_w, dy + 15], radius=3, fill=(23, 17, 38))
    d.text((x0 + 15, dy + 2.5), card["data"], font=F["p_data"], fill=GOLD)
    if tag_where == "data":
        tw = d.textlength(tag_text, font=F["p_tag"])
        d.text((x1 - 9 - tw, dy + 3), tag_text, font=F["p_tag"], fill=(107, 98, 82))
    return ph


def numbers_strip(img):
    d = ImageDraw.Draw(img)
    d.rectangle([0, 640, W, 676], fill=(12, 9, 24))
    d.rectangle([0, 640, W, 641], fill=GOLD)
    cw = W / 6
    for i, (big, cap, n) in enumerate(S.NUMBERS):
        x = i * cw + 12
        d.text((x, 643), big, font=F["num_big"], fill=GOLD)
        bw = d.textlength(big, font=F["num_big"])
        d.text((x + bw + 5, 652), f"(#{n})", font=F["p_data"], fill=(150, 132, 96))
        d.text((x, 665), cap, font=F["num_cap"], fill=(216, 205, 178))
        if i:
            d.line([i * cw, 646, i * cw, 670], fill=(42, 33, 64))


def timeline_strip(img):
    d = ImageDraw.Draw(img)
    d.rectangle([0, 676, W, 714], fill=(18, 13, 36))
    cw = W / 5
    for i, (lab, txt) in enumerate(S.TIMELINE):
        x = i * cw + 12
        tracked(d, (x, 680), lab, F["tl_lab"], GOLD, tracking=1)
        for j, ln in enumerate(wrap(d, txt, F["tl_txt"], cw - 22)[:2]):
            d.text((x, 693 + j * 12), ln, font=F["tl_txt"], fill=(226, 216, 192))
        if i:
            d.line([i * cw, 680, i * cw, 710], fill=(42, 33, 64))


def briefs(img):
    d = ImageDraw.Draw(img)
    d.rectangle([0, 714, W, 950], fill=(10, 8, 20))
    tracked(d, (14, 718), "ALSO ON THE WIRES - THE REST OF SATURDAY, ONE LINE EACH",
            F["br_head"], GOLD, tracking=1)
    rw = d.textlength(S.REGION_LINE, font=F["br_reg"])
    d.text((W - 14 - rw, 721), S.REGION_LINE, font=F["br_reg"], fill=DIM)
    d.rectangle([14, 734, 1010, 735], fill=(42, 33, 64))
    cols = [(14 + i * 250, 250 - 14) for i in range(4)]
    per = [S.BRIEFS[i * 7:(i + 1) * 7] for i in range(4)]
    for ci, (x, cwd) in enumerate(cols):
        y = 740
        for (n, place, text, src) in per[ci]:
            head = f"{n} {place.upper()} - "
            body = text + f" ({src})"
            hw = d.textlength(head, font=F["br_num"])
            # two-stage wrap: first line shares space with the head, the rest
            # get the full column width (keeps sources from being clipped)
            first = wrap(d, body, F["br_txt"], cwd - hw)
            lines = [first[0]]
            rest = " ".join(first[1:])
            if rest:
                lines += wrap(d, rest, F["br_txt"], cwd)
            lines = lines[:3]
            d.text((x, y), head, font=F["br_num"], fill=(255, 226, 160))
            for j, ln in enumerate(lines):
                d.text((x + (hw if j == 0 else 0), y + j * 12.2), ln,
                       font=F["br_txt"], fill=(216, 205, 178))
            y += len(lines) * 12.2 + 3.5


def date_check(img):
    d = ImageDraw.Draw(img)
    d.rectangle([0, 950, W, 988], fill=(42, 13, 18))
    d.rectangle([0, 950, W, 951], fill=(255, 122, 107))
    lab = "DATE CHECK - LEFT OUT AS FRIDAY 20 NOVEMBER'S NEWS: "
    body = (lab + " · ".join(S.DATE_DISCARDS) +
            ".  NOT YET HAPPENED, SO NOT SHOWN: " + " · ".join(S.DATE_NOT_YET) + ".")
    lw = d.textlength(lab, font=F["dc_lab"])
    lines = wrap(d, body[len(lab):], F["dc"], W - 28 - lw)
    d.text((14, 956), lab, font=F["dc_lab"], fill=(255, 150, 138))
    for j, ln in enumerate(lines[:3]):
        d.text((14 + (lw if j == 0 else 0), 956 + j * 11.5), ln, font=F["dc"],
               fill=(238, 205, 198))


def footer(img):
    d = ImageDraw.Draw(img)
    d.rectangle([0, 988, W, H], fill=(8, 6, 16))
    d.text((14, 1000), S.FOOTER, font=F["foot"], fill=(154, 143, 120))
    rw = d.textlength(S.FOOTER_R, font=F["foot"])
    d.text((W - 14 - rw, 1000), S.FOOTER_R, font=F["foot"], fill=(154, 143, 120))
    d.text((14, 1012), S.KICKER, font=F["foot"], fill=(110, 100, 82))


def build():
    img = sky()
    masthead(img)
    scene = Image.open(os.path.join(HERE, "scene.png")).convert("RGBA")
    scene = scene.resize((W, BAND_H), Image.LANCZOS)
    img.alpha_composite(scene, (0, BAND_Y))
    anchors = json.load(open(os.path.join(HERE, "anchors.json")))
    by_n = {c["n"]: c for c in S.CARDS}
    for n in sorted(by_n, key=int):
        a = anchors[str(n)]
        cx, top = a["cx"] / 2, BAND_Y + a["top"] / 2 + 3
        pw = 192 if a["top"] / 2 < 100 else (200 if a["top"] / 2 < 250 else 208)
        panel(img, by_n[n], cx, top, pw)
    numbers_strip(img)
    timeline_strip(img)
    briefs(img)
    date_check(img)
    footer(img)
    return img.convert("RGB")


def main():
    out_dir = "/output"
    os.makedirs(out_dir, exist_ok=True)
    scene_ok = os.path.exists(os.path.join(HERE, "scene.png")) and \
        os.path.exists(os.path.join(HERE, "anchors.json"))
    if scene_ok:
        img = build()
        img.save(os.path.join(HERE, "entry.png"))
    else:
        img = Image.open(os.path.join(HERE, "entry.png"))
    img.save(os.path.join(out_dir, "entry.png"))
    print("entry.png written:", os.path.getsize(os.path.join(out_dir, "entry.png")), "bytes")


if __name__ == "__main__":
    main()
