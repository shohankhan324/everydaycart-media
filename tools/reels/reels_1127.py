"""Everyday Cart Reel for 27 Nov: "All day, one neckband": Oraimo Necklace Lite ENC Wireless Neckband (1,300 Tk, regular 1,485).
Flat palette: deep navy + tangerine + mint, cream cards. Bangla hook in the first second ("সারাদিন চার্জের টেনশন?") over a
blinking low battery icon, the neckband swings in like a pendulum, a day timeline (morning music, office calls, evening ride)
fills a big flat battery that counts up to 30 hours, a checklist with only listing facts (up to 30 hours playtime, ENC
calls, dual device connectivity, call vibration alert), price card with a comment prompt, end card.
Original 124 BPM drive track in key 4. About 23 s."""

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
R9.OUT = _R + "/out/out1127/"; os.makedirs(R9.OUT, exist_ok=True)
B = DR.B
NAVY = (22, 30, 74); NAVY2 = (36, 48, 110); TANG = (255, 138, 60); MINT = (120, 226, 190); CREAM = (255, 246, 232)
INK = (16, 18, 36); RED = (255, 84, 84); BUTTER = (255, 220, 110)
NB = "04.png"


def battery(d, cx, cy, w, h, level, fill, ink=INK, shell=CREAM):
    x0, y0, x1, y1 = cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2
    d.rounded_rectangle((x0 + 12, y0 + 12, x1 + 12, y1 + 12), radius=36, fill=rgba(ink))
    d.rounded_rectangle((x0, y0, x1, y1), radius=36, fill=rgba(shell), outline=rgba(ink), width=10)
    d.rounded_rectangle((x1, cy - h * .18, x1 + 34, cy + h * .18), radius=10, fill=rgba(ink))
    if level > 0:
        d.rounded_rectangle((x0 + 22, y0 + 22, x0 + 22 + (w - 44) * level, y1 - 22), radius=20, fill=rgba(fill))


def dots(d, t, col, a=110):
    for i in range(14):
        x = (i * 157) % 1040 + 20; y = (i * 263 + t * 40 * (1 + i % 3)) % 1960 - 20
        r = 6 + (i % 3) * 4; d.ellipse((x - r, y - r, x + r, y + r), fill=rgba(col, a))


def p_hook(t, b, prev):
    img = bg(NAVY); d = ImageDraw.Draw(img)
    dots(d, t, MINT, 90)
    blink = 1 if (t * 4) % 2 < 1.3 else 0
    battery(d, W / 2, 1180, 520, 250, .14 if blink else 0, RED)
    k1 = (t - .05) / .22
    if k1 > 0: put(img, TB("সারাদিন চার্জের", 700, 100, WHITE), W / 2, 420, scale=1.4 - .4 * ease(k1), a=clamp(k1 * 2))
    k2 = (t - .4) / .25
    if k2 > 0: put(img, TB("টেনশন?", 700, 170, TANG), W / 2, 610, scale=1.35 - .35 * back(k2), a=clamp(k2 * 2))
    kk = back((t - 1.3) / .3)
    if kk > 0: put(img, pill("LOW BATTERY AGAIN?", 46, RED, WHITE, padx=40), W / 2, 1420, scale=kk, rot=-3)
    kk2 = back((t - 1.75) / .3)
    if kk2 > 0: put(img, pill("TRY THIS", 56, MINT, INK, padx=50), W / 2, 1620, scale=kk2, rot=2)
    logo(img); return img


def p_reveal(t, b, prev):
    img = bg(TANG); d = ImageDraw.Draw(img)
    dots(d, t, WHITE, 70)
    km = back(t / .4)
    if km > 0: disc(img, W / 2, 960, 410 * km, CREAM)
    sw = 24 * math.exp(-t * 1.6) * math.cos(t * 6)          # pendulum swing settling down
    drop = ease(clamp(t / .5))
    put(img, P(NB, 600, 760), W / 2, 260 + 720 * drop, rot=sw)
    kt = back((t - .7) / .35)
    if kt > 0: put(img, T("Oraimo Necklace Lite", f("Poppins-Bold.ttf", 82), INK), W / 2, 1490, scale=kt)
    ks = back((t - 1.0) / .35)
    if ks > 0: put(img, TB("হালকা ওয়্যারলেস নেকব্যান্ড", 700, 70, NAVY), W / 2, 1610, scale=ks)
    ko = back((t - 1.3) / .35)
    if ko > 0: put(img, pill("OFFICIAL ORAIMO", 44, NAVY, WHITE, padx=40), W / 2, 1740, scale=ko, rot=-2)
    logo(img); return wipe(img, prev, t, TANG)


DAY = [("Morning music", TANG), ("Office calls", MINT), ("Evening ride", BUTTER)]


