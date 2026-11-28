"""Style set 23 (added 28 Nov 2026):
AU instant photo poster (solid colour poster, the product sits inside a big tilted white instant photo frame held by
two flat tape strips, the frame's bottom margin carries the product's short name, a round price sticker overlaps the
lower right corner, flat sparkle shapes, big left aligned headline, rounded info card with Bangla line, title and tick
chips; collection mode fans two or three smaller photo frames with name and price under each),
AV ticket poster (big flat event ticket across the poster with notched edges and a dashed perforation, a coloured
panel with a spotlight circle holds the product on the left, the stub on the right holds the price and flat barcode
bars, bold centred headline above, rounded info card with Bangla line, title and tick chips below).
Flat only (no gradients, no blur, no 3D), Poppins + Hind Siliguri, small logo chip in a corner."""
import math
from PIL import Image, ImageDraw
import render_flat as rf
from render_flat import P, f, fit, wrap, tk, S, W, H, W0, H0
from render_styles4 import logo_chip, mix, strike
from render_styles16 import _bnq, _paste_c
from render_styles19 import _lum, _on, _ticks
from render_styles20 import _put, _tagpill

WHITE = (255, 255, 255)
FOOT = "everydaycart.online  |  Inbox us to order"


def _sparkle(d, cx, cy, r, col):
    k = r * .28
    d.polygon(P(cx, cy - r, cx + k, cy - k, cx + r, cy, cx + k, cy + k, cx, cy + r, cx - k, cy + k, cx - r, cy, cx - k, cy - k), fill=col)


def _headline(d, p, bg, ink, y=112, center=False):
    h1, h2 = p["head"]; hf = f("Poppins-Bold.ttf", p.get("hsize", 74))
    for l in (h1, h2): hf = fit(d, l, "Poppins-Bold.ttf", hf.size / S, W0 - 100)
    lh = hf.size / S * 1.04
    if center:
        d.text(P(W0 / 2, y), h1, font=hf, fill=_on(bg), anchor="mt"); d.text(P(W0 / 2, y + lh), h2, font=hf, fill=p.get("h2c", ink), anchor="mt")
    else:
        d.text(P(48, y), h1, font=hf, fill=_on(bg)); d.text(P(48, y + lh), h2, font=hf, fill=p.get("h2c", ink))
    return y + 2 * lh


def _card(d, p, bg, ink, acc, CY):
    d.rounded_rectangle(P(32, CY, W0 - 32, H0 - 78), radius=30 * S, fill=p.get("card", WHITE))
    by = CY + 48
    _bnq(d, 64, by, p["bn"], 33, W0 - 140, p.get("bnc", acc if _lum(acc) < 170 else ink))
    ftt, tl = wrap(d, p["title"], "Poppins-Bold.ttf", 29, W0 - 130, 1)
    d.text(P(64, by + 32), tl[0], font=ftt, fill=ink)
    _ticks(d, p.get("feats", []), by + 86, H0 - 100, p.get("tick", acc), ink, x0=56, x1=W0 - 56, chip=mix(WHITE, bg, 0.22))
    d.text(P(W0 / 2, H0 - 40), FOOT, font=f("Poppins-Bold.ttf", 23), fill=_on(bg), anchor="mm")


