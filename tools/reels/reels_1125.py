"""Everyday Cart Reel for 25 Nov: "Winter morning walk, phone in the pocket": COLMI P81 Calling Smartwatch (1,350 Tk).
Flat palette: dawn navy + sunrise orange + mint, cream cards. Bangla hook in the first second ("শীতের সকালে হাঁটতে যান?")
over a flat sunrise with drifting fog bands, the watch drops onto a cream disc with a ringing call bubble, a 0 to 100+
sports mode counter, spec checklist (only listing facts: 1.9 inch HD display, Bluetooth calling, IP68, 300mAh battery),
price card (1,350, regular 1,540) with a comment prompt, end card. Original upbeat synth track (116 BPM) in key 5. About 23 s."""

import os as _os
_R = _os.path.dirname(_os.path.abspath(__file__)); _T = _os.path.dirname(_R)

import os, sys, math
from PIL import Image, ImageDraw
sys.path.insert(0, _T); sys.path.insert(0, _R)
from mega import T, TB, P, pill, bg, wipe, logo, disc, put, rgba, f, ease, back, clamp, HQ, WHITE
import reels9 as R9
from reels9 import end_card

W, H = 1080, 1920
R9.OUT = _R + "/out/out1125/"; os.makedirs(R9.OUT, exist_ok=True)
UB = 60 / 116
NAVY = (28, 40, 96); NAVY2 = (40, 56, 124); SUN = (255, 128, 60); MINT = (150, 226, 196)
CREAM = (255, 244, 230); INK = (20, 22, 30); FOG = (196, 200, 236)
WATCH = "09.png"


def p_hook(t, b, prev):
    img = bg(NAVY); d = ImageDraw.Draw(img)
    rise = ease(t / 2.2); sy = 1380 - 260 * rise
    d.ellipse((W / 2 - 330, sy - 330, W / 2 + 330, sy + 330), fill=rgba((70, 70, 140)))
    d.ellipse((W / 2 - 250, sy - 250, W / 2 + 250, sy + 250), fill=rgba(SUN))
    d.ellipse((-400, 1300, 760, 2100), fill=rgba(NAVY2))
    d.ellipse((360, 1340, 1500, 2100), fill=rgba((52, 72, 150)))
    d.rectangle((0, 1640, W, H), fill=rgba((52, 72, 150)))
    for i, (y, w_, sp) in enumerate(((1180, 560, 60), (1300, 700, -45), (1480, 620, 70))):   # drifting fog bands
        x = (W / 2 - w_ / 2) + sp * t + (i - 1) * 120
        d.rounded_rectangle((x, y, x + w_, y + 44), radius=22, fill=rgba(FOG, 150))
    k1 = (t - .05) / .22
    if k1 > 0: put(img, TB("শীতের সকালে হাঁটতে যান?", 700, 96, WHITE), W / 2, 380, scale=1.4 - .4 * ease(k1), a=clamp(k1 * 2))
    k2 = (t - .9) / .25
    if k2 > 0: put(img, TB("ফোন থাকুক পকেটে", 700, 116, MINT), W / 2, 570, scale=1.35 - .35 * back(k2), a=clamp(k2 * 2))
    kk = back((t - 1.6) / .3)
    if kk > 0: put(img, pill("MORNING WALK MODE", 52, SUN, INK, padx=46), W / 2, 1780, scale=kk, rot=-3)
    logo(img); return img


def call_bubble(img, cx, cy, t, s):
    d = ImageDraw.Draw(img); w, h = 540 * s, 130 * s
    if s <= 0.05: return
    d.rounded_rectangle((cx - w / 2 + 10, cy - h / 2 + 12, cx + w / 2 + 10, cy + h / 2 + 12), radius=int(h / 2), fill=rgba(INK))
    d.rounded_rectangle((cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2), radius=int(h / 2), fill=rgba(MINT), outline=rgba(INK), width=6)
    r = 42 * s; px = cx - w / 2 + 70 * s
    d.ellipse((px - r, cy - r, px + r, cy + r), fill=rgba((40, 170, 90)))
    for k in range(3):   # ringing arcs
        ph = (t * 2 + k / 3) % 1; rr = r + 10 + 26 * ph
        d.arc((px - rr, cy - rr, px + rr, cy + rr), -60, 60, fill=rgba(INK, int(255 * (1 - ph))), width=5)
    put(img, T("Incoming call", f("Poppins-Bold.ttf", max(8, int(46 * s))), INK), cx + 50 * s, cy)


def p_reveal(t, b, prev):
    img = bg(SUN)
    d = ImageDraw.Draw(img)
    for i in range(9): d.ellipse((60 + i * 120 - 7, 1840 - 7, 60 + i * 120 + 7, 1840 + 7), fill=rgba(CREAM))
    km = back(t / .45)
    if km > 0: disc(img, W / 2, 960, 390 * km, CREAM)
    drop = ease((t - .05) / .5)
    if drop > 0: put(img, P(WATCH, 560, 640), W / 2, 980 - 700 * (1 - drop), rot=-4 + 4 * drop)
    kt = back((t - .6) / .35)
    if kt > 0: put(img, T("COLMI P81 Calling Smartwatch", f("Poppins-Bold.ttf", 66), INK), W / 2, 260, scale=kt)
    ks = back((t - .9) / .35)
    if ks > 0: put(img, TB("কলিং স্মার্ট ওয়াচ", 700, 86, WHITE), W / 2, 380, scale=ks)
    call_bubble(img, W / 2, 1490, t, back((t - 1.4) / .35))
    kp = back((t - 2.2) / .35)
    if kp > 0: put(img, TB("কল ধরুন হাত থেকেই", 700, 70, INK), W / 2, 1660, scale=kp)
    logo(img); return wipe(img, prev, t, SUN)


