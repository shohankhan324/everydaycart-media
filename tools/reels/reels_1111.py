"""Everyday Cart Reel for 11 Nov: Awei T88 "budget earbuds checklist" (Bangla hook under 1,000 taka, drop,
animated tick checklist, price reveal, end card). Deep teal + orange palette, original drive track in a new key."""
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
R9.OUT = _R + "/out/out1111/"; os.makedirs(R9.OUT, exist_ok=True)
TEAL = (8, 62, 70); TEAL2 = (14, 92, 100); ORG = (255, 140, 46); CRM = (255, 241, 222)
PROD = "11.png"


def dots(img, t, col):
    d = ImageDraw.Draw(img)
    for i in range(18):
        x = (i * 173 + 60) % W; y = (i * 311 + t * 40 * (1 + i % 3)) % H
        r = 6 + (i % 3) * 4; d.ellipse((x - r, y - r, x + r, y + r), fill=rgba(col))


def p_hook(t, b, prev):
    img = bg(TEAL); dots(img, t, (20, 84, 92))
    put(img, TB("১,০০০ টাকার নিচে", 700, 130, ORG, True), W / 2, 560, scale=1.3 - .3 * ease(t / .25), a=clamp(t / .12))
    kk = (t - b) / .3
    if kk > 0: put(img, TB("ভালো ইয়ারবাড পাওয়া যায়?", 700, 92, WHITE, True), W / 2, 740, scale=1.25 - .25 * ease(kk), a=clamp(kk * 2))
    kk = back((t - 2.2 * b) / .35)
    if kk > 0:
        disc(img, W / 2, 1270, 360, TEAL2)
        put(img, P(PROD, 560, 560), W / 2, 1270 + 10 * math.sin(t * 3), scale=kk)
        kq = back((t - 3 * b) / .3)
        if kq > 0:
            disc(img, W / 2 + 310, 1000, 100 * kq, ORG); put(img, T("?", f("Poppins-Bold.ttf", 140), TEAL), W / 2 + 310, 1000, scale=kq)
    logo(img); return img


def p_drop(t, b, prev):
    img = bg(ORG); rays(img, W / 2, 1050, t, WHITE, a=26)
    disc(img, W / 2, 1050, 390, (255, 170, 96))
    k = back(t / .45)
    put(img, P(PROD, 760, 760), W / 2, 1050 - 700 * (1 - min(1, k)) + 10 * math.sin(t * 3), a=clamp(t / .15))
    kk = ease((t - .4) / .4)
    put(img, T("Awei T88", f("Poppins-Bold.ttf", 140), TEAL, False), W / 2, 330 + 30 * (1 - kk), a=kk)
    put(img, T("Wireless Earbuds  •  Black", f("Poppins-Medium.ttf", 48), WHITE), W / 2, 460, a=clamp((t - .6) / .3))
    put(img, TB("হ্যাঁ, পাওয়া যায়!", 700, 70, TEAL), W / 2, 1600, a=clamp((t - .9) / .3))
    logo(img); return wipe(img, prev, t, ORG, W / 2, 1050)


CHECKS = [("ANC Support", "নয়েজ কমায়"), ("IPX6 Water Resistant", "পানি প্রতিরোধী"),
          ("Bluetooth 5.4", "সহজ কানেকশন"), ("Touch Control", "এক টাচেই কন্ট্রোল")]
def p_check(t, b, prev):
    img = bg(CRM)
    put(img, TB("বাজেট ইয়ারবাড চেকলিস্ট", 700, 72, TEAL), W / 2, 230, a=clamp(t / .2))
    disc(img, W / 2, 570, 280, (255, 222, 190))
    put(img, P(PROD, 460, 460), W / 2, 570 + 8 * math.sin(t * 3))
    for i, (en, bn) in enumerate(CHECKS):
        st = (1.5 + i * 2.2) * b; kk = back((t - st) / .3)
        if kk <= 0: continue
        y = 960 + i * 215
        key = ("row1111", i); row = _tc.get(key)
        if row is None:
            row = Image.new("RGBA", (900, 180), (0, 0, 0, 0)); d = ImageDraw.Draw(row)
            d.rounded_rectangle((0, 0, 899, 179), radius=40, fill=rgba(WHITE))
            d.rounded_rectangle((34, 45, 124, 135), radius=20, outline=rgba(TEAL), width=7)
            e = T(en, f("Poppins-Bold.ttf", 54), TEAL); row.alpha_composite(e, (160, 18))
            s = TB(bn, 600, 40, (110, 110, 110)); row.alpha_composite(s, (154, 96)); _tc[key] = row
        put(img, row, W / 2, y, scale=kk)
        tk_ = ease((t - st - .25) / .25)
        if tk_ > 0:
            d = ImageDraw.Draw(img); x0 = W / 2 - 450 + 34; y0 = y - 90 + 45
            p1 = (x0 + 18, y0 + 46); p2 = (x0 + 40, y0 + 70); p3 = (x0 + 100, y0 - 6)
            if tk_ < .4:
                q = tk_ / .4; d.line([p1, (p1[0] + (p2[0] - p1[0]) * q, p1[1] + (p2[1] - p1[1]) * q)], fill=rgba(ORG), width=16)
            else:
                q = (tk_ - .4) / .6; d.line([p1, p2, (p2[0] + (p3[0] - p2[0]) * q, p2[1] + (p3[1] - p2[1]) * q)], fill=rgba(ORG), width=16, joint="curve")
    logo(img); return wipe(img, prev, t, CRM)


def p_price(t, b, prev):
    img = bg(TEAL); rays(img, W / 2, 900, t, ORG, a=22)
    put(img, P(PROD, 560, 520), W / 2, 640 + 10 * math.sin(t * 3), scale=back(t / .4))
    kk = ease((t - 1.5 * b) / .3)
    if kk > 0: put(img, TB("দাম মাত্র", 700, 90, WHITE, True), W / 2, 1060, a=kk)
    kk = back((t - 2.5 * b) / .35)
    if kk > 0:
        put(img, T("Tk 990", f("Poppins-Bold.ttf", 210), ORG, True), W / 2, 1260, scale=kk)
        rt = T("Tk 1,450", f("Poppins-Regular.ttf", 64), (170, 200, 204)); put(img, rt, W / 2, 1420, a=clamp(kk))
        d = ImageDraw.Draw(img); d.line((W / 2 - rt.width / 2 + 20, 1424, W / 2 + rt.width / 2 - 20, 1424), fill=rgba((170, 200, 204)), width=6)
        confetti(img, t - 2.5 * b, seed=11)
    kk = back((t - 4 * b) / .35)
    if kk > 0: put(img, pill("Inbox us to order", 50, WHITE, TEAL, padx=50), W / 2, 1590, scale=kk)
    logo(img); return wipe(img, prev, t, TEAL)


REELS = [
    dict(id="awei-t88-budget-check", time="18:30", music=("drive", 3), b=DR.B, cover=3200,
         scenes=[(p_hook, 7), (p_drop, 6), (p_check, 11), (p_price, 9),
                 (end_card([(PROD, HQ), ("04.png", HQ), ("10.png", HQ)], TEAL2, ORG, "Good sound, smart price"), 6)]),
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
