"""Style set 12 (added 17 Nov 2026): Y pinboard (flat dotted board, tilted polaroid with washi tape holding the
product, hanging price tag on a string, Bangla line on a taped paper strip, features on a row of tilted sticky notes;
collection mode pins two polaroids, each with its name and price written in the bottom margin),
Z wave poster (bold colour top half with a flat wave edge, concentric circles behind a big product that crosses the
wave, round price badge with a ring, centred title, Bangla line, 2x2 feature list, colour footer;
collection mode puts two products on the wave, each with its own round badge).
Flat only (no gradients, no blur), Poppins + Hind Siliguri, small logo chip in a corner."""
import math
from PIL import Image, ImageDraw
import render_flat as rf
from render_flat import P, f, fit, wrap, tk, S, W, H, W0, H0, INK, check_icon
from render_styles4 import logo_chip, mix, strike
from render_styles6 import _layer
from render_styles8 import _scaled, _bn_fit

WHITE = (255, 255, 255)


def _paste_center(L, prod, cx, cy, maxw, maxh):
    pr = _scaled(prod, maxw, maxh)
    L.alpha_composite(pr, (int(cx * S - pr.width / 2), int(cy * S - pr.height / 2)))


def _tagpill(d, text, fill, col, y=40):
    tf = f("Poppins-Bold.ttf", 21); tw = d.textlength(text, font=tf) / S
    d.rounded_rectangle(P(W0 - 44 - tw - 40, y, W0 - 44, y + 46), radius=23 * S, fill=fill)
    d.text(P(W0 - 44 - tw - 20, y + 23), text, font=tf, fill=col, anchor="mm" if False else "lm")


