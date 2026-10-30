"""Everyday Cart vertical promo videos (1080x1920, 30fps) in the flat brand style."""
import os, sys, math, subprocess
from PIL import Image, ImageDraw, ImageFont, ImageFilter
D = os.path.dirname(os.path.abspath(__file__)) + "/"
sys.path.insert(0, D)
from render_flat import load_logo

OUT = "/mnt/user-data/outputs/everydaycart_videos/"; os.makedirs(OUT, exist_ok=True)
G = "/usr/share/fonts/truetype/google-fonts/"
W, H, FPS, T = 1080, 1920, 30, 0.3
SAGE = (98, 120, 92); SAGE_L = (220, 230, 214); ROSE = (165, 112, 111)
INK = (44, 46, 42); MUTE = (122, 116, 114); CREAM = (251, 246, 242)
SAGE_T = (232, 238, 229); ROSE_T = (246, 229, 227)
HQ = D + "cutouts/hq/"; FL = D + "cutouts/flat/"
_fc = {}
def f(n, s):
    k = (n, int(s))
    if k not in _fc: _fc[k] = ImageFont.truetype(G + n, int(s))
    return _fc[k]
def clamp(x): return max(0.0, min(1.0, x))
def ease(x): x = clamp(x); return 1 - (1 - x) ** 3
def back(x):
    x = clamp(x); c = 1.6; return 1 + (c + 1) * (x - 1) ** 3 + c * (x - 1) ** 2
def tk(n): return f"Tk {n:,}"
def fit(text, name, size, maxw):
    while size > 16 and f(name, size).getlength(text) > maxw: size -= 2
    return f(name, size)

LOGO_S = load_logo(130); LOGO_L = load_logo(240)
def logo_small(): return LOGO_S

class Frame:
    def __init__(self, bg, circles=()):
        self.img = Image.new("RGBA", (W, H), bg + (255,))
        d = ImageDraw.Draw(self.img)
        for (cx, cy, r, col) in circles: d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=col)
        self.ov = Image.new("RGBA", (W, H), (0, 0, 0, 0)); self.d = ImageDraw.Draw(self.ov)
    def flush(self):
        self.img.alpha_composite(self.ov); self.ov = Image.new("RGBA", (W, H), (0, 0, 0, 0)); self.d = ImageDraw.Draw(self.ov)
    def text_c(self, text, font, y, color, a=1.0, dy=0, cx=W / 2):
        if a <= 0: return
        w = font.getlength(text); self.d.text((cx - w / 2, y + dy), text, font=font, fill=color + (int(255 * a),))
    def sprite(self, spr, cx, cy, scale=1.0, a=1.0):
        if a <= 0 or scale <= 0.01: return
        self.flush()
        s = spr if abs(scale - 1) < 1e-3 else spr.resize((max(1, int(spr.width * scale)), max(1, int(spr.height * scale))), Image.BILINEAR)
        if a < 0.999:
            s = s.copy(); s.putalpha(s.split()[3].point(lambda v: int(v * a)))
        self.img.alpha_composite(s, (int(cx - s.width / 2), int(cy - s.height / 2)))
    def done(self):
        self.flush(); return self.img.convert("RGB")

def product_sprite(path, maxw, maxh):
    p = Image.open(path).convert("RGBA"); s = min(maxw / p.width, maxh / p.height)
    return p.resize((int(p.width * s), int(p.height * s)), Image.LANCZOS)

def shadow_sprite(w):
    L = Image.new("RGBA", (int(w + 120), 120), (0, 0, 0, 0))
    ImageDraw.Draw(L).ellipse((60, 40, 60 + w, 80), fill=(80, 50, 50, 110))
    return L.filter(ImageFilter.GaussianBlur(14))

