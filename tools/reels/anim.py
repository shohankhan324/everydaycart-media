"""Animated Reels for review (4 Nov): day story, cart fill, product drop, Bangla winter."""
import os, sys, math, subprocess
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
sys.path.insert(0, "/home/claude/everydaycart-media/tools"); sys.path.insert(0, "/home/claude/viral")
from mega import T, TB, P, pill, bn_pill, bg, wipe, logo, rays, disc, confetti, steam, put, rgba, f, ease, back, clamp, HQ, FL, DARK, WHITE, YEL, CORAL, BLUE, PURP, GREEN, ORANGE, _tc
from reels9 import end_card, encode, bn_num, LOGO_BIG
import drive as DR
import make_music as MM
from scipy.io import wavfile

W, H, FPS = 1080, 1920, 30
OUT = "/home/claude/viral/anim/"; os.makedirs(OUT, exist_ok=True)
def lerp(a, b, k): return tuple(int(x + (y - x) * k) for x, y in zip(a, b))

# ======================================================= A. A day with Everyday Cart
DAY = [("7:00 AM", "Morning tea", "Big Mac 316 Thermos Cup", "15.png", 1000, (255, 200, 150), (255, 236, 200), 0.10),
       ("9:00 AM", "Music on the way", "Awei T108 Earbuds", "10.png", 950, (140, 200, 255), (210, 236, 255), 0.30),
       ("1:00 PM", "Hot lunch at work", "Insulated Lunch Box", "26.png", 3000, (90, 170, 240), (190, 226, 255), 0.50),
       ("6:00 PM", "Evening walk", "COLMI P81 Smartwatch", "09.png", 1350, (250, 140, 100), (255, 196, 150), 0.80),
       ("11:00 PM", "Peaceful sleep", "Silent Alarm Clock", "07.png", 500, (24, 30, 70), (50, 60, 120), 1.00)]
SKY = [(rng := np.random.default_rng(3)).uniform(0, W, 50), rng.uniform(0, 900, 50)]
def skyline(img, night):
    d = ImageDraw.Draw(img); rng = np.random.default_rng(7); x = -20; base = 1920
    while x < W:
        w = int(rng.uniform(90, 170)); h = int(rng.uniform(260, 620)); col = (40, 46, 80) if night else (70, 90, 120)
        d.rectangle((x, base - h, x + w, base), fill=rgba(col))
        for wy in range(base - h + 30, base - 40, 56):
            for wx in range(x + 18, x + w - 24, 40):
                if rng.random() < (0.55 if night else 0.25): d.rectangle((wx, wy, wx + 18, wy + 26), fill=rgba((255, 214, 120) if night else (170, 200, 230)))
        x += w + 8
def day_scene(i):
    tm, line, name, im, pr, top, bot, k = DAY[i]
    def fn(t, b, prev):
        night = i == 4
        img = Image.new("RGBA", (W, H)); arr = np.zeros((H, W, 4), np.uint8)
        for c in range(3): arr[..., c] = np.linspace(top[c], bot[c], H)[:, None]
        arr[..., 3] = 255; img = Image.fromarray(arr, "RGBA"); d = ImageDraw.Draw(img)
        if night:
            for x, y in zip(*SKY): r = 2 + (int(x) % 3); a = int(160 + 90 * math.sin(t * 3 + x)); d.ellipse((x - r, y - r, x + r, y + r), fill=(255, 255, 255, a))
        kk = k + 0.08 * min(1, t / 3)                      # sun / moon travels across the sky
        ang = math.pi * (1 - kk); sx, sy = W / 2 + 430 * math.cos(ang), 820 - 560 * math.sin(ang)
        disc(img, sx, sy, 80, (255, 245, 210) if night else (255, 214, 90))
        if night: disc(img, sx + 34, sy - 22, 70, top)
        skyline(img, night)
        put(img, pill(tm, 64, WHITE, DARK if not night else (24, 30, 70), padx=46), W / 2, 260, scale=back(t / .35))
        put(img, T(line, f("Poppins-Bold.ttf", 82), WHITE, True), W / 2, 400, a=clamp((t - .15) / .3))
        cd = Image.new("RGBA", (640, 640), (0, 0, 0, 0)); ImageDraw.Draw(cd).ellipse((0, 0, 639, 639), fill=(255, 255, 255, 235))
        put(img, cd, W / 2, 900, scale=back((t - .1) / .4))
        put(img, P(im, 470, 470), W / 2, 900 + 10 * math.sin(t * 3), scale=back((t - .25) / .4))
        if i == 0 and t > .4: steam(img, W / 2 - 20, 650, t)
        kk2 = ease((t - .5) / .35)
        put(img, T(name, f("Poppins-Bold.ttf", 60), WHITE, True), W / 2, 1290 + 30 * (1 - kk2), a=kk2)
        put(img, pill(f"Tk {pr:,}", 64, YEL, DARK, padx=46), W / 2, 1410, scale=back((t - .7) / .35))
        logo(img)
        return wipe(img, prev, t, top, W / 2, 900)
    return fn
