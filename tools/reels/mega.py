"""Everyday Cart 'Gadget Show' long Reel: 10 beat-synced segments, original music, flat style."""
import os as _os
_R = _os.path.dirname(_os.path.abspath(__file__)); _T = _os.path.dirname(_R)

import os, sys, math, subprocess
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont
sys.path.insert(0, _T); sys.path.insert(0, _R)
from render_video import f, clamp, ease, back, product_sprite, pill_sprite
from viral import put, LOGO, LOGO_CARD, rgba
from drive import drive, B, SR
from scipy.io import wavfile

W, H, FPS = 1080, 1920, 30
HQ = _T + "/cutouts/hq/"; FL = _T + "/cutouts/flat/"
OUT = _R + "/out/out_mega/"; os.makedirs(OUT, exist_ok=True)
_tc = {}
BN = _T + "/assets/fonts/hind-siliguri-bengali-%d-normal.woff"
DARK = (20, 21, 27); WHITE = (255, 255, 255); YEL = (255, 200, 46); CORAL = (255, 98, 86); BLUE = (46, 98, 255)
PURP = (124, 76, 245); GREEN = (18, 184, 134); CREAM = (255, 246, 236); ORANGE = (255, 138, 40)

_fb = {}
def fb(w, s):
    if (w, s) not in _fb: _fb[(w, s)] = ImageFont.truetype(BN % w, s, layout_engine=ImageFont.Layout.RAQM)
    return _fb[(w, s)]
BNL = _T + "/assets/fonts/hind-siliguri-latin-%d-normal.woff"
def is_bn(ch): return '\u0980' <= ch <= '\u09ff' or ch in ' \u200c\u200d'
def TB(text, w, size, col, shadow=False):
    k = ("tb", text, w, size, col, shadow)
    if k in _tc: return _tc[k]
    fbn = fb(w, size); fl = ImageFont.truetype(BNL % w, size)
    runs = []
    for ch in text:
        b = is_bn(ch)
        if runs and runs[-1][0] == b: runs[-1][1] += ch
        else: runs.append([b, ch])
    asc = fbn.getmetrics()[0]; tw = sum(int((fbn if b else fl).getlength(r)) for b, r in runs) + 30
    s = Image.new("RGBA", (tw, int(size * 1.9)), (0, 0, 0, 0)); d = ImageDraw.Draw(s); x = 15
    for b, r in runs:
        ft = fbn if b else fl; d.text((x, 12 + asc), r, font=ft, fill=rgba(col), anchor="ls"); x += ft.getlength(r)
    s = s.crop(s.getbbox()); pad = Image.new("RGBA", (s.width + 24, s.height + 24), (0, 0, 0, 0)); pad.alpha_composite(s, (12, 12)); s = pad
    if shadow:
        sh = Image.new("RGBA", s.size, (0, 0, 0, 255)); sh.putalpha(s.split()[3].filter(ImageFilter.GaussianBlur(10)).point(lambda v: int(v * .5)))
        o = Image.new("RGBA", s.size, (0, 0, 0, 0)); o.alpha_composite(sh, (0, 6)); o.alpha_composite(s); s = o
    _tc[k] = s; return s
_tc = {}
def T(text, font, col, shadow=False):
    k = (text, id(font), col, shadow)
    if k in _tc: return _tc[k]
    bb = font.getbbox(text); w = bb[2] - bb[0] + 24; h = bb[3] - bb[1] + 30
    s = Image.new("RGBA", (w, h), (0, 0, 0, 0)); ImageDraw.Draw(s).text((12 - bb[0], 12 - bb[1]), text, font=font, fill=rgba(col) if len(col) == 3 else col)
    if shadow:
        sh = Image.new("RGBA", s.size, (0, 0, 0, 255)); sh.putalpha(s.split()[3].filter(ImageFilter.GaussianBlur(10)).point(lambda v: int(v * .5)))
        o = Image.new("RGBA", s.size, (0, 0, 0, 0)); o.alpha_composite(sh, (0, 6)); o.alpha_composite(s); s = o
    _tc[k] = s; return s
_pc = {}
def P(name, mw, mh=None, folder=HQ):
    k = (name, mw, mh)
    if k not in _pc: _pc[k] = product_sprite(folder + name, mw, mh or mw)
    return _pc[k]
def pill(text, size, fill, col, padx=36, bold=True):
    k = ("pill", text, size, fill, col)
    if k not in _tc: _tc[k] = pill_sprite(text, f("Poppins-Bold.ttf" if bold else "Poppins-Medium.ttf", size), rgba(fill), rgba(col), padx=padx)
    return _tc[k]
