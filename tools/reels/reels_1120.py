"""Everyday Cart Reel for 20 Nov: "Good night kit": silent alarm clock (no tick tock) + 22 inch teddy bear.
Flat deep teal night + lilac + butter yellow palette, twinkling flat stars. Bangla hook in the first second
("TICK TOCK" words popping around a moon), the tick tock gets struck out and the silent clock pops in with its
features, then the teddy as the cuddle buddy, twin price cards, comment prompt, end card.
All facts from earlier store captions. Original upbeat synth track in key 3. About 24 s."""

import os as _os
_R = _os.path.dirname(_os.path.abspath(__file__)); _T = _os.path.dirname(_R)

import os, sys, math
from PIL import Image, ImageDraw
sys.path.insert(0, _T); sys.path.insert(0, _R)
from mega import T, TB, P, pill, bg, wipe, logo, disc, put, rgba, f, ease, back, clamp, HQ, WHITE
import reels9 as R9
from reels9 import end_card

W, H = 1080, 1920
R9.OUT = _R + "/out/out1120/"; os.makedirs(R9.OUT, exist_ok=True)
NIGHT = (14, 52, 62); NIGHT2 = (26, 74, 86); LILAC = (196, 172, 255); BUTTER = (255, 222, 110); CORAL = (255, 112, 96)
CREAM = (255, 248, 236)
CLK, TED = "07.png", "06.png"   # silent alarm clock, 22 inch teddy
UB = 60 / 116


def stars(img, t, col=WHITE, n=40, seed=7):
    d = ImageDraw.Draw(img)
    for i in range(n):
        x = (i * 263 + seed * 97) % W; y = (i * 389 + seed * 53) % (H - 200) + 60
        tw = 0.5 + 0.5 * math.sin(t * 3 + i * 1.7); r = 4 + 5 * tw
        a = int(90 + 140 * tw)
        d.polygon([(x, y - r * 2), (x + r * .5, y - r * .5), (x + r * 2, y), (x + r * .5, y + r * .5), (x, y + r * 2),
                   (x - r * .5, y + r * .5), (x - r * 2, y), (x - r * .5, y - r * .5)], fill=rgba(col, a))


def moon(img, cx, cy, r, col, bgc):
    disc(img, cx, cy, r, col); disc(img, cx + r * .45, cy - r * .3, r * .85, bgc)


def p_hook(t, b, prev):
    img = bg(NIGHT); stars(img, t)
    moon(img, 820, 330, 120, BUTTER, NIGHT)
    put(img, TB("রাতে টিকটিক শব্দে", 700, 104, WHITE, True), W / 2, 640, scale=1.35 - .35 * ease(t / .22), a=clamp(t / .1))
    kk = (t - .35) / .25
    if kk > 0: put(img, TB("ঘুম ভাঙে?", 700, 170, BUTTER, True), W / 2, 830, scale=1.3 - .3 * ease(kk), a=clamp(kk * 2))
    words = [(250, 1150, -12, .7), (800, 1240, 10, 1.0), (330, 1420, 8, 1.3), (760, 1520, -9, 1.6)]
    for i, (x, y, rot, st) in enumerate(words):
        k = back((t - st) / .22)
        if k > 0:
            put(img, pill("TICK" if i % 2 == 0 else "TOCK", 64, LILAC if i % 2 == 0 else CORAL, NIGHT, padx=40), x, y, scale=k, rot=rot + 4 * math.sin(t * 9 + i))
    logo(img); return img


FEATS = ["Non ticking, silent operation", "Precise quartz movement", "Classic twin bell design"]


def p_clock(t, b, prev):
    img = bg(CREAM); d = ImageDraw.Draw(img)
    d.rectangle((0, 0, W, 980), fill=rgba(NIGHT)); stars(img, t, n=16, seed=3)
    # struck tick tock
    k0 = back(t / .3)
    put(img, pill("TICK TOCK", 70, CORAL, NIGHT, padx=50), W / 2, 230, scale=k0)
    ks = ease((t - .4) / .3)
    if ks > 0:
        ov = Image.new("RGBA", (W, H), (0, 0, 0, 0)); od = ImageDraw.Draw(ov)
        od.line((W / 2 - 230, 270, W / 2 - 230 + 460 * ks, 190), fill=rgba(WHITE), width=16)
        img.alpha_composite(ov)
    kc = back((t - .7) / .4)
    disc(img, W / 2, 640, 280 * kc, NIGHT2)
    if kc > 0: put(img, P(CLK, 420, 420), W / 2, 650 + 8 * math.sin(t * 3), scale=kc, rot=3 * math.sin(t * 2))
    kt = back((t - 1.2) / .35)
    if kt > 0: put(img, pill("SILENT ALARM CLOCK", 56, BUTTER, NIGHT, padx=50), W / 2, 975, scale=kt)
    for i, fe in enumerate(FEATS):
        st = 2.0 + 0.8 * i; kk = ease((t - st) / .3)
        if kk <= 0: continue
        y = 1160 + i * 200
        ov = Image.new("RGBA", (W, 140), (0, 0, 0, 0)); od = ImageDraw.Draw(ov)
        od.rounded_rectangle((90, 0, W - 90, 128), radius=36, fill=rgba(WHITE), outline=rgba(NIGHT), width=6)
        od.ellipse((128, 34, 188, 94), fill=rgba(LILAC))
        od.line([(142, 64), (155, 78), (176, 50)], fill=rgba(NIGHT), width=8)
        img.alpha_composite(ov, (int(-200 * (1 - kk)), y))
        fz = 46
        while f("Poppins-Bold.ttf", fz).getlength(fe) > 700 and fz > 30: fz -= 2
        put(img, T(fe, f("Poppins-Bold.ttf", fz), NIGHT), W / 2 + 50 - 200 * (1 - kk), y + 64, a=kk)
    logo(img); return wipe(img, prev, t, CREAM)


