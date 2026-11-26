#!/usr/bin/env python3
"""THE THURSDAY GAZETTE — one image summing up Thursday 26 November 2026.

Build-time renderer (Pillow). Draws entry.png 1024x1024, <=1 MiB.
All facts come from ~/workspace/makefun/news-image-20261126-lab/RESEARCH.md.
Discipline: claims are marked as claims; postponed is never cancelled;
no single figure where sources conflict.
"""
import os
import hashlib
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
BASE = os.path.dirname(os.path.abspath(__file__))
F_SANS = os.path.join(BASE, "fonts", "DejaVuSans.ttf")
F_SANSB = os.path.join(BASE, "fonts", "DejaVuSans-Bold.ttf")
F_SERIFB = os.path.join(BASE, "fonts", "DejaVuSerif-Bold.ttf")

INK = (18, 18, 18)
PAPER = (250, 247, 238)
RULE = (18, 18, 18)
ACCENT = (158, 28, 24)      # deep broadsheet red
NAVY = (24, 42, 72)
TEAL = (18, 84, 96)
GOLD = (176, 128, 28)
SKY = (214, 231, 240)
SEA = (38, 98, 128)

def font(path, size):
    return ImageFont.truetype(path, size)

def wrap(draw, text, fnt, max_w):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines

def para(draw, x, y, text, fnt, max_w, fill=INK, leading=None, max_lines=None):
    lines = wrap(draw, text, fnt, max_w)
    if max_lines:
        lines = lines[:max_lines]
    lh = leading or int(fnt.size * 1.28)
    for ln in lines:
        draw.text((x, y), ln, font=fnt, fill=fill)
        y += lh
    return y

def head(draw, x, y, text, fnt, max_w, fill=INK, leading=None, max_lines=2):
    return para(draw, x, y, text, fnt, max_w, fill=fill, leading=leading, max_lines=max_lines)

