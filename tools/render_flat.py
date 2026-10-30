"""Everyday Cart flat post templates (no 3D): A split panel, B colour card, C collection grid. Rendered at 2x."""
import os, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from scipy import ndimage

D = os.path.dirname(os.path.abspath(__file__)) + "/"
LOGO = os.path.dirname(os.path.abspath(__file__)) + "/assets/logo.png"
OUTDIR = "/mnt/user-data/outputs/everydaycart_posts_oct30/"
os.makedirs(OUTDIR, exist_ok=True)
G = "/usr/share/fonts/truetype/google-fonts/"
S = 2
W0, H0 = 1080, 1350
W, H = W0 * S, H0 * S
SAGE = (98, 120, 92); SAGE_L = (220, 230, 214); ROSE = (165, 112, 111)
INK = (44, 46, 42); MUTE = (122, 116, 114); CREAM = (251, 246, 242)

def f(n, s): return ImageFont.truetype(G + n, int(round(s * S)))
def P(*v): return tuple(int(round(x * S)) for x in v)
def tk(n): return f"Tk {n:,}"

def load_logo(width):
    lg = Image.open(LOGO).convert("RGB"); a = np.asarray(lg).astype(int)
    cream = (np.abs(a - np.array([253, 250, 245])).max(axis=2) <= 12)
    lab, _ = ndimage.label(cream)
    b = set(np.unique(np.concatenate([lab[0], lab[-1], lab[:, 0], lab[:, -1]]))) - {0}
    al = Image.fromarray(((~np.isin(lab, list(b))) * 255).astype("uint8")).filter(ImageFilter.GaussianBlur(0.7))
    lg = lg.convert("RGBA"); lg.putalpha(al); lg = lg.crop(lg.getbbox())
    w = int(width * S); return lg.resize((w, int(lg.height * w / lg.width)), Image.LANCZOS)

def fit(d, text, name, size, maxw):
    while size > 14:
        ft = f(name, size)
        if d.textlength(text, font=ft) <= maxw * S: return ft
        size -= 1
    return f(name, size)

def wrap(d, text, name, size, maxw, max_lines=3):
    """Wrap text to maxw, shrinking font until it fits in max_lines."""
    while size > 20:
        ft = f(name, size); words = text.split(); lines = [""]
        for w_ in words:
            t = (lines[-1] + " " + w_).strip()
            if d.textlength(t, font=ft) <= maxw * S: lines[-1] = t
            else: lines.append(w_)
        if len(lines) <= max_lines and all(d.textlength(l, font=ft) <= maxw * S for l in lines): return ft, lines
        size -= 2
    return ft, lines

def shadow(img, box, alpha=70, blur=14, color=(60, 40, 40)):
    L = Image.new("RGBA", img.size, (0, 0, 0, 0)); ImageDraw.Draw(L).ellipse(P(*box), fill=color + (alpha,))
    return Image.alpha_composite(img, L.filter(ImageFilter.GaussianBlur(blur * S)))

def card_shadow(img, box, r, alpha=40, blur=18, dy=10):
    L = Image.new("RGBA", img.size, (0, 0, 0, 0))
    x0, y0, x1, y1 = box
    ImageDraw.Draw(L).rounded_rectangle(P(x0, y0 + dy, x1, y1 + dy), radius=r * S, fill=(80, 60, 60, alpha))
    return Image.alpha_composite(img, L.filter(ImageFilter.GaussianBlur(blur * S)))

def place(img, prod, cx, cy, maxw, maxh, floor=True):
    s = min(maxw * S / prod.width, maxh * S / prod.height)
    pr = prod.resize((max(1, int(prod.width * s)), max(1, int(prod.height * s))), Image.LANCZOS)
    x = int(cx * S - pr.width / 2); y = int(cy * S - pr.height / 2)
    if floor:
        bw = pr.width / S
        img = shadow(img, (cx - bw * 0.42, cy + pr.height / S / 2 - 16, cx + bw * 0.42, cy + pr.height / S / 2 + 18), alpha=80, blur=12)
    img.alpha_composite(pr, (x, y)); return img

def check_icon(d, x, y, r, bg, fg):
    d.ellipse(P(x - r, y - r, x + r, y + r), fill=bg)
    d.line([P(x - r * 0.45, y + r * 0.02), P(x - r * 0.1, y + r * 0.38), P(x + r * 0.5, y - r * 0.35)], fill=fg, width=int(r * 0.32 * S), joint="curve")