def day_hook(t, b, prev):
    img = bg((255, 214, 170)); disc(img, W / 2, 1300, 260 + 20 * math.sin(t * 2), (255, 190, 90))
    for i, wd in enumerate(["A DAY", "WITH"]):
        kk = (t - i * b) / .2
        if kk > 0: put(img, T(wd, f("Poppins-Bold.ttf", 150), DARK), W / 2, 520 + i * 180, scale=1.4 - .4 * ease(kk), a=clamp(kk * 2))
    put(img, LOGO_BIG, W / 2, 940, scale=back((t - 2 * b) / .4))
    logo(img); return img

# ======================================================= B. Fill the cart
CART = [("20.png", "Minitree Mumpot", 400), ("10.png", "Awei T108", 950), ("07.png", "Silent Alarm Clock", 500),
        ("25.png", "Elephant Plush", 750), ("23.png", "Auto Umbrella", 900), ("29.png", "Cleaning Gloves", 200)]
def draw_cart(img, cx, cy, s=1.0, col=(255, 255, 255)):
    d = ImageDraw.Draw(img); c = rgba(col)
    d.line([(cx - 330 * s, cy - 230 * s), (cx - 250 * s, cy - 230 * s), (cx - 170 * s, cy + 110 * s), (cx + 250 * s, cy + 110 * s)], fill=c, width=int(22 * s), joint="curve")
    d.polygon([(cx - 230 * s, cy - 150 * s), (cx + 330 * s, cy - 150 * s), (cx + 270 * s, cy + 60 * s), (cx - 180 * s, cy + 60 * s)], outline=c, width=int(20 * s))
    for wx in (-130, 200): d.ellipse((cx + (wx - 38) * s, cy + 150 * s, cx + (wx + 38) * s, cy + 226 * s), fill=c)
