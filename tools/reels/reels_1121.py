"""Everyday Cart Reel for 21 Nov: "Lights off, music on": Oraimo SpaceBox portable Bluetooth speaker.
Deep violet room + neon magenta / cyan / lime flat palette. Bangla hook in the first second (a flat light switch flips
off, "লাইট অফ" then "মিউজিক অন!" with bouncing equaliser bars), the SpaceBox drops in with flat rainbow rings pulsing
on the beat (its personalised light show), four spec cards, Bangla use-case chips (adda, picnic, room party),
price card, comment prompt, end card. All facts from the store listing. Original drive synth track in key 6. About 23 s."""

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
R9.OUT = _R + "/out/out1121/"; os.makedirs(R9.OUT, exist_ok=True)
ROOM = (30, 18, 62); ROOM2 = (48, 30, 92); MAG = (255, 72, 170); CYAN = (60, 220, 255); LIME = (196, 255, 84)
SUN = (255, 196, 48); INK = (22, 14, 44)
SPK = "01.png"   # Oraimo SpaceBox
B = DR.B
NEON = [MAG, SUN, LIME, CYAN, (150, 110, 255)]


def beat(t, b=B):
    """0..1 pulse that peaks on every beat."""
    ph = (t / b) % 1.0
    return math.exp(-ph * 5)


def eq_bars(img, cx, y, t, n=9, w=46, gap=18, hmax=260, cols=NEON):
    d = ImageDraw.Draw(img); x0 = cx - (n * w + (n - 1) * gap) / 2
    for i in range(n):
        h = 40 + hmax * (0.35 + 0.65 * abs(math.sin(t * 5.3 + i * 1.3))) * (0.6 + 0.4 * beat(t + i * .03))
        x = x0 + i * (w + gap)
        d.rounded_rectangle((x, y - h, x + w, y), radius=14, fill=rgba(cols[i % len(cols)]))


def rings(img, cx, cy, t, r0=300, n=5, width=22):
    """Flat concentric rings cycling through neon colours, pulsing with the beat."""
    d = ImageDraw.Draw(img); p = beat(t)
    for i in range(n, 0, -1):
        r = r0 + i * 62 + 22 * p
        col = NEON[(i + int(t / B)) % len(NEON)]
        d.ellipse((cx - r, cy - r, cx + r, cy + r), outline=rgba(col), width=width)


def switch(img, cx, cy, on, s=1.0):
    d = ImageDraw.Draw(img)
    d.rounded_rectangle((cx - 90 * s, cy - 140 * s, cx + 90 * s, cy + 140 * s), radius=36 * s, fill=rgba(WHITE))
    d.rounded_rectangle((cx - 50 * s, cy - 100 * s, cx + 50 * s, cy + 100 * s), radius=22 * s, fill=rgba((220, 216, 236)))
    ty = cy - 50 * s if on else cy + 50 * s
    d.rounded_rectangle((cx - 44 * s, ty - 46 * s, cx + 44 * s, ty + 46 * s), radius=18 * s, fill=rgba(INK if not on else SUN))


def p_hook(t, b, prev):
    dark = t > .55
    img = bg(ROOM if dark else (255, 236, 170))
    switch(img, 170, 420, on=not dark, s=.8)
    put(img, TB("লাইট অফ", 700, 150, WHITE if dark else INK, dark), W / 2 + 110, 420, scale=1.3 - .3 * ease(t / .2), a=clamp(t / .08))
    k = (t - .9) / .25
    if k > 0:
        put(img, TB("মিউজিক অন!", 700, 150, LIME, True), W / 2, 740, scale=1.35 - .35 * back(k), a=clamp(k * 2))
        eq_bars(img, W / 2, 1380, t, hmax=380)
    kk = back((t - 1.6) / .3)
    if kk > 0: put(img, pill("LIGHT SHOW SPEAKER", 54, MAG, WHITE, padx=46), W / 2, 1560, scale=kk, rot=-3)
    logo(img); return img


def p_reveal(t, b, prev):
    img = bg(ROOM); d = ImageDraw.Draw(img)
    k = back((t - .1) / .45)
    if k > 0: rings(img, W / 2, 1000, t, r0=240 * k)
    disc(img, W / 2, 1000, 250 * k, ROOM2)
    drop = ease((t - .05) / .5)
    if drop > 0: put(img, P(SPK, 640, 380), W / 2, 1000 - 600 * (1 - drop) + 8 * math.sin(t * 4), scale=1 + .04 * beat(t))
    kt = back((t - .8) / .35)
    if kt > 0: put(img, T("Oraimo SpaceBox", f("Poppins-Bold.ttf", 86), WHITE), W / 2, 250, scale=kt)
    ks = back((t - 1.1) / .35)
    if ks > 0: put(img, TB("আলো জ্বলে গানের তালে", 700, 84, SUN), W / 2, 370, scale=ks)
    kp = back((t - 1.6) / .35)
    if kp > 0: put(img, pill("Personalized light show", 52, LIME, INK, padx=46), W / 2, 1680, scale=kp, rot=2)
    logo(img); return wipe(img, prev, t, ROOM)


SPECS = [("8W", "audio output", MAG), ("45mm", "driver", CYAN), ("1800", "mAh battery", SUN), ("BASS", "thumping bass", LIME)]


