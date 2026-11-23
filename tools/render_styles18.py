"""Style set 18 (added 23 Nov 2026):
AK diagonal split poster (bold solid colour top cut by a diagonal edge with a parallel racing stripe, product on a big
flat disc straddling the split, solid price flag and spec stack on the colour side, Bangla line with an accent bar,
numbered feature pills on the paper side, ink footer; collection mode puts each product on its own disc with a
price flag),
AL fanned card stack (soft solid background with big flat circles, two tilted colour cards fanned behind a white
front card holding the product, round price badge over the card corner, spec pill, Bangla line, feature chips;
collection mode fans one card per product like a hand of cards, each with name and price pill).
Flat only (no gradients, no blur, no 3D), Poppins + Hind Siliguri, small logo chip in a corner."""
from PIL import Image, ImageDraw
import render_flat as rf
from render_flat import P, f, fit, wrap, tk, S, W, H, W0, H0
from render_styles4 import logo_chip, mix, strike
from render_styles8 import _scaled
from render_styles16 import _bnq, _paste_c

WHITE = (255, 255, 255)
FOOT = "everydaycart.online  |  Inbox us to order"


def _lum(c): return 0.299 * c[0] + 0.587 * c[1] + 0.114 * c[2]


def _on(c, ink=(22, 22, 30)): return WHITE if _lum(c) < 160 else ink


def _put(img, prod, cx, cy, maxw, maxh, ang=0):
    pr = _scaled(prod, maxw, maxh)
    if ang: pr = pr.rotate(ang, expand=True, resample=Image.BICUBIC)
    img.alpha_composite(pr, (int(cx * S - pr.width / 2), int(cy * S - pr.height / 2)))


def _layer(w, h, ang, fill, cx, cy, img, draw_fn=None, r=34, outline=None, ow=0):
    pad = 20; L = Image.new("RGBA", P(w + 2 * pad, h + 2 * pad), (0, 0, 0, 0)); d = ImageDraw.Draw(L)
    d.rounded_rectangle(P(pad, pad, pad + w, pad + h), radius=r * S, fill=fill, outline=outline, width=ow * S)
    if draw_fn: draw_fn(L, d, pad, pad, w, h)
    if ang: L = L.rotate(ang, expand=True, resample=Image.BICUBIC)
    _paste_c(img, L, cx, cy)


def _tag(d, text, fill, col, outline=None):
    tf = f("Poppins-Bold.ttf", 21); tw = d.textlength(text, font=tf) / S
    d.rounded_rectangle(P(W0 - 44 - tw - 40, 38, W0 - 44, 84), radius=23 * S, fill=fill, outline=outline, width=3 * S if outline else 0)
    d.text(P(W0 - 64 - tw, 61), text, font=tf, fill=col, anchor="lm")