# ---------------- Template Y: pinboard ----------------
def template_y(p):
    bg = p.get("bg", (236, 214, 184)); ink = p.get("ink", INK)
    acc = p.get("acc", (226, 88, 64)); acc2 = p.get("acc2", (120, 200, 190))
    notes = p.get("notes", [(255, 226, 110), (255, 182, 196), (170, 226, 200), (184, 206, 255)])
    img = Image.new("RGBA", (W, H), bg + (255,)); d = ImageDraw.Draw(img)
    # flat dotted board texture
    dc = mix(bg, ink, 0.08)
    for yy in range(20, H0, 44):
        off = 22 if (yy // 44) % 2 else 0
        for xx in range(10 + off, W0, 44): d.ellipse(P(xx - 2.2, yy - 2.2, xx + 2.2, yy + 2.2), fill=dc)
    # headline
    h1, h2 = p["head"]; y = 128
    ft = f("Poppins-Bold.ttf", p.get("hsize", 60))
    for l in (h1, h2): ft = fit(d, l, "Poppins-Bold.ttf", ft.size / S, p.get("hw", 960))
    d.text(P(60, y), h1, font=ft, fill=ink); d.text(P(60, y + ft.size / S * 1.12), h2, font=ft, fill=acc)

    def polaroid(box, prod, ang, mw, mh, name=None, price=None, regular=None, tape=acc2, pdy=0):
        x0, y0, x1, y1 = box; w, h = x1 - x0, y1 - y0; bm = 110 if name else 70

        def dr(L):
            dl = ImageDraw.Draw(L)
            dl.rectangle(P(6, 8, w, h), fill=mix(bg, ink, 0.22))           # flat offset shadow
            dl.rectangle(P(0, 0, w - 6, h - 8), fill=WHITE)
            dl.rectangle(P(26, 26, w - 32, h - 8 - bm), fill=p.get("photo", mix(tape, WHITE, 0.72)))
            _paste_center(L, prod, (w - 6) / 2, (26 + h - 8 - bm) / 2 + pdy, mw, mh)
            dl = ImageDraw.Draw(L)
            if name:
                nf = fit(dl, name, "Poppins-Bold.ttf", 26, w - 70)
                dl.text(P((w - 6) / 2, h - 8 - bm + 32), name, font=nf, fill=ink, anchor="mm")
                pt = tk(price); pf = f("Poppins-Bold.ttf", 34)
                if regular and regular > price:
                    rt = tk(regular); rfo = f("Poppins-Medium.ttf", 20)
                    pw = dl.textlength(pt, font=pf) / S; rw = dl.textlength(rt, font=rfo) / S; gx = (w - 6) / 2 - (pw + 16 + rw) / 2
                    dl.text(P(gx, h - 8 - bm + 74), pt, font=pf, fill=acc, anchor="lm")
                    strike(dl, gx + pw + 16, h - 8 - bm + 62, rt, rfo, mix(WHITE, ink, 0.5))
                else:
                    dl.text(P((w - 6) / 2, h - 8 - bm + 74), pt, font=pf, fill=acc, anchor="mm")
        _layer(img, box, dr, ang)
        # washi tape across the top edge
        tw_, th_ = 170, 46
        cx = (x0 + x1) / 2; ty = y0 - 4

        def dt(L):
            dl = ImageDraw.Draw(L); dl.rectangle(P(0, 0, tw_, th_), fill=tape)
            for k in range(0, tw_, 24): dl.rectangle(P(k, 0, k + 10, th_), fill=mix(tape, WHITE, 0.3))
            for k in range(0, th_, 8):   # zigzag ends
                dl.polygon([P(0, k), P(5, k + 4), P(0, k + 8)], fill=(0, 0, 0, 0))
        _layer(img, (cx - tw_ / 2, ty - th_ / 2, cx + tw_ / 2, ty + th_ / 2), dt, -ang * 2 + 4)

    items = p.get("items")
    PY0, PY1 = 300, p.get("py1", 900)
    if items:
        for it in items:
            w2 = it.get("w", 440); polaroid((it["cx"] - w2 / 2, PY0 + it.get("oy", 0), it["cx"] + w2 / 2, PY1 + it.get("oy", 0)),
                                            it["img"], it.get("ang", -3), it["mw"], it["mh"], it["name"], it["price"], it.get("regular"),
                                            it.get("tape", acc2), it.get("pdy", 0))
    else:
        polaroid((70, PY0, 640, PY1), p["img"], p.get("ang", -3), p.get("maxw", 430), p.get("maxh", 440), pdy=p.get("pdy", 0))
        # hanging price tag on a string from a pin
        d = ImageDraw.Draw(img); TX = 850; pin_y = 300
        d.line(P(TX, pin_y, TX - 6, pin_y + 92), fill=ink, width=3 * S)
        d.ellipse(P(TX - 13, pin_y - 13, TX + 13, pin_y + 13), fill=acc)
        d.ellipse(P(TX - 5, pin_y - 7, TX + 1, pin_y - 1), fill=mix(acc, WHITE, 0.5))
        tw2, th2 = 290, 250

        def dp(L):
            dl = ImageDraw.Draw(L)
            dl.polygon([P(tw2 / 2, 0), P(tw2, 56), P(tw2, th2), P(0, th2), P(0, 56)], fill=p.get("tagc", ink))
            dl.ellipse(P(tw2 / 2 - 11, 26, tw2 / 2 + 11, 48), fill=bg)
            tc = p.get("tagt", WHITE)
            dl.text(P(tw2 / 2, 84), p.get("label", "PRICE"), font=f("Poppins-Bold.ttf", 22), fill=mix(tc, p.get("tagc", ink), 0.3), anchor="mm")
            pt = tk(p["price"]); pf = fit(dl, pt, "Poppins-Bold.ttf", 60, tw2 - 40)
            dl.text(P(tw2 / 2, 142), pt, font=pf, fill=tc, anchor="mm")
            if p.get("regular", 0) > p["price"]:
                rt = "Regular " + tk(p["regular"]); rfo = f("Poppins-Medium.ttf", 21); rw = dl.textlength(rt, font=rfo) / S
                strike(dl, tw2 / 2 - rw / 2, 192, rt, rfo, mix(tc, p.get("tagc", ink), 0.4))
        _layer(img, (TX - tw2 / 2 - 4, pin_y + 70, TX + tw2 / 2 - 4, pin_y + 70 + th2), dp, p.get("tang", 5))
        st = p.get("sticker")
        if st:   # round sticker under the tag
            d = ImageDraw.Draw(img); sx, sy, r = 860, 760, 92
            d.ellipse(P(sx - r, sy - r, sx + r, sy + r), fill=notes[0])
            d.ellipse(P(sx - r + 10, sy - r + 10, sx + r - 10, sy + r - 10), outline=ink, width=2 * S)
            words = st.split(); ln = [" ".join(words[:len(words) // 2 or 1]), " ".join(words[len(words) // 2 or 1:])]
            ln = [l for l in ln if l]
            for i, l in enumerate(ln):
                sf = fit(d, l, "Poppins-Bold.ttf", 28, 2 * r - 50)
                d.text(P(sx, sy + (i - (len(ln) - 1) / 2) * 34), l, font=sf, fill=ink, anchor="mm")
    d = ImageDraw.Draw(img)
    # title
    y = PY1 + 34
    ftt, tl = wrap(d, p["title"], "Poppins-Bold.ttf", 34, W0 - 120, 1)
    d.text(P(60, y), tl[0], font=ftt, fill=ink); y += ftt.size / S * 1.45
    # Bangla on a taped paper strip
    if p.get("bn"):
        fb = _bn_fit(d, p["bn"], 29, W0 - 180); bw = d.textlength(p["bn"], font=fb) / S
        d.rectangle(P(56, y, 56 + bw + 50, y + 58), fill=WHITE)
        tc = mix(acc, WHITE, 0.35)
        _layer(img, (32, y - 2, 98, y + 26), lambda L: ImageDraw.Draw(L).rectangle(P(0, 0, 66, 28), fill=tc + (225,)), 32)
        d = ImageDraw.Draw(img)
        d.text(P(81, y + 33), p["bn"], font=fb, fill=ink, anchor="lm"); y += 84
    # sticky notes row
    feats = p.get("feats", [])[:4]; n = len(feats)
    if n:
        gap = 18; nw = (W0 - 100 - gap * (n - 1)) / n; nh = H0 - 86 - y
        angs = [-3, 2, -2, 3]
        for i, fe in enumerate(feats):
            x0 = 50 + i * (nw + gap); col = notes[i % len(notes)]

            def dn(L, fe=fe, col=col):
                dl = ImageDraw.Draw(L)
                dl.rectangle(P(4, 6, nw, nh), fill=mix(bg, ink, 0.2))
                dl.rectangle(P(0, 0, nw - 4, nh - 6), fill=col)
                dl.rectangle(P(0, 0, nw - 4, 16), fill=mix(col, ink, 0.12))
                fo, ls = wrap(dl, fe, "Poppins-SemiBold.ttf" if False else "Poppins-Bold.ttf", 24, nw - 34, 3)
                lh = fo.size / S * 1.18; ty = 16 + (nh - 22 - lh * len(ls)) / 2
                for j, l in enumerate(ls):
                    dl.text(P((nw - 4) / 2, ty + j * lh + lh / 2), l, font=fo, fill=ink, anchor="mm")
            _layer(img, (x0, y, x0 + nw, y + nh), dn, angs[i % 4])
    d = ImageDraw.Draw(img)
    d.text(P(W0 / 2, H0 - 40), "everydaycart.online  |  Inbox us to order", font=f("Poppins-Bold.ttf", 25), fill=ink, anchor="mm")
    logo_chip(img, 40, 32, 110); d = ImageDraw.Draw(img)
    _tagpill(d, p["tag"], ink, WHITE, 42)
    return rf.finish(img, p["out"])


# ---------------- Template Z: wave poster ----------------
def template_z(p):
    top = p.get("top", (34, 74, 150)); bg = p.get("bg", (250, 246, 238)); ink = p.get("ink", INK)
    acc = p.get("acc", (255, 196, 60)); htxt = p.get("htxt", WHITE)
    img = Image.new("RGBA", (W, H), bg + (255,)); d = ImageDraw.Draw(img)
    WY = p.get("wave_y", 760); amp = 26; per = W0 / 1.5
    pts = [P(0, 0)] + [P(x, WY + amp * math.sin(2 * math.pi * x / per + 0.6)) for x in range(0, W0 + 1, 6)] + [P(W0, 0)]
    d.polygon(pts, fill=top)
    items = p.get("items"); pcx, pcy = p.get("pcx", 430), p.get("pcy", 560)
    ring = mix(top, WHITE, 0.12); ring2 = mix(top, WHITE, 0.24)
    for (cx_, r) in ([(it["cx"], it.get("r", 210)) for it in items] if items else [(pcx, p.get("r", 280))]):
        d.ellipse(P(cx_ - r, pcy - r, cx_ + r, pcy + r), fill=ring)
        d.ellipse(P(cx_ - r * 0.72, pcy - r * 0.72, cx_ + r * 0.72, pcy + r * 0.72), fill=ring2)
    # repaint below the wave so the rings stay in the colour half
    low = [P(0, H0)] + [P(x, WY + amp * math.sin(2 * math.pi * x / per + 0.6)) for x in range(0, W0 + 1, 6)] + [P(W0, H0)]
    d.polygon(low, fill=bg)
    # thin second wave line in accent
    d.line([P(x, WY + 30 + amp * math.sin(2 * math.pi * x / per + 0.6)) for x in range(0, W0 + 1, 6)], fill=mix(acc, bg, 0.2), width=5 * S)
    # headline
    h1, h2 = p["head"]; y = 126
    ft = f("Poppins-Bold.ttf", p.get("hsize", 64))
    for l in (h1, h2): ft = fit(d, l, "Poppins-Bold.ttf", ft.size / S, 960)
    d.text(P(60, y), h1, font=ft, fill=htxt); d.text(P(60, y + ft.size / S * 1.1), h2, font=ft, fill=acc)
    if items:
        for it in items:
            pr = _scaled(it["img"], it["mw"], it["mh"])
            img.alpha_composite(pr, (int(it["cx"] * S - pr.width / 2), int((pcy + it.get("dy", 0)) * S - pr.height / 2)))
        d = ImageDraw.Draw(img)
        for it in items:
            bx, by, r = it["bx"], it["by"], 86
            d.ellipse(P(bx - r - 6, by - r - 6, bx + r + 6, by + r + 6), fill=bg)
            d.ellipse(P(bx - r, by - r, bx + r, by + r), fill=acc)
            d.ellipse(P(bx - r + 9, by - r + 9, bx + r - 9, by + r - 9), outline=ink, width=2 * S)
            nf = fit(d, it["name"], "Poppins-Bold.ttf", 19, 2 * r - 46)
            d.text(P(bx, by - 30), it["name"], font=nf, fill=ink, anchor="mm")
            pf = fit(d, tk(it["price"]), "Poppins-Bold.ttf", 36, 2 * r - 34)
            d.text(P(bx, by + 10), tk(it["price"]), font=pf, fill=ink, anchor="mm")
            if it.get("regular", 0) > it["price"]:
                rt = tk(it["regular"]); rfo = f("Poppins-Medium.ttf", 17); rw = d.textlength(rt, font=rfo) / S
                strike(d, bx - rw / 2, by + 36, rt, rfo, mix(acc, ink, 0.55))
    else:
        pr = _scaled(p["img"], p.get("maxw", 520), p.get("maxh", 520))
        img.alpha_composite(pr, (int((pcx + p.get("dx", 0)) * S - pr.width / 2), int((pcy + p.get("dy", 0)) * S - pr.height / 2)))
        d = ImageDraw.Draw(img)
        bx, by, r = p.get("bx", 855), p.get("by", 470), 128
        d.ellipse(P(bx - r - 8, by - r - 8, bx + r + 8, by + r + 8), fill=top)
        d.ellipse(P(bx - r, by - r, bx + r, by + r), fill=acc)
        d.ellipse(P(bx - r + 12, by - r + 12, bx + r - 12, by + r - 12), outline=ink, width=2 * S)
        d.text(P(bx, by - 52), p.get("label", "PRICE"), font=f("Poppins-Bold.ttf", 22), fill=ink, anchor="mm")
        pf = fit(d, tk(p["price"]), "Poppins-Bold.ttf", 54, 2 * r - 50)
        d.text(P(bx, by + 2), tk(p["price"]), font=pf, fill=ink, anchor="mm")
        if p.get("regular", 0) > p["price"]:
            rt = tk(p["regular"]); rfo = f("Poppins-Medium.ttf", 24); rw = d.textlength(rt, font=rfo) / S
            strike(d, bx - rw / 2, by + 40, rt, rfo, mix(acc, ink, 0.55))
        st = p.get("sticker")
        if st:
            sf = f("Poppins-Bold.ttf", 22); sw = d.textlength(st, font=sf) / S + 44; sx, sy = p.get("sx", 855), p.get("sy", 660)
            d.rounded_rectangle(P(sx - sw / 2, sy - 25, sx + sw / 2, sy + 25), radius=25 * S, fill=WHITE)
            d.text(P(sx, sy), st, font=sf, fill=top, anchor="mm")
    # lower half: title, Bangla line, features
    y = p.get("text_y", WY + 140)
    ftt, tl = wrap(d, p["title"], "Poppins-Bold.ttf", 40, W0 - 120, 1)
    d.text(P(W0 / 2, y), tl[0], font=ftt, fill=ink, anchor="mt"); y += ftt.size / S * 1.5
    if p.get("bn"):
        fb = _bn_fit(d, p["bn"], 34, W0 - 140)
        d.text(P(W0 / 2, y + 24), p["bn"], font=fb, fill=p.get("bncol", top), anchor="mm"); y += 92
    feats = p.get("feats", [])[:4]; cw = (W0 - 140) / 2
    y = max(y, p.get("feat_y", 0))
    for i, fe in enumerate(feats):
        fx = 70 + (i % 2) * cw; fy = y + (i // 2) * 68
        check_icon(d, fx + 18, fy + 22, 18, top, WHITE)
        d.text(P(fx + 50, fy + 22), fe, font=fit(d, fe, "Poppins-Medium.ttf", 28, cw - 66), fill=ink, anchor="lm")
    d.rectangle(P(0, H0 - 74, W0, H0), fill=top)
    d.text(P(W0 / 2, H0 - 37), "everydaycart.online  |  Inbox us to order", font=f("Poppins-Bold.ttf", 26), fill=acc, anchor="mm")
    logo_chip(img, 40, 32, 110); d = ImageDraw.Draw(img)
    _tagpill(d, p["tag"], acc, ink, 42)
    return rf.finish(img, p["out"])


TEMPLATES12 = {"Y": template_y, "Z": template_z}
