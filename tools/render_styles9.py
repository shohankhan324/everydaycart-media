"""Style set 9 (added 14 Nov 2026): S order slip (bold colour poster, product on a flat disc on the left, tilted white
paper receipt on the right with zigzag edge, ticked feature rows, TOTAL price, barcode; collection mode lists each item
on the slip and stacks the products), T app card (pastel background, big white shopping-app product card with a
tinted photo panel, hook bubble, carousel dots, feature chips, price and a flat "Add to cart" button; collection mode
shows two product tiles). Flat only (no gradients, no blur), Poppins + Hind Siliguri, small logo chip top left."""
import random
from PIL import Image, ImageDraw
import render_flat as rf
from render_flat import P, f, fit, wrap, tk, S, W, H, W0, H0, INK, check_icon
from render_styles4 import logo_chip, mix, strike
from render_styles6 import fbn, _layer
from render_styles8 import _center, _tag, _bn_fit

WHITE = (255, 255, 255)


def _dash(d, x0, x1, y, col, dash=10, gap=8, width=2):
    x = x0
    while x < x1:
        d.line(P(x, y, min(x + dash, x1), y), fill=col, width=width * S); x += dash + gap


def _barcode(d, x0, y0, w, h, col, seed=7):
    rnd = random.Random(seed); x = x0
    while x < x0 + w - 6:
        bw = rnd.choice([2, 2, 3, 4, 6]); d.rectangle(P(x, y0, x + bw, y0 + h), fill=col); x += bw + rnd.choice([3, 4, 5, 7])


