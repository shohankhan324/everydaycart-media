"""Everyday Cart Reel for 26 Nov: "Gift box surprise": 617 Elephant Plush Soft Toy, 18 inch (750 Tk, regular 1,100).
Flat palette: sky blue + bubblegum pink + butter yellow, cream cards. Bangla hook in the first second
("ছোট্ট সোনার জন্য গিফট খুঁজছেন?") over a shaking flat gift box with floating hearts, the lid pops and the elephant rises,
a ruler counts 0 to 18 inch beside it, a checklist (only listing facts: 18 inch, super soft, huggable, gift for kids),
price card with a comment prompt, end card. Original upbeat synth track in key 8. About 23 s."""

import os as _os
_R = _os.path.dirname(_os.path.abspath(__file__)); _T = _os.path.dirname(_R)

import os, sys, math
from PIL import Image, ImageDraw
sys.path.insert(0, _T); sys.path.insert(0, _R)
from mega import T, TB, P, pill, bg, wipe, logo, disc, put, rgba, f, ease, back, clamp, HQ, WHITE
import reels9 as R9
from reels9 import end_card

W, H = 1080, 1920
R9.OUT = _R + "/out/out1126/"; os.makedirs(R9.OUT, exist_ok=True)
UB = 60 / 112
SKY = (110, 186, 250); SKY2 = (150, 208, 255); PINK = (255, 112, 160); BUTTER = (255, 222, 110)
CREAM = (255, 247, 236); INK = (24, 26, 40); LILAC = (200, 180, 250)
ELE = "25.png"


def heart(d, cx, cy, s, col):
    d.ellipse((cx - s, cy - s * .6, cx, cy + s * .4), fill=col)
    d.ellipse((cx, cy - s * .6, cx + s, cy + s * .4), fill=col)
    d.polygon([(cx - s * .96, cy - s * .02), (cx + s * .96, cy - s * .02), (cx, cy + s * 1.05)], fill=col)


def floaters(d, t, col, a=200, seed=0):
    for i in range(9):
        x = 80 + ((i * 137 + seed * 61) % 920); sp = 70 + (i % 4) * 25
        y = 1900 - ((t * sp + i * 230) % 2000); s = 18 + (i % 3) * 10
        heart(d, x + 18 * math.sin(t * 2 + i), y, s, rgba(col, a))


def gift_box(img, cx, cy, t, lid_up=0.0, shake=0.0):
    L = Image.new("RGBA", (760, 760), (0, 0, 0, 0)); d = ImageDraw.Draw(L)
    bx0, bx1, by0, by1 = 120, 640, 330, 740
    d.rectangle((bx0 + 14, by0 + 14, bx1 + 14, by1 + 14), fill=rgba(INK))
    d.rectangle((bx0, by0, bx1, by1), fill=rgba(PINK), outline=rgba(INK), width=8)
    d.rectangle((345, by0, 415, by1), fill=rgba(BUTTER), outline=rgba(INK), width=6)
    ly = 250 - 420 * lid_up
    if ly > -200:
        d.rectangle((90, ly, 670, ly + 96), fill=rgba(PINK), outline=rgba(INK), width=8)
        d.rectangle((345, ly, 415, ly + 96), fill=rgba(BUTTER), outline=rgba(INK), width=6)
        d.ellipse((270, ly - 80, 380, ly + 10), fill=rgba(BUTTER), outline=rgba(INK), width=6)
        d.ellipse((380, ly - 80, 490, ly + 10), fill=rgba(BUTTER), outline=rgba(INK), width=6)
    put(img, L, cx, cy, rot=shake)


