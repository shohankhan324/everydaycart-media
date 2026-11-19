"""Everyday Cart Reel for 19 Nov: "Spot the difference: two earbuds under 1,000 Tk" (Awei T108 vs Awei T88).
Flat indigo + lime + pink palette. Bangla hook in the first second, both earbuds slide in with a VS badge;
spec rows reveal one by one on a split board (all specs from earlier store captions); twin price cards;
comment prompt; end card. Original drive track in key 2. About 21 s."""

import os as _os
_R = _os.path.dirname(_os.path.abspath(__file__)); _T = _os.path.dirname(_R)

import os, sys, math
from PIL import Image, ImageDraw
sys.path.insert(0, _T); sys.path.insert(0, _R)
from mega import T, TB, P, pill, bg, wipe, logo, disc, put, rgba, f, ease, back, clamp, HQ, DARK, WHITE
import reels9 as R9
from reels9 import end_card
import drive as DR

W, H = 1080, 1920
R9.OUT = _R + "/out/out1119/"; os.makedirs(R9.OUT, exist_ok=True)
IND = (36, 28, 86); IND2 = (54, 44, 120); LIME = (196, 240, 70); PINK = (255, 112, 150); CREAM = (255, 248, 236)
A, B_ = "10.png", "11.png"   # Awei T108, Awei T88


