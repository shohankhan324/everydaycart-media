"""Everyday Cart Reel for 23 Nov: "Stuck in Dhaka traffic? Calls stay clear": Proove Intro Pro (APP) Black TWS.
Traffic light flat palette: asphalt charcoal + signal yellow + stop red + go green, cream cards. Bangla hook in the first
second ("জ্যামে আটকে আছেন?" over a flat traffic light with the red lamp on and a row of flat cars), then the light turns
green and the earbuds drop in, LED display case callout ("চার্জ কত? কেসেই দেখুন"), spec checklist (only listing facts:
13mm driver, Transparent ENC for clear calls, Bluetooth 5.4 touch control, up to 6 hours playback), price card with a
comment prompt, end card. Original drive synth track in key 5. About 21 s."""

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
R9.OUT = _R + "/out/out1123/"; os.makedirs(R9.OUT, exist_ok=True)
ASPH = (30, 34, 42); ASPH2 = (46, 52, 64); YEL = (255, 206, 30); RED = (240, 62, 58); GO = (60, 210, 120)
CREAM = (255, 246, 228); INK = (20, 20, 28); LANE = (250, 250, 240)
BUDS = "03.png"
B = DR.B


def road(img, t, base=1500, speed=0.0):
    d = ImageDraw.Draw(img)
    d.rectangle((0, base, W, H), fill=rgba(ASPH2))
    off = (t * speed * 400) % 260
    for x in range(-260, W + 260, 260):
        d.rounded_rectangle((x - off, base + 170, x - off + 140, base + 190), radius=10, fill=rgba(LANE))


def car(img, cx, by, w, col, t=0, ph=0):
    d = ImageDraw.Draw(img); h = w * .42; bob = 2 * math.sin(t * 8 + ph)
    y = by - h + bob
    d.rounded_rectangle((cx - w / 2, y + h * .35, cx + w / 2, y + h), radius=int(h * .22), fill=rgba(col))
    d.rounded_rectangle((cx - w * .3, y, cx + w * .26, y + h * .5), radius=int(h * .2), fill=rgba(col))
    d.rounded_rectangle((cx - w * .24, y + h * .08, cx - w * .02, y + h * .38), radius=8, fill=rgba(CREAM))
    d.rounded_rectangle((cx + w * .02, y + h * .08, cx + w * .2, y + h * .38), radius=8, fill=rgba(CREAM))
    for wx in (cx - w * .3, cx + w * .3):
        r = h * .2; d.ellipse((wx - r, by - r * 1.1, wx + r, by + r * .9), fill=rgba(INK))
        d.ellipse((wx - r * .45, by - r * .65, wx + r * .45, by + r * .45), fill=rgba((150, 150, 160)))
    d.ellipse((cx + w / 2 - 26, y + h * .5, cx + w / 2 - 6, y + h * .5 + 20), fill=rgba(YEL))


def light(img, cx, top, state, s=1.0):
    d = ImageDraw.Draw(img); w, h = 170 * s, 440 * s
    d.rectangle((cx - 12 * s, top + h, cx + 12 * s, top + h + 380 * s), fill=rgba(INK))
    d.rounded_rectangle((cx - w / 2, top, cx + w / 2, top + h), radius=int(40 * s), fill=rgba(INK))
    for i, col in enumerate((RED, YEL, GO)):
        cy = top + 80 * s + i * 140 * s; r = 56 * s
        on = (state == i)
        d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=rgba(col if on else (60, 62, 72)))
        if on: d.ellipse((cx - r * .45, cy - r * .6, cx - r * .05, cy - r * .2), fill=rgba(WHITE))


def p_hook(t, b, prev):
    img = bg(ASPH); road(img, t, base=1480)
    light(img, 160, 800, 0 if t < 2.0 else 2, s=.75)
    for i, (x, col) in enumerate(((180, RED), (520, YEL), (880, (90, 150, 240)))):
        car(img, x, 1600, 300, col, t, i)
    k1 = (t - .05) / .22
    if k1 > 0: put(img, TB("জ্যামে আটকে আছেন?", 700, 104, WHITE, True), W / 2, 430, scale=1.4 - .4 * ease(k1), a=clamp(k1 * 2))
    k2 = (t - .95) / .25
    if k2 > 0: put(img, TB("কল হোক পরিষ্কার", 700, 120, YEL, True), W / 2, 640, scale=1.35 - .35 * back(k2), a=clamp(k2 * 2))
    kk = back((t - 1.6) / .3)
    if kk > 0: put(img, pill("DHAKA TRAFFIC MODE", 52, RED, WHITE, padx=46), W / 2 + 80, 1000, scale=kk, rot=-3)
    logo(img); return img


def p_reveal(t, b, prev):
    img = bg(YEL); d = ImageDraw.Draw(img)
    for i in range(-2, 12):   # flat zebra crossing stripes at the bottom
        x = i * 150 - (t * 60) % 150; d.rectangle((x, 1560, x + 80, H), fill=rgba(CREAM))
    km = back(t / .45)
    if km > 0: disc(img, W / 2, 960, 400 * km, INK)
    drop = ease((t - .05) / .5)
    if drop > 0: put(img, P(BUDS, 640, 700), W / 2, 980 - 700 * (1 - drop) + 6 * math.sin(t * 4))
    kt = back((t - .6) / .35)
    if kt > 0: put(img, T("Proove Intro Pro", f("Poppins-Bold.ttf", 100), INK), W / 2, 260, scale=kt)
    ks = back((t - .9) / .35)
    if ks > 0: put(img, TB("ENC সহ ওয়্যারলেস ইয়ারবাড", 700, 70, INK), W / 2, 380, scale=ks)
    kp = back((t - 1.4) / .35)
    if kp > 0: put(img, pill("Transparent ENC for clear calls", 50, INK, YEL, padx=46), W / 2, 1480, scale=kp, rot=2)
    logo(img); return wipe(img, prev, t, YEL)