def _photo(img, prod, cx, cy, w, h, ang, inner, ink, caption, tape, cap_size=30, mw=None, mh=None, pdy=0, sub=None, subc=None):
    """White instant photo frame with product, rotated, pasted centred at (cx, cy)."""
    m = w * .06; bot = h - w + m           # square-ish photo window, deep bottom margin
    pad = 40
    L = Image.new("RGBA", P(w + 2 * pad, h + 2 * pad), (0, 0, 0, 0)); d = ImageDraw.Draw(L)
    d.rectangle(P(pad + 14, pad + 16, pad + w + 14, pad + h + 16), fill=ink)
    d.rectangle(P(pad, pad, pad + w, pad + h), fill=WHITE)
    pw = w - 2 * m; ph = h - m - bot
    d.rectangle(P(pad + m, pad + m, pad + m + pw, pad + m + ph), fill=inner)
    # flat floor ellipse + light spotlight circle behind product
    r = min(pw, ph) * .40
    d.ellipse(P(pad + w / 2 - r, pad + m + ph / 2 - r, pad + w / 2 + r, pad + m + ph / 2 + r), fill=mix(inner, WHITE, .35))
    _put(L, prod, pad + w / 2, pad + m + ph / 2 + pdy, mw or pw * .86, mh or ph * .86)
    d = ImageDraw.Draw(L)
    cyc = pad + m + ph + (bot - m) / 2 + m / 2
    cf = fit(d, caption, "Poppins-Bold.ttf", cap_size, w - 2 * m - 10)
    if sub:
        d.text(P(pad + w / 2, cyc - cap_size * .6), caption, font=cf, fill=ink, anchor="mm")
        sf = f("Poppins-Bold.ttf", cap_size * 1.05)
        d.text(P(pad + w / 2, cyc + cap_size * .75), sub, font=sf, fill=subc or ink, anchor="mm")
    else:
        d.text(P(pad + w / 2, cyc), caption, font=cf, fill=ink, anchor="mm")
    lay = L.rotate(ang, expand=True, resample=Image.BICUBIC)
    _paste_c(img, lay, cx, cy)
    # tape strips (drawn unrotated relative to frame corners, approximated after rotation)
    a = math.radians(-ang)
    for sx, ta in ((-w / 2 + w * .16, -18), (w / 2 - w * .16, 16)):
        tx = cx + sx * math.cos(a) - (-h / 2) * math.sin(a); ty = cy + sx * math.sin(a) + (-h / 2) * math.cos(a)
        tw, th = w * .26, 44
        T = Image.new("RGBA", P(tw + 20, th + 20), (0, 0, 0, 0)); td = ImageDraw.Draw(T)
        td.rectangle(P(10, 10, 10 + tw, 10 + th), fill=tape + (225,))
        _paste_c(img, T.rotate(ta + ang, expand=True, resample=Image.BICUBIC), tx, ty)


def _sticker(img, cx, cy, r, fill, ink, price, regular, label="ONLY", ang=-8):
    pad = 24; sz = 2 * r + 2 * pad
    L = Image.new("RGBA", P(sz, sz), (0, 0, 0, 0)); d = ImageDraw.Draw(L); c = sz / 2
    d.ellipse(P(c - r + 10, c - r + 12, c + r + 10, c + r + 12), fill=ink)
    d.ellipse(P(c - r, c - r, c + r, c + r), fill=fill, outline=ink, width=5 * S)
    d.ellipse(P(c - r + 16, c - r + 16, c + r - 16, c + r - 16), outline=_on(fill), width=2 * S)
    tc = _on(fill); hasr = regular and regular > price
    d.text(P(c, c - r * .42), label, font=f("Poppins-Bold.ttf", r * .17), fill=tc, anchor="mm")
    pt = tk(price); d.text(P(c, c - r * .02), pt, font=fit(d, pt, "Poppins-Bold.ttf", r * .40, r * 1.6), fill=tc, anchor="mm")
    if hasr:
        rt = "Regular " + tk(regular); rfo = fit(d, rt, "Poppins-Medium.ttf", r * .15, r * 1.3); rw = d.textlength(rt, font=rfo) / S
        strike(d, c - rw / 2, c + r * .30, rt, rfo, tc)
    _paste_c(img, L.rotate(ang, expand=True, resample=Image.BICUBIC), cx, cy)


