"""Style set 14 (added 19 Nov 2026):
AC sunburst retro poster (solid headline band, flat two-tone sunburst rays behind the product on a ringed disc,
zigzag starburst price badge, cream info card with Bangla line + 2x2 ticked features, ink footer; collection mode puts
several products on the rays, each with its own price chip),
AD comic panel (cream paper, thick ink panel borders, flat halftone dots, speech bubble hook, yellow caption box,
ink title strip, feature panel with Bangla line, POW-style starburst price panel; collection mode with price chips).
Flat only (no gradients, no blur), Poppins + Hind Siliguri, small logo chip in a corner."""
import math
from PIL import Image, ImageDraw
import render_flat as rf
from render_flat import P, f, fit, wrap, tk, S, W, H, W0, H0, INK, check_icon
from render_styles4 import logo_chip, mix, strike
from render_styles8 import _scaled, _bn_fit

WHITE = (255, 255, 255)
FOOT = "everydaycart.online  |  Inbox us to order"


def _burst(d, cx, cy, r, fill, n=22, inner=0.84, outline=None, ow=0, rot=0):
    pts = []
    for i in range(2 * n):
        a = math.pi * i / n + math.radians(rot); rr = r if i % 2 == 0 else r * inner
        pts.append(P(cx + rr * math.cos(a), cy + rr * math.sin(a)))
    if outline: d.polygon(pts, fill=fill, outline=outline, width=ow * S)
    else: d.polygon(pts, fill=fill)


def _price_burst(d, cx, cy, r, fill, col, price, regular, label="ONLY", outline=None, n=22):
    _burst(d, cx, cy, r, fill, n=n, outline=outline, ow=5 if outline else 0)
    d.text(P(cx, cy - r * 0.38), label, font=f("Poppins-Bold.ttf", max(18, r * 0.16)), fill=col, anchor="mm")
    pt = tk(price); pf = fit(d, pt, "Poppins-Bold.ttf", r * 0.42, r * 1.5)
    d.text(P(cx, cy + r * 0.02), pt, font=pf, fill=col, anchor="mm")
    if regular and regular > price:
        rt = "Regular " + tk(regular); rfo = fit(d, rt, "Poppins-Medium.ttf", max(16, r * 0.15), r * 1.3)
        rw = d.textlength(rt, font=rfo) / S
        strike(d, cx - rw / 2, cy + r * 0.3, rt, rfo, mix(col, fill, 0.3))


def _tagpill(d, text, fill, col, y=42):
    tf = f("Poppins-Bold.ttf", 21); tw = d.textlength(text, font=tf) / S
    d.rounded_rectangle(P(W0 - 44 - tw - 40, y, W0 - 44, y + 46), radius=23 * S, fill=fill)
    d.text(P(W0 - 44 - tw - 20, y + 23), text, font=tf, fill=col, anchor="lm")


def _place(img, prod, cx, cy, mw, mh):
    pr = _scaled(prod, mw, mh)
    img.alpha_composite(pr, (int(cx * S - pr.width / 2), int(cy * S - pr.height / 2)))
    return pr.width / S, pr.height / S


def _chip(d, cx, y, name, price, regular, fill, col, nmax=300):
    nf = fit(d, name, "Poppins-Bold.ttf", 22, nmax); pt = tk(price); pf = f("Poppins-Bold.ttf", 30)
    w = max(d.textlength(name, font=nf), d.textlength(pt, font=pf)) / S + 40
    d.rounded_rectangle(P(cx - w / 2, y, cx + w / 2, y + 86), radius=18 * S, fill=fill)
    d.text(P(cx, y + 24), name, font=nf, fill=col, anchor="mm")
    d.text(P(cx, y + 60), pt, font=pf, fill=col, anchor="mm")