def tag_pill(d, x1, y, text, fill, color, outline=None):
    pf = f("Poppins-Medium.ttf", 22); tw = d.textlength(text, font=pf) / S
    x0 = x1 - tw - 40
    d.rounded_rectangle(P(x0, y, x1, y + 46), radius=23 * S, fill=fill, outline=outline, width=2 * S if outline else 0)
    d.text(P(x0 + 20, y + 8), text, font=pf, fill=color)
    return x0

def finish(img, name):
    out = img.convert("RGB").resize((W0, H0), Image.LANCZOS).filter(ImageFilter.UnsharpMask(radius=1.0, percent=30, threshold=2))
    path = OUTDIR + name + ".jpg"; out.save(path, quality=95, subsampling=0); print(path, flush=True); return path

# ---------------- Template A: split panel ----------------
def template_a(p):
    img = Image.new("RGBA", (W, H), CREAM + (255,)); d = ImageDraw.Draw(img)
    LW = 440
    d.rectangle(P(0, 0, LW, H0), fill=SAGE)
    # soft accent circle + thin ring on the product side
    acc = p.get("accent", (238, 226, 220))
    cx, cy = (LW + W0) / 2, 640
    d.ellipse(P(cx - 270, cy - 270, cx + 270, cy + 270), fill=acc)
    d.ellipse(P(cx - 302, cy - 302, cx + 302, cy + 302), outline=acc, width=3 * S)
    img = place(img, p["img"], cx, cy + 10, 520, 720)
    d = ImageDraw.Draw(img)
    lg = load_logo(230); img.alpha_composite(lg, (W - lg.width - 44 * S, 44 * S)); d = ImageDraw.Draw(img)
    # left column
    x = 56
    pf = f("Poppins-Medium.ttf", 22); tw = d.textlength(p["tag"], font=pf) / S
    d.rounded_rectangle(P(x, 64, x + tw + 40, 110), radius=23 * S, outline=(235, 242, 232), width=2 * S)
    d.text(P(x + 20, 72), p["tag"], font=pf, fill="white")
    ft, lines = wrap(d, p["title"], "Poppins-Bold.ttf", 60, LW - 2 * x, 3)
    y = 150; lh = ft.size / S * 1.15
    for l in lines: d.text(P(x, y), l, font=ft, fill="white"); y += lh
    y += 10
    sf = f("Poppins-Regular.ttf", 25)
    d.text(P(x, y), p["sub"], font=sf, fill=SAGE_L); y += 70
    ff = f("Poppins-Medium.ttf", 25)
    for t in p["feats"]:
        check_icon(d, x + 15, y + 17, 15, (255, 255, 255), SAGE)
        d.text(P(x + 44, y), t, font=fit(d, t, "Poppins-Medium.ttf", 25, LW - x - 44 - 30), fill="white"); y += 58
    # price block
    y = max(y + 90, 700)
    d.text(P(x, y), p.get("label", "ONLY"), font=f("Poppins-Medium.ttf", 22), fill=SAGE_L)
    pfnt = f("Poppins-Bold.ttf", 66); d.text(P(x, y + 26), tk(p["price"]), font=pfnt, fill="white")
    if p["regular"] > p["price"]:
        of = f("Poppins-Regular.ttf", 28); o = tk(p["regular"]); ow = d.textlength(o, font=of) / S
        d.text(P(x, y + 118), o, font=of, fill=(200, 214, 196))
        d.line(P(x, y + 137, x + ow, y + 137), fill=(200, 214, 196), width=2 * S)
    # CTA
    d.rounded_rectangle(P(x, 1196, LW - x, 1262), radius=33 * S, fill="white")
    bf = f("Poppins-Bold.ttf", 28); bt = "Order Now"; bw = d.textlength(bt, font=bf) / S
    d.text(P((x + LW - x) / 2 - bw / 2, 1210), bt, font=bf, fill=SAGE)
    uf = f("Poppins-Medium.ttf", 21); u = "everydaycart.online"; uw = d.textlength(u, font=uf) / S
    d.text(P(LW / 2 - uw / 2, 1282), u, font=uf, fill=SAGE_L)
    # colour dots on product side, bottom
    if p.get("colours"):
        n = len(p["colours"]); cw = 34; gap = 16; tot = n * cw + (n - 1) * gap
        lab = f("Poppins-Medium.ttf", 22); lt = p.get("colour_label", "Available colours")
        ltw = d.textlength(lt, font=lab) / S
        sx = cx - (ltw + 20 + tot) / 2
        d.text(P(sx, 1206), lt, font=lab, fill=MUTE)
        bx = sx + ltw + 20
        for c in p["colours"]:
            d.ellipse(P(bx, 1204, bx + cw, 1204 + cw), fill=c, outline=(200, 190, 186), width=2 * S); bx += cw + gap
    return finish(img, p["out"])

