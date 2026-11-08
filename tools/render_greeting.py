"""Everyday Cart flat occasion greeting cards and offer drafts (no 3D, logo small in a corner)."""
import math, os, sys
from PIL import Image, ImageDraw, ImageFilter
import render_flat as rf
from render_flat import P, f, fit, S, W, H, W0, H0, SAGE, SAGE_L, ROSE, INK, MUTE, CREAM, load_logo

GOLD = (226, 170, 84); GOLD_L = (246, 214, 150); ROSE_D = (138, 88, 88); ROSE_L = (240, 222, 219)


def centered(d, y, text, name, size, maxw, fill):
    ft = fit(d, text, name, size, maxw); tw = d.textlength(text, font=ft) / S
    d.text(P(540 - tw / 2, y), text, font=ft, fill=fill); return ft


def glow(img, cx, cy, r, color, alpha):
    L = Image.new("RGBA", img.size, color + (0,))
    ImageDraw.Draw(L).ellipse(P(cx - r, cy - r, cx + r, cy + r), fill=color + (alpha,))
    return Image.alpha_composite(img, L.filter(ImageFilter.GaussianBlur(r * 0.45 * S)))


def diya(img, cx, cy, sc=1.0, body=ROSE, rim=ROSE_D):
    """Flat diya: bowl, rim band, dotted pattern, teardrop flame."""
    img = glow(img, cx + 170 * sc * 1.14, cy - 70 * sc, 80 * sc, GOLD_L, 170)
    d = ImageDraw.Draw(img)
    w, h = 170 * sc, 70 * sc
    # bowl (half ellipse) + spout
    d.pieslice(P(cx - w, cy - h, cx + w, cy + h), 0, 180, fill=body)
    d.polygon([P(cx + w * 0.78, cy), P(cx + w * 1.18, cy - 22 * sc), P(cx + w * 0.92, cy + 26 * sc)], fill=body)
    d.rounded_rectangle(P(cx - w - 6 * sc, cy - 10 * sc, cx + w + 6 * sc, cy + 10 * sc), radius=10 * sc * S, fill=rim)
    for i in range(-3, 4):
        x = cx + i * 38 * sc
        d.ellipse(P(x - 7 * sc, cy + 30 * sc - 7 * sc, x + 7 * sc, cy + 30 * sc + 7 * sc), fill=GOLD_L)
    # base
    d.rounded_rectangle(P(cx - 60 * sc, cy + h - 6 * sc, cx + 60 * sc, cy + h + 14 * sc), radius=8 * sc * S, fill=rim)
    # flame: upright teardrop on the spout tip
    fx, fy = cx + w * 1.14, cy - 19 * sc
    d.line([P(fx, fy), P(fx, fy - 18 * sc)], fill=INK, width=int(4 * sc * S))
    def drop(bx, by, r, hgt, fill):
        d.ellipse(P(bx - r, by - r, bx + r, by + r), fill=fill)
        a = math.asin(r / hgt) if hgt > r else 0.9
        d.polygon([P(bx - r * math.cos(a), by - r * math.sin(a)), P(bx, by - hgt), P(bx + r * math.cos(a), by - r * math.sin(a))], fill=fill)
    drop(fx, fy - 50 * sc, 30 * sc, 84 * sc, GOLD)
    drop(fx, fy - 40 * sc, 15 * sc, 46 * sc, (255, 240, 205))
    return img


def sparkle(d, x, y, r, fill):
    d.polygon([P(x, y - r), P(x + r * 0.28, y - r * 0.28), P(x + r, y), P(x + r * 0.28, y + r * 0.28),
               P(x, y + r), P(x - r * 0.28, y + r * 0.28), P(x - r, y), P(x - r * 0.28, y - r * 0.28)], fill=fill)


