"""Everyday Cart Reel for 9 Nov: Awei KA5 20W speaker spotlight (Bangla hook, drop, feature beats, price, end card)."""
import os as _os
_R = _os.path.dirname(_os.path.abspath(__file__)); _T = _os.path.dirname(_R)

import os, sys, math
import numpy as np
from PIL import Image, ImageDraw
sys.path.insert(0, _T); sys.path.insert(0, _R)
from mega import T, TB, P, pill, bg, wipe, logo, rays, disc, put, rgba, f, ease, back, clamp, HQ, DARK, WHITE, _tc
import reels9 as R9
from reels9 import end_card
import drive as DR

W, H = 1080, 1920
R9.OUT = _R + "/out/out1109/"; os.makedirs(R9.OUT, exist_ok=True)
DEEP = (10, 52, 64); SEA = (18, 80, 96); AMBER = (255, 186, 64); CORAL2 = (240, 104, 84)


def rings(img, cx, cy, t, col, n=4):
    """Flat sound rings pulsing out from the speaker."""
    ov = Image.new("RGBA", img.size, (0, 0, 0, 0)); d = ImageDraw.Draw(ov)
    for i in range(n):
        ph = (t * 0.9 + i / n) % 1.0; r = 260 + ph * 520
        a = int(110 * (1 - ph)); d.ellipse((cx - r, cy - r, cx + r, cy + r), outline=col + (a,), width=6)
    img.alpha_composite(ov)


def eq(img, t, col, y1=H, n=13):
    d = ImageDraw.Draw(img); bw = W / (n * 2)
    for i in range(n):
        h = 50 + 90 * abs(math.sin(t * 6 + i * .8))
        x = bw / 2 + i * 2 * bw; d.rounded_rectangle((x, y1 - h, x + bw, y1), radius=int(bw / 2), fill=rgba(col))