# ---------------------------------------------------------------- map data
# Rough lon/lat outlines (equirectangular). Good enough to read at a glance.
NA = [(-168,66),(-150,70),(-135,69),(-125,71),(-115,68),(-100,69),(-90,68),(-85,66),(-80,73),(-75,68),(-70,62),(-65,60),(-58,55),(-55,52),(-60,47),(-65,44),(-70,42),(-75,35),(-80,32),(-81,26),(-84,30),(-89,29),(-94,29),(-97,26),(-100,22),(-97,16),(-92,15),(-86,13),(-82,9),(-79,9),(-83,10),(-88,13),(-93,15),(-97,16),(-102,18),(-106,22),(-110,24),(-114,29),(-118,33),(-122,37),(-124,42),(-124,48),(-128,52),(-133,56),(-140,60),(-148,60),(-155,58),(-162,58),(-166,60),(-168,66)]
SA = [(-80,9),(-76,10),(-71,12),(-64,11),(-59,8),(-54,6),(-51,4),(-50,0),(-46,-2),(-42,-3),(-38,-5),(-35,-8),(-37,-11),(-39,-15),(-41,-22),(-46,-24),(-48,-27),(-52,-32),(-55,-35),(-58,-38),(-62,-41),(-65,-45),(-68,-50),(-69,-52),(-71,-54),(-73,-50),(-73,-44),(-73,-37),(-72,-30),(-71,-22),(-72,-18),(-76,-14),(-79,-8),(-81,-4),(-80,0),(-80,9)]
EU = [(-10,36),(-9,38),(-9,43),(-4,44),(-2,48),(-4,49),(-1,51),(2,51),(4,53),(7,54),(8,57),(10,59),(7,58),(5,60),(6,62),(10,64),(14,67),(18,69),(22,70),(27,71),(30,70),(34,68),(38,68),(42,68),(46,68),(50,69),(55,68),(60,69),(65,70),(68,72),(72,72),(75,73),(70,72),(65,70),(60,68),(55,67),(50,66),(45,66),(40,64),(36,65),(33,64),(30,62),(28,60),(25,59),(22,59),(19,58),(18,56),(21,55),(19,54),(15,54),(12,55),(8,57),(5,58),(3,58),(0,57),(-2,57),(-5,56),(-5,50),(-4,48),(-2,47),(-1,44),(-2,43),(-6,43),(-9,43),(-9,38),(-6,36),(-10,36)]
AF = [(-6,35),(-10,31),(-14,28),(-16,24),(-17,21),(-17,15),(-16,12),(-13,9),(-10,7),(-7,5),(-4,5),(0,6),(4,6),(7,4),(9,4),(9,0),(10,-3),(12,-6),(13,-10),(12,-15),(13,-19),(14,-23),(16,-28),(18,-33),(20,-35),(25,-34),(28,-33),(32,-29),(35,-24),(37,-20),(40,-15),(40,-11),(41,-6),(43,-2),(46,0),(48,2),(51,10),(48,11),(45,11),(42,12),(40,15),(38,18),(36,21),(34,25),(32,28),(30,31),(26,32),(22,33),(18,33),(14,33),(10,34),(6,35),(-6,35)]
AS = [(30,36),(33,36),(36,36),(38,38),(41,39),(44,39),(47,38),(49,40),(51,41),(53,43),(55,45),(57,47),(59,49),(61,51),(64,53),(67,55),(70,57),(73,60),(76,63),(79,66),(82,68),(85,69),(88,70),(92,71),(95,72),(99,73),(103,74),(108,74),(113,73),(118,73),(123,72),(128,71),(133,72),(138,72),(143,72),(148,71),(153,70),(158,69),(163,68),(168,67),(173,66),(178,65),(178,62),(172,62),(168,60),(162,58),(158,53),(156,51),(152,56),(148,59),(143,59),(140,55),(139,50),(136,44),(132,42),(129,38),(126,38),(123,38),(121,34),(120,31),(118,28),(115,24),(111,21),(109,18),(106,14),(104,10),(102,8),(100,9),(98,12),(96,15),(94,17),(92,20),(90,22),(88,22),(86,20),(84,19),(82,17),(80,14),(78,9),(76,10),(75,14),(73,18),(71,21),(69,23),(67,25),(64,25),(61,25),(59,26),(57,27),(55,28),(53,28),(51,29),(49,30),(48,30),(46,29),(44,29),(42,29),(40,30),(38,31),(36,33),(34,35),(32,36),(30,36)]
AU = [(113,-22),(114,-28),(115,-32),(117,-35),(121,-34),(126,-32),(130,-32),(133,-33),(136,-35),(139,-37),(142,-38),(146,-39),(149,-37),(151,-34),(153,-31),(153,-27),(151,-24),(148,-20),(145,-17),(142,-14),(142,-11),(139,-12),(136,-12),(134,-13),(131,-12),(128,-14),(125,-15),(122,-17),(119,-19),(115,-21),(113,-22)]
GL = [(-45,60),(-42,64),(-38,66),(-32,68),(-28,70),(-24,72),(-20,74),(-22,77),(-28,79),(-35,80),(-45,79),(-52,77),(-56,74),(-58,70),(-56,65),(-52,61),(-48,60),(-45,60)]

CONTINENTS = [NA, SA, EU, AF, AS, AU, GL]

def project(lon, lat, x0, y0, w, h):
    x = x0 + (lon + 180.0) / 360.0 * w
    y = y0 + (90.0 - lat) / 180.0 * h
    return (x, y)

# ---------------------------------------------------------------- scenes
def scene_gulf(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(16, 34, 52))
    d.rectangle([x, y + h * 0.62, x + w, y + h], fill=SEA)
    # sun / haze
    d.ellipse([x + w * 0.68, y + 8, x + w * 0.86, y + 26], fill=(232, 190, 90))
    # tanker
    tx, ty, tw, th = x + w * 0.12, y + h * 0.58, w * 0.55, h * 0.16
    d.rectangle([tx, ty, tx + tw, ty + th], fill=(40, 40, 44))
    d.rectangle([tx + tw * 0.62, ty - h * 0.12, tx + tw * 0.78, ty], fill=(120, 30, 26))
    d.line([tx + tw * 0.7, ty - h * 0.12, tx + tw * 0.7, ty - h * 0.22], fill=(200, 200, 200), width=2)
    # flames
    for fx, fh in [(0.18, 26), (0.30, 34), (0.44, 24)]:
        px = x + w * fx
        d.polygon([(px, ty - fh), (px - 8, ty), (px + 8, ty)], fill=(232, 120, 20))
        d.polygon([(px, ty - fh * 0.6), (px - 5, ty), (px + 5, ty)], fill=(245, 200, 60))
    # missile arcs to Riyadh
    for i, (sx, sy, ex, ey) in enumerate([(0.1, 0.9, 0.55, 0.15), (0.2, 0.95, 0.7, 0.2)]):
        pts = []
        for t in range(0, 21):
            tt = t / 20.0
            px = x + w * (sx + (ex - sx) * tt)
            py = y + h * (sy + (ey - sy) * tt) - 34 * (1 - (2 * tt - 1) ** 2)
            pts.append((px, py))
        d.line(pts, fill=(245, 200, 90), width=2)
    # waves
    for wy in (0.74, 0.84, 0.94):
        d.arc([x + 8, y + h * wy, x + w - 8, y + h * wy + 12], 200, 340, fill=(120, 180, 205), width=2)

