"""Everyday Cart Reel for 18 Nov: "Rooftop adda volume check" for the Awei KA5 20W speaker.
Flat night rooftop (moon, city skyline, string lights) with a Bangla hook, the speaker drops in on the beat with
sound rings; spec scene with beat bouncing equalizer bars and count up numbers (all specs from the store listing);
price reveal on a yellow card; end card. Midnight teal + electric yellow + cyan palette, original drive track in key 4.
About 18 s."""

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
R9.OUT = _R + "/out/out1118/"; os.makedirs(R9.OUT, exist_ok=True)
NIGHT = (16, 40, 58); NIGHT2 = (24, 58, 80); SKYLINE = (10, 26, 38); YEL = (255, 212, 0); CYAN = (96, 226, 214)
SPK = "14.png"   # Awei KA5 20W
BPM_B = DR.B


def skyline(img, t):
    d = ImageDraw.Draw(img)
    d.ellipse((780, 250, 920, 390), fill=rgba((255, 240, 200)))
    d.ellipse((815, 236, 955, 376), fill=rgba(NIGHT))            # crescent moon
    for i, (x, y) in enumerate([(120, 300), (260, 420), (420, 260), (600, 380), (980, 520), (60, 560), (700, 200)]):
        tw = 0.5 + 0.5 * math.sin(t * 3 + i)
        r = 4 + 2 * tw; d.ellipse((x - r, y - r, x + r, y + r), fill=rgba(WHITE, int(140 + 115 * tw)))
    bx = [(0, 1340, 150), (150, 1240, 120), (270, 1300, 160), (430, 1180, 110), (540, 1280, 170), (710, 1220, 130), (840, 1320, 240)]
    for x, y, w in bx:
        d.rectangle((x, y, x + w, H), fill=rgba(SKYLINE))
        for wy in range(y + 40, 1560, 70):
            for wx in range(x + 22, x + w - 30, 46):
                if (wx * 7 + wy * 3) % 5 < 2: d.rectangle((wx, wy, wx + 18, wy + 26), fill=rgba((255, 214, 120), 200))
    # rooftop floor + parapet
    d.rectangle((0, 1560, W, H), fill=rgba(NIGHT2)); d.rectangle((0, 1540, W, 1580), fill=rgba((40, 84, 110)))
    # string lights
    pts = [(x, 470 + 70 * math.sin(math.pi * x / W)) for x in range(-20, W + 40, 90)]
    d.line(pts, fill=rgba((60, 90, 110)), width=3)
    for i, (x, y) in enumerate(pts):
        on = (int(t / BPM_B) + i) % 2
        c = YEL if on else CYAN; d.ellipse((x - 11, y + 4, x + 11, y + 26), fill=rgba(c))


def rings(img, cx, cy, t, col):
    ov = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(ov)
    for k in range(3):
        ph = ((t / BPM_B) + k / 3) % 1
        r = 240 + 300 * ph; a = int(200 * (1 - ph))
        d.ellipse((cx - r, cy - r, cx + r, cy + r), outline=rgba(col, a), width=10)
    img.alpha_composite(ov)


def p_hook(t, b, prev):
    img = bg(NIGHT); skyline(img, t)
    put(img, TB("ছাদের আড্ডায়", 700, 112, WHITE, True), W / 2, 640, scale=1.3 - .3 * ease(t / .25), a=clamp(t / .12))
    kk = (t - .4) / .3
    if kk > 0: put(img, TB("গান চাই?", 700, 176, YEL, True), W / 2, 850, scale=1.3 - .3 * ease(kk), a=clamp(kk * 2))
    k = (t - .7) / .35
    if k > 0:
        y = 1250 - (1 - ease(min(1, k))) * 1300
        if k >= 1: rings(img, W / 2, 1250, t, CYAN)
        bump = 1 + .04 * max(0, math.cos(2 * math.pi * t / b)) if k >= 1 else 1
        put(img, P(SPK, 420, 560), W / 2, y, scale=bump)
    kk = back((t - 1.6) / .35)
    if kk > 0: put(img, pill("VOLUME CHECK", 58, YEL, SKYLINE, padx=54), W / 2, 1680, scale=kk)
    logo(img); return img


SPECS = [("20W", "10W x 2 output", 20, "W"), ("2400", "mAh battery", 2400, ""), ("8h", "playback (7.5 to 8h, 70% vol)", 8, "h"),
         ("IPX5", "Waterproof", None, ""), ("5.3", "Bluetooth", None, "")]


