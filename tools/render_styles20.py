"""Style set 20 (added 25 Nov 2026):
AO shopping bag poster (solid colour with faint diagonal pinstripes, a big flat paper shopping bag in the middle with
rope handles, a folded top band and a darker side gusset; the product sits on a circle printed on the bag front, a
scalloped price seal over the bag's bottom right corner, a tilted spec tag on the top left, headline above; collection
mode lines products up on the bag front with ink name pills; cream info panel with Bangla line, title and tick rows),
AP flat landscape scene (sky colour with a big sun or moon that carries the spec, flat clouds, two layers of rolling
hills, the product standing on the front hill with a flat ground shadow, a wooden-style signpost on the hill holding the
price; the front hill colour runs to the bottom and holds the Bangla line, title and white feature chips; collection
mode stands products side by side on the hill with name pills).
Flat only (no gradients, no blur, no 3D), Poppins + Hind Siliguri, small logo chip in a corner."""
import math
from PIL import Image, ImageDraw
import render_flat as rf
from render_flat import P, f, fit, wrap, tk, S, W, H, W0, H0
from render_styles4 import logo_chip, mix, strike
from render_styles8 import _scaled
from render_styles16 import _bnq, _paste_c
from render_styles19 import _lum, _on, _ticks

WHITE = (255, 255, 255)
FOOT = "everydaycart.online  |  Inbox us to order"


def _put(img, prod, cx, cy, maxw, maxh, ang=0):
    pr = _scaled(prod, maxw, maxh)
    if ang: pr = pr.rotate(ang, expand=True, resample=Image.BICUBIC)
    img.alpha_composite(pr, (int(cx * S - pr.width / 2), int(cy * S - pr.height / 2)))
    return pr.width / S, pr.height / S


def _stand(img, prod, cx, base, maxw, maxh):
    """Paste with the product's bottom edge on y=base. Returns (w, h)."""
    pr = _scaled(prod, maxw, maxh)
    img.alpha_composite(pr, (int(cx * S - pr.width / 2), int(base * S - pr.height)))
    return pr.width / S, pr.height / S


def _tagpill(d, text, x1, y, fill, ink, size=21):
    tf = f("Poppins-Bold.ttf", size); tw = d.textlength(text, font=tf) / S
    d.rounded_rectangle(P(x1 - tw - 40, y, x1, y + 46), radius=23 * S, fill=fill)
    d.text(P(x1 - 20 - tw, y + 23), text, font=tf, fill=ink, anchor="lm")


def _seal(img, cx, cy, r, ang, fill, ink, acc, price, regular=None, label="ONLY"):
    pad = 20; sz = 2 * r + 2 * pad; L = Image.new("RGBA", P(sz, sz), (0, 0, 0, 0)); d = ImageDraw.Draw(L)
    c = sz / 2; n = 22
    pts = [P(c + (r if k % 2 == 0 else r * .9) * math.cos(math.pi * k / n), c + (r if k % 2 == 0 else r * .9) * math.sin(math.pi * k / n)) for k in range(2 * n)]
    d.polygon(pts, fill=fill)
    d.ellipse(P(c - r * .8, c - r * .8, c + r * .8, c + r * .8), outline=_on(fill) if _lum(fill) < 160 else ink, width=2 * S)
    tc = _on(fill)
    d.text(P(c, c - r * .42), label, font=f("Poppins-Bold.ttf", r * .2), fill=tc, anchor="mm")
    pt = tk(price); d.text(P(c, c - r * .05), pt, font=fit(d, pt, "Poppins-Bold.ttf", r * .42, r * 1.45), fill=tc, anchor="mm")
    if regular and regular > price:
        rt = "Regular " + tk(regular); rfo = fit(d, rt, "Poppins-Medium.ttf", r * .15, r * 1.2); rw = d.textlength(rt, font=rfo) / S
        strike(d, c - rw / 2, c + r * .27, rt, rfo, tc)
    L = L.rotate(ang, expand=True, resample=Image.BICUBIC); _paste_c(img, L, cx, cy)


