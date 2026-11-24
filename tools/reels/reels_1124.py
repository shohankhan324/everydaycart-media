"""Everyday Cart Reel for 24 Nov: "Tired after office? Relax at home": Portable Rechargeable Massage Gun (850 Tk).
Flat palette: deep teal evening + coral + butter, cream cards. Bangla hook in the first second ("অফিস শেষে ক্লান্ত?" over a
flat wall clock and a laptop lid closing), the gun drops onto a coral disc with flat pulse rings, "কাঁধ, পিঠ না পা?" chips,
spec checklist (only listing facts: 4 interchangeable heads, powerful yet quiet motor, lightweight ergonomic design,
rechargeable and portable), price card (850, regular 1,200) with a comment prompt, end card. Original drive synth track in key 2. About 21 s."""

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
R9.OUT = _R + "/out/out1124/"; os.makedirs(R9.OUT, exist_ok=True)
TEAL = (14, 72, 80); TEAL2 = (24, 96, 104); CORAL = (255, 112, 92); BUT = (255, 212, 104)
CREAM = (255, 244, 230); INK = (20, 22, 30)
GUN = "31.png"
B = DR.B


def clock(img, cx, cy, r, t):
    d = ImageDraw.Draw(img)
    d.ellipse((cx - r - 14, cy - r - 14, cx + r + 14, cy + r + 14), fill=rgba(BUT))
    d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=rgba(CREAM))
    for k in range(12):
        a = math.radians(k * 30); r0 = r * (.78 if k % 3 else .7)
        d.line((cx + r0 * math.sin(a), cy - r0 * math.cos(a), cx + r * .88 * math.sin(a), cy - r * .88 * math.cos(a)), fill=rgba(INK), width=8 if k % 3 == 0 else 4)
    hm = math.radians(180 + 360 * clamp(t / 2.4) * .5); hh = math.radians(210 + 15 * clamp(t / 2.4))   # 7:00 to 7:30
    d.line((cx, cy, cx + r * .7 * math.sin(hm), cy - r * .7 * math.cos(hm)), fill=rgba(INK), width=10)
    d.line((cx, cy, cx + r * .45 * math.sin(hh), cy - r * .45 * math.cos(hh)), fill=rgba(CORAL), width=14)
    d.ellipse((cx - 14, cy - 14, cx + 14, cy + 14), fill=rgba(INK))


def laptop(img, cx, base, w, lid):
    d = ImageDraw.Draw(img); h = w * .62 * lid
    d.rounded_rectangle((cx - w / 2 - 40, base, cx + w / 2 + 40, base + 36), radius=18, fill=rgba((200, 206, 214)))
    if h > 40:
        d.rounded_rectangle((cx - w / 2, base - h, cx + w / 2, base), radius=20, fill=rgba(INK))
        d.rounded_rectangle((cx - w / 2 + 22, base - h + 22, cx + w / 2 - 22, base - 10), radius=10, fill=rgba((90, 160, 230)))


def p_hook(t, b, prev):
    img = bg(TEAL); d = ImageDraw.Draw(img)
    d.rectangle((0, 1500, W, H), fill=rgba(TEAL2))   # desk
    clock(img, 250, 900, 150, t)
    laptop(img, 680, 1500, 560, 1 - ease((t - 1.2) / .6))
    k1 = (t - .05) / .22
    if k1 > 0: put(img, TB("অফিস শেষে ক্লান্ত?", 700, 110, WHITE), W / 2, 380, scale=1.4 - .4 * ease(k1), a=clamp(k1 * 2))
    k2 = (t - .9) / .25
    if k2 > 0: put(img, TB("ঘরেই নিন আরাম", 700, 120, BUT), W / 2, 580, scale=1.35 - .35 * back(k2), a=clamp(k2 * 2))
    kk = back((t - 1.7) / .3)
    if kk > 0: put(img, pill("AFTER OFFICE MODE", 52, CORAL, WHITE, padx=46), W / 2 + 120, 1700, scale=kk, rot=-3)
    logo(img); return img


def pulse(img, cx, cy, t, col, n=3, r0=330, gap=60):
    d = ImageDraw.Draw(img)
    for i in range(n):
        ph = (t * 1.2 + i / n) % 1; r = r0 + gap * n * ph; a = int(200 * (1 - ph))
        d.ellipse((cx - r, cy - r, cx + r, cy + r), outline=rgba(col, a), width=10)


def p_reveal(t, b, prev):
    img = bg(CORAL)
    pulse(img, W / 2, 960, t, CREAM)
    km = back(t / .45)
    if km > 0: disc(img, W / 2, 960, 380 * km, CREAM)
    drop = ease((t - .05) / .5); jit = 4 * math.sin(t * 70) if t > .6 else 0
    if drop > 0: put(img, P(GUN, 640, 560), W / 2 + jit, 980 - 700 * (1 - drop))
    kt = back((t - .6) / .35)
    if kt > 0: put(img, T("Portable Massage Gun", f("Poppins-Bold.ttf", 84), INK), W / 2, 270, scale=kt)
    ks = back((t - .9) / .35)
    if ks > 0: put(img, TB("রিচার্জেবল ম্যাসাজ গান", 700, 76, WHITE), W / 2, 390, scale=ks)
    kp = back((t - 1.4) / .35)
    if kp > 0: put(img, pill("4 interchangeable massage heads", 48, INK, BUT, padx=46), W / 2, 1480, scale=kp, rot=2)
    logo(img); return wipe(img, prev, t, CORAL)