# ---------------- Template B: colour card ----------------
def template_b(p):
    bgc = p.get("bg", (234, 242, 246)); circ = p.get("circle", (246, 250, 252))
    img = Image.new("RGBA", (W, H), bgc + (255,)); d = ImageDraw.Draw(img)
    d.ellipse(P(540 - 380, 640 - 380, 540 + 380, 640 + 380), fill=circ)
    # small flat decorative dots
    for (x, y, r) in [(120, 420, 14), (980, 760, 10), (150, 900, 8), (930, 330, 8)]:
        d.ellipse(P(x - r, y - r, x + r, y + r), fill=p.get("dot", (255, 255, 255)))
    lg = load_logo(250); img.alpha_composite(lg, (44 * S, 44 * S)); d = ImageDraw.Draw(img)
    tag_pill(d, W0 - 48, 56, p["tag"], SAGE, "white")
    tf = fit(d, p["title"], "Poppins-Bold.ttf", 58, W0 - 120); tw = d.textlength(p["title"], font=tf) / S
    d.text(P(540 - tw / 2, 168), p["title"], font=tf, fill=INK)
    sf = fit(d, p["sub"], "Poppins-Regular.ttf", 27, W0 - 160); sw = d.textlength(p["sub"], font=sf) / S
    d.text(P(540 - sw / 2, 242), p["sub"], font=sf, fill=MUTE)
    img = place(img, p["img"], 540, 650, p.get("maxw", 760), p.get("maxh", 560))
    d = ImageDraw.Draw(img)
    # flat price sticker
    bx, by, r = p.get("badge", (905, 395)) + (98,)
    d.ellipse(P(bx - r, by - r, bx + r, by + r), fill=ROSE)
    d.ellipse(P(bx - r + 9, by - r + 9, bx + r - 9, by + r - 9), outline=(232, 196, 192), width=2 * S)
    has_old = p["regular"] > p["price"]
    yl, yp = (-66, -38) if has_old else (-50, -20)
    lf = f("Poppins-Medium.ttf", 21); lt = p.get("label", "ONLY"); lw_ = d.textlength(lt, font=lf) / S
    d.text(P(bx - lw_ / 2, by + yl), lt, font=lf, fill=(255, 232, 228))
    pf = fit(d, tk(p["price"]), "Poppins-Bold.ttf", 40, 2 * r - 34); pw = d.textlength(tk(p["price"]), font=pf) / S
    d.text(P(bx - pw / 2, by + yp), tk(p["price"]), font=pf, fill="white")
    if has_old:
        of = f("Poppins-Regular.ttf", 25); o = tk(p["regular"]); ow = d.textlength(o, font=of) / S
        d.text(P(bx - ow / 2, by + 16), o, font=of, fill=(255, 222, 218))
        d.line(P(bx - ow / 2, by + 33, bx + ow / 2, by + 33), fill=(255, 222, 218), width=2 * S)
    # bottom card
    box = (48, 1036, 1032, 1302)
    img = card_shadow(img, box, 34, alpha=35); d = ImageDraw.Draw(img)
    d.rounded_rectangle(P(*box), radius=34 * S, fill="white")
    feats = p["feats"]; size = 23; gap = 14
    while True:
        cf = f("Poppins-Medium.ttf", size); ws = [d.textlength(t, font=cf) / S + 36 for t in feats]
        if sum(ws) + gap * (len(ws) - 1) <= 984 - 60 or size <= 16: break
        size -= 1
    x = 540 - (sum(ws) + gap * (len(ws) - 1)) / 2
    chip = p.get("chip", (238, 244, 236))
    for t, w_ in zip(feats, ws):
        d.rounded_rectangle(P(x, 1068, x + w_, 1116), radius=24 * S, fill=chip)
        d.text(P(x + 18, 1068 + (48 - size * 1.4) / 2), t, font=cf, fill=INK); x += w_ + gap
    d.line(P(88, 1146, 992, 1146), fill=(236, 232, 230), width=2 * S)
    uf = f("Poppins-Medium.ttf", 27); d.text(P(92, 1196), "everydaycart.online", font=uf, fill=MUTE)
    bf = f("Poppins-Bold.ttf", 28); bt = "Order Now"; bw = d.textlength(bt, font=bf) / S
    d.rounded_rectangle(P(992 - bw - 64, 1180, 992, 1250), radius=35 * S, fill=SAGE)
    d.text(P(992 - bw - 32, 1196), bt, font=bf, fill="white")
    return finish(img, p["out"])