# ---------------- Template AO: shopping bag poster ----------------
def template_ao(p):
    bg = p.get("bg", (40, 70, 190)); bag = p.get("bag", (252, 248, 240)); acc = p.get("acc", (255, 128, 54))
    ink = p.get("ink", (22, 22, 32)); paper = p.get("paper", (252, 247, 238)); circ = p.get("circ", mix(acc, WHITE, 0.72))
    gus = mix(bag, (0, 0, 0), 0.12); band = p.get("band", acc); PY = p.get("panel_y", 1000)
    img = Image.new("RGBA", (W, H), bg + (255,)); d = ImageDraw.Draw(img)
    st = mix(bg, WHITE, 0.07)
    for k in range(-H0, W0, 38):   # faint diagonal pinstripes
        d.line(P(k, 0, k + PY, PY), fill=st, width=3 * S)
    logo_chip(img, 44, 30, 110, fill=WHITE); d = ImageDraw.Draw(img)
    _tagpill(d, p["tag"], W0 - 44, 38, acc, _on(acc))
    h1, h2 = p["head"]; hf = f("Poppins-Bold.ttf", p.get("hsize", 72))
    for l in (h1, h2): hf = fit(d, l, "Poppins-Bold.ttf", hf.size / S, W0 - 100)
    lh = hf.size / S * 1.06
    d.text(P(W0 / 2, 116), h1, font=hf, fill=_on(bg), anchor="mt"); d.text(P(W0 / 2, 116 + lh), h2, font=hf, fill=p.get("h2c", acc), anchor="mt")
    # bag geometry
    bx0, bx1, by0, by1 = 180, W0 - 180, p.get("bag_y0", 400), PY - 34; inset = 22
    hc = (bx0 + bx1) / 2
    # rope handles behind the body
    for hx in (hc - 140, hc + 140):
        d.arc(P(hx - 80, by0 - 120, hx + 80, by0 + 182), 180, 360, fill=ink, width=12 * S)
    # body (slight trapezoid: wider at the bottom)
    d.polygon([P(bx0 + inset, by0), P(bx1 - inset, by0), P(bx1, by1), P(bx0, by1)], fill=bag)
    # side gusset on the right
    d.polygon([P(bx1 - inset - 70, by0), P(bx1 - inset, by0), P(bx1, by1), P(bx1 - 52, by1)], fill=gus)
    d.line(P(bx1 - inset - 70, by0, bx1 - 52, by1), fill=mix(gus, (0, 0, 0), 0.1), width=2 * S)
    # top band
    d.polygon([P(bx0 + inset, by0), P(bx1 - inset, by0), P(bx1 - inset + 3, by0 + 56), P(bx0 + inset - 3, by0 + 56)], fill=band)
    for hx in (hc - 140, hc + 140):   # rope holes and knots
        d.ellipse(P(hx - 13 - 80, by0 + 18, hx + 13 - 80, by0 + 44), fill=ink)
        d.ellipse(P(hx - 13 + 80, by0 + 18, hx + 13 + 80, by0 + 44), fill=ink)
    fx0, fx1 = bx0 + 10, bx1 - 70   # printable front
    fcx = (fx0 + fx1) / 2; fcy = (by0 + 56 + by1) / 2 + 4
    items = p.get("items")
    if items:
        n = len(items); xs = p.get("xs", [fx0 + (fx1 - fx0) * (k + .5) / n for k in range(n)])
        for k, it in enumerate(items):
            cx = xs[k]; cy = it.get("cy", fcy - 30); r = it.get("r", 150)
            d.ellipse(P(cx - r, cy - r, cx + r, cy + r), fill=it.get("circ", [circ, mix(bg, WHITE, 0.75)][k % 2]))
            _put(img, it["img"], cx + it.get("dx", 0), cy + it.get("dy", 0), it.get("mw", r * 1.5), it.get("mh", r * 1.9), it.get("ang", 0)); d = ImageDraw.Draw(img)
            nm = it["name"]; nf = fit(d, nm, "Poppins-Bold.ttf", 22, (fx1 - fx0) / n - 24)
            pt = tk(it["price"]); pf = f("Poppins-Bold.ttf", 26)
            nw = max(d.textlength(nm, font=nf), d.textlength(pt, font=pf)) / S + 36; ny = cy + r + 6
            d.rounded_rectangle(P(cx - nw / 2, ny, cx + nw / 2, ny + 84), radius=20 * S, fill=ink)
            d.text(P(cx, ny + 24), nm, font=nf, fill=WHITE, anchor="mm")
            d.text(P(cx, ny + 60), pt, font=pf, fill=mix(acc, WHITE, 0.25) if _lum(acc) < 200 else acc, anchor="mm")
    else:
        r = p.get("r", 215)
        d.ellipse(P(fcx - r, fcy - r, fcx + r, fcy + r), fill=circ)
        _put(img, p["img"], fcx + p.get("dx", 0), fcy + p.get("dy", 0), p.get("maxw", 380), p.get("maxh", 420), p.get("ang", 0)); d = ImageDraw.Draw(img)
    if p.get("spec"):   # tilted spec tag on the bag's top left
        big_, lab = p["spec"]; tw_, th_ = 190, 112; pad = 20
        L = Image.new("RGBA", P(tw_ + 2 * pad, th_ + 2 * pad), (0, 0, 0, 0)); ld = ImageDraw.Draw(L)
        ld.rounded_rectangle(P(pad, pad, pad + tw_, pad + th_), radius=18 * S, fill=ink)
        ld.text(P(pad + tw_ / 2, pad + 44), big_, font=fit(ld, big_, "Poppins-Bold.ttf", 46, tw_ - 24), fill=acc if _lum(acc) > 90 else WHITE, anchor="mm")
        ld.text(P(pad + tw_ / 2, pad + 88), lab, font=fit(ld, lab, "Poppins-Bold.ttf", 18, tw_ - 24), fill=WHITE, anchor="mm")
        L = L.rotate(p.get("spec_ang", 8), expand=True, resample=Image.BICUBIC)
        _paste_c(img, L, p.get("spec_x", bx0 + 40), p.get("spec_y", by0 + 150))
    if p.get("seal", True):
        _seal(img, p.get("seal_x", bx1 - 20), p.get("seal_y", by1 - 100), p.get("seal_r", 118), p.get("seal_ang", -10),
              p.get("sealc", acc), ink, acc, p["price"], p.get("regular"), p.get("plabel", "ONLY"))
    d = ImageDraw.Draw(img)
    # info panel
    d.rectangle(P(0, PY, W0, H0), fill=paper)
    by = PY + 46
    d.rounded_rectangle(P(44, by - 22, 56, by + 22), radius=6 * S, fill=acc)
    _bnq(d, 74, by, p["bn"], 33, W0 - 130, ink)
    ftt, tl = wrap(d, p["title"], "Poppins-Bold.ttf", 30, W0 - 90, 1)
    d.text(P(44, by + 34), tl[0], font=ftt, fill=bg if _lum(bg) < 150 else ink)
    _ticks(d, p.get("feats", []), by + 88, H0 - 84, acc, ink, chip=mix(paper, bg, 0.08))
    d.rectangle(P(0, H0 - 62, W0, H0), fill=bg)
    d.text(P(W0 / 2, H0 - 31), FOOT, font=f("Poppins-Bold.ttf", 23), fill=_on(bg), anchor="mm")
    return rf.finish(img, p["out"])


