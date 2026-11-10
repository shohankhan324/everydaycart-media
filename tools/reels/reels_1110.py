"""Everyday Cart Reel for 10 Nov: Proove Intro Pro "guess the price" (Bangla hook, drop, feature cards,
A/B/C guess with countdown and reveal, end card). Violet + lime palette, original drive track in a new key."""
import os as _os
_R = _os.path.dirname(_os.path.abspath(__file__)); _T = _os.path.dirname(_R)

import os, sys, math
from PIL import Image, ImageDraw
sys.path.insert(0, _T); sys.path.insert(0, _R)
from mega import T, TB, P, pill, bg, wipe, logo, rays, disc, put, rgba, f, ease, back, clamp, confetti, HQ, DARK, WHITE, _tc
import reels9 as R9
from reels9 import end_card
import drive as DR

W, H = 1080, 1920
R9.OUT = _R + "/out/out1110/"; os.makedirs(R9.OUT, exist_ok=True)
VIO = (44, 24, 92); VIO2 = (70, 40, 140); LIME = (196, 240, 72); PINK = (255, 112, 150)
PROD = "03.png"


def bars(img, t, col, y0=H, n=11):
    """Flat equaliser bars along the bottom edge."""
    d = ImageDraw.Draw(img); bw = W / (n * 2)
    for i in range(n):
        h = 40 + 80 * abs(math.sin(t * 5 + i * .9))
        x = bw / 2 + i * 2 * bw; d.rounded_rectangle((x, y0 - h, x + bw, y0), radius=int(bw / 2), fill=rgba(col))


def p_hook(t, b, prev):
    img = bg(VIO); bars(img, t, (60, 36, 116))
    put(img, TB("এই ইয়ারবাডের দাম", 700, 120, WHITE, True), W / 2, 640, scale=1.3 - .3 * ease(t / .25), a=clamp(t / .15))
    kk = (t - b) / .3
    if kk > 0: put(img, TB("কত হতে পারে?", 700, 150, LIME, True), W / 2, 830, scale=1.3 - .3 * ease(kk), a=clamp(kk * 2))
    kk = back((t - 2.5 * b) / .35)
    if kk > 0: put(img, pill("GUESS THE PRICE", 56, PINK, WHITE, padx=50), W / 2, 1080, scale=kk)
    kk = (t - 3.5 * b) / .3
    if kk > 0: put(img, TB("কমেন্টে আপনার উত্তর দিন", 600, 58, (210, 200, 240)), W / 2, 1220, a=clamp(kk))
    kk = back((t - .2) / .4)
    if kk > 0:
        disc(img, W / 2, 1560, 230, (66, 40, 128))
        put(img, P(PROD, 380, 380), W / 2, 1560 + 10 * math.sin(t * 3), scale=kk)
        kq = back((t - .5) / .3)
        if kq > 0:
            disc(img, W / 2 + 230, 1400, 95 * kq, LIME); put(img, T("?", f("Poppins-Bold.ttf", 140), VIO), W / 2 + 230, 1400, scale=kq)
    logo(img); return img


def p_drop(t, b, prev):
    img = bg(VIO2); rays(img, W / 2, 1050, t, LIME, a=18)
    disc(img, W / 2, 1050, 380, (88, 56, 160))
    k = back(t / .45)
    put(img, P(PROD, 820, 820), W / 2, 1050 - 700 * (1 - min(1, k)) + 10 * math.sin(t * 3), a=clamp(t / .15))
    kk = ease((t - .4) / .4)
    put(img, T("Proove Intro Pro", f("Poppins-Bold.ttf", 110), WHITE, True), W / 2, 330 + 30 * (1 - kk), a=kk)
    put(img, T("TWS Earbuds  •  Official", f("Poppins-Medium.ttf", 46), LIME), W / 2, 450, a=clamp((t - .6) / .3))
    logo(img); return wipe(img, prev, t, VIO2, W / 2, 1050)