# ---------------- Template AU: instant photo poster ----------------
def template_au(p):
    bg = p.get("bg", (255, 214, 90)); ink = p.get("ink", (24, 24, 32)); acc = p.get("acc", (240, 80, 90))
    CY = p.get("card_y", 1010); tape = p.get("tape", (255, 255, 255))
    img = Image.new("RGBA", (W, H), bg + (255,)); d = ImageDraw.Draw(img)
    spc = p.get("spark", mix(bg, WHITE, .45))
    for (sx, sy, sr) in p.get("sparks", [(100, 420, 26), (980, 330, 20), (960, 940, 24), (70, 900, 16)]):
        _sparkle(d, sx, sy, sr, spc)
    logo_chip(img, 40, 26, 104, fill=WHITE); d = ImageDraw.Draw(img)
    _tagpill(d, p["tag"], W0 - 40, 34, ink, WHITE, size=20)
    top = _headline(d, p, bg, ink) + 10
    items = p.get("items")
    if items:
        n = len(items); xs = p.get("xs", [W0 * (i + .5) / n for i in range(n)])
        pw_, ph_ = p.get("pw", 300), p.get("ph", 390); angs = p.get("angs", [-6, 3, -4][:n])
        cy = p.get("pcy", (top + CY) / 2 + 10)
        for k, it in enumerate(items):
            _photo(img, it["img"], xs[k], cy + it.get("y", 0), pw_, ph_, angs[k], it.get("inner", mix(acc, WHITE, .5)), ink,
                   it["name"], it.get("tape", tape), cap_size=22, mw=it.get("mw"), mh=it.get("mh"), pdy=it.get("dy", 0),
                   sub=tk(it["price"]), subc=it.get("pc", acc if _lum(acc) < 190 else ink))
        d = ImageDraw.Draw(img)
    else:
        cx = p.get("pcx", 520); cy = p.get("pcy", (top + CY) / 2 + 14)
        _photo(img, p["img"], cx, cy, p.get("pw", 560), p.get("ph", 640), p.get("ang", -4), p.get("inner", mix(acc, WHITE, .55)), ink,
               p["cap"], tape, cap_size=p.get("cap_size", 34), mw=p.get("maxw"), mh=p.get("maxh"), pdy=p.get("dy", 0))
        _sticker(img, p.get("sx", 860), p.get("sy", cy + 210), p.get("sr", 132), p.get("pricec", WHITE), ink, p["price"], p.get("regular"), p.get("plabel", "ONLY"))
        d = ImageDraw.Draw(img)
    _card(d, p, bg, ink, acc, CY)
    return rf.finish(img, p["out"])


# ---------------- Template AV: ticket poster ----------------
def _ticket_mask(w, h, perf, nr):
    m = Image.new("L", P(w, h), 0); d = ImageDraw.Draw(m)
    d.rounded_rectangle(P(0, 0, w, h), radius=28 * S, fill=255)
    for (x, y) in ((perf, 0), (perf, h), (0, h / 2), (w, h / 2)):
        d.ellipse(P(x - nr, y - nr, x + nr, y + nr), fill=0)
    return m