def pill_sprite(text, font, fill, color, padx=44, h=None):
    w = int(font.getlength(text) + 2 * padx); h = h or int(font.size * 1.9)
    s = Image.new("RGBA", (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(s)
    d.rounded_rectangle((0, 0, w - 1, h - 1), radius=h // 2, fill=fill)
    d.text((padx, (h - font.size * 1.35) / 2), text, font=font, fill=color)
    return s

def circle_sprite(r, col):
    s = Image.new("RGBA", (2 * r + 2, 2 * r + 2), (0, 0, 0, 0)); ImageDraw.Draw(s).ellipse((1, 1, 2 * r, 2 * r), fill=col); return s

# ---------------- scenes ----------------
def intro_scene(lines, sub, pill, bg, deco):
    pf = f("Poppins-Bold.ttf", 46); pil = pill_sprite(pill, pf, ROSE if bg == SAGE else SAGE, (255, 255, 255))
    badge = Image.new("RGBA", (LOGO_S.width + 56, LOGO_S.height + 36), (0, 0, 0, 0))
    ImageDraw.Draw(badge).rounded_rectangle((0, 0, badge.width - 1, badge.height - 1), radius=30, fill=CREAM)
    badge.alpha_composite(LOGO_S, (28, 18))
    def fn(t):
        drift = 18 * math.sin(t * 1.4)
        fr = Frame(bg, [(900, 380 + drift, 230, deco[0]), (160, 1500 - drift, 260, deco[1])])
        fr.sprite(badge, W / 2, 300, back(t / 0.5), ease(t / 0.3))
        y = 640
        for i, ln in enumerate(lines):
            p = ease((t - 0.15 - 0.15 * i) / 0.45)
            fr.text_c(ln, f("Poppins-Bold.ttf", 150), y, (255, 255, 255), p, 60 * (1 - p)); y += 170
        p = ease((t - 0.6) / 0.4); fr.text_c(sub, fit(sub, "Poppins-Medium.ttf", 46, 940), y + 30, SAGE_L if bg == SAGE else (255, 236, 232), p, 30 * (1 - p))
        fr.sprite(pil, W / 2, y + 190, back((t - 0.85) / 0.45), ease((t - 0.85) / 0.2))
        return fr.done()
    return fn

def product_scene(p, accent):
    spr = product_sprite(p["img"], 640, 600); sh = shadow_sprite(spr.width * 0.8)
    circ = circle_sprite(370, (255, 255, 255))
    tagf = f("Poppins-Medium.ttf", 32); tag = pill_sprite(p["tag"], tagf, SAGE, (255, 255, 255), padx=30)
    pricef = f("Poppins-Bold.ttf", 64); price = pill_sprite(tk(p["price"]), pricef, ROSE, (255, 255, 255), padx=48)
    namef = fit(p["name"], "Poppins-Bold.ttf", 76, 960); linef = fit(p["line"], "Poppins-Regular.ttf", 38, 960)
    oldf = f("Poppins-Regular.ttf", 44)
    def fn(t):
        drift = 14 * math.sin(t * 1.6)
        fr = Frame(CREAM, [(940, 300 + drift, 200, accent), (120, 1650 - drift, 220, SAGE_T)])
        fr.sprite(LOGO_S, 60 + LOGO_S.width / 2, 150 + LOGO_S.height / 2)
        fr.sprite(tag, W - 60 - tag.width / 2, 170, 1, ease(t / 0.3))
        fr.sprite(circ, W / 2, 790, ease(t / 0.45))
        pp = ease((t - 0.1) / 0.5)
        fr.sprite(sh, W / 2, 790 + spr.height / 2 + 6, 0.8 + 0.2 * pp, pp)
        fr.sprite(spr, W / 2, 790 + 50 * (1 - pp), (0.82 + 0.18 * pp) * (1 + 0.015 * math.sin(t * 2.2)), pp)
        a = ease((t - 0.4) / 0.4); fr.text_c(p["name"], namef, 1230, INK, a, 40 * (1 - a))
        a = ease((t - 0.55) / 0.4); fr.text_c(p["line"], linef, 1335, MUTE, a, 30 * (1 - a))
        a = back((t - 0.75) / 0.45)
        has_old = p["regular"] > p["price"]
        ow = oldf.getlength(tk(p["regular"])) if has_old else 0
        tot = price.width + (28 + ow if has_old else 0); x0 = W / 2 - tot / 2
        fr.sprite(price, x0 + price.width / 2, 1470, a, ease((t - 0.75) / 0.2))
        if has_old:
            oa = ease((t - 0.95) / 0.3); ox = x0 + price.width + 28
            fr.d.text((ox, 1442), tk(p["regular"]), font=oldf, fill=MUTE + (int(255 * oa),))
            fr.d.line((ox, 1470, ox + ow * ease((t - 1.05) / 0.3), 1470), fill=MUTE + (int(255 * oa),), width=4)
        return fr.done()
    return fn

def end_scene(lines=("Order now",), btn="Inbox us to order"):
    bf = f("Poppins-Bold.ttf", 50); b = pill_sprite(btn, bf, SAGE, (255, 255, 255), padx=60, h=120)
    def fn(t):
        drift = 16 * math.sin(t * 1.4)
        fr = Frame(CREAM, [(920, 330 + drift, 220, ROSE_T), (150, 1560 - drift, 250, SAGE_T)])
        fr.sprite(LOGO_L, W / 2, 600, back(t / 0.55), ease(t / 0.3))
        a = ease((t - 0.3) / 0.4); fr.text_c(lines[0], f("Poppins-Bold.ttf", 104), 860, INK, a, 40 * (1 - a))
        a = ease((t - 0.5) / 0.4); fr.text_c("everydaycart.online", f("Poppins-Medium.ttf", 52), 1010, SAGE, a, 30 * (1 - a))
        pulse = 1 + 0.035 * math.sin(max(0, t - 1.0) * 5) if t > 1.0 else back((t - 0.7) / 0.4)
        fr.sprite(b, W / 2, 1190, pulse, ease((t - 0.7) / 0.2))
        a = ease((t - 1.0) / 0.4); fr.text_c("Limited stock  •  Official products", f("Poppins-Medium.ttf", 38), 1320, MUTE, a)
        return fr.done()
    return fn

# single product story
def hero_scene(p, accent):
    spr = product_sprite(p["img"], 760, 740); sh = shadow_sprite(spr.width * 0.8); circ = circle_sprite(440, (255, 255, 255))
    tag = pill_sprite(p["tag"], f("Poppins-Medium.ttf", 34), SAGE, (255, 255, 255), padx=32)
    namef = fit(p["name"], "Poppins-Bold.ttf", 92, 980)
    def fn(t):
        drift = 14 * math.sin(t * 1.6)
        fr = Frame(CREAM, [(930, 280 + drift, 210, accent), (130, 1680 - drift, 230, SAGE_T)])
        fr.sprite(LOGO_S, 60 + LOGO_S.width / 2, 150 + LOGO_S.height / 2)
        fr.sprite(circ, W / 2, 820, ease(t / 0.5))
        pp = ease((t - 0.15) / 0.7)
        fr.sprite(sh, W / 2, 820 + spr.height / 2 + 6, 0.7 + 0.3 * pp, pp)
        fr.sprite(spr, W / 2, 820 + 80 * (1 - pp), (0.7 + 0.3 * pp) * (1 + 0.02 * math.sin(t * 2)), pp)
        fr.sprite(tag, W / 2, 1350, back((t - 0.7) / 0.4), ease((t - 0.7) / 0.2))
        a = ease((t - 0.9) / 0.45); fr.text_c(p["name"], namef, 1420, INK, a, 40 * (1 - a))
        a = ease((t - 1.15) / 0.45); fr.text_c(p["line"], fit(p["line"], "Poppins-Regular.ttf", 40, 960), 1540, MUTE, a, 30 * (1 - a))
        return fr.done()
    return fn

def features_scene(p, accent):
    spr = product_sprite(p["img"], 520, 500); circ = circle_sprite(300, (255, 255, 255))
    ff = f("Poppins-Medium.ttf", 52)
    def fn(t):
        drift = 14 * math.sin(t * 1.6)
        fr = Frame(CREAM, [(930, 280 + drift, 210, accent), (130, 1680 - drift, 230, SAGE_T)])
        fr.sprite(LOGO_S, 60 + LOGO_S.width / 2, 150 + LOGO_S.height / 2)
        fr.sprite(circ, W / 2, 620); fr.sprite(spr, W / 2, 620, 1 + 0.015 * math.sin(t * 2))
        fr.text_c("Why you'll love it", f("Poppins-Bold.ttf", 64), 980, INK, ease(t / 0.4))
        y = 1110
        for i, ft in enumerate(p["feats"]):
            a = ease((t - 0.4 - 0.45 * i) / 0.4); x = 170 + 60 * (1 - a)
            if a > 0:
                cx, cy, r = x + 26, y + 34, 26
                fr.d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=SAGE + (int(255 * a),))
                fr.d.line([(cx - 11, cy + 1), (cx - 3, cy + 10), (cx + 13, cy - 9)], fill=(255, 255, 255, int(255 * a)), width=6, joint="curve")
                fr.d.text((x + 76, y), ft, font=ff, fill=INK + (int(255 * a),))
            y += 110
        return fr.done()
    return fn

def price_scene(p, accent):
    spr = product_sprite(p["img"], 560, 540); circ = circle_sprite(320, (255, 255, 255))
    pf = f("Poppins-Bold.ttf", 120); price = pill_sprite(tk(p["price"]), pf, ROSE, (255, 255, 255), padx=70, h=190)
    btn = pill_sprite("Order at everydaycart.online", f("Poppins-Bold.ttf", 44), SAGE, (255, 255, 255), padx=50, h=110)
    def fn(t):
        drift = 14 * math.sin(t * 1.6)
        fr = Frame(CREAM, [(930, 280 + drift, 210, accent), (130, 1680 - drift, 230, SAGE_T)])
        fr.sprite(LOGO_S, 60 + LOGO_S.width / 2, 150 + LOGO_S.height / 2)
        fr.sprite(circ, W / 2, 650); fr.sprite(spr, W / 2, 650, 1 + 0.015 * math.sin(t * 2))
        fr.text_c("Special price", f("Poppins-Medium.ttf", 52), 1000, MUTE, ease(t / 0.4))
        fr.sprite(price, W / 2, 1215, back((t - 0.25) / 0.5), ease((t - 0.25) / 0.2))
        if p["regular"] > p["price"]:
            of = f("Poppins-Regular.ttf", 54); o = "Regular " + tk(p["regular"]); a = ease((t - 0.7) / 0.4)
            fr.text_c(o, of, 1340, MUTE, a)
            w = of.getlength(o); x0 = W / 2 - w / 2 + of.getlength("Regular ")
            fr.d.line((x0, 1374, x0 + (w - of.getlength("Regular ")) * ease((t - 0.9) / 0.35), 1374), fill=MUTE + (int(255 * a),), width=5)
        pulse = 1 + 0.03 * math.sin(max(0, t - 1.3) * 5) if t > 1.3 else back((t - 0.95) / 0.4)
        fr.sprite(btn, W / 2, 1500, pulse, ease((t - 0.95) / 0.2))
        return fr.done()
    return fn

def render(name, scenes):
    starts = []; s = 0.0
    for dur, _ in scenes: starts.append(s); s += dur - T
    total = s + T
    n = int(round(total * FPS))
    path = OUT + name + ".mp4"
    cmd = ["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
           "-c:v", "libx264", "-preset", "veryfast", "-crf", "19", "-pix_fmt", "yuv420p", "-movflags", "+faststart", path]
    pr = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    for k in range(n):
        g = k / FPS
        act = [(i, g - starts[i]) for i, (dur, _) in enumerate(scenes) if starts[i] <= g < starts[i] + dur]
        if not act: act = [(len(scenes) - 1, scenes[-1][0] - 1 / FPS)]
        if len(act) == 1:
            fr = scenes[act[0][0]][1](act[0][1])
        else:
            a = clamp(act[1][1] / T)
            fr = Image.blend(scenes[act[0][0]][1](act[0][1]), scenes[act[1][0]][1](act[1][1]), a)
        pr.stdin.write(fr.tobytes())
    pr.stdin.close(); pr.wait()
    print(path, f"{total:.1f}s", flush=True)

GADGETS = [
    dict(img=HQ + "02.png", tag="SMART WATCH", name="Oraimo Watch 5 Lite", line="2.01\" HD  •  Bluetooth Calling  •  IP68", price=1650, regular=1870),
    dict(img=HQ + "12.png", tag="EARBUDS", name="Oraimo SpaceBuds Neo+", line="Sound360 Audio  •  30 Hrs Battery", price=1940, regular=2189),
    dict(img=HQ + "13.png", tag="EARBUDS", name="Oraimo SpaceBuds Lite", line="AI Call ENC  •  40 Hrs with Case", price=1310, regular=1496),
    dict(img=HQ + "04.png", tag="NECKBAND", name="Oraimo Necklace Lite", line="30 Hrs Playtime  •  Dual Device", price=1300, regular=1485),
    dict(img=HQ + "10.png", tag="EARBUDS", name="Awei T108 Earbuds", line="13mm Drivers  •  ENC Calls", price=950, regular=1199),
]
BABY = [
    dict(img=FL + "kodomo_lotion.png", tag="BABY CARE", name="Kodomo Baby Lotion Powder", line="180 ml  •  Extra Mild  •  0+ Months", price=720, regular=880),
    dict(img=FL + "kodomo_paste.png", tag="BABY CARE", name="Kodomo Baby Toothpaste", line="Orange Flavour  •  Fluoride 1000 ppm", price=280, regular=400),
    dict(img=FL + "kodomo_brush.png", tag="BABY CARE", name="Kodomo Baby Toothbrush", line="Extra Soft  •  6 Months to 3 Years", price=200, regular=400),
    dict(img=HQ + "21.png", tag="BABY CARE", name="10 Pc Baby Care Kit", line="Nail Care  •  Hair Care  •  Thermometer", price=480, regular=650),
]
WATCH = dict(img=HQ + "02.png", tag="OFFICIAL ORAIMO", name="Oraimo Watch 5 Lite", line="Smart Watch with Bluetooth Calling",
             feats=["2.01\" HD Display", "HD Voice Calling", "IP68 Water Resistant", "7 Day Battery"], price=1650, regular=1870)

if __name__ == "__main__":
    which = sys.argv[1:] or ["1", "2", "3"]
    if "1" in which:
        render("01_gadget_deals_reel", [(2.4, intro_scene(["Gadget", "Deals"], "Official Oraimo & Awei", "Save up to 20%", SAGE, ((122, 142, 115), (122, 142, 115))))]
               + [(2.1, product_scene(p, ROSE_T if i % 2 else SAGE_T)) for i, p in enumerate(GADGETS)] + [(2.8, end_scene())])
    if "2" in which:
        render("02_oraimo_watch_5_lite_reel", [(3.0, hero_scene(WATCH, SAGE_T)), (3.4, features_scene(WATCH, SAGE_T)), (3.2, price_scene(WATCH, SAGE_T))])
    if "3" in which:
        render("03_baby_care_reel", [(2.4, intro_scene(["Baby Care", "Essentials"], "Gentle picks for your little one", "From Tk 200", ROSE, ((182, 132, 131), (182, 132, 131))))]
               + [(2.1, product_scene(p, ROSE_T if i % 2 == 0 else SAGE_T)) for i, p in enumerate(BABY)] + [(2.8, end_scene())])