def scene_macys(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(88, 102, 118))
    # buildings
    for bx, bw, bh in [(0.02, 0.16, 0.55), (0.2, 0.13, 0.7), (0.35, 0.15, 0.5), (0.52, 0.14, 0.66), (0.68, 0.15, 0.52), (0.85, 0.13, 0.62)]:
        d.rectangle([x + w * bx, y + h - h * bh, x + w * (bx + bw), y + h], fill=(52, 60, 74))
        for wy in range(3):
            for wx in range(2):
                d.rectangle([x + w * (bx + 0.03 + wx * 0.06), y + h - h * bh + 8 + wy * 12,
                             x + w * (bx + 0.05 + wx * 0.06), y + h - h * bh + 14 + wy * 12], fill=(240, 210, 110))
    # deflated balloon: sagging envelope slumped onto the rooftops
    # lumpy, wrinkled outline — top edge caves in, sides bulge in folds
    env = [
        (0.26, 0.40), (0.32, 0.33), (0.40, 0.36), (0.48, 0.31), (0.56, 0.36),
        (0.64, 0.32), (0.72, 0.38), (0.76, 0.46), (0.72, 0.52), (0.62, 0.55),
        (0.50, 0.52), (0.40, 0.56), (0.30, 0.52), (0.25, 0.46),
    ]
    d.polygon([(x + w * px, y + h * py) for px, py in env], fill=(158, 28, 24))
    # lighter top panel, also sagging
    d.polygon([(x + w * px, y + h * py) for px, py in [
        (0.32, 0.38), (0.40, 0.34), (0.48, 0.37), (0.56, 0.34), (0.66, 0.38),
        (0.68, 0.44), (0.58, 0.47), (0.46, 0.45), (0.36, 0.47), (0.30, 0.43),
    ]], fill=(196, 64, 52))
    # crease lines: folds where the fabric collapses
    for (sx, sy, ex, ey) in [(0.34, 0.40, 0.44, 0.50), (0.50, 0.38, 0.52, 0.52), (0.62, 0.39, 0.58, 0.50)]:
        d.line([x + w * sx, y + h * sy, x + w * ex, y + h * ey], fill=(110, 18, 16), width=2)
    # slack tethers: drooping curves, hanging loose to the street
    for (sx, sy, ex, ey) in [(0.30, 0.52, 0.44, 0.86), (0.70, 0.52, 0.58, 0.86)]:
        pts = []
        for t in range(0, 11):
            tt = t / 10.0
            px = sx + (ex - sx) * tt
            py = sy + (ey - sy) * tt + 0.06 * (1 - (2 * tt - 1) ** 2)
            pts.append((x + w * px, y + h * py))
        d.line(pts, fill=(220, 220, 220), width=2)
    # rain
    for rx in range(6, 100, 9):
        d.line([x + w * rx / 100.0, y + 4, x + w * rx / 100.0 - 4, y + 18], fill=(200, 215, 228), width=2)
    # street
    d.rectangle([x, y + h * 0.86, x + w, y + h], fill=(38, 40, 46))

