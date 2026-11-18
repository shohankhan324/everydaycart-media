"""Style set 13 (added 18 Nov 2026):
AA airmail stamp (flat airmail striped border, product on a big perforated postage stamp with its price as the stamp
value, round postmark with the price and wavy cancel lines, Bangla line + ticked features on a white address label;
collection mode puts two stamps side by side, each with its own name and value),
AB callout diagram (flat pastel board with a faint grid, product on a big disc, four numbered feature callouts joined
to the product by dotted leader lines, dark price block, Bangla line, colour footer).
Flat only (no gradients, no blur), Poppins + Hind Siliguri, small logo chip in a corner."""
import math
from PIL import Image, ImageDraw
import render_flat as rf
from render_flat import P, f, fit, wrap, tk, S, W, H, W0, H0, INK, check_icon
from render_styles4 import logo_chip, mix, strike
from render_styles6 import _layer
from render_styles8 import _scaled, _bn_fit

WHITE = (255, 255, 255)
FOOT = "everydaycart.online  |  Inbox us to order"


def _tagpill(d, text, fill, col, y=42):
    tf = f("Poppins-Bold.ttf", 21); tw = d.textlength(text, font=tf) / S
    d.rounded_rectangle(P(W0 - 44 - tw - 40, y, W0 - 44, y + 46), radius=23 * S, fill=fill)
    d.text(P(W0 - 44 - tw - 20, y + 23), text, font=tf, fill=col, anchor="lm")


def _headline(d, head, x, y, c1, c2, size=60, maxw=960):
    h1, h2 = head; ft = f("Poppins-Bold.ttf", size)
    for l in (h1, h2): ft = fit(d, l, "Poppins-Bold.ttf", ft.size / S, maxw)
    d.text(P(x, y), h1, font=ft, fill=c1); d.text(P(x, y + ft.size / S * 1.12), h2, font=ft, fill=c2)
    return y + ft.size / S * 2.3


# ---------------- Template AA: airmail stamp ----------------
def _stamp(L, w, h, prod, mw, mh, photo, ink, acc, value, regular=None, name=None, pdy=0):
    """Perforated postage stamp drawn on layer L (size w x h)."""
    dl = ImageDraw.Draw(L)
    dl.rectangle(P(0, 0, w, h), fill=WHITE)
    # perforations: punch semicircles along every edge
    r = 11; step = 34
    for x in range(int(step / 2), int(w), step):
        dl.ellipse(P(x - r, -r, x + r, r), fill=(0, 0, 0, 0)); dl.ellipse(P(x - r, h - r, x + r, h + r), fill=(0, 0, 0, 0))
    for y in range(int(step / 2), int(h), step):
        dl.ellipse(P(-r, y - r, r, y + r), fill=(0, 0, 0, 0)); dl.ellipse(P(w - r, y - r, w + r, y + r), fill=(0, 0, 0, 0))
    m = 34; bm = 104 if name else 64
    dl.rectangle(P(m, m, w - m, h - bm), fill=photo)
    dl.rectangle(P(m + 10, m + 10, w - m - 10, h - bm - 10), outline=mix(photo, ink, 0.18), width=2 * S)
    pr = _scaled(prod, mw, mh)
    L.alpha_composite(pr, (int(w / 2 * S - pr.width / 2), int(((m + h - bm) / 2 + 14 + pdy) * S - pr.height / 2)))
    dl = ImageDraw.Draw(L)
    # stamp value in the corner of the picture
    if value is None: value = 0
    vt = tk(value); vf = f("Poppins-Bold.ttf", 34 if not name else 28); vw = dl.textlength(vt, font=vf) / S
    if not value: vt = None
    if vt: dl.rounded_rectangle(P(w - m - 22 - vw - 26, m + 20, w - m - 22, m + 72 if not name else m + 64), radius=10 * S, fill=acc)
    if vt: dl.text(P(w - m - 22 - vw / 2 - 13, m + (46 if not name else 42)), vt, font=vf, fill=WHITE, anchor="mm")
    if name:
        nf = fit(dl, name, "Poppins-Bold.ttf", 26, w - 80)
        dl.text(P(w / 2, h - bm + 30), name, font=nf, fill=ink, anchor="mm")
        if regular and regular > value:
            rt = "Regular " + tk(regular); rfo = f("Poppins-Medium.ttf", 20); rw = dl.textlength(rt, font=rfo) / S
            strike(dl, w / 2 - rw / 2, h - bm + 54, rt, rfo, mix(WHITE, ink, 0.5))
    else:
        dl.text(P(w / 2, h - bm / 2 - 2), "EVERYDAY CART  ·  DHAKA", font=f("Poppins-Bold.ttf", 20), fill=mix(WHITE, ink, 0.55), anchor="mm")