def p_teddy(t, b, prev):
    img = bg(LILAC); stars(img, t, col=WHITE, n=22, seed=11)
    put(img, TB("আর ঘুমের সঙ্গী", 700, 116, NIGHT), W / 2, 330, scale=back(t / .35))
    k = back((t - .3) / .45)
    disc(img, W / 2, 900, 360 * k, CREAM)
    if k > 0: put(img, P(TED, 560, 600), W / 2, 920 + 10 * math.sin(t * 3), scale=k)
    for i, (txt, x, y, fill, col, rot) in enumerate([("22 INCH", 250, 1380, NIGHT, BUTTER, -5), ("SUPER SOFT PLUSH", 700, 1500, BUTTER, NIGHT, 4)]):
        kk = back((t - 1.0 - .4 * i) / .35)
        if kk > 0: put(img, pill(txt, 54, fill, col, padx=44), x, y, scale=kk, rot=rot)
    logo(img); return wipe(img, prev, t, LILAC)


def _price_card(name, price, reg, fill, col):
    card = Image.new("RGBA", (460, 330), (0, 0, 0, 0)); cd = ImageDraw.Draw(card)
    cd.rounded_rectangle((0, 0, 459, 329), radius=44, fill=rgba(fill), outline=rgba(NIGHT), width=7)
    nf = f("Poppins-Bold.ttf", 42)
    nt = T(name, nf, col); card.alpha_composite(nt, (230 - nt.width // 2, 30))
    pt = T(f"Tk {price:,}", f("Poppins-Bold.ttf", 96), col); card.alpha_composite(pt, (230 - pt.width // 2, 105))
    rt = f"Regular Tk {reg:,}"; rf_ = f("Poppins-Medium.ttf", 36); rw = rf_.getlength(rt)
    cd.text((230 - rw / 2, 250), rt, font=rf_, fill=rgba(col)); cd.line((230 - rw / 2 - 4, 273, 230 + rw / 2 + 4, 273), fill=rgba(col), width=4)
    return card


def p_price(t, b, prev):
    img = bg(BUTTER)
    put(img, TB("দাম কত?", 700, 124, NIGHT), W / 2, 300, scale=back(t / .35))
    put(img, P(CLK, 300, 300), 285, 720 + 10 * math.sin(t * 4), scale=back((t - .1) / .4))
    put(img, P(TED, 330, 360), 795, 720 + 10 * math.sin(t * 4 + 1), scale=back((t - .2) / .4))
    k1 = back((t - .6) / .35); k2 = back((t - 1.0) / .35)
    if k1 > 0: put(img, _price_card("Silent Clock", 500, 800, WHITE, NIGHT), 285, 1170, scale=k1, rot=3)
    if k2 > 0: put(img, _price_card("22\" Teddy", 1150, 2000, NIGHT, WHITE), 795, 1170, scale=k2, rot=-3)
    logo(img); return wipe(img, prev, t, BUTTER)


def p_vote(t, b, prev):
    img = bg(NIGHT); stars(img, t)
    put(img, TB("আজ রাতে কোনটা চাই?", 700, 96, WHITE, True), W / 2, 560, scale=back(t / .35))
    k = back((t - .4) / .35)
    if k > 0:
        put(img, pill("1  =  Silent Clock", 70, BUTTER, NIGHT, padx=56), W / 2, 860, scale=k, rot=-3)
        put(img, pill("2  =  Teddy Bear", 70, LILAC, NIGHT, padx=56), W / 2, 1060, scale=back((t - .6) / .35), rot=3)
    kk = back((t - 1.1) / .35)
    if kk > 0: put(img, TB("কমেন্টে লিখুন ১ না ২", 700, 80, BUTTER), W / 2, 1320, scale=kk)
    logo(img); return wipe(img, prev, t, NIGHT)


REELS = [
    dict(id="reel-good-night-silent-clock-teddy", time="18:30", music=("upbeat", 3), b=UB, cover=1900,
         scenes=[(p_hook, 5), (p_clock, 12), (p_teddy, 8), (p_price, 8), (p_vote, 6),
                 (end_card([(CLK, HQ), (TED, HQ)], NIGHT2, BUTTER, "Sleep tight, Dhaka"), 7)]),
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