def scene_ukraine(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(10, 16, 34))
    # stars
    for sx, sy in [(0.08, 0.12), (0.22, 0.06), (0.38, 0.16), (0.55, 0.08), (0.7, 0.14), (0.85, 0.07), (0.93, 0.2), (0.45, 0.05), (0.15, 0.3), (0.62, 0.28)]:
        d.ellipse([x + w * sx - 1, y + h * sy - 1, x + w * sx + 1, y + h * sy + 1], fill=(240, 240, 255))
    # interceptor arcs
    for (sx, sy, ex, ey, col) in [(0.05, 0.95, 0.5, 0.2, (245, 200, 90)), (0.25, 0.95, 0.75, 0.1, (255, 255, 255)), (0.55, 0.95, 0.9, 0.3, (245, 200, 90))]:
        pts = []
        for t in range(0, 21):
            tt = t / 20.0
            px = x + w * (sx + (ex - sx) * tt)
            py = y + h * (sy + (ey - sy) * tt) - 44 * (1 - (2 * tt - 1) ** 2)
            pts.append((px, py))
        d.line(pts, fill=col, width=2)
    # explosion bursts
    for bx, by in [(0.5, 0.2), (0.75, 0.12), (0.9, 0.3)]:
        cx, cy = x + w * bx, y + h * by
        for ang in range(0, 360, 45):
            import math
            ex = cx + 12 * math.cos(math.radians(ang))
            ey = cy + 12 * math.sin(math.radians(ang))
            d.line([(cx, cy), (ex, ey)], fill=(255, 160, 40), width=2)
        d.ellipse([cx - 4, cy - 4, cx + 4, cy + 4], fill=(255, 220, 120))
    # skyline
    for bx, bw, bh in [(0.0, 0.18, 0.28), (0.2, 0.15, 0.4), (0.38, 0.16, 0.32), (0.56, 0.14, 0.44), (0.72, 0.15, 0.3), (0.88, 0.12, 0.38)]:
        d.rectangle([x + w * bx, y + h - h * bh, x + w * (bx + bw), y + h], fill=(24, 30, 52))

# ---------------------------------------------------------------- tile icons
def icon(d, kind, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=SKY)
    cx, cy = x + w / 2, y + h / 2
    if kind == "tariffs":
        d.rectangle([x + 8, cy - 6, x + w - 8, cy + 10], fill=(150, 60, 50))
        d.rectangle([x + 14, cy - 16, x + w - 14, cy - 6], fill=(200, 90, 70))
        d.line([(x + 10, cy + 16), (x + w * 0.4, cy + 2), (x + w * 0.6, cy + 8), (x + w - 10, cy - 10)], fill=(24, 90, 40), width=3)
    elif kind == "gaza":
        d.rectangle([x + 10, cy - 14, x + w - 10, cy + 16], fill=(90, 90, 96))
        d.rectangle([x + 16, cy + 2, x + 22, cy + 8], fill=(240, 210, 110))
        d.ellipse([x + w - 22, cy - 24, x + w - 6, cy - 8], fill=(150, 150, 155))
        d.ellipse([x + w - 18, cy - 18, x + w - 10, cy - 10], fill=(180, 180, 185))
    elif kind == "bogor":
        d.rectangle([x + 10, cy - 18, x + w - 10, cy - 10], fill=(120, 84, 40))
        d.rectangle([x + w * 0.4, cy - 10, x + w * 0.6, cy + 16], fill=(60, 44, 26))
        for rx in range(0, 5):
            d.line([x + 10 + rx * 10, y + 4, x + 6 + rx * 10, y + 14], fill=(120, 170, 205), width=2)
    elif kind == "pound":
        d.rectangle([x + 8, cy - 16, x + w - 8, cy + 16], fill=(24, 90, 40))
        d.rectangle([x + 8, cy - 16, x + w - 8, cy - 8], fill=(18, 60, 30))
        d.text((cx - 8, cy - 8), "£", font=font(F_SANSB, 22), fill=(255, 255, 255))
    elif kind == "ukeu":
        d.rectangle([x + 10, cy - 14, cx - 2, cy + 14], fill=(24, 42, 120))
        d.rectangle([cx + 2, cy - 14, x + w - 10, cy + 14], fill=(180, 30, 30))
        d.text((cx - 4, cy - 6), "×", font=font(F_SANSB, 14), fill=(255, 255, 255))
    elif kind == "boat":
        d.polygon([(x + 10, cy + 6), (x + w - 10, cy + 6), (x + w - 16, cy + 16), (x + 16, cy + 16)], fill=(120, 60, 30))
        d.line([(cx, cy + 6), (cx, cy - 18)], fill=(60, 60, 60), width=2)
        d.polygon([(cx, cy - 18), (cx + 16, cy - 2), (cx, cy - 2)], fill=(240, 240, 240))
    elif kind == "iran":
        d.line([(cx, cy - 18), (cx, cy + 16)], fill=(60, 60, 60), width=3)
        d.line([(cx - 14, cy - 18), (cx + 14, cy - 18)], fill=(60, 60, 60), width=3)
        d.arc([cx - 18, cy - 6, cx - 2, cy + 8], 0, 180, fill=(158, 28, 24), width=2)
        d.arc([cx + 2, cy - 6, cx + 18, cy + 8], 0, 180, fill=(158, 28, 24), width=2)
    elif kind == "kim":
        d.polygon([(x + 8, cy + 16), (cx, cy - 18), (x + w - 8, cy + 16)], fill=(70, 80, 100))
        d.polygon([(cx - 6, cy - 8), (cx, cy - 16), (cx + 6, cy - 8)], fill=(255, 255, 255))
        d.ellipse([cx - 3, cy - 26, cx + 3, cy - 20], fill=(232, 180, 40))
    elif kind == "space":
        d.polygon([(cx - 5, cy - 18), (cx + 5, cy - 18), (cx + 3, cy + 2), (cx - 3, cy + 2)], fill=(200, 200, 210))
        d.polygon([(cx - 8, cy + 2), (cx - 3, cy + 2), (cx - 5, cy + 12)], fill=(232, 120, 40))
        d.polygon([(cx + 8, cy + 2), (cx + 3, cy + 2), (cx + 5, cy + 12)], fill=(232, 120, 40))
        d.ellipse([x + w - 16, y + 6, x + w - 4, y + 18], fill=(232, 180, 40))
    elif kind == "football":
        d.ellipse([x + 10, cy - 10, x + w - 10, cy + 10], fill=(120, 60, 30))
        d.line([(cx - 12, cy), (cx + 12, cy)], fill=(255, 255, 255), width=2)
        for lx in (-8, -3, 2, 7):
            d.line([(cx + lx, cy - 4), (cx + lx, cy + 4)], fill=(255, 255, 255), width=2)
    elif kind == "cia":
        d.rectangle([x + 10, cy - 12, x + w - 10, cy + 8], fill=(40, 50, 70))
        d.rectangle([x + 14, cy - 8, x + w - 14, cy + 4], fill=(160, 210, 230))
        d.ellipse([cx + 6, cy + 4, cx + 18, cy + 16], fill=(255, 255, 255), outline=(60, 60, 60), width=2)
        d.line([(cx + 16, cy + 14), (cx + 22, cy + 20)], fill=(60, 60, 60), width=2)
    elif kind == "wave":
        for wy, ww in [(0.25, 1.0), (0.5, 0.85), (0.75, 1.0)]:
            d.arc([x + 6, y + h * wy - 8, x + w - 6, y + h * wy + 14], 180, 360, fill=(38, 98, 158), width=3)
        d.line([(x + 8, cy - 20), (x + 8, cy + 10)], fill=(120, 80, 40), width=3)
        d.line([(x + 8, cy - 20), (x + w - 8, cy - 20)], fill=(120, 80, 40), width=3)

