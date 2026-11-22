"""Everyday Cart Reel for 22 Nov: "Winter night + rooftop = BBQ": Portable BBQ Grill Machine.
Deep night navy sky + ember orange / flame yellow / smoke cream flat palette. Bangla hook in the first second
("শীতের রাত + ছাদ = ?" over a flat moon and city skyline, then "বারবিকিউ পার্টি!" with flat flames), the grill drops onto
the rooftop with bobbing flat flames above it, a BBQ night checklist (only listing facts: durable steel body, adjustable
charcoal tray, manual air blower, picnic / camping / rooftop), "কী গ্রিল করবেন?" chips, price card with comment prompt,
end card. Original drive synth track in key 2. About 22 s."""

import os as _os
_R = _os.path.dirname(_os.path.abspath(__file__)); _T = _os.path.dirname(_R)

import os, sys, math
from PIL import Image, ImageDraw
sys.path.insert(0, _T); sys.path.insert(0, _R)
from mega import T, TB, P, pill, bg, wipe, logo, disc, put, rgba, f, ease, back, clamp, HQ, WHITE
import reels9 as R9
from reels9 import end_card
import drive as DR

W, H = 1080, 1920
R9.OUT = _R + "/out/out1122/"; os.makedirs(R9.OUT, exist_ok=True)
NIGHT = (16, 24, 58); NIGHT2 = (28, 40, 88); EMBER = (255, 112, 44); FLAME = (255, 204, 60); SMOKE = (255, 242, 222)
INK = (20, 18, 30); SKY2 = (40, 54, 110); ROOF = (36, 34, 52)
GRILL = "27.png"
B = DR.B


def stars(img, t, n=40, seed=5):
    import random
    r = random.Random(seed); d = ImageDraw.Draw(img)
    for i in range(n):
        x, y = r.uniform(30, W - 30), r.uniform(80, 900); s = 3 + 3 * (0.5 + 0.5 * math.sin(t * 3 + i))
        d.ellipse((x - s, y - s, x + s, y + s), fill=rgba(SMOKE))


def moon(img, cx, cy, r):
    d = ImageDraw.Draw(img)
    d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=rgba(FLAME))
    d.ellipse((cx - r + r * .55, cy - r - r * .2, cx + r + r * .55, cy + r - r * .2), fill=rgba(NIGHT))


def skyline(img, base=1460, col=SKY2):
    d = ImageDraw.Draw(img)
    blds = [(0, 160, 330), (150, 300, 420), (290, 400, 280), (390, 560, 470), (540, 660, 340), (650, 820, 520), (810, 930, 300), (920, 1080, 430)]
    for x0, x1, h in blds:
        d.rectangle((x0, base - h, x1, base), fill=rgba(col))
        for wy in range(int(base - h + 40), base - 40, 70):
            for wx in range(x0 + 24, x1 - 30, 50):
                if (wx * 7 + wy) % 3 == 0: d.rectangle((wx, wy, wx + 20, wy + 30), fill=rgba(FLAME))
    d.rectangle((0, base, W, H), fill=rgba(ROOF))
    d.rectangle((0, base, W, base + 22), fill=rgba((60, 58, 82)))


def flame(img, cx, by, h, t, ph=0):
    d = ImageDraw.Draw(img); w = h * .55; k = 1 + .12 * math.sin(t * 9 + ph)
    for col, s in ((EMBER, 1.0), (FLAME, .62)):
        hh = h * s * k; ww = w * s
        pts = [(cx - ww / 2, by), (cx - ww / 2 - 4, by - hh * .45), (cx - ww * .1, by - hh * .7), (cx, by - hh), (cx + ww * .15, by - hh * .62),
               (cx + ww / 2 + 4, by - hh * .45), (cx + ww / 2, by)]
        d.polygon(pts, fill=rgba(col)); d.ellipse((cx - ww / 2, by - ww / 2, cx + ww / 2, by + ww / 2), fill=rgba(col))


