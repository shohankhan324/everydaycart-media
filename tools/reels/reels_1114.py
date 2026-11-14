"""Everyday Cart Reel for 14 Nov: Elephant plush "bedtime buddy" (Bangla hook on a flat night sky, elephant drops onto
a cloud, 18 inch size ruler, gift box pop, price reveal, end card). Indigo + peach + lavender palette,
original gentle track in a new key."""
import os as _os
_R = _os.path.dirname(_os.path.abspath(__file__)); _T = _os.path.dirname(_R)

import os, sys, math
import numpy as np
from PIL import Image, ImageDraw
sys.path.insert(0, _T); sys.path.insert(0, _R)
from mega import T, TB, P, pill, bg, wipe, logo, rays, disc, put, rgba, f, ease, back, clamp, confetti, HQ, DARK, WHITE
import reels9 as R9
from reels9 import end_card

W, H = 1080, 1920
R9.OUT = _R + "/out/out1114/"; os.makedirs(R9.OUT, exist_ok=True)
IND = (44, 40, 104); IND2 = (62, 58, 132); PEACH = (255, 198, 170); LAV = (226, 218, 255); CRM = (255, 247, 240)
GOLD = (255, 222, 140); PINK = (246, 140, 170)
PROD = "25.png"
RNG = np.random.default_rng(14)
STARS = [(RNG.uniform(40, W - 40), RNG.uniform(120, 1250), RNG.uniform(0, 6.28), int(RNG.integers(3, 7))) for _ in range(46)]


def sky(img, t, col=WHITE):
    d = ImageDraw.Draw(img)
    for x, y, ph, r in STARS:
        a = int(110 + 120 * (0.5 + 0.5 * math.sin(t * 2.2 + ph)))
        d.polygon([(x, y - r * 2), (x + r * .6, y - r * .6), (x + r * 2, y), (x + r * .6, y + r * .6), (x, y + r * 2),
                   (x - r * .6, y + r * .6), (x - r * 2, y), (x - r * .6, y - r * .6)], fill=rgba(col, a))


def moon(img, cx, cy, r, bgc):
    disc(img, cx, cy, r, GOLD); disc(img, cx + r * .45, cy - r * .3, r * .9, bgc)


def cloud(img, cx, cy, s, col):
    d = ImageDraw.Draw(img)
    for dx, dy, rr in [(-1.1, .15, .55), (-.45, -.25, .75), (.35, -.35, .8), (1.05, .1, .6)]:
        d.ellipse((cx + dx * s - rr * s, cy + dy * s - rr * s, cx + dx * s + rr * s, cy + dy * s + rr * s), fill=rgba(col))
    d.rounded_rectangle((cx - 1.65 * s, cy - .05 * s, cx + 1.65 * s, cy + .62 * s), radius=int(.3 * s), fill=rgba(col))


def zzz(img, x, y, t):
    for k in range(3):
        ph = (t * .6 + k / 3) % 1
        put(img, T("z", f("Poppins-Bold.ttf", 46 + k * 16), GOLD), x + ph * 90 + k * 20, y - ph * 200 - k * 40, a=clamp(1 - ph) * .9)


def s_hook(t, b, prev):
    img = bg(IND); sky(img, t); moon(img, 170, 220, 85, IND)
    put(img, TB("ঘুমের নতুন বন্ধু", 700, 120, WHITE), W / 2, 430, scale=1.25 - .25 * ease(t / .3), a=clamp(t / .12))
    kk = ease((t - .5) / .35)
    if kk > 0: put(img, T("Meet the bedtime buddy", f("Poppins-Bold.ttf", 66), PEACH), W / 2, 580 + 30 * (1 - kk), a=kk)
    cloud(img, W / 2, 1420, 230, IND2)
    k = back(min(1, t / .55))
    put(img, P(PROD, 700, 760), W / 2, 1120 - 900 * (1 - k) + 10 * math.sin(t * 2.4), a=clamp(t / .1))
    if t > 3 * b: zzz(img, W / 2 + 250, 820, t - 3 * b)
    kk = back((t - 4 * b) / .35)
    if kk > 0: put(img, pill("Elephant Plush Soft Toy", 50, PEACH, IND, padx=46), W / 2, 1720, scale=kk)
    logo(img); return img


def s_size(t, b, prev):
    img = bg(LAV)
    disc(img, W / 2 - 80, 1050, 420, (238, 232, 255))
    put(img, T("Big and huggable", f("Poppins-Bold.ttf", 84), IND), W / 2, 300, a=clamp(t / .2))
    put(img, TB("জড়িয়ে ধরার মতো সফট টয়", 700, 66, PINK), W / 2, 420, a=clamp((t - .3) / .3))
    put(img, P(PROD, 620, 740), W / 2 - 110, 1060 + 6 * math.sin(t * 2.4), scale=.85 + .15 * back(t / .5))
    # ruler grows next to the toy
    d = ImageDraw.Draw(img); x = 860; y1 = 1430; full = 740; k = ease((t - 1.0 * b) / .9); top = y1 - full * k
    if k > 0:
        d.rounded_rectangle((x - 46, top, x + 46, y1), radius=20, fill=rgba(GOLD))
        for i in range(19):
            yy = y1 - i * full / 18
            if yy < top + 8: break
            w_ = 34 if i % 6 == 0 else 18
            d.line((x - 46, yy, x - 46 + w_, yy), fill=rgba(IND), width=5)
        n = int(round(18 * k))
        put(img, pill(f'{n}"', 64, IND, WHITE, padx=34), x, top - 70)
    kk = back((t - 4.5 * b) / .35)
    if kk > 0: put(img, pill("18 inch  •  Super soft", 52, IND, WHITE, padx=46), W / 2, 1640, scale=kk)
    logo(img); return wipe(img, prev, t, LAV, W / 2, 1100)


