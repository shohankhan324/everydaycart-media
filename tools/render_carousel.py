"""Everyday Cart gadget carousel: 7 square cards (1080x1080) with decor that flows across card edges."""
import os, sys
sys.path.insert(0, "/tmp/claude-0/-home-claude/da0f4f16-de8b-599c-9c43-7f614620f3dd/scratchpad")
import render_flat as rf
from render_flat import f, P, fit, place, tk, load_logo, check_icon, card_shadow, S, SAGE, SAGE_L, ROSE, INK, MUTE, CREAM
from PIL import Image, ImageDraw

D = os.path.dirname(os.path.abspath(__file__)) + "/"
OUT = "/mnt/user-data/outputs/everydaycart_carousel_gadgets/"; os.makedirs(OUT, exist_ok=True)
C = 1080; N = 7
HQ = D + "cutouts/hq/"
SAGE_T = (232, 238, 229); ROSE_T = (246, 229, 227)

PRODUCTS = [
    dict(img=HQ + "02.png", tag="SMART WATCH", name="Oraimo Watch 5 Lite", line="2.01\" HD Display  •  Bluetooth Calling  •  IP68", price=1650, regular=1870),
    dict(img=HQ + "12.png", tag="EARBUDS", name="Oraimo SpaceBuds Neo+", line="Sound360 Audio  •  30 Hrs Battery  •  Game Mode", price=1940, regular=2189),
    dict(img=HQ + "13.png", tag="EARBUDS", name="Oraimo SpaceBuds Lite", line="AI Call ENC  •  40 Hrs with Case  •  IPX4", price=1310, regular=1496),
    dict(img=HQ + "04.png", tag="NECKBAND", name="Oraimo Necklace Lite", line="30 Hrs Playtime  •  Dual Device  •  ENC Calls", price=1300, regular=1485),
    dict(img=HQ + "10.png", tag="EARBUDS", name="Awei T108 Earbuds", line="13mm Drivers  •  ENC Calls  •  Bluetooth 5.3", price=950, regular=1199),
]
# decor circles in strip coordinates, centred on card seams so they flow across
SEAMS = [(C * k, 150 if k % 2 else 930, 150, SAGE_T if k % 2 else ROSE_T) for k in range(1, N)]

def base(i, bg):
    img = Image.new("RGBA", (C * S, C * S), bg + (255,)); d = ImageDraw.Draw(img)
    for (sx, sy, r, col) in SEAMS:
        x = sx - i * C
        if -r < x < C + r:
            fill = col
            d.ellipse(P(x - r, sy - r, x + r, sy + r), fill=fill)
    return img, d

def dots(d, i, color_on, color_off):
    w = N * 14 + (N - 1) * 10; x = C / 2 - w / 2
    for k in range(N):
        d.ellipse(P(x, 1036, x + 14, 1050), fill=color_on if k == i else color_off); x += 24

def swipe(d, color):
    sf = f("Poppins-Medium.ttf", 24); t = "Swipe"; tw = d.textlength(t, font=sf) / S
    x = C - 64 - tw - 40
    d.text(P(x, 1022), t, font=sf, fill=color)
    ax = x + tw + 12; ay = 1038
    d.line(P(ax, ay, ax + 26, ay), fill=color, width=3 * S)
    d.line([P(ax + 16, ay - 9), P(ax + 27, ay), P(ax + 16, ay + 9)], fill=color, width=3 * S, joint="curve")

def save(img, i, name):
    out = img.convert("RGB").resize((C, C), Image.LANCZOS)
    p = f"{OUT}{i + 1:02d}_{name}.jpg"; out.save(p, quality=95, subsampling=0); print(p, flush=True)

def cover():
    img, d = base(0, SAGE)
    lg = load_logo(230)
    pad = Image.new("RGBA", (lg.width + 40 * S, lg.height + 28 * S), (0, 0, 0, 0))
    ImageDraw.Draw(pad).rounded_rectangle((0, 0, pad.width - 1, pad.height - 1), radius=24 * S, fill=CREAM + (255,))
    pad.alpha_composite(lg, (20 * S, 14 * S)); img.alpha_composite(pad, (48 * S, 44 * S)); d = ImageDraw.Draw(img)
    d.text(P(64, 250), "Gadget", font=f("Poppins-Bold.ttf", 96), fill="white")
    d.text(P(64, 350), "Deals", font=f("Poppins-Bold.ttf", 96), fill="white")
    d.text(P(66, 478), "Official Oraimo & Awei", font=f("Poppins-Medium.ttf", 32), fill=SAGE_L)
    # save badge
    d.rounded_rectangle(P(64, 548, 400, 616), radius=34 * S, fill=ROSE)
    bf = f("Poppins-Bold.ttf", 30); bt = "Save up to 20%"; bw = d.textlength(bt, font=bf) / S
    d.text(P(232 - bw / 2, 562), bt, font=bf, fill="white")
    # collage of three products on white circles
    for (cx, cy, r, k) in [(790, 330, 190, 0), (640, 720, 165, 1), (930, 760, 140, 4)]:
        d.ellipse(P(cx - r, cy - r, cx + r, cy + r), fill=(250, 248, 244))
        img = place(img, Image.open(PRODUCTS[k]["img"]).convert("RGBA"), cx, cy, r * 1.45, r * 1.45, floor=False)
        d = ImageDraw.Draw(img)
    d.text(P(64, 690), "5 picks inside", font=f("Poppins-Medium.ttf", 28), fill="white")
    d.text(P(64, 736), "from Tk 950", font=f("Poppins-Bold.ttf", 44), fill="white")
    dots(d, 0, (255, 255, 255), (150, 168, 143)); swipe(d, (255, 255, 255))
    save(img, 0, "cover")