# ---------------- Template AP: flat landscape scene ----------------
def _cloud(d, x, y, s, col):
    d.rounded_rectangle(P(x, y + 30 * s, x + 200 * s, y + 70 * s), radius=int(20 * s * S), fill=col)
    d.ellipse(P(x + 30 * s, y + 4 * s, x + 100 * s, y + 70 * s), fill=col)
    d.ellipse(P(x + 80 * s, y - 16 * s, x + 170 * s, y + 70 * s), fill=col)


def _signpost(img, x, base, w, h, ang, board, ink, label, price, regular=None, post=(120, 82, 56)):
    d = ImageDraw.Draw(img)
    d.rectangle(P(x - 8, base - h / 2 - 20, x + 8, base), fill=post)
    pad = 24; L = Image.new("RGBA", P(w + 2 * pad, h + 2 * pad), (0, 0, 0, 0)); ld = ImageDraw.Draw(L)
    ld.rounded_rectangle(P(pad, pad, pad + w, pad + h), radius=18 * S, fill=board, outline=ink, width=4 * S)
    for yy in (pad + 14, pad + h - 14):
        for xx in (pad + 16, pad + w - 16): ld.ellipse(P(xx - 4, yy - 4, xx + 4, yy + 4), fill=ink)
    c = pad + w / 2; tc = _on(board)
    hasr = regular and regular > price
    ld.text(P(c, pad + (32 if hasr else 38)), label, font=f("Poppins-Bold.ttf", 21), fill=tc, anchor="mm")
    pt = tk(price); ld.text(P(c, pad + (h / 2 + (2 if hasr else 12))), pt, font=fit(ld, pt, "Poppins-Bold.ttf", 52, w - 40), fill=tc, anchor="mm")
    if hasr:
        rt = "Regular " + tk(regular); rfo = f("Poppins-Medium.ttf", 19); rw = ld.textlength(rt, font=rfo) / S
        strike(ld, c - rw / 2, pad + h - 40, rt, rfo, mix(tc, board, 0.3))
    L = L.rotate(ang, expand=True, resample=Image.BICUBIC); _paste_c(img, L, x, base - h / 2 - 40)