# ---------------- Template S: order slip ----------------
def template_s(p):
    bg = p.get("bg", (30, 60, 110)); acc = p.get("acc", (255, 200, 60)); ink = p.get("ink", INK)
    paper = p.get("paper", (255, 253, 247))
    img = Image.new("RGBA", (W, H), bg + (255,)); d = ImageDraw.Draw(img)
    # flat diagonal stripes in the top-right corner for texture
    sc = mix(bg, WHITE, 0.07)
    for k in range(0, 900, 70):
        d.polygon([P(W0 - 520 + k, 0), P(W0 - 490 + k, 0), P(W0 - 490 + k - 380, 380), P(W0 - 520 + k - 380, 380)], fill=sc)
    # headline (left)
    head = p["head"]; hx = 56; hy = p.get("hy", 160); hw = p.get("hw", 520)
    ft = f("Poppins-Bold.ttf", p.get("hsize", 58))
    for l in head: ft = fit(d, l, "Poppins-Bold.ttf", ft.size / S, hw)
    for i, l in enumerate(head):
        d.text(P(hx, hy + i * ft.size / S * 1.12), l, font=ft, fill=acc if i == len(head) - 1 else WHITE)
    # product(s) on flat disc
    cx, cy, r = p.get("cx", 320), p.get("cy", 760), p.get("r", 250)
    d.ellipse(P(cx - r, cy - r, cx + r, cy + r), fill=mix(bg, WHITE, 0.13))
    d.ellipse(P(cx - r * 0.78, cy - r * 0.78, cx + r * 0.78, cy + r * 0.78), fill=mix(bg, WHITE, 0.2))
    items = p.get("items")
    if items:
        for (pi, ox, oy, mw, mh) in p["place"]:
            _center(img, pi, cx + ox, cy + oy, mw, mh)
    else:
        _center(img, p["img"], cx + p.get("dx", 0), cy + p.get("dy", 0), p.get("maxw", 500), p.get("maxh", 560))
    # receipt layer (drawn flat, tilted)
    RW, RH = p.get("rw", 430), p.get("rh", 930)

    def draw(L):
        dl = ImageDraw.Draw(L)
        z = 14
        dl.rectangle(P(0, 0, RW, RH - z), fill=paper)
        for x in range(0, RW, 2 * z):   # zigzag bottom edge
            dl.polygon([P(x, RH - z), P(x + z, RH), P(x + 2 * z, RH - z)], fill=paper)
        dl.rectangle(P(0, 0, RW, 14), fill=acc)
        mute = mix(paper, ink, 0.5); line = mix(paper, ink, 0.3)
        dl.text(P(RW / 2, 62), "ORDER SLIP", font=f("Poppins-Bold.ttf", 30), fill=ink, anchor="mm")
        dl.text(P(RW / 2, 98), p.get("slipno", "everydaycart.online"), font=f("Poppins-Medium.ttf", 18), fill=mute, anchor="mm")
        _dash(dl, 26, RW - 26, 128, line)
        y = 150
        if items:
            for (name, price) in items:
                ftn, nl = wrap(dl, name, "Poppins-Bold.ttf", 25, RW - 56, 2)
                for l in nl: dl.text(P(28, y), l, font=ftn, fill=ink); y += ftn.size / S * 1.2
                pt = tk(price); dl.text(P(RW - 28, y + 6), pt, font=f("Poppins-Bold.ttf", 30), fill=bg, anchor="ra"); y += 56
                for fe in p.get("ifeats", {}).get(name, []):
                    check_icon(dl, 40, y + 15, 12, acc, ink)
                    dl.text(P(64, y + 15), fe, font=fit(dl, fe, "Poppins-Medium.ttf", 21, RW - 92), fill=ink, anchor="lm"); y += 38
                y += 14; _dash(dl, 26, RW - 26, y, line); y += 22
        else:
            ftn, nl = wrap(dl, p["title"], "Poppins-Bold.ttf", 30, RW - 56, 3)
            for l in nl: dl.text(P(28, y), l, font=ftn, fill=ink); y += ftn.size / S * 1.22
            y += 12; _dash(dl, 26, RW - 26, y, line); y += 26
            for fe in p["feats"][:5]:
                fs = 23; ftf, fl = wrap(dl, fe, "Poppins-Medium.ttf", fs, RW - 96, 2)
                check_icon(dl, 42, y + ftf.size / S * 0.62, 14, acc, ink)
                for l in fl: dl.text(P(70, y), l, font=ftf, fill=ink); y += ftf.size / S * 1.25
                y += 16
            y += 2; _dash(dl, 26, RW - 26, y, line); y += 24
        # totals
        if p.get("regular", 0) > p.get("price", 0):
            dl.text(P(28, y), "Regular", font=f("Poppins-Medium.ttf", 22), fill=mute)
            rt = tk(p["regular"]); rfo = f("Poppins-Medium.ttf", 22); rw = dl.textlength(rt, font=rfo) / S
            strike(dl, RW - 28 - rw, y, rt, rfo, mute); y += 40
        if p.get("price"):
            dl.text(P(28, y + 26), p.get("total_label", "TOTAL"), font=f("Poppins-Bold.ttf", 26), fill=ink, anchor="lm")
            pt = (p.get("from", "") + tk(p["price"])).strip()
            dl.text(P(RW - 28, y + 26), pt, font=fit(dl, pt, "Poppins-Bold.ttf", 50, RW - 170), fill=bg, anchor="rm"); y += 70
            _dash(dl, 26, RW - 26, y, line)
        y += 24
        _barcode(dl, 50, y, RW - 100, 62, ink, seed=len(p["out"]))
        dl.text(P(RW / 2, y + 92), "Inbox us to order", font=f("Poppins-Medium.ttf", 19), fill=mute, anchor="mm")
        return y + 130
    if "rh" not in p:   # measure the slip content once, then size the paper to fit
        RH = 3000; RH = min(draw(Image.new("RGBA", P(RW, 3000), (0, 0, 0, 0))), p.get("rhmax", 1000))
    rx, ry = p.get("rx", 610), p.get("ry", 150)
    _layer(img, (rx, ry, rx + RW, ry + RH), draw, p.get("rang", -3))
    d = ImageDraw.Draw(img)
    # Bangla strip at the bottom
    by = H0 - 150
    d.rectangle(P(0, by, W0, H0), fill=mix(bg, (0, 0, 0), 0.25))
    if p.get("bn"):
        fb = _bn_fit(d, p["bn"], 38, 960)
        d.text(P(W0 / 2, by + 52), p["bn"], font=fb, fill=acc, anchor="mm")
    d.text(P(W0 / 2, H0 - 42), "everydaycart.online", font=f("Poppins-Bold.ttf", 28), fill=WHITE, anchor="mm")
    logo_chip(img, 44, 44, 120); d = ImageDraw.Draw(img)
    _tag(img, d, p["tag"], acc, ink)
    return rf.finish(img, p["out"])


# ---------------- Template T: app card ----------------
def _heart(d, cx, cy, s, col):
    d.ellipse(P(cx - s, cy - s * 0.7, cx, cy + s * 0.3), fill=col)
    d.ellipse(P(cx, cy - s * 0.7, cx + s, cy + s * 0.3), fill=col)
    d.polygon([P(cx - s * 0.96, cy - s * 0.05), P(cx + s * 0.96, cy - s * 0.05), P(cx, cy + s * 0.95)], fill=col)