# ---------------------------------------------------------------- content
LEADS = [
    {
        "kicker": "THE GULF WAR — DAY 12",
        "headline": "IRGC CLAIMS A THIRD TANKER MINED IN HORMUZ",
        "sub": "Unconfirmed — UKMTO cites an 'unknown projectile'. Riyadh missiles downed; Jazan hit confirmed.",
        "scene": scene_gulf,
    },
    {
        "kicker": "NO PARADE TODAY",
        "headline": "MACY'S POSTPONED — FIRST TIME IN 100 YEARS",
        "sub": "The 100th parade moves to Sat 28 Nov, 08:30 ET — POSTPONED, not cancelled. First in 100 years.",
        "scene": scene_macys,
    },
    {
        "kicker": "UKRAINE OVERNIGHT BLITZ",
        "headline": "113 DRONES, 20 IMPACTS",
        "sub": "Iskander-M, Tsirkon, S-400 + 113 drones overnight; Kyiv, Kharkiv, Nikopol hit; 87 downed.",
        "scene": scene_ukraine,
    },
]

TILES = [
    ("tariffs", "TARIFFS: ASIA RALLIES", "US hits 14 partners; markets call it 'not as bad as feared' — no stacking on July rates."),
    ("gaza", "GAZA: 9 DEAD, 3RD NIGHT", "Strikes continue despite the year-old ceasefire; toll 74,746. A Hamas official is among the dead."),
    ("bogor", "BOGOR MINE FLOOD: 13 DEAD", "Illegal gold mine floods in W. Java; 13 confirmed dead, 13 still trapped as rescue goes on."),
    ("pound", "POUNDLAND IN ADMINISTRATION [WED 25 NOV]", "11,000 jobs, ~600 shops at risk — stores stay open. Bought for £1 in June."),
    ("ukeu", "UK + EU PUBLISH TWO DEALS", "Food trade + emissions pacts; a 10-year break clause with border rebuild costs."),
    ("boat", "THE BOAT DEALER BEHIND 29% OF CROSSINGS", "BBC probe: a German dealer, MaReBoote, linked to 29% of detected Channel crossings."),
    ("iran", "SIX IRANIAN WOMEN SENTENCED TO DEATH", "Over the January protests; UN rapporteur cites forced confessions. 2,003 executions in a year."),
    ("kim", "KIM INSPECTS NUCLEAR SITES", "N. Korea expels a Swiss diplomat in 48 hours; Kim calls nuclear status 'irreversible'."),
    ("space", "FIRST PAKISTANI IN ORBIT [WED 25 NOV]", "Shenzhou-24 docks at Tiangong; Muhammad Zeeshan Ali, the first foreign astronaut there."),
    ("football", "RODGERS RELEASED BY STEELERS [WED 25 NOV]", "After blasting his coach on TV: 'That ship has sailed.' The 4× MVP, 42, heads to waivers."),
    ("cia", "CIA/ODNI OSINT NETWORK HACKED", "Unclassified open-source system breached; classified systems untouched. Origin unconfirmed."),
    ("wave", "KING TIDES BATTER CALIFORNIA", "Pacifica pier collapses; La Jolla tide hits a record 8.11 ft. 81.5m travel for Thanksgiving."),
]