def template_av(p):
    bg = p.get("bg", (30, 40, 90)); ink = p.get("ink", (20, 20, 32)); acc = p.get("acc", (255, 200, 60))
    tf_ = p.get("ticket", (255, 248, 236)); pc = p.get("panel", acc); CY = p.get("card_y", 1000)
    img = Image.new("RGBA", (W, H), bg + (255,)); d = ImageDraw.Draw(img)
    for (sx, sy, sr) in p.get("sparks", [(90, 300, 18), (1000, 250, 22), (60, 940, 14), (1020, 950, 18)]):
        _sparkle(d, sx, sy, sr, p.get("spark", mix(bg, WHITE, .3)))
    logo_chip(img, 40, 26, 104, fill=WHITE); d = ImageDraw.Draw(img)
    _tagpill(d, p["tag"], W0 - 40, 34, acc, _on(acc), size=20)
    top = _headline(d, p, bg, ink, y=118, center=True) + 34
    x0, x1 = 40, W0 - 40; y0, y1 = top, CY - 44; w, h = x1 - x0, y1 - y0; perf = p.get("perf", 690); nr = 30
    mask = _ticket_mask(w, h, perf, nr)
    sh = Image.new("RGBA", mask.size, ink + (255,)); sh.putalpha(mask)
    img.alpha_composite(sh, (int((x0 + 14) * S), int((y0 + 16) * S)))
    tk_ = Image.new("RGBA", mask.size, tf_ + (255,)); tk_.putalpha(mask)
    img.alpha_composite(tk_, (int(x0 * S), int(y0 * S))); d = ImageDraw.Draw(img)
    # perforation
    px = x0 + perf; yy = y0 + nr + 16
    while yy < y1 - nr - 16:
        d.line(P(px, yy, px, yy + 16), fill=mix(tf_, ink, .45), width=4 * S); yy += 30
    # left product panel
    a, b, c_, e = x0 + 26 + 18, y0 + 26, x0 + perf - 26, y1 - 26
    d.rounded_rectangle(P(a, b, c_, e), radius=24 * S, fill=pc)
    # flat rays behind the product (stripes from the centre, clipped to the panel)
    cx, cy = (a + c_) / 2, (b + e) / 2
    R = Image.new("RGBA", P(c_ - a, e - b), (0, 0, 0, 0)); rd = ImageDraw.Draw(R); rcx, rcy = (c_ - a) / 2, (e - b) / 2
    rc = mix(pc, WHITE, .16)
    for i in range(12):
        t0 = math.radians(i * 30); t1 = math.radians(i * 30 + 13); L_ = 900
        rd.polygon(P(rcx, rcy, rcx + L_ * math.cos(t0), rcy + L_ * math.sin(t0), rcx + L_ * math.cos(t1), rcy + L_ * math.sin(t1)), fill=rc + (255,))
    rm = Image.new("L", R.size, 0); ImageDraw.Draw(rm).rounded_rectangle((0, 0, R.width, R.height), radius=24 * S, fill=255)
    R.putalpha(Image.composite(R.split()[3], Image.new("L", R.size, 0), rm))
    img.alpha_composite(R, (int(a * S), int(b * S))); d = ImageDraw.Draw(img)
    sr = min(c_ - a, e - b) * .36
    d.ellipse(P(cx - sr, cy - sr, cx + sr, cy + sr), fill=mix(pc, WHITE, .55))
    _put(img, p["img"], cx + p.get("dx", 0), cy + p.get("dy", 0), p.get("maxw", c_ - a - 70), p.get("maxh", e - b - 50), p.get("ang", 0))
    d = ImageDraw.Draw(img)
    if p.get("ptag"):
        pf = f("Poppins-Bold.ttf", 19); pw = d.textlength(p["ptag"], font=pf) / S + 32
        d.rounded_rectangle(P(a + 18, b + 18, a + 18 + pw, b + 58), radius=20 * S, fill=ink)
        d.text(P(a + 18 + pw / 2, b + 38), p["ptag"], font=pf, fill=WHITE, anchor="mm")
    # stub
    sx0, sx1 = x0 + perf + 12, x1 - 22; scx = (sx0 + sx1) / 2; sw = sx1 - sx0
    d.text(P(scx, y0 + 70), p.get("stub_top", "TODAY'S PICK"), font=fit(d, p.get("stub_top", "TODAY'S PICK"), "Poppins-Bold.ttf", 22, sw - 30), fill=mix(tf_, ink, .6), anchor="mm")
    nm = p.get("stub_name", "")
    if nm:
        nf, nl = wrap(d, nm, "Poppins-Bold.ttf", 30, sw - 30, 2); ny = y0 + 120
        for l in nl: d.text(P(scx, ny), l, font=nf, fill=ink, anchor="mm"); ny += nf.size / S * 1.15
    py = (y0 + y1) / 2 + 10
    d.rounded_rectangle(P(sx0 + 14, py - 70, sx1 - 14, py + (80 if p.get("regular") else 60)), radius=22 * S, fill=p.get("pricebox", ink))
    pb = p.get("pricebox", ink)
    d.text(P(scx, py - 40), p.get("plabel", "ONLY"), font=f("Poppins-Bold.ttf", 20), fill=acc if _lum(pb) < 140 else ink, anchor="mm")
    pt = tk(p["price"]); d.text(P(scx, py + 6), pt, font=fit(d, pt, "Poppins-Bold.ttf", 52, sw - 60), fill=_on(pb), anchor="mm")
    if p.get("regular") and p["regular"] > p["price"]:
        rt = "Regular " + tk(p["regular"]); rfo = fit(d, rt, "Poppins-Medium.ttf", 20, sw - 70); rw = d.textlength(rt, font=rfo) / S
        strike(d, scx - rw / 2, py + 44, rt, rfo, _on(pb))
    # barcode
    bx = sx0 + 34; by0, by1 = y1 - 120, y1 - 46; k = 0
    while bx < sx1 - 34:
        bw = (3, 6, 2, 4, 8, 3)[k % 6]; d.rectangle(P(bx, by0, bx + bw, by1), fill=ink); bx += bw + (5, 3, 6, 4)[k % 4]; k += 1
    _card(d, p, bg, ink, acc, CY)
    return rf.finish(img, p["out"])


TEMPLATES23 = {"AU": template_au, "AV": template_av}
