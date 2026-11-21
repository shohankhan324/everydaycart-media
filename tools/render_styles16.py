"""Style set 16 (added 21 Nov 2026):
AG die-cut sticker sheet (solid colour background with a flat dot grid, the product as a die-cut sticker with a thick
white border and a solid offset shadow, tilted price sticker, round spec sticker, Bangla pill sticker, four label
stickers for features; collection mode gives every product its own die-cut sticker and price sticker),
AH film strip (deep background, tilted film strip with sprocket holes, product in the centre frame, spec numbers in the
side frames, price tag overlapping the strip, title + Bangla line + features below; collection mode puts each product in
its own frame with a name and price chip).
Flat only (no gradients, no blur, no 3D), Poppins + Hind Siliguri, small logo chip in a corner."""
import numpy as np
from PIL import Image, ImageDraw
from scipy import ndimage
import render_flat as rf
from render_flat import P, f, fit, wrap, tk, S, W, H, W0, H0
from render_styles4 import logo_chip, mix, strike
from render_styles8 import _scaled, _bn_fit

WHITE = (255, 255, 255)
FOOT = "everydaycart.online  |  Inbox us to order"


def _bnq(d, x, y, text, size, maxw, col, anchor="lm"):
    """Bangla text; a trailing ? is drawn in Poppins (Hind Siliguri build has no ? we like)."""
    q = text.endswith("?"); body = text[:-1].rstrip() if q else text
    fb = _bn_fit(d, body, size, maxw - (30 if q else 0))
    w = d.textlength(body, font=fb) / S
    qf = f("Poppins-Bold.ttf", fb.size / S * 0.9)
    tw = w + (d.textlength("?", font=qf) / S + 4 if q else 0)
    if anchor == "mm": x = x - tw / 2
    d.text(P(x, y), body, font=fb, fill=col, anchor="lm")
    if q: d.text(P(x + w + 4, y), "?", font=qf, fill=col, anchor="lm")
    return tw


def diecut(prod, maxw, maxh, border=14, shadow=None, off=(12, 14)):
    """Scale product and return an RGBA die-cut sticker (white border + optional solid offset shadow)."""
    pr = _scaled(prod, maxw, maxh)
    b = int(border * S); ox, oy = int(off[0] * S), int(off[1] * S)
    pad = b + max(ox, oy) + 4
    Wc, Hc = pr.width + 2 * pad, pr.height + 2 * pad
    a = np.zeros((Hc, Wc), float); a[pad:pad + pr.height, pad:pad + pr.width] = np.asarray(pr)[..., 3] / 255
    fg = a > 0.35
    fg = ndimage.binary_fill_holes(fg)
    dist = ndimage.distance_transform_edt(~fg)
    m = np.clip(b - dist + 0.5, 0, 1)
    out = Image.new("RGBA", (Wc, Hc), (0, 0, 0, 0))
    if shadow:
        sh = np.zeros_like(m); sh[oy:, ox:] = m[:Hc - oy, :Wc - ox]
        L = Image.new("RGBA", (Wc, Hc), shadow + (0,)); L.putalpha(Image.fromarray((sh * 255).astype(np.uint8)))
        out.alpha_composite(L)
    L = Image.new("RGBA", (Wc, Hc), WHITE + (0,)); L.putalpha(Image.fromarray((m * 255).astype(np.uint8)))
    out.alpha_composite(L)
    out.alpha_composite(pr, (pad, pad))
    return out


def _paste_c(img, layer, cx, cy):
    img.alpha_composite(layer, (int(cx * S - layer.width / 2), int(cy * S - layer.height / 2)))