def _feat_pills(d, feats, y0, y1, acc, ink, chip=WHITE, x0=44, x1=None):
    x1 = x1 or W0 - 44; feats = feats[:4]; gap = 14; cw = (x1 - x0 - gap) / 2
    rows = (len(feats) + 1) // 2; rh = min(70, (y1 - y0 - gap * (rows - 1)) / max(1, rows))
    for i, fe in enumerate(feats):
        x = x0 + (i % 2) * (cw + gap); y = y0 + (i // 2) * (rh + gap)
        d.rounded_rectangle(P(x, y, x + cw, y + rh), radius=rh / 2 * S, fill=chip)
        r = rh / 2 - 10; cx = x + rh / 2; cy = y + rh / 2
        d.ellipse(P(cx - r, cy - r, cx + r, cy + r), fill=acc)
        d.text(P(cx, cy), str(i + 1), font=f("Poppins-Bold.ttf", r * 1.05), fill=_on(acc), anchor="mm")
        d.text(P(x + rh + 4, cy), fe, font=fit(d, fe, "Poppins-Medium.ttf", 24, cw - rh - 22), fill=ink, anchor="lm")


# ---------------- Template AK: diagonal split poster ----------------
def template_ak(p):
    top = p.get("top", (30, 50, 120)); paper = p.get("paper", (250, 246, 238)); ink = p.get("ink", (22, 22, 30))
    acc = p.get("acc", (255, 200, 60)); disc = p.get("disc", mix(top, WHITE, 0.82)); stripe = p.get("stripe", acc)
    yl, yr = p.get("split", (860, 600))   # diagonal edge: y at left and right
    img = Image.new("RGBA", (W, H), paper + (255,)); d = ImageDraw.Draw(img)
    d.polygon([P(0, 0), P(W0, 0), P(W0, yr + 46), P(0, yl + 46)], fill=stripe)
    d.polygon([P(0, 0), P(W0, 0), P(W0, yr + 22), P(0, yl + 22)], fill=paper)
    d.polygon([P(0, 0), P(W0, 0), P(W0, yr), P(0, yl)], fill=top)
    logo_chip(img, 44, 30, 110, fill=WHITE); d = ImageDraw.Draw(img)
    _tag(d, p["tag"], acc, _on(acc))
    h1, h2 = p["head"]; hf = f("Poppins-Bold.ttf", p.get("hsize", 76))
    for l in (h1, h2): hf = fit(d, l, "Poppins-Bold.ttf", hf.size / S, W0 - 100)
    lh = hf.size / S * 1.05
    d.text(P(44, 126), h1, font=hf, fill=_on(top)); d.text(P(44, 126 + lh), h2, font=hf, fill=acc)
    items = p.get("items")
    if items:
        for it in items:
            r = it.get("r", 170); cx, cy = it["cx"], it["cy"]
            d.ellipse(P(cx - r, cy - r, cx + r, cy + r), fill=it.get("disc", disc))
            _put(img, it["img"], cx + it.get("dx", 0), cy + it.get("dy", 0), it.get("mw", r * 1.6), it.get("mh", r * 1.6), it.get("ang", 0)); d = ImageDraw.Draw(img)
            # name + price flag under the disc
            nm = it["name"]; nf = fit(d, nm, "Poppins-Bold.ttf", 23, 2 * r + 20)
            fx, fy = it.get("fx", cx), it.get("fy", cy + r + 8)
            pt = tk(it["price"]); pf = f("Poppins-Bold.ttf", 34); pw = max(d.textlength(pt, font=pf), d.textlength(nm, font=nf)) / S + 44
            d.rectangle(P(fx - pw / 2, fy, fx + pw / 2, fy + 92), fill=ink)
            d.text(P(fx, fy + 24), nm, font=nf, fill=acc, anchor="mm")
            d.text(P(fx, fy + 64), pt, font=pf, fill=WHITE, anchor="mm")
            if it.get("regular") and it["regular"] > it["price"]:
                rt = tk(it["regular"]); rfo = f("Poppins-Medium.ttf", 19); rw = d.textlength(rt, font=rfo) / S
                d.rectangle(P(fx - rw / 2 - 12, fy + 92, fx + rw / 2 + 12, fy + 124), fill=acc)
                strike(d, fx - rw / 2, fy + 96, rt, rfo, ink)
    else:
        r = p.get("r", 265); cx, cy = p.get("dcx", 680), p.get("dcy", 640)
        d.ellipse(P(cx - r, cy - r, cx + r, cy + r), fill=disc)
        d.ellipse(P(cx - r + 18, cy - r + 18, cx + r - 18, cy + r - 18), outline=mix(disc, top, 0.25), width=3 * S)
        _put(img, p["img"], p.get("cx", cx), p.get("cy", cy), p.get("maxw", 470), p.get("maxh", 470), p.get("ang", 0)); d = ImageDraw.Draw(img)
        # price flag (left, on the colour side)
        fx0, fy0 = 0, p.get("flag_y", 430); fw = p.get("flag_w", 330)
        d.polygon([P(fx0, fy0), P(fx0 + fw, fy0), P(fx0 + fw - 34, fy0 + 70), P(fx0 + fw, fy0 + 140), P(fx0, fy0 + 140)], fill=acc)
        d.text(P(44, fy0 + 28), p.get("plabel", "PRICE"), font=f("Poppins-Bold.ttf", 18), fill=_on(acc), anchor="lm")
        pt = tk(p["price"]); pf = fit(d, pt, "Poppins-Bold.ttf", 60, fw - 90)
        d.text(P(44, fy0 + 84), pt, font=pf, fill=_on(acc), anchor="lm")
        if p.get("regular") and p["regular"] > p["price"]:
            strike(d, 46, fy0 + 152, "Regular " + tk(p["regular"]), f("Poppins-Medium.ttf", 22), mix(_on(top), top, 0.3))
        if p.get("spec"):
            big_, lab = p["spec"]; sy = fy0 + 206
            d.text(P(44, sy), big_, font=fit(d, big_, "Poppins-Bold.ttf", 72, 260), fill=_on(top))
            d.text(P(46, sy + 86), lab, font=fit(d, lab, "Poppins-Bold.ttf", 20, 260), fill=acc)
    # Bangla line with accent bar
    by = p.get("bn_y", max(yl, yr) + 104)
    d.rectangle(P(44, by - 26, 54, by + 26), fill=stripe)
    _bnq(d, 74, by, p["bn"], 34, W0 - 130, ink)
    ty = by + 46
    ftt, tl = wrap(d, p["title"], "Poppins-Bold.ttf", 33, W0 - 90, 1)
    d.text(P(44, ty), tl[0], font=ftt, fill=top if _lum(top) < 140 else ink)
    _feat_pills(d, p.get("feats", []), ty + 64, H0 - 96, top, ink, chip=mix(paper, top, 0.10))
    d.rectangle(P(0, H0 - 70, W0, H0), fill=ink)
    d.text(P(44, H0 - 35), FOOT, font=f("Poppins-Bold.ttf", 23), fill=WHITE, anchor="lm")
    d.text(P(W0 - 44, H0 - 35), p.get("code", "EC/18"), font=f("Poppins-Bold.ttf", 23), fill=acc, anchor="rm")
    return rf.finish(img, p["out"])


# ---------------- Template AL: fanned card stack ----------------
def template_al(p):
    bg = p.get("bg", (252, 232, 222)); ink = p.get("ink", (24, 24, 34)); acc = p.get("acc", (230, 70, 90))
    c1 = p.get("c1", (255, 196, 90)); c2 = p.get("c2", (110, 170, 240)); card = p.get("card", WHITE)
    img = Image.new("RGBA", (W, H), bg + (255,)); d = ImageDraw.Draw(img)
    # big flat background circles
    blob = mix(bg, WHITE, 0.45)
    d.ellipse(P(-180, 260, 260, 700), fill=blob); d.ellipse(P(W0 - 230, 520, W0 + 200, 950), fill=blob)
    logo_chip(img, 44, 30, 110, fill=WHITE); d = ImageDraw.Draw(img)
    _tag(d, p["tag"], ink, WHITE)
    h1, h2 = p["head"]; hf = f("Poppins-Bold.ttf", p.get("hsize", 70))
    for l in (h1, h2): hf = fit(d, l, "Poppins-Bold.ttf", hf.size / S, W0 - 110)
    lh = hf.size / S * 1.05
    d.text(P(W0 / 2, 118), h1, font=hf, fill=ink, anchor="ma"); d.text(P(W0 / 2, 118 + lh), h2, font=hf, fill=acc, anchor="ma")
    CY = p.get("card_cy", 640); items = p.get("items")
    if items:
        n = len(items); angs = p.get("angs", [10, 0, -10][:n] if n == 3 else [7, -7]); xs = p.get("xs", [270, 540, 810][:n] if n == 3 else [370, 710])
        cw, ch = p.get("cw", 310), p.get("ch", 430)
        order = sorted(range(n), key=lambda k: -abs(xs[k] - W0 / 2))
        for k in order:
            it = items[k]; col = it.get("fill", [c1, c2, mix(acc, WHITE, 0.55)][k % 3])
            def fn(L, dd, x, y, w, h, it=it, col=col):
                dd.rounded_rectangle(P(x + 14, y + 14, x + w - 14, y + h - 120), radius=24 * S, fill=col)
                pr = _scaled(it["img"], it.get("mw", w - 60), it.get("mh", h - 190))
                L.alpha_composite(pr, (int((x + w / 2) * S - pr.width / 2), int((y + 14 + (h - 134) / 2) * S - pr.height / 2)))
                nm = it["name"]; nf = fit(dd, nm, "Poppins-Bold.ttf", 23, w - 36)
                dd.text(P(x + w / 2, y + h - 92), nm, font=nf, fill=ink, anchor="mm")
                pt = tk(it["price"]); pf = f("Poppins-Bold.ttf", 30); pw = dd.textlength(pt, font=pf) / S + 40
                dd.rounded_rectangle(P(x + w / 2 - pw / 2, y + h - 66, x + w / 2 + pw / 2, y + h - 18), radius=24 * S, fill=acc)
                dd.text(P(x + w / 2, y + h - 42), pt, font=pf, fill=_on(acc), anchor="mm")
            _layer(cw, ch, angs[k], card, xs[k], CY + abs(angs[k]) * 2.5, img, fn, r=30, outline=ink, ow=3)
        d = ImageDraw.Draw(img)
        if p.get("from"):
            cx, cy, r = p.get("bx", 940), p.get("by", 370), 86
            d.ellipse(P(cx - r, cy - r, cx + r, cy + r), fill=ink)
            d.text(P(cx, cy - 26), "FROM", font=f("Poppins-Bold.ttf", 19), fill=c1, anchor="mm")
            d.text(P(cx, cy + 14), tk(p["from"]), font=fit(d, tk(p["from"]), "Poppins-Bold.ttf", 38, 2 * r - 26), fill=WHITE, anchor="mm")
        BOT = CY + ch / 2 + 50
    else:
        cw, ch = p.get("cw", 560), p.get("ch", 560)
        _layer(cw, ch, p.get("a2", -9), c2, W0 / 2 + 30, CY + 10, img, r=40)
        _layer(cw, ch, p.get("a1", 6), c1, W0 / 2 - 20, CY, img, r=40)
        def fn(L, dd, x, y, w, h):
            pr = _scaled(p["img"], p.get("maxw", w - 120), p.get("maxh", h - 110))
            L.alpha_composite(pr, (int((x + w / 2 + p.get("dx", 0)) * S - pr.width / 2), int((y + h / 2 + p.get("dy", 0)) * S - pr.height / 2)))
        _layer(cw, ch, p.get("a0", -1.5), card, W0 / 2, CY, img, fn, r=40, outline=ink, ow=3); d = ImageDraw.Draw(img)
        # price badge over the top-right corner
        bx, byy, r = p.get("bx", W0 / 2 + cw / 2 - 20), p.get("by", CY - ch / 2 + 30), 104
        d.ellipse(P(bx - r, byy - r, bx + r, byy + r), fill=acc)
        d.ellipse(P(bx - r + 8, byy - r + 8, bx + r - 8, byy + r - 8), outline=_on(acc), width=2 * S)
        has_reg = p.get("regular") and p["regular"] > p["price"]
        d.text(P(bx, byy - (40 if has_reg else 30)), p.get("plabel", "ONLY"), font=f("Poppins-Bold.ttf", 18), fill=_on(acc), anchor="mm")
        pt = tk(p["price"]); d.text(P(bx, byy + (2 if has_reg else 8)), pt, font=fit(d, pt, "Poppins-Bold.ttf", 40, 2 * r - 30), fill=_on(acc), anchor="mm")
        if has_reg:
            rt = tk(p["regular"]); rfo = f("Poppins-Medium.ttf", 18); rw = d.textlength(rt, font=rfo) / S
            strike(d, bx - rw / 2, byy + 32, rt, rfo, mix(_on(acc), acc, 0.25))
        if p.get("spec"):
            big_, lab = p["spec"]; sx, sy = p.get("sx", W0 / 2 - cw / 2 + 10), p.get("sy", CY + ch / 2 - 40)
            bf = f("Poppins-Bold.ttf", 34); lf = f("Poppins-Bold.ttf", 19)
            sw = (d.textlength(big_, font=bf) + d.textlength(lab, font=lf)) / S + 60
            d.rounded_rectangle(P(sx - 30, sy - 32, sx - 30 + sw, sy + 32), radius=32 * S, fill=ink)
            d.text(P(sx - 8, sy), big_, font=bf, fill=c1, anchor="lm")
            d.text(P(sx + d.textlength(big_, font=bf) / S + 4, sy + 2), lab, font=lf, fill=WHITE, anchor="lm")
        BOT = CY + ch / 2 + 62
    by = p.get("bn_y", BOT + 30)
    _bnq(d, W0 / 2, by, p["bn"], 34, W0 - 120, ink, anchor="mm")
    ty = by + 40
    ftt, tl = wrap(d, p["title"], "Poppins-Bold.ttf", 32, W0 - 100, 1)
    d.text(P(W0 / 2, ty), tl[0], font=ftt, fill=acc if _lum(acc) < 150 else ink, anchor="ma")
    _feat_pills(d, p.get("feats", []), ty + 60, H0 - 84, acc, ink, chip=WHITE)
    d.text(P(W0 / 2, H0 - 42), FOOT, font=f("Poppins-Bold.ttf", 23), fill=ink, anchor="mm")
    return rf.finish(img, p["out"])


TEMPLATES18 = {"AK": template_ak, "AL": template_al}
