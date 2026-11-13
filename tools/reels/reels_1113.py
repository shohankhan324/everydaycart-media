"""Everyday Cart Reel for 13 Nov: COLMI P81 "phone in the bag" (Bangla POV hook: phone is in the bag and a call
comes in, ringing waves, answer on your wrist, sliding spec cards, price reveal, end card).
Berry + sunshine yellow palette, original drive track in a new key."""
import os as _os
_R = _os.path.dirname(_os.path.abspath(__file__)); _T = _os.path.dirname(_R)

import os, sys, math
from PIL import Image, ImageDraw
sys.path.insert(0, _T); sys.path.insert(0, _R)
from mega import T, TB, P, pill, bg, wipe, logo, rays, disc, put, rgba, f, ease, back, clamp, confetti, HQ, DARK, WHITE
import reels9 as R9
from reels9 import end_card
import drive as DR

W, H = 1080, 1920
R9.OUT = _R + "/out/out1113/"; os.makedirs(R9.OUT, exist_ok=True)
BERRY = (122, 28, 72); BERRY2 = (150, 46, 94); SUN = (255, 208, 72); CRM = (255, 247, 236); GRN = (64, 200, 120)
PROD = "09.png"


_HS = {}
def handset(img, cx, cy, s, col, ang=0):
    """Flat phone-handset icon (Material 'call' glyph, Apache 2.0) rendered with cairosvg."""
    if col not in _HS:
        import cairosvg, io
        svg = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="200" height="200"><path fill="rgb%s" '
               'd="M6.62 10.79c1.44 2.83 3.76 5.14 6.59 6.59l2.2-2.2c.27-.27.67-.36 1.02-.24 1.12.37 2.33.57 3.57.57.55 0 1 .45 1 1V20'
               'c0 .55-.45 1-1 1-9.39 0-17-7.61-17-17 0-.55.45-1 1-1h3.5c.55 0 1 .45 1 1 0 1.25.2 2.45.57 3.57.11.35.03.74-.25 1.02l-2.2 2.2z"/></svg>') % (tuple(col),)
        _HS[col] = Image.open(io.BytesIO(cairosvg.svg2png(bytestring=svg.encode()))).convert("RGBA")
    L = _HS[col].rotate(ang, resample=Image.BICUBIC)
    put(img, L, cx, cy, scale=s * 0.62)


def waves(img, cx, cy, t, col, r0=300, grow=260):
    d = ImageDraw.Draw(img)
    for k in range(3):
        ph = (t * 1.2 + k / 3) % 1; r = r0 + ph * grow; a = int(150 * (1 - ph))
        d.ellipse((cx - r, cy - r, cx + r, cy + r), outline=rgba(col, a), width=10)


def bag(img, cx, cy, t):
    shake = 10 * math.sin(t * 60) if (t % .8) < .45 else 0
    L = Image.new("RGBA", (560, 520), (0, 0, 0, 0)); d = ImageDraw.Draw(L)
    d.arc((150, 0, 410, 220), 180, 360, fill=rgba(SUN), width=34)
    d.rounded_rectangle((20, 110, 540, 500), radius=60, fill=rgba(SUN))
    d.rounded_rectangle((20, 110, 540, 190), radius=30, fill=rgba((235, 178, 40)))
    d.rounded_rectangle((240, 170, 320, 230), radius=16, fill=rgba(BERRY))
    put(img, L, cx + shake, cy)


def p_hook(t, b, prev):
    img = bg(BERRY)
    put(img, TB("ফোন ব্যাগের ভেতরে", 700, 100, WHITE, True), W / 2, 430, scale=1.3 - .3 * ease(t / .25), a=clamp(t / .12))
    kk = (t - 1.6 * b) / .3
    if kk > 0: put(img, TB("আর তখনই কল আসলো?", 700, 92, SUN, True), W / 2, 590, scale=1.25 - .25 * ease(kk), a=clamp(kk * 2))
    kk = back((t - 1.0 * b) / .35)
    if kk > 0:
        waves(img, W / 2, 1180, t, SUN, r0=250)
        L = Image.new("RGBA", (W, H), (0, 0, 0, 0)); bag(L, W / 2, 1200, t)
        put(img, L, W / 2, H / 2 + 0, scale=1, a=clamp(kk))
        kq = back((t - 3 * b) / .3)
        if kq > 0:
            disc(img, W / 2 + 290, 960, 95 * kq, GRN); handset(img, W / 2 + 290, 960, .62 * kq, WHITE, 8 * math.sin(t * 30))
    logo(img); return img


def p_wrist(t, b, prev):
    img = bg(CRM)
    waves(img, W / 2, 1000, t, BERRY2, r0=330, grow=150)
    disc(img, W / 2, 1000, 330, (255, 226, 150))
    k = back(t / .45)
    put(img, P(PROD, 600, 600), W / 2, 1000 - 700 * (1 - min(1, k)) + 8 * math.sin(t * 3), a=clamp(t / .15))
    kk = back((t - 1.2 * b) / .35)
    if kk > 0:
        disc(img, W / 2 + 330, 760, 90 * kk, GRN); handset(img, W / 2 + 330, 760, .58 * kk, WHITE, 6 * math.sin(t * 25))
    kk = ease((t - .5) / .4)
    put(img, T("Take the call", f("Poppins-Bold.ttf", 92), BERRY), W / 2, 300 + 30 * (1 - kk), a=kk)
    put(img, T("right on your wrist", f("Poppins-Bold.ttf", 76), (40, 40, 48)), W / 2, 410 + 30 * (1 - kk), a=kk)
    kk = ease((t - 2.5 * b) / .3)
    if kk > 0: put(img, TB("কব্জিতেই কথা বলুন", 700, 78, BERRY), W / 2, 1600, a=kk)
    kk = back((t - 4 * b) / .35)
    if kk > 0: put(img, pill("COLMI P81 Calling Smartwatch", 46, BERRY, WHITE, padx=44), W / 2, 1740, scale=kk)
    logo(img); return wipe(img, prev, t, CRM, W / 2, 1000)