def gift_box(img, cx, cy, s, lid_k, col, rib):
    d = ImageDraw.Draw(img)
    d.rectangle((cx - s, cy - s * .2, cx + s, cy + s * .9), fill=rgba(col))
    d.rectangle((cx - s * .14, cy - s * .2, cx + s * .14, cy + s * .9), fill=rgba(rib))
    ly = cy - s * .2 - 1700 * lid_k; cx = cx + 500 * lid_k
    d.rectangle((cx - s * 1.1, ly - s * .28, cx + s * 1.1, ly), fill=rgba(col))
    d.rectangle((cx - s * .14, ly - s * .28, cx + s * .14, ly), fill=rgba(rib))
    d.ellipse((cx - s * .5, ly - s * .62, cx - s * .02, ly - s * .26), outline=rgba(rib), width=22)
    d.ellipse((cx + s * .02, ly - s * .62, cx + s * .5, ly - s * .26), outline=rgba(rib), width=22)


def s_gift(t, b, prev):
    img = bg(PEACH); rays(img, W / 2, 1000, t, WHITE, a=40)
    put(img, T("A sweet gift", f("Poppins-Bold.ttf", 96), IND), W / 2, 290, a=clamp(t / .2))
    put(img, T("for kids and loved ones", f("Poppins-Bold.ttf", 58), (150, 70, 90)), W / 2, 400, a=clamp((t - .25) / .3))
    open_k = ease((t - 1.5 * b) / .5)
    pop = back((t - 2.0 * b) / .5)
    gift_box(img, W / 2, 1300, 260, open_k, IND, GOLD)
    if pop > 0:
        put(img, P(PROD, 560, 640), W / 2, 1180 - 380 * min(pop, 1.1), scale=.4 + .6 * min(pop, 1))
        confetti(img, t - 2.0 * b, seed=21, n=50)
    kk = ease((t - 4 * b) / .35)
    if kk > 0: put(img, TB("জন্মদিনের উপহারে নরম তুলতুলে বন্ধু", 700, 60, IND), W / 2, 1720, a=kk)
    logo(img); return wipe(img, prev, t, PEACH)


def s_price(t, b, prev):
    img = bg(IND); sky(img, t, LAV); moon(img, 190, 260, 80, IND)
    cloud(img, W / 2, 1000, 210, IND2)
    put(img, P(PROD, 520, 600), W / 2, 760 + 8 * math.sin(t * 2.4), scale=back(t / .4))
    kk = ease((t - 1.2 * b) / .3)
    if kk > 0: put(img, TB("সফট টয় মাত্র", 700, 80, PEACH), W / 2, 1240, a=kk)
    kk = back((t - 2.2 * b) / .35)
    if kk > 0:
        put(img, T("Tk 750", f("Poppins-Bold.ttf", 200), GOLD), W / 2, 1420, scale=kk)
        col = (180, 176, 220); rt = T("Tk 1,100", f("Poppins-Regular.ttf", 64), col); put(img, rt, W / 2, 1580, a=clamp(kk))
        d = ImageDraw.Draw(img); d.line((W / 2 - rt.width / 2 + 20, 1584, W / 2 + rt.width / 2 - 20, 1584), fill=rgba(col), width=6)
    kk = back((t - 3.6 * b) / .35)
    if kk > 0: put(img, pill("Inbox us to order", 50, PEACH, IND, padx=50), W / 2, 1730, scale=kk)
    logo(img); return wipe(img, prev, t, IND)


G = 60 / 92
REELS = [
    dict(id="reel-elephant-bedtime-buddy", time="18:30", music=("gentle", 2), b=G, cover=1900,
         scenes=[(s_hook, 7), (s_size, 8), (s_gift, 8), (s_price, 7),
                 (end_card([(PROD, HQ), ("06.png", HQ)], IND2, PEACH, "Soft hugs, sweet dreams"), 5)]),
]

if __name__ == "__main__":
    mode = sys.argv[1]
    for r in REELS:
        if mode == "preview":
            parts, starts, total = R9.build(r, True); print(r["id"], round(total, 1)); shots = []
            for (fn, dur), st in zip(parts, starts):
                for fr in (.15, .5, .95): shots.append(fn(min(dur * fr, dur - .1)).convert("RGB"))
            cols = 5; rows = math.ceil(len(shots) / cols); sheet = Image.new("RGB", (cols * 270, rows * 480), "white")
            for i, s_ in enumerate(shots): sheet.paste(s_.resize((270, 480), Image.LANCZOS), ((i % cols) * 270, (i // cols) * 480))
            sheet.save(sys.argv[2], quality=86)
        else:
            R9.build(r)
