"""Style set 7 (added 12 Nov 2026): O spotlight stage (flat spotlight beam onto a two-tone podium, hanging price tag,
headline hook at the top, Bangla ribbon, numbered feature strip), P seam poster (product sits across the seam between a
colour top and a cream bottom, giant outlined category word, price pill on the seam, 01/02/03 feature columns;
collection mode shows several products with their own price chips). Flat only, Poppins + Hind Siliguri, small logo chip."""
import math
from PIL import Image, ImageDraw
import render_flat as rf
from render_flat import P, f, fit, wrap, tk, S, W, H, W0, H0, INK
from render_styles4 import logo_chip, mix, strike
from render_styles6 import fbn, bn_text

WHITE = (255, 255, 255)


def _scaled(prod, maxw, maxh):
    s = min(maxw * S / prod.width, maxh * S / prod.height)
    return prod.resize((max(1, int(prod.width * s)), max(1, int(prod.height * s))), Image.LANCZOS)


def _put(img, prod, cx, bottom, maxw, maxh, shadow_col=None):
    """Place a cutout with its base on `bottom`; optional crisp flat ellipse shadow (no blur)."""
    pr = _scaled(prod, maxw, maxh); w, h = pr.width / S, pr.height / S
    if shadow_col:
        ImageDraw.Draw(img).ellipse(P(cx - w * 0.40, bottom - 12, cx + w * 0.40, bottom + 12), fill=shadow_col)
    img.alpha_composite(pr, (int((cx - w / 2) * S), int((bottom - h) * S)))
    return img, w, h


def _hang_tag(img, cx, top, w, h, fill, ink, price, regular, label, hole_bg):
    d = ImageDraw.Draw(img)
    # string
    d.line(P(cx, top - 70, cx, top + 26), fill=mix(fill, WHITE, 0.6), width=3 * S)
    pts = [(cx, top), (cx + w / 2, top + 46), (cx + w / 2, top + h), (cx - w / 2, top + h), (cx - w / 2, top + 46)]
    d.polygon([P(*q) for q in pts], fill=fill)
    d.ellipse(P(cx - 11, top + 26, cx + 11, top + 48), fill=hole_bg)
    d.text(P(cx, top + 90), label, font=f("Poppins-Medium.ttf", 22), fill=mix(fill, ink, 0.7), anchor="mm")
    pt = tk(price); pf = fit(d, pt, "Poppins-Bold.ttf", 56, w - 36)
    d.text(P(cx, top + 146), pt, font=pf, fill=ink, anchor="mm")
    if regular and regular > price:
        rt = tk(regular); rfo = f("Poppins-Regular.ttf", 26); rw = d.textlength(rt, font=rfo) / S
        strike(d, cx - rw / 2, top + 186, rt, rfo, mix(fill, ink, 0.55))


