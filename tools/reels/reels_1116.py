"""Everyday Cart Reel for 16 Nov: Portable Massage Gun "after a long day" (Bangla hook with a flat office clock racing
to 6 pm and an energy bar draining, product drop with flat pulse rings, 4 feature cards from the store listing, who it
is for, drum roll price reveal, end card). Plum + tangerine + cream palette, original drive track in a new key (5).
Under 25 s."""

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
R9.OUT = _R + "/out/out1116/"; os.makedirs(R9.OUT, exist_ok=True)
PLUM = (58, 22, 70); PLUM2 = (84, 34, 98); TAN = (255, 150, 60); CREAM = (255, 238, 214); RED = (255, 84, 84)
PROD = "31.png"


def clock(img, cx, cy, r, t, dur):
    """Flat wall clock whose hands race from 9 am to 6 pm."""
    d = ImageDraw.Draw(img)
    d.ellipse((cx - r - 16, cy - r - 16, cx + r + 16, cy + r + 16), fill=rgba(TAN))
    d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=rgba(CREAM))
    for i in range(12):
        a = math.radians(i * 30); r0 = r * (.78 if i % 3 else .70)
        d.line((cx + r0 * math.sin(a), cy - r0 * math.cos(a), cx + r * .88 * math.sin(a), cy - r * .88 * math.cos(a)),
               fill=rgba(PLUM), width=10 if i % 3 == 0 else 5)
    k = ease(clamp(t / dur)); hours = 9 + 9 * k   # 9:00 -> 18:00
    ha = math.radians((hours % 12) * 30); ma = math.radians((hours * 60 % 60) * 6)
    d.line((cx, cy, cx + r * .48 * math.sin(ha), cy - r * .48 * math.cos(ha)), fill=rgba(PLUM), width=18)
    d.line((cx, cy, cx + r * .74 * math.sin(ma), cy - r * .74 * math.cos(ma)), fill=rgba(TAN), width=10)
    d.ellipse((cx - 16, cy - 16, cx + 16, cy + 16), fill=rgba(PLUM))
    return hours


def energy(img, cx, cy, level):
    """Flat energy bar that drains (green -> orange -> red)."""
    d = ImageDraw.Draw(img); w, h = 520, 70
    d.rounded_rectangle((cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2), radius=35, fill=rgba(PLUM2))
    col = (120, 220, 120) if level > .6 else (TAN if level > .3 else RED)
    if level > .02: d.rounded_rectangle((cx - w / 2 + 10, cy - h / 2 + 10, cx - w / 2 + 10 + (w - 20) * level, cy + h / 2 - 10), radius=25, fill=rgba(col))


def p_hook(t, b, prev):
    img = bg(PLUM)
    dur = 6 * b
    hours = clock(img, W / 2, 1180, 250, t, dur)
    put(img, T(f"{int(hours) if hours < 13 else int(hours) - 12}:00 {'AM' if hours < 12 else 'PM'}", f("Poppins-Bold.ttf", 64), CREAM), W / 2, 1500)
    energy(img, W / 2, 1640, 1 - .92 * ease(clamp(t / dur)))
    put(img, TB("সারাদিন অফিসের পর", 700, 100, WHITE, True), W / 2, 470, scale=1.3 - .3 * ease(t / .25), a=clamp(t / .12))
    kk = (t - b) / .3
    if kk > 0: put(img, TB("শরীর ক্লান্ত?", 700, 150, TAN, True), W / 2, 660, scale=1.3 - .3 * ease(kk), a=clamp(kk * 2))
    kk = back((t - 6.3 * b) / .3)
    if kk > 0: put(img, pill("WE HAVE A FIX", 58, TAN, PLUM, padx=50), W / 2, 860, scale=kk)
    logo(img); return img


def pulse(img, cx, cy, t, col):
    """Flat expanding rings for the massage pulse."""
    d = ImageDraw.Draw(img)
    for i in range(3):
        k = (t * 1.6 + i / 3) % 1; r = 260 + 260 * k; a = .55 * (1 - k)
        c = tuple(int(col[j] * a + PLUM2[j] * (1 - a)) for j in range(3))
        d.ellipse((cx - r, cy - r, cx + r, cy + r), outline=rgba(c), width=10)


