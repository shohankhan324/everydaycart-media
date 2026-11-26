"""Style set 21 (added 26 Nov 2026):
AQ checkerboard blob poster (retro two tone checkerboard on the top part, a big cream organic blob made of overlapping
circles with a thick ink outline holding the product, a round price bubble overlapping the blob's lower right edge, a
small rotated spec sticker on the upper left of the blob, chunky two line headline on an ink band; collection mode puts
two blobs side by side with name pills; solid colour info panel below with Bangla line, title and tick rows),
AR crossing tape banners (solid colour poster, the product large in the middle on a flat oval floor, two long diagonal
tapes with repeated keyword text crossing behind the product, a straight price tape label in front at the bottom right,
big left aligned headline, white rounded info card at the bottom).
Flat only (no gradients, no blur, no 3D), Poppins + Hind Siliguri, small logo chip in a corner."""
import math
from PIL import Image, ImageDraw
import render_flat as rf
from render_flat import P, f, fit, wrap, tk, S, W, H, W0, H0
from render_styles4 import logo_chip, mix, strike
from render_styles8 import _scaled
from render_styles16 import _bnq, _paste_c
from render_styles19 import _lum, _on, _ticks
from render_styles20 import _put, _tagpill

WHITE = (255, 255, 255)
FOOT = "everydaycart.online  |  Inbox us to order"


def _blob(d, cx, cy, r, fill, ink, ow=7, seed=0):
    """Organic blob: a big circle plus 6 lobes; drawn twice (ink outline bigger, then fill)."""
    lobes = [(math.cos(a) * r * .42, math.sin(a) * r * .42, r * (.62 + .08 * ((k + seed) % 3)))
             for k, a in enumerate([i * math.pi / 3 + seed * .4 for i in range(6)])]
    for grow, col in ((ow, ink), (0, fill)):
        rr = r * .78 + grow; d.ellipse(P(cx - rr, cy - rr, cx + rr, cy + rr), fill=col)
        for (dx, dy, lr) in lobes:
            q = lr + grow; d.ellipse(P(cx + dx - q, cy + dy - q, cx + dx + q, cy + dy + q), fill=col)


def _bubble(img, cx, cy, r, fill, ink, price, regular=None, label="ONLY"):
    d = ImageDraw.Draw(img)
    d.ellipse(P(cx - r - 7, cy - r - 7, cx + r + 7, cy + r + 7), fill=ink)
    d.ellipse(P(cx - r, cy - r, cx + r, cy + r), fill=fill)
    tc = _on(fill); hasr = regular and regular > price
    d.text(P(cx, cy - r * (.46 if hasr else .38)), label, font=f("Poppins-Bold.ttf", r * .2), fill=tc, anchor="mm")
    pt = tk(price); d.text(P(cx, cy - r * (.04 if hasr else -.04)), pt, font=fit(d, pt, "Poppins-Bold.ttf", r * .42, r * 1.55), fill=tc, anchor="mm")
    if hasr:
        rt = "Regular " + tk(regular); rfo = fit(d, rt, "Poppins-Medium.ttf", r * .16, r * 1.3); rw = d.textlength(rt, font=rfo) / S
        strike(d, cx - rw / 2, cy + r * .3, rt, rfo, tc)


def _sticker(img, cx, cy, ang, big_, lab, fill, ink):
    tw_, th_, pad = 180, 104, 20
    L = Image.new("RGBA", P(tw_ + 2 * pad, th_ + 2 * pad), (0, 0, 0, 0)); ld = ImageDraw.Draw(L)
    ld.rounded_rectangle(P(pad - 5, pad - 5, pad + tw_ + 5, pad + th_ + 5), radius=22 * S, fill=ink)
    ld.rounded_rectangle(P(pad, pad, pad + tw_, pad + th_), radius=18 * S, fill=fill)
    tc = _on(fill)
    ld.text(P(pad + tw_ / 2, pad + 42), big_, font=fit(ld, big_, "Poppins-Bold.ttf", 44, tw_ - 24), fill=tc, anchor="mm")
    ld.text(P(pad + tw_ / 2, pad + 82), lab, font=fit(ld, lab, "Poppins-Bold.ttf", 17, tw_ - 24), fill=tc, anchor="mm")
    _paste_c(img, L.rotate(ang, expand=True, resample=Image.BICUBIC), cx, cy)