def dipaboli(out):
    img = Image.new("RGBA", (W, H), CREAM + (255,)); d = ImageDraw.Draw(img)
    # sage top band with hanging string of small lamps
    d.rectangle(P(0, 0, W0, 470), fill=SAGE)
    d.ellipse(P(-200, 330, W0 + 200, 610), fill=SAGE)
    lg = load_logo(190)
    # string lights
    for i in range(9):
        x = 90 + i * 112.5; y = 120 + 34 * math.sin(i / 8 * math.pi)
        d.line(P(x, 0, x, y), fill=(140, 160, 134), width=2 * S)
        img = glow(img, x, y + 6, 26, GOLD_L, 150); d = ImageDraw.Draw(img)
        d.ellipse(P(x - 11, y - 4, x + 11, y + 20), fill=GOLD)
    for (x, y, r) in [(150, 290, 12), (930, 270, 14), (90, 450, 8), (990, 430, 9), (540, 245, 9)]:
        sparkle(d, x, y, r, GOLD_L)
    # title on sage
    centered(d, 330, "Shubho Dipaboli", "Poppins-Bold.ttf", 78, 900, "white")
    centered(d, 438, "Happy Shyama Puja & Diwali", "Poppins-Medium.ttf", 32, 900, (232, 240, 228))
    # central diya on cream
    img = diya(img, 500, 830, 1.25); d = ImageDraw.Draw(img)
    for (x, y, r) in [(220, 700, 16), (870, 640, 12), (180, 900, 9), (900, 880, 10)]:
        sparkle(d, x, y, r, (236, 196, 130))
    # message
    msg = ["May the light of every lamp fill your home", "with peace, joy and togetherness."]
    y = 1000
    for l in msg:
        centered(d, y, l, "Poppins-Regular.ttf", 32, 960, INK); y += 50
    centered(d, y + 22, "With warm wishes from Everyday Cart", "Poppins-Medium.ttf", 27, 900, ROSE)
    # footer: small logo bottom-left, URL bottom-right
    d.rectangle(P(0, 1236, W0, H0), fill=(255, 255, 255))
    d.line(P(0, 1236, W0, 1236), fill=ROSE_L, width=3 * S)
    img.alpha_composite(lg, (44 * S, int((1293 - lg.height / S / 2) * S)))
    uf = f("Poppins-Medium.ttf", 25); u = "everydaycart.online"; uw = d.textlength(u, font=uf) / S
    d.text(P(1036 - uw, 1275), u, font=uf, fill=ROSE_D)
    return rf.finish(img, out)


def r10(x): return int(round(x / 10.0)) * 10