def _cart(d, cx, cy, s, col):
    w = max(2, int(s * 0.16 * S))
    d.line([P(cx - s * 1.0, cy - s * 0.75), P(cx - s * 0.7, cy - s * 0.75), P(cx - s * 0.45, cy + s * 0.35), P(cx + s * 0.75, cy + s * 0.35)],
           fill=col, width=w, joint="curve")
    d.polygon([P(cx - s * 0.62, cy - s * 0.5), P(cx + s * 0.95, cy - s * 0.5), P(cx + s * 0.75, cy + s * 0.15), P(cx - s * 0.45, cy + s * 0.15)], fill=col)
    for x in (cx - s * 0.35, cx + s * 0.62):
        d.ellipse(P(x - s * 0.16, cy + s * 0.55, x + s * 0.16, cy + s * 0.87), fill=col)


def template_t(p):
    bg = p.get("bg", (255, 228, 214)); acc = p.get("acc", (240, 90, 60)); ink = p.get("ink", INK)
    panel = p.get("panel", mix(bg, WHITE, 0.35)); acc2 = p.get("acc2", ink)
    img = Image.new("RGBA", (W, H), bg + (255,)); d = ImageDraw.Draw(img)
    # flat background blobs
    d.ellipse(P(-160, 980, 260, 1400), fill=mix(bg, acc, 0.16))
    d.ellipse(P(860, -120, 1240, 260), fill=mix(bg, acc, 0.16))
    X0, Y0, X1, Y1 = 56, 138, W0 - 56, 1258
    d.rounded_rectangle(P(X0 + 10, Y0 + 14, X1 + 10, Y1 + 14), radius=56 * S, fill=mix(bg, ink, 0.18))   # flat offset
    d.rounded_rectangle(P(X0, Y0, X1, Y1), radius=56 * S, fill=WHITE)
    # top bar
    d.text(P(X0 + 44, Y0 + 58), "<", font=f("Poppins-Bold.ttf", 40), fill=ink, anchor="mm")
    d.text(P((X0 + X1) / 2, Y0 + 58), p.get("bar", "Product details"), font=f("Poppins-Bold.ttf", 26), fill=ink, anchor="mm")
    d.ellipse(P(X1 - 74, Y0 + 28, X1 - 18, Y0 + 84), fill=mix(WHITE, acc, 0.14)); _heart(d, X1 - 46, Y0 + 56, 15, acc)
    # photo panel
    PX0, PY0, PX1, PY1 = X0 + 30, Y0 + 106, X1 - 30, p.get("py1", 730)
    d.rounded_rectangle(P(PX0, PY0, PX1, PY1), radius=40 * S, fill=panel)
    d.ellipse(P((PX0 + PX1) / 2 - 250, (PY0 + PY1) / 2 - 250 + 14, (PX0 + PX1) / 2 + 250, (PY0 + PY1) / 2 + 250 + 14), fill=mix(panel, WHITE, 0.45))
    items = p.get("items")
    if items:
        n = len(items); sw = (PX1 - PX0) / n
        for i, (pi, name, price, reg, mw, mh) in enumerate(items):
            cx = PX0 + sw * (i + 0.5)
            _center(img, pi, cx, (PY0 + PY1) / 2 - 10 + p.get("dy", 0), mw, mh)
        d = ImageDraw.Draw(img)
        for i, (pi, name, price, reg, mw, mh) in enumerate(items):
            cx = PX0 + sw * (i + 0.5); lt = f"{name}  {tk(price)}"
            lf = fit(d, lt, "Poppins-Bold.ttf", 23, sw - 50); lw = d.textlength(lt, font=lf) / S
            d.rounded_rectangle(P(cx - lw / 2 - 20, PY1 - 66, cx + lw / 2 + 20, PY1 - 22), radius=22 * S, fill=WHITE)
            d.text(P(cx, PY1 - 44), lt, font=lf, fill=ink, anchor="mm")
    else:
        _center(img, p["img"], (PX0 + PX1) / 2 + p.get("dx", 0), (PY0 + PY1) / 2 + 10 + p.get("dy", 0), p.get("maxw", 560), p.get("maxh", 500))
    d = ImageDraw.Draw(img)
    # hook bubble on the photo panel (top-left)
    if p.get("hook"):
        hf = fit(d, p["hook"], "Poppins-Bold.ttf", 30, 560); hw = d.textlength(p["hook"], font=hf) / S
        bx, byy = PX0 + 26, PY0 + 26
        d.rounded_rectangle(P(bx, byy, bx + hw + 44, byy + 62), radius=31 * S, fill=acc2)
        d.polygon([P(bx + 40, byy + 60), P(bx + 70, byy + 60), P(bx + 38, byy + 86)], fill=acc2)
        d.text(P(bx + 22, byy + 31), p["hook"], font=hf, fill=WHITE, anchor="lm")
    # carousel dots
    dy_ = PY1 + 28
    for k in range(4):
        x = (X0 + X1) / 2 - 45 + k * 30
        if k == 0: d.rounded_rectangle(P(x - 14, dy_ - 6, x + 14, dy_ + 6), radius=6 * S, fill=acc)
        else: d.ellipse(P(x - 6, dy_ - 6, x + 6, dy_ + 6), fill=mix(WHITE, ink, 0.2))
    y = PY1 + 60
    # category chip + title
    cf = f("Poppins-Bold.ttf", 20); cw = d.textlength(p["tag"], font=cf) / S
    d.rounded_rectangle(P(PX0 + 6, y, PX0 + 6 + cw + 36, y + 40), radius=20 * S, fill=mix(WHITE, acc, 0.14))
    d.text(P(PX0 + 24, y + 20), p["tag"], font=cf, fill=acc, anchor="lm")
    y += 58
    ft, tl = wrap(d, p["title"], "Poppins-Bold.ttf", 40, PX1 - PX0 - 10, 2)
    for l in tl: d.text(P(PX0 + 6, y), l, font=ft, fill=ink); y += ft.size / S * 1.18
    if p.get("bn"):
        fb = _bn_fit(d, p["bn"], 30, PX1 - PX0 - 10)
        d.text(P(PX0 + 6, y + 4), p["bn"], font=fb, fill=mix(ink, WHITE, 0.25)); y += 54
    y += 8
    # feature chips (wrap)
    x = PX0 + 6; chf = f("Poppins-SemiBold.ttf", 22) if _has("Poppins-SemiBold.ttf") else f("Poppins-Medium.ttf", 22)
    rows = 0
    for fe in p.get("feats", []):
        tw = d.textlength(fe, font=chf) / S; w = tw + 64
        if x + w > PX1:
            x = PX0 + 6; y += 58; rows += 1
            if rows >= p.get("chip_rows", 2) or y + 46 > Y1 - 150: break
        d.rounded_rectangle(P(x, y, x + w, y + 46), radius=23 * S, fill=WHITE, outline=mix(WHITE, ink, 0.18), width=2 * S)
        check_icon(d, x + 24, y + 23, 10, acc, WHITE)
        d.text(P(x + 42, y + 23), fe, font=chf, fill=ink, anchor="lm"); x += w + 12
    # bottom row: price + button
    by = Y1 - 112
    d.line(P(X0 + 30, by - 22, X1 - 30, by - 22), fill=mix(WHITE, ink, 0.1), width=2 * S)
    if p.get("price"):
        d.text(P(PX0 + 6, by + 4), p.get("plabel", "Price"), font=f("Poppins-Medium.ttf", 22), fill=mix(ink, WHITE, 0.4))
        pt = (p.get("from", "") + tk(p["price"])).strip(); pf = fit(d, pt, "Poppins-Bold.ttf", 52, 300)
        d.text(P(PX0 + 6, by + 36), pt, font=pf, fill=ink)
        if p.get("regular", 0) > p["price"]:
            pw = d.textlength(pt, font=pf) / S; rt = tk(p["regular"]); rfo = f("Poppins-Regular.ttf", 24)
            strike(d, PX0 + 22 + pw, by + 58, rt, rfo, mix(ink, WHITE, 0.45))
    btw = 330; bx1 = PX1; bx0 = bx1 - btw
    d.rounded_rectangle(P(bx0, by + 6, bx1, by + 90), radius=42 * S, fill=acc)
    _cart(d, bx0 + 62, by + 46, 22, WHITE)
    d.text(P(bx0 + 98, by + 48), p.get("btn", "Add to cart"), font=f("Poppins-Bold.ttf", 30), fill=WHITE, anchor="lm")
    # outside footer
    d.text(P(W0 / 2, H0 - 46), "everydaycart.online  |  Inbox us to order", font=f("Poppins-Bold.ttf", 25), fill=mix(bg, ink, 0.75), anchor="mm")
    logo_chip(img, 44, 34, 110)
    return rf.finish(img, p["out"])


def _has(name):
    import os
    return os.path.exists(rf.G + name)


TEMPLATES9 = {"S": template_s, "T": template_t}