def p_hook(t, b, prev):
    img = bg(NIGHT); stars(img, t); moon(img, 820, 330, 110); skyline(img)
    k1 = (t - .05) / .22
    if k1 > 0: put(img, TB("শীতের রাত + ছাদ = ?", 700, 120, WHITE, True), W / 2, 620, scale=1.4 - .4 * ease(k1), a=clamp(k1 * 2))
    k2 = (t - 1.0) / .25
    if k2 > 0:
        put(img, TB("বারবিকিউ পার্টি!", 700, 150, FLAME, True), W / 2, 860, scale=1.35 - .35 * back(k2), a=clamp(k2 * 2))
        for i, x in enumerate((300, 540, 780)): flame(img, x, 1440, 170 * ease(k2) + 30 * (i == 1), t, i)
    kk = back((t - 1.7) / .3)
    if kk > 0: put(img, pill("WINTER BBQ NIGHT", 54, EMBER, WHITE, padx=46), W / 2, 1640, scale=kk, rot=-3)
    logo(img); return img


def p_reveal(t, b, prev):
    img = bg(NIGHT); stars(img, t, seed=8); skyline(img, base=1520, col=NIGHT2)
    drop = ease((t - .05) / .5)
    km = back(t / .45)
    if km > 0: disc(img, W / 2, 1040, 400 * km, (255, 228, 150))
    if drop > 0:
        y = 1180 - 700 * (1 - drop) + 4 * math.sin(t * 4)
        put(img, P(GRILL, 860, 720), W / 2, y)
        for i, x in enumerate((380, 520, 660)):
            flame(img, x, y - 318, 110 * drop, t, i)
    kt = back((t - .7) / .35)
    if kt > 0: put(img, T("Portable BBQ Grill", f("Poppins-Bold.ttf", 92), WHITE, True), W / 2, 250, scale=kt)
    ks = back((t - 1.0) / .35)
    if ks > 0: put(img, TB("ছাদ পিকনিক বা ক্যাম্পিং সব জায়গায়", 700, 66, FLAME), W / 2, 370, scale=ks)
    kp = back((t - 1.5) / .35)
    if kp > 0: put(img, pill("Charcoal BBQ grill machine", 50, FLAME, INK, padx=46), W / 2, 1700, scale=kp, rot=2)
    logo(img); return wipe(img, prev, t, NIGHT)


CHECK = [("Durable steel body", EMBER), ("Adjustable charcoal tray", FLAME), ("Manual air blower", (120, 200, 255)), ("Picnic, camping, rooftop", (150, 230, 140))]