def _rot_sticker(img, w, h, ang, draw_fn, cx, cy, fill, border=WHITE, bw=8, shadow=None, r=26):
    """Draw a rounded sticker on its own layer, rotate it, paste centred at (cx, cy)."""
    pad = 40
    L = Image.new("RGBA", P(w + 2 * pad, h + 2 * pad), (0, 0, 0, 0)); d = ImageDraw.Draw(L)
    if shadow: d.rounded_rectangle(P(pad + 10, pad + 12, pad + w + 10, pad + h + 12), radius=r * S, fill=shadow)
    d.rounded_rectangle(P(pad, pad, pad + w, pad + h), radius=r * S, fill=border)
    d.rounded_rectangle(P(pad + bw, pad + bw, pad + w - bw, pad + h - bw), radius=(r - bw / 2) * S, fill=fill)
    draw_fn(d, pad, pad, w, h)
    L = L.rotate(ang, expand=True, resample=Image.BICUBIC)
    _paste_c(img, L, cx, cy)


def _price_sticker(img, cx, cy, price, regular, fill, col, sub, ang=6, shadow=None, w=250, h=186, label="ONLY"):
    def fn(d, x, y, w_, h_):
        d.text(P(x + w_ / 2, y + 38), label, font=f("Poppins-Bold.ttf", 22), fill=col, anchor="mm")
        pt = tk(price); pf = fit(d, pt, "Poppins-Bold.ttf", 54, w_ - 40)
        d.text(P(x + w_ / 2, y + h_ / 2 - 2), pt, font=pf, fill=col, anchor="mm")
        if regular and regular > price:
            rt = "Regular " + tk(regular); rfo = fit(d, rt, "Poppins-Medium.ttf", 20, w_ - 50); rw = d.textlength(rt, font=rfo) / S
            strike(d, x + w_ / 2 - rw / 2, y + h_ - 52, rt, rfo, sub)
    _rot_sticker(img, w, h, ang, fn, cx, cy, fill, shadow=shadow)