def p_hook(t, b, prev):
    img = bg(SKY); d = ImageDraw.Draw(img)
    floaters(d, t, WHITE, 150)
    d.rectangle((0, 1560, W, H), fill=rgba(SKY2))
    sh = 6 * math.sin(t * 22) * clamp((t - .3) / .2)
    gift_box(img, W / 2, 1220, t, shake=sh)
    k1 = (t - .05) / .22
    if k1 > 0: put(img, TB("ছোট্ট সোনার জন্য", 700, 92, WHITE), W / 2, 330, scale=1.4 - .4 * ease(k1), a=clamp(k1 * 2))
    k2 = (t - .45) / .25
    if k2 > 0: put(img, TB("গিফট খুঁজছেন?", 700, 124, BUTTER), W / 2, 500, scale=1.35 - .35 * back(k2), a=clamp(k2 * 2))
    kk = back((t - 1.5) / .3)
    if kk > 0: put(img, pill("OPEN THE BOX", 52, INK, WHITE, padx=46), W / 2, 1720, scale=kk, rot=-3)
    logo(img); return img


def p_reveal(t, b, prev):
    img = bg(BUTTER); d = ImageDraw.Draw(img)
    floaters(d, t, PINK, 120, 3)
    lid = ease(t / .4)
    rise = back((t - .25) / .6)
    km = back((t - .1) / .4)
    if km > 0: disc(img, W / 2, 900, 420 * km, CREAM)
    if rise > 0: put(img, P(ELE, 560, 700), W / 2, 1300 - 420 * rise, scale=.6 + .4 * clamp(rise))
    gift_box(img, W / 2, 1500, t, lid_up=lid)
    kt = back((t - .8) / .35)
    if kt > 0: put(img, T("Elephant Plush Soft Toy", f("Poppins-Bold.ttf", 70), INK), W / 2, 240, scale=kt)
    ks = back((t - 1.1) / .35)
    if ks > 0: put(img, TB("নরম তুলতুলে হাতির সফট টয়", 700, 72, PINK), W / 2, 360, scale=ks)
    logo(img); return wipe(img, prev, t, BUTTER)


def p_size(t, b, prev):
    img = bg(CREAM); d = ImageDraw.Draw(img)
    put(img, TB("কত বড় জানেন?", 700, 104, INK), W / 2, 250, scale=back(t / .3))
    kd = back(t / .4)
    if kd > 0:
        disc(img, 430, 1000, 330 * kd, SKY2)
        put(img, P(ELE, 470, 600), 430, 1010, scale=kd)
    # ruler on the right: grows with the count
    g = ease(clamp((t - .4) / 1.6)); n = int(round(18 * g))
    rx0, rx1, ry1 = 800, 900, 1330; full = 640; ry0 = ry1 - full * g
    if g > 0:
        d.rectangle((rx0 + 10, ry0 + 10, rx1 + 10, ry1 + 10), fill=rgba(INK))
        d.rectangle((rx0, ry0, rx1, ry1), fill=rgba(BUTTER), outline=rgba(INK), width=6)
        for k in range(0, n + 1):
            y = ry1 - full * k / 18; ln = 44 if k % 6 == 0 else 24
            d.line((rx0, y, rx0 + ln, y), fill=rgba(INK), width=5)
    put(img, T(f"{n}\"", f("Poppins-Bold.ttf", 150), PINK), 850, 560 if g > 0 else 1200, a=1 if g > 0 else 0)
    ks = back((t - 2.0) / .3)
    if ks > 0: put(img, pill("18 INCH SIZE", 60, PINK, WHITE, padx=50), W / 2, 1520, scale=ks, rot=-2)
    kb = back((t - 2.4) / .35)
    if kb > 0: put(img, TB("জড়িয়ে ধরার মতো বড়", 700, 76, SKY), W / 2, 1690, scale=kb)
    logo(img); return wipe(img, prev, t, CREAM)


CHECK = [("18 inch size", PINK), ("Super soft", SKY2), ("Huggable", BUTTER), ("Sweet gift for kids", LILAC)]