def offer_teaser(out, items, pct, code, dates):
    """11.11 offer announcement card: big flat 11.11, % off, coupon chip, product strip."""
    img = Image.new("RGBA", (W, H), CREAM + (255,)); d = ImageDraw.Draw(img)
    d.rectangle(P(0, 0, W0, 760), fill=SAGE)
    for (x, y, r) in [(110, 190, 14), (960, 170, 12), (180, 620, 9), (930, 600, 10), (80, 420, 7), (1000, 420, 8)]:
        sparkle(d, x, y, r, GOLD_L)
    lg = load_logo(190)
    d.rounded_rectangle(P(36, 32, 36 + lg.width / S + 24, 32 + lg.height / S + 20), radius=16 * S, fill=(255, 255, 255))
    img.alpha_composite(lg, (48 * S, 42 * S)); d = ImageDraw.Draw(img)
    rf.tag_pill(d, W0 - 48, 48, "MEGA SALE", ROSE, "white")
    centered(d, 150, "11.11", "Poppins-Bold.ttf", 230, 900, "white")
    centered(d, 440, "SHOPPING FESTIVAL", "Poppins-Medium.ttf", 40, 900, SAGE_L)
    # discount ribbon
    t = f"Extra {pct}% OFF"; ft = f("Poppins-Bold.ttf", 64); tw = d.textlength(t, font=ft) / S
    d.rounded_rectangle(P(540 - tw / 2 - 44, 520, 540 + tw / 2 + 44, 618), radius=49 * S, fill=ROSE)
    d.text(P(540 - tw / 2, 526), t, font=ft, fill="white")
    centered(d, 650, dates, "Poppins-Medium.ttf", 30, 900, "white")
    # coupon chip
    ct = "Use code"; cf = f("Poppins-Medium.ttf", 28); kf = f("Poppins-Bold.ttf", 34)
    w1 = d.textlength(ct, font=cf) / S; w2 = d.textlength(code, font=kf) / S; tot = w1 + 18 + w2 + 56
    x0 = 540 - tot / 2
    d.rounded_rectangle(P(x0, 796, x0 + tot, 866), radius=35 * S, fill=(255, 255, 255), outline=ROSE, width=3 * S)
    d.text(P(x0 + 28, 812), ct, font=cf, fill=MUTE); d.text(P(x0 + 28 + w1 + 18, 806), code, font=kf, fill=ROSE)
    # product strip
    n = len(items); cw = 230; g = 18; sx = 540 - (n * cw + (n - 1) * g) / 2
    for i, it in enumerate(items):
        x = sx + i * (cw + g); box = (x, 900, x + cw, 1160)
        img = rf.card_shadow(img, box, 24, alpha=28, blur=12, dy=6); d = ImageDraw.Draw(img)
        d.rounded_rectangle(P(*box), radius=24 * S, fill="white")
        d.ellipse(P(x + cw / 2 - 82, 934, x + cw / 2 + 82, 1098), fill=it.get("accent", (238, 243, 235)))
        img = rf.place(img, it["img"], x + cw / 2, 1016, 180, 150, floor=False); d = ImageDraw.Draw(img)
        nf = fit(d, it["short"], "Poppins-Medium.ttf", 21, cw - 24); nw = d.textlength(it["short"], font=nf) / S
        d.text(P(x + cw / 2 - nw / 2, 1112), it["short"], font=nf, fill=INK)
    d.rectangle(P(0, 1200, W0, H0), fill=SAGE)
    centered(d, 1222, "Order at everydaycart.online", "Poppins-Bold.ttf", 34, 960, "white")
    centered(d, 1280, "Limited stock  •  Inbox us to order", "Poppins-Medium.ttf", 24, 960, SAGE_L)
    return rf.finish(img, out)


def offer_grid(out, items, pct, code, dates):
    p = dict(out=out, tag="11.11 SALE", title=f"11.11 Deals: Extra {pct}% OFF", sub=f"Code {code}  •  {dates}",
             items=[dict(img=it["img"], name=it["name"], price=r10(it["price"] * (100 - pct) / 100), regular=it["price"],
                         accent=it.get("accent", (238, 243, 235))) for it in items],
             foot=f"Use code {code}  •  Inbox us to order")
    return rf.template_c(p)


def offer_11_11():
    HQ = rf.HQ; FL = rf.FL; im = rf.im
    items = [dict(img=im(HQ + "02.png"), name="Oraimo Watch 5 Lite", short="Watch 5 Lite", price=1650, accent=(232, 238, 229)),
             dict(img=im(HQ + "12.png"), name="Oraimo SpaceBuds Neo+", short="SpaceBuds Neo+", price=1940, accent=(241, 235, 228)),
             dict(img=im(HQ + "01.png"), name="Oraimo SpaceBox Speaker", short="SpaceBox Speaker", price=1841, accent=(230, 236, 242)),
             dict(img=im(FL + "hgt_tumbler.png"), name="Have Good Time Tumbler", short="HGT Tumbler", price=1000, accent=(246, 228, 230))]
    offer_teaser("01_11_11_teaser", items, 11, "EC1111", "10 to 12 November")
    offer_grid("02_11_11_deals", items, 11, "EC1111", "10 to 12 Nov")


BD_GREEN = (0, 106, 78); BD_RED = (244, 42, 65)


