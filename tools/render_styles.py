"""Extra flat post styles so each day's batch looks different (no 3D, small corner logo, brand palette, Poppins).

Style sets (rotate daily, see posts/style_log.json):
  set 1 = render_flat A/B/C (split panel, colour card, collection grid)
  set 2 = D/E/F below (arch poster, header ribbon, list menu)
"""
import os
from PIL import Image, ImageDraw
import render_flat as rf
from render_flat import P, f, fit, wrap, tk, S, W, H, W0, H0, SAGE, SAGE_L, ROSE, INK, MUTE, CREAM, load_logo

ROSE_D = (138, 88, 88)


def spaced(d, xy, text, font, fill, spacing=3):
    x, y = xy
    for ch in text:
        d.text(P(x, y), ch, font=font, fill=fill); x += d.textlength(ch, font=font) / S + spacing
    return x


def spaced_w(d, text, font, spacing=3):
    return sum(d.textlength(ch, font=font) / S + spacing for ch in text) - spacing


def strike(d, x, y, text, font, fill):
    w = d.textlength(text, font=font) / S
    d.text(P(x, y), text, font=font, fill=fill)
    d.line(P(x, y + font.size / S * 0.72, x + w, y + font.size / S * 0.72), fill=fill, width=2 * S)
    return w


# ---------------- Template D: arch poster ----------------
def template_d(p):
    bg = p.get("bg", (226, 234, 222)); arch = p.get("arch", CREAM)
    img = Image.new("RGBA", (W, H), bg + (255,)); d = ImageDraw.Draw(img)
    lg = load_logo(170); img.alpha_composite(lg, (52 * S, 46 * S)); d = ImageDraw.Draw(img)
    tf = f("Poppins-Medium.ttf", 21); tw = spaced_w(d, p["tag"], tf, 4)
    spaced(d, (W0 - 56 - tw, 66), p["tag"], tf, p.get("ink", SAGE), 4)
    # arch window
    x0, x1, y0, y1 = 150, 930, 150, 930; r = (x1 - x0) / 2
    d.rounded_rectangle(P(x0, y0 + r, x1, y1), radius=0, fill=arch)
    d.pieslice(P(x0, y0, x1, y0 + 2 * r), 180, 360, fill=arch)
    d.arc(P(x0 - 22, y0 - 22, x1 + 22, y0 + 2 * r + 22), 180, 360, fill=arch, width=3 * S)
    d.line(P(x0 - 22, y0 + r, x0 - 22, y1), fill=arch, width=3 * S); d.line(P(x1 + 22, y0 + r, x1 + 22, y1), fill=arch, width=3 * S)
    img = rf.place(img, p["img"], 540, 575, p.get("maxw", 600), p.get("maxh", 560)); d = ImageDraw.Draw(img)
    # price tag hanging on the arch edge
    pr = tk(p["price"]); pf = f("Poppins-Bold.ttf", 46); pw = d.textlength(pr, font=pf) / S
    has_old = p["regular"] > p["price"]
    bx1 = x1 + 10; bx0 = bx1 - pw - 56; by0 = 830
    d.rounded_rectangle(P(bx0, by0, bx1, by0 + (118 if has_old else 86)), radius=18 * S, fill=ROSE)
    d.text(P(bx0 + 28, by0 + 12), pr, font=pf, fill="white")
    if p.get("label"):
        lf = f("Poppins-Bold.ttf", 22); lt = p["label"]; lw_ = d.textlength(lt, font=lf) / S
        d.rounded_rectangle(P(bx0, by0 - 40, bx0 + lw_ + 32, by0 - 4), radius=18 * S, fill=INK)
        d.text(P(bx0 + 16, by0 - 37), lt, font=lf, fill="white")
    if has_old:
        of = f("Poppins-Regular.ttf", 24); o = tk(p["regular"]); ow = d.textlength(o, font=of) / S
        strike(d, bx0 + 28, by0 + 76, o, of, (255, 222, 218))
    # title block
    ft, lines = wrap(d, p["title"], "Poppins-Bold.ttf", 56, 920, 2)
    y = 985
    for l in lines:
        lw_ = d.textlength(l, font=ft) / S; d.text(P(540 - lw_ / 2, y), l, font=ft, fill=INK); y += ft.size / S * 1.12
    feats = "  •  ".join(p["feats"])
    ff = fit(d, feats, "Poppins-Regular.ttf", 26, 960); fw = d.textlength(feats, font=ff) / S
    d.text(P(540 - fw / 2, y + 12), feats, font=ff, fill=MUTE)
    # footer
    d.line(P(80, 1218, 1000, 1218), fill=p.get("rule", (200, 210, 196)), width=2 * S)
    uf = f("Poppins-Medium.ttf", 26); d.text(P(80, 1250), "everydaycart.online", font=uf, fill=INK)
    bf = f("Poppins-Bold.ttf", 25); bt = "Inbox to order"; bw = d.textlength(bt, font=bf) / S
    d.rounded_rectangle(P(1000 - bw - 56, 1240, 1000, 1298), radius=29 * S, fill=SAGE)
    d.text(P(1000 - bw - 28, 1252), bt, font=bf, fill="white")
    return rf.finish(img, p["out"])


