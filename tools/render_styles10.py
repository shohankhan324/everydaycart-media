"""Style set 10 (added 15 Nov 2026): U hang tag poster (solid colour poster, bold diagonal band, giant outlined
product word behind the product, a tilted paper price tag hanging on a string, white bottom card with title,
Bangla line and a 2 column feature grid; collection mode lists each item on the tag), V chat inbox (pastel
background, product panel with hook bubble, then a flat Messenger style Q and A: Bangla questions on the left,
brand answers on the right with price, ticked features and how to order). Flat only (no gradients, no blur),
Poppins + Hind Siliguri, small logo chip in the top-left corner."""
import math
from PIL import Image, ImageDraw
import render_flat as rf
from render_flat import P, f, fit, wrap, tk, S, W, H, W0, H0, INK, check_icon
from render_styles4 import logo_chip, mix, strike
from render_styles6 import fbn, _layer
from render_styles8 import _center, _tag, _bn_fit

WHITE = (255, 255, 255)


# ---------------- Template U: hang tag poster ----------------
def template_u(p):
    bg = p.get("bg", (24, 52, 96)); acc = p.get("acc", (255, 196, 64)); band = p.get("band", mix(bg, WHITE, 0.1))
    ink = p.get("ink", INK); paper = p.get("paper", (255, 252, 244))
    img = Image.new("RGBA", (W, H), bg + (255,)); d = ImageDraw.Draw(img)
    # bold diagonal band
    d.polygon([P(0, 560), P(W0, 300), P(W0, 560), P(0, 820)], fill=band)
    # headline
    hx, hy = 56, p.get("hy", 150); head = p["head"]
    ft = f("Poppins-Bold.ttf", p.get("hsize", 60))
    for l in head: ft = fit(d, l, "Poppins-Bold.ttf", ft.size / S, p.get("hw", 640))
    for i, l in enumerate(head):
        d.text(P(hx, hy + i * ft.size / S * 1.12), l, font=ft, fill=acc if i == len(head) - 1 else WHITE)
    # giant outlined word
    word = p.get("word")
    if word:
        _outline_word(img, word, p.get("wy", 352), mix(bg, WHITE, 0.34), size=p.get("wsize", 150)); d = ImageDraw.Draw(img)
    # product(s) on a flat disc
    cx, cy, r = p.get("cx", 400), p.get("cy", 680), p.get("r", 270)
    d.ellipse(P(cx - r, cy - r, cx + r, cy + r), fill=mix(bg, WHITE, 0.16))
    d.ellipse(P(cx - r - 22, cy - r - 22, cx + r + 22, cy + r + 22), outline=mix(bg, WHITE, 0.3), width=3 * S)
    items = p.get("items")
    if items:
        for it in items:
            _center(img, it["img"], cx + it["ox"], cy + it["oy"], it["mw"], it["mh"])
    else:
        _center(img, p["img"], cx + p.get("dx", 0), cy + p.get("dy", 0), p.get("maxw", 520), p.get("maxh", 560))
    d = ImageDraw.Draw(img)
    # hanging price tag
    TW, TH = p.get("tw", 300), p.get("th", 390 if not items else 430)
    tx, ty = p.get("tx", 735), p.get("ty", 470); ang = p.get("tang", 7)

    def draw_tag(L):
        dl = ImageDraw.Draw(L); c = 46
        dl.polygon([P(c, 0), P(TW - c, 0), P(TW, c), P(TW, TH), P(0, TH), P(0, c)], fill=paper)
        dl.ellipse(P(TW / 2 - 15, 26, TW / 2 + 15, 56), fill=bg)
        dl.rectangle(P(0, TH - 18, TW, TH), fill=acc)
        mute = mix(paper, ink, 0.5)
        y = 82
        if items:
            dl.text(P(TW / 2, y), p.get("tag_label", "PRICE LIST"), font=f("Poppins-Bold.ttf", 22), fill=mute, anchor="mm"); y += 34
            for it in items:
                ftn, nl = wrap(dl, it["name"], "Poppins-Bold.ttf", 24, TW - 44, 2)
                for l in nl: dl.text(P(22, y), l, font=ftn, fill=ink); y += ftn.size / S * 1.18
                pt = tk(it["price"]); pf = f("Poppins-Bold.ttf", 44)
                dl.text(P(22, y), pt, font=pf, fill=bg)
                if it.get("regular", 0) > it["price"]:
                    pw = dl.textlength(pt, font=pf) / S
                    strike(dl, 34 + pw, y + 16, tk(it["regular"]), f("Poppins-Medium.ttf", 20), mute)
                y += 66
                dl.line(P(22, y - 6, TW - 22, y - 6), fill=mix(paper, ink, 0.15), width=2 * S); y += 10
        else:
            dl.text(P(TW / 2, y), p.get("tag_label", "PRICE"), font=f("Poppins-Bold.ttf", 24), fill=mute, anchor="mm"); y += 52
            pt = (p.get("from", "") + tk(p["price"])).strip()
            dl.text(P(TW / 2, y + 30), pt, font=fit(dl, pt, "Poppins-Bold.ttf", 66, TW - 36), fill=bg, anchor="mm"); y += 84
            if p.get("regular", 0) > p["price"]:
                rt = "Regular " + tk(p["regular"]); rfo = f("Poppins-Medium.ttf", 22); rw = dl.textlength(rt, font=rfo) / S
                strike(dl, TW / 2 - rw / 2, y, rt, rfo, mute); y += 44
            dl.line(P(26, y + 6, TW - 26, y + 6), fill=mix(paper, ink, 0.15), width=2 * S); y += 30
            for l in p.get("tag_lines", ["Inbox us", "to order"]):
                dl.text(P(TW / 2, y + 14), l, font=f("Poppins-Bold.ttf", 24), fill=ink, anchor="mm"); y += 34
    # string from a flat pin to the tag hole (computed after rotation)
    a = math.radians(ang); dy = -(TH / 2 - 41)
    hx_, hy_ = tx + TW / 2 + dy * math.sin(a), ty + TH / 2 + dy * math.cos(a)
    nx, ny = hx_ + p.get("pin_dx", 30), ty - 70
    d.line(P(nx, ny, hx_, hy_), fill=WHITE, width=3 * S)
    d.ellipse(P(nx - 11, ny - 11, nx + 11, ny + 11), fill=acc)
    _layer(img, (tx, ty, tx + TW, ty + TH), draw_tag, ang)
    d = ImageDraw.Draw(img)
    # bottom card
    X0, X1, Y1 = 40, W0 - 40, H0 - 72
    Y0 = Y1 - (26 + 44 + (50 if p.get("bn") else 0) + 92 + 14)
    d.rounded_rectangle(P(X0, Y0, X1, Y1), radius=36 * S, fill=WHITE)
    y = Y0 + 26
    ftt, tl = wrap(d, p["title"], "Poppins-Bold.ttf", 34, X1 - X0 - 60, 1)
    d.text(P(X0 + 30, y), tl[0], font=ftt, fill=ink); y += ftt.size / S * 1.3
    if p.get("bn"):
        fb = _bn_fit(d, p["bn"], 28, X1 - X0 - 60)
        d.text(P(X0 + 30, y), p["bn"], font=fb, fill=mix(bg, ink, 0.2)); y += 50
    feats = p.get("feats", [])[:4]; cw = (X1 - X0 - 60) / 2
    for i, fe in enumerate(feats):
        fx = X0 + 30 + (i % 2) * cw; fy = y + (i // 2) * 46
        check_icon(d, fx + 14, fy + 18, 14, acc, ink)
        d.text(P(fx + 40, fy + 18), fe, font=fit(d, fe, "Poppins-Medium.ttf", 24, cw - 56), fill=ink, anchor="lm")
    d.text(P(W0 / 2, H0 - 36), "everydaycart.online  |  Inbox us to order", font=f("Poppins-Bold.ttf", 25),
           fill=WHITE, anchor="mm")
    logo_chip(img, 44, 44, 120); d = ImageDraw.Draw(img)
    _tag(img, d, p["tag"], acc, ink)
    return rf.finish(img, p["out"])


def _outline_word(img, word, cy, col, size=230, maxw=980, sw=3):
    """Outline-only text (transparent inside) drawn via a mask: stroked minus filled."""
    d = ImageDraw.Draw(img)
    wf = fit(d, word, "Poppins-Bold.ttf", size, maxw)
    m1 = Image.new("L", img.size, 0); m2 = Image.new("L", img.size, 0)
    ImageDraw.Draw(m1).text(P(W0 / 2, cy), word, font=wf, fill=255, anchor="mm", stroke_width=sw * S, stroke_fill=255)
    ImageDraw.Draw(m2).text(P(W0 / 2, cy), word, font=wf, fill=255, anchor="mm")
    from PIL import ImageChops
    m = ImageChops.subtract(m1, m2)
    img.paste(Image.new("RGBA", img.size, col + (255,)), (0, 0), m)


# ---------------- Template V: chat inbox ----------------
def _bubble(img, d, x, y, w, h, fill, side):
    d.rounded_rectangle(P(x, y, x + w, y + h), radius=28 * S, fill=fill)
    if side == "l": d.polygon([P(x, y + h - 30), P(x + 30, y + h), P(x - 12, y + h + 8)], fill=fill)
    else: d.polygon([P(x + w, y + h - 30), P(x + w - 30, y + h), P(x + w + 12, y + h + 8)], fill=fill)


def template_v(p):
    bg = p.get("bg", (226, 240, 255)); acc = p.get("acc", (0, 112, 240)); ink = p.get("ink", INK)
    panel = p.get("panel", mix(bg, WHITE, 0.5)); qcol = WHITE
    img = Image.new("RGBA", (W, H), bg + (255,)); d = ImageDraw.Draw(img)
    # flat dot pattern
    dc = mix(bg, acc, 0.12)
    for yy in range(30, H0, 54):
        for xx in range(30 + (yy // 54 % 2) * 27, W0, 54):
            d.ellipse(P(xx - 3, yy - 3, xx + 3, yy + 3), fill=dc)
    # product panel
    PX0, PY0, PX1, PY1 = 40, 120, W0 - 40, p.get("py1", 560)
    d.rounded_rectangle(P(PX0, PY0, PX1, PY1), radius=40 * S, fill=panel)
    d.ellipse(P(W0 / 2 + 150 - 250, (PY0 + PY1) / 2 - 230, W0 / 2 + 150 + 250, (PY0 + PY1) / 2 + 270), fill=mix(panel, acc, 0.12))
    _center(img, p["img"], W0 / 2 + 150 + p.get("dx", 0), (PY0 + PY1) / 2 + 20 + p.get("dy", 0), p.get("maxw", 520), p.get("maxh", 450))
    d = ImageDraw.Draw(img)
    # headline on the panel (left)
    hx, hy = PX0 + 36, PY0 + 44
    ftb = f("Poppins-Bold.ttf", 22); tw = d.textlength(p["tag"], font=ftb) / S
    d.rounded_rectangle(P(hx, hy, hx + tw + 36, hy + 42), radius=21 * S, fill=acc)
    d.text(P(hx + 18, hy + 21), p["tag"], font=ftb, fill=WHITE, anchor="lm")
    hy += 66; ft = f("Poppins-Bold.ttf", p.get("hsize", 46))
    for l in p["head"]: ft = fit(d, l, "Poppins-Bold.ttf", ft.size / S, p.get("hw", 340))
    for i, l in enumerate(p["head"]):
        d.text(P(hx, hy), l, font=ft, fill=acc if i == len(p["head"]) - 1 else ink); hy += ft.size / S * 1.14
    ftn, nl = wrap(d, p["title"], "Poppins-Medium.ttf", 24, p.get("hw", 340), 3)
    hy += 14
    for l in nl: d.text(P(hx, hy), l, font=ftn, fill=mix(ink, WHITE, 0.3)); hy += ftn.size / S * 1.25
    # chat header
    y = PY1 + 26
    y -= 6
    d.text(P(W0 / 2, y + 14), p.get("chat_label", "Everyday Cart inbox"), font=f("Poppins-Medium.ttf", 21),
           fill=mix(bg, ink, 0.55), anchor="mm")
    y += 40
    for kind, content in p["chat"]:
        if kind == "q":
            fb = fbn(28); body = content.rstrip("?"); q = content.endswith("?")
            qf = f("Poppins-Bold.ttf", 28); tw = d.textlength(body, font=fb) / S + (d.textlength("?", font=qf) / S + 4 if q else 0)
            _bubble(img, d, 70, y, tw + 56, 58, qcol, "l")
            d.text(P(98, y + 29), body, font=fb, fill=ink, anchor="lm")
            if q: d.text(P(98 + d.textlength(body, font=fb) / S + 4, y + 29), "?", font=qf, fill=ink, anchor="lm")
            y += 78
        elif kind == "price":
            pt = (p.get("from", "") + tk(p["price"])).strip(); pf = f("Poppins-Bold.ttf", 44)
            w_ = d.textlength(pt, font=pf) / S + 60
            rt = None
            if p.get("regular", 0) > p["price"]:
                rt = tk(p["regular"]); rfo = f("Poppins-Medium.ttf", 24); w_ += d.textlength(rt, font=rfo) / S + 24
            x1 = W0 - 70; x0 = x1 - w_
            _bubble(img, d, x0, y, w_, 70, acc, "r")
            d.text(P(x0 + 30, y + 35), pt, font=pf, fill=WHITE, anchor="lm")
            if rt:
                pw = d.textlength(pt, font=pf) / S
                strike(d, x0 + 54 + pw, y + 21, rt, rfo, mix(acc, WHITE, 0.6))
            y += 90
        elif kind == "feats":
            ff = f("Poppins-Medium.ttf", 25); lw = max(d.textlength(fe, font=ff) / S for fe in content)
            w_ = lw + 96; h_ = len(content) * 40 + 24; x1 = W0 - 70; x0 = x1 - w_
            _bubble(img, d, x0, y, w_, h_, acc, "r")
            for i, fe in enumerate(content):
                yy = y + 12 + i * 40 + 20
                check_icon(d, x0 + 38, yy, 13, WHITE, acc)
                d.text(P(x0 + 64, yy), fe, font=ff, fill=WHITE, anchor="lm")
            y += h_ + 22
        elif kind == "a":
            ff = f("Poppins-SemiBold.ttf", 26) if rf.os.path.exists(rf.G + "Poppins-SemiBold.ttf") else f("Poppins-Bold.ttf", 26)
            w_ = d.textlength(content, font=ff) / S + 60; x1 = W0 - 70; x0 = x1 - w_
            _bubble(img, d, x0, y, w_, 60, acc, "r")
            d.text(P(x0 + 30, y + 30), content, font=ff, fill=WHITE, anchor="lm"); y += 80
    p["_chat_end"] = y
    d.text(P(W0 / 2, H0 - 38), "everydaycart.online", font=f("Poppins-Bold.ttf", 27), fill=mix(bg, ink, 0.8), anchor="mm")
    logo_chip(img, 44, 34, 110)
    return rf.finish(img, p["out"])


TEMPLATES10 = {"U": template_u, "V": template_v}