MARKET_LINE = ("MARKETS  •  THU 26 NOV — ASIA CLOSE / EUROPE MORNING; US CLOSED — THANKSGIVING    "
               "DAX +1.8% 25,131.36   •   CAC +1.6% 8,110.88   •   FTSE +1.3% 10,563.62   •   "
               "NIKKEI +1.3% 57,745.27 (WSJ)   •   KOSPI +1.5–1.9%   •   HANG SENG +1.9%   •   "
               "TAIWAN +1.4–2.6%   •   BRENT FUTURES $94.83 +0.2%   •   BITCOIN $60,825.53 (THU 26 NOV 09:10 UTC)")

PINS = [
    ("Hormuz", 26.5, 56.3), ("Riyadh", 24.7, 46.7), ("Jazan", 16.9, 42.55),
    ("Kyiv", 50.45, 30.52), ("Gaza", 31.5, 34.45), ("Bogor", -6.6, 106.8),
    ("New York", 40.7, -74.0), ("California", 32.85, -117.27),
    ("London", 51.5, -0.12), ("Pyongyang", 39.03, 125.75),
    ("Jiuquan", 40.96, 100.3), ("Kinshasa", -4.32, 15.31),
]
PIN_NAMES = ["1 Hormuz — tanker claim", "2 Riyadh — missiles", "3 Jazan — port hit",
             "4 Kyiv — overnight blitz", "5 Gaza — 9 dead", "6 Bogor — mine flood",
             "7 New York — parade", "8 California — king tides", "9 London — Poundland",
             "10 Pyongyang — nuclear", "11 Jiuquan — Shenzhou-24", "12 Kinshasa — envoy row"]

ALSO = [
    ("17", "Huawei: Beijing condemns, Huawei to appeal — verdict Tue (US), reaction Wed", "26 NOV — REACTION"),
    ("18", "Sudan: UN condemns Damazin strike; army downs an FH-95 drone", "26 NOV"),
    ("19", "DR Congo summons Uganda envoy over a general's tweets", "26 NOV"),
    ("20", "Solomon Islands–Australia pact signed, no foreign bases", "WED 25 NOV"),
    ("21", "COP31 blame game — OPEC blames the EU, COP president defends the process", "26 NOV"),
    ("22", "FedEx cargo jet slides off a Miami runway — ground stop on Thanksgiving eve", "WED 25 NOV"),
    ("23", "Trump: Thanksgiving proclamation + turkey pardons 'Freedom' & 'Feathers'", "26 NOV"),
    ("24", "Bank of Korea hikes to 3.25%; Fed futures imply a 98% Dec hike", "26 NOV"),
    ("25", "UK to publish more Mandelson papers after police clearance", "26 NOV"),
    ("26", "UK stalking law simplified into one offence; max term stays 10 years", "26 NOV"),
    ("27", "Spain: snap election Sun 29 Nov — conservatives lead narrowly", "26 NOV — PREVIEW"),
    ("28", "Two Pakistani drama screenings cancelled in Bengaluru after online protests", "26 NOV"),
    ("29", "Guinea orders a Conakry clean-up after the dump collapse (31 dead)", "WED 25 NOV"),
    ("30", "Gang attack at Bonga market, Kenscoff, Haiti — 10 dead", "WED 25 NOV"),
    ("31", "First close-up photos of the DART crater on Dimorphos — stadium-sized", "TUE 25 NOV"),
    ("32", "2nd India vs NZ Test starts Fri in Christchurch", "26 NOV — PREVIEW"),
    ("33", "F1 Qatar GP this weekend — title decided, P2 fight open", "26 NOV — PREVIEW"),
    ("34", "Pochettino's Man Utd nightmare — 4–0 loss to Liverpool", "SUN 22 NOV"),
    ("35", "Cairo: no new toll Thu — still 31 dead / 21 hurt", "26 NOV — UPDATE"),
    ("36", "Manipur: no new toll Thu — still 20 dead", "26 NOV — UPDATE"),
    ("37", "Cikande: no new figures Thu — 26 body bags / 28 still missing", "26 NOV — UPDATE"),
    ("38", "UK to double its social-media unit spend to £25m", "26 NOV"),
    ("39", "Met Office: fewer frosts, more hot days as UK seasons shift", "26 NOV"),
    ("40", "France's mainstream risks failing in the presidential vote", "26 NOV"),
]