CARDS = [('1.9"', "HD Display", "বড় এইচডি ডিসপ্লে"), ("CALL", "Bluetooth Calling", "ব্লুটুথ কলিং"),
         ("IP68", "Waterproof", "পানি প্রতিরোধী"), ("100+", "Sports Modes", "স্পোর্টস মোড")]
def p_cards(t, b, prev):
    img = bg(BERRY); rays(img, W / 2, 420, t, BERRY2, a=90)
    put(img, TB("স্মার্ট ওয়াচে যা পাচ্ছেন", 700, 74, SUN), W / 2, 200, a=clamp(t / .2))
    disc(img, W / 2, 500, 210, BERRY2)
    put(img, P(PROD, 360, 360), W / 2, 500 + 8 * math.sin(t * 3))
    for i, (big, en, bn) in enumerate(CARDS):
        st = (1.0 + i * 2.4) * b; kk = ease((t - st) / .35)
        if kk <= 0: continue
        cy = 870 + i * 250; x = W / 2 + (1 - kk) * (W if i % 2 == 0 else -W)
        card = Image.new("RGBA", (900, 210), (0, 0, 0, 0)); d = ImageDraw.Draw(card)
        dark = i % 2 == 1
        d.rounded_rectangle((0, 0, 899, 209), radius=40, fill=rgba(SUN if dark else WHITE))
        d.rounded_rectangle((24, 24, 254, 185), radius=30, fill=rgba(BERRY))
        tv = T(big, f("Poppins-Bold.ttf", 76 if len(big) <= 4 else 64), SUN); card.alpha_composite(tv, (int(139 - tv.width / 2), int(105 - tv.height / 2)))
        te = T(en, f("Poppins-Bold.ttf", 52), (40, 30, 40)); card.alpha_composite(te, (290, 30))
        tb = TB(bn, 600, 44, BERRY); card.alpha_composite(tb, (290, 108))
        put(img, card, x, cy)
    logo(img); return wipe(img, prev, t, BERRY)


def p_price(t, b, prev):
    img = bg(SUN); rays(img, W / 2, 760, t, WHITE, a=50)
    disc(img, W / 2, 680, 300, (255, 232, 160))
    put(img, P(PROD, 520, 520), W / 2, 680 + 10 * math.sin(t * 3), scale=back(t / .4))
    kk = ease((t - 1.5 * b) / .3)
    if kk > 0: put(img, TB("কলিং স্মার্ট ওয়াচ মাত্র", 700, 84, BERRY), W / 2, 1100, a=kk)
    kk = back((t - 2.5 * b) / .35)
    if kk > 0:
        put(img, T("Tk 1,350", f("Poppins-Bold.ttf", 190), BERRY), W / 2, 1290, scale=kk)
        col = (150, 104, 60)
        rt = T("Tk 1,540", f("Poppins-Regular.ttf", 64), col); put(img, rt, W / 2, 1450, a=clamp(kk))
        d = ImageDraw.Draw(img); d.line((W / 2 - rt.width / 2 + 20, 1454, W / 2 + rt.width / 2 - 20, 1454), fill=rgba(col), width=6)
        confetti(img, t - 2.5 * b, seed=13)
    kk = back((t - 4 * b) / .35)
    if kk > 0: put(img, pill("Inbox us to order", 50, BERRY, WHITE, padx=50), W / 2, 1620, scale=kk)
    logo(img); return wipe(img, prev, t, SUN)


REELS = [
    dict(id="reel-colmi-p81-call-on-wrist", time="18:30", music=("drive", 6), b=DR.B, cover=5600,
         scenes=[(p_hook, 8), (p_wrist, 9), (p_cards, 12), (p_price, 9),
                 (end_card([(PROD, HQ), ("02.png", HQ), ("12.png", HQ)], BERRY2, SUN, "Calls on your wrist"), 6)]),
]

if __name__ == "__main__":
    mode = sys.argv[1]
    for r in REELS:
        if mode == "preview":
            parts, starts, total = R9.build(r, True); print(r["id"], round(total, 1)); shots = []
            for (fn, dur), st in zip(parts, starts):
                for fr in (.3, .9): shots.append(fn(min(dur * fr, dur - .1)).convert("RGB"))
            cols = 5; rows = math.ceil(len(shots) / cols); sheet = Image.new("RGB", (cols * 270, rows * 480), "white")
            for i, s_ in enumerate(shots): sheet.paste(s_.resize((270, 480), Image.LANCZOS), ((i % cols) * 270, (i // cols) * 480))
            sheet.save(sys.argv[2], quality=86)
        else:
            R9.build(r)