def _postmark(img, cx, cy, r, ink, bg, lines, wave_left=260):
    d = ImageDraw.Draw(img)
    # wavy cancel lines running left from the postmark
    for k in range(-2, 3):
        yy = cy + k * 26
        pts = [P(x, yy + 8 * math.sin(x / 26.0)) for x in range(int(cx - r - wave_left), int(cx - r + 6), 4)]
        d.line(pts, fill=ink, width=4 * S)
    d.ellipse(P(cx - r - 8, cy - r - 8, cx + r + 8, cy + r + 8), fill=bg)
    d.ellipse(P(cx - r, cy - r, cx + r, cy + r), outline=ink, width=5 * S)
    d.ellipse(P(cx - r + 16, cy - r + 16, cx + r - 16, cy + r - 16), outline=ink, width=2 * S)
    lab, price, reg = lines
    d.text(P(cx, cy - r * 0.42), lab, font=f("Poppins-Bold.ttf", 22), fill=ink, anchor="mm")
    pf = fit(d, price, "Poppins-Bold.ttf", 58, 2 * r - 60)
    d.text(P(cx, cy + 4), price, font=pf, fill=ink, anchor="mm")
    if reg:
        rfo = f("Poppins-Medium.ttf", 22); rw = d.textlength(reg, font=rfo) / S
        strike(d, cx - rw / 2, cy + r * 0.34, reg, rfo, mix(ink, bg, 0.35))