# ---------------- Template O: spotlight stage ----------------
def template_o(p):
    bg = p.get("bg", (30, 34, 64)); beam = p.get("beam", mix(bg, WHITE, 0.10)); acc = p.get("acc", (255, 200, 70))
    pod = p.get("pod", acc); ink = p.get("ink", INK); hl = p.get("hl", WHITE)
    img = Image.new("RGBA", (W, H), bg + (255,)); d = ImageDraw.Draw(img)
    cx = p.get("cx", 430)
    # spotlight beam (flat trapezoid) + lamp
    d.polygon([P(cx - 70, 370), P(cx + 70, 370), P(cx + 330, 980), P(cx - 330, 980)], fill=beam)
    d.pieslice(P(cx - 62, 330, cx + 62, 402), 180, 360, fill=mix(bg, WHITE, 0.30))
    d.rounded_rectangle(P(cx - 90, 358, cx + 90, 378), radius=10 * S, fill=mix(bg, WHITE, 0.30))
    # confetti dots / sparkles
    for (sx, sy, r, t) in p.get("dots", [(80, 520, 7, .3), (980, 760, 6, .3), (860, 940, 4, .5), (120, 900, 5, .5), (700, 380, 4, .4)]):
        d.ellipse(P(sx - r, sy - r, sx + r, sy + r), fill=mix(bg, acc, t))
    # headline hook
    logo_chip(img, 44, 44, 120); d = ImageDraw.Draw(img)
    tag = p["tag"]; tf = f("Poppins-Bold.ttf", 21); tw = d.textlength(tag, font=tf) / S
    d.rounded_rectangle(P(W0 - 44 - tw - 40, 52, W0 - 44, 98), radius=23 * S, fill=acc)
    d.text(P(W0 - 44 - tw - 20, 75), tag, font=tf, fill=ink, anchor="lm")
    if isinstance(p["head"], (list, tuple)):
        lines = list(p["head"]); ft = f("Poppins-Bold.ttf", 64)
        for l in lines: ft = fit(d, l, "Poppins-Bold.ttf", ft.size / S, 960)
    else:
        ft, lines = wrap(d, p["head"], "Poppins-Bold.ttf", 64, 960, 2)
    y = 150
    for i, l in enumerate(lines):
        d.text(P(60, y), l, font=ft, fill=acc if i == len(lines) - 1 and p.get("hl_last", True) else WHITE); y += ft.size / S * 1.08
    # podium (flat two-tone ellipses)
    PY = 960; pw = p.get("podw", 300)
    d.rectangle(P(cx - pw, PY, cx + pw, PY + 70), fill=mix(pod, bg, 0.35))
    d.ellipse(P(cx - pw, PY + 30, cx + pw, PY + 110), fill=mix(pod, bg, 0.35))
    d.ellipse(P(cx - pw, PY - 40, cx + pw, PY + 40), fill=pod)
    d.ellipse(P(cx - pw + 40, PY - 26, cx + pw - 40, PY + 26), fill=mix(pod, WHITE, 0.25))
    imgs = p["img"] if isinstance(p["img"], (list, tuple)) else [p["img"]]
    gap = p.get("gap", 24); maxw, maxh = p.get("maxw", 480), p.get("maxh", 560)
    ratios = [i.width / i.height for i in imgs]; hgt = min(maxh, (maxw - gap * (len(imgs) - 1)) / sum(ratios))
    x = cx - (sum(r * hgt for r in ratios) + gap * (len(imgs) - 1)) / 2
    for i, r in zip(imgs, ratios):
        img, w_, _ = _put(img, i, x + r * hgt / 2, PY + p.get("sink", 6), r * hgt, hgt, shadow_col=mix(pod, bg, 0.2)); x += r * hgt + gap
    d = ImageDraw.Draw(img)
    # hanging price tag on the right
    _hang_tag(img, p.get("tx", 880), p.get("ty", 470), 270, 230, hl, ink, p["price"], p.get("regular"), p.get("label", "ONLY"), bg)
    d = ImageDraw.Draw(img)
    # Bangla ribbon under the tag
    if p.get("bn"):
        lines_bn = p["bn"] if isinstance(p["bn"], (list, tuple)) else [p["bn"]]
        by = p.get("bny", 760)
        for l in lines_bn:
            ftb = fbn(p.get("bn_size", 32))
            while d.textlength(l, font=ftb) / S > 300: ftb = fbn(ftb.size / S - 1)
            d.text(P(p.get("tx", 880), by), l, font=ftb, fill=WHITE, anchor="mm"); by += ftb.size / S * 1.5
    # bottom strip: title + numbered features
    CY = 1090
    d.rectangle(P(0, CY, W0, H0), fill=WHITE)
    ft, tl = wrap(d, p["title"], "Poppins-Bold.ttf", 40, 960, 1)
    d.text(P(60, CY + 46), tl[0], font=ft, fill=ink, anchor="lm")
    feats = p["feats"][:3]; colw = 960 / len(feats); yy = CY + 122
    for i, t in enumerate(feats):
        x0 = 60 + i * colw
        d.ellipse(P(x0, yy - 22, x0 + 44, yy + 22), fill=bg)
        d.text(P(x0 + 22, yy), str(i + 1), font=f("Poppins-Bold.ttf", 22), fill=acc, anchor="mm")
        d.text(P(x0 + 56, yy), t, font=fit(d, t, "Poppins-Medium.ttf", 26, colw - 70), fill=ink, anchor="lm")
    d.rectangle(P(0, H0 - 70, W0, H0), fill=acc)
    d.text(P(60, H0 - 35), "everydaycart.online", font=f("Poppins-Bold.ttf", 26), fill=ink, anchor="lm")
    nt = "Inbox us to order"; nf = f("Poppins-Medium.ttf", 24)
    d.text(P(W0 - 60, H0 - 35), nt, font=nf, fill=ink, anchor="rm")
    return rf.finish(img, p["out"])