def bg(col): return Image.new("RGBA", (W, H), rgba(col))
def wipe(img, prev, t, col, ox=W / 2, oy=H / 2):
    """Circle reveal of the new segment colour over the previous one."""
    k = ease(t / 0.32)
    if k >= 1: return img
    base = Image.new("RGBA", (W, H), rgba(prev)); r = k * math.hypot(W, H)
    m = Image.new("L", (W, H), 0); ImageDraw.Draw(m).ellipse((ox - r, oy - r, ox + r, oy + r), fill=255)
    base.paste(img, (0, 0), m); return base
def logo(img): img.alpha_composite(LOGO_CARD, (W - LOGO_CARD.width - 50, 60))
def rays(img, cx, cy, t, col, n=14, a=60, r=1300):
    ov = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(ov)
    for i in range(n):
        ang = 2 * math.pi * i / n + t * 0.4
        d.polygon([(cx, cy), (cx + r * math.cos(ang - 0.09), cy + r * math.sin(ang - 0.09)), (cx + r * math.cos(ang + 0.09), cy + r * math.sin(ang + 0.09))], fill=rgba(col, a))
    img.alpha_composite(ov)
def disc(img, cx, cy, r, col):
    ImageDraw.Draw(img).ellipse((cx - r, cy - r, cx + r, cy + r), fill=rgba(col) if len(col) == 3 else col)
def price_tag(p, size=88, col=WHITE): return T(f"Tk {p:,}", f("Poppins-Bold.ttf", size), col)
def confetti(img, t, seed=3, n=70):
    rng = np.random.default_rng(seed); d = ImageDraw.Draw(img)
    cols = [CORAL, YEL, BLUE, GREEN, PURP, WHITE]
    for i in range(n):
        x0 = rng.uniform(0, W); v = rng.uniform(500, 900); y = -50 + v * t + rng.uniform(-300, 0); x = x0 + 40 * math.sin(t * 4 + i)
        c = cols[i % len(cols)]; s = rng.uniform(10, 20); ang = t * 6 + i
        pts = [(x + s * math.cos(ang + k * math.pi / 2), y + s * 0.5 * math.sin(ang + k * math.pi / 2)) for k in range(4)]
        if -40 < y < H + 40: d.polygon(pts, fill=rgba(c))

# ======================= segments =======================
def seg_intro(t):
    img = bg(DARK); rays(img, W / 2, 900, t, YEL, a=18)
    for i, (wd, col) in enumerate([("STOP", WHITE), ("SCROLLING", YEL)]):
        kk = (t - i * B) / 0.2
        if kk > 0: put(img, T(wd, f("Poppins-Bold.ttf", 170 if i == 0 else 140), col), W / 2, 700 + i * 200, scale=1.5 - .5 * ease(kk), a=clamp(kk * 2))
    kk = (t - 2 * B) / 0.3
    if kk > 0: put(img, T("10 reasons to shop at", f("Poppins-Medium.ttf", 54), (255, 255, 255, 220)), W / 2, 1110 + 30 * (1 - ease(kk)), a=clamp(kk))
    kk = back((t - 3 * B) / 0.4)
    if kk > 0:
        lc = LOGO.resize((420, int(LOGO.height * 420 / LOGO.width)), Image.LANCZOS)
        cd = Image.new("RGBA", (lc.width + 70, lc.height + 50), (0, 0, 0, 0))
        ImageDraw.Draw(cd).rounded_rectangle((0, 0, cd.width - 1, cd.height - 1), radius=36, fill=(255, 255, 255, 255)); cd.alpha_composite(lc, (35, 25))
        put(img, cd, W / 2, 1290, scale=kk)
    kk = (t - 4.5 * B) / 0.3
    if kk > 0: put(img, pill("Watch till the end", 40, YEL, DARK), W / 2, 1520, a=clamp(kk))
    return img

