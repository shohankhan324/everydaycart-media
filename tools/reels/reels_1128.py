"""Everyday Cart Reel for 28 Nov: "Under 1,000 Tk earbuds": Awei T88 Wireless Earbuds (990 Tk, regular 1,450).
Flat palette: ink black + lime + hot pink, cream cards. Bangla hook in the first second ("১০০০ টাকার নিচে ভালো ইয়ারবাড?")
with a flat price meter, the earbuds drop in with a bounce, a price counter rolls down from the regular price to 990,
a checklist with only listing facts (ANC support, 10mm driver, IPX6, Bluetooth 5.4, 1 hour fast charging), a
"music, calls or movies" comment prompt, end card. Original 124 BPM drive track in key 7. About 21 s."""

import os as _os
_R = _os.path.dirname(_os.path.abspath(__file__)); _T = _os.path.dirname(_R)

import os, sys, math
from PIL import Image, ImageDraw
sys.path.insert(0, _T); sys.path.insert(0, _R)
from mega import T, TB, P, pill, bg, wipe, logo, disc, put, rgba, f, ease, back, clamp, HQ, WHITE
import reels9 as R9
from reels9 import end_card
import drive as DR

W, H = 1080, 1920
R9.OUT = _R + "/out/out1128/"; os.makedirs(R9.OUT, exist_ok=True)
B = DR.B
INK = (18, 18, 22); INK2 = (40, 40, 48); LIME = (196, 240, 64); PINK = (255, 84, 156); CREAM = (255, 247, 236)
SKY = (120, 200, 255); GREY = (130, 130, 140)
EB = "11.png"


def stripes(d, t, col, a=60):
    off = (t * 120) % 160
    for i in range(-2, 16):
        x = i * 160 + off
        d.polygon([(x, 0), (x + 60, 0), (x - 540, H), (x - 600, H)], fill=rgba(col, a))


def meter(img, cx, cy, w, level, col):
    d = ImageDraw.Draw(img)
    d.rounded_rectangle((cx - w / 2 + 10, cy - 40 + 12, cx + w / 2 + 10, cy + 40 + 12), radius=40, fill=rgba(INK2))
    d.rounded_rectangle((cx - w / 2, cy - 40, cx + w / 2, cy + 40), radius=40, fill=rgba(CREAM), outline=rgba(WHITE), width=6)
    if level > 0:
        d.rounded_rectangle((cx - w / 2 + 12, cy - 28, cx - w / 2 + 12 + (w - 24) * level, cy + 28), radius=28, fill=rgba(col))


def p_hook(t, b, prev):
    img = bg(INK); d = ImageDraw.Draw(img)
    stripes(d, t, INK2, 255)
    k1 = (t - .05) / .22
    if k1 > 0: put(img, TB("১০০০ টাকার নিচে", 700, 104, WHITE), W / 2, 470, scale=1.4 - .4 * ease(k1), a=clamp(k1 * 2))
    k2 = (t - .4) / .25
    if k2 > 0: put(img, TB("ভালো ইয়ারবাড?", 700, 150, LIME), W / 2, 660, scale=1.35 - .35 * back(k2), a=clamp(k2 * 2))
    lv = .2 + .55 * abs(math.sin(t * 2.4))
    meter(img, W / 2, 1060, 700, lv, PINK)
    put(img, T("BUDGET", f("Poppins-Bold.ttf", 40), GREY), W / 2 - 290, 1150)
    put(img, T("PREMIUM", f("Poppins-Bold.ttf", 40), GREY), W / 2 + 280, 1150)
    kk = back((t - 1.2) / .3)
    if kk > 0: put(img, pill("UNDER Tk 1,000?", 60, PINK, WHITE, padx=50), W / 2, 1380, scale=kk, rot=-3)
    kk2 = back((t - 1.7) / .3)
    if kk2 > 0: put(img, pill("YES, IT EXISTS", 52, LIME, INK, padx=46), W / 2, 1580, scale=kk2, rot=2)
    logo(img); return img