def p_specs(t, b, prev):
    img = bg((246, 240, 255)); d = ImageDraw.Draw(img)
    put(img, T("Small box. Big sound.", f("Poppins-Bold.ttf", 80), INK), W / 2, 280, scale=back(t / .35))
    put(img, P(SPK, 700, 380), W / 2, 600 + 8 * math.sin(t * 3), scale=back((t - .15) / .4) * (1 + .03 * beat(t)))
    for i, (big_, small_, col) in enumerate(SPECS):
        st = .7 + .45 * i; kk = back((t - st) / .35)
        if kk <= 0: continue
        cx = 290 + (i % 2) * 500; cy = 1080 + (i // 2) * 440
        card = Image.new("RGBA", (440, 380), (0, 0, 0, 0)); cd = ImageDraw.Draw(card)
        cd.rounded_rectangle((14, 18, 439, 379), radius=48, fill=rgba(INK))
        cd.rounded_rectangle((0, 0, 425, 361), radius=48, fill=rgba(col), outline=rgba(INK), width=7)
        bt = T(big_, f("Poppins-Bold.ttf", 118 if len(big_) <= 4 else 96), INK); card.alpha_composite(bt, (212 - bt.width // 2, 70))
        stx = T(small_, f("Poppins-Bold.ttf", 44), INK); card.alpha_composite(stx, (212 - stx.width // 2, 240))
        put(img, card, cx, cy, scale=kk, rot=(-3 if i % 2 == 0 else 3))
    logo(img); return wipe(img, prev, t, (246, 240, 255))


def p_where(t, b, prev):
    img = bg(MAG)
    put(img, TB("কোথায় বাজাবেন?", 700, 120, WHITE, True), W / 2, 300, scale=back(t / .35))
    put(img, P(SPK, 700, 380), W / 2, 720 + 10 * math.sin(t * 4), scale=back((t - .1) / .4) * (1 + .04 * beat(t)))
    chips = [("বন্ধুদের আড্ডায়", SUN, INK, -4, 1160), ("পিকনিকে", LIME, INK, 3, 1390), ("রুমে পার্টিতে", CYAN, INK, -2, 1620)]
    for i, (txt, fill, col, rot, y) in enumerate(chips):
        kk = back((t - .7 - .45 * i) / .35)
        if kk <= 0: continue
        s = TB(txt, 700, 96, col); cw, ch = s.width + 100, s.height + 40
        c = Image.new("RGBA", (cw + 12, ch + 14), (0, 0, 0, 0)); cd = ImageDraw.Draw(c)
        cd.rounded_rectangle((12, 14, cw + 11, ch + 13), radius=ch // 2, fill=rgba(INK))
        cd.rounded_rectangle((0, 0, cw, ch), radius=ch // 2, fill=rgba(fill), outline=rgba(INK), width=6)
        c.alpha_composite(s, (50, 20)); put(img, c, W / 2 + (i - 1) * 60, y, scale=kk, rot=rot)
    logo(img); return wipe(img, prev, t, MAG)


def p_price(t, b, prev):
    img = bg(ROOM); rings(img, W / 2, 830, t, r0=200, n=4, width=16)
    disc(img, W / 2, 830, 210, ROOM2)
    put(img, P(SPK, 480, 280), W / 2, 830, scale=back(t / .4) * (1 + .04 * beat(t)))
    put(img, TB("দাম কত?", 700, 120, WHITE, True), W / 2, 220, scale=back(t / .3))
    kk = back((t - .7) / .4)
    if kk > 0:
        card = Image.new("RGBA", (760, 400), (0, 0, 0, 0)); cd = ImageDraw.Draw(card)
        cd.rounded_rectangle((16, 20, 759, 399), radius=56, fill=rgba(MAG))
        cd.rounded_rectangle((0, 0, 743, 379), radius=56, fill=rgba(LIME), outline=rgba(INK), width=8)
        lt = T("ONLY", f("Poppins-Bold.ttf", 48), INK); card.alpha_composite(lt, (372 - lt.width // 2, 34))
        pt = T("Tk 1,841", f("Poppins-Bold.ttf", 150), INK); card.alpha_composite(pt, (372 - pt.width // 2, 96))
        rt = "Regular Tk 2,299"; rfo = f("Poppins-Medium.ttf", 44); rw = rfo.getlength(rt)
        cd.text((372 - rw / 2, 290), rt, font=rfo, fill=rgba(INK)); cd.line((372 - rw / 2 - 6, 318, 372 + rw / 2 + 6, 318), fill=rgba(INK), width=5)
        put(img, card, W / 2, 1490, scale=kk, rot=-2)
    kc = back((t - 1.6) / .35)
    if kc > 0: put(img, TB("প্রথম গানটা কী হবে? কমেন্টে লিখুন", 700, 64, SUN), W / 2, 1790, scale=kc)
    logo(img); return wipe(img, prev, t, ROOM)


REELS = [
    dict(id="reel-oraimo-spacebox-lights-off-music-on", time="18:30", music=("drive", 6), b=B, cover=2000,
         scenes=[(p_hook, 5), (p_reveal, 8), (p_specs, 9), (p_where, 7), (p_price, 8),
                 (end_card([(SPK, HQ), ("13.png", HQ), ("09.png", HQ)], ROOM2, LIME, "Lights off. Music on."), 7)]),
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