def seg_guess(t, prev):
    img = bg(CORAL); rays(img, W / 2, 760, t, WHITE, a=26)
    put(img, T("GUESS THE PRICE?", f("Poppins-Bold.ttf", 92), WHITE, True), W / 2, 230 + 30 * (1 - ease(t / .3)), a=clamp(t / .2))
    put(img, T("Oraimo SpaceBuds Neo+", f("Poppins-Medium.ttf", 50), WHITE), W / 2, 335, a=clamp((t - .2) / .3))
    kp = (t - 0.15) / 0.5
    put(img, P("12.png", 560), W / 2, 760 + 14 * math.sin(t * 3), scale=0.4 + 0.6 * back(kp), rot=(1 - ease(kp)) * 25, a=clamp(kp * 3))
    opts = [("A", "Tk 2,500"), ("B", "Tk 1,940"), ("C", "Tk 1,500")]
    reveal = 12 * B
    for i, (l, v) in enumerate(opts):
        kk = back((t - (2 + i) * B) / 0.35)
        if kk <= 0: continue
        ok = i == 1 and t > reveal; wrong = i != 1 and t > reveal
        fill = (40, 200, 120) if ok else ((255, 255, 255, 120) if wrong else WHITE); col = WHITE if ok else DARK
        card = Image.new("RGBA", (300, 130), (0, 0, 0, 0)); d = ImageDraw.Draw(card)
        d.rounded_rectangle((0, 0, 299, 129), radius=30, fill=rgba(fill) if len(fill) == 3 else fill)
        d.text((26, 30), l, font=f("Poppins-Bold.ttf", 52), fill=rgba(col) if not ok else rgba(WHITE)); d.text((88, 38), v, font=f("Poppins-Bold.ttf", 44), fill=rgba(col))
        sc = kk * (1 + 0.12 * math.exp(-(t - reveal) * 6) if ok else kk)
        put(img, card, 180 + i * 360, 1230, scale=sc)
    for n in range(3):           # 3, 2, 1 countdown
        s = (6 + 2 * n) * B
        if s <= t < s + 2 * B:
            k = (t - s) / (2 * B); put(img, T(str(3 - n), f("Poppins-Bold.ttf", 260), WHITE, True), W / 2, 1520, scale=1.6 - 0.6 * ease(k * 3), a=clamp(1.3 - k))
    if t > reveal:
        k = back((t - reveal) / 0.35)
        put(img, T("Tk 1,940", f("Poppins-Bold.ttf", 150), YEL, True), W / 2, 1500, scale=k, rot=4 * (1 - ease((t - reveal) / .3)))
        kk = (t - reveal - 0.4) / .3
        if kk > 0: put(img, pill("Got it right? Comment below", 40, WHITE, CORAL), W / 2, 1680, a=clamp(kk))
        confetti(img, t - reveal)
    logo(img); return wipe(img, prev, t, CORAL)

def seg_vs(t, prev):
    img = bg(CORAL); ImageDraw.Draw(img).rectangle((W / 2, 0, W, H), fill=rgba(PURP))
    k = ease(t / .4)
    put(img, P("12.png", 400), W / 4 - (1 - k) * 500, 620, a=clamp(t / .2))
    put(img, P("13.png", 400), 3 * W / 4 + (1 - k) * 500, 620, a=clamp(t / .2))
    put(img, T("THIS", f("Poppins-Bold.ttf", 90), WHITE, True), W / 4, 230, a=k); put(img, T("THAT", f("Poppins-Bold.ttf", 90), WHITE, True), 3 * W / 4, 230, a=k)
    put(img, T("SpaceBuds Neo+", f("Poppins-Bold.ttf", 44), WHITE), W / 4, 880, a=k); put(img, T("SpaceBuds Lite", f("Poppins-Bold.ttf", 44), WHITE), 3 * W / 4, 880, a=k)
    vs = Image.new("RGBA", (190, 190), (0, 0, 0, 0)); ImageDraw.Draw(vs).ellipse((0, 0, 189, 189), fill=rgba(YEL))
    vs.alpha_composite(T("VS", f("Poppins-Bold.ttf", 76), DARK), (40, 30)); put(img, vs, W / 2, 620, scale=back((t - .3) / .35), rot=10 * math.sin(t * 5))
    rows = [("Price", "Tk 1,940", "Tk 1,310"), ("Battery", "30 Hrs", "40 Hrs"), ("Audio", "Sound360", "Spatial"), ("Colour", "Off White", "Black")]
    for i, (lab, a_, b_) in enumerate(rows):
        kk = ease((t - (2 + i) * B) / .3)
        if kk <= 0: continue
        y = 1040 + i * 120
        ov = Image.new("RGBA", (W, 100), (0, 0, 0, 0)); ImageDraw.Draw(ov).rounded_rectangle((60, 0, W - 60, 96), radius=48, fill=(255, 255, 255, int(235 * kk))); img.alpha_composite(ov, (0, y))
        put(img, T(a_, f("Poppins-Bold.ttf", 40), CORAL), 250, y + 48, a=kk); put(img, T(b_, f("Poppins-Bold.ttf", 40), PURP), W - 250, y + 48, a=kk)
        put(img, T(lab, f("Poppins-Medium.ttf", 30), (120, 120, 130)), W / 2, y + 48, a=kk)
    kk = back((t - 7 * B) / .35)
    if kk > 0: put(img, pill("Comment your pick: NEO+ or LITE?", 42, YEL, DARK), W / 2, 1600, scale=kk)
    logo(img); return wipe(img, prev, t, CORAL)