def product(i, p):
    img, d = base(i, CREAM)
    lg = load_logo(200); img.alpha_composite(lg, (44 * S, 40 * S)); d = ImageDraw.Draw(img)
    pf = f("Poppins-Medium.ttf", 21); tw = d.textlength(p["tag"], font=pf) / S
    d.rounded_rectangle(P(C - 48 - tw - 40, 48, C - 48, 92), radius=22 * S, fill=SAGE)
    d.text(P(C - 48 - tw - 20, 55), p["tag"], font=pf, fill="white")
    d.ellipse(P(540 - 250, 430 - 250, 540 + 250, 430 + 250), fill=(255, 255, 255))
    img = place(img, Image.open(p["img"]).convert("RGBA"), 540, 430, 470, 450); d = ImageDraw.Draw(img)
    nf = fit(d, p["name"], "Poppins-Bold.ttf", 52, C - 120); nw = d.textlength(p["name"], font=nf) / S
    d.text(P(540 - nw / 2, 718), p["name"], font=nf, fill=INK)
    lf = fit(d, p["line"], "Poppins-Regular.ttf", 26, C - 140); lw = d.textlength(p["line"], font=lf) / S
    d.text(P(540 - lw / 2, 792), p["line"], font=lf, fill=MUTE)
    pfnt = f("Poppins-Bold.ttf", 40); pt = tk(p["price"]); pw = d.textlength(pt, font=pfnt) / S
    has_old = p["regular"] > p["price"]
    of = f("Poppins-Regular.ttf", 28); o = tk(p["regular"]); ow = d.textlength(o, font=of) / S
    pill_w = pw + 56; tot = pill_w + (20 + ow if has_old else 0); x = 540 - tot / 2
    d.rounded_rectangle(P(x, 862, x + pill_w, 934), radius=36 * S, fill=ROSE)
    d.text(P(x + 28, 870), pt, font=pfnt, fill="white")
    if has_old:
        ox = x + pill_w + 20; d.text(P(ox, 880), o, font=of, fill=MUTE)
        d.line(P(ox, 899, ox + ow, 899), fill=MUTE, width=2 * S)
    dots(d, i, SAGE, (214, 206, 202)); swipe(d, SAGE)
    save(img, i, p["name"].lower().replace(" ", "_").replace("+", "_plus"))

def end():
    i = N - 1
    img, d = base(i, CREAM)
    lg = load_logo(400); img.alpha_composite(lg, (int((C * S - lg.width) / 2), 90 * S)); d = ImageDraw.Draw(img)
    t = "Ready to order?"; tf = f("Poppins-Bold.ttf", 66); tw = d.textlength(t, font=tf) / S
    d.text(P(540 - tw / 2, 310), t, font=tf, fill=INK)
    steps = ["Pick your favourite gadget", "Order at everydaycart.online", "Or inbox us on Facebook"]
    sf = f("Poppins-Medium.ttf", 32); y = 450
    for k, s in enumerate(steps):
        x = 250
        d.ellipse(P(x, y, x + 56, y + 56), fill=SAGE)
        nf = f("Poppins-Bold.ttf", 28); nt = str(k + 1); nw = d.textlength(nt, font=nf) / S
        d.text(P(x + 28 - nw / 2, y + 7), nt, font=nf, fill="white")
        d.text(P(x + 80, y + 6), s, font=sf, fill=INK); y += 92
    bf = f("Poppins-Bold.ttf", 36); bt = "Shop Now"; bw = d.textlength(bt, font=bf) / S
    d.rounded_rectangle(P(540 - bw / 2 - 60, 768, 540 + bw / 2 + 60, 852), radius=42 * S, fill=SAGE)
    d.text(P(540 - bw / 2, 784), bt, font=bf, fill="white")
    lt = "Limited stock  •  Official products"; lf = f("Poppins-Medium.ttf", 26); lw = d.textlength(lt, font=lf) / S
    d.text(P(540 - lw / 2, 892), lt, font=lf, fill=MUTE)
    dots(d, i, SAGE, (214, 206, 202))
    save(img, i, "order_now")

if __name__ == "__main__":
    cover()
    for k, p in enumerate(PRODUCTS): product(k + 1, p)
    end()