def _dots(d, bg, step=54):
    dc = mix(bg, (0, 0, 0), 0.07) if sum(bg) > 300 else mix(bg, WHITE, 0.08)
    for y in range(24, H0, step):
        for x in range(24 + (step // 2 if (y // step) % 2 else 0), W0, step):
            d.ellipse(P(x - 3, y - 3, x + 3, y + 3), fill=dc)


def _pill(d, x1, y, text, fill, col):
    tf = f("Poppins-Bold.ttf", 21); tw = d.textlength(text, font=tf) / S
    d.rounded_rectangle(P(x1 - tw - 40, y, x1, y + 46), radius=23 * S, fill=fill)
    d.text(P(x1 - tw - 20, y + 23), text, font=tf, fill=col, anchor="lm")


# ---------------- Template AG: die-cut sticker sheet ----------------
def template_ag(p):
    bg = p.get("bg", (255, 214, 64)); ink = p.get("ink", (24, 26, 36)); acc = p.get("acc", (236, 72, 96))
    acc2 = p.get("acc2", (60, 110, 230)); shc = p.get("shadow", mix(bg, ink, 0.28)); hcol = p.get("hcol", ink)
    labels = p.get("labels", [mix(acc, WHITE, 0.75), mix(acc2, WHITE, 0.75), mix(acc, WHITE, 0.75), mix(acc2, WHITE, 0.75)])
    img = Image.new("RGBA", (W, H), bg + (255,)); d = ImageDraw.Draw(img); _dots(d, bg)
    logo_chip(img, 44, 32, 110, fill=WHITE); d = ImageDraw.Draw(img)
    _pill(d, W0 - 44, 40, p["tag"], ink, WHITE)
    # headline
    h1, h2 = p["head"]; hf = f("Poppins-Bold.ttf", p.get("hsize", 70))
    for l in (h1, h2): hf = fit(d, l, "Poppins-Bold.ttf", hf.size / S, p.get("hw", 980))
    d.text(P(52, 120), h1, font=hf, fill=hcol); d.text(P(52, 120 + hf.size / S * 1.08), h2, font=hf, fill=p.get("hcol2", acc))
    items = p.get("items")
    if items:
        for it in items:
            st = diecut(it["img"], it["mw"], it["mh"], border=it.get("border", 12), shadow=shc)
            st = st.rotate(it.get("ang", 0), expand=True, resample=Image.BICUBIC)
            _paste_c(img, st, it["cx"], it["cy"])
            d = ImageDraw.Draw(img)
            nm = it["name"]; nf = fit(d, nm, "Poppins-Bold.ttf", 23, it.get("nmax", 300)); nw = d.textlength(nm, font=nf) / S + 40
            ny = it.get("ny", it["cy"] + it["mh"] / 2 + 34)
            d.rounded_rectangle(P(it["cx"] - nw / 2 + 6, ny + 6, it["cx"] + nw / 2 + 6, ny + 54), radius=24 * S, fill=shc)
            d.rounded_rectangle(P(it["cx"] - nw / 2, ny, it["cx"] + nw / 2, ny + 48), radius=24 * S, fill=WHITE)
            d.text(P(it["cx"], ny + 24), nm, font=nf, fill=ink, anchor="mm")
            _price_sticker(img, it.get("px", it["cx"] + 120), it.get("py", it["cy"] - it["mh"] / 2 + 40), it["price"], it.get("regular"),
                           it.get("pfill", acc), WHITE, mix(WHITE, acc, 0.35), ang=it.get("pang", 7), shadow=shc, w=214, h=170)
            d = ImageDraw.Draw(img)
    else:
        st = diecut(p["img"], p.get("maxw", 560), p.get("maxh", 520), border=p.get("border", 16), shadow=shc)
        st = st.rotate(p.get("ang", -4), expand=True, resample=Image.BICUBIC)
        _paste_c(img, st, p.get("cx", 440), p.get("cy", 600))
        _price_sticker(img, p.get("px", 850), p.get("py", 470), p["price"], p.get("regular"), acc, WHITE, mix(WHITE, acc, 0.35),
                       ang=p.get("pang", 7), shadow=shc)
        d = ImageDraw.Draw(img)
        if p.get("spec"):   # round spec sticker
            big_, small_ = p["spec"]; cx, cy, r = p.get("sx", 860), p.get("sy", 730), 92
            d.ellipse(P(cx - r + 8, cy - r + 10, cx + r + 8, cy + r + 10), fill=shc)
            d.ellipse(P(cx - r, cy - r, cx + r, cy + r), fill=WHITE)
            d.ellipse(P(cx - r + 8, cy - r + 8, cx + r - 8, cy + r - 8), fill=acc2)
            bf = fit(d, big_, "Poppins-Bold.ttf", 44, 130); d.text(P(cx, cy - 12), big_, font=bf, fill=WHITE, anchor="mm")
            sf = fit(d, small_, "Poppins-Bold.ttf", 17, 120); d.text(P(cx, cy + 30), small_, font=sf, fill=WHITE, anchor="mm")
    # Bangla pill sticker
    by = p.get("bn_y", 950)
    d.rounded_rectangle(P(58, by + 8, W0 - 42, by + 82), radius=37 * S, fill=shc)
    d.rounded_rectangle(P(50, by, W0 - 50, by + 74), radius=37 * S, fill=WHITE)
    d.rounded_rectangle(P(58, by + 8, W0 - 58, by + 66), radius=29 * S, fill=mix(acc2, WHITE, 0.88))
    _bnq(d, W0 / 2, by + 37, p["bn"], 33, W0 - 180, ink, anchor="mm")
    # title
    ty = by + 100
    ftt, tl = wrap(d, p["title"], "Poppins-Bold.ttf", 34, W0 - 110, 1)
    d.text(P(W0 / 2, ty + 18), tl[0], font=ftt, fill=hcol, anchor="mm")
    # four label stickers
    feats = p.get("feats", [])[:4]; y0 = ty + 52; gap = 18; cw = (W0 - 100 - gap) / 2; rh = 66
    for i, fe in enumerate(feats):
        x = 50 + (i % 2) * (cw + gap); y = y0 + (i // 2) * (rh + 16)
        d.rounded_rectangle(P(x + 6, y + 7, x + cw + 6, y + rh + 7), radius=16 * S, fill=shc)
        d.rounded_rectangle(P(x, y, x + cw, y + rh), radius=16 * S, fill=WHITE)
        d.rounded_rectangle(P(x + 6, y + 6, x + cw - 6, y + rh - 6), radius=12 * S, fill=labels[i])
        d.ellipse(P(x + 20, y + rh / 2 - 12, x + 44, y + rh / 2 + 12), fill=ink)
        d.line([P(x + 26, y + rh / 2), P(x + 30, y + rh / 2 + 5), P(x + 38, y + rh / 2 - 6)], fill=WHITE, width=3 * S, joint="curve")
        d.text(P(x + 58, y + rh / 2), fe, font=fit(d, fe, "Poppins-Medium.ttf", 25, cw - 80), fill=ink, anchor="lm")
    d.text(P(W0 / 2, H0 - 36), FOOT, font=f("Poppins-Bold.ttf", 24), fill=p.get("foot", ink), anchor="mm")
    return rf.finish(img, p["out"])


# ---------------- Template AH: film strip ----------------
def template_ah(p):
    bg = p.get("bg", (22, 40, 64)); film = p.get("film", (16, 16, 20)); acc = p.get("acc", (255, 196, 48))
    frames = p.get("frames", [(250, 232, 214), (214, 232, 250), (232, 250, 214)]); ink = (22, 24, 30)
    img = Image.new("RGBA", (W, H), bg + (255,)); d = ImageDraw.Draw(img)
    logo_chip(img, 44, 32, 110, fill=WHITE); d = ImageDraw.Draw(img)
    _pill(d, W0 - 44, 40, p["tag"], acc, ink)
    h1, h2 = p["head"]; hf = f("Poppins-Bold.ttf", p.get("hsize", 64))
    for l in (h1, h2): hf = fit(d, l, "Poppins-Bold.ttf", hf.size / S, 980)
    d.text(P(52, 120), h1, font=hf, fill=WHITE); d.text(P(52, 120 + hf.size / S * 1.08), h2, font=hf, fill=acc)
    # film strip layer (wider than canvas so the tilt never shows ends)
    SW, SH = 1400, p.get("strip_h", 560); ang = p.get("ang", -3)
    L = Image.new("RGBA", P(SW, SH), (0, 0, 0, 0)); ld = ImageDraw.Draw(L)
    ld.rectangle(P(0, 0, SW, SH), fill=film)
    hole = mix(bg, WHITE, 0.15)
    for x in range(14, SW, 58):
        ld.rounded_rectangle(P(x, 16, x + 32, 40), radius=6 * S, fill=hole)
        ld.rounded_rectangle(P(x, SH - 40, x + 32, SH - 16), radius=6 * S, fill=hole)
    FY0, FY1 = 62, SH - 62; ox = (SW - W0) / 2   # canvas x -> layer x
    eb = f("Poppins-Bold.ttf", 15)
    items = p.get("items")
    if items:
        n = len(items); gap = 26; fw = (W0 - 80 - gap * (n - 1)) / n
        for k, it in enumerate(items):
            x0 = ox + 40 + k * (fw + gap); x1 = x0 + fw
            ld.rectangle(P(x0, FY0, x1, FY1), fill=frames[k % len(frames)])
            ld.text(P(x0 + 4, FY1 + 6), f"EC {k + 1:02d}A", font=eb, fill=acc)
            pr = _scaled(it["img"], it.get("mw", fw - 70), it.get("mh", FY1 - FY0 - 150))
            L.alpha_composite(pr, (int((x0 + x1) / 2 * S - pr.width / 2), int(((FY0 + FY1 - 110) / 2 + it.get("dy", 0)) * S - pr.height / 2)))
            ld = ImageDraw.Draw(L)
            nm = it["name"]; nf = fit(ld, nm, "Poppins-Bold.ttf", 22, fw - 40)
            ld.text(P((x0 + x1) / 2, FY1 - 92), nm, font=nf, fill=ink, anchor="mm")
            pt = tk(it["price"]); pf = f("Poppins-Bold.ttf", 30); pw = ld.textlength(pt, font=pf) / S + 36
            ld.rounded_rectangle(P((x0 + x1) / 2 - pw / 2, FY1 - 66, (x0 + x1) / 2 + pw / 2, FY1 - 18), radius=10 * S, fill=ink)
            ld.text(P((x0 + x1) / 2, FY1 - 42), pt, font=pf, fill=acc, anchor="mm")
    else:
        cx0, cx1 = ox + 250, ox + W0 - 250
        side = p.get("side", [])
        # side frames
        for k, (sx0, sx1) in enumerate([(ox - 340, ox + 222), (ox + W0 - 222, ox + W0 + 340)]):
            ld.rectangle(P(sx0, FY0, sx1, FY1), fill=frames[(k + 1) % len(frames)])
            if k < len(side):
                big_, small_ = side[k]; tx = (ox + 30 + ox + 222) / 2 if k == 0 else (ox + W0 - 222 + ox + W0 - 30) / 2
                bf = fit(ld, big_, "Poppins-Bold.ttf", 54, 175); ld.text(P(tx, (FY0 + FY1) / 2 - 22), big_, font=bf, fill=ink, anchor="mm")
                sf = fit(ld, small_, "Poppins-Bold.ttf", 19, 170); ld.text(P(tx, (FY0 + FY1) / 2 + 30), small_, font=sf, fill=mix(ink, WHITE, 0.25), anchor="mm")
        ld.rectangle(P(cx0, FY0, cx1, FY1), fill=frames[0])
        for k, x in enumerate((ox + 30, cx0, ox + W0 - 222)):
            ld.text(P(x + 4, FY1 + 6), f"EC {k + 11}A", font=eb, fill=acc)
        pr = _scaled(p["img"], p.get("maxw", cx1 - cx0 - 70), p.get("maxh", FY1 - FY0 - 60))
        L.alpha_composite(pr, (int(((cx0 + cx1) / 2 + p.get("dx", 0)) * S - pr.width / 2), int(((FY0 + FY1) / 2 + p.get("dy", 0)) * S - pr.height / 2)))
    L = L.rotate(ang, expand=True, resample=Image.BICUBIC)
    SY = p.get("strip_y", 600)
    _paste_c(img, L, W0 / 2, SY); d = ImageDraw.Draw(img)
    if not items:
        _price_sticker(img, p.get("px", 830), p.get("py", SY + SH / 2 - 10), p["price"], p.get("regular"), acc, ink, mix(ink, acc, 0.4),
                       ang=p.get("pang", 5), shadow=None, w=240, h=160)
        d = ImageDraw.Draw(img)
    # info area
    y = SY + SH / 2 + p.get("info_gap", 95)
    ftt, tl = wrap(d, p["title"], "Poppins-Bold.ttf", 36, W0 - 110, 1)
    d.text(P(52, y), tl[0], font=ftt, fill=WHITE); y += ftt.size / S * 1.62
    if p.get("bn"):
        _bnq(d, 52, y + 22, p["bn"], 31, W0 - 110, acc); y += 70
    feats = p.get("feats", [])[:4]; cw = (W0 - 104) / 2; Y1 = H0 - 80; rowh = min(72, (Y1 - y) / 2)
    for i, fe in enumerate(feats):
        fx = 52 + (i % 2) * cw; fy = y + (i // 2) * rowh + rowh / 2
        d.rectangle(P(fx, fy - 12, fx + 16, fy + 12), fill=acc)
        d.rectangle(P(fx + 6, fy - 12, fx + 10, fy + 12), fill=bg)
        d.text(P(fx + 32, fy), fe, font=fit(d, fe, "Poppins-Medium.ttf", 26, cw - 50), fill=WHITE, anchor="lm")
    d.line(P(52, H0 - 70, W0 - 52, H0 - 70), fill=mix(bg, WHITE, 0.25), width=2 * S)
    d.text(P(W0 / 2, H0 - 36), FOOT, font=f("Poppins-Bold.ttf", 24), fill=WHITE, anchor="mm")
    return rf.finish(img, p["out"])


TEMPLATES16 = {"AG": template_ag, "AH": template_ah}