FOOTER = ("SOURCES: BBC • REUTERS • CHANNEL NEWS ASIA • BLOOMBERG • AP • CNN • THE MOTLEY FOOL • INVESTOPEDIA • "
          "FINNHUB • WSJ • EURONEXT — PLUS OFFICIAL RELEASES (UKMTO, NWS, FAA, CMSA, BANK OF KOREA, HOME OFFICE, "
          "CABINET OFFICE, SAUDI-LED COALITION, WHITE HOUSE)")

# ---------------------------------------------------------------- build
def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    f_mast = font(F_SERIFB, 62)
    f_date = font(F_SANSB, 19)
    f_sub = font(F_SANS, 12)
    f_kick = font(F_SANSB, 11)
    f_lead_h = font(F_SANSB, 16)
    f_lead_s = font(F_SANS, 11)
    f_tile_h = font(F_SANSB, 11)
    f_tile_b = font(F_SANS, 9)
    f_mkt = font(F_SANSB, 11)
    f_map_h = font(F_SANSB, 13)
    f_leg = font(F_SANS, 10)
    f_also_h = font(F_SANSB, 12)
    f_also = font(F_SANS, 9)
    f_also_n = font(F_SANSB, 9)
    f_foot = font(F_SANS, 8)

    # ---- masthead
    d.text((W / 2, 8), "THE THURSDAY GAZETTE", font=f_mast, fill=INK, anchor="ma")
    d.line([(14, 78), (W - 14, 78)], fill=RULE, width=2)
    d.text((14, 84), "THURSDAY 26 NOVEMBER 2026", font=f_date, fill=INK)
    d.text((W - 14, 84), "40 STORIES  •  4 CONTINENTS", font=f_date, fill=ACCENT, anchor="ra")

    # ---- leads
    y0, lh = 106, 190
    col_w = (W - 28 - 16) / 3
    for i, lead in enumerate(LEADS):
        x = 14 + i * (col_w + 8)
        d.rectangle([x, y0, x + col_w, y0 + lh], outline=(120, 115, 100), width=1)
        lead["scene"](d, x + 1, y0 + 1, col_w - 2, 98)
        d.text((x + 6, y0 + 102), lead["kicker"], font=f_kick, fill=ACCENT)
        head(d, x + 6, y0 + 118, lead["headline"], f_lead_h, col_w - 12, max_lines=2, leading=18)
        para(d, x + 6, y0 + 156, lead["sub"], f_lead_s, col_w - 12, max_lines=2, leading=13)

    # ---- tiles 4 x 3
    ty0 = 302
    tw, th, gap = 244, 80, 8
    for i, (kind, hline, body) in enumerate(TILES):
        r, c = divmod(i, 4)
        x = 14 + c * (tw + gap)
        y = ty0 + r * (th + gap)
        d.rectangle([x, y, x + tw, y + th], outline=(120, 115, 100), width=1)
        icon(d, kind, x + 1, y + 1, 60, th - 2)
        head(d, x + 68, y + 5, hline, f_tile_h, tw - 74, max_lines=2, leading=13)
        para(d, x + 68, y + 33, body, f_tile_b, tw - 74, max_lines=3, leading=11)

    # ---- markets strip
    my = 560
    d.rectangle([14, my, W - 14, my + 52], fill=NAVY)
    lines = wrap(d, MARKET_LINE, f_mkt, W - 28 - 16)
    yy = my + 7
    for ln in lines[:3]:
        d.text((22, yy), ln, font=f_mkt, fill=(255, 255, 255))
        yy += 14

    # ---- map band
    map_y, map_h = 618, 172
    d.text((14, map_y), "WHERE IT HAPPENED", font=f_map_h, fill=INK)
    d.text((W - 14, map_y), "ASIA 7  •  EUROPE 2  •  NORTH AMERICA 2  •  AFRICA 1", font=f_leg, fill=ACCENT, anchor="ra")
    mx, myy, mw, mh = 14, map_y + 20, 700, map_h - 20
    d.rectangle([mx, myy, mx + mw, myy + mh], fill=(196, 222, 235), outline=(120, 115, 100), width=1)
    # graticule
    for lon in range(-150, 181, 30):
        gx = mx + (lon + 180) / 360 * mw
        d.line([(gx, myy), (gx, myy + mh)], fill=(170, 200, 215), width=1)
    for lat in (-60, -30, 0, 30, 60):
        gy = myy + (90 - lat) / 180 * mh
        d.line([(mx, gy), (mx + mw, gy)], fill=(170, 200, 215), width=1)
    for poly in CONTINENTS:
        pts = [project(lon, lat, mx, myy, mw, mh) for lon, lat in poly]
        d.polygon(pts, fill=(196, 178, 138), outline=(140, 120, 80))
    # pins
    for i, (name, lat, lon) in enumerate(PINS, start=1):
        px, py = project(lon, lat, mx, myy, mw, mh)
        d.ellipse([px - 8, py - 8, px + 8, py + 8], fill=ACCENT, outline=(255, 255, 255), width=1)
        d.text((px, py - 1), str(i), font=font(F_SANSB, 9), fill=(255, 255, 255), anchor="mm")
    # legend
    lx = 730
    for i, name in enumerate(PIN_NAMES):
        yy = myy + 4 + i * 12
        d.ellipse([lx, yy + 1, lx + 9, yy + 10], fill=ACCENT)
        d.text((lx + 5, yy + 1), str(i + 1), font=font(F_SANSB, 7), fill=(255, 255, 255), anchor="ma")
        d.text((lx + 14, yy), name, font=f_leg, fill=INK)

    # ---- ALSO
    ay = 796
    d.line([(14, ay), (W - 14, ay)], fill=RULE, width=2)
    d.text((14, ay + 4), "ALSO — IN BRIEF", font=f_also_h, fill=INK)
    d.text((W - 14, ay + 4), "24 MORE STORIES", font=f_also_h, fill=ACCENT, anchor="ra")
    col2_w = (W - 28 - 16) / 2
    for i, (num, text, tag) in enumerate(ALSO):
        col = 0 if i < 12 else 1
        row = i % 12
        x = 14 + col * (col2_w + 16)
        y = ay + 24 + row * 14
        d.text((x, y), num + ".", font=f_also_n, fill=ACCENT)
        d.text((x + 20, y), text, font=f_also, fill=INK)
        twd = d.textlength(text, font=f_also)
        d.text((x + 20 + twd + 4, y), "[" + tag + "]", font=f_also, fill=(120, 115, 100))

    # ---- footer
    fy = 988
    d.line([(14, fy), (W - 14, fy)], fill=RULE, width=1)
    flines = wrap(d, FOOTER, f_foot, W - 28)
    yy = fy + 4
    for ln in flines:
        d.text((14, yy), ln, font=f_foot, fill=(90, 85, 75))
        yy += 11
    d.text((W - 14, fy + 4 + 11), "ALL STORIES VERIFIED 26 NOV 2026 • CLAIMS MARKED AS CLAIMS",
           font=font(F_SANSB, 8), fill=(90, 85, 75), anchor="ra")

    out = os.path.join(BASE, "entry.png")
    img.save(out, optimize=True)
    size = os.path.getsize(out)
    sha = hashlib.sha256(open(out, "rb").read()).hexdigest()
    print("entry.png", size, "bytes, sha256", sha)
    assert img.size == (1024, 1024)
    assert size <= 1024 * 1024, "over 1 MiB"

if __name__ == "__main__":
    main()