def p_case(t, b, prev):
    img = bg(ASPH); d = ImageDraw.Draw(img)
    put(img, TB("চার্জ কত?", 700, 130, WHITE, True), W / 2, 260, scale=back(t / .3))
    kd = back((t - .1) / .4)
    if kd > 0:
        disc(img, W / 2, 920, 380 * kd, CREAM)
        put(img, P(BUDS, 620, 680), W / 2, 930 + 5 * math.sin(t * 3), scale=kd)
    ka = ease((t - .9) / .35)
    if ka > 0:   # flat callout line to the LED display on the case
        d = ImageDraw.Draw(img); x0, y0 = 600, 1120; x1, y1 = 600 + 220 * ka, 1120 + 300 * ka
        d.line((x0, y0, x1, y1), fill=rgba(YEL), width=10)
        d.ellipse((x0 - 18, y0 - 18, x0 + 18, y0 + 18), fill=rgba(YEL))
    kp = back((t - 1.2) / .35)
    if kp > 0: put(img, pill("LED display charging case", 52, YEL, INK, padx=46), W / 2 + 60, 1480, scale=kp, rot=-2)
    kb = back((t - 1.7) / .35)
    if kb > 0: put(img, TB("কেসের ডিসপ্লেতেই দেখুন", 700, 78, GO), W / 2, 1650, scale=kb)
    logo(img); return wipe(img, prev, t, ASPH)


CHECK = [("Powerful 13mm driver", RED), ("Transparent ENC calls", YEL), ("Bluetooth 5.4, touch", GO), ("Up to 6 hours playback", (110, 170, 250))]


def p_check(t, b, prev):
    img = bg(CREAM)
    put(img, T("Commute checklist", f("Poppins-Bold.ttf", 86), INK), W / 2, 250, scale=back(t / .35))
    put(img, TB("জ্যাম হোক বা লম্বা রাস্তা", 700, 64, RED), W / 2, 360, scale=back((t - .15) / .35))
    put(img, P(BUDS, 460, 470), W / 2, 680 + 6 * math.sin(t * 3), scale=back((t - .2) / .4))
    for i, (txt, col) in enumerate(CHECK):
        st = .7 + .5 * i; kk = back((t - st) / .32)
        if kk <= 0: continue
        card = Image.new("RGBA", (900, 150), (0, 0, 0, 0)); cd = ImageDraw.Draw(card)
        cd.rounded_rectangle((10, 12, 899, 149), radius=34, fill=rgba(INK))
        cd.rounded_rectangle((0, 0, 889, 137), radius=34, fill=rgba(WHITE), outline=rgba(INK), width=6)
        cd.ellipse((30, 26, 116, 112), fill=rgba(col), outline=rgba(INK), width=5)
        tick = clamp((t - st - .2) / .2)
        if tick > 0:
            pts = [(50, 70), (68, 90), (98, 50)]
            if tick < .5: pts = pts[:2]
            cd.line(pts, fill=rgba(INK), width=11, joint="curve")
        tt = T(txt, f("Poppins-Bold.ttf", 54), INK); card.alpha_composite(tt, (140, 69 - tt.height // 2))
        put(img, card, W / 2, 1030 + i * 180, scale=kk, rot=(-1.5 if i % 2 == 0 else 1.5))
    logo(img); return wipe(img, prev, t, CREAM)


def p_price(t, b, prev):
    img = bg(ASPH); road(img, t, base=1620, speed=1.0)
    light(img, 150, 140, 2, s=.55)
    put(img, TB("দাম কত?", 700, 120, WHITE, True), W / 2 + 60, 230, scale=back(t / .3))
    kd = back(t / .4); disc(img, W / 2, 740, 310 * kd, YEL)
    put(img, P(BUDS, 500, 540), W / 2, 750, scale=kd)
    kk = back((t - .7) / .4)
    if kk > 0:
        card = Image.new("RGBA", (780, 360), (0, 0, 0, 0)); cd = ImageDraw.Draw(card)
        cd.rounded_rectangle((16, 20, 779, 359), radius=56, fill=rgba(RED))
        cd.rounded_rectangle((0, 0, 763, 339), radius=56, fill=rgba(CREAM), outline=rgba(INK), width=8)
        lt = T("OFFICIAL  |  ONLY", f("Poppins-Bold.ttf", 44), RED); card.alpha_composite(lt, (382 - lt.width // 2, 38))
        pt = T("Tk 2,300", f("Poppins-Bold.ttf", 160), INK); card.alpha_composite(pt, (382 - pt.width // 2, 110))
        put(img, card, W / 2, 1270, scale=kk, rot=-2)
    kc = back((t - 1.6) / .35)
    if kc > 0: put(img, TB("জ্যামে গান না পডকাস্ট? কমেন্টে লিখুন", 700, 64, YEL), W / 2, 1540, scale=kc)
    logo(img); return wipe(img, prev, t, ASPH)


REELS = [
    dict(id="reel-proove-intro-pro-traffic-clear-calls", time="18:30", music=("drive", 5), b=B, cover=2100,
         scenes=[(p_hook, 5), (p_reveal, 8), (p_case, 7), (p_check, 9), (p_price, 8),
                 (end_card([(BUDS, HQ), ("12.png", HQ), ("13.png", HQ)], ASPH2, YEL, "Jam outside, clear calls inside."), 7)]),
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