def template_aa(p):
    bg = p.get("bg", (214, 232, 246)); ink = p.get("ink", (28, 44, 84))
    acc = p.get("acc", (222, 64, 64)); acc2 = p.get("acc2", (40, 84, 170)); photo = p.get("photo", (255, 236, 200))
    img = Image.new("RGBA", (W, H), bg + (255,)); d = ImageDraw.Draw(img)
    # airmail striped border
    B = 22
    d.rectangle(P(0, 0, W0, H0), fill=WHITE)
    stripe = 46
    for k in range(-H0, W0 + H0, stripe):
        col = acc if (k // stripe) % 2 == 0 else acc2
        d.polygon([P(k, 0), P(k + stripe / 2, 0), P(k + stripe / 2 + H0, H0), P(k + H0, H0)], fill=col)
    d.rectangle(P(B, B, W0 - B, H0 - B), fill=bg)
    y = _headline(d, p["head"], 60, 126, ink, acc, p.get("hsize", 58))
    items = p.get("items")
    SY0, SY1 = 312, p.get("sy1", 860)
    if items:
        for it in items:
            w2 = it.get("w", 430); x0 = it["cx"] - w2 / 2; oy = it.get("oy", 0)
            _layer(img, (x0, SY0 + oy, x0 + w2, SY1 + oy),
                   lambda L, it=it, w2=w2: _stamp(L, w2, SY1 - SY0, it["img"], it["mw"], it["mh"], it.get("photo", photo), ink,
                                                   it.get("vcol", acc), it["price"], it.get("regular"), it["name"], it.get("pdy", 0)),
                   it.get("ang", 0))
        if p.get("postmark"):
            _postmark(img, p.get("pmx", 905), p.get("pmy", 250), 92, ink, bg, p["postmark"], wave_left=0)
    else:
        _layer(img, (70, SY0, 610, SY1),
               lambda L: _stamp(L, 540, SY1 - SY0, p["img"], p.get("maxw", 400), p.get("maxh", 400), photo, ink, acc,
                                None, pdy=p.get("pdy", 0)), p.get("ang", -3))
        reg = ("Regular " + tk(p["regular"])) if p.get("regular", 0) > p["price"] else None
        _postmark(img, p.get("pmx", 830), p.get("pmy", 500), 150, ink, bg, (p.get("label", "ONLY"), tk(p["price"]), reg), wave_left=p.get("wave", 90))
        st = p.get("sticker")
        if st:
            d = ImageDraw.Draw(img)
            sf = fit(d, st, "Poppins-Bold.ttf", 24, 300); sw = d.textlength(st, font=sf) / S + 48; sx, sy = p.get("sx", 830), p.get("sy", 740)

            def ds(L):
                dl = ImageDraw.Draw(L); dl.rounded_rectangle(P(0, 0, sw, 58), radius=12 * S, fill=ink)
                dl.text(P(sw / 2, 29), st, font=sf, fill=WHITE, anchor="mm")
            _layer(img, (sx - sw / 2, sy - 29, sx + sw / 2, sy + 29), ds, 4)
    d = ImageDraw.Draw(img)
    # title
    y = SY1 + 36
    ftt, tl = wrap(d, p["title"], "Poppins-Bold.ttf", 36, W0 - 130, 1)
    d.text(P(62, y), tl[0], font=ftt, fill=ink); y += ftt.size / S * 1.5
    # white address label with Bangla line + features
    LX0, LX1, LY1 = 56, W0 - 56, H0 - 100
    d.rounded_rectangle(P(LX0 + 6, y + 8, LX1 + 6, LY1 + 8), radius=18 * S, fill=mix(bg, ink, 0.22))
    d.rounded_rectangle(P(LX0, y, LX1, LY1), radius=18 * S, fill=WHITE)
    d.rectangle(P(LX0 + 26, y + 22, LX0 + 34, LY1 - 22), fill=acc)
    if p.get("bn"):
        fb = _bn_fit(d, p["bn"], 30, LX1 - LX0 - 110)
        d.text(P(LX0 + 60, y + 44), p["bn"], font=fb, fill=acc2, anchor="lm")
        d.line(P(LX0 + 60, y + 80, LX1 - 40, y + 80), fill=mix(WHITE, ink, 0.15), width=2 * S)
    feats = p.get("feats", [])[:4]; cw = (LX1 - LX0 - 100) / 2; fy0 = y + 112
    rowh = (LY1 - 24 - fy0) / 2
    for i, fe in enumerate(feats):
        fx = LX0 + 60 + (i % 2) * cw; fy = fy0 + (i // 2) * rowh + rowh / 2 - 6
        check_icon(d, fx + 17, fy, 17, acc2, WHITE)
        d.text(P(fx + 48, fy), fe, font=fit(d, fe, "Poppins-Medium.ttf", 27, cw - 64), fill=ink, anchor="lm")
    d.text(P(W0 / 2, H0 - 61), FOOT, font=f("Poppins-Bold.ttf", 25), fill=ink, anchor="mm")
    logo_chip(img, 44, 40, 110); d = ImageDraw.Draw(img)
    _tagpill(d, p["tag"], ink, WHITE, 46)
    return rf.finish(img, p["out"])


# ---------------- Template AB: callout diagram ----------------
def template_ab(p):
    bg = p.get("bg", (232, 240, 228)); ink = p.get("ink", INK)
    acc = p.get("acc", (40, 120, 90)); disc = p.get("disc", mix(bg, WHITE, 0.6)); dark = p.get("dark", ink)
    img = Image.new("RGBA", (W, H), bg + (255,)); d = ImageDraw.Draw(img)
    gc = mix(bg, ink, 0.06)
    for x in range(0, W0, 54): d.line(P(x, 0, x, H0), fill=gc, width=1 * S)
    for yy in range(0, H0, 54): d.line(P(0, yy, W0, yy), fill=gc, width=1 * S)
    _headline(d, p["head"], 60, 126, ink, acc, p.get("hsize", 60))
    CX, CY, R = 540, p.get("cy", 640), p.get("r", 262)
    d.ellipse(P(CX - R - 26, CY - R - 26, CX + R + 26, CY + R + 26), outline=mix(acc, bg, 0.55), width=3 * S)
    d.ellipse(P(CX - R, CY - R, CX + R, CY + R), fill=disc)
    pr = _scaled(p["img"], p.get("maxw", 380), p.get("maxh", 400))
    img.alpha_composite(pr, (int((CX + p.get("dx", 0)) * S - pr.width / 2), int((CY + p.get("dy", 0)) * S - pr.height / 2)))
    d = ImageDraw.Draw(img)
    # callouts: (side, pill y, angle of the target point inside the disc)
    feats = p.get("feats", [])[:4]; tr = R * p.get("tr", 0.74)
    spots = [("L", CY - 190, 225), ("R", CY - 190, -45), ("L", CY + 190, 135), ("R", CY + 190, 45)]
    PW, PH = 262, 108
    for i, (fe, (side, py, ang)) in enumerate(zip(feats, spots)):
        x0 = 34 if side == "L" else W0 - 34 - PW
        tx, ty = CX + tr * math.cos(math.radians(ang)), CY + tr * math.sin(math.radians(ang))
        if p.get("tg"): tx, ty = p["tg"][i]
        sx = x0 + PW if side == "L" else x0
        n = 16
        d.line(P(sx, py, tx, ty), fill=WHITE, width=8 * S)
        for k in range(0, n, 2):
            a = k / n; b = (k + 1) / n
            d.line(P(sx + (tx - sx) * a, py + (ty - py) * a, sx + (tx - sx) * b, py + (ty - py) * b), fill=ink, width=3 * S)
        d.ellipse(P(tx - 13, ty - 13, tx + 13, ty + 13), fill=WHITE)
        d.ellipse(P(tx - 9, ty - 9, tx + 9, ty + 9), fill=acc)
        d.rounded_rectangle(P(x0 + 5, py - PH / 2 + 7, x0 + PW + 5, py + PH / 2 + 7), radius=20 * S, fill=mix(bg, ink, 0.2))
        d.rounded_rectangle(P(x0, py - PH / 2, x0 + PW, py + PH / 2), radius=20 * S, fill=WHITE)
        nx = x0 + 34
        d.ellipse(P(nx - 20, py - 20, nx + 20, py + 20), fill=acc)
        d.text(P(nx, py), str(i + 1), font=f("Poppins-Bold.ttf", 22), fill=WHITE, anchor="mm")
        fo, ls = wrap(d, fe, "Poppins-Bold.ttf", 25, PW - 84, 2)
        lh = fo.size / S * 1.2
        for j, l in enumerate(ls):
            d.text(P(x0 + 66, py + (j - (len(ls) - 1) / 2) * lh), l, font=fo, fill=ink, anchor="lm")
    st = p.get("sticker")
    if st:
        sf = fit(d, st, "Poppins-Bold.ttf", 22, 300); sw = d.textlength(st, font=sf) / S + 44
        sy = CY - R - 8
        d.rounded_rectangle(P(CX - sw / 2, sy - 25, CX + sw / 2, sy + 25), radius=25 * S, fill=acc)
        d.text(P(CX, sy), st, font=sf, fill=WHITE, anchor="mm")
    # title + Bangla
    y = CY + R + 52
    ftt, tl = wrap(d, p["title"], "Poppins-Bold.ttf", 38, W0 - 120, 1)
    d.text(P(W0 / 2, y), tl[0], font=ftt, fill=ink, anchor="mt"); y += ftt.size / S * 1.45
    if p.get("bn"):
        fb = _bn_fit(d, p["bn"], 32, W0 - 160)
        d.text(P(W0 / 2, y + 22), p["bn"], font=fb, fill=acc, anchor="mm"); y += 70
    # price block
    pt = tk(p["price"]); pf = f("Poppins-Bold.ttf", 54); pw = d.textlength(pt, font=pf) / S
    lab = p.get("label", "PRICE"); lf = f("Poppins-Bold.ttf", 20); lw = d.textlength(lab, font=lf) / S
    rt = ("Regular " + tk(p["regular"])) if p.get("regular", 0) > p["price"] else None
    rfo = f("Poppins-Medium.ttf", 22); rw = (d.textlength(rt, font=rfo) / S) if rt else 0
    bw = 40 + lw + 24 + pw + (28 + rw if rt else 0) + 40
    bh = 96; bx0 = W0 / 2 - bw / 2; by0 = y + max(14, (H0 - 70 - y - bh) / 2 - 6)
    d.rounded_rectangle(P(bx0, by0, bx0 + bw, by0 + bh), radius=48 * S, fill=dark)
    x = bx0 + 40
    d.text(P(x, by0 + bh / 2), lab, font=lf, fill=mix(WHITE, dark, 0.35), anchor="lm"); x += lw + 24
    d.text(P(x, by0 + bh / 2 + 2), pt, font=pf, fill=WHITE, anchor="lm"); x += pw + 28
    if rt: strike(d, x, by0 + bh / 2 - 14, rt, rfo, mix(WHITE, dark, 0.45))
    d.rectangle(P(0, H0 - 70, W0, H0), fill=acc)
    d.text(P(W0 / 2, H0 - 35), FOOT, font=f("Poppins-Bold.ttf", 25), fill=WHITE, anchor="mm")
    logo_chip(img, 40, 32, 110); d = ImageDraw.Draw(img)
    _tagpill(d, p["tag"], dark, WHITE, 42)
    return rf.finish(img, p["out"])


TEMPLATES13 = {"AA": template_aa, "AB": template_ab}
