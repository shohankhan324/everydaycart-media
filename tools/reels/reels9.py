"""Nine Everyday Cart Reels for 3 Nov: each its own concept, palette and music."""
import os as _os
_R = _os.path.dirname(_os.path.abspath(__file__)); _T = _os.path.dirname(_R)

import os, sys, math, subprocess
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
sys.path.insert(0, _T); sys.path.insert(0, _R)
from mega import (T, TB, P, pill, bn_pill, bg, wipe, logo, rays, disc, confetti, steam, put, rgba, f, ease, back, clamp,
                  LOGO, HQ, FL, DARK, WHITE, YEL, CORAL, BLUE, PURP, GREEN, CREAM, ORANGE, _tc)
import drive as DR
import make_music as MM
from scipy.io import wavfile

W, H, FPS = 1080, 1920, 30
OUT = _R + "/out/out9/"; os.makedirs(OUT, exist_ok=True)
NAVY = (22, 30, 66); MINT = (198, 238, 222); PEACH = (255, 214, 196); LILAC = (226, 214, 255); TEAL = (14, 120, 120)
BN_DIG = str.maketrans("0123456789", "০১২৩৪৫৬৭৮৯")
def bn_num(n): return f"{n:,}".translate(BN_DIG)

def logo_card(width):
    lc = LOGO.resize((width, int(LOGO.height * width / LOGO.width)), Image.LANCZOS)
    cd = Image.new("RGBA", (lc.width + int(width * .18), lc.height + int(width * .13)), (0, 0, 0, 0))
    ImageDraw.Draw(cd).rounded_rectangle((0, 0, cd.width - 1, cd.height - 1), radius=int(width * .09), fill=(255, 255, 255, 255))
    cd.alpha_composite(lc, ((cd.width - lc.width) // 2, (cd.height - lc.height) // 2)); return cd
LOGO_BIG = logo_card(400)

def end_card(prods, col, accent, line):
    def fn(t, b, prev):
        img = bg(col); rays(img, W / 2, 800, t, WHITE, a=14)
        for i, (n, fol) in enumerate(prods):
            kk = (t - .1 - i * .07) / .4; ang = math.radians(-150 + i * (120 / max(1, len(prods) - 1)))
            put(img, P(n, 250, 250, fol), W / 2 + 400 * math.cos(ang), 720 + 360 * math.sin(ang) + 10 * math.sin(t * 3 + i), scale=.8 * back(kk), a=clamp(kk * 3))
        put(img, LOGO_BIG, W / 2, 860, scale=back((t - .3) / .4))
        def ln(spr, y, st):
            kk = (t - st) / .35
            if kk > 0: put(img, spr, W / 2, y + 40 * (1 - ease(kk)), a=clamp(kk))
        ln(T(line, f("Poppins-Bold.ttf", 64), WHITE, True), 1100, .5)
        kk = back((t - .7) / .4)
        if kk > 0: put(img, pill("Order: everydaycart.online", 50, accent, DARK if (0.299*accent[0]+0.587*accent[1]+0.114*accent[2]) > 150 else WHITE, padx=50), W / 2, 1240, scale=kk)
        ln(T("Inbox us to order  •  Limited stock", f("Poppins-Medium.ttf", 40), WHITE), 1370, .9)
        return wipe(img, prev, t, col)
    return fn

# ---------------------------------------------------------------- 1. Guess the price: SpaceBox
def r1_hook(t, b, prev):
    img = bg(DARK); rays(img, W / 2, 960, t, (0, 200, 255), a=20)
    for i, (wd, col) in enumerate([("CAN YOU", WHITE), ("GUESS", (0, 220, 255)), ("THE PRICE?", WHITE)]):
        kk = (t - i * b) / .2
        if kk > 0: put(img, T(wd, f("Poppins-Bold.ttf", 150 if i != 1 else 210), col, True), W / 2, 700 + i * 220, scale=1.5 - .5 * ease(kk), a=clamp(kk * 2))
    logo(img); return img
def r1_guess(t, b, prev):
    img = bg((10, 16, 40)); rays(img, W / 2, 760, t, (0, 200, 255), a=24)
    put(img, T("Oraimo SpaceBox Speaker", f("Poppins-Bold.ttf", 66), WHITE, True), W / 2, 220)
    put(img, T("Light show  •  Thumping bass", f("Poppins-Medium.ttf", 40), (150, 220, 255)), W / 2, 310)
    put(img, P("01.png", 820, 460), W / 2, 740 + 12 * math.sin(t * 3), scale=back(t / .45), rot=(1 - ease(t / .4)) * 15)
    opts = [("A", "Tk 2,500"), ("B", "Tk 1,200"), ("C", "Tk 1,841")]; reveal = 12 * b
    for i, (l, v) in enumerate(opts):
        kk = back((t - (1.5 + i) * b) / .35)
        if kk <= 0: continue
        ok = i == 2 and t > reveal; dim = i != 2 and t > reveal
        card = Image.new("RGBA", (300, 130), (0, 0, 0, 0)); d = ImageDraw.Draw(card)
        d.rounded_rectangle((0, 0, 299, 129), radius=30, fill=(0, 200, 120, 255) if ok else ((255, 255, 255, 90) if dim else (255, 255, 255, 255)))
        d.text((26, 30), l, font=f("Poppins-Bold.ttf", 52), fill=rgba(WHITE if ok else DARK)); d.text((88, 38), v, font=f("Poppins-Bold.ttf", 44), fill=rgba(WHITE if ok else DARK))
        put(img, card, 180 + i * 360, 1180, scale=kk * (1 + .12 * math.exp(-(t - reveal) * 6) if ok else kk))
    for n in range(3):
        s = (6 + 2 * n) * b
        if s <= t < s + 2 * b:
            k = (t - s) / (2 * b); put(img, T(str(3 - n), f("Poppins-Bold.ttf", 260), WHITE, True), W / 2, 1500, scale=1.6 - .6 * ease(k * 3), a=clamp(1.3 - k))
    if t > reveal:
        put(img, T("Tk 1,841", f("Poppins-Bold.ttf", 150), (0, 220, 255), True), W / 2, 1480, scale=back((t - reveal) / .35))
        kk = (t - reveal - .4) / .3
        if kk > 0: put(img, pill("Regular Tk 2,299  •  Comment if you got it", 36, WHITE, (10, 16, 40)), W / 2, 1660, a=clamp(kk))
        confetti(img, t - reveal, seed=4)
    logo(img); return wipe(img, prev, t, (10, 16, 40))

# ---------------------------------------------------------------- 2. Mom's must-haves (soft)
BABY = [("22.png", HQ, "Minitree 120 ml Bottle", 450), ("08.png", HQ, "Minitree Tritan Bottle", 450), ("20.png", HQ, "Minitree Mumpot", 400),
        ("21.png", HQ, "10 Pc Baby Care Kit", 480), ("kodomo_paste.png", FL, "Kodomo Baby Toothpaste", 280), ("kodomo_lotion.png", FL, "Kodomo Lotion Powder", 720)]
def r2_hook(t, b, prev):
    img = bg(PEACH); d = ImageDraw.Draw(img)
    for i in range(7): disc(img, 120 + i * 150, 300 + 90 * math.sin(i + t), 40 + 10 * math.sin(t * 2 + i), (255, 236, 228))
    put(img, TB("নতুন মায়েদের জন্য", 700, 110, (150, 70, 80)), W / 2, 760, a=clamp(t / .4), scale=1.1 - .1 * ease(t / .5))
    kk = ease((t - b) / .5)
    if kk > 0: put(img, T("Mom's Must-Haves", f("Poppins-Bold.ttf", 96), (120, 60, 70)), W / 2, 920 + 30 * (1 - kk), a=kk)
    kk = ease((t - 2 * b) / .5)
    if kk > 0: put(img, T("Gentle care for your little one", f("Poppins-Medium.ttf", 46), (150, 100, 100)), W / 2, 1030, a=kk)
    logo(img); return img
def r2_item(i):
    im, fol, name, pr = BABY[i]; cols = [MINT, LILAC, PEACH, (255, 236, 200), MINT, LILAC]
    def fn(t, b, prev):
        col = cols[i]; img = bg(col)
        disc(img, W / 2, 900, 380 + 10 * math.sin(t * 2), (255, 255, 255, 120) if False else tuple(min(255, c + 22) for c in col))
        put(img, P(im, 560, 560, fol), W / 2, 900 + 12 * math.sin(t * 2.2), scale=.85 + .15 * ease(t / .6), a=clamp(t / .3))
        kk = ease((t - .3) / .5)
        put(img, T(name, f("Poppins-Bold.ttf", 70), (70, 60, 70)), W / 2, 1400 + 30 * (1 - kk), a=kk)
        put(img, T(f"Tk {pr:,}", f("Poppins-Bold.ttf", 100), (190, 80, 95)), W / 2, 1530, a=clamp((t - .5) / .4))
        put(img, T(f"{i + 1}/6", f("Poppins-Medium.ttf", 40), (110, 100, 110)), W / 2, 260, a=clamp(t / .3))
        logo(img); return wipe(img, prev, t, col, W / 2, 900)
    return fn

# ---------------------------------------------------------------- 3. This or that: smartwatches
def r3_vs(t, b, prev):
    L, R = (24, 24, 30), BLUE
    img = bg(L); ImageDraw.Draw(img).rectangle((W / 2, 0, W, H), fill=rgba(R))
    k = ease(t / .4)
    put(img, P("09.png", 400, 460), W / 4 - (1 - k) * 500, 620); put(img, P("02.png", 400, 460), 3 * W / 4 + (1 - k) * 500, 620)
    put(img, T("COLMI P81", f("Poppins-Bold.ttf", 54), WHITE), W / 4, 900, a=k); put(img, T("Oraimo Watch 5 Lite", f("Poppins-Bold.ttf", 44), WHITE), 3 * W / 4, 900, a=k)
    put(img, T("WHICH ONE?", f("Poppins-Bold.ttf", 100), YEL, True), W / 2, 230, scale=1.3 - .3 * ease(t / .3))
    vs = Image.new("RGBA", (180, 180), (0, 0, 0, 0)); ImageDraw.Draw(vs).ellipse((0, 0, 179, 179), fill=rgba(YEL)); vs.alpha_composite(T("VS", f("Poppins-Bold.ttf", 72), DARK), (36, 28))
    put(img, vs, W / 2, 620, scale=back((t - .3) / .35), rot=8 * math.sin(t * 5))
    rows = [("Price", "Tk 1,350", "Tk 1,650"), ("Display", "1.9\" HD", "2.01\" HD"), ("Calling", "Yes", "Yes"), ("Water", "IP68", "IP68"), ("Sports", "100+", "105+")]
    for i, (lab, a_, b_) in enumerate(rows):
        kk = ease((t - (2 + i) * b) / .3)
        if kk <= 0: continue
        y = 1040 + i * 112
        ov = Image.new("RGBA", (W, 96), (0, 0, 0, 0)); ImageDraw.Draw(ov).rounded_rectangle((60, 0, W - 60, 92), radius=46, fill=(255, 255, 255, int(240 * kk))); img.alpha_composite(ov, (0, y))
        put(img, T(a_, f("Poppins-Bold.ttf", 40), DARK), 250, y + 46, a=kk); put(img, T(b_, f("Poppins-Bold.ttf", 40), BLUE), W - 250, y + 46, a=kk)
        put(img, T(lab, f("Poppins-Medium.ttf", 30), (120, 120, 130)), W / 2, y + 46, a=kk)
    kk = back((t - 8 * b) / .35)
    if kk > 0: put(img, pill("Comment: COLMI or ORAIMO?", 44, YEL, DARK), W / 2, 1650, scale=kk)
    logo(img); return wipe(img, prev, t, L)

# ---------------------------------------------------------------- 4. Bangla POV: tea goes cold
def cup(img, cx, cy, warm):
    d = ImageDraw.Draw(img)
    d.rounded_rectangle((cx - 120, cy - 110, cx + 120, cy + 120), radius=30, fill=rgba(WHITE))
    d.arc((cx + 80, cy - 60, cx + 180, cy + 50), -90, 90, fill=rgba(WHITE), width=26)
    d.ellipse((cx - 104, cy - 124, cx + 104, cy - 86), fill=rgba((150, 95, 60) if warm else (120, 100, 90)))
def r4_pov(t, b, prev):
    img = bg((30, 40, 60))
    put(img, T("POV:", f("Poppins-Bold.ttf", 110), YEL), W / 2, 420, a=clamp(t / .2))
    for i, line in enumerate(["শীতের সকালে চা বানালাম", "৫ মিনিট পরেই ঠান্ডা..."]):
        kk = ease((t - .3 - i * b) / .3)
        if kk > 0: put(img, TB(line, 700, 84, WHITE), W / 2, 610 + i * 120 + 30 * (1 - kk), a=kk)
    warm = t < 2.5 * b
    cup(img, W / 2, 1150, warm)
    if warm: steam(img, W / 2 - 10, 1010, t)
    else:
        for i in range(6):   # frost flakes
            x = W / 2 - 260 + i * 100; y = 1000 + 30 * math.sin(t * 2 + i); d = ImageDraw.Draw(img)
            for a in range(3):
                ang = a * math.pi / 3; d.line((x - 22 * math.cos(ang), y - 22 * math.sin(ang), x + 22 * math.cos(ang), y + 22 * math.sin(ang)), fill=rgba((180, 220, 255)), width=5)
    if t > 2.5 * b: put(img, T("COLD", f("Poppins-Bold.ttf", 90), (140, 200, 255), True), W / 2, 1420, scale=back((t - 2.5 * b) / .3))
    logo(img); return wipe(img, prev, t, (30, 40, 60))
def r4_fix(t, b, prev):
    img = bg(ORANGE); rays(img, W / 2, 900, t, WHITE, a=30)
    put(img, TB("সমাধান?", 700, 120, WHITE, True), W / 2, 280, scale=1.4 - .4 * ease(t / .25))
    put(img, P("16.png", 420, 560), W / 2 - 170, 900 + 10 * math.sin(t * 3), scale=back(t / .4))
    put(img, P("15.png", 380, 520), W / 2 + 190, 930 + 10 * math.sin(t * 3 + 1), scale=back((t - .15) / .4))
    steam(img, W / 2 - 170, 600, t)
    kk = ease((t - .5) / .3)
    put(img, TB("সারাদিন গরম থাকবে চা", 700, 76, WHITE, True), W / 2, 1320, a=kk)
    put(img, T("Premium Thermal Tumbler  •  Big Mac 316 Cup", f("Poppins-Medium.ttf", 38), WHITE), W / 2, 1420, a=kk)
    kk = back((t - .8) / .35)
    if kk > 0: put(img, bn_pill(f"মাত্র {bn_num(800)} টাকা থেকে"), W / 2, 1570, scale=kk)
    logo(img); return wipe(img, prev, t, ORANGE)

# ---------------------------------------------------------------- 5. Unboxing: Proove Intro Pro
def r5_unbox(t, b, prev):
    img = bg((14, 14, 18)); cx, cy = W / 2, 1150; ot = 3 * b
    if t > ot: rays(img, cx, cy - 150, t, (255, 60, 60), a=int(60 * clamp((t - ot) / .3)))
    shake = 10 * math.sin(t * 50) * (1 if b < t < ot else 0); bw, bh = 520, 380
    def box(dx):
        d = ImageDraw.Draw(img)
        d.rounded_rectangle((cx - bw / 2 + dx, cy - bh / 2 + 60, cx + bw / 2 + dx, cy + bh / 2 + 60), radius=24, fill=rgba((40, 40, 48)))
        d.rectangle((cx - 36 + dx, cy - bh / 2 + 60, cx + 36 + dx, cy + bh / 2 + 60), fill=rgba((230, 40, 50)))
    box(shake)
    if t > ot:
        k = back((t - ot) / .5); put(img, P("03.png", 460, 520), cx, cy - 60 - 430 * k, scale=.5 + .5 * k, a=clamp((t - ot) / .15)); box(0)
    lid = Image.new("RGBA", (bw + 40, 110), (0, 0, 0, 0)); dl = ImageDraw.Draw(lid)
    dl.rounded_rectangle((0, 0, bw + 39, 109), radius=24, fill=rgba((56, 56, 66))); dl.rectangle(((bw + 40) / 2 - 36, 0, (bw + 40) / 2 + 36, 109), fill=rgba((230, 40, 50)))
    lk = ease((t - ot) / .45); put(img, lid, cx + shake - 380 * lk, cy - bh / 2 + 10 - 700 * lk, rot=35 * lk, a=1 - clamp((t - ot - .3) / .3))
    put(img, T("UNBOXING", f("Poppins-Bold.ttf", 110), WHITE, True), W / 2, 230, a=clamp(t / .2))
    put(img, T("the earbuds with an LED case", f("Poppins-Medium.ttf", 44), (255, 120, 120)), W / 2, 340, a=clamp((t - .3) / .3))
    logo(img); return img
def r5_feats(t, b, prev):
    img = bg((14, 14, 18)); rays(img, W / 2, 820, t, (255, 60, 60), a=22)
    put(img, P("03.png", 520, 580), W / 2, 760 + 10 * math.sin(t * 3))
    put(img, T("Proove Intro Pro", f("Poppins-Bold.ttf", 84), WHITE, True), W / 2, 230)
    feats = ["13mm Driver", "Transparent ENC Calls", "Bluetooth 5.4", "LED Display Case"]
    for i, ft in enumerate(feats):
        kk = back((t - i * b) / .3)
        if kk > 0: put(img, pill(ft, 40, (230, 40, 50), WHITE), W / 2, 1180 + i * 105, scale=kk)
    kk = back((t - 4.5 * b) / .35)
    if kk > 0: put(img, T("Tk 2,300", f("Poppins-Bold.ttf", 140), WHITE, True), W / 2, 1680, scale=kk)
    logo(img); return wipe(img, prev, t, (14, 14, 18))

# ---------------------------------------------------------------- 6. Under 1,000 Taka (new picks)
U = [("11.png", "Awei T88 Earbuds", 990), ("10.png", "Awei T108 Earbuds", 950), ("07.png", "Silent Alarm Clock", 500),
     ("19.png", "Smart LED Bottle", 350), ("20.png", "Minitree Mumpot", 400), ("17.png", "Kids Thermal Bottle", 800)]
def r6_grid(t, b, prev):
    img = bg(GREEN)
    put(img, T("UNDER", f("Poppins-Bold.ttf", 90), WHITE), W / 2, 200, scale=1.3 - .3 * ease(t / .25))
    put(img, T("1,000 TAKA", f("Poppins-Bold.ttf", 140), YEL, True), W / 2, 320, scale=1.3 - .3 * ease((t - .1) / .25))
    for i, (im, name, pr) in enumerate(U):
        k = back((t - (1 + i * 1.5) * b) / .35)
        if k <= 0: continue
        cx = 285 + (i % 2) * 510; cy = 600 + (i // 2) * 410
        key = ("u9", i); card = _tc.get(key)
        if card is None:
            card = Image.new("RGBA", (470, 390), (0, 0, 0, 0)); d = ImageDraw.Draw(card); d.rounded_rectangle((0, 0, 469, 389), radius=36, fill=rgba(WHITE))
            p = P(im, 250, 230); card.alpha_composite(p, (235 - p.width // 2, 135 - p.height // 2))
            nm = T(name, f("Poppins-Medium.ttf", 32), (80, 80, 90)); card.alpha_composite(nm, (235 - nm.width // 2, 262))
            pt = T(f"Tk {pr:,}", f("Poppins-Bold.ttf", 52), GREEN); card.alpha_composite(pt, (235 - pt.width // 2, 302)); _tc[key] = card
        put(img, card, cx, cy + 230, scale=k, rot=(1 - ease((t - (1 + i * 1.5) * b) / .3)) * (8 if i % 2 else -8))
    logo(img); return wipe(img, prev, t, GREEN)

# ---------------------------------------------------------------- 7. Gift guide by budget
GIFTS = [("UNDER TK 500", "07.png", "Silent Alarm Clock", "Tk 500", (120, 90, 200)), ("UNDER TK 1,500", "06.png", "22\" Big Teddy Bear", "Tk 1,150", CORAL),
         ("UNDER TK 2,000", "12.png", "Oraimo SpaceBuds Neo+", "Tk 1,940", BLUE), ("BIG GIFT", "05.png", "Forkan Trolley Luggage", "from Tk 4,000", TEAL)]
def r7_hook(t, b, prev):
    img = bg((250, 240, 230))
    for i in range(8):
        x = 140 + i * 115; y = 1600 - ((t * 300 + i * 160) % 1500); disc(img, x, y, 26, [CORAL, YEL, BLUE, GREEN][i % 4])
    put(img, T("GIFT IDEAS", f("Poppins-Bold.ttf", 150), DARK), W / 2, 760, scale=1.3 - .3 * ease(t / .3))
    kk = back((t - b) / .4)
    if kk > 0: put(img, pill("for every budget", 60, CORAL, WHITE, padx=50), W / 2, 930, scale=kk)
    logo(img); return wipe(img, prev, t, (250, 240, 230))
def r7_card(i):
    lab, im, name, pr, col = GIFTS[i]
    def fn(t, b, prev):
        img = bg(col); rays(img, W / 2, 900, t, WHITE, a=26)
        put(img, pill(lab, 52, WHITE, col, padx=44), W / 2, 260, scale=back(t / .3))
        put(img, P(im, 600, 640), W / 2, 880 + 12 * math.sin(t * 3), scale=back((t - .1) / .4))
        kk = ease((t - .3) / .3)
        put(img, T(name, f("Poppins-Bold.ttf", 72), WHITE, True), W / 2, 1360 + 30 * (1 - kk), a=kk)
        put(img, T(pr, f("Poppins-Bold.ttf", 120), YEL if col != YEL else DARK, True), W / 2, 1500, scale=back((t - .45) / .3))
        logo(img); return wipe(img, prev, t, col, W / 2, 880)
    return fn

# ---------------------------------------------------------------- 8. Top 5 gadgets
TOP = [(5, "09.png", "COLMI P81 Smartwatch", 1350, (40, 40, 52)), (4, "04.png", "Oraimo Necklace Lite", 1300, PURP),
       (3, "01.png", "Oraimo SpaceBox Speaker", 1841, (0, 150, 200)), (2, "03.png", "Proove Intro Pro", 2300, (200, 40, 50)), (1, "14.png", "Awei KA5 20W Speaker", 2525, (240, 160, 20))]
def r8_top(t, b, prev):
    step = 3.2 * b; i = min(4, int(t / step)); lt = t - i * step
    n, im, name, pr, col = TOP[i]
    img = bg(col); rays(img, W / 2, 950, t, WHITE, a=22)
    put(img, T("TOP 5 GADGETS", f("Poppins-Bold.ttf", 84), WHITE, True), W / 2, 210)
    put(img, T(f"#{n}", f("Poppins-Bold.ttf", 300), (255, 255, 255, 70)), W / 2, 560, scale=1.3 - .3 * ease(lt / .25))
    put(img, P(im, 560, 540), W / 2, 980 + 10 * math.sin(t * 3), scale=back(lt / .35))
    kk = ease((lt - .15) / .25)
    put(img, T(name, f("Poppins-Bold.ttf", 66), WHITE, True), W / 2, 1380 + 30 * (1 - kk), a=kk)
    put(img, T(f"Tk {pr:,}", f("Poppins-Bold.ttf", 110), WHITE, True), W / 2, 1510, scale=back((lt - .2) / .3))
    if n == 1: confetti(img, lt, seed=11)
    logo(img); return wipe(img, prev, t, TOP[0][4])

# ---------------------------------------------------------------- 9. Good night: silent clock
STARS = [(np.random.default_rng(5).uniform(0, W), np.random.default_rng(i).uniform(0, 1100), i) for i in range(60)]
def r9_night(t, b, prev):
    img = bg(NAVY); d = ImageDraw.Draw(img)
    for x, y, i in STARS:
        a = int(140 + 110 * math.sin(t * 2 + i)); r = 2 + (i % 3)
        d.ellipse((x * ((i % 7) + 1) % W - r, y - r, x * ((i % 7) + 1) % W + r, y + r), fill=(255, 255, 255, max(0, a)))
    disc(img, 820, 300, 110, (255, 240, 200)); disc(img, 870, 270, 100, NAVY)
    put(img, T("Shhh...", f("Poppins-Bold.ttf", 120), WHITE), W / 2, 520, a=clamp(t / .6))
    put(img, T("No ticking. Just sleep.", f("Poppins-Medium.ttf", 56), (200, 210, 255)), W / 2, 650, a=clamp((t - b) / .6))
    put(img, P("07.png", 520, 560), W / 2, 1080 + 8 * math.sin(t * 1.6), scale=.9 + .1 * ease(t / 1.2), a=clamp(t / .5))
    kk = ease((t - 3 * b) / .6)
    put(img, T("Silent Alarm Clock", f("Poppins-Bold.ttf", 72), WHITE), W / 2, 1450, a=kk)
    put(img, T("Non-ticking  •  Twin bell design", f("Poppins-Medium.ttf", 42), (200, 210, 255)), W / 2, 1540, a=kk)
    put(img, T("Tk 500", f("Poppins-Bold.ttf", 110), (255, 220, 140)), W / 2, 1680, a=clamp((t - 4 * b) / .5))
    put(img, TB("শুভ রাত্রি", 700, 64, (255, 220, 140)), W / 2, 1830, a=clamp((t - 5 * b) / .5))
    logo(img); return wipe(img, prev, t, NAVY)

# ---------------------------------------------------------------- reel table
G = 60 / 92; U_ = 60 / 116
REELS = [
    dict(id="guess-spacebox", time="11:30", music=("drive", 0), b=DR.B, scenes=[(r1_hook, 4), (r1_guess, 16), (end_card([("01.png", HQ), ("14.png", HQ), ("03.png", HQ)], (10, 16, 40), (0, 220, 255), "Light up your music"), 7)], cover=8000,
         caption="🔊 Can you guess the price? Watch till the end 👀\n\nOraimo SpaceBox Portable Bluetooth Speaker\n✔️ Personalized light show\n✔️ Thumping bass\n✔️ 8W audio output, 45mm driver\n✔️ 1800mAh battery\n\n💰 Price: 1,841৳ (regular 2,299৳)\n\n💬 Comment your guess before the reveal!",
         tags="#EverydayCart #Oraimo #SpaceBox #BluetoothSpeaker #GuessThePrice #Gadgets #TechBD"),
    dict(id="mom-must-haves", time="12:45", music=("gentle", 3), b=G, scenes=[(r2_hook, 4)] + [(r2_item(i), 3) for i in range(6)] + [(end_card([(x[0], x[1]) for x in BABY[:5]], (190, 110, 120), PEACH, "Gentle care, everyday"), 4)], cover=1500,
         caption="👶 নতুন মায়েদের জন্য! Mom's must-haves at Everyday Cart 💕\n\n🍼 Minitree 120 ml Bottle: 450৳\n🍼 Minitree Tritan Bottle: 450৳\n🥤 Minitree Duckbill Mumpot: 400৳\n🎁 10 Pc Baby Care Kit: 480৳\n🦷 Kodomo Baby Toothpaste: 280৳\n🧴 Kodomo Lotion Powder: 720৳",
         tags="#EverydayCart #BabyEssentials #NewMom #Minitree #Kodomo #BabyCare #BabyProductsBD"),
    dict(id="watch-vs", time="14:00", music=("drive", 2), b=DR.B, scenes=[(r3_vs, 18), (end_card([("09.png", HQ), ("02.png", HQ)], (24, 24, 30), YEL, "Smart on every wrist"), 7)], cover=5000,
         caption="⌚ Which smartwatch would you pick?\n\nCOLMI P81: 1,350৳\n✔️ 1.9\" HD display, Bluetooth calling, 100+ sports modes, IP68\n\nOraimo Watch 5 Lite: 1,650৳\n✔️ 2.01\" HD display, Bluetooth calling, 105+ sports modes, IP68\n\n💬 Comment COLMI or ORAIMO 👇",
         tags="#EverydayCart #SmartWatch #COLMI #Oraimo #ThisOrThat #Gadgets #TechBD"),
    dict(id="pov-cold-tea", time="15:15", music=("upbeat", 5), b=U_, scenes=[(r4_pov, 8), (r4_fix, 10), (end_card([("16.png", HQ), ("15.png", HQ), ("18.png", HQ)], (200, 90, 20), YEL, "Hot drinks, all day"), 6)], cover=6000,
         caption="☕ POV: শীতের সকালে চা বানালাম, ৫ মিনিট পরেই ঠান্ডা 😩\n\nসমাধান? Thermal tumblers from Everyday Cart 🔥\n\n💜 Premium Thermal Tumbler: 800৳\n💙 Big Mac 316 Thermos Cup: 1,000৳\n🤍 Premium Thermal Water Bottle: 800৳",
         tags="#EverydayCart #ThermalTumbler #WinterEssentials #Tea #ThermosCup #BanglaPOV"),
    dict(id="unbox-proove", time="16:30", music=("drive", 5), b=DR.B, scenes=[(r5_unbox, 8), (r5_feats, 10), (end_card([("03.png", HQ), ("11.png", HQ), ("10.png", HQ)], (14, 14, 18), (230, 40, 50), "Hear every beat"), 7)], cover=5500,
         caption="📦 Unboxing the Proove Intro Pro earbuds!\n\n✔️ 13mm driver, powerful sound\n✔️ Transparent ENC for clear calls\n✔️ Bluetooth 5.4, touch control\n✔️ LED display charging case\n✔️ Up to 6 hours playback\n\n💰 Price: 2,300৳",
         tags="#EverydayCart #Proove #Unboxing #WirelessEarbuds #TWS #Gadgets #TechBD"),
    dict(id="under-1000", time="17:45", music=("drive", 7), b=DR.B, scenes=[(r6_grid, 16), (end_card([(u[0], HQ) for u in U[:5]], (10, 120, 85), YEL, "Big value, small price"), 7)], cover=5800,
         caption="💸 Everything under 1,000 Taka!\n\n🎧 Awei T88 Earbuds: 990৳\n🎧 Awei T108 Earbuds: 950৳\n⏰ Silent Alarm Clock: 500৳\n🌡️ Smart LED Temperature Bottle: 350৳\n🍼 Minitree Duckbill Mumpot: 400৳\n🐻 Kids Thermal Bottle: 800৳",
         tags="#EverydayCart #Under1000 #BudgetFinds #Awei #OnlineShoppingBD"),
    dict(id="gift-guide", time="19:00", music=("upbeat", 0), b=U_, scenes=[(r7_hook, 4)] + [(r7_card(i), 5) for i in range(4)] + [(end_card([(g[1], HQ) for g in GIFTS], (60, 50, 70), CORAL, "Gift something they'll love"), 7)], cover=2000,
         caption="🎁 Gift ideas for every budget!\n\n⏰ Under 500৳: Silent Alarm Clock, 500৳\n🧸 Under 1,500৳: 22\" Big Teddy Bear, 1,150৳\n🎧 Under 2,000৳: Oraimo SpaceBuds Neo+, 1,940৳\n🧳 Big gift: Forkan Trolley Luggage, from 4,000৳",
         tags="#EverydayCart #GiftIdeas #TeddyBear #Oraimo #GiftsBD"),
    dict(id="top5-gadgets", time="20:15", music=("drive", 3), b=DR.B, scenes=[(r8_top, 17), (end_card([(x[1], HQ) for x in TOP], (30, 30, 40), YEL, "Your next gadget is here"), 7)], cover=5300,
         caption="🏆 Top 5 gadgets at Everyday Cart right now!\n\n#5 ⌚ COLMI P81 Smartwatch: 1,350৳\n#4 🎶 Oraimo Necklace Lite: 1,300৳\n#3 🔊 Oraimo SpaceBox Speaker: 1,841৳\n#2 🎧 Proove Intro Pro: 2,300৳\n#1 🔊 Awei KA5 20W Speaker: 2,525৳\n\n💬 Which one is your #1?",
         tags="#EverydayCart #Top5 #Gadgets #Oraimo #Awei #TechBD"),
    dict(id="good-night-clock", time="21:30", music=("gentle", 0), b=G, scenes=[(r9_night, 16), (end_card([("07.png", HQ), ("06.png", HQ)], NAVY, (255, 220, 140), "Sleep peacefully"), 5)], cover=7000,
         caption="🌙 Shhh... no ticking, just sleep.\n\nSilent Alarm Clock\n✔️ Non-ticking, silent operation\n✔️ Precise quartz movement\n✔️ Classic twin bell design\n✔️ Elegant bedside decor\n\n💰 Price: 500৳ (regular 800৳)\n\nশুভ রাত্রি 💤",
         tags="#EverydayCart #SilentClock #AlarmClock #Bedroom #HomeDecor #GoodNight"),
]
CTA = "\n\n⚡ Limited stock available!\n🛒 Order now: everydaycart.online\n📩 Or inbox us to place your order\n\n"

def encode(path, fn, dur):
    tmp = path[:-4] + ".tmp.mp4"; n = int(round(dur * FPS))
    p = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
                          "-c:v", "libx264", "-preset", "veryfast", "-crf", "18", "-pix_fmt", "yuv420p", tmp], stdin=subprocess.PIPE)
    for k in range(n): p.stdin.write(fn(k / FPS).convert("RGB").tobytes())
    p.stdin.close()
    if p.wait() == 0: os.replace(tmp, path)

def music(r, total, starts):
    kind, key = r["music"]
    if kind == "drive": mix = DR.drive(total, starts[1], starts[1:], starts[-1], key=key)
    elif kind == "upbeat": mix = MM.upbeat(total, key)
    else: mix = MM.gentle(total, key)
    return mix

def build(r, preview=False):
    b = r["b"]; prev = DARK; parts = []; s = 0; starts = []
    for k, (fn, beats) in enumerate(r["scenes"]):
        dur = beats * b; pv = prev
        parts.append(((lambda fn, pv: (lambda t: fn(t, b, pv)))(fn, pv), dur)); starts.append(s); s += dur
        tmp = fn(min(dur - .05, 1.0), b, pv)                   # colour of this scene for the next wipe
        prev = tuple(tmp.getpixel((5, H - 5))[:3])
    if preview: return parts, starts, s
    d = OUT + r["id"] + "/"; os.makedirs(d, exist_ok=True)
    for k, (fn, dur) in enumerate(parts): encode(d + f"s{k}.mp4", fn, dur)
    open(d + "list.txt", "w").write("".join(f"file 's{k}.mp4'\n" for k in range(len(parts))))
    mix = music(r, s, starts)
    wavfile.write(d + "music.wav", 44100, (np.stack([mix, mix], 1) * 32767).astype(np.int16))
    out = OUT + f"{r['time'].replace(':', '')}_{r['id']}.mp4"
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", d + "list.txt", "-i", d + "music.wav",
                    "-map", "0:v", "-map", "1:a", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-shortest", "-movflags", "+faststart", out], check=True)
    print(out, round(s, 1), flush=True)

if __name__ == "__main__":
    mode = sys.argv[1]; ids = sys.argv[2:]
    sel = [r for r in REELS if not ids or r["id"] in ids]
    if mode == "preview":
        shots = []
        for r in sel:
            parts, starts, total = build(r, True)
            for (fn, dur), st in zip(parts, starts):
                shots.append(fn(min(dur * .75, dur - .1)).convert("RGB"))
        cols = 8; rows = math.ceil(len(shots) / cols); sheet = Image.new("RGB", (cols * 216, rows * 384))
        for i, s_ in enumerate(shots): sheet.paste(s_.resize((216, 384), Image.LANCZOS), ((i % cols) * 216, (i // cols) * 384))
        sheet.save("/tmp/r9_sheet.jpg", quality=86)
    else:
        for r in sel: build(r)