def p_reveal(t, b, prev):
    img = bg(LIME); d = ImageDraw.Draw(img)
    stripes(d, t, (214, 248, 120), 255)
    km = back(t / .4)
    if km > 0: disc(img, W / 2, 900, 400 * km, INK)
    drop = clamp(t / .45); y = 200 + 700 * ease(drop) - (40 * math.sin(clamp((t - .45) / .35) * math.pi) if t > .45 else 0)
    put(img, P(EB, 620, 560), W / 2, y, rot=-6 * (1 - drop))
    kt = back((t - .7) / .35)
    if kt > 0: put(img, T("Awei T88", f("Poppins-Bold.ttf", 130), INK), W / 2, 1440, scale=kt)
    ks = back((t - 1.0) / .35)
    if ks > 0: put(img, TB("ওয়্যারলেস ইয়ারবাড", 700, 76, INK), W / 2, 1580, scale=ks)
    ko = back((t - 1.3) / .35)
    if ko > 0: put(img, pill("ANC SUPPORT", 46, PINK, WHITE, padx=40), W / 2, 1720, scale=ko, rot=-2)
    logo(img); return wipe(img, prev, t, LIME)


def p_price(t, b, prev):
    img = bg(PINK); d = ImageDraw.Draw(img)
    stripes(d, t, (240, 66, 140), 255)
    put(img, TB("দাম কত?", 700, 120, INK), W / 2, 230, scale=back(t / .3))
    kd = back(t / .4); disc(img, W / 2, 640, 280 * kd, CREAM)
    put(img, P(EB, 400, 380), W / 2, 650 + 8 * math.sin(t * 3), scale=kd)
    g = ease(clamp((t - .5) / 1.4)); n = int(round(1450 - (1450 - 990) * g))
    card = Image.new("RGBA", (800, 400), (0, 0, 0, 0)); cd = ImageDraw.Draw(card)
    cd.rounded_rectangle((16, 20, 799, 399), radius=56, fill=rgba(INK))
    cd.rounded_rectangle((0, 0, 783, 379), radius=56, fill=rgba(CREAM), outline=rgba(INK), width=8)
    lt = T("ONLY" if g >= 1 else "PRICE", f("Poppins-Bold.ttf", 46), PINK); card.alpha_composite(lt, (392 - lt.width // 2, 30))
    pt = T(f"Tk {n:,}", f("Poppins-Bold.ttf", 150), INK); card.alpha_composite(pt, (392 - pt.width // 2, 100))
    if g >= 1:
        rt = T("Regular Tk 1,450", f("Poppins-Medium.ttf", 44), GREY); rx = 392 - rt.width // 2; card.alpha_composite(rt, (rx, 296))
        ImageDraw.Draw(card).line((rx + 14, 296 + rt.height // 2, rx + rt.width - 14, 296 + rt.height // 2), fill=rgba(GREY), width=5)
    put(img, card, W / 2, 1210, scale=back((t - .2) / .4), rot=-2)
    kc = back((t - 2.2) / .35)
    if kc > 0: put(img, TB("দাম মাত্র ৯৯০ টাকা", 700, 90, INK), W / 2, 1560, scale=kc)
    logo(img); return wipe(img, prev, t, PINK)


CHECK = [("ANC support", LIME), ("10mm driver unit", PINK), ("IPX6 water resistant", SKY), ("Bluetooth 5.4, touch control", LIME), ("1 hour fast charging", PINK)]


def p_check(t, b, prev):
    img = bg(INK); d = ImageDraw.Draw(img)
    stripes(d, t, INK2, 255)
    put(img, T("What you get", f("Poppins-Bold.ttf", 92), WHITE), W / 2, 220, scale=back(t / .35))
    put(img, TB("কম দামে দরকারি সব ফিচার", 700, 64, LIME), W / 2, 340, scale=back((t - .15) / .35))
    kd = back((t - .1) / .4)
    if kd > 0: disc(img, W / 2, 590, 180 * kd, LIME)
    put(img, P(EB, 280, 260), W / 2, 590 + 8 * math.sin(t * 3), scale=back((t - .2) / .4), rot=3 * math.sin(t * 2))
    for i, (txt, col) in enumerate(CHECK):
        st = .5 + .42 * i; kk = back((t - st) / .32)
        if kk <= 0: continue
        card = Image.new("RGBA", (920, 150), (0, 0, 0, 0)); cd = ImageDraw.Draw(card)
        cd.rounded_rectangle((10, 12, 919, 149), radius=34, fill=rgba(col))
        cd.rounded_rectangle((0, 0, 909, 137), radius=34, fill=rgba(CREAM), outline=rgba(INK), width=6)
        cd.ellipse((30, 26, 116, 112), fill=rgba(col), outline=rgba(INK), width=5)
        tick = clamp((t - st - .2) / .2)
        if tick > 0:
            pts = [(50, 70), (68, 90), (98, 50)]
            if tick < .5: pts = pts[:2]
            cd.line(pts, fill=rgba(INK), width=11, joint="curve")
        tt = T(txt, f("Poppins-Bold.ttf", 52), INK); card.alpha_composite(tt, (140, 69 - tt.height // 2))
        put(img, card, W / 2, 870 + i * 175, scale=kk, rot=(-1.5 if i % 2 == 0 else 1.5))
    logo(img); return wipe(img, prev, t, INK)


USES = [("Music", LIME, "1"), ("Calls", SKY, "2"), ("Movies", PINK, "3")]


def p_uses(t, b, prev):
    img = bg(CREAM); d = ImageDraw.Draw(img)
    put(img, TB("কিসে বেশি ব্যবহার করবেন?", 700, 84, INK), W / 2, 260, scale=back(t / .3))
    put(img, P(EB, 420, 380), W / 2, 620 + 10 * math.sin(t * 3), scale=back((t - .1) / .4))
    for i, (txt, col, num) in enumerate(USES):
        st = .4 + .35 * i; kk = back((t - st) / .3)
        if kk <= 0: continue
        card = Image.new("RGBA", (300, 300), (0, 0, 0, 0)); cd = ImageDraw.Draw(card)
        cd.rounded_rectangle((10, 12, 299, 299), radius=40, fill=rgba(INK))
        cd.rounded_rectangle((0, 0, 289, 287), radius=40, fill=rgba(col), outline=rgba(INK), width=6)
        nt = T(num, f("Poppins-Bold.ttf", 120), INK); card.alpha_composite(nt, (145 - nt.width // 2, 40))
        tt = T(txt, f("Poppins-Bold.ttf", 50), INK); card.alpha_composite(tt, (145 - tt.width // 2, 190))
        put(img, card, 200 + i * 340, 1110, scale=kk, rot=(-3, 2, -2)[i])
    kc = back((t - 1.6) / .35)
    if kc > 0: put(img, pill("COMMENT 1, 2 OR 3", 56, INK, WHITE, padx=50), W / 2, 1440, scale=kc, rot=-2)
    kb = back((t - 2.0) / .35)
    if kb > 0: put(img, TB("কমেন্টে জানান", 700, 76, PINK), W / 2, 1600, scale=kb)
    logo(img); return wipe(img, prev, t, CREAM)


REELS = [
    dict(id="reel-awei-t88-earbuds-under-1000", time="18:30", music=("drive", 7), b=B, cover=1500,
         scenes=[(p_hook, 5), (p_reveal, 7), (p_price, 8), (p_check, 10), (p_uses, 7),
                 (end_card([(EB, HQ), ("02.png", HQ), ("31.png", HQ)], INK, LIME, "Good sound, smart price."), 7)]),
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