# ---------------- Template E: header ribbon + feature tiles ----------------
def template_e(p):
    hd = p.get("head", SAGE); bg = p.get("bg", CREAM); tile = p.get("tile", (255, 255, 255))
    img = Image.new("RGBA", (W, H), bg + (255,)); d = ImageDraw.Draw(img)
    d.rectangle(P(0, 0, W0, 330), fill=hd)
    # scalloped bottom edge of the header (flat semicircles)
    for i in range(12):
        cx = 45 + i * 90; d.ellipse(P(cx - 45, 285, cx + 45, 375), fill=hd)
    lg = load_logo(160)
    d.rounded_rectangle(P(W0 - 52 - lg.width / S - 24, 40, W0 - 52, 40 + lg.height / S + 20), radius=14 * S, fill=(255, 255, 255))
    img.alpha_composite(lg, (int((W0 - 64 - lg.width / S) * S), 50 * S)); d = ImageDraw.Draw(img)
    tf = f("Poppins-Medium.ttf", 22); spaced(d, (64, 84), p["tag"], tf, SAGE_L if hd == SAGE else (255, 236, 232), 4)
    ft = fit(d, p["title"], "Poppins-Bold.ttf", 62, 740); lines = [p["title"]]
    if ft.size / S < 48: ft, lines = wrap(d, p["title"], "Poppins-Bold.ttf", 50, 740, 2)
    y = 138 if len(lines) == 1 else 112
    for l in lines: d.text(P(64, y), l, font=ft, fill="white"); y += ft.size / S * 1.1
    sf = fit(d, p["sub"], "Poppins-Regular.ttf", 28, 900); d.text(P(64, y + 14), p["sub"], font=sf, fill=(236, 240, 232))
    # product zone
    acc = p.get("accent", (238, 232, 228))
    d.rounded_rectangle(P(300, 430, 780, 910), radius=240 * S, fill=acc)
    img = rf.place(img, p["img"], 540, 670, p.get("maxw", 560), p.get("maxh", 500)); d = ImageDraw.Draw(img)
    # vertical price ribbon on the left
    has_old = p["regular"] > p["price"]
    d.rectangle(P(64, 400, 236, 640), fill=ROSE)
    d.polygon([P(64, 640), P(150, 600), P(236, 640), P(236, 680), P(150, 640), P(64, 680)], fill=ROSE)
    lf = f("Poppins-Medium.ttf", 21); lt = p.get("label", "PRICE"); lw_ = d.textlength(lt, font=lf) / S
    d.text(P(150 - lw_ / 2, 430), lt, font=lf, fill=(255, 228, 224))
    pf = fit(d, tk(p["price"]), "Poppins-Bold.ttf", 40, 150); pw = d.textlength(tk(p["price"]), font=pf) / S
    d.text(P(150 - pw / 2, 470), tk(p["price"]), font=pf, fill="white")
    if has_old:
        of = f("Poppins-Regular.ttf", 23); o = tk(p["regular"]); ow = d.textlength(o, font=of) / S
        strike(d, 150 - ow / 2, 534, o, of, (255, 222, 218))
    # 2x2 feature tiles
    for i, t in enumerate(p["feats"][:4]):
        cx0 = 64 + (i % 2) * 484; cy0 = 960 + (i // 2) * 100
        d.rounded_rectangle(P(cx0, cy0, cx0 + 468, cy0 + 84), radius=20 * S, fill=tile)
        d.ellipse(P(cx0 + 24, cy0 + 28, cx0 + 52, cy0 + 56), fill=hd)
        tf2 = fit(d, t, "Poppins-Medium.ttf", 27, 370); d.text(P(cx0 + 72, cy0 + 22), t, font=tf2, fill=INK)
    d.text(P(64, 1188), "Order now", font=f("Poppins-Bold.ttf", 34), fill=INK)
    uf = f("Poppins-Medium.ttf", 26); d.text(P(64, 1238), "everydaycart.online  •  Inbox us to order", font=uf, fill=MUTE)
    d.ellipse(P(940, 1196, 1016, 1272), fill=hd)
    d.line([P(962, 1234), P(994, 1234)], fill="white", width=5 * S)
    d.line([P(980, 1218), P(996, 1234), P(980, 1250)], fill="white", width=5 * S, joint="curve")
    return rf.finish(img, p["out"])


# ---------------- Template F: list menu (collection) ----------------
def template_f(p):
    bg = p.get("bg", (244, 236, 232))
    img = Image.new("RGBA", (W, H), bg + (255,)); d = ImageDraw.Draw(img)
    lg = load_logo(170); img.alpha_composite(lg, (52 * S, 46 * S)); d = ImageDraw.Draw(img)
    tf = f("Poppins-Medium.ttf", 21); tw = spaced_w(d, p["tag"], tf, 4)
    spaced(d, (W0 - 56 - tw, 66), p["tag"], tf, ROSE, 4)
    ft = fit(d, p["title"], "Poppins-Bold.ttf", 62, 960); d.text(P(60, 150), p["title"], font=ft, fill=INK)
    sf = fit(d, p["sub"], "Poppins-Regular.ttf", 27, 960); d.text(P(60, 232), p["sub"], font=sf, fill=MUTE)
    rh, gap, y = 196, 20, 296
    for i, it in enumerate(p["items"]):
        box = (60, y, 1020, y + rh)
        img = rf.card_shadow(img, box, 28, alpha=26, blur=12, dy=6); d = ImageDraw.Draw(img)
        d.rounded_rectangle(P(*box), radius=28 * S, fill="white")
        acc = it.get("accent", (240, 234, 230))
        d.rounded_rectangle(P(78, y + 18, 78 + 220, y + rh - 18), radius=22 * S, fill=acc)
        img = rf.place(img, it["img"], 188, y + rh / 2, 190, 150, floor=False); d = ImageDraw.Draw(img)
        d.text(P(330, y + 40), f"0{i + 1}", font=f("Poppins-Medium.ttf", 22), fill=ROSE)
        nf = fit(d, it["name"], "Poppins-Bold.ttf", 34, 420); d.text(P(330, y + 70), it["name"], font=nf, fill=INK)
        if it.get("note"):
            d.text(P(330, y + 120), it["note"], font=fit(d, it["note"], "Poppins-Regular.ttf", 23, 420), fill=MUTE)
        pf = f("Poppins-Bold.ttf", 38); pt = tk(it["price"]); pw = d.textlength(pt, font=pf) / S
        d.text(P(992 - pw, y + 56), pt, font=pf, fill=ROSE)
        if it["regular"] > it["price"]:
            of = f("Poppins-Regular.ttf", 23); o = tk(it["regular"]); ow = d.textlength(o, font=of) / S
            strike(d, 992 - ow, y + 112, o, of, MUTE)
        y += rh + gap
    d.rounded_rectangle(P(60, 1196, 1020, 1300), radius=52 * S, fill=SAGE)
    bf = f("Poppins-Bold.ttf", 31); bt = "Order at everydaycart.online"; bw = d.textlength(bt, font=bf) / S
    d.text(P(540 - bw / 2, 1210), bt, font=bf, fill="white")
    lf = f("Poppins-Medium.ttf", 22); lt = p.get("foot", "Limited stock  •  Inbox us to order"); lw_ = d.textlength(lt, font=lf) / S
    d.text(P(540 - lw_ / 2, 1256), lt, font=lf, fill=SAGE_L)
    return rf.finish(img, p["out"])


TEMPLATES = {"A": rf.template_a, "B": rf.template_b, "C": rf.template_c, "D": template_d, "E": template_e, "F": template_f}
