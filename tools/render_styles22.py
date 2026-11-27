"""Style set 22 (added 27 Nov 2026):
AS vinyl record poster (solid colour poster, the product sits on a big flat vinyl record with groove rings and a
coloured centre label, a flat tonearm reaches in from the upper right, a tilted price label on the lower left of the
record, big left aligned headline, rounded info card with Bangla line, title and tick chips; collection mode puts two
or three smaller records in a row with name and price pills),
AT pillar timeline (left column with a bold headline and a numbered feature timeline 01 to 04 on a vertical line, a
tall rounded colour pillar on the right with a dot pattern holding the product, an ink price band at the foot of the
pillar, white strip at the bottom with the Bangla line and title; collection mode puts two or three pillars in a row
under the headline, each with its own product and price band).
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


def _record(d, cx, cy, r, ink, label, ring=None):
    ring = ring or mix(ink, WHITE, 0.16)
    d.ellipse(P(cx - r, cy - r, cx + r, cy + r), fill=ink)
    k = r * .93
    while k > r * .42:
        d.ellipse(P(cx - k, cy - k, cx + k, cy + k), outline=ring, width=max(1, int(1.6 * S)))
        k -= r * .055
    # flat highlight arcs (two light strokes, no gradient)
    d.arc(P(cx - r * .84, cy - r * .84, cx + r * .84, cy + r * .84), 200, 245, fill=mix(ink, WHITE, 0.32), width=int(5 * S))
    d.arc(P(cx - r * .84, cy - r * .84, cx + r * .84, cy + r * .84), 20, 65, fill=mix(ink, WHITE, 0.32), width=int(5 * S))
    lr = r * .4
    d.ellipse(P(cx - lr, cy - lr, cx + lr, cy + lr), fill=label)
    d.ellipse(P(cx - r * .05, cy - r * .05, cx + r * .05, cy + r * .05), fill=ink)


def _tonearm(d, x0, y0, x1, y1, col, ink):
    d.ellipse(P(x0 - 46, y0 - 46, x0 + 46, y0 + 46), fill=col, outline=ink, width=5 * S)
    d.ellipse(P(x0 - 16, y0 - 16, x0 + 16, y0 + 16), fill=ink)
    d.line(P(x0, y0, x1, y1), fill=ink, width=14 * S)
    d.line(P(x0, y0, x1, y1), fill=col, width=7 * S)
    a = math.atan2(y1 - y0, x1 - x0); hx, hy = x1 + 30 * math.cos(a), y1 + 30 * math.sin(a)
    d.line(P(x1, y1, hx, hy), fill=ink, width=34 * S)
    d.line(P(x1, y1, hx, hy), fill=col, width=24 * S)


def _label(img, cx, cy, ang, price, regular, fill, ink, plabel="ONLY", w=290):
    hasr = regular and regular > price; h = 150 if hasr else 124; pad = 24
    L = Image.new("RGBA", P(w + 2 * pad + 12, h + 2 * pad + 12), (0, 0, 0, 0)); d = ImageDraw.Draw(L)
    d.rounded_rectangle(P(pad + 10, pad + 10, pad + w + 10, pad + h + 10), radius=20 * S, fill=ink)
    d.rounded_rectangle(P(pad, pad, pad + w, pad + h), radius=20 * S, fill=fill, outline=ink, width=4 * S)
    d.ellipse(P(pad + 16, pad + h / 2 - 9, pad + 34, pad + h / 2 + 9), fill=ink)   # tag hole
    tc = _on(fill); c = pad + w / 2 + 16
    d.text(P(c, pad + 26), plabel, font=f("Poppins-Bold.ttf", 20), fill=tc, anchor="mm")
    pt = tk(price); d.text(P(c, pad + 74), pt, font=fit(d, pt, "Poppins-Bold.ttf", 56, w - 84), fill=tc, anchor="mm")
    if hasr:
        rt = "Regular " + tk(regular); rfo = f("Poppins-Medium.ttf", 19); rw = d.textlength(rt, font=rfo) / S
        strike(d, c - rw / 2, pad + 112, rt, rfo, tc)
    _paste_c(img, L.rotate(ang, expand=True, resample=Image.BICUBIC), cx, cy)


# ---------------- Template AS: vinyl record poster ----------------
def template_as(p):
    bg = p.get("bg", (255, 214, 90)); ink = p.get("ink", (24, 24, 32)); acc = p.get("acc", (240, 80, 90))
    lab = p.get("label", acc); arm = p.get("arm", WHITE); CY = p.get("card_y", 1000)
    img = Image.new("RGBA", (W, H), bg + (255,)); d = ImageDraw.Draw(img)
    logo_chip(img, 40, 26, 104, fill=WHITE); d = ImageDraw.Draw(img)
    _tagpill(d, p["tag"], W0 - 40, 34, ink, WHITE, size=20)
    h1, h2 = p["head"]; hf = f("Poppins-Bold.ttf", p.get("hsize", 74))
    for l in (h1, h2): hf = fit(d, l, "Poppins-Bold.ttf", hf.size / S, W0 - 100)
    lh = hf.size / S * 1.04; hy = 112
    d.text(P(48, hy), h1, font=hf, fill=_on(bg)); d.text(P(48, hy + lh), h2, font=hf, fill=p.get("h2c", ink))
    top = hy + 2 * lh + 16
    items = p.get("items")
    if items:
        n = len(items); xs = p.get("xs", [W0 * (i + .5) / n for i in range(n)]); r = p.get("r", 300 if n == 2 else 168)
        cy = p.get("rcy", (top + CY) / 2 - 30)
        for k, it in enumerate(items):
            cx = xs[k]
            _record(d, cx, cy, r, ink, it.get("label", lab))
            _put(img, it["img"], cx + it.get("dx", 0), cy + it.get("dy", 0), it.get("mw", r * 1.3), it.get("mh", r * 1.6), it.get("ang", 0)); d = ImageDraw.Draw(img)
            nm = it["name"]; nf = fit(d, nm, "Poppins-Bold.ttf", 22, min(320, W0 / n - 40)); pt = tk(it["price"]); pf = f("Poppins-Bold.ttf", 27)
            nw = max(d.textlength(nm, font=nf), d.textlength(pt, font=pf)) / S + 40; ny = cy + r + it.get("ny", 22)
            d.rounded_rectangle(P(cx - nw / 2 + 6, ny + 6, cx + nw / 2 + 6, ny + 86), radius=20 * S, fill=ink)
            d.rounded_rectangle(P(cx - nw / 2, ny, cx + nw / 2, ny + 80), radius=20 * S, fill=WHITE, outline=ink, width=3 * S)
            d.text(P(cx, ny + 24), nm, font=nf, fill=ink, anchor="mm")
            d.text(P(cx, ny + 58), pt, font=pf, fill=acc if _lum(acc) < 190 else ink, anchor="mm")
    else:
        cx = p.get("rcx", 590); cy = p.get("rcy", (top + CY) / 2 + 6); r = p.get("r", 315)
        _record(d, cx, cy, r, ink, lab)
        _tonearm(d, p.get("ax0", W0 - 70), p.get("ay0", top + 10), p.get("ax1", cx + r * .74), p.get("ay1", cy - r * .58), arm, ink)
        _put(img, p["img"], cx + p.get("dx", 0), cy + p.get("dy", 0), p.get("maxw", 440), p.get("maxh", 460), p.get("ang", 0)); d = ImageDraw.Draw(img)
        _label(img, p.get("lx", 178), p.get("ly", cy + r * .62), p.get("lang", 7), p["price"], p.get("regular"), p.get("pricec", WHITE), ink, p.get("plabel", "ONLY"))
        d = ImageDraw.Draw(img)
    d.rounded_rectangle(P(32, CY, W0 - 32, H0 - 78), radius=30 * S, fill=p.get("card", WHITE))
    by = CY + 48
    _bnq(d, 64, by, p["bn"], 33, W0 - 140, p.get("bnc", acc if _lum(acc) < 170 else ink))
    ftt, tl = wrap(d, p["title"], "Poppins-Bold.ttf", 29, W0 - 130, 1)
    d.text(P(64, by + 32), tl[0], font=ftt, fill=ink)
    _ticks(d, p.get("feats", []), by + 86, H0 - 100, p.get("tick", acc), ink, x0=56, x1=W0 - 56, chip=mix(WHITE, bg, 0.22))
    d.text(P(W0 / 2, H0 - 40), FOOT, font=f("Poppins-Bold.ttf", 23), fill=_on(bg), anchor="mm")
    return rf.finish(img, p["out"])


# ---------------- Template AT: pillar timeline ----------------
def _pillar(img, x0, y0, x1, y1, col, ink, dots=None):
    d = ImageDraw.Draw(img); rr = min(90, (x1 - x0) / 2)
    d.rounded_rectangle(P(x0 + 12, y0 + 12, x1 + 12, y1 + 12), radius=rr * S, fill=ink)
    d.rounded_rectangle(P(x0, y0, x1, y1), radius=rr * S, fill=col, outline=ink, width=5 * S)
    dots = dots or mix(col, WHITE, 0.3); step = 46
    yy = y0 + 70
    while yy < y1 - 200:
        xx = x0 + 34 + ((yy - y0) // step % 2) * step / 2
        while xx < x1 - 30:
            d.ellipse(P(xx - 5, yy - 5, xx + 5, yy + 5), fill=dots); xx += step
        yy += step


def _band(d, x0, x1, y, price, regular, ink, acc, h=None, pre=""):
    hasr = regular and regular > price; h = h or (122 if hasr else 100)
    d.rounded_rectangle(P(x0, y, x1, y + h), radius=26 * S, fill=ink)
    cx = (x0 + x1) / 2; pt = (pre + " " if pre else "") + tk(price)
    d.text(P(cx, y + (44 if hasr else h / 2)), pt, font=fit(d, pt, "Poppins-Bold.ttf", 54, x1 - x0 - 40), fill=acc, anchor="mm")
    if hasr:
        rt = "Regular " + tk(regular); rfo = fit(d, rt, "Poppins-Medium.ttf", 21, x1 - x0 - 40); rw = d.textlength(rt, font=rfo) / S
        strike(d, cx - rw / 2, y + 80, rt, rfo, WHITE)
    return h


def template_at(p):
    bg = p.get("bg", (250, 240, 228)); ink = p.get("ink", (24, 24, 32)); acc = p.get("acc", (255, 200, 60))
    pc = p.get("pillar", (120, 180, 255)); num = p.get("num", pc); SY = p.get("strip_y", 1070)
    img = Image.new("RGBA", (W, H), bg + (255,)); d = ImageDraw.Draw(img)
    items = p.get("items")
    if items:
        logo_chip(img, 40, 26, 104, fill=WHITE); d = ImageDraw.Draw(img)
        _tagpill(d, p["tag"], W0 - 40, 34, ink, WHITE, size=20)
        h1, h2 = p["head"]; hf = f("Poppins-Bold.ttf", p.get("hsize", 70))
        for l in (h1, h2): hf = fit(d, l, "Poppins-Bold.ttf", hf.size / S, W0 - 100)
        lh = hf.size / S * 1.04
        d.text(P(W0 / 2, 118), h1, font=hf, fill=_on(bg), anchor="mt"); d.text(P(W0 / 2, 118 + lh), h2, font=hf, fill=p.get("h2c", ink), anchor="mt")
        n = len(items); gap = 34; x0 = 52; pw = (W0 - 2 * x0 - gap * (n - 1)) / n; y0 = 118 + 2 * lh + 40; y1 = SY - 40
        for k, it in enumerate(items):
            a = x0 + k * (pw + gap); b = a + pw
            _pillar(img, a, y0, b, y1, it.get("pillar", pc), ink)
            d = ImageDraw.Draw(img)
            bh = 122 if it.get("regular") and it["regular"] > it["price"] else 100
            band_y = y1 - bh - 44
            nm = it["name"]; nf = fit(d, nm, "Poppins-Bold.ttf", 24, pw - 40)
            d.text(P((a + b) / 2, band_y - 30), nm, font=nf, fill=_on(it.get("pillar", pc)), anchor="mm")
            _put(img, it["img"], (a + b) / 2 + it.get("dx", 0), (y0 + band_y - 60) / 2 + it.get("dy", 0), it.get("mw", pw - 50), it.get("mh", band_y - y0 - 110), it.get("ang", 0))
            d = ImageDraw.Draw(img)
            _band(d, a + 30, b - 30, band_y, it["price"], it.get("regular"), ink, acc, bh)
    else:
        logo_chip(img, 40, 26, 104, fill=WHITE); d = ImageDraw.Draw(img)
        px0, px1, py0, py1 = p.get("px0", 560), W0 - 44, 40, SY - 40
        _pillar(img, px0, py0, px1, py1, pc, ink); d = ImageDraw.Draw(img)
        bh = 122 if p.get("regular") and p["regular"] > p["price"] else 100
        band_y = py1 - bh - 50
        _put(img, p["img"], (px0 + px1) / 2 + p.get("dx", 0), (py0 + band_y) / 2 + p.get("dy", 0), p.get("maxw", px1 - px0 - 70), p.get("maxh", band_y - py0 - 90), p.get("ang", 0))
        d = ImageDraw.Draw(img)
        _band(d, px0 + 40, px1 - 40, band_y, p["price"], p.get("regular"), ink, acc, bh, p.get("pre", ""))
        # left column
        lw = px0 - 44 - 30; tf = f("Poppins-Bold.ttf", 20); tw = d.textlength(p["tag"], font=tf) / S
        d.rounded_rectangle(P(44, 140, 44 + tw + 40, 186), radius=23 * S, fill=ink)
        d.text(P(64, 163), p["tag"], font=tf, fill=WHITE, anchor="lm")
        hf, hl = wrap(d, p["headline"], "Poppins-Bold.ttf", p.get("hsize", 64), lw, 3)
        y = 214; lh = hf.size / S * 1.06
        for i, l in enumerate(hl):
            d.text(P(44, y), l, font=hf, fill=p.get("h2c", ink) if i == len(hl) - 1 else _on(bg)); y += lh
        feats = p.get("feats", [])[:4]; ty0 = y + 46; ty1 = SY - 80; step = (ty1 - ty0) / max(1, len(feats))
        cxn = 44 + 34
        d.line(P(cxn, ty0 + 34, cxn, ty0 + step * (len(feats) - 1) + 34), fill=ink, width=4 * S)
        for i, fe in enumerate(feats):
            cy = ty0 + i * step + 34
            d.ellipse(P(cxn - 34, cy - 34, cxn + 34, cy + 34), fill=num, outline=ink, width=4 * S)
            d.text(P(cxn, cy), f"0{i + 1}", font=f("Poppins-Bold.ttf", 24), fill=_on(num), anchor="mm")
            ff, fl = wrap(d, fe, "Poppins-Bold.ttf", 28, lw - 84, 2)
            fh = ff.size / S * 1.12; yy = cy - fh * len(fl) / 2 + fh / 2
            for l in fl:
                d.text(P(cxn + 52, yy), l, font=ff, fill=_on(bg), anchor="lm"); yy += fh
    # bottom strip
    d.rectangle(P(0, SY, W0, H0), fill=p.get("strip", ink))
    sc = p.get("strip", ink); by = SY + 52
    _bnq(d, 48, by, p["bn"], 36, W0 - 110, p.get("bnc", acc))
    ftt, tl = wrap(d, p["title"], "Poppins-Bold.ttf", 30, W0 - 96, 1)
    d.text(P(48, by + 40), tl[0], font=ftt, fill=_on(sc))
    if p.get("chips"):
        x = 48; cf = f("Poppins-Bold.ttf", 21)
        for c in p["chips"]:
            cw = d.textlength(c, font=cf) / S + 36
            d.rounded_rectangle(P(x, by + 104, x + cw, by + 150), radius=23 * S, fill=mix(sc, WHITE, 0.14))
            d.text(P(x + cw / 2, by + 127), c, font=cf, fill=_on(sc), anchor="mm"); x += cw + 12
    d.text(P(W0 / 2, H0 - 34), FOOT, font=f("Poppins-Bold.ttf", 23), fill=acc, anchor="mm")
    return rf.finish(img, p["out"])


TEMPLATES22 = {"AS": template_as, "AT": template_at}