def p_check(t, b, prev):
    img = bg(SMOKE); d = ImageDraw.Draw(img)
    put(img, T("BBQ night checklist", f("Poppins-Bold.ttf", 84), INK), W / 2, 250, scale=back(t / .35))
    put(img, TB("শুধু কয়লা আর মশলা আনুন", 700, 64, EMBER), W / 2, 360, scale=back((t - .15) / .35))
    put(img, P(GRILL, 640, 470), W / 2, 680 + 6 * math.sin(t * 3), scale=back((t - .2) / .4))
    for i, (txt, col) in enumerate(CHECK):
        st = .7 + .5 * i; kk = back((t - st) / .32)
        if kk <= 0: continue
        card = Image.new("RGBA", (900, 150), (0, 0, 0, 0)); cd = ImageDraw.Draw(card)
        cd.rounded_rectangle((10, 12, 899, 149), radius=34, fill=rgba(INK))
        cd.rounded_rectangle((0, 0, 889, 137), radius=34, fill=rgba(WHITE), outline=rgba(INK), width=6)
        cd.ellipse((30, 26, 116, 112), fill=rgba(col), outline=rgba(INK), width=5)
        tick = clamp((t - st - .2) / .2)
        if tick > 0:
            pts = [(50, 70), (68, 90), (98, 50)]
            if tick < 1: pts = pts[:2] if tick < .5 else pts
            cd.line(pts, fill=rgba(INK), width=11, joint="curve")
        tt = T(txt, f("Poppins-Bold.ttf", 54), INK); card.alpha_composite(tt, (140, 69 - tt.height // 2))
        put(img, card, W / 2, 1030 + i * 180, scale=kk, rot=(-1.5 if i % 2 == 0 else 1.5))
    logo(img); return wipe(img, prev, t, SMOKE)


def p_menu(t, b, prev):
    img = bg(EMBER)
    put(img, TB("কী গ্রিল করবেন?", 700, 124, WHITE, True), W / 2, 300, scale=back(t / .35))
    yb = 760 + 6 * math.sin(t * 4); kb = back((t - .1) / .4)
    put(img, P(GRILL, 620, 440), W / 2, yb, scale=kb)
    if kb > .9:
        for i, x in enumerate((440, 540, 640)): flame(img, x, yb - 195, 90, t, i)
    chips = [("চিকেন", FLAME, INK, -4, 1150), ("বিফ", SMOKE, INK, 3, 1380), ("সবজি", (150, 230, 140), INK, -2, 1610)]
    for i, (txt, fill, col, rot, y) in enumerate(chips):
        kk = back((t - .7 - .45 * i) / .35)
        if kk <= 0: continue
        s = TB(txt, 700, 104, col); cw, ch = s.width + 120, s.height + 40
        c = Image.new("RGBA", (cw + 12, ch + 14), (0, 0, 0, 0)); cd = ImageDraw.Draw(c)
        cd.rounded_rectangle((12, 14, cw + 11, ch + 13), radius=ch // 2, fill=rgba(INK))
        cd.rounded_rectangle((0, 0, cw, ch), radius=ch // 2, fill=rgba(fill), outline=rgba(INK), width=6)
        c.alpha_composite(s, (60, 20)); put(img, c, W / 2 + (i - 1) * 70, y, scale=kk, rot=rot)
    logo(img); return wipe(img, prev, t, EMBER)


def p_price(t, b, prev):
    img = bg(NIGHT); stars(img, t, seed=11); moon(img, 880, 200, 70)
    kd = back(t / .4); disc(img, W / 2, 790, 330 * kd, (255, 228, 150))
    put(img, P(GRILL, 640, 520), W / 2, 820, scale=kd)
    if kd > .9:
        for i, x in enumerate((430, 540, 650)): flame(img, x, 820 - 232, 90, t, i)
    put(img, TB("দাম কত?", 700, 120, WHITE, True), W / 2, 230, scale=back(t / .3))
    kk = back((t - .7) / .4)
    if kk > 0:
        card = Image.new("RGBA", (780, 400), (0, 0, 0, 0)); cd = ImageDraw.Draw(card)
        cd.rounded_rectangle((16, 20, 779, 399), radius=56, fill=rgba(EMBER))
        cd.rounded_rectangle((0, 0, 763, 379), radius=56, fill=rgba(FLAME), outline=rgba(INK), width=8)
        lt = T("ONLY", f("Poppins-Bold.ttf", 48), INK); card.alpha_composite(lt, (382 - lt.width // 2, 34))
        pt = T("Tk 5,500", f("Poppins-Bold.ttf", 150), INK); card.alpha_composite(pt, (382 - pt.width // 2, 96))
        rt = "Regular Tk 9,500"; rfo = f("Poppins-Medium.ttf", 44); rw = rfo.getlength(rt)
        cd.text((382 - rw / 2, 290), rt, font=rfo, fill=rgba(INK)); cd.line((382 - rw / 2 - 6, 318, 382 + rw / 2 + 6, 318), fill=rgba(INK), width=5)
        put(img, card, W / 2, 1400, scale=kk, rot=-2)
    kc = back((t - 1.6) / .35)
    if kc > 0: put(img, TB("চিকেন না বিফ? কমেন্টে লিখুন", 700, 70, FLAME), W / 2, 1720, scale=kc)
    logo(img); return wipe(img, prev, t, NIGHT)


REELS = [
    dict(id="reel-rooftop-bbq-grill-winter-night", time="18:30", music=("drive", 2), b=B, cover=2000,
         scenes=[(p_hook, 5), (p_reveal, 8), (p_check, 9), (p_menu, 7), (p_price, 8),
                 (end_card([(GRILL, HQ), ("15.png", HQ), ("14.png", HQ)], NIGHT2, FLAME, "Winter nights, BBQ lights."), 7)]),
]

if __name__ == "__main__":
    mode = sys.argv[1]
    for r in REELS:
        if mode == "preview":
            parts, starts, total = R9.build(r, True); print(r["id"], round(total, 1)); shots = []
            for (fn, dur), st in zip(parts, starts):
                for fr in (.15, .5, .95): shots.append(fn(min(dur * fr, dur - .1)).convert("RGB"))
            cols = 6; rows = math.ceil(len(shots) / cols); sheet = Image.new("RGB", (cols * 270, rows * 480), "white")
            for i, s_ in enumerate(shots): sheet.paste(s_.resize((270, 480), Image.LANCZOS), ((i % cols) * 270, (i // cols) * 480))
            sheet.save(sys.argv[2], quality=86)
        else:
            R9.build(r)
