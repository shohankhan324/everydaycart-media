"""Everyday Cart Reel for 17 Nov: "This or that, winter flask edition" (Bangla hook with steam over a flat mug,
both products slam in from the sides in the first second, split screen spec rows from the store listing and earlier
captions, "comment 1 or 2" vote scene, end card). Cocoa brown + sky blue + butter palette, original drive track in a new
key (7). About 18 s."""

import os as _os
_R = _os.path.dirname(_os.path.abspath(__file__)); _T = _os.path.dirname(_R)

import os, sys, math
from PIL import Image, ImageDraw
sys.path.insert(0, _T); sys.path.insert(0, _R)
from mega import T, TB, P, pill, bg, wipe, logo, rays, disc, put, rgba, f, ease, back, clamp, confetti, steam, HQ, DARK, WHITE, _tc
import reels9 as R9
from reels9 import end_card
import drive as DR

W, H = 1080, 1920
R9.OUT = _R + "/out/out1117/"; os.makedirs(R9.OUT, exist_ok=True)
COCOA = (62, 38, 32); COCOA2 = (88, 56, 46); SKY = (140, 200, 255); BUTTER = (255, 222, 120); CREAMY = (255, 244, 228)
A, B_ = "15.png", "18.png"   # Big Mac 316 thermos cup (blue), Premium thermal water bottle (white)


def mug(img, cx, cy):
    d = ImageDraw.Draw(img)
    d.rounded_rectangle((cx - 110, cy - 100, cx + 110, cy + 110), radius=28, fill=rgba(CREAMY))
    d.arc((cx + 70, cy - 55, cx + 170, cy + 45), -90, 90, fill=rgba(CREAMY), width=24)
    d.ellipse((cx - 96, cy - 114, cx + 96, cy - 80), fill=rgba((150, 95, 60)))


def p_hook(t, b, prev):
    img = bg(COCOA); rays(img, W / 2, 1250, t, SKY, a=14)
    put(img, TB("শীতে কোন ফ্লাস্কটা", 700, 104, WHITE, True), W / 2, 330, scale=1.3 - .3 * ease(t / .25), a=clamp(t / .12))
    kk = (t - .45) / .3
    if kk > 0: put(img, TB("নেবেন?", 700, 170, BUTTER, True), W / 2, 530, scale=1.3 - .3 * ease(kk), a=clamp(kk * 2))
    k = back(t / .4)
    put(img, P(A, 420, 640), W / 4 + 20 - (1 - min(1, k)) * 600, 1180, rot=(1 - ease(t / .4)) * 12)
    put(img, P(B_, 420, 640), 3 * W / 4 - 20 + (1 - min(1, k)) * 600, 1180, rot=-(1 - ease(t / .4)) * 12)
    vs = Image.new("RGBA", (190, 190), (0, 0, 0, 0)); ImageDraw.Draw(vs).ellipse((0, 0, 189, 189), fill=rgba(BUTTER))
    vt = T("VS", f("Poppins-Bold.ttf", 76), COCOA); vs.alpha_composite(vt, (95 - vt.width // 2, 95 - vt.height // 2))
    put(img, vs, W / 2, 1180, scale=back((t - .5) / .35), rot=8 * math.sin(t * 5))
    kk = back((t - 1.2) / .35)
    if kk > 0: put(img, pill("THIS or THAT?", 60, SKY, COCOA, padx=54), W / 2, 1640, scale=kk)
    logo(img); return img


ROWS = [("Price", "Tk 1,000", "Tk 800"), ("Capacity", "1000 ml", "600 ml"), ("Straw", "Yes", "Built in"),
        ("Handle", "Yes", "Side handle"), ("Lid", "Leak resistant", "Leak proof")]


def p_vs(t, b, prev):
    img = bg(COCOA); ImageDraw.Draw(img).rectangle((W / 2, 0, W, H), fill=rgba(SKY))
    k = ease(t / .4)
    disc(img, W / 4, 560, 230, COCOA2); disc(img, 3 * W / 4, 560, 230, (176, 218, 255))
    put(img, P(A, 330, 520), W / 4, 560 + 8 * math.sin(t * 3), a=k)
    put(img, P(B_, 330, 520), 3 * W / 4, 560 + 8 * math.sin(t * 3 + 1.5), a=k)
    n1 = pill("1", 64, BUTTER, COCOA, padx=40); n2 = pill("2", 64, COCOA, WHITE, padx=40)
    put(img, n1, 90, 250, scale=back(t / .35)); put(img, n2, W - 90, 250, scale=back(t / .35))
    put(img, T("Big Mac 316 Cup", f("Poppins-Bold.ttf", 46), WHITE), W / 4, 870, a=k)
    put(img, T("Thermal Bottle", f("Poppins-Bold.ttf", 46), COCOA), 3 * W / 4, 870, a=k)
    for i, (lab, a_, b_) in enumerate(ROWS):
        kk = ease((t - (1.5 + 1.8 * i) * b) / .3)
        if kk <= 0: continue
        y = 990 + i * 128
        ov = Image.new("RGBA", (W, 108), (0, 0, 0, 0))
        ImageDraw.Draw(ov).rounded_rectangle((50, 0, W - 50, 104), radius=52, fill=(255, 255, 255, int(245 * kk))); img.alpha_composite(ov, (0, y))
        put(img, T(a_, fit_font(a_, 40, 300), COCOA), 250, y + 52, a=kk)
        put(img, T(b_, fit_font(b_, 40, 300), (40, 110, 190)), W - 250, y + 52, a=kk)
        put(img, T(lab, f("Poppins-Medium.ttf", 28), (140, 120, 112)), W / 2, y + 52, a=kk)
    logo(img); return wipe(img, prev, t, COCOA)


def fit_font(text, size, maxw):
    while size > 20:
        ft = f("Poppins-Bold.ttf", size)
        if ft.getlength(text) <= maxw: return ft
        size -= 2
    return f("Poppins-Bold.ttf", size)


def p_vote(t, b, prev):
    img = bg(COCOA2); rays(img, W / 2, 900, t, BUTTER, a=16)
    mug(img, W / 2, 470); steam(img, W / 2, 350, t)
    put(img, TB("কমেন্টে লিখুন", 700, 96, WHITE, True), W / 2, 720, scale=back(t / .35))
    put(img, TB("১ না ২?", 700, 150, BUTTER, True), W / 2, 900, scale=back((t - .3) / .35))
    for i, (img_, num, col, tc) in enumerate([(A, "1", BUTTER, COCOA), (B_, "2", SKY, COCOA)]):
        cx = W / 4 + 40 + i * (W / 2 - 80); kk = back((t - .6 - i * .15) / .4)
        if kk <= 0: continue
        put(img, P(img_, 300, 440), cx, 1330 + 14 * math.sin(t * 4 + i * 2), scale=kk)
        put(img, pill(num, 56, col, tc, padx=36), cx, 1610, scale=kk)
    logo(img); return wipe(img, prev, t, COCOA2)


REELS = [
    dict(id="reel-winter-flask-this-or-that", time="18:30", music=("drive", 7), b=DR.B, cover=1900,
         scenes=[(p_hook, 6), (p_vs, 16), (p_vote, 8),
                 (end_card([(A, HQ), ("19.png", HQ), (B_, HQ)], COCOA, BUTTER, "Stay warm this winter"), 8)]),
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