def template_ap(p):
    sky = p.get("sky", (178, 222, 250)); sun = p.get("sun", (255, 206, 72)); hb = p.get("hill_b", (140, 200, 150))
    hf_ = p.get("hill_f", (92, 168, 110)); ink = p.get("ink", (24, 26, 36)); acc = p.get("acc", (240, 90, 70))
    cloud = p.get("cloud", WHITE); HT = p.get("hill_top", 860); night = p.get("night", False)
    img = Image.new("RGBA", (W, H), sky + (255,)); d = ImageDraw.Draw(img)
    if night:
        import random
        rnd = random.Random(7)
        for _ in range(60):
            x, y, r = rnd.uniform(20, W0 - 20), rnd.uniform(240, HT - 120), rnd.choice((2, 2, 3, 4))
            d.ellipse(P(x - r, y - r, x + r, y + r), fill=mix(sky, WHITE, 0.7))
    # sun or moon (carries the spec)
    sx, sy, sr = p.get("sun_x", W0 - 190), p.get("sun_y", 360), p.get("sun_r", 120)
    d.ellipse(P(sx - sr - 26, sy - sr - 26, sx + sr + 26, sy + sr + 26), fill=mix(sky, sun, 0.35))
    d.ellipse(P(sx - sr, sy - sr, sx + sr, sy + sr), fill=sun)
    if p.get("spec"):
        big_, lab = p["spec"]; tc = _on(sun)
        d.text(P(sx, sy - 14), big_, font=fit(d, big_, "Poppins-Bold.ttf", 54, 2 * sr - 40), fill=tc, anchor="mm")
        d.text(P(sx, sy + 36), lab, font=fit(d, lab, "Poppins-Bold.ttf", 18, 2 * sr - 50), fill=tc, anchor="mm")
    for (cx, cy, s) in p.get("clouds", [(70, 330, 1.0), (W0 - 420, 560, 0.8), (210, 600, 0.6)]):
        _cloud(d, cx, cy, s, cloud)
    logo_chip(img, 44, 30, 110, fill=WHITE); d = ImageDraw.Draw(img)
    _tagpill(d, p["tag"], W0 - 44, 38, acc, _on(acc))
    h1, h2 = p["head"]; hfo = f("Poppins-Bold.ttf", p.get("hsize", 72))
    for l in (h1, h2): hfo = fit(d, l, "Poppins-Bold.ttf", hfo.size / S, W0 - 110)
    lh = hfo.size / S * 1.06
    hc = p.get("head_col", ink if _lum(sky) > 150 else WHITE)
    d.text(P(48, 118), h1, font=hfo, fill=hc); d.text(P(48, 118 + lh), h2, font=hfo, fill=p.get("h2c", acc))
    # hills
    d.ellipse(P(-420, HT - 110, 640, HT + 560), fill=hb)
    d.ellipse(P(420, HT - 70, 1560, HT + 560), fill=hb)
    d.ellipse(P(-360, HT, W0 + 360, HT + 900), fill=hf_)
    d.rectangle(P(0, HT + 200, W0, H0), fill=hf_)
    # tufts of flat grass
    gc = mix(hf_, (0, 0, 0), 0.12)
    for gx, gy in p.get("tufts", [(130, HT + 70), (930, HT + 70), (300, HT + 30)]):
        for k in (-14, 0, 14): d.polygon([P(gx + k - 7, gy), P(gx + k + 7, gy), P(gx + k * 1.6, gy - 30 + abs(k))], fill=gc)
    items = p.get("items"); base = HT + p.get("base_dy", 30); sh = mix(hf_, (0, 0, 0), 0.18)
    if items:
        for it in items:
            cx = it["cx"]; b0 = base + it.get("dy", 0)
            w_, h_ = _scaled(it["img"], it.get("mw", 260), it.get("mh", 400)).size
            w_ /= S; d.ellipse(P(cx - w_ * .48, b0 - 16, cx + w_ * .48, b0 + 16), fill=sh)
            _stand(img, it["img"], cx, b0 + 6, it.get("mw", 260), it.get("mh", 400)); d = ImageDraw.Draw(img)
            nm = it["name"]; nf = fit(d, nm, "Poppins-Bold.ttf", 22, it.get("nmw", 300)); pt = tk(it["price"])
            nw = d.textlength(nm + "   " + pt, font=nf) / S + 40; ny = b0 + 44
            d.rounded_rectangle(P(cx - nw / 2, ny - 24, cx + nw / 2, ny + 24), radius=24 * S, fill=WHITE, outline=ink, width=3 * S)
            tw1 = d.textlength(nm + "   ", font=nf) / S
            d.text(P(cx - nw / 2 + 20, ny), nm, font=nf, fill=ink, anchor="lm")
            d.text(P(cx - nw / 2 + 20 + tw1, ny), pt, font=nf, fill=acc, anchor="lm")
    else:
        cx = p.get("pcx", 470)
        w_ = _scaled(p["img"], p.get("maxw", 440), p.get("maxh", 480)).size[0] / S
        d.ellipse(P(cx - w_ * .5, base - 18, cx + w_ * .5, base + 18), fill=sh)
        _stand(img, p["img"], cx, base + 8, p.get("maxw", 440), p.get("maxh", 480)); d = ImageDraw.Draw(img)
    _signpost(img, p.get("sign_x", W0 - 175), base + p.get("sign_dy", 50), p.get("sign_w", 250), p.get("sign_h", 150), p.get("sign_ang", 4),
              p.get("board", WHITE), ink, p.get("plabel", "ONLY"), p["price"], p.get("regular"))
    d = ImageDraw.Draw(img)
    # info on the front hill
    tcol = _on(hf_); by = p.get("bn_y", HT + 168)
    _bnq(d, 48, by, p["bn"], 34, W0 - 110, tcol)
    ftt, tl = wrap(d, p["title"], "Poppins-Bold.ttf", 30, W0 - 96, 1)
    d.text(P(48, by + 34), tl[0], font=ftt, fill=p.get("title_c", mix(tcol, hf_, 0.12)))
    _ticks(d, p.get("feats", []), by + 90, H0 - 78, acc, ink, x0=48, x1=W0 - 48, chip=WHITE)
    d.text(P(W0 / 2, H0 - 36), FOOT, font=f("Poppins-Bold.ttf", 23), fill=tcol, anchor="mm")
    return rf.finish(img, p["out"])


TEMPLATES20 = {"AO": template_ao, "AP": template_ap}