def battery(img, cx, cy, level, col):
    d = ImageDraw.Draw(img); w, h = 220, 110
    d.rounded_rectangle((cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2), radius=18, outline=rgba(WHITE), width=8)
    d.rounded_rectangle((cx + w / 2 + 4, cy - 22, cx + w / 2 + 22, cy + 22), radius=6, fill=rgba(WHITE))
    if level > 0: d.rounded_rectangle((cx - w / 2 + 14, cy - h / 2 + 14, cx - w / 2 + 14 + (w - 28) * level, cy + h / 2 - 14), radius=8, fill=rgba(col))

def seg_pov(t, prev):
    cut = 6 * B
    if t < cut:
        img = bg(DARK)
        put(img, T("POV:", f("Poppins-Bold.ttf", 110), YEL), W / 2, 520, a=clamp(t / .2))
        for i, line in enumerate(["জিমের মাঝখানে", "ইয়ারবাডসের চার্জ শেষ..."]):
            kk = ease((t - .3 - i * B) / .3)
            if kk > 0: put(img, TB(line, 700, 96, WHITE), W / 2, 700 + i * 130 + 30 * (1 - kk), a=kk)
        lvl = max(0.02, 0.35 - t * 0.25); blink = (int(t * 6) % 2 == 0) or lvl > .05
        if blink: battery(img, W / 2, 1150, lvl, (240, 60, 60))
        put(img, T("1%", f("Poppins-Bold.ttf", 60), (240, 60, 60)), W / 2, 1290, a=clamp((t - .5) / .2))
        shake = 8 * math.sin(t * 60) if t > cut - 0.4 else 0
        if shake: img = img.transform(img.size, Image.AFFINE, (1, 0, shake, 0, 1, 0))
        logo(img); return wipe(img, prev, t, DARK)
    t2 = t - cut; img = bg(GREEN); rays(img, W / 2, 900, t2, WHITE, a=30)
    put(img, TB("সমাধান?", 700, 120, WHITE, True), W / 2, 330, scale=1.4 - .4 * ease(t2 / .25))
    put(img, P("10.png", 560), W / 2, 860 + 12 * math.sin(t2 * 3), scale=back(t2 / .4))
    kk = ease((t2 - .4) / .3)
    put(img, T("Awei T108", f("Poppins-Bold.ttf", 76), WHITE), W / 2, 1230, a=kk)
    put(img, TB("কেসসহ ২০ ঘণ্টা ব্যাটারি", 600, 64, WHITE), W / 2, 1340, a=kk)
    kk = back((t2 - .7) / .35)
    if kk > 0: put(img, pill("মাত্র Tk 950", 0, YEL, DARK) if False else bn_pill("মাত্র ৯৫০ টাকা"), W / 2, 1500, scale=kk)
    logo(img); return img