def cart_scene(t, b, prev):
    img = bg(GREEN); rays(img, W / 2, 1300, t, WHITE, a=16)
    roll = ease(t / .6); cx = -400 + (W / 2 + 400) * roll; cy = 1350
    put(img, T("FILL YOUR CART", f("Poppins-Bold.ttf", 104), WHITE, True), W / 2, 230, scale=1.3 - .3 * ease(t / .3))
    total = 0; inside = []
    for i, (im, name, pr) in enumerate(CART):
        st = (2 + 2 * i) * b; k = (t - st) / (1.2 * b)
        if k <= 0: continue
        if k < 1:   # fly in on an arc
            sx, sy = (180 if i % 2 == 0 else W - 180), 560
            ex, ey = cx + (-120 + (i % 3) * 120), cy - 250
            x = sx + (ex - sx) * ease(k); y = sy + (ey - sy) * k - 380 * math.sin(math.pi * k)
            put(img, P(im, 300, 300), x, y, scale=1 - .35 * k, rot=360 * k * (1 if i % 2 else -1))
            put(img, T(name, f("Poppins-Bold.ttf", 54), WHITE, True), W / 2, 420, a=1 - abs(2 * k - 1) * 0.2)
        else:
            total += pr; inside.append(i)
            kk = (t - st - 1.2 * b) / .6
            if kk < 1: put(img, T(f"+ Tk {pr:,}", f("Poppins-Bold.ttf", 70), YEL, True), cx + 260, cy - 420 - 120 * kk, a=1 - kk)
    for j in inside[-6:]:
        im = CART[j][0]; put(img, P(im, 190, 190), cx + (-150 + (j % 3) * 150), cy - 230 - (j // 3) * 70)
    draw_cart(img, cx, cy, 1.0)
    card = Image.new("RGBA", (640, 150), (0, 0, 0, 0)); ImageDraw.Draw(card).rounded_rectangle((0, 0, 639, 149), radius=75, fill=rgba(WHITE))
    card.alpha_composite(T(f"Cart total  Tk {total:,}", f("Poppins-Bold.ttf", 54), GREEN), (60, 34))
    put(img, card, W / 2, 1720, a=clamp((t - 2 * b) / .3))
    logo(img); return wipe(img, prev, t, GREEN)

# ======================================================= C. Product drop
DROP = ["12.png", "02.png", "14.png", "06.png", "15.png", "21.png", "01.png", "05.png", "03.png", "26.png", "25.png", "09.png", "24.png", "19.png"]
rngd = np.random.default_rng(21)
DROPS = [(im, rngd.uniform(170, W - 170), rngd.uniform(-20, 20), 0.18 * i, rngd.uniform(-1, 1)) for i, im in enumerate(DROP)]
def drop_scene(t, b, prev):
    img = bg((255, 236, 210))
    put(img, T("EVERYTHING", f("Poppins-Bold.ttf", 130), DARK), W / 2, 330, scale=1.3 - .3 * ease(t / .3))
    put(img, T("you need.", f("Poppins-Bold.ttf", 110), CORAL), W / 2, 470, a=clamp((t - b) / .3))
    floor_by_col = {}
    order = sorted(range(len(DROPS)), key=lambda j: DROPS[j][3])
    for j in order:
        im, x, rot0, st, spin = DROPS[j]
        lt = t - st - .3
        if lt <= 0: continue
        col = int(x // 220); fl = floor_by_col.get(col, 1780)
        g = 4200; y0 = -200; y = y0 + .5 * g * lt * lt
        if y >= fl - 120:   # landed: settle with a small bounce
            tl = lt - math.sqrt(2 * (fl - 120 - y0) / g)
            y = fl - 120 - 60 * abs(math.sin(tl * 9)) * math.exp(-tl * 6)
        put(img, P(im, 250, 250), x, y, rot=rot0 + spin * 30 * max(0, 1 - lt))
        floor_by_col[col] = fl - 150
    kk = back((t - 9 * b) / .4)
    if kk > 0: put(img, pill("One cart. Everyday Cart.", 60, DARK, WHITE, padx=50), W / 2, 620, scale=kk)
    logo(img); return wipe(img, prev, t, (255, 236, 210))

# ======================================================= D. শীত আসছে (winter is coming)
SNOW = [(np.random.default_rng(i).uniform(0, W), np.random.default_rng(i + 99).uniform(0, H), 3 + i % 6) for i in range(90)]
def snow(img, t):
    d = ImageDraw.Draw(img)
    for x, y0, r in SNOW:
        y = (y0 + t * (60 + r * 30)) % H; xx = x + 25 * math.sin(t + y0)
        d.ellipse((xx - r, y - r, xx + r, y + r), fill=(255, 255, 255, 220))
WINTER = [("16.png", "Premium Thermal Tumbler", 800), ("15.png", "Big Mac 316 Thermos Cup", 1000), ("26.png", "Insulated Lunch Box", 3000), ("27.png", "Portable BBQ Grill", 5500)]
def winter_hook(t, b, prev):
    img = bg((30, 60, 110)); snow(img, t)
    put(img, TB("শীত আসছে", 700, 190, WHITE, True), W / 2, 760, scale=1.3 - .3 * ease(t / .5), a=clamp(t / .3))
    kk = ease((t - 1.5 * b) / .5)
    if kk > 0: put(img, TB("প্রস্তুত তো?", 600, 110, (180, 220, 255)), W / 2, 960 + 30 * (1 - kk), a=kk)
    logo(img); return img
def winter_item(i):
    im, name, pr = WINTER[i]; cols = [(40, 80, 140), (60, 50, 120), (20, 100, 120), (110, 50, 40)]
    def fn(t, b, prev):
        col = cols[i]; img = bg(col); snow(img, t + i * 3)
        disc(img, W / 2, 920, 340, tuple(min(255, c + 30) for c in col))
        put(img, P(im, 520, 560), W / 2, 920 + 10 * math.sin(t * 2.5), scale=back(t / .4))
        if i < 2 and t > .3: steam(img, W / 2 - 20, 620, t)
        kk = ease((t - .3) / .35)
        put(img, T(name, f("Poppins-Bold.ttf", 70), WHITE, True), W / 2, 1380 + 30 * (1 - kk), a=kk)
        put(img, bn_price_pill(f"মাত্র {bn_num(pr)} টাকা"), W / 2, 1530, scale=back((t - .5) / .35))
        put(img, TB(["গরম চা সারাদিন", "শীতের সকালে গরম কফি", "অফিসে গরম খাবার", "শীতের রাতে বারবিকিউ"][i], 700, 80, WHITE, True), W / 2, 330, a=clamp(t / .3))
        logo(img); return wipe(img, prev, t, col)
    return fn

def bn_price_pill(text):
    k = ("bnpp", text)
    if k not in _tc:
        tx = TB(text, 700, 62, DARK); w, h = tx.width + 60, 118
        p_ = Image.new("RGBA", (w, h), (0, 0, 0, 0)); ImageDraw.Draw(p_).rounded_rectangle((0, 0, w - 1, h - 1), radius=59, fill=rgba(YEL))
        p_.alpha_composite(tx, (30, (h - tx.height) // 2)); _tc[k] = p_
    return _tc[k]

# ======================================================= table + render
G = 60 / 92; U = 60 / 116
REELS = [
    dict(id="a-day-with-everyday-cart", music=("upbeat", 2), b=U, scenes=[(day_hook, 4)] + [(day_scene(i), 6) for i in range(5)] + [(end_card([(d[3], HQ) for d in DAY], (40, 50, 90), YEL, "Everyday Cart, all day"), 7)]),
    dict(id="fill-your-cart", music=("drive", 4), b=DR.B, scenes=[(cart_scene, 16), (end_card([(c[0], HQ) for c in CART[:5]], (10, 120, 85), YEL, "Add to cart today"), 7)]),
    dict(id="everything-you-need", music=("drive", 9), b=DR.B, scenes=[(drop_scene, 14), (end_card([("12.png", HQ), ("14.png", HQ), ("06.png", HQ), ("26.png", HQ), ("21.png", HQ)], (60, 40, 40), CORAL, "Everything you need"), 7)]),
    dict(id="sheet-ashchhe-winter", music=("gentle", 2), b=G, scenes=[(winter_hook, 5)] + [(winter_item(i), 5) for i in range(4)] + [(end_card([(w[0], HQ) for w in WINTER], (30, 60, 110), (180, 220, 255), "Get winter ready"), 5)]),
]

def build(r, preview=False):
    b = r["b"]; prev = DARK; parts = []; s = 0; starts = []
    for fn, beats in r["scenes"]:
        dur = beats * b; pv = prev
        parts.append(((lambda fn, pv: (lambda t: fn(t, b, pv)))(fn, pv), dur)); starts.append(s); s += dur
        prev = tuple(fn(min(dur - .05, 1.0), b, pv).getpixel((5, H - 5))[:3])
    if preview: return parts
    d = OUT + r["id"] + "/"; os.makedirs(d, exist_ok=True)
    for k, (fn, dur) in enumerate(parts): encode(d + f"s{k}.mp4", fn, dur)
    open(d + "list.txt", "w").write("".join(f"file 's{k}.mp4'\n" for k in range(len(parts))))
    kind, key = r["music"]
    mix = DR.drive(s, starts[1], starts[1:], starts[-1], key=key) if kind == "drive" else (MM.upbeat(s, key) if kind == "upbeat" else MM.gentle(s, key))
    wavfile.write(d + "music.wav", 44100, (np.stack([mix, mix], 1) * 32767).astype(np.int16))
    out = OUT + r["id"] + ".mp4"
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", d + "list.txt", "-i", d + "music.wav", "-map", "0:v", "-map", "1:a",
                    "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-shortest", "-movflags", "+faststart", out], check=True)
    print(out, round(s, 1), flush=True)

if __name__ == "__main__":
    mode = sys.argv[1]; ids = sys.argv[2:]
    sel = [r for r in REELS if not ids or r["id"] in ids]
    if mode == "preview":
        shots = []
        for r in sel:
            for fn, dur in build(r, True): shots.append(fn(min(dur * .7, dur - .1)).convert("RGB"))
        cols = 8; rows = math.ceil(len(shots) / cols); sh = Image.new("RGB", (cols * 216, rows * 384))
        for i, s_ in enumerate(shots): sh.paste(s_.resize((216, 384), Image.LANCZOS), ((i % cols) * 216, (i // cols) * 384))
        sh.save("/tmp/anim_sheet.jpg", quality=86)
    else:
        for r in sel: build(r)