def p_where(t, b, prev):
    img = bg(CREAM)
    put(img, TB("কাঁধ, পিঠ না পা?", 700, 120, TEAL), W / 2, 300, scale=back(t / .3))
    kd = back((t - .1) / .4)
    if kd > 0:
        disc(img, W / 2, 900, 330 * kd, BUT)
        put(img, P(GUN, 560, 480), W / 2 + 3 * math.sin(t * 60), 910, scale=kd)
    for i, (txt, col, x, y, rot) in enumerate((("Shoulders", CORAL, 300, 1360, -4), ("Back", TEAL, 760, 1420, 3), ("Legs", INK, 420, 1560, 2))):
        kk = back((t - .8 - .3 * i) / .3)
        if kk > 0: put(img, pill(txt, 58, col, WHITE, padx=52), x, y, scale=kk, rot=rot)
    kb = back((t - 1.9) / .35)
    if kb > 0: put(img, TB("যেখানে দরকার, সেখানেই", 700, 66, CORAL), W / 2, 1720, scale=kb)
    logo(img); return wipe(img, prev, t, CREAM)


CHECK = [("4 massage heads", CORAL), ("Powerful, quiet motor", BUT), ("Lightweight, ergonomic", (120, 200, 190)), ("Rechargeable, portable", (150, 170, 250))]


def p_check(t, b, prev):
    img = bg(TEAL)
    put(img, T("After office kit", f("Poppins-Bold.ttf", 86), WHITE), W / 2, 250, scale=back(t / .35))
    put(img, TB("অফিস হোক বা জিম", 700, 64, BUT), W / 2, 360, scale=back((t - .15) / .35))
    put(img, P(GUN, 460, 400), W / 2, 650 + 6 * math.sin(t * 3), scale=back((t - .2) / .4))
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
        put(img, card, W / 2, 1010 + i * 180, scale=kk, rot=(-1.5 if i % 2 == 0 else 1.5))
    logo(img); return wipe(img, prev, t, TEAL)


def p_price(t, b, prev):
    img = bg(TEAL2); d = ImageDraw.Draw(img)
    for i in range(7): d.ellipse((80 + i * 150 - 8, 1760 - 8, 80 + i * 150 + 8, 1760 + 8), fill=rgba(BUT))
    put(img, TB("দাম কত?", 700, 120, WHITE), W / 2, 230, scale=back(t / .3))
    kd = back(t / .4); disc(img, W / 2, 740, 310 * kd, BUT)
    put(img, P(GUN, 520, 440), W / 2, 750, scale=kd)
    kk = back((t - .7) / .4)
    if kk > 0:
        card = Image.new("RGBA", (780, 380), (0, 0, 0, 0)); cd = ImageDraw.Draw(card)
        cd.rounded_rectangle((16, 20, 779, 379), radius=56, fill=rgba(CORAL))
        cd.rounded_rectangle((0, 0, 763, 359), radius=56, fill=rgba(CREAM), outline=rgba(INK), width=8)
        lt = T("ONLY", f("Poppins-Bold.ttf", 44), CORAL); card.alpha_composite(lt, (382 - lt.width // 2, 30))
        pt = T("Tk 850", f("Poppins-Bold.ttf", 160), INK); card.alpha_composite(pt, (382 - pt.width // 2, 92))
        rt = T("Regular Tk 1,200", f("Poppins-Medium.ttf", 42), (120, 120, 130)); rx = 382 - rt.width // 2; card.alpha_composite(rt, (rx, 282))
        ImageDraw.Draw(card).line((rx + 14, 282 + rt.height // 2, rx + rt.width - 14, 282 + rt.height // 2), fill=rgba((120, 120, 130)), width=5)
        put(img, card, W / 2, 1270, scale=kk, rot=-2)
    kc = back((t - 1.6) / .35)
    if kc > 0: put(img, TB("কোথায় বেশি লাগবে? কমেন্টে লিখুন", 700, 62, BUT), W / 2, 1560, scale=kc)
    logo(img); return wipe(img, prev, t, TEAL2)


REELS = [
    dict(id="reel-massage-gun-after-office-relax", time="18:30", music=("drive", 2), b=B, cover=2000,
         scenes=[(p_hook, 5), (p_reveal, 8), (p_where, 7), (p_check, 9), (p_price, 8),
                 (end_card([(GUN, HQ), ("02.png", HQ), ("11.png", HQ)], TEAL, BUT, "Long day? Relax at home."), 7)]),
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