# ---------------- Template P: seam poster ----------------
def template_p(p):
    top = p.get("top", (232, 96, 76)); cream = p.get("cream", (252, 247, 240)); acc = p.get("acc", (30, 40, 70))
    ink = p.get("ink", INK); SEAM = p.get("seam", 760)
    img = Image.new("RGBA", (W, H), cream + (255,)); d = ImageDraw.Draw(img)
    d.rectangle(P(0, 0, W0, SEAM), fill=top)
    # giant outlined word behind the product
    word = p["word"]; wf = fit(d, word, "Poppins-Bold.ttf", 260, 1000)
    d.text(P(W0 / 2, SEAM - 40), word, font=wf, fill=mix(top, WHITE, p.get("word_t", 0.16)), anchor="ms")
    # small half-circle bites on the seam for a flat cut-paper feel
    for x in range(0, W0 + 60, 60):
        d.ellipse(P(x - 14, SEAM - 14, x + 14, SEAM + 14), fill=cream)
    logo_chip(img, 44, 44, 120); d = ImageDraw.Draw(img)
    tag = p["tag"]; tf = f("Poppins-Bold.ttf", 21); tw = d.textlength(tag, font=tf) / S
    d.rounded_rectangle(P(W0 - 44 - tw - 40, 52, W0 - 44, 98), radius=23 * S, fill=WHITE)
    d.text(P(W0 - 44 - tw - 20, 75), tag, font=tf, fill=top, anchor="lm")
    if isinstance(p["head"], (list, tuple)):
        lines = list(p["head"]); ft = f("Poppins-Bold.ttf", 58)
        for l in lines: ft = fit(d, l, "Poppins-Bold.ttf", ft.size / S, 960)
    else:
        ft, lines = wrap(d, p["head"], "Poppins-Bold.ttf", 58, 960, 2)
    y = 140
    for l in lines: d.text(P(60, y), l, font=ft, fill=WHITE); y += ft.size / S * 1.08
    items = p.get("items")
    if items:   # collection mode: [(img, name, price, regular)]
        n = len(items); slot = (W0 - 80) / n; base = SEAM + p.get("sink", 150)
        maxh = p.get("maxh", 470)
        nsz = min(fit(d, it[1], "Poppins-Bold.ttf", 25, slot - 20).size / S for it in items)
        for i, (pi, name, price, reg) in enumerate(items):
            cx = 40 + slot * (i + 0.5)
            img, w_, h_ = _put(img, pi, cx, base, slot - 34, maxh * pi_scale(p, i), shadow_col=mix(cream, ink, 0.10))
            d = ImageDraw.Draw(img)
            nf = f("Poppins-Bold.ttf", nsz)
            d.text(P(cx, base + 44), name, font=nf, fill=ink, anchor="mm")
            pt = tk(price); pf = f("Poppins-Bold.ttf", 25); pw = d.textlength(pt, font=pf) / S
            d.rounded_rectangle(P(cx - pw / 2 - 18, base + 70, cx + pw / 2 + 18, base + 116), radius=23 * S, fill=top)
            d.text(P(cx, base + 93), pt, font=pf, fill=WHITE, anchor="mm")
            if reg and reg > price:
                rt = tk(reg); rfo = f("Poppins-Regular.ttf", 21); rw = d.textlength(rt, font=rfo) / S
                strike(d, cx - rw / 2, base + 124, rt, rfo, (150, 140, 136))
        if p.get("bn"):
            bn_text(d, W0 / 2, p.get("bny", 1222), p["bn"], 34, acc, anchor="mm")
    else:
        cx = p.get("cx", 540); base = SEAM + p.get("sink", 150)
        img, w_, h_ = _put(img, p["img"], cx, base, p.get("maxw", 560), p.get("maxh", 640), shadow_col=mix(cream, ink, 0.10))
        d = ImageDraw.Draw(img)
        # price pill on the seam (right) and Bangla note (left)
        px = p.get("px", 840); py = SEAM + p.get("pdy", 40)
        d.rounded_rectangle(P(px - 150, py - 70, px + 150, py + 70), radius=70 * S, fill=acc)
        d.text(P(px, py - 34), p.get("label", "ONLY"), font=f("Poppins-Medium.ttf", 20), fill=mix(acc, WHITE, 0.7), anchor="mm")
        pt = tk(p["price"]); d.text(P(px, py + 6), pt, font=fit(d, pt, "Poppins-Bold.ttf", 48, 250), fill=WHITE, anchor="mm")
        if p.get("regular", 0) > p["price"]:
            rt = tk(p["regular"]); rfo = f("Poppins-Regular.ttf", 21); rw = d.textlength(rt, font=rfo) / S
            strike(d, px - rw / 2, py + 34, rt, rfo, mix(acc, WHITE, 0.6))
        if p.get("bn"):
            lines_bn = p["bn"] if isinstance(p["bn"], (list, tuple)) else [p["bn"]]
            by = p.get("bny", SEAM + 60)
            for l in lines_bn:
                ftb = fbn(p.get("bn_size", 32))
                while d.textlength(l, font=ftb) / S > 300: ftb = fbn(ftb.size / S - 1)
                d.text(P(60, by), l, font=ftb, fill=acc); by += ftb.size / S * 1.45
        # title + 01/02/03 columns
        ty = p.get("ty", 1000)
        ft, tl = wrap(d, p["title"], "Poppins-Bold.ttf", 42, 960, 1)
        d.text(P(W0 / 2, ty), tl[0], font=ft, fill=ink, anchor="mm")
        feats = p["feats"][:3]; colw = 960 / len(feats); yy = ty + 60
        for i, t in enumerate(feats):
            x0 = 60 + i * colw
            if i: d.line(P(x0 - 8, yy + 4, x0 - 8, yy + 92), fill=mix(cream, ink, 0.15), width=2 * S)
            d.text(P(x0 + 14, yy), f"{i + 1:02d}", font=f("Poppins-Bold.ttf", 40), fill=top)
            d.text(P(x0 + 14, yy + 74), t, font=fit(d, t, "Poppins-Medium.ttf", 26, colw - 36), fill=ink, anchor="lm")
    # footer
    d.text(P(60, H0 - 52), "everydaycart.online", font=f("Poppins-Bold.ttf", 28), fill=acc, anchor="lm")
    nt = "Inbox us to order"; nf = f("Poppins-Bold.ttf", 23); nw = d.textlength(nt, font=nf) / S
    d.rounded_rectangle(P(W0 - 60 - nw - 44, H0 - 78, W0 - 60, H0 - 26), radius=26 * S, fill=top)
    d.text(P(W0 - 60 - nw - 22, H0 - 52), nt, font=nf, fill=WHITE, anchor="lm")
    return rf.finish(img, p["out"])


def pi_scale(p, i):
    s = p.get("scales")
    return s[i] if s else 1.0


TEMPLATES7 = {"O": template_o, "P": template_p}