def bd_flag(img, x, y, w, wave=0.0):
    """Flat Bangladesh flag (10:6, red disc offset toward hoist) on a slim pole."""
    d = ImageDraw.Draw(img); h = w * 0.6
    d.rounded_rectangle(P(x - 14, y - 26, x - 2, y + h + 110), radius=6 * S, fill=(150, 140, 132))
    d.rounded_rectangle(P(x - 44, y + h + 104, x + 28, y + h + 122), radius=9 * S, fill=(150, 140, 132))
    d.ellipse(P(x - 20, y - 40, x + 4, y - 16), fill=GOLD)
    d.rectangle(P(x, y, x + w, y + h), fill=BD_GREEN)
    r = w * 0.2; cx = x + w * 0.45; cy = y + h / 2
    d.ellipse(P(cx - r, cy - r, cx + r, cy + r), fill=BD_RED)
    return img


def armed_forces_day(out):
    img = Image.new("RGBA", (W, H), CREAM + (255,)); d = ImageDraw.Draw(img)
    d.rectangle(P(0, 0, W0, 430), fill=SAGE)
    d.ellipse(P(-220, 300, W0 + 220, 560), fill=SAGE)
    lg = load_logo(170)
    d.rounded_rectangle(P(36, 32, 36 + lg.width / S + 24, 32 + lg.height / S + 20), radius=16 * S, fill=(255, 255, 255))
    img.alpha_composite(lg, (48 * S, 42 * S)); d = ImageDraw.Draw(img)
    centered(d, 175, "21 November", "Poppins-Medium.ttf", 36, 900, SAGE_L)
    centered(d, 230, "Armed Forces Day", "Poppins-Bold.ttf", 84, 940, "white")
    centered(d, 347, "Sashastra Bahini Dibosh", "Poppins-Medium.ttf", 32, 900, (232, 240, 228))
    # flag with three service bands below (Army, Navy, Air Force), all flat
    img = bd_flag(img, 382, 630, 330); d = ImageDraw.Draw(img)
    labels = [("Army", (88, 110, 80)), ("Navy", (44, 62, 102)), ("Air Force", (92, 150, 196))]
    bw, g = 250, 26; sx = 540 - (3 * bw + 2 * g) / 2
    for i, (t, c) in enumerate(labels):
        x = sx + i * (bw + g)
        d.rounded_rectangle(P(x, 960, x + bw, 1024), radius=32 * S, fill=c)
        ft = f("Poppins-SemiBold.ttf", 28) if os.path.exists(rf.G + "Poppins-SemiBold.ttf") else f("Poppins-Bold.ttf", 28)
        tw = d.textlength(t, font=ft) / S; d.text(P(x + bw / 2 - tw / 2, 974), t, font=ft, fill="white")
    for (x, y, r) in [(170, 650, 14), (910, 620, 12), (140, 860, 9), (940, 860, 10)]:
        sparkle(d, x, y, r, GOLD)
    y = 1068
    for l in ["Saluting the courage, sacrifice and service", "of our Army, Navy and Air Force."]:
        centered(d, y, l, "Poppins-Regular.ttf", 32, 960, INK); y += 48
    centered(d, y + 14, "With respect from Everyday Cart", "Poppins-Medium.ttf", 26, 900, ROSE)
    d.rectangle(P(0, 1250, W0, H0), fill=(255, 255, 255))
    d.line(P(0, 1250, W0, 1250), fill=ROSE_L, width=3 * S)
    uf = f("Poppins-Medium.ttf", 25); u = "everydaycart.online"; uw = d.textlength(u, font=uf) / S
    d.text(P(540 - uw / 2, 1283), u, font=uf, fill=ROSE_D)
    return rf.finish(img, out)


if __name__ == "__main__":
    rf.OUTDIR = sys.argv[1] if len(sys.argv) > 1 else rf.OUTDIR
    os.makedirs(rf.OUTDIR, exist_ok=True)
    if len(sys.argv) > 2 and sys.argv[2] == "1111": offer_11_11()
    elif len(sys.argv) > 2 and sys.argv[2] == "afd": armed_forces_day("2026-11-21-armed-forces-day")
    else: print("usage: render_greeting.py OUTDIR 1111|afd")