def dots(img, col, a=40, step=60, t=0):
    d = ImageDraw.Draw(img); off = (t * 30) % step
    for y in range(-step, H + step, step):
        for x in range(0, W + step, step):
            d.ellipse((x - 5 + ((y // step) % 2) * step / 2, y + off - 5, x + 5 + ((y // step) % 2) * step / 2, y + off + 5), fill=rgba(col, a))


def p_hook(t, b, prev):
    img = bg(IND); dots(img, LIME, 34, t=t)
    put(img, TB("১০০০ টাকার নিচে", 700, 118, WHITE, True), W / 2, 430, scale=1.35 - .35 * ease(t / .22), a=clamp(t / .1))
    kk = (t - .35) / .25
    if kk > 0: put(img, TB("দুইটা ইয়ারবাড", 700, 150, LIME, True), W / 2, 620, scale=1.3 - .3 * ease(kk), a=clamp(kk * 2))
    k = ease(clamp((t - .6) / .4))
    disc(img, 300, 1120, 230 * k, IND2); disc(img, 780, 1120, 230 * k, IND2)
    if k > 0:
        put(img, P(A, 380, 380), 300 - 700 * (1 - k), 1120 + 8 * math.sin(t * 4))
        put(img, P(B_, 300, 380), 780 + 700 * (1 - k), 1120 + 8 * math.sin(t * 4 + 1))
    kv = back((t - 1.0) / .3)
    if kv > 0:
        disc(img, W / 2, 1120, 92 * kv, PINK)
        put(img, T("VS", f("Poppins-Bold.ttf", 84), WHITE), W / 2, 1118, scale=kv, rot=-8)
    kk = back((t - 1.5) / .35)
    if kk > 0: put(img, pill("SPOT THE DIFFERENCE", 58, LIME, IND, padx=54), W / 2, 1520, scale=kk)
    logo(img); return img


ROWS = [("Bluetooth", "5.3", "5.4"), ("Calls / Noise", "ENC for calls", "ANC support"),
        ("Extra", "20h with case", "IPX6 water resistant"), ("Feature", "13mm drivers", "Touch control")]


def p_compare(t, b, prev):
    img = bg(CREAM); d = ImageDraw.Draw(img)
    d.rectangle((0, 0, W, 760), fill=rgba(IND))
    d.rectangle((W / 2 - 4, 120, W / 2 + 4, 700), fill=rgba(IND2))
    for cx, name, pr, sw in ((270, "Awei T108", A, 340), (810, "Awei T88", B_, 260)):
        disc(img, cx, 400, 200, IND2)
        put(img, P(pr, sw, 330), cx, 400 + 8 * math.sin(t * 3 + cx), scale=back(t / .35))
        put(img, T(name, f("Poppins-Bold.ttf", 56), LIME), cx, 660, a=ease(t / .3))
    for i, (lab, l, r) in enumerate(ROWS):
        st = (1.5 + 3.2 * i) * b; kk = ease((t - st) / .3)
        if kk <= 0: continue
        y = 830 + i * 220
        put(img, pill(lab.upper(), 30, IND, WHITE, padx=26), W / 2, y + 18, a=kk)
        ov = Image.new("RGBA", (W, 150), (0, 0, 0, 0)); od = ImageDraw.Draw(ov)
        od.rounded_rectangle((50, 0, W / 2 - 16, 140), radius=30, fill=(255, 255, 255, 255), outline=rgba(IND), width=5)
        od.rounded_rectangle((W / 2 + 16, 0, W - 50, 140), radius=30, fill=rgba(LIME), outline=rgba(IND), width=5)
        img.alpha_composite(ov, (0, int(y + 46 + 60 * (1 - kk))))
        for cx, txt in ((W / 4 + 17, l), (3 * W / 4 - 17, r)):
            fsz = 50
            while f("Poppins-Bold.ttf", fsz).getlength(txt) > 420 and fsz > 26: fsz -= 2
            put(img, T(txt, f("Poppins-Bold.ttf", fsz), IND), cx, y + 46 + 70 + 60 * (1 - kk), a=kk)
    logo(img); return wipe(img, prev, t, CREAM)


def _price_card(price, reg, fill, col, sub):
    card = Image.new("RGBA", (460, 330), (0, 0, 0, 0)); cd = ImageDraw.Draw(card)
    cd.rounded_rectangle((0, 0, 459, 329), radius=44, fill=rgba(fill), outline=rgba(IND), width=7)
    nt = T(sub, f("Poppins-Bold.ttf", 46), col); card.alpha_composite(nt, (230 - nt.width // 2, 30))
    pt = T(f"Tk {price:,}", f("Poppins-Bold.ttf", 98), col); card.alpha_composite(pt, (230 - pt.width // 2, 105))
    rt = f"Regular Tk {reg:,}"; rf_ = f("Poppins-Medium.ttf", 36); rw = rf_.getlength(rt)
    cd.text((230 - rw / 2, 250), rt, font=rf_, fill=rgba(col)); cd.line((230 - rw / 2 - 4, 273, 230 + rw / 2 + 4, 273), fill=rgba(col), width=4)
    return card


def p_price(t, b, prev):
    img = bg(LIME); dots(img, IND, 30, t=t)
    put(img, TB("দাম কত", 700, 120, IND), W / 2, 300, scale=back(t / .35))
    put(img, P(A, 330, 330), 285, 720 + 10 * math.sin(t * 4), scale=back((t - .1) / .4))
    put(img, P(B_, 260, 330), 795, 720 + 10 * math.sin(t * 4 + 1), scale=back((t - .2) / .4))
    k1 = back((t - .6) / .35); k2 = back((t - 1.0) / .35)
    if k1 > 0: put(img, _price_card(950, 1199, WHITE, IND, "Awei T108"), 285, 1160, scale=k1, rot=3)
    if k2 > 0: put(img, _price_card(990, 1450, IND, WHITE, "Awei T88"), 795, 1160, scale=k2, rot=-3)
    kk = back((t - 1.6) / .35)
    if kk > 0: put(img, pill("Both under Tk 1,000", 56, PINK, WHITE, padx=50), W / 2, 1560, scale=kk)
    logo(img); return wipe(img, prev, t, LIME)


def p_vote(t, b, prev):
    img = bg(PINK); dots(img, WHITE, 40, t=t)
    put(img, TB("আপনি কোনটা নেবেন", 700, 104, WHITE, True), W / 2, 560, scale=back(t / .35))
    k = back((t - .4) / .35)
    if k > 0:
        put(img, pill("1  =  T108", 76, WHITE, IND, padx=60), W / 2, 860, scale=k, rot=-3)
        put(img, pill("2  =  T88", 76, IND, WHITE, padx=60), W / 2, 1060, scale=back((t - .6) / .35), rot=3)
    kk = back((t - 1.1) / .35)
    if kk > 0: put(img, TB("কমেন্টে লিখুন", 700, 84, IND), W / 2, 1320, scale=kk)
    logo(img); return wipe(img, prev, t, PINK)


REELS = [
    dict(id="reel-earbuds-under-1000-spot-difference", time="18:30", music=("drive", 2), b=DR.B, cover=2300,
         scenes=[(p_hook, 6), (p_compare, 16), (p_price, 8), (p_vote, 6),
                 (end_card([(A, HQ), (B_, HQ), ("04.png", HQ)], IND, LIME, "Budget sound, sorted"), 8)]),
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