# ---------------- Template AQ: checkerboard blob poster ----------------
def template_aq(p):
    c1 = p.get("c1", (250, 214, 90)); c2 = p.get("c2", mix(c1, WHITE, 0.45)); ink = p.get("ink", (26, 24, 34))
    acc = p.get("acc", (236, 72, 96)); blobc = p.get("blob", (255, 249, 236)); panel = p.get("panel", (30, 46, 120))
    PY = p.get("panel_y", 1010); cell = p.get("cell", 90)
    img = Image.new("RGBA", (W, H), c1 + (255,)); d = ImageDraw.Draw(img)
    for j in range(0, PY // cell + 1):
        for i in range(0, W0 // cell + 1):
            if (i + j) % 2: d.rectangle(P(i * cell, j * cell, (i + 1) * cell, min(PY, (j + 1) * cell)), fill=c2)
    # headline band
    h1, h2 = p["head"]; hf = f("Poppins-Bold.ttf", p.get("hsize", 64))
    for l in (h1, h2): hf = fit(d, l, "Poppins-Bold.ttf", hf.size / S, W0 - 150)
    lh = hf.size / S * 1.08; hy = 132
    d.rounded_rectangle(P(40, hy - 18, W0 - 40, hy + 2 * lh + 20), radius=30 * S, fill=ink)
    d.text(P(W0 / 2, hy), h1, font=hf, fill=WHITE, anchor="mt")
    d.text(P(W0 / 2, hy + lh), h2, font=hf, fill=p.get("h2c", c1), anchor="mt")
    logo_chip(img, 40, 26, 104, fill=WHITE); d = ImageDraw.Draw(img)
    _tagpill(d, p["tag"], W0 - 40, 34, acc, _on(acc), size=20)
    top = hy + 2 * lh + 20; mid = (top + PY) / 2 + 8
    items = p.get("items")
    if items:
        xs = p.get("xs", [290, 790])
        for k, it in enumerate(items):
            cx = xs[k]; cy = it.get("cy", mid - 36); r = it.get("r", 215)
            _blob(d, cx, cy, r, it.get("blob", blobc), ink, seed=k * 2 + 1)
            _put(img, it["img"], cx + it.get("dx", 0), cy + it.get("dy", 0), it.get("mw", r * 1.25), it.get("mh", r * 1.45), it.get("ang", 0)); d = ImageDraw.Draw(img)
            nm = it["name"]; nf = fit(d, nm, "Poppins-Bold.ttf", 22, 300); pt = tk(it["price"]); pf = f("Poppins-Bold.ttf", 25)
            nw = max(d.textlength(nm, font=nf), d.textlength(pt, font=pf)) / S + 40; ny = cy + r * .98
            d.rounded_rectangle(P(cx - nw / 2 - 4, ny - 4, cx + nw / 2 + 4, ny + 84), radius=22 * S, fill=ink)
            d.rounded_rectangle(P(cx - nw / 2, ny, cx + nw / 2, ny + 80), radius=19 * S, fill=WHITE)
            d.text(P(cx, ny + 24), nm, font=nf, fill=ink, anchor="mm")
            d.text(P(cx, ny + 58), pt, font=pf, fill=acc if _lum(acc) < 190 else ink, anchor="mm")
    else:
        cx = p.get("bcx", W0 / 2 - 30); cy = p.get("bcy", mid); r = p.get("r", 300)
        _blob(d, cx, cy, r, blobc, ink, seed=p.get("seed", 0))
        _put(img, p["img"], cx + p.get("dx", 0), cy + p.get("dy", 0), p.get("maxw", 440), p.get("maxh", 460), p.get("ang", 0)); d = ImageDraw.Draw(img)
        if p.get("spec"):
            _sticker(img, p.get("spec_x", cx - r * .82), p.get("spec_y", cy - r * .62), p.get("spec_ang", -9), *p["spec"], p.get("specc", c1), ink)
        _bubble(img, p.get("bx", cx + r * .88), p.get("by", cy + r * .6), p.get("br", 118), acc, ink, p["price"], p.get("regular"), p.get("plabel", "ONLY"))
    d = ImageDraw.Draw(img)
    d.rectangle(P(0, PY, W0, H0), fill=panel); d.line(P(0, PY, W0, PY), fill=ink, width=6 * S)
    tc = _on(panel); by = PY + 50
    _bnq(d, 44, by, p["bn"], 34, W0 - 100, p.get("bnc", c1 if _lum(panel) < 150 else ink))
    ftt, tl = wrap(d, p["title"], "Poppins-Bold.ttf", 30, W0 - 90, 1)
    d.text(P(44, by + 32), tl[0], font=ftt, fill=tc)
    _ticks(d, p.get("feats", []), by + 88, H0 - 76, acc, ink, chip=WHITE)
    d.text(P(W0 / 2, H0 - 36), FOOT, font=f("Poppins-Bold.ttf", 23), fill=tc, anchor="mm")
    return rf.finish(img, p["out"])


# ---------------- Template AR: crossing tape banners ----------------
def _tape(img, cy, ang, text, fill, ink, h=78, size=30):
    Lw = int(W0 * 1.6); L = Image.new("RGBA", P(Lw, h), fill + (255,)); ld = ImageDraw.Draw(L)
    ld.line(P(0, 4, Lw, 4), fill=ink, width=4 * S); ld.line(P(0, h - 4, Lw, h - 4), fill=ink, width=4 * S)
    tf = f("Poppins-Bold.ttf", size); unit = text + "   •   "
    uw = ld.textlength(unit, font=tf) / S; x = -uw / 2
    while x < Lw:
        ld.text(P(x, h / 2), unit, font=tf, fill=_on(fill), anchor="lm"); x += uw
    _paste_c(img, L.rotate(ang, expand=True, resample=Image.BICUBIC), W0 / 2, cy)


def template_ar(p):
    bg = p.get("bg", (24, 110, 98)); ink = p.get("ink", (22, 22, 30)); t1 = p.get("t1", (255, 214, 64)); t2 = p.get("t2", (255, 120, 150))
    acc = p.get("acc", t1); floor = p.get("floor", mix(bg, (0, 0, 0), 0.16)); CY = p.get("card_y", 1000)
    img = Image.new("RGBA", (W, H), bg + (255,)); d = ImageDraw.Draw(img)
    logo_chip(img, 40, 26, 104, fill=WHITE); d = ImageDraw.Draw(img)
    _tagpill(d, p["tag"], W0 - 40, 34, ink, WHITE, size=20)
    h1, h2 = p["head"]; hf = f("Poppins-Bold.ttf", p.get("hsize", 76))
    for l in (h1, h2): hf = fit(d, l, "Poppins-Bold.ttf", hf.size / S, W0 - 100)
    lh = hf.size / S * 1.04
    d.text(P(48, 116), h1, font=hf, fill=_on(bg)); d.text(P(48, 116 + lh), h2, font=hf, fill=p.get("h2c", t1))
    # two tapes that cross exactly behind the product centre (pcx, tcy), so the crossing is hidden
    a1, a2 = p.get("a1", 11), p.get("a2", -8); tcy = p.get("tcy", 640); dx = p.get("pcx", 470) - W0 / 2
    t1_, t2_ = math.tan(math.radians(a1)), math.tan(math.radians(-a2))
    _tape(img, tcy + t1_ * dx, a1, p["tape1"], t1, ink)
    _tape(img, tcy - t2_ * dx, a2, p["tape2"], t2, ink)
    d = ImageDraw.Draw(img)
    base = p.get("base", 900)
    items = p.get("items")
    if items:
        for it in items:
            w_, h_ = [v / S for v in _scaled(it["img"], it.get("mw", 300), it.get("mh", 420)).size]
            d.ellipse(P(it["cx"] - w_ * .55, base - 22, it["cx"] + w_ * .55, base + 22), fill=floor)
            img.alpha_composite(_scaled(it["img"], it.get("mw", 300), it.get("mh", 420)), (int((it["cx"] - w_ / 2) * S), int((base + 8 - h_) * S))); d = ImageDraw.Draw(img)
            nm = it["name"] + "   " + tk(it["price"]); nf = fit(d, nm, "Poppins-Bold.ttf", 22, 330)
            nw = d.textlength(nm, font=nf) / S + 36; ny = base + 46
            d.rounded_rectangle(P(it["cx"] - nw / 2, ny - 22, it["cx"] + nw / 2, ny + 22), radius=22 * S, fill=WHITE, outline=ink, width=3 * S)
            d.text(P(it["cx"], ny), nm, font=nf, fill=ink, anchor="mm")
    else:
        cx = p.get("pcx", 470); mw, mh = p.get("maxw", 520), p.get("maxh", 520)
        pr = _scaled(p["img"], mw, mh); w_, h_ = pr.width / S, pr.height / S
        if p.get("disc"):   # solid disc behind see-through products so the tapes do not show through
            dcy = base - h_ / 2; dr = min(max(w_, h_) * .5 + 40, CY - 26 - dcy)
            d.ellipse(P(cx - dr - 6, dcy - dr - 6, cx + dr + 6, dcy + dr + 6), fill=ink)
            d.ellipse(P(cx - dr, dcy - dr, cx + dr, dcy + dr), fill=p["disc"])
        d.ellipse(P(cx - w_ * .58, base - 24, cx + w_ * .58, base + 24), fill=floor)
        img.alpha_composite(pr, (int((cx - w_ / 2) * S), int((base + 10 - h_) * S))); d = ImageDraw.Draw(img)
    # straight price label in front
    if p.get("price_label", True):
        px1, py0 = p.get("lx1", W0 - 44), p.get("ly", base - 150); hasr = p.get("regular") and p["regular"] > p["price"]
        pt = tk(p["price"]); pf = f("Poppins-Bold.ttf", 58); pw = d.textlength(pt, font=pf) / S
        lw = max(pw, 190) + 56; lh2 = 150 if hasr else 124
        d.rectangle(P(px1 - lw + 9, py0 + 9, px1 + 9, py0 + lh2 + 9), fill=ink)
        d.rectangle(P(px1 - lw, py0, px1, py0 + lh2), fill=acc)
        tc = _on(acc); lc = px1 - lw / 2
        d.text(P(lc, py0 + 28), p.get("plabel", "ONLY"), font=f("Poppins-Bold.ttf", 21), fill=tc, anchor="mm")
        d.text(P(lc, py0 + 78), pt, font=pf, fill=tc, anchor="mm")
        if hasr:
            rt = "Regular " + tk(p["regular"]); rfo = f("Poppins-Medium.ttf", 20); rw = d.textlength(rt, font=rfo) / S
            strike(d, lc - rw / 2, py0 + 110, rt, rfo, tc)
    # info card
    d.rounded_rectangle(P(32, CY, W0 - 32, H0 - 78), radius=30 * S, fill=WHITE)
    by = CY + 48
    _bnq(d, 64, by, p["bn"], 33, W0 - 140, p.get("bnc", bg if _lum(bg) < 150 else ink))
    ftt, tl = wrap(d, p["title"], "Poppins-Bold.ttf", 29, W0 - 130, 1)
    d.text(P(64, by + 32), tl[0], font=ftt, fill=ink)
    _ticks(d, p.get("feats", []), by + 86, H0 - 100, p.get("tick", bg), ink, x0=56, x1=W0 - 56, chip=mix(WHITE, bg, 0.1))
    d.text(P(W0 / 2, H0 - 40), FOOT, font=f("Poppins-Bold.ttf", 23), fill=_on(bg), anchor="mm")
    return rf.finish(img, p["out"])


TEMPLATES21 = {"AQ": template_aq, "AR": template_ar}
