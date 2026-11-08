"""Two Everyday Cart Reels for 8 Nov: earbuds face-off (top/bottom split, Bangla hook) and Bangla winter tea thermals."""
import os as _os
_R = _os.path.dirname(_os.path.abspath(__file__)); _T = _os.path.dirname(_R)

import os, sys, math
import numpy as np
from PIL import Image, ImageDraw
sys.path.insert(0, _T); sys.path.insert(0, _R)
from mega import T, TB, P, pill, bg, wipe, logo, disc, put, rgba, f, ease, back, clamp, HQ, FL, DARK, WHITE, YEL, _tc, steam
import reels9 as R9
from reels9 import end_card
import drive as DR

W, H = 1080, 1920
R9.OUT = _R + "/out/out1108/"; os.makedirs(R9.OUT, exist_ok=True)
CRIM = (196, 40, 72); INKB = (16, 28, 58); LIME = (200, 240, 90)
COCOA = (70, 44, 36); LATTE = (238, 214, 186); CHAI = (196, 120, 70); MILK = (255, 246, 232)

def tb_pill(text, size, fill, col):
    k = ("tbp", text, size, fill, col)
    if k not in _tc:
        tx = TB(text, 700, size, col); w, h = tx.width + 70, int(size * 1.9)
        s = Image.new("RGBA", (w, h), (0, 0, 0, 0)); ImageDraw.Draw(s).rounded_rectangle((0, 0, w - 1, h - 1), radius=h // 2, fill=rgba(fill))
        s.alpha_composite(tx, ((w - tx.width) // 2, (h - tx.height) // 2)); _tc[k] = s
    return _tc[k]

def bars(img, t, col, n=9, y0=0, y1=H):
    """Flat equaliser bars along the bottom of a zone."""
    d = ImageDraw.Draw(img); bw = W / (n * 2)
    for i in range(n):
        h = 40 + 70 * abs(math.sin(t * 5 + i * .9))
        x = bw / 2 + i * 2 * bw; d.rounded_rectangle((x, y1 - h, x + bw, y1), radius=int(bw / 2), fill=rgba(col))

# ---------------------------------------------------------------- 1. Earbuds face-off: Proove Intro Pro vs Awei T108
def e_hook(t, b, prev):
    img = bg(INKB); bars(img, t, (40, 56, 100), n=11, y1=H)
    for i, (wd, col, sz) in enumerate([("EARBUDS", WHITE, 150), ("FACE OFF", LIME, 170)]):
        kk = (t - i * b) / .25
        if kk > 0: put(img, T(wd, f("Poppins-Bold.ttf", sz), col, True), W / 2, 700 + i * 210, scale=1.4 - .4 * ease(kk), a=clamp(kk * 2))
    kk = back((t - 2.5 * b) / .35)
    if kk > 0: put(img, tb_pill("আপনি কোনটা নেবেন?", 64, CRIM, WHITE), W / 2, 1210, scale=kk)
    logo(img); return img

def e_vs(t, b, prev):
    img = bg(CRIM); ImageDraw.Draw(img).rectangle((0, H / 2, W, H), fill=rgba(INKB))
    k = ease(t / .45)
    put(img, P("03.png", 380, 400), 280 - (1 - k) * 600, 520 + 8 * math.sin(t * 3))
    put(img, P("10.png", 380, 400), W - 280 + (1 - k) * 600, 1400 + 8 * math.sin(t * 3 + 1))
    put(img, T("Proove", f("Poppins-Bold.ttf", 76), WHITE, True), 720, 330, a=k)
    put(img, T("Intro Pro", f("Poppins-Medium.ttf", 52), WHITE), 720, 410, a=k)
    put(img, T("Awei", f("Poppins-Bold.ttf", 76), LIME, True), 360, 1210, a=k)
    put(img, T("T108", f("Poppins-Medium.ttf", 52), WHITE), 360, 1290, a=k)
    vs = Image.new("RGBA", (190, 190), (0, 0, 0, 0)); dd = ImageDraw.Draw(vs); dd.ellipse((0, 0, 189, 189), fill=rgba(LIME))
    tv = T("VS", f("Poppins-Bold.ttf", 76), INKB); vs.alpha_composite(tv, ((190 - tv.width) // 2, (190 - tv.height) // 2))
    put(img, vs, W / 2, H / 2, scale=back((t - .3) / .35), rot=6 * math.sin(t * 5))
    rowsA = ["Tk 2,300", "Bluetooth 5.4", "Transparent ENC", "LED Display Case"]
    rowsB = ["Tk 950", "Bluetooth 5.3", "ENC Calls", "20 Hrs with Case"]
    for i in range(4):
        kk = back((t - (2 + i * 1.3) * b) / .3)
        if kk <= 0: continue
        put(img, pill(rowsA[i], 38, WHITE, CRIM, padx=30), 720, 520 + i * 92 - 30, scale=kk)
        put(img, pill(rowsB[i], 38, LIME, INKB, padx=30), 360, 1370 + i * 92, scale=kk)
    logo(img); return wipe(img, prev, t, CRIM)

def e_ask(t, b, prev):
    img = bg(INKB); bars(img, t, (40, 56, 100), n=11, y1=H)
    put(img, P("03.png", 400, 420), W / 2 - 230, 860 + 10 * math.sin(t * 3), scale=back(t / .4))
    put(img, P("10.png", 400, 420), W / 2 + 230, 860 + 10 * math.sin(t * 3 + 1), scale=back((t - .15) / .4))
    put(img, TB("কোনটা আপনার পছন্দ?", 700, 96, WHITE, True), W / 2, 420, scale=1.25 - .25 * ease(t / .3))
    kk = back((t - .6) / .35)
    if kk > 0: put(img, pill("Comment: PROOVE or T108", 48, LIME, INKB), W / 2, 1300, scale=kk)
    logo(img); return wipe(img, prev, t, INKB)

# ---------------------------------------------------------------- 2. Winter tea thermals (Bangla)
DOTS = [(np.random.default_rng(i).uniform(40, W - 40), np.random.default_rng(i + 50).uniform(0, H), 3 + i % 4) for i in range(40)]
def drift(img, t, col):
    d = ImageDraw.Draw(img)
    for x, y, r in DOTS:
        yy = (y + t * 60 * (r / 3)) % (H + 40) - 20
        d.ellipse((x - r, yy - r, x + r, yy + r), fill=rgba(col))

def mug(img, cx, cy, s=1.0):
    d = ImageDraw.Draw(img); w, h = 150 * s, 170 * s
    d.rounded_rectangle((cx - w, cy - h, cx + w, cy + h), radius=int(40 * s), fill=rgba(MILK))
    d.arc((cx + w - 40 * s, cy - 80 * s, cx + w + 90 * s, cy + 60 * s), -90, 90, fill=rgba(MILK), width=int(32 * s))
    d.ellipse((cx - w + 14 * s, cy - h - 20 * s, cx + w - 14 * s, cy - h + 26 * s), fill=rgba(CHAI))
    d.rounded_rectangle((cx - w, cy + 10 * s, cx + w, cy + 50 * s), radius=0, fill=rgba(CHAI))

def w_hook(t, b, prev):
    img = bg(COCOA); drift(img, t, (96, 64, 52))
    mug(img, W / 2, 1220, 1.0); steam(img, W / 2, 1020, t)
    put(img, TB("শীতের সকাল", 700, 132, LATTE, True), W / 2, 470, a=clamp(t / .3), scale=1.1 - .1 * ease(t / .5))
    kk = ease((t - b) / .5)
    if kk > 0: put(img, TB("গরম চা হাতে, চলুন যেখানেই যান", 600, 60, WHITE), W / 2, 630 + 30 * (1 - kk), a=kk)
    kk = back((t - 2.5 * b) / .35)
    if kk > 0: put(img, pill("3 thermal picks", 50, LATTE, COCOA), W / 2, 1560, scale=kk)
    logo(img); return img

def w_item(n, im, folder, mw, mh, name, cap, colours, price, regular, col, soft, acc):
    def fn(t, b, prev):
        img = bg(col); drift(img, t, soft)
        disc(img, W / 2, 820, 380 + 8 * math.sin(t * 2), soft)
        put(img, P(im, mw, mh, folder), W / 2, 820 + 10 * math.sin(t * 2.2), scale=.85 + .15 * ease(t / .6), a=clamp(t / .3))
        put(img, T(f"{n}/3", f("Poppins-Bold.ttf", 44), acc), W / 2, 200, a=clamp(t / .3))
        put(img, pill(cap, 48, acc, col, padx=40), W / 2, 300, scale=back((t - .1) / .35))
        kk = ease((t - .3) / .45)
        put(img, T(name, f("Poppins-Bold.ttf", 66), WHITE, True), W / 2, 1300 + 30 * (1 - kk), a=kk)
        put(img, T(colours, f("Poppins-Medium.ttf", 40), acc), W / 2, 1390, a=clamp((t - .5) / .3))
        put(img, T(f"Tk {price:,}", f("Poppins-Bold.ttf", 116), WHITE, True), W / 2, 1530, scale=back((t - .6) / .35))
        kk = clamp((t - 1.0) / .3)
        if kk > 0:
            a2 = T(f"Regular Tk {regular:,}", f("Poppins-Medium.ttf", 42), WHITE); put(img, a2, W / 2, 1650, a=kk)
            x0 = W / 2 - a2.width / 2 + T("Regular ", f("Poppins-Medium.ttf", 42), WHITE).width
            ImageDraw.Draw(img).line((x0, 1652, W / 2 + a2.width / 2 - 6, 1652), fill=(255, 255, 255, int(255 * kk)), width=4)
        logo(img); return wipe(img, prev, t, col, W / 2, 820)
    return fn

G = 60 / 92
REELS = [
    dict(id="earbuds-face-off", time="13:30", music=("drive", 9), b=DR.B, cover=6500,
         scenes=[(e_hook, 6), (e_vs, 16), (e_ask, 6), (end_card([("03.png", HQ), ("10.png", HQ), ("13.png", HQ)], INKB, LIME, "Pick your sound"), 7)],
         caption="🎧 Earbuds face off! আপনি কোনটা নেবেন?\n\nProove Intro Pro (APP) Black TWS: 2,300৳\n✔️ 13mm driver, powerful sound\n✔️ Transparent ENC for clear calls\n✔️ Bluetooth 5.4, touch control\n✔️ LED display charging case\n\nAwei T108 Earbuds: 950৳ (regular 1,199৳)\n✔️ 13mm driver\n✔️ ENC, Bluetooth 5.3, USB Type C\n✔️ Up to 6 hours (buds) and 20 hours with case\n\n💬 Comment PROOVE or T108 👇",
         tags="#EverydayCart #EarbudsBattle #Proove #Awei #T108 #WirelessEarbuds #ThisOrThat #TechBD"),
    dict(id="winter-tea-thermals", time="18:00", music=("gentle", 9), b=G, cover=4500,
         scenes=[(w_hook, 7),
                 (w_item(1, "16.png", HQ, 560, 600, "Premium Thermal Tumbler", "860 ML", "Purple  •  White", 800, 1200, (92, 60, 120), (120, 88, 150), (226, 206, 255)), 6),
                 (w_item(2, "hgt_tumbler.png", FL, 600, 560, "Have Good Time Tumbler", "750 ML", "Pink  •  White", 1000, 1200, (176, 84, 104), (200, 112, 132), (255, 222, 230)), 6),
                 (w_item(3, "17.png", HQ, 300, 620, "316 Steel Thermal Bottle", "700 ML", "Brown  •  Pink", 800, 1100, (120, 76, 48), (148, 102, 72), LATTE), 6),
                 (end_card([("16.png", HQ), ("hgt_tumbler.png", FL), ("17.png", HQ)], COCOA, LATTE, "Warm sips, all winter"), 6)],
         caption="☕ শীতের সকাল, গরম চা হাতে চলুন যেখানেই যান!\n\n3 thermal picks for winter:\n\n💜 Premium Thermal Tumbler (860 ml): 800৳ (regular 1,200৳)\n✔️ Double wall vacuum insulation\n✔️ Reusable straw, leak resistant lid\n\n🩷 Have Good Time Insulated Steel Tumbler (750 ml): 1,000৳ (regular 1,200৳)\n✔️ Insulated stainless steel, secure lid\n✔️ Carry handle, Pink and White\n\n🤎 316 Stainless Steel Thermal Bottle (700 ml): 800৳ (regular 1,100৳)\n✔️ Safety lock lid, Brown and Pink",
         tags="#EverydayCart #WinterEssentials #ThermalTumbler #ThermosBottle #TeaLover #শীত #OnlineShoppingBD"),
]

if __name__ == "__main__":
    mode = sys.argv[1]; ids = sys.argv[2:]
    sel = [r for r in REELS if not ids or r["id"] in ids]
    if mode == "preview":
        shots = []
        for r in sel:
            parts, starts, total = R9.build(r, True); print(r["id"], round(total, 1))
            for (fn, dur), st in zip(parts, starts):
                for fr in (.3, .9): shots.append(fn(min(dur * fr, dur - .1)).convert("RGB"))
        cols = 6; rows = math.ceil(len(shots) / cols); sheet = Image.new("RGB", (cols * 270, rows * 480), "white")
        for i, s_ in enumerate(shots): sheet.paste(s_.resize((270, 480), Image.LANCZOS), ((i % cols) * 270, (i // cols) * 480))
        sheet.save(sys.argv[2] if False else _R + "/out/r1108_sheet.jpg", quality=86)
    else:
        for r in sel: R9.build(r)