def p_modes(t, b, prev):
    img = bg(CREAM); d = ImageDraw.Draw(img)
    for k in range(6): d.rounded_rectangle((-60 + k * 220, 1560 + (k % 2) * 40, 100 + k * 220, 1600 + (k % 2) * 40), radius=20, fill=rgba(MINT))
    kd = back(t / .4)
    if kd > 0:
        disc(img, W / 2, 760, 300 * kd, MINT)
        put(img, P(WATCH, 440, 500), W / 2, 770, scale=kd, rot=3)
    n = int(round(100 * ease(clamp((t - .4) / 1.6))))
    put(img, T(f"{n}+" if n >= 100 else str(n), f("Poppins-Bold.ttf", 230), NAVY), W / 2, 1230)
    ks = back((t - .5) / .3)
    if ks > 0: put(img, pill("SPORTS MODES", 56, SUN, INK, padx=50), W / 2, 1400, scale=ks, rot=-2)
    put(img, TB("প্রিয় খেলা কোনটা?", 700, 104, NAVY), W / 2, 280, scale=back(t / .3))
    kb = back((t - 2.2) / .35)
    if kb > 0: put(img, TB("প্রতিদিনের হাঁটায় সঙ্গী", 700, 70, SUN), W / 2, 1720, scale=kb)
    logo(img); return wipe(img, prev, t, CREAM)


CHECK = [("1.9\" HD display", SUN), ("Bluetooth calling", MINT), ("IP68 water resistant", (150, 170, 250)), ("300mAh battery", (255, 214, 104))]


def p_check(t, b, prev):
    img = bg(NAVY)
    put(img, T("Walk ready", f("Poppins-Bold.ttf", 92), WHITE), W / 2, 250, scale=back(t / .35))
    put(img, TB("সকাল থেকে রাত", 700, 66, MINT), W / 2, 365, scale=back((t - .15) / .35))
    put(img, P(WATCH, 400, 420), W / 2, 650 + 6 * math.sin(t * 3), scale=back((t - .2) / .4))
    for i, (txt, col) in enumerate(CHECK):
        st = .7 + .5 * i; kk = back((t - st) / .32)
        if kk <= 0: continue
        card = Image.new("RGBA", (900, 150), (0, 0, 0, 0)); cd = ImageDraw.Draw(card)
        cd.rounded_rectangle((10, 12, 899, 149), radius=34, fill=rgba(SUN))
        cd.rounded_rectangle((0, 0, 889, 137), radius=34, fill=rgba(CREAM), outline=rgba(INK), width=6)
        cd.ellipse((30, 26, 116, 112), fill=rgba(col), outline=rgba(INK), width=5)
        tick = clamp((t - st - .2) / .2)
        if tick > 0:
            pts = [(50, 70), (68, 90), (98, 50)]
            if tick < .5: pts = pts[:2]
            cd.line(pts, fill=rgba(INK), width=11, joint="curve")
        tt = T(txt, f("Poppins-Bold.ttf", 54), INK); card.alpha_composite(tt, (140, 69 - tt.height // 2))
        put(img, card, W / 2, 1010 + i * 180, scale=kk, rot=(-1.5 if i % 2 == 0 else 1.5))
    logo(img); return wipe(img, prev, t, NAVY)


def p_price(t, b, prev):
    img = bg(NAVY2); d = ImageDraw.Draw(img)
    for i in range(7): d.ellipse((80 + i * 150 - 8, 1780 - 8, 80 + i * 150 + 8, 1780 + 8), fill=rgba(MINT))
    put(img, TB("দাম কত?", 700, 120, WHITE), W / 2, 230, scale=back(t / .3))
    kd = back(t / .4); disc(img, W / 2, 740, 310 * kd, SUN)
    put(img, P(WATCH, 460, 480), W / 2, 750, scale=kd)
    kk = back((t - .7) / .4)
    if kk > 0:
        card = Image.new("RGBA", (780, 380), (0, 0, 0, 0)); cd = ImageDraw.Draw(card)
        cd.rounded_rectangle((16, 20, 779, 379), radius=56, fill=rgba(MINT))
        cd.rounded_rectangle((0, 0, 763, 359), radius=56, fill=rgba(CREAM), outline=rgba(INK), width=8)
        lt = T("ONLY", f("Poppins-Bold.ttf", 44), SUN); card.alpha_composite(lt, (382 - lt.width // 2, 30))
        pt = T("Tk 1,350", f("Poppins-Bold.ttf", 150), INK); card.alpha_composite(pt, (382 - pt.width // 2, 96))
        rt = T("Regular Tk 1,540", f("Poppins-Medium.ttf", 42), (120, 120, 130)); rx = 382 - rt.width // 2; card.alpha_composite(rt, (rx, 282))
        ImageDraw.Draw(card).line((rx + 14, 282 + rt.height // 2, rx + rt.width - 14, 282 + rt.height // 2), fill=rgba((120, 120, 130)), width=5)
        put(img, card, W / 2, 1270, scale=kk, rot=-2)
    kc = back((t - 1.6) / .35)
    if kc > 0: put(img, TB("কোন খেলায় পরবেন? কমেন্টে লিখুন", 700, 60, MINT), W / 2, 1580, scale=kc)
    logo(img); return wipe(img, prev, t, NAVY2)


REELS = [
    dict(id="reel-colmi-p81-winter-morning-walk", time="18:30", music=("upbeat", 5), b=UB, cover=3600,
         scenes=[(p_hook, 5), (p_reveal, 8), (p_modes, 7), (p_check, 9), (p_price, 8),
                 (end_card([(WATCH, HQ), ("10.png", HQ), ("01.png", HQ)], NAVY, SUN, "Phone in pocket, calls on wrist."), 7)]),
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