def p_drop(t, b, prev):
    img = bg(PLUM2); rays(img, W / 2, 1060, t, TAN, a=16)
    pulse(img, W / 2, 1060, t, CREAM)
    disc(img, W / 2, 1060, 300, (110, 50, 124))
    k = back(t / .45); jit = 6 * math.sin(t * 60) if t > .6 else 0
    put(img, P(PROD, 760, 640), W / 2 + jit, 1060 - 700 * (1 - min(1, k)), a=clamp(t / .15))
    kk = ease((t - .4) / .4)
    put(img, T("Portable Massage Gun", f("Poppins-Bold.ttf", 80), WHITE, True), W / 2, 330 + 30 * (1 - kk), a=kk)
    put(img, T("Rechargeable and portable", f("Poppins-Medium.ttf", 50), TAN), W / 2, 450, a=clamp((t - .6) / .3))
    kk = (t - 1.2) / .3
    if kk > 0: put(img, TB("ঘরে বসেই ম্যাসাজ", 700, 70, CREAM), W / 2, 1560, a=clamp(kk))
    logo(img); return wipe(img, prev, t, PLUM2, W / 2, 1060)


FEATS = [("4 Heads", "Interchangeable"), ("Quiet", "Powerful yet quiet motor"), ("Light", "Ergonomic design"), ("Recharge", "Use it on the go")]
def p_feats(t, b, prev):
    img = bg(PLUM)
    disc(img, W / 2, 560, 290, PLUM2)
    put(img, P(PROD, 620, 520), W / 2 + (4 * math.sin(t * 50) if (t % 1.5) < .5 else 0), 560)
    for i, (big, small) in enumerate(FEATS):
        kk = back((t - i * 1.6 * b) / .3)
        if kk <= 0: continue
        cx = 285 + (i % 2) * 510; cy = 1110 + (i // 2) * 290
        key = ("pf16", i); card = _tc.get(key)
        if card is None:
            card = Image.new("RGBA", (470, 250), (0, 0, 0, 0)); d = ImageDraw.Draw(card)
            d.rounded_rectangle((0, 0, 469, 249), radius=36, fill=rgba(TAN if i in (0, 3) else CREAM))
            bt = T(big, f("Poppins-Bold.ttf", 76), PLUM); card.alpha_composite(bt, (235 - bt.width // 2, 44))
            st = T(small, f("Poppins-Medium.ttf", 34), (90, 50, 90)); card.alpha_composite(st, (235 - st.width // 2, 160)); _tc[key] = card
        put(img, card, cx, cy, scale=kk)
    for i, w_ in enumerate(["Gym", "Office", "Home"]):
        kk = back((t - (8 + i) * b) / .3)
        if kk > 0: put(img, pill(w_, 46, WHITE, PLUM, padx=44), W / 2 + (i - 1) * 300, 1720, scale=kk)
    logo(img); return wipe(img, prev, t, PLUM)


def p_price(t, b, prev):
    BGc = (40, 14, 50); img = bg(BGc); rays(img, W / 2, 900, t, TAN, a=18)
    put(img, T("Price?", f("Poppins-Bold.ttf", 90), WHITE, True), W / 2, 300)
    put(img, P(PROD, 560, 440), W / 2, 680 + 10 * math.sin(t * 3), scale=back(t / .4))
    stop = 4 * b
    if t >= stop: confetti(img, t - stop, seed=16)
    if t < stop:   # slot style rolling numbers
        put(img, T("Tk ???", f("Poppins-Bold.ttf", 170), (170, 130, 180), True), W / 2, 1160, scale=1 + .06 * math.sin(t * 14))
    else:
        put(img, T("Tk 850", f("Poppins-Bold.ttf", 190), TAN, True), W / 2, 1160, scale=back((t - stop) / .35))
        kk = (t - stop - .3) / .3
        if kk > 0:
            col = (190, 160, 200); rt = T("Regular Tk 1,200", f("Poppins-Regular.ttf", 50), col); put(img, rt, W / 2, 1320, a=clamp(kk))
            d = ImageDraw.Draw(img); d.line((W / 2 - rt.width / 2 + 10, 1324, W / 2 + rt.width / 2 - 10, 1324), fill=rgba(col), width=5)
        kk2 = back((t - stop - .5) / .35)
        if kk2 > 0: put(img, pill("Inbox us to order", 50, CREAM, PLUM, padx=50), W / 2, 1480, scale=kk2)
    logo(img); return wipe(img, prev, t, BGc)


REELS = [
    dict(id="reel-massage-gun-long-day", time="18:30", music=("drive", 5), b=DR.B, cover=4600,
         scenes=[(p_hook, 9), (p_drop, 7), (p_feats, 14), (p_price, 9),
                 (end_card([(PROD, HQ), ("02.png", HQ), ("32.png", HQ)], PLUM, TAN, "Relax after a long day"), 8)]),
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
