"""Everyday Cart Reel for 12 Nov: Oraimo SpaceBuds Lite "spec counter" (Bangla hook about 40 hours with the case,
product drop, 2x2 stat cards that count up, price reveal, end card). Navy + mint palette, original drive track in a new key."""
import os as _os
_R = _os.path.dirname(_os.path.abspath(__file__)); _T = _os.path.dirname(_R)

import os, sys, math
from PIL import Image, ImageDraw
sys.path.insert(0, _T); sys.path.insert(0, _R)
from mega import T, TB, P, pill, bg, wipe, logo, rays, disc, put, rgba, f, ease, back, clamp, confetti, HQ, DARK, WHITE
import reels9 as R9
from reels9 import end_card
import drive as DR

W, H = 1080, 1920
R9.OUT = _R + "/out/out1112/"; os.makedirs(R9.OUT, exist_ok=True)
NAVY = (18, 30, 78); NAVY2 = (32, 50, 116); MINT = (92, 230, 182); CRM = (240, 250, 246)
PROD = "13.png"


def dots(img, t, col):
    d = ImageDraw.Draw(img)
    for i in range(16):
        x = (i * 197 + 40) % W; y = (i * 283 - t * 45 * (1 + i % 3)) % H
        r = 5 + (i % 3) * 4; d.ellipse((x - r, y - r, x + r, y + r), fill=rgba(col))


def p_hook(t, b, prev):
    img = bg(NAVY); dots(img, t, NAVY2)
    put(img, TB("কেসসহ ৪০ ঘণ্টা পর্যন্ত", 700, 108, MINT, True), W / 2, 540, scale=1.3 - .3 * ease(t / .25), a=clamp(t / .12))
    kk = (t - b) / .3
    if kk > 0: put(img, TB("গান চলবে এই ইয়ারবাডে?", 700, 88, WHITE, True), W / 2, 700, scale=1.25 - .25 * ease(kk), a=clamp(kk * 2))
    kk = back((t - 2.2 * b) / .35)
    if kk > 0:
        disc(img, W / 2, 1250, 360, NAVY2)
        put(img, P(PROD, 560, 560), W / 2, 1250 + 10 * math.sin(t * 3), scale=kk)
        kq = back((t - 3 * b) / .3)
        if kq > 0:
            disc(img, W / 2 + 300, 980, 100 * kq, MINT); put(img, T("?", f("Poppins-Bold.ttf", 140), NAVY), W / 2 + 300, 980, scale=kq)
    logo(img); return img


def p_drop(t, b, prev):
    img = bg(MINT); rays(img, W / 2, 1060, t, WHITE, a=30)
    disc(img, W / 2, 1060, 390, (150, 242, 208))
    k = back(t / .45)
    put(img, P(PROD, 740, 740), W / 2, 1060 - 700 * (1 - min(1, k)) + 10 * math.sin(t * 3), a=clamp(t / .15))
    kk = ease((t - .4) / .4)
    put(img, T("Oraimo SpaceBuds Lite", f("Poppins-Bold.ttf", 86), NAVY, False), W / 2, 330 + 30 * (1 - kk), a=kk)
    put(img, T("Wireless Earbuds  •  Official", f("Poppins-Medium.ttf", 48), NAVY2), W / 2, 450, a=clamp((t - .6) / .3))
    put(img, TB("দেখে নিন স্পেকস!", 700, 72, NAVY), W / 2, 1600, a=clamp((t - .9) / .3))
    logo(img); return wipe(img, prev, t, MINT, W / 2, 1060)


# (big value, counter target or None, unit, English label, Bangla sub)
STATS = [("40", 40, "H", "Playback with case", "কেসসহ পর্যন্ত"), ("5.4", None, "", "Bluetooth", "সহজ কানেকশন"),
         ("IPX4", None, "", "Water resistant", "পানি প্রতিরোধী"), ("AI", None, "", "Call noise cancel", "কলে নয়েজ কমায়")]
def p_stats(t, b, prev):
    img = bg(CRM)
    put(img, TB("এক নজরে স্পেকস", 700, 76, NAVY), W / 2, 230, a=clamp(t / .2))
    disc(img, W / 2, 560, 250, (206, 240, 228))
    put(img, P(PROD, 400, 400), W / 2, 560 + 8 * math.sin(t * 3))
    for i, (val, num, unit, en, bn) in enumerate(STATS):
        st = (1.2 + i * 2.0) * b; kk = back((t - st) / .32)
        if kk <= 0: continue
        cx = W / 2 + (-235 if i % 2 == 0 else 235); cy = 1000 + (i // 2) * 420
        card = Image.new("RGBA", (440, 380), (0, 0, 0, 0)); d = ImageDraw.Draw(card)
        d.rounded_rectangle((0, 0, 439, 379), radius=44, fill=rgba(NAVY if i in (0, 3) else WHITE))
        fg = MINT if i in (0, 3) else NAVY; sub = WHITE if i in (0, 3) else (90, 96, 120)
        if num is not None:
            v = int(round(num * ease((t - st) / (1.2 * b))))
            txt = f"{max(0, min(num, v))}{unit}"
        else:
            txt = val
        tv = T(txt, f("Poppins-Bold.ttf", 120 if len(txt) <= 4 else 100), fg)
        card.alpha_composite(tv, (int(220 - tv.width / 2), 40))
        te = T(en, f("Poppins-Bold.ttf", 38), sub); card.alpha_composite(te, (int(220 - te.width / 2), 210))
        tb = TB(bn, 600, 40, fg); card.alpha_composite(tb, (int(220 - tb.width / 2), 270))
        put(img, card, cx, cy, scale=kk)
    logo(img); return wipe(img, prev, t, CRM)


def p_price(t, b, prev):
    img = bg(NAVY); rays(img, W / 2, 900, t, MINT, a=22)
    put(img, P(PROD, 560, 520), W / 2, 640 + 10 * math.sin(t * 3), scale=back(t / .4))
    kk = ease((t - 1.5 * b) / .3)
    if kk > 0: put(img, TB("দাম মাত্র", 700, 90, WHITE, True), W / 2, 1060, a=kk)
    kk = back((t - 2.5 * b) / .35)
    if kk > 0:
        put(img, T("Tk 1,310", f("Poppins-Bold.ttf", 190), MINT, True), W / 2, 1260, scale=kk)
        rt = T("Tk 1,496", f("Poppins-Regular.ttf", 64), (170, 182, 214)); put(img, rt, W / 2, 1420, a=clamp(kk))
        d = ImageDraw.Draw(img); d.line((W / 2 - rt.width / 2 + 20, 1424, W / 2 + rt.width / 2 - 20, 1424), fill=rgba((170, 182, 214)), width=6)
        confetti(img, t - 2.5 * b, seed=12)
    kk = back((t - 4 * b) / .35)
    if kk > 0: put(img, pill("Inbox us to order", 50, WHITE, NAVY, padx=50), W / 2, 1590, scale=kk)
    logo(img); return wipe(img, prev, t, NAVY)


REELS = [
    dict(id="reel-oraimo-spacebuds-lite-specs", time="18:30", music=("drive", -2), b=DR.B, cover=3000,
         scenes=[(p_hook, 7), (p_drop, 6), (p_stats, 11), (p_price, 9),
                 (end_card([(PROD, HQ), ("11.png", HQ), ("03.png", HQ)], NAVY2, MINT, "Spatial sound, smart price"), 6)]),
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