def bn_pill(text):
    k = ("bnp", text)
    if k not in _tc:
        ft = fb(700, 64); bb = ft.getbbox(text); w = bb[2] - bb[0] + 90; h = 120
        s = Image.new("RGBA", (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(s); d.rounded_rectangle((0, 0, w - 1, h - 1), radius=60, fill=rgba(YEL))
        d.text((45 - bb[0], (h - (bb[3] - bb[1])) / 2 - bb[1]), text, font=ft, fill=rgba(DARK)); _tc[k] = s
    return _tc[k]

def seg_explain(t, prev):
    img = bg(BLUE); disc(img, W / 2, 900, 330, (255, 255, 255, 40) if False else (70, 120, 255))
    put(img, T("Oraimo Watch 5 Lite", f("Poppins-Bold.ttf", 80), WHITE, True), W / 2, 230, a=clamp(t / .25))
    put(img, T("in 8 seconds", f("Poppins-Medium.ttf", 48), (255, 255, 255, 220)), W / 2, 330, a=clamp((t - .2) / .25))
    put(img, P("02.png", 470, 540), W / 2, 900 + 10 * math.sin(t * 2.5), scale=back(t / .45))
    calls = [("2.01\" HD Display", (W / 2 - 40, 760), (190, 560)), ("Bluetooth Calling", (W / 2 + 120, 800), (880, 560)),
             ("IP68 Water Resistant", (W / 2 - 60, 1000), (200, 1290)), ("Up to 7 Days Battery", (W / 2 + 150, 1000), (870, 1290)),
             ("105+ Sports Modes", (W / 2, 1120), (W / 2, 1450))]
    ov = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(ov)
    for i, (txt, a_, b_) in enumerate(calls):
        k = ease((t - (2 + 2 * i) * B) / .35)
        if k <= 0: continue
        ex, ey = a_[0] + (b_[0] - a_[0]) * k, a_[1] + (b_[1] - a_[1]) * k
        d.line((a_[0], a_[1], ex, ey), fill=rgba(YEL), width=6); d.ellipse((a_[0] - 12, a_[1] - 12, a_[0] + 12, a_[1] + 12), fill=rgba(YEL))
    img.alpha_composite(ov)
    for i, (txt, a_, b_) in enumerate(calls):
        k = back((t - (2 + 2 * i) * B - .25) / .3)
        if k > 0: put(img, pill(txt, 34, WHITE, BLUE, padx=28), b_[0], b_[1], scale=k)
    kk = back((t - 13 * B) / .35)
    if kk > 0: put(img, T("Tk 1,650", f("Poppins-Bold.ttf", 130), YEL, True), W / 2, 1640, scale=kk)
    logo(img); return wipe(img, prev, t, BLUE)

def seg_unbox(t, prev):
    img = bg(PURP); cx, cy = W / 2, 1150
    open_t = 3 * B
    if t > open_t: rays(img, cx, cy - 120, t, YEL, a=int(70 * clamp((t - open_t) / .3)))
    d = ImageDraw.Draw(img)
    shake = 10 * math.sin(t * 50) * (1 if 1.0 * B < t < open_t else 0)
    bw, bh = 520, 380
    # box body
    d.rounded_rectangle((cx - bw / 2 + shake, cy - bh / 2 + 60, cx + bw / 2 + shake, cy + bh / 2 + 60), radius=24, fill=rgba((26, 27, 33)))
    d.rectangle((cx - 40 + shake, cy - bh / 2 + 60, cx + 40 + shake, cy + bh / 2 + 60), fill=rgba(YEL))
    # product rising
    if t > open_t:
        k = back((t - open_t) / .5); put(img, P("04.png", 470), cx, cy - 60 - 420 * k, scale=0.5 + 0.5 * k, a=clamp((t - open_t) / .15))
        d = ImageDraw.Draw(img)
        d.rounded_rectangle((cx - bw / 2, cy - bh / 2 + 60, cx + bw / 2, cy + bh / 2 + 60), radius=24, fill=rgba((26, 27, 33)))
        d.rectangle((cx - 40, cy - bh / 2 + 60, cx + 40, cy + bh / 2 + 60), fill=rgba(YEL))
    # lid
    lid = Image.new("RGBA", (bw + 40, 110), (0, 0, 0, 0)); ImageDraw.Draw(lid).rounded_rectangle((0, 0, bw + 39, 109), radius=24, fill=rgba((40, 41, 48)))
    ImageDraw.Draw(lid).rectangle(((bw + 40) / 2 - 40, 0, (bw + 40) / 2 + 40, 109), fill=rgba(YEL))
    lk = ease((t - open_t) / .45)
    put(img, lid, cx + shake + 380 * lk, cy - bh / 2 + 10 - 700 * lk, rot=-35 * lk, a=1 - clamp((t - open_t - .3) / .3))
    put(img, T("UNBOXING", f("Poppins-Bold.ttf", 100), WHITE, True), W / 2, 230, a=clamp(t / .2))
    kk = ease((t - open_t - .4) / .3)
    if kk > 0:
        put(img, T("Oraimo Necklace Lite", f("Poppins-Bold.ttf", 66), WHITE), W / 2, 1520, a=kk)
        put(img, T("ENC Calls  •  30 Hrs Playtime", f("Poppins-Medium.ttf", 42), (255, 255, 255, 220)), W / 2, 1610, a=kk)
        put(img, price_tag(1300, 100, YEL), W / 2, 1730, scale=back((t - open_t - .5) / .35))
    logo(img); return wipe(img, prev, t, PURP)

def steam(img, cx, top, t):
    ov = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(ov)
    for j in range(3):
        pts = []
        for i in range(30):
            y = top - i * 9; x = cx + (j - 1) * 55 + 18 * math.sin(i * 0.35 + t * 4 + j)
            pts.append((x, y))
        d.line(pts, fill=(255, 255, 255, 170), width=12, joint="curve")
    img.alpha_composite(ov.filter(ImageFilter.GaussianBlur(3)))

def seg_hot(t, prev):
    k = clamp(t / (11 * B))
    top = tuple(int(a + (b - a) * k) for a, b in zip((255, 190, 120), (40, 44, 90)))
    img = bg(top); d = ImageDraw.Draw(img)
    # sun/moon arc
    ang = math.pi * (1 - k); sx, sy = W / 2 + 420 * math.cos(ang), 760 - 360 * math.sin(ang)
    disc(img, sx, sy, 60, YEL if k < .7 else (240, 240, 255))
    put(img, T("HOT FOR HOURS", f("Poppins-Bold.ttf", 96), WHITE, True), W / 2, 230, a=clamp(t / .2))
    put(img, T("Morning to night, your drink stays hot", f("Poppins-Medium.ttf", 40), WHITE), W / 2, 330, a=clamp((t - .2) / .3))
    put(img, P("15.png", 430, 560), W / 2, 1060, scale=back(t / .4))
    steam(img, W / 2 - 10, 760, t)
    stops = [("8 AM", "Office"), ("1 PM", "Lunch"), ("6 PM", "Home")]
    d = ImageDraw.Draw(img); d.line((170, 1440, 910, 1440), fill=rgba(WHITE, 120), width=8); d.line((170, 1440, 170 + 740 * k, 1440), fill=rgba(YEL), width=8)
    for i, (tm, lab) in enumerate(stops):
        x = 170 + 370 * i; on = k >= i / 2 - .01
        disc(img, x, 1440, 26, YEL if on else (255, 255, 255, 140))
        put(img, T(tm, f("Poppins-Bold.ttf", 44), WHITE), x, 1515, a=1 if on else .5); put(img, T(lab, f("Poppins-Medium.ttf", 34), WHITE), x, 1570, a=1 if on else .5)
    kk = back((t - 8 * B) / .35)
    if kk > 0: put(img, pill("Big Mac 316 Thermos Cup  •  Tk 1,000", 40, WHITE, DARK), W / 2, 1720, scale=kk)
    logo(img); return wipe(img, prev, t, (255, 190, 120))

def seg_under(t, prev):
    img = bg(YEL)
    put(img, T("UNDER", f("Poppins-Bold.ttf", 90), DARK), W / 2, 210, scale=1.3 - .3 * ease(t / .25))
    put(img, T("1,000 TAKA", f("Poppins-Bold.ttf", 140), DARK, False), W / 2, 330, scale=1.3 - .3 * ease((t - .1) / .25))
    items = [("10.png", "Awei T108", 950, HQ), ("19.png", "Smart LED Bottle", 350, HQ), ("20.png", "Minitree Mumpot", 400, HQ),
             ("21.png", "Baby Care Kit", 480, HQ), ("08.png", "Minitree Tritan Bottle", 450, HQ), ("17.png", "Kids Thermal Bottle", 800, HQ)]
    for i, (im, name, pr, fol) in enumerate(items):
        k = back((t - (1 + i * 1.5) * B) / .35)
        if k <= 0: continue
        cx = 285 + (i % 2) * 510; cy = 600 + (i // 2) * 410
        card = _tc.get(("ucard", i))
        if card is None:
            card = Image.new("RGBA", (470, 390), (0, 0, 0, 0)); d = ImageDraw.Draw(card); d.rounded_rectangle((0, 0, 469, 389), radius=36, fill=rgba(WHITE))
            p = P(im, 250, 230, fol); card.alpha_composite(p, (235 - p.width // 2, 135 - p.height // 2))
            nm = T(name, f("Poppins-Medium.ttf", 32 if len(name) < 18 else 28), (80, 80, 90)); card.alpha_composite(nm, (235 - nm.width // 2, 262))
            pt = T(f"Tk {pr:,}", f("Poppins-Bold.ttf", 52), CORAL); card.alpha_composite(pt, (235 - pt.width // 2, 302)); _tc[("ucard", i)] = card
        put(img, card, cx, cy + 230, scale=k, rot=(1 - ease((t - (1 + i * 1.5) * B) / .3)) * (8 if i % 2 else -8))
    logo(img); return wipe(img, prev, t, YEL)

def seg_top5(t, prev):
    ranks = [(5, "flat/hgt_tumbler.png", "Have Good Time Tumbler", 1000, (255, 150, 170)), (4, "04.png", "Oraimo Necklace Lite", 1300, PURP),
             (3, "10.png", "Awei T108 Earbuds", 950, GREEN), (2, "02.png", "Oraimo Watch 5 Lite", 1650, BLUE), (1, "12.png", "Oraimo SpaceBuds Neo+", 1940, CORAL)]
    step = 2.4 * B; i = min(4, int(t / step)); lt = t - i * step
    n, im, name, pr, col = ranks[i]
    img = bg(col); rays(img, W / 2, 950, t, WHITE, a=24)
    put(img, T("TOP 5 PICKS THIS MONTH", f("Poppins-Bold.ttf", 64), WHITE, True), W / 2, 210)
    put(img, T(f"#{n}", f("Poppins-Bold.ttf", 300), (255, 255, 255, 70)), W / 2, 560, scale=1.3 - .3 * ease(lt / .25))
    folder = FL if im.startswith("flat/") else HQ; nm = im.replace("flat/", "")
    put(img, P(nm, 520, 520, folder), W / 2, 980 + 10 * math.sin(t * 3), scale=back(lt / .35))
    kk = ease((lt - .15) / .25)
    put(img, T(name, f("Poppins-Bold.ttf", 64), WHITE, True), W / 2, 1380 + 30 * (1 - kk), a=kk)
    put(img, T(f"Tk {pr:,}", f("Poppins-Bold.ttf", 110), WHITE, True), W / 2, 1510, scale=back((lt - .2) / .3))
    if n == 1: confetti(img, lt, seed=9)
    logo(img); return wipe(img, prev, t, ranks[0][4])

def pumpkin(img, cx, cy, s):
    d = ImageDraw.Draw(img)
    for dx, w in ((-0.45, .55), (0.45, .55), (0, .6)):
        d.ellipse((cx + dx * s - w * s, cy - .75 * s, cx + dx * s + w * s, cy + .75 * s), fill=rgba(ORANGE if dx else (255, 155, 60)))
    d.rounded_rectangle((cx - .1 * s, cy - 1.0 * s, cx + .1 * s, cy - .65 * s), radius=6, fill=rgba((70, 120, 60)))
    for ex in (-.32, .32): d.polygon([(cx + ex * s - .14 * s, cy - .05 * s), (cx + ex * s + .14 * s, cy - .05 * s), (cx + ex * s, cy - .3 * s)], fill=rgba(DARK))
    d.chord((cx - .45 * s, cy - .1 * s, cx + .45 * s, cy + .45 * s), 0, 180, fill=rgba(DARK))

def seg_gift(t, prev):
    img = bg((40, 26, 60))
    if t < 5 * B:
        pumpkin(img, W / 2, 760 + 15 * math.sin(t * 5), 170 * back(t / .4))
        put(img, T("Halloween is over.", f("Poppins-Bold.ttf", 78), WHITE, True), W / 2, 1120, a=clamp((t - .2) / .25))
        kk = back((t - 2 * B) / .35)
        if kk > 0: put(img, T("The treats aren't.", f("Poppins-Bold.ttf", 90), ORANGE, True), W / 2, 1260, scale=kk)
        logo(img); return wipe(img, prev, t, (40, 26, 60))
    t2 = t - 5 * B; img = bg(CREAM)
    put(img, T("GIFT IDEAS", f("Poppins-Bold.ttf", 110), DARK), W / 2, 220, scale=1.2 - .2 * ease(t2 / .25))
    put(img, T("Treat someone you love", f("Poppins-Medium.ttf", 46), (100, 100, 110)), W / 2, 330)
    gifts = [("FOR HIM", "02.png", "Oraimo Watch 5 Lite", 1650, BLUE), ("FOR HER", "12.png", "Oraimo SpaceBuds Neo+", 1940, CORAL),
             ("FOR NEW MOMS", "21.png", "10 Pc Baby Care Kit", 480, GREEN)]
    for i, (lab, im, name, pr, col) in enumerate(gifts):
        k = ease((t2 - i * 1.5 * B) / .35)
        if k <= 0: continue
        y = 560 + i * 400; card = _tc.get(("gcard", i))
        if card is None:
            card = Image.new("RGBA", (940, 360), (0, 0, 0, 0)); d = ImageDraw.Draw(card); d.rounded_rectangle((0, 0, 939, 359), radius=40, fill=rgba(col))
            p = P(im, 280, 290); card.alpha_composite(p, (190 - p.width // 2, 180 - p.height // 2))
            card.alpha_composite(pill(lab, 30, WHITE, col, padx=24), (380, 50))
            card.alpha_composite(T(name, f("Poppins-Bold.ttf", 46 if len(name) < 20 else 40), WHITE), (370, 130))
            card.alpha_composite(T(f"Tk {pr:,}", f("Poppins-Bold.ttf", 80), WHITE), (370, 200)); _tc[("gcard", i)] = card
        put(img, card, W / 2 + (1 - k) * (W if i % 2 else -W), y + 180)
    logo(img); return img

def seg_end(t, prev):
    img = bg(DARK); rays(img, W / 2, 800, t, YEL, a=16)
    prods = [P(n, 260) for n in ("12.png", "02.png", "04.png", "15.png", "21.png")]
    for i, p in enumerate(prods):
        kk = (t - .1 - i * .07) / .4; ang = math.radians(-150 + i * 30)
        put(img, p, W / 2 + 400 * math.cos(ang), 720 + 360 * math.sin(ang) + 10 * math.sin(t * 3 + i), scale=0.75 * back(kk), a=clamp(kk * 3))
    lc = LOGO.resize((400, int(LOGO.height * 400 / LOGO.width)), Image.LANCZOS)
    cd = Image.new("RGBA", (lc.width + 70, lc.height + 50), (0, 0, 0, 0))
    ImageDraw.Draw(cd).rounded_rectangle((0, 0, cd.width - 1, cd.height - 1), radius=36, fill=(255, 255, 255, 255)); cd.alpha_composite(lc, (35, 25))
    put(img, cd, W / 2, 860, scale=back((t - .3) / .4))
    def line(spr, y, st):
        kk = (t - st) / .35
        if kk > 0: put(img, spr, W / 2, y + 40 * (1 - ease(kk)), a=clamp(kk))
    line(T("Gadgets • Thermal Bottles • Baby Care", f("Poppins-Medium.ttf", 40), WHITE), 1090, .5)
    kk = back((t - .7) / .4)
    if kk > 0: put(img, pill("Order: everydaycart.online", 50, YEL, DARK, padx=50), W / 2, 1230, scale=kk)
    line(T("Inbox us to order  •  Limited stock", f("Poppins-Medium.ttf", 40), WHITE), 1360, .9)
    line(T("Follow for more", f("Poppins-Bold.ttf", 60), YEL), 1500, 1.2)
    return wipe(img, prev, t, DARK)

SEGS = [  # (name, fn, beats, colour the next segment wipes from)
    ("intro", lambda t, p: seg_intro(t), 6, DARK), ("guess", seg_guess, 16, CORAL), ("vs", seg_vs, 12, PURP), ("pov", seg_pov, 12, GREEN),
    ("explain", seg_explain, 16, BLUE), ("unbox", seg_unbox, 10, PURP), ("hot", seg_hot, 12, (40, 44, 90)), ("under", seg_under, 12, YEL),
    ("top5", seg_top5, 13, CORAL), ("gift", seg_gift, 14, CREAM), ("end", seg_end, 10, DARK)]

def encode(name, fn, dur):
    tmp = OUT + name + ".tmp.mp4"; n = int(round(dur * FPS))
    p = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
                          "-c:v", "libx264", "-preset", "veryfast", "-crf", "18", "-pix_fmt", "yuv420p", tmp], stdin=subprocess.PIPE)
    for k in range(n): p.stdin.write(fn(k / FPS).convert("RGB").tobytes())
    p.stdin.close()
    if p.wait() == 0: os.replace(tmp, OUT + name + ".mp4")

if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else "preview"
    if mode == "preview":
        prev = DARK; shots = []
        moments = {"intro": [2.6], "guess": [3.0, 6.5], "vs": [4.5], "pov": [2.0, 4.6], "explain": [7.4], "unbox": [3.6], "hot": [4.5],
                   "under": [5.5], "top5": [1.0, 5.6], "gift": [1.6, 5.8], "end": [2.6]}
        for name, fn, beats, nxt in SEGS:
            for m in moments[name]: shots.append(fn(m, prev).convert("RGB"))
            prev = nxt
        cols = 8; rows = math.ceil(len(shots) / cols); sheet = Image.new("RGB", (cols * 270, rows * 480))
        for i, s in enumerate(shots): sheet.paste(s.resize((270, 480), Image.LANCZOS), ((i % cols) * 270, (i // cols) * 480))
        sheet.save("/tmp/mega_sheet.jpg", quality=88)
        for i, s in enumerate(shots): s.save(f"/tmp/mg{i}.jpg", quality=88)
    else:
        prev = DARK; parts = []; starts = []; s = 0
        for name, fn, beats, nxt in SEGS:
            dur = beats * B; parts.append((name, (lambda fn, pv: (lambda t: fn(t, pv)))(fn, prev), dur)); starts.append(s); s += dur; prev = nxt
        only = sys.argv[2:] or [p[0] for p in parts]
        for name, fn, dur in parts:
            if name in only: encode(name, fn, dur); print(name, flush=True)
        open(OUT + "list.txt", "w").write("".join(f"file '{n}.mp4'\n" for n, _, _ in parts))
        total = s; mix = drive(total, starts[1], starts[1:], starts[-1])
        wavfile.write(OUT + "music.wav", SR, (np.stack([mix, mix], 1) * 32767).astype(np.int16))
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", OUT + "list.txt", "-i", OUT + "music.wav",
                        "-map", "0:v", "-map", "1:a", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-shortest", "-movflags", "+faststart",
                        OUT + "07_everyday_cart_gadget_show.mp4"], check=True)
        print("done", round(total, 1))