def p_day(t, b, prev):
    img = bg(CREAM); d = ImageDraw.Draw(img)
    put(img, TB("সারাদিন চলবে?", 700, 104, NAVY), W / 2, 230, scale=back(t / .3))
    for i, (txt, col) in enumerate(DAY):
        st = .25 + .45 * i; kk = back((t - st) / .3)
        if kk <= 0: continue
        card = Image.new("RGBA", (300, 120), (0, 0, 0, 0)); cd = ImageDraw.Draw(card)
        cd.rounded_rectangle((8, 10, 299, 119), radius=28, fill=rgba(INK))
        cd.rounded_rectangle((0, 0, 291, 109), radius=28, fill=rgba(col), outline=rgba(INK), width=5)
        tt = T(txt, f("Poppins-Bold.ttf", 34), INK); card.alpha_composite(tt, (146 - tt.width // 2, 55 - tt.height // 2))
        put(img, card, 200 + i * 340, 440, scale=kk, rot=(-3, 2, -2)[i])
    put(img, P(NB, 460, 500), W / 2, 790 + 10 * math.sin(t * 3), scale=back((t - .2) / .4))
    g = ease(clamp((t - 1.4) / 1.8)); n = int(round(30 * g))
    battery(d, W / 2 - 17, 1290, 640, 260, g, MINT)
    put(img, T(f"{n}h", f("Poppins-Bold.ttf", 140), NAVY), W / 2 - 17, 1290)
    ks = back((t - 3.2) / .3)
    if ks > 0: put(img, pill("UP TO 30 HOURS PLAYTIME", 54, NAVY, WHITE, padx=46), W / 2, 1530, scale=ks, rot=-2)
    kb = back((t - 3.5) / .35)
    if kb > 0: put(img, TB("একবার চার্জে সারাদিন গান", 700, 70, TANG), W / 2, 1690, scale=kb)
    logo(img); return wipe(img, prev, t, CREAM)


CHECK = [("Up to 30 hours playtime", TANG), ("ENC for clear calls", MINT), ("Dual device connectivity", BUTTER), ("Call vibration alert", (190, 170, 255))]


def p_check(t, b, prev):
    img = bg(NAVY); d = ImageDraw.Draw(img)
    dots(d, t, TANG, 70)
    put(img, T("Why it works all day", f("Poppins-Bold.ttf", 80), WHITE), W / 2, 230, scale=back(t / .35))
    put(img, TB("কল আর গান দুটোই পরিষ্কার", 700, 64, MINT), W / 2, 340, scale=back((t - .15) / .35))
    kd = back((t - .1) / .4)
    if kd > 0: disc(img, W / 2, 630, 210 * kd, CREAM)
    put(img, P(NB, 300, 340), W / 2, 630 + 8 * math.sin(t * 3), scale=back((t - .2) / .4), rot=3 * math.sin(t * 2))
    for i, (txt, col) in enumerate(CHECK):
        st = .6 + .5 * i; kk = back((t - st) / .32)
        if kk <= 0: continue
        card = Image.new("RGBA", (920, 150), (0, 0, 0, 0)); cd = ImageDraw.Draw(card)
        cd.rounded_rectangle((10, 12, 919, 149), radius=34, fill=rgba(INK))
        cd.rounded_rectangle((0, 0, 909, 137), radius=34, fill=rgba(CREAM), outline=rgba(INK), width=6)
        cd.ellipse((30, 26, 116, 112), fill=rgba(col), outline=rgba(INK), width=5)
        tick = clamp((t - st - .2) / .2)
        if tick > 0:
            pts = [(50, 70), (68, 90), (98, 50)]
            if tick < .5: pts = pts[:2]
            cd.line(pts, fill=rgba(INK), width=11, joint="curve")
        tt = T(txt, f("Poppins-Bold.ttf", 52), INK); card.alpha_composite(tt, (140, 69 - tt.height // 2))
        put(img, card, W / 2, 940 + i * 180, scale=kk, rot=(-1.5 if i % 2 == 0 else 1.5))
    logo(img); return wipe(img, prev, t, NAVY)


def p_price(t, b, prev):
    img = bg(TANG); d = ImageDraw.Draw(img)
    dots(d, t, WHITE, 80)
    put(img, TB("দাম কত?", 700, 120, WHITE), W / 2, 230, scale=back(t / .3))
    kd = back(t / .4); disc(img, W / 2, 720, 310 * kd, CREAM)
    put(img, P(NB, 430, 480), W / 2, 730, scale=kd)
    kk = back((t - .7) / .4)
    if kk > 0:
        card = Image.new("RGBA", (780, 380), (0, 0, 0, 0)); cd = ImageDraw.Draw(card)
        cd.rounded_rectangle((16, 20, 779, 379), radius=56, fill=rgba(NAVY))
        cd.rounded_rectangle((0, 0, 763, 359), radius=56, fill=rgba(CREAM), outline=rgba(INK), width=8)
        lt = T("ONLY", f("Poppins-Bold.ttf", 44), TANG); card.alpha_composite(lt, (382 - lt.width // 2, 30))
        pt = T("Tk 1,300", f("Poppins-Bold.ttf", 140), INK); card.alpha_composite(pt, (382 - pt.width // 2, 98))
        rt = T("Regular Tk 1,485", f("Poppins-Medium.ttf", 42), (120, 120, 130)); rx = 382 - rt.width // 2; card.alpha_composite(rt, (rx, 282))
        ImageDraw.Draw(card).line((rx + 14, 282 + rt.height // 2, rx + rt.width - 14, 282 + rt.height // 2), fill=rgba((120, 120, 130)), width=5)
        put(img, card, W / 2, 1250, scale=kk, rot=-2)
    kc = back((t - 1.6) / .35)
    if kc > 0: put(img, TB("কোথায় বেশি পরবেন? কমেন্ট করুন", 700, 60, NAVY), W / 2, 1570, scale=kc)
    logo(img); return wipe(img, prev, t, TANG)


REELS = [
    dict(id="reel-oraimo-necklace-lite-all-day-battery", time="18:30", music=("drive", 4), b=B, cover=2000,
         scenes=[(p_hook, 5), (p_reveal, 7), (p_day, 10), (p_check, 10), (p_price, 9),
                 (end_card([(NB, HQ), ("13.png", HQ), ("14.png", HQ)], TANG, NAVY, "Music all day, calls all clear."), 7)]),
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
