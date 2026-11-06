"""Three Everyday Cart Reels for 6 Nov: speaker battle, cuddle buddies (Bangla), after-office POV (Bangla)."""
import os as _os
_R = _os.path.dirname(_os.path.abspath(__file__)); _T = _os.path.dirname(_R)

import os, sys, math
import numpy as np
from PIL import Image, ImageDraw
sys.path.insert(0, _T); sys.path.insert(0, _R)
from mega import T, TB, P, pill, bn_pill, bg, wipe, logo, rays, disc, confetti, put, rgba, f, ease, back, clamp, HQ, DARK, WHITE, YEL, _tc
import reels9 as R9
from reels9 import end_card, bn_num
import drive as DR

W, H = 1080, 1920
R9.OUT = _R + "/out/out1106/"; os.makedirs(R9.OUT, exist_ok=True)
TEAL = (0, 128, 140); TANG = (255, 120, 40); INKB = (16, 22, 34)
ROSE = (240, 120, 150); BLUSH = (255, 226, 234); PLUM = (52, 34, 78); LAV = (196, 176, 255); MOON = (255, 224, 150)

def tb_pill(text, size, fill, col):
    """Yellow-style pill for mixed Bangla/Latin text (the Bangla font has no '?')."""
    k = ("tbp", text, size, fill, col)
    if k not in _tc:
        tx = TB(text, 700, size, col); w, h = tx.width + 70, int(size * 1.9)
        s = Image.new("RGBA", (w, h), (0, 0, 0, 0)); ImageDraw.Draw(s).rounded_rectangle((0, 0, w - 1, h - 1), radius=h // 2, fill=rgba(fill))
        s.alpha_composite(tx, ((w - tx.width) // 2, (h - tx.height) // 2)); _tc[k] = s
    return _tc[k]

# ---------------------------------------------------------------- 1. Speaker battle: SpaceBox vs KA5
def s1_hook(t, b, prev):
    img = bg(INKB); rays(img, W / 2, 900, t, TANG, a=18)
    for i, (wd, col, sz) in enumerate([("SPEAKER", WHITE, 150), ("BATTLE", TANG, 210)]):
        kk = (t - i * b) / .2
        if kk > 0: put(img, T(wd, f("Poppins-Bold.ttf", sz), col, True), W / 2, 700 + i * 230, scale=1.5 - .5 * ease(kk), a=clamp(kk * 2))
    kk = back((t - 2 * b) / .35)
    if kk > 0: put(img, tb_pill("কোনটা নেবেন?", 64, YEL, DARK), W / 2, 1230, scale=kk)
    logo(img); return img
def s1_vs(t, b, prev):
    L, Rr = TEAL, TANG
    img = bg(L); ImageDraw.Draw(img).rectangle((W / 2, 0, W, H), fill=rgba(Rr))
    k = ease(t / .4)
    put(img, P("01.png", 440, 300), W / 4 - (1 - k) * 500, 640 + 8 * math.sin(t * 3))
    put(img, P("14.png", 300, 460), 3 * W / 4 + (1 - k) * 500, 640 + 8 * math.sin(t * 3 + 1))
    put(img, T("Oraimo SpaceBox", f("Poppins-Bold.ttf", 46), WHITE, True), W / 4, 920, a=k)
    put(img, T("Awei KA5", f("Poppins-Bold.ttf", 52), WHITE, True), 3 * W / 4, 920, a=k)
    put(img, T("WHICH ONE?", f("Poppins-Bold.ttf", 100), WHITE, True), W / 2, 240, scale=1.3 - .3 * ease(t / .3))
    vs = Image.new("RGBA", (180, 180), (0, 0, 0, 0)); ImageDraw.Draw(vs).ellipse((0, 0, 179, 179), fill=rgba(WHITE)); vs.alpha_composite(T("VS", f("Poppins-Bold.ttf", 72), INKB), (36, 28))
    put(img, vs, W / 2, 640, scale=back((t - .3) / .35), rot=8 * math.sin(t * 5))
    rows = [("Price", "Tk 1,841", "Tk 2,525"), ("Output", "8W", "10W x 2"), ("Battery", "1800mAh", "2400mAh"), ("Special", "Light Show", "IPX5")]
    for i, (lab, a_, b_) in enumerate(rows):
        kk = ease((t - (2 + i * 1.2) * b) / .3)
        if kk <= 0: continue
        y = 1040 + i * 112
        ov = Image.new("RGBA", (W, 96), (0, 0, 0, 0)); ImageDraw.Draw(ov).rounded_rectangle((60, 0, W - 60, 92), radius=46, fill=(255, 255, 255, int(240 * kk))); img.alpha_composite(ov, (0, y))
        put(img, T(a_, f("Poppins-Bold.ttf", 40), TEAL), 250, y + 46, a=kk); put(img, T(b_, f("Poppins-Bold.ttf", 40), (220, 90, 20)), W - 250, y + 46, a=kk)
        put(img, T(lab, f("Poppins-Medium.ttf", 30), (120, 120, 130)), W / 2, y + 46, a=kk)
    kk = back((t - 8 * b) / .35)
    if kk > 0: put(img, pill("Comment: SPACEBOX or KA5?", 44, INKB, WHITE), W / 2, 1620, scale=kk)
    logo(img); return wipe(img, prev, t, L)

# ---------------------------------------------------------------- 2. Cuddle buddies (Bangla)
def heart(img, cx, cy, s, col):
    d = ImageDraw.Draw(img); r = s * .5
    d.ellipse((cx - s, cy - r, cx, cy + r), fill=rgba(col)); d.ellipse((cx, cy - r, cx + s, cy + r), fill=rgba(col))
    d.polygon([(cx - s * .97, cy + r * .25), (cx + s * .97, cy + r * .25), (cx, cy + s * 1.25)], fill=rgba(col))
def hearts(img, t, col, n=10, seed=2):
    rng = np.random.default_rng(seed)
    for i in range(n):
        x = rng.uniform(60, W - 60); sp = rng.uniform(140, 260); s = rng.uniform(16, 34)
        y = H + 60 - ((t * sp + rng.uniform(0, H)) % (H + 160))
        heart(img, x + 20 * math.sin(t * 2 + i), y, s, col)
def s2_hook(t, b, prev):
    img = bg(BLUSH); hearts(img, t, (255, 196, 212))
    put(img, TB("ছোট্ট সোনার জন্য", 700, 110, (180, 60, 100)), W / 2, 760, a=clamp(t / .4), scale=1.1 - .1 * ease(t / .5))
    kk = ease((t - b) / .5)
    if kk > 0: put(img, T("Cuddle Buddies", f("Poppins-Bold.ttf", 110), (150, 50, 85)), W / 2, 930 + 30 * (1 - kk), a=kk)
    kk = ease((t - 2 * b) / .5)
    if kk > 0: put(img, TB("নরম, তুলতুলে বন্ধু", 600, 64, (170, 100, 120)), W / 2, 1060, a=kk)
    logo(img); return img
def s2_toy(im, name, size, price, regular, col, soft):
    def fn(t, b, prev):
        img = bg(col); hearts(img, t, soft, n=8, seed=len(name))
        disc(img, W / 2, 860, 400 + 10 * math.sin(t * 2), soft)
        put(img, P(im, 620, 640), W / 2, 860 + 12 * math.sin(t * 2.2), scale=.85 + .15 * ease(t / .6), a=clamp(t / .3), rot=3 * math.sin(t * 1.5))
        put(img, pill(size, 52, WHITE, col, padx=44), W / 2, 300, scale=back(t / .35))
        kk = ease((t - .3) / .5)
        put(img, T(name, f("Poppins-Bold.ttf", 76), WHITE, True), W / 2, 1360 + 30 * (1 - kk), a=kk)
        put(img, T(f"Tk {price:,}", f("Poppins-Bold.ttf", 120), WHITE, True), W / 2, 1500, scale=back((t - .5) / .35))
        kk = clamp((t - .9) / .3)
        if kk > 0:
            a1 = T("Regular", f("Poppins-Medium.ttf", 44), WHITE); a2 = T(f"Tk {regular:,}", f("Poppins-Medium.ttf", 44), WHITE)
            tot = a1.width + a2.width - 10; x0 = W / 2 - tot / 2
            put(img, a1, x0 + a1.width / 2, 1630, a=kk); x2 = x0 + a1.width - 10; put(img, a2, x2 + a2.width / 2, 1630, a=kk)
            ImageDraw.Draw(img).line((x2 + 10, 1630, x2 + a2.width - 10, 1630), fill=(255, 255, 255, int(255 * kk)), width=4)
        logo(img); return wipe(img, prev, t, col, W / 2, 860)
    return fn
def s2_ask(t, b, prev):
    img = bg((150, 50, 85)); hearts(img, t, (190, 90, 125), n=12, seed=9)
    put(img, P("06.png", 420, 440), W / 2 - 220, 900 + 10 * math.sin(t * 3), scale=back(t / .4))
    put(img, P("25.png", 420, 440), W / 2 + 220, 900 + 10 * math.sin(t * 3 + 1), scale=back((t - .15) / .4))
    put(img, TB("কোনটা পছন্দ?", 700, 120, WHITE, True), W / 2, 420, scale=1.3 - .3 * ease(t / .3))
    kk = back((t - .6) / .35)
    if kk > 0: put(img, pill("Comment: TEDDY or ELEPHANT", 46, WHITE, (150, 50, 85)), W / 2, 1380, scale=kk)
    logo(img); return wipe(img, prev, t, (150, 50, 85))

# ---------------------------------------------------------------- 3. POV after office (Bangla)
STARS = [(np.random.default_rng(i).uniform(0, W), np.random.default_rng(i + 99).uniform(0, 900), i) for i in range(50)]
def stars(img, t):
    d = ImageDraw.Draw(img)
    for x, y, i in STARS:
        a = int(140 + 110 * math.sin(t * 2 + i)); r = 2 + (i % 3); d.ellipse((x - r, y - r, x + r, y + r), fill=(255, 255, 255, max(0, a)))
def s3_pov(t, b, prev):
    img = bg(PLUM); stars(img, t)
    put(img, T("POV:", f("Poppins-Bold.ttf", 120), MOON), W / 2, 560, a=clamp(t / .2))
    for i, line in enumerate(["সারাদিন অফিসের পর...", "শরীর ক্লান্ত, মন চায় একটু আরাম"]):
        kk = ease((t - .4 - i * 1.5 * b) / .35)
        if kk > 0: put(img, TB(line, 700, 76 if i == 0 else 62, WHITE), W / 2, 760 + i * 130 + 30 * (1 - kk), a=kk)
    kk = back((t - 4 * b) / .35)
    if kk > 0: put(img, pill("3 picks for your evening", 46, LAV, PLUM), W / 2, 1200, scale=kk)
    logo(img); return img
def s3_step(n, bn, im, mw, mh, name, feats, price, col, acc):
    def fn(t, b, prev):
        img = bg(col); stars(img, t)
        put(img, T(f"{n}/3", f("Poppins-Bold.ttf", 44), acc), W / 2, 200, a=clamp(t / .3))
        put(img, TB(bn, 700, 96, WHITE, True), W / 2, 330, scale=1.2 - .2 * ease(t / .3), a=clamp(t / .2))
        disc(img, W / 2, 820, 360, tuple(min(255, c + 26) for c in col))
        put(img, P(im, mw, mh), W / 2, 820 + 10 * math.sin(t * 2.4), scale=back((t - .1) / .4))
        kk = ease((t - .3) / .35)
        put(img, T(name, f("Poppins-Bold.ttf", 68), WHITE, True), W / 2, 1270 + 30 * (1 - kk), a=kk)
        for i, ft in enumerate(feats):
            k2 = back((t - .6 - i * .25) / .3)
            if k2 > 0: put(img, pill(ft, 38, acc, col), W / 2, 1390 + i * 96, scale=k2)
        put(img, T(f"Tk {price:,}", f("Poppins-Bold.ttf", 112), MOON, True), W / 2, 1700, scale=back((t - 1.3) / .35))
        logo(img); return wipe(img, prev, t, col, W / 2, 820)
    return fn

G = 60 / 92; U_ = 60 / 116
REELS = [
    dict(id="speaker-battle", time="13:00", music=("drive", 4), b=DR.B, scenes=[(s1_hook, 5), (s1_vs, 17), (end_card([("01.png", HQ), ("14.png", HQ), ("12.png", HQ)], INKB, TANG, "Turn the volume up"), 7)], cover=9000,
         caption="🔊 Speaker battle! Which one would you take home?\n\nOraimo SpaceBox Portable Bluetooth Speaker: 1,841৳ (regular 2,299৳)\n✔️ 8W audio output, 45mm driver\n✔️ 1800mAh battery\n✔️ Personalized light show, thumping bass\n\nAwei KA5 20W Portable Bluetooth Speaker: 2,525৳ (regular 2,849৳)\n✔️ 10W x 2 output\n✔️ 2400mAh battery, 7.5 to 8 hours playback (at 70% volume)\n✔️ IPX5 waterproof, Bluetooth 5.3\n\n💬 Comment SPACEBOX or KA5 👇",
         tags="#EverydayCart #SpeakerBattle #Oraimo #SpaceBox #Awei #BluetoothSpeaker #ThisOrThat #TechBD"),
    dict(id="cuddle-buddies", time="16:00", music=("gentle", 2), b=G, scenes=[(s2_hook, 5), (s2_toy("06.png", "22\" Big Teddy Bear", "22 INCH", 1150, 2000, ROSE, (255, 170, 192)), 6),
         (s2_toy("25.png", "Elephant Plush Toy", "18 INCH", 750, 1100, (120, 150, 210), (160, 186, 236)), 6), (s2_ask, 5),
         (end_card([("06.png", HQ), ("25.png", HQ)], (150, 50, 85), BLUSH, "Soft hugs, every day"), 5)], cover=2600,
         caption="🧸 ছোট্ট সোনার জন্য নরম, তুলতুলে বন্ধু! Meet our cuddle buddies 💕\n\n🧸 22\" Big Teddy Bear: 1,150৳ (regular 2,000৳)\n✔️ Super soft premium plush\n✔️ Perfect for cuddling, decorating and gifting\n\n🐘 Elephant Plush Soft Toy: 750৳ (regular 1,100৳)\n✔️ 18 inch soft plush\n\n💬 Teddy or Elephant? Comment below 👇",
         tags="#EverydayCart #TeddyBear #SoftToys #PlushToy #GiftIdeas #KidsGift #GiftsBD"),
    dict(id="after-office-pov", time="21:30", music=("gentle", 7), b=G, scenes=[(s3_pov, 7),
         (s3_step(1, "ক্লান্ত শরীর?", "31.png", 600, 520, "Portable Massage Gun", ["4 Massage Heads", "Powerful, Quiet Motor"], 850, (78, 52, 112), LAV), 6),
         (s3_step(2, "একটু গান শুনুন", "12.png", 560, 520, "Oraimo SpaceBuds Neo+", ["Sound360 Spatial Audio", "Up to 30 Hrs Battery"], 1940, (40, 58, 110), (180, 210, 255)), 6),
         (s3_step(3, "শান্তির ঘুম", "07.png", 520, 540, "Silent Alarm Clock", ["Non-ticking, Silent", "Precise Quartz Movement"], 500, (24, 30, 70), MOON), 6),
         (end_card([("31.png", HQ), ("12.png", HQ), ("07.png", HQ)], PLUM, MOON, "Relax, you earned it"), 5)], cover=7000,
         caption="🌙 POV: সারাদিন অফিসের পর... শরীর ক্লান্ত, মন চায় একটু আরাম 😌\n\n3 picks for your evening:\n\n💆 Portable Massage Gun: 850৳ (regular 1,200৳)\n✔️ 4 interchangeable massage heads\n✔️ Powerful yet quiet motor, lightweight design\n\n🎧 Oraimo SpaceBuds Neo+: 1,940৳ (regular 2,189৳)\n✔️ Sound360 spatial audio\n✔️ Up to 30 hours battery\n\n⏰ Silent Alarm Clock: 500৳ (regular 800৳)\n✔️ Non-ticking, precise quartz movement\n\nশুভ রাত্রি 💤",
         tags="#EverydayCart #MassageGun #Oraimo #SpaceBuds #SilentClock #SelfCare #BanglaPOV"),
]

if __name__ == "__main__":
    mode = sys.argv[1]; ids = sys.argv[2:]
    R9.REELS = REELS
    sel = [r for r in REELS if not ids or r["id"] in ids]
    if mode == "preview":
        shots = []
        for r in sel:
            parts, starts, total = R9.build(r, True); print(r["id"], round(total, 1))
            for (fn, dur), st in zip(parts, starts):
                for fr in (.3, .8): shots.append(fn(min(dur * fr, dur - .1)).convert("RGB"))
        cols = 8; rows = math.ceil(len(shots) / cols); sheet = Image.new("RGB", (cols * 270, rows * 480), "white")
        for i, s_ in enumerate(shots): sheet.paste(s_.resize((270, 480), Image.LANCZOS), ((i % cols) * 270, (i // cols) * 480))
        sheet.save(sys.argv[0].rsplit("/", 1)[0] + "/out/r1106_sheet.jpg" if "/" in sys.argv[0] else "out/r1106_sheet.jpg", quality=86)
    else:
        for r in sel: R9.build(r)