# ---------------- Template AC: sunburst retro poster ----------------
def template_ac(p):
    bg = p.get("bg", (255, 214, 120)); ray = p.get("ray", mix(bg, WHITE, 0.35)); band = p.get("band", (36, 52, 110))
    acc = p.get("acc", (232, 74, 60)); ink = p.get("ink", INK); hl = p.get("hl", (255, 214, 90))
    cream = p.get("cream", (255, 249, 238))
    img = Image.new("RGBA", (W, H), bg + (255,)); d = ImageDraw.Draw(img)
    CX, CY = 540, p.get("cy", 600)
    n = 18
    for i in range(n):
        a0 = 2 * math.pi * i / n; a1 = a0 + math.pi / n; R = 1600
        d.polygon([P(CX, CY), P(CX + R * math.cos(a0), CY + R * math.sin(a0)), P(CX + R * math.cos(a1), CY + R * math.sin(a1))], fill=ray)
    # headline band
    BH = 290
    d.rectangle(P(0, 0, W0, BH), fill=band)
    for k in range(0, W0, 36): d.ellipse(P(k + 6, BH - 12, k + 30, BH + 12), fill=band)  # scalloped edge
    h1, h2 = p["head"]; ft = f("Poppins-Bold.ttf", p.get("hsize", 62))
    for l in (h1, h2): ft = fit(d, l, "Poppins-Bold.ttf", ft.size / S, 960)
    d.text(P(60, 128), h1, font=ft, fill=WHITE); d.text(P(60, 128 + ft.size / S * 1.1), h2, font=ft, fill=hl)
    items = p.get("items")
    if items:
        for it in items:
            cx, cy = it["cx"], it.get("cy", CY)
            rr = it.get("r", 170)
            d.ellipse(P(cx - rr, cy - rr, cx + rr, cy + rr), fill=cream)
            d.ellipse(P(cx - rr - 14, cy - rr - 14, cx + rr + 14, cy + rr + 14), outline=cream, width=4 * S)
            _place(img, it["img"], cx, cy + it.get("dy", 0), it["mw"], it["mh"]); d = ImageDraw.Draw(img)
            _chip(d, cx, cy + rr + 24, it["name"], it["price"], it.get("regular"), band, WHITE, it.get("nmax", 300))
        d = ImageDraw.Draw(img)
    else:
        R = p.get("r", 250)
        d.ellipse(P(CX - R - 22, CY - R - 22, CX + R + 22, CY + R + 22), outline=cream, width=6 * S)
        d.ellipse(P(CX - R, CY - R, CX + R, CY + R), fill=p.get("disc", cream))
        _place(img, p["img"], CX + p.get("dx", 0), CY + p.get("dy", 0), p.get("maxw", 420), p.get("maxh", 440))
        d = ImageDraw.Draw(img)
        bx, by = p.get("bx", 880), p.get("by", CY + 190)
        _price_burst(d, bx, by, p.get("br", 138), acc, WHITE, p["price"], p.get("regular"), p.get("label", "ONLY"))
        st = p.get("sticker")
        if st:
            sf = fit(d, st, "Poppins-Bold.ttf", 22, 330); sw = d.textlength(st, font=sf) / S + 44
            sx, sy = p.get("sx", 60), p.get("sy", CY - 250)
            d.rounded_rectangle(P(sx, sy, sx + sw, sy + 52), radius=26 * S, fill=ink)
            d.text(P(sx + sw / 2, sy + 26), st, font=sf, fill=WHITE, anchor="mm")
    # cream info card
    y0 = p.get("card_y", 920); X0, X1, Y1 = 44, W0 - 44, H0 - 92
    d.rounded_rectangle(P(X0 + 8, y0 + 8, X1 + 8, Y1 + 8), radius=26 * S, fill=band)
    d.rounded_rectangle(P(X0, y0, X1, Y1), radius=26 * S, fill=cream)
    y = y0 + 30
    ftt, tl = wrap(d, p["title"], "Poppins-Bold.ttf", 36, X1 - X0 - 80, 1)
    d.text(P(X0 + 40, y), tl[0], font=ftt, fill=ink); y += ftt.size / S * 1.45
    if p.get("bn"):
        fb = _bn_fit(d, p["bn"], 30, X1 - X0 - 80)
        d.text(P(X0 + 40, y + 18), p["bn"], font=fb, fill=acc, anchor="lm"); y += 52
    feats = p.get("feats", [])[:4]; cw = (X1 - X0 - 80) / 2
    rowh = (Y1 - 22 - y) / 2
    for i, fe in enumerate(feats):
        fx = X0 + 40 + (i % 2) * cw; fy = y + (i // 2) * rowh + rowh / 2
        check_icon(d, fx + 16, fy, 16, band, WHITE)
        d.text(P(fx + 44, fy), fe, font=fit(d, fe, "Poppins-Medium.ttf", 26, cw - 56), fill=ink, anchor="lm")
    d.rectangle(P(0, H0 - 62, W0, H0), fill=band)
    d.text(P(W0 / 2, H0 - 31), FOOT, font=f("Poppins-Bold.ttf", 24), fill=WHITE, anchor="mm")
    logo_chip(img, 44, 34, 110); d = ImageDraw.Draw(img)
    _tagpill(d, p["tag"], hl, band, 40)
    return rf.finish(img, p["out"])


# ---------------- Template AD: comic panel ----------------
def _halftone(d, box, base, dot, step=26, r=5):
    x0, y0, x1, y1 = box
    d.rectangle(P(x0, y0, x1, y1), fill=base)
    row = 0
    for yy in range(int(y0) + 10, int(y1) - 4, step):
        off = (step / 2) if row % 2 else 0
        for xx in range(int(x0 + 10 + off), int(x1) - 4, step):
            d.ellipse(P(xx - r, yy - r, xx + r, yy + r), fill=dot)
        row += 1


def template_ad(p):
    paper = p.get("paper", (252, 246, 232)); ink = p.get("ink", (24, 24, 32)); panel = p.get("panel", (120, 200, 230))
    acc = p.get("acc", (236, 56, 72)); yel = p.get("yel", (255, 216, 64)); bw = 7
    img = Image.new("RGBA", (W, H), paper + (255,)); d = ImageDraw.Draw(img)
    # panel 1
    X0, Y0, X1, Y1 = 40, 130, W0 - 40, p.get("p1y", 830)
    _halftone(d, (X0, Y0, X1, Y1), panel, mix(panel, WHITE, 0.3))
    # action lines from the product centre (flat, behind product)
    CX, CY = p.get("cx", 560), p.get("cy", 520)
    for i in range(14):
        a = 2 * math.pi * i / 14 + 0.12
        r0, r1 = 300, 900
        d.line(P(CX + r0 * math.cos(a), CY + r0 * math.sin(a), CX + r1 * math.cos(a), CY + r1 * math.sin(a)), fill=mix(panel, WHITE, 0.55), width=6 * S)
    items = p.get("items")
    if items:
        for it in items:
            _place(img, it["img"], it["cx"], it.get("cy", CY + 20), it["mw"], it["mh"])
        d = ImageDraw.Draw(img)
        for it in items:
            _chip(d, it["cx"], it.get("chy", Y1 - 196), it["name"], it["price"], it.get("regular"), ink, WHITE, it.get("nmax", 260))
    else:
        _place(img, p["img"], CX + p.get("dx", 0), CY + p.get("dy", 0), p.get("maxw", 460), p.get("maxh", 470))
        d = ImageDraw.Draw(img)
    # repaint the outside of the panel (action lines overflow) then the thick border
    d.rectangle(P(0, 0, W0, Y0), fill=paper); d.rectangle(P(0, Y1, W0, H0), fill=paper)
    d.rectangle(P(0, 0, X0, H0), fill=paper); d.rectangle(P(X1, 0, W0, H0), fill=paper)
    d.rectangle(P(X0, Y0, X1, Y1), outline=ink, width=bw * S)
    # caption box (tag)
    tf = f("Poppins-Bold.ttf", 22); tw = d.textlength(p["tag"], font=tf) / S
    d.rectangle(P(X0, Y0, X0 + tw + 44, Y0 + 54), fill=yel, outline=ink, width=4 * S)
    d.text(P(X0 + 22, Y0 + 27), p["tag"], font=tf, fill=ink, anchor="lm")
    # speech bubble hook
    h1, h2 = p["head"]; hf = f("Poppins-Bold.ttf", p.get("hsize", 44))
    for l in (h1, h2): hf = fit(d, l, "Poppins-Bold.ttf", hf.size / S, p.get("bw", 420))
    tw = max(d.textlength(h1, font=hf), d.textlength(h2, font=hf)) / S
    bx0, by0 = p.get("bx", X0 + 30), Y0 + 80; bx1 = bx0 + tw + 64; by1 = by0 + hf.size / S * 2.3 + 40
    tx, ty = p.get("tail", (bx0 + (bx1 - bx0) * 0.7, by1 + 70))
    tail = [P(bx0 + (bx1 - bx0) * 0.5, by1 - 6), P(bx0 + (bx1 - bx0) * 0.68, by1 - 6), P(tx, ty)]
    d.polygon(tail, fill=WHITE, outline=ink, width=5 * S)
    d.rounded_rectangle(P(bx0, by0, bx1, by1), radius=40 * S, fill=WHITE, outline=ink, width=5 * S)
    d.polygon([P(bx0 + (bx1 - bx0) * 0.5 + 6, by1 - 8), P(bx0 + (bx1 - bx0) * 0.68 - 6, by1 - 8), P(tx - 2, ty - 14)], fill=WHITE)
    d.text(P(bx0 + 32, by0 + 20), h1, font=hf, fill=ink)
    d.text(P(bx0 + 32, by0 + 20 + hf.size / S * 1.12), h2, font=hf, fill=acc)
    if p.get("sticker"):
        st = p["sticker"]; sf = fit(d, st, "Poppins-Bold.ttf", 22, 520); sw = d.textlength(st, font=sf) / S + 40
        sx1, sy0 = X1, 44
        d.rectangle(P(sx1 - sw, sy0, sx1, sy0 + 50), fill=yel, outline=ink, width=4 * S)
        d.text(P(sx1 - sw / 2, sy0 + 25), st, font=sf, fill=ink, anchor="mm")
    # title strip at the bottom of panel 1
    ftt, tl = wrap(d, p["title"], "Poppins-Bold.ttf", 32, X1 - X0 - 80, 1)
    th = ftt.size / S + 34
    d.rectangle(P(X0, Y1 - th, X1, Y1), fill=ink)
    d.text(P(W0 / 2, Y1 - th / 2), tl[0], font=ftt, fill=WHITE, anchor="mm")
    # bottom panels
    Y2, Y3 = Y1 + 26, H0 - 96
    SPL = p.get("split", 640)
    d.rectangle(P(X0, Y2, SPL, Y3), fill=WHITE, outline=ink, width=bw * S)
    y = Y2 + 26
    if p.get("bn"):
        fb = _bn_fit(d, p["bn"], 29, SPL - X0 - 60)
        d.text(P(X0 + 30, y + 20), p["bn"], font=fb, fill=acc, anchor="lm"); y += 56
        d.line(P(X0 + 30, y, SPL - 30, y), fill=mix(WHITE, ink, 0.15), width=2 * S); y += 6
    feats = p.get("feats", [])[:4]; rowh = (Y3 - 16 - y) / max(1, len(feats))
    for i, fe in enumerate(feats):
        fy = y + rowh * i + rowh / 2
        check_icon(d, X0 + 46, fy, 16, ink, yel)
        d.text(P(X0 + 76, fy), fe, font=fit(d, fe, "Poppins-Medium.ttf", 26, SPL - X0 - 100), fill=ink, anchor="lm")
    PX0 = SPL + 22
    _halftone(d, (PX0, Y2, X1, Y3), yel, mix(yel, WHITE, 0.45), step=22, r=4)
    d.rectangle(P(PX0, Y2, X1, Y3), outline=ink, width=bw * S)
    pcx, pcy = (PX0 + X1) / 2, (Y2 + Y3) / 2
    pr = min((X1 - PX0) / 2 - 18, (Y3 - Y2) / 2 - 14)
    _price_burst(d, pcx, pcy, pr, acc, WHITE, p["price"], p.get("regular"), p.get("label", "ONLY"), outline=ink, n=14)
    d.text(P(W0 / 2, H0 - 50), FOOT, font=f("Poppins-Bold.ttf", 25), fill=ink, anchor="mm")
    logo_chip(img, 40, 30, 110, fill=WHITE); d = ImageDraw.Draw(img)
    return rf.finish(img, p["out"])


TEMPLATES14 = {"AC": template_ac, "AD": template_ad}