def p_specs(t, b, prev):
    img = bg(NIGHT2); d = ImageDraw.Draw(img)
    # equalizer bars bouncing to the beat behind the speaker
    n = 13
    for i in range(n):
        x = 90 + i * (W - 180) / (n - 1)
        hgt = 80 + 220 * abs(math.sin(t * 2 * math.pi / b * .5 + i * .7)) * (0.6 + 0.4 * math.sin(i * 1.3 + t))
        col = YEL if i % 2 else CYAN
        d.rounded_rectangle((x - 22, 760 - hgt, x + 22, 760), radius=14, fill=rgba(col, 120))
    disc(img, W / 2, 560, 250, (36, 80, 106))
    put(img, P(SPK, 300, 430), W / 2, 560 + 10 * math.sin(t * 3), rot=4 * math.sin(t * 2 * math.pi / b / 2))
    put(img, T("Awei KA5 20W Speaker", f("Poppins-Bold.ttf", 54), WHITE), W / 2, 880, a=ease(t / .3))
    for i, (big, small, num, unit) in enumerate(SPECS):
        st = (1.2 + 2.6 * i) * b; kk = ease((t - st) / .3)
        if kk <= 0: continue
        y = 990 + i * 150
        ov = Image.new("RGBA", (W, 130), (0, 0, 0, 0)); od = ImageDraw.Draw(ov)
        od.rounded_rectangle((60, 0, W - 60, 124), radius=34, fill=(255, 255, 255, int(250 * kk))); img.alpha_composite(ov, (int(-200 * (1 - kk)), y))
        if num:
            v = num * ease(min(1, (t - st) / (1.4 * b)))
            txt = (f"{v:,.0f}" if num > 50 else f"{v:.0f}") + unit
        else:
            txt = big
        col = (20, 120, 112) if i % 2 else (196, 140, 0)
        put(img, T(txt, f("Poppins-Bold.ttf", 62), col), 240 + int(-200 * (1 - kk)), y + 62, a=kk)
        fsz = 42
        while f("Poppins-Medium.ttf", fsz).getlength(small) > 560 and fsz > 24: fsz -= 2
        put(img, T(small, f("Poppins-Medium.ttf", fsz), SKYLINE), 680 + int(-200 * (1 - kk)), y + 62, a=kk)
    logo(img); return wipe(img, prev, t, NIGHT2)


def p_price(t, b, prev):
    img = bg(YEL); d = ImageDraw.Draw(img)
    for i in range(10):
        r = 120 + i * 120; d.ellipse((W / 2 - r, 980 - r, W / 2 + r, 980 + r), outline=rgba((255, 196, 0)), width=26)
    put(img, TB("ব্লুটুথ স্পিকারের দাম", 700, 92, SKYLINE), W / 2, 300, scale=back(t / .35))
    put(img, P(SPK, 300, 470), W / 2, 830 + 12 * math.sin(t * 4), scale=back((t - .15) / .4))
    kk = back((t - .7) / .35)
    if kk > 0:
        card = Image.new("RGBA", (720, 300), (0, 0, 0, 0)); cd = ImageDraw.Draw(card)
        cd.rounded_rectangle((0, 0, 719, 299), radius=50, fill=rgba(SKYLINE))
        pt = T("Tk 2,525", f("Poppins-Bold.ttf", 120), WHITE); card.alpha_composite(pt, (360 - pt.width // 2, 40))
        rt = "Regular Tk 2,849"; rf_ = f("Poppins-Medium.ttf", 44); rw = rf_.getlength(rt)
        cd.text((360 - rw / 2, 200), rt, font=rf_, fill=rgba(CYAN)); cd.line((360 - rw / 2 - 4, 230, 360 + rw / 2 + 4, 230), fill=rgba(CYAN), width=4)
        put(img, card, W / 2, 1350, scale=kk, rot=-3)
    kk = back((t - 1.3) / .35)
    if kk > 0: put(img, pill("Inbox us to order", 50, WHITE, SKYLINE, padx=48), W / 2, 1630, scale=kk)
    logo(img); return wipe(img, prev, t, YEL)


REELS = [
    dict(id="reel-awei-ka5-rooftop-volume", time="18:30", music=("drive", 4), b=DR.B, cover=2600,
         scenes=[(p_hook, 6), (p_specs, 16), (p_price, 8),
                 (end_card([(SPK, HQ), ("01.png", HQ), ("12.png", HQ)], NIGHT, YEL, "Sound for every adda"), 8)]),
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