FEATS = [("13mm", "Driver, powerful sound"), ("BT 5.4", "Touch control"), ("ENC", "Clear calls"), ("LED", "Display case")]
def p_feats(t, b, prev):
    img = bg(VIO); bars(img, t, (58, 34, 112))
    put(img, P(PROD, 600, 600), W / 2, 600 + 8 * math.sin(t * 3))
    for i, (big, small) in enumerate(FEATS):
        kk = back((t - i * 1.5 * b) / .3)
        if kk <= 0: continue
        cx = 285 + (i % 2) * 510; cy = 1180 + (i // 2) * 290
        key = ("pf10", i); card = _tc.get(key)
        if card is None:
            card = Image.new("RGBA", (470, 250), (0, 0, 0, 0)); d = ImageDraw.Draw(card)
            d.rounded_rectangle((0, 0, 469, 249), radius=36, fill=rgba(LIME if i in (0, 3) else WHITE))
            bt = T(big, f("Poppins-Bold.ttf", 80), VIO); card.alpha_composite(bt, (235 - bt.width // 2, 44))
            st = T(small, f("Poppins-Medium.ttf", 36), (70, 60, 100)); card.alpha_composite(st, (235 - st.width // 2, 160)); _tc[key] = card
        put(img, card, cx, cy, scale=kk)
    logo(img); return wipe(img, prev, t, VIO)


def p_guess(t, b, prev):
    BGc = (24, 14, 56); img = bg(BGc); rays(img, W / 2, 740, t, PINK, a=20)
    put(img, T("So, what's the price?", f("Poppins-Bold.ttf", 70), WHITE, True), W / 2, 220)
    put(img, TB("দাম আন্দাজ করুন", 700, 56, LIME), W / 2, 315)
    put(img, P(PROD, 620, 460), W / 2, 720 + 12 * math.sin(t * 3), scale=back(t / .45))
    opts = [("A", "Tk 3,500"), ("B", "Tk 2,300"), ("C", "Tk 1,500")]; reveal = 12 * b; right = 1
    for i, (l, v) in enumerate(opts):
        kk = back((t - (1.5 + i) * b) / .35)
        if kk <= 0: continue
        ok = i == right and t > reveal; dim = i != right and t > reveal
        card = Image.new("RGBA", (300, 130), (0, 0, 0, 0)); d = ImageDraw.Draw(card)
        d.rounded_rectangle((0, 0, 299, 129), radius=30, fill=rgba(LIME) if ok else ((255, 255, 255, 80) if dim else (255, 255, 255, 255)))
        d.text((26, 30), l, font=f("Poppins-Bold.ttf", 52), fill=rgba(VIO)); d.text((88, 38), v, font=f("Poppins-Bold.ttf", 44), fill=rgba(VIO))
        put(img, card, 180 + i * 360, 1140, scale=kk * (1 + .12 * math.exp(-(t - reveal) * 6)) if ok else kk)
    for n in range(3):
        s = (6 + 2 * n) * b
        if s <= t < s + 2 * b:
            k = (t - s) / (2 * b); put(img, T(str(3 - n), f("Poppins-Bold.ttf", 260), WHITE, True), W / 2, 1480, scale=1.6 - .6 * ease(k * 3), a=clamp(1.3 - k))
    if t > reveal:
        put(img, T("Tk 2,300", f("Poppins-Bold.ttf", 160), LIME, True), W / 2, 1460, scale=back((t - reveal) / .35))
        kk = (t - reveal - .4) / .3
        if kk > 0: put(img, pill("Did you get it? Tell us in the comments", 36, WHITE, BGc), W / 2, 1650, a=clamp(kk))
        confetti(img, t - reveal, seed=10)
    logo(img); return wipe(img, prev, t, BGc)


REELS = [
    dict(id="proove-guess-price", time="18:30", music=("drive", 2), b=DR.B, cover=2500,
         scenes=[(p_hook, 6), (p_drop, 6), (p_feats, 10), (p_guess, 16),
                 (end_card([(PROD, HQ), ("10.png", HQ), ("13.png", HQ)], VIO, LIME, "Sound that fits your day"), 6)]),
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