def p_check(t, b, prev):
    img = bg(PINK); d = ImageDraw.Draw(img)
    floaters(d, t, WHITE, 90, 5)
    put(img, T("Why kids love it", f("Poppins-Bold.ttf", 88), WHITE), W / 2, 240, scale=back(t / .35))
    put(img, TB("ছোটদের প্রিয় খেলার সাথী", 700, 64, BUTTER), W / 2, 350, scale=back((t - .15) / .35))
    put(img, P(ELE, 360, 430), W / 2, 640 + 8 * math.sin(t * 3), scale=back((t - .2) / .4), rot=3 * math.sin(t * 2))
    for i, (txt, col) in enumerate(CHECK):
        st = .7 + .5 * i; kk = back((t - st) / .32)
        if kk <= 0: continue
        card = Image.new("RGBA", (900, 150), (0, 0, 0, 0)); cd = ImageDraw.Draw(card)
        cd.rounded_rectangle((10, 12, 899, 149), radius=34, fill=rgba(INK))
        cd.rounded_rectangle((0, 0, 889, 137), radius=34, fill=rgba(CREAM), outline=rgba(INK), width=6)
        cd.ellipse((30, 26, 116, 112), fill=rgba(col), outline=rgba(INK), width=5)
        tick = clamp((t - st - .2) / .2)
        if tick > 0:
            pts = [(50, 70), (68, 90), (98, 50)]
            if tick < .5: pts = pts[:2]
            cd.line(pts, fill=rgba(INK), width=11, joint="curve")
        tt = T(txt, f("Poppins-Bold.ttf", 54), INK); card.alpha_composite(tt, (140, 69 - tt.height // 2))
        put(img, card, W / 2, 1000 + i * 180, scale=kk, rot=(-1.5 if i % 2 == 0 else 1.5))
    logo(img); return wipe(img, prev, t, PINK)


def p_price(t, b, prev):
    img = bg(SKY); d = ImageDraw.Draw(img)
    floaters(d, t, WHITE, 110, 7)
    put(img, TB("দাম কত?", 700, 120, WHITE), W / 2, 230, scale=back(t / .3))
    kd = back(t / .4); disc(img, W / 2, 730, 320 * kd, BUTTER)
    put(img, P(ELE, 430, 520), W / 2, 740, scale=kd)
    kk = back((t - .7) / .4)
    if kk > 0:
        card = Image.new("RGBA", (780, 380), (0, 0, 0, 0)); cd = ImageDraw.Draw(card)
        cd.rounded_rectangle((16, 20, 779, 379), radius=56, fill=rgba(PINK))
        cd.rounded_rectangle((0, 0, 763, 359), radius=56, fill=rgba(CREAM), outline=rgba(INK), width=8)
        lt = T("ONLY", f("Poppins-Bold.ttf", 44), PINK); card.alpha_composite(lt, (382 - lt.width // 2, 30))
        pt = T("Tk 750", f("Poppins-Bold.ttf", 150), INK); card.alpha_composite(pt, (382 - pt.width // 2, 96))
        rt = T("Regular Tk 1,100", f("Poppins-Medium.ttf", 42), (120, 120, 130)); rx = 382 - rt.width // 2; card.alpha_composite(rt, (rx, 282))
        ImageDraw.Draw(card).line((rx + 14, 282 + rt.height // 2, rx + rt.width - 14, 282 + rt.height // 2), fill=rgba((120, 120, 130)), width=5)
        put(img, card, W / 2, 1270, scale=kk, rot=-2)
    kc = back((t - 1.6) / .35)
    if kc > 0: put(img, TB("কাকে গিফট দেবেন? ট্যাগ করুন", 700, 62, WHITE), W / 2, 1580, scale=kc)
    logo(img); return wipe(img, prev, t, SKY)


REELS = [
    dict(id="reel-elephant-plush-gift-box-surprise", time="18:30", music=("upbeat", 8), b=UB, cover=4200,
         scenes=[(p_hook, 5), (p_reveal, 7), (p_size, 8), (p_check, 9), (p_price, 8),
                 (end_card([(ELE, HQ), ("06.png", HQ), ("07.png", HQ)], PINK, BUTTER, "Soft hugs, sweet gifts."), 6)]),
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