def tb_pill(text, size, fill, col):
    k = ("tbp9", text, size, fill, col)
    if k not in _tc:
        tx = TB(text, 700, size, col); w, h = tx.width + 80, int(size * 1.9)
        s = Image.new("RGBA", (w, h), (0, 0, 0, 0)); ImageDraw.Draw(s).rounded_rectangle((0, 0, w - 1, h - 1), radius=h // 2, fill=rgba(fill))
        s.alpha_composite(tx, ((w - tx.width) // 2, (h - tx.height) // 2)); _tc[k] = s
    return _tc[k]


def k_hook(t, b, prev):
    img = bg(DEEP); eq(img, t, (24, 78, 92))
    put(img, TB("আড্ডা জমাতে", 700, 140, WHITE, True), W / 2, 640, scale=1.3 - .3 * ease(t / .3), a=clamp(t / .2))
    kk = (t - b) / .3
    if kk > 0: put(img, TB("চাই জোরালো সাউন্ড?", 700, 104, AMBER, True), W / 2, 830, scale=1.3 - .3 * ease(kk), a=clamp(kk * 2))
    kk = back((t - 2.5 * b) / .35)
    if kk > 0: put(img, pill("20W PORTABLE SPEAKER", 48, CORAL2, WHITE, padx=44), W / 2, 1120, scale=kk)
    logo(img); return img


def k_drop(t, b, prev):
    img = bg(SEA); rings(img, W / 2, 1060, t, AMBER)
    k = back(t / .45)
    put(img, P("14.png", 900, 900), W / 2, 1060 - 700 * (1 - min(1, k)) + 10 * math.sin(t * 3), a=clamp(t / .15))
    kk = ease((t - .4) / .4)
    put(img, T("Awei KA5", f("Poppins-Bold.ttf", 120), WHITE, True), W / 2, 330 + 30 * (1 - kk), a=kk)
    put(img, T("20W Portable Bluetooth Speaker", f("Poppins-Medium.ttf", 46), AMBER), W / 2, 450, a=clamp((t - .6) / .3))
    logo(img); return wipe(img, prev, t, SEA, W / 2, 1060)


FEATS = [("10W x 2", "Output power"), ("2400mAh", "Battery"), ("IPX5", "Waterproof"), ("BT 5.3", "Bluetooth")]
def k_feats(t, b, prev):
    img = bg(DEEP); eq(img, t, (20, 70, 84))
    put(img, P("14.png", 640, 640), W / 2, 600 + 8 * math.sin(t * 3))
    for i, (big, small) in enumerate(FEATS):
        kk = back((t - i * 1.5 * b) / .3)
        if kk <= 0: continue
        cx = 285 + (i % 2) * 510; cy = 1180 + (i // 2) * 290
        key = ("kf", i); card = _tc.get(key)
        if card is None:
            card = Image.new("RGBA", (470, 250), (0, 0, 0, 0)); d = ImageDraw.Draw(card)
            d.rounded_rectangle((0, 0, 469, 249), radius=36, fill=rgba(WHITE if i % 3 == 0 else AMBER))
            bt = T(big, f("Poppins-Bold.ttf", 76), DEEP); card.alpha_composite(bt, (235 - bt.width // 2, 50))
            st = T(small, f("Poppins-Medium.ttf", 38), (60, 70, 80)); card.alpha_composite(st, (235 - st.width // 2, 160)); _tc[key] = card
        put(img, card, cx, cy, scale=kk)
    logo(img); return wipe(img, prev, t, DEEP)


def k_price(t, b, prev):
    img = bg(CORAL2); rays(img, W / 2, 780, t, WHITE, a=22)
    disc(img, W / 2, 780, 360 + 8 * math.sin(t * 2), (250, 130, 110))
    put(img, P("14.png", 560, 560), W / 2, 780 + 10 * math.sin(t * 3), scale=back(t / .4))
    put(img, TB("দাম মাত্র", 700, 80, WHITE, True), W / 2, 1270, a=clamp((t - .2) / .3))
    put(img, T("Tk 2,525", f("Poppins-Bold.ttf", 170), WHITE, True), W / 2, 1430, scale=back((t - .35) / .35))
    kk = clamp((t - .8) / .3)
    if kk > 0:
        a2 = T("Regular Tk 2,849", f("Poppins-Medium.ttf", 46), WHITE); put(img, a2, W / 2, 1570, a=kk)
        x0 = W / 2 - a2.width / 2 + T("Regular ", f("Poppins-Medium.ttf", 46), WHITE).width
        ImageDraw.Draw(img).line((x0, 1572, W / 2 + a2.width / 2 - 6, 1572), fill=(255, 255, 255, int(255 * kk)), width=4)
    kk = back((t - 1.2) / .35)
    if kk > 0: put(img, tb_pill("অর্ডার করতে ইনবক্স করুন", 54, DEEP, WHITE), W / 2, 1710, scale=kk)
    logo(img); return wipe(img, prev, t, CORAL2, W / 2, 780)


REELS = [
    dict(id="awei-ka5-spotlight", time="17:45", music=("drive", 4), b=DR.B, cover=5200,
         scenes=[(k_hook, 6), (k_drop, 6), (k_feats, 10), (k_price, 7),
                 (end_card([("14.png", HQ), ("09.png", HQ), ("04.png", HQ)], DEEP, AMBER, "Turn up the adda"), 6)]),
]

if __name__ == "__main__":
    mode = sys.argv[1]
    for r in REELS:
        if mode == "preview":
            parts, starts, total = R9.build(r, True); print(r["id"], round(total, 1)); shots = []
            for (fn, dur), st in zip(parts, starts):
                for fr in (.3, .9): shots.append(fn(min(dur * fr, dur - .1)).convert("RGB"))
            cols = 5; rows = math.ceil(len(shots) / cols); sheet = Image.new("RGB", (cols * 270, rows * 480), "white")
            for i, s_ in enumerate(shots): sheet.paste(s_.resize((270, 480), Image.LANCZOS), ((i % cols) * 270, (i // cols) * 480))
            sheet.save(sys.argv[2], quality=86)
        else:
            R9.build(r)