# ---------------- Template C: collection grid ----------------
def template_c(p):
    img = Image.new("RGBA", (W, H), CREAM + (255,)); d = ImageDraw.Draw(img)
    lg = load_logo(250); img.alpha_composite(lg, (44 * S, 44 * S)); d = ImageDraw.Draw(img)
    tag_pill(d, W0 - 48, 56, p["tag"], SAGE, "white")
    tf = fit(d, p["title"], "Poppins-Bold.ttf", 58, W0 - 120); tw = d.textlength(p["title"], font=tf) / S
    d.text(P(540 - tw / 2, 160), p["title"], font=tf, fill=INK)
    sf = fit(d, p["sub"], "Poppins-Regular.ttf", 27, W0 - 160); sw = d.textlength(p["sub"], font=sf) / S
    d.text(P(540 - sw / 2, 234), p["sub"], font=sf, fill=MUTE)
    cw, ch, g = 476, 392, 32
    for i, it in enumerate(p["items"]):
        cx0 = 48 + (i % 2) * (cw + g); cy0 = 296 + (i // 2) * (ch + g)
        box = (cx0, cy0, cx0 + cw, cy0 + ch)
        img = card_shadow(img, box, 30, alpha=30, blur=14, dy=8); d = ImageDraw.Draw(img)
        d.rounded_rectangle(P(*box), radius=30 * S, fill="white")
        acc = it.get("accent", p.get("accent", (240, 234, 230)))
        ccx, ccy = cx0 + cw / 2, cy0 + 138
        d.ellipse(P(ccx - 118, ccy - 118, ccx + 118, ccy + 118), fill=acc)
        img = place(img, it["img"], ccx, ccy, 300, 220, floor=False); d = ImageDraw.Draw(img)
        nf = fit(d, it["name"], "Poppins-Bold.ttf", 27, cw - 48); nw = d.textlength(it["name"], font=nf) / S
        d.text(P(ccx - nw / 2, cy0 + 278), it["name"], font=nf, fill=INK)
        pf = f("Poppins-Bold.ttf", 30); pt = tk(it["price"]); pw = d.textlength(pt, font=pf) / S
        has_old = it["regular"] > it["price"]
        of = f("Poppins-Regular.ttf", 22); o = tk(it["regular"]); ow = d.textlength(o, font=of) / S if has_old else 0
        tot = pw + (14 + ow if has_old else 0); sx = ccx - tot / 2
        d.text(P(sx, cy0 + 320), pt, font=pf, fill=ROSE)
        if has_old:
            ox = sx + pw + 14; d.text(P(ox, cy0 + 328), o, font=of, fill=MUTE)
            d.line(P(ox, cy0 + 343, ox + ow, cy0 + 343), fill=MUTE, width=2 * S)
    d.rectangle(P(0, 1150, W0, H0), fill=SAGE)
    bf = f("Poppins-Bold.ttf", 34); bt = "Order now at everydaycart.online"; bw = d.textlength(bt, font=bf) / S
    d.text(P(540 - bw / 2, 1196), bt, font=bf, fill="white")
    lf = f("Poppins-Medium.ttf", 24); lt = p.get("foot", "Limited stock  •  Inbox us to order"); lw_ = d.textlength(lt, font=lf) / S
    d.text(P(540 - lw_ / 2, 1258), lt, font=lf, fill=SAGE_L)
    return finish(img, p["out"])

HQ = D + "cutouts/hq/"; FL = D + "cutouts/flat/"
def im(p): return Image.open(p).convert("RGBA")

POSTS = [
    ("C", dict(out="01_top_gadget_picks", tag="GADGETS", title="Top Gadget Picks", sub="Official Oraimo & Awei  •  Best prices in Dhaka",
               items=[dict(img=HQ + "02.png", name="Oraimo Watch 5 Lite", price=1650, regular=1870),
                      dict(img=HQ + "13.png", name="Oraimo SpaceBuds Lite", price=1310, regular=1496),
                      dict(img=HQ + "04.png", name="Oraimo Necklace Lite", price=1300, regular=1485),
                      dict(img=HQ + "10.png", name="Awei T108 Earbuds", price=950, regular=1199)],
               accent=(236, 242, 233))),
    ("A", dict(out="02_oraimo_watch_5_lite", img=HQ + "02.png", tag="SMART WATCH", title="Oraimo Watch 5 Lite",
               sub="Official  •  Bluetooth Calling", feats=["2.01\" HD Display", "HD Voice Calling", "IP68 Water Resistant", "7 Day Battery"],
               price=1650, regular=1870, accent=(232, 238, 229))),
    ("B", dict(out="03_oraimo_spacebuds_neo_plus", img=HQ + "12.png", tag="EARBUDS", title="Oraimo SpaceBuds Neo+",
               sub="Spatial Audio Earbuds  •  Off White", feats=["Sound360 Audio", "30 Hrs Battery", "Game Mode", "IPX4"],
               price=1940, regular=2189, bg=(241, 235, 228), circle=(250, 246, 241), chip=(244, 238, 231), maxw=600, maxh=560)),
    ("A", dict(out="04_kodomo_baby_lotion_powder", img=FL + "kodomo_lotion.png", tag="BABY CARE", title="Kodomo Baby Lotion Powder",
               sub="180 ml  •  For 0+ Months", feats=["Extra Mild Formula", "Gentle on Baby Skin", "Lotion + Powder in One", "Daily Use"],
               price=720, regular=880, accent=(222, 238, 246))),
    ("B", dict(out="05_kodomo_baby_toothpaste", img=FL + "kodomo_paste.png", tag="BABY CARE", title="Kodomo Baby Toothpaste",
               sub="Orange Flavour  •  For 6+ Months", feats=["Fluoride 1000 ppm", "Xylitol Plus", "Ultra Shield Formula", "Kids Love the Taste"],
               price=280, regular=400, bg=(253, 236, 226), circle=(255, 247, 241), chip=(253, 238, 229), maxw=860, maxh=420, badge=(905, 420))),
    ("B", dict(out="06_kodomo_toothbrush", img=FL + "kodomo_brush.png", tag="BABY CARE", title="Kodomo Baby Toothbrush",
               sub="Lion Kodomo  •  For 6 Months to 3 Years", feats=["Extra Soft Bristles", "Small Brush Head", "Easy Grip Handle", "Japan Quality"],
               price=200, regular=400, bg=(232, 243, 236), circle=(246, 251, 247), chip=(234, 244, 237), maxw=540, maxh=600, badge=(935, 380))),
    ("C", dict(out="07_baby_care_essentials", tag="BABY CARE", title="Baby Care Essentials", sub="Gentle picks for your little one",
               items=[dict(img=FL + "kodomo_lotion.png", name="Kodomo Lotion Powder", price=720, regular=880, accent=(226, 240, 247)),
                      dict(img=FL + "kodomo_paste.png", name="Kodomo Toothpaste", price=280, regular=400, accent=(253, 236, 226)),
                      dict(img=FL + "kodomo_brush.png", name="Kodomo Toothbrush", price=200, regular=400, accent=(232, 243, 236)),
                      dict(img=HQ + "21.png", name="10 Pc Baby Care Kit", price=480, regular=650, accent=(247, 234, 238))],
               foot="Limited stock  •  Inbox us to order")),
    ("A", dict(out="08_have_good_time_tumbler", img=FL + "hgt_tumbler.png", tag="THERMAL", title="Have Good Time Tumbler",
               sub="750 ml  •  Insulated Steel", feats=["Hot & Cold Drinks", "Secure Travel Lid", "Easy Carry Handle", "Double Wall Steel"],
               price=1000, regular=1200, accent=(246, 228, 230), colours=[(244, 170, 186), (255, 255, 255)])),
]

if __name__ == "__main__":
    keys = sys.argv[1:]
    for kind, p in POSTS:
        if keys and p["out"][:2] not in keys: continue
        if "img" in p: p["img"] = im(p["img"])
        for it in p.get("items", []): it["img"] = im(it["img"])
        {"A": template_a, "B": template_b, "C": template_c}[kind](p)
