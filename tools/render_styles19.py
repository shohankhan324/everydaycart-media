"""Style set 19 (added 24 Nov 2026):
AM gift ribbon poster (solid colour with a flat polka dot pattern, a vertical and a horizontal satin ribbon crossing near
the top right with a flat bow, the category written along the horizontal ribbon, product on a big white disc with a thin
ring, a tilted gift tag hanging from the bow on a string holding the price, spec and regular price, cream info panel with
Bangla line, title and tick rows; collection mode puts each product on its own disc with a name and price pill),
AN Memphis window poster (pastel background scattered with flat Memphis shapes: squiggles, zigzags, outlined triangles,
dot grids and half circles; headline with a solid highlight block; a big rounded window with a thick ink outline and a
solid offset shadow holding the product on a colour circle, a spec sticker over the window corner, a two tone capsule
price pill over the bottom edge, outlined feature boxes with offset shadows; collection mode lines products up in the
window with outlined name pills).
Flat only (no gradients, no blur, no 3D), Poppins + Hind Siliguri, small logo chip in a corner."""
import math
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


def _ticks(d, feats, y0, y1, acc, ink, x0=44, x1=None, chip=WHITE):
    """2 column tick rows."""
    x1 = x1 or W0 - 44; feats = feats[:4]; gap = 14; cw = (x1 - x0 - gap) / 2
    rows = (len(feats) + 1) // 2; rh = min(80, (y1 - y0 - gap * (rows - 1)) / max(1, rows))
    for i, fe in enumerate(feats):
        x = x0 + (i % 2) * (cw + gap); y = y0 + (i // 2) * (rh + gap)
        d.rounded_rectangle(P(x, y, x + cw, y + rh), radius=16 * S, fill=chip)
        r = rh / 2 - 12; cx = x + rh / 2 + 2; cy = y + rh / 2
        d.ellipse(P(cx - r, cy - r, cx + r, cy + r), fill=acc)
        d.line(P(cx - r * .45, cy + r * .02, cx - r * .1, cy + r * .38, cx + r * .5, cy - r * .35), fill=_on(acc), width=int(3.4 * S), joint="curve")
        d.text(P(x + rh + 8, cy), fe, font=fit(d, fe, "Poppins-Medium.ttf", 26, cw - rh - 24), fill=ink, anchor="lm")


# ---------------- Template AM: gift ribbon poster ----------------
def _bow(img, cx, cy, rib, dark, s=1.0):
    pad = 200; L = Image.new("RGBA", P(2 * pad, 2 * pad), (0, 0, 0, 0)); d = ImageDraw.Draw(L)
    c = pad
    # tails
    d.polygon([P(c - 14 * s, c + 10 * s), P(c - 92 * s, c + 128 * s), P(c - 62 * s, c + 132 * s), P(c - 52 * s, c + 108 * s), P(c + 6 * s, c + 16 * s)], fill=dark)
    d.polygon([P(c + 14 * s, c + 10 * s), P(c + 92 * s, c + 128 * s), P(c + 62 * s, c + 132 * s), P(c + 52 * s, c + 108 * s), P(c - 6 * s, c + 16 * s)], fill=dark)
    # loops: drawn as rotated ellipses on sub-layers
    for sgn in (-1, 1):
        lp = Image.new("RGBA", P(240 * s, 140 * s), (0, 0, 0, 0)); ld = ImageDraw.Draw(lp)
        ld.ellipse(P(8 * s, 12 * s, 232 * s, 128 * s), fill=rib, outline=dark, width=int(5 * s * S))
        ld.ellipse(P(64 * s, 46 * s, 196 * s, 96 * s), fill=dark)
        ld.ellipse(P(92 * s, 56 * s, 196 * s, 88 * s), fill=mix(dark, (0, 0, 0), 0.18))
        if sgn < 0: lp = lp.transpose(Image.FLIP_LEFT_RIGHT)
        lp = lp.rotate(-sgn * 22, expand=True, resample=Image.BICUBIC)
        L.alpha_composite(lp, (int((c + sgn * 92 * s) * S - lp.width / 2), int((c - 34 * s) * S - lp.height / 2)))
    d = ImageDraw.Draw(L)
    d.rounded_rectangle(P(c - 36 * s, c - 36 * s, c + 36 * s, c + 32 * s), radius=int(20 * s * S), fill=rib, outline=dark, width=int(5 * s * S))
    d.line(P(c - 14 * s, c - 26 * s, c - 14 * s, c + 22 * s), fill=dark, width=int(3 * s * S))
    d.line(P(c + 14 * s, c - 26 * s, c + 14 * s, c + 22 * s), fill=dark, width=int(3 * s * S))
    _paste_c(img, L, cx, cy)


def _gift_tag(img, cx, cy, ang, fill, ink, acc, price, regular=None, label="ONLY", spec=None, sub=None, w=250, h=350, line=None):
    pad = 30; L = Image.new("RGBA", P(w + 2 * pad, h + 2 * pad), (0, 0, 0, 0)); d = ImageDraw.Draw(L)
    x0, y0, x1, y1 = pad, pad, pad + w, pad + h; ch = 58
    d.polygon([P(x0 + ch, y0), P(x1 - ch, y0), P(x1, y0 + ch), P(x1, y1), P(x0, y1), P(x0, y0 + ch)], fill=ink)
    b = 7
    d.polygon([P(x0 + ch + 3, y0 + b), P(x1 - ch - 3, y0 + b), P(x1 - b, y0 + ch + 3), P(x1 - b, y1 - b), P(x0 + b, y1 - b), P(x0 + b, y0 + ch + 3)], fill=fill)
    hx, hy = (x0 + x1) / 2, y0 + 40
    d.ellipse(P(hx - 16, hy - 16, hx + 16, hy + 16), fill=ink); d.ellipse(P(hx - 9, hy - 9, hx + 9, hy + 9), fill=(0, 0, 0, 0))
    mx = (x0 + x1) / 2
    d.text(P(mx, y0 + 92), label, font=f("Poppins-Bold.ttf", 22), fill=acc if _lum(fill) > 150 else WHITE, anchor="mm")
    pt = tk(price); d.text(P(mx, y0 + 146), pt, font=fit(d, pt, "Poppins-Bold.ttf", 56, w - 40), fill=ink, anchor="mm")
    yy = y0 + 196
    if regular and regular > price:
        rt = "Regular " + tk(regular); rfo = f("Poppins-Medium.ttf", 20); rw = d.textlength(rt, font=rfo) / S
        strike(d, mx - rw / 2, yy - 12, rt, rfo, mix(ink, fill, 0.35)); yy += 34
    if sub:
        d.text(P(mx, yy), sub, font=f("Poppins-Bold.ttf", 22), fill=ink, anchor="mm"); yy += 34
    if spec:
        for k in range(int(x0 + 26), int(x1 - 26), 18): d.line(P(k, yy, k + 9, yy), fill=mix(ink, fill, 0.5), width=2 * S)
        big_, lab = spec
        d.text(P(mx, yy + 42), big_, font=fit(d, big_, "Poppins-Bold.ttf", 44, w - 40), fill=acc if _lum(fill) > 150 else WHITE, anchor="mm")
        d.text(P(mx, yy + 82), lab, font=fit(d, lab, "Poppins-Bold.ttf", 18, w - 36), fill=ink, anchor="mm")
    L = L.rotate(ang, expand=True, resample=Image.BICUBIC)
    # hole position after rotation (around layer centre)
    lw0, lh0 = (w + 2 * pad), (h + 2 * pad); ox, oy = hx - lw0 / 2, hy - lh0 / 2; a = math.radians(-ang)
    rx, ry = ox * math.cos(a) - oy * math.sin(a), ox * math.sin(a) + oy * math.cos(a)
    if line:
        d0 = ImageDraw.Draw(img); sx, sy, col = line
        d0.line(P(sx, sy, cx + rx, cy + ry), fill=col, width=4 * S)
    _paste_c(img, L, cx, cy)


def template_am(p):
    bg = p.get("bg", (196, 40, 60)); dot = p.get("dot", mix(bg, WHITE, 0.16)); rib = p.get("rib", (255, 214, 102))
    dark = p.get("rib_dark", mix(rib, (0, 0, 0), 0.22)); ink = p.get("ink", (24, 22, 30)); paper = p.get("paper", (252, 247, 238))
    acc = p.get("acc", bg); tagc = p.get("tagc", WHITE); PY = p.get("panel_y", 905)
    img = Image.new("RGBA", (W, H), bg + (255,)); d = ImageDraw.Draw(img)
    for j, y in enumerate(range(24, PY, 64)):   # flat polka dots
        for x in range(24 + (32 if j % 2 else 0), W0, 64):
            d.ellipse(P(x - 7, y - 7, x + 7, y + 7), fill=dot)
    RX = p.get("rib_x", W0 - 176); RY = p.get("rib_y", 318); rw = 66
    d.rectangle(P(RX - rw / 2, 0, RX + rw / 2, PY), fill=rib)
    d.rectangle(P(0, RY - rw / 2, W0, RY + rw / 2), fill=rib)
    for e in (-rw / 2 + 8, rw / 2 - 10):
        d.line(P(RX + e, 0, RX + e, PY), fill=dark, width=2 * S); d.line(P(0, RY + e, W0, RY + e), fill=dark, width=2 * S)
    # ribbon text
    tf = f("Poppins-Bold.ttf", 24); txt = p["tag"]; x = 44; tw_ = d.textlength(txt, font=tf) / S; lim = RX - 150
    while x + tw_ <= lim:
        d.text(P(x, RY), txt, font=tf, fill=_on(rib), anchor="lm"); x += tw_ + 26
        if x + tw_ <= lim: d.ellipse(P(x - 15, RY - 5, x - 5, RY + 5), fill=_on(rib)); x += 6
    logo_chip(img, 44, 30, 110, fill=WHITE); d = ImageDraw.Draw(img)
    h1, h2 = p["head"]; hf = f("Poppins-Bold.ttf", p.get("hsize", 74))
    for l in (h1, h2): hf = fit(d, l, "Poppins-Bold.ttf", hf.size / S, RX - 130)
    lh = hf.size / S * 1.04
    d.text(P(44, 112), h1, font=hf, fill=_on(bg)); d.text(P(44, 112 + lh), h2, font=hf, fill=rib)
    items = p.get("items")
    if items:
        for it in items:
            r = it.get("r", 175); cx, cy = it["cx"], it["cy"]
            d.ellipse(P(cx - r, cy - r, cx + r, cy + r), fill=WHITE)
            d.ellipse(P(cx - r - 12, cy - r - 12, cx + r + 12, cy + r + 12), outline=WHITE, width=3 * S)
            _put(img, it["img"], cx + it.get("dx", 0), cy + it.get("dy", 0), it.get("mw", r * 1.5), it.get("mh", r * 1.6), it.get("ang", 0)); d = ImageDraw.Draw(img)
            nm = it["name"]; nf = fit(d, nm, "Poppins-Bold.ttf", 23, 2 * r + 30); pt = tk(it["price"]); pf = f("Poppins-Bold.ttf", 28)
            nw = d.textlength(nm, font=nf) / S; pw = d.textlength(pt, font=pf) / S
            ny = cy + r - 6; tw = max(nw, pw) + 50
            d.rounded_rectangle(P(cx - tw / 2, ny, cx + tw / 2, ny + 92), radius=22 * S, fill=ink)
            d.text(P(cx, ny + 26), nm, font=nf, fill=WHITE, anchor="mm")
            d.rounded_rectangle(P(cx - pw / 2 - 20, ny + 46, cx + pw / 2 + 20, ny + 84), radius=19 * S, fill=rib)
            d.text(P(cx, ny + 65), pt, font=pf, fill=_on(rib), anchor="mm")
    else:
        r = p.get("r", 255); cx, cy = p.get("dcx", 410), p.get("dcy", 640)
        d.ellipse(P(cx - r - 14, cy - r - 14, cx + r + 14, cy + r + 14), outline=WHITE, width=3 * S)
        d.ellipse(P(cx - r, cy - r, cx + r, cy + r), fill=WHITE)
        _put(img, p["img"], cx + p.get("dx", 0), cy + p.get("dy", 0), p.get("maxw", 400), p.get("maxh", 420), p.get("ang", 0)); d = ImageDraw.Draw(img)
    tcx, tcy = p.get("tag_cx", RX + 6), p.get("tag_cy", 640)
    _gift_tag(img, tcx, tcy, p.get("tag_ang", -7), tagc, ink, acc, p["price"], p.get("regular"), p.get("plabel", "ONLY"),
              p.get("spec"), p.get("sub"), line=(RX, RY + 40, ink))
    _bow(img, RX, RY, rib, dark, s=p.get("bow_s", 0.95)); d = ImageDraw.Draw(img)
    # info panel
    d.rectangle(P(0, PY, W0, H0), fill=paper)
    by = PY + 52
    d.rounded_rectangle(P(44, by - 24, 56, by + 24), radius=6 * S, fill=bg)
    _bnq(d, 74, by, p["bn"], 34, W0 - 130, ink)
    ftt, tl = wrap(d, p["title"], "Poppins-Bold.ttf", 32, W0 - 90, 1)
    d.text(P(44, by + 40), tl[0], font=ftt, fill=bg if _lum(bg) < 150 else ink)
    _ticks(d, p.get("feats", []), by + 98, H0 - 92, bg, ink, chip=mix(paper, bg, 0.08))
    d.rectangle(P(0, H0 - 64, W0, H0), fill=bg)
    d.text(P(W0 / 2, H0 - 32), FOOT, font=f("Poppins-Bold.ttf", 23), fill=_on(bg), anchor="mm")
    return rf.finish(img, p["out"])


# ---------------- Template AN: Memphis window poster ----------------
def _squiggle(d, x, y, w, amp, col, width=7, n=3, vert=False):
    pts = []
    for k in range(0, 61):
        t = k / 60; a = math.sin(t * n * 2 * math.pi) * amp
        pts.append(P(x + a, y + t * w) if vert else P(x + t * w, y + a))
    d.line(pts, fill=col, width=int(width * S), joint="curve")


def _zigzag(d, x, y, w, h, col, n=5, width=7):
    pts = [P(x + i * w / n, y + (0 if i % 2 == 0 else h)) for i in range(n + 1)]
    d.line(pts, fill=col, width=int(width * S), joint="curve")


def _tri(d, cx, cy, r, ang, col, width=6):
    pts = [P(cx + r * math.cos(math.radians(ang + k * 120)), cy + r * math.sin(math.radians(ang + k * 120))) for k in range(3)]
    d.polygon(pts, outline=col, width=int(width * S))


def _dots(d, x, y, nx, ny, col, step=24, r=5):
    for i in range(nx):
        for j in range(ny): d.ellipse(P(x + i * step - r, y + j * step - r, x + i * step + r, y + j * step + r), fill=col)


def template_an(p):
    bg = p.get("bg", (255, 236, 214)); ink = p.get("ink", (24, 22, 34)); win = p.get("win", (120, 200, 230))
    acc = p.get("acc", (255, 92, 120)); c2 = p.get("c2", (255, 206, 60)); c3 = p.get("c3", (90, 70, 200)); circ = p.get("circ", c2)
    img = Image.new("RGBA", (W, H), bg + (255,)); d = ImageDraw.Draw(img)
    # Memphis confetti around the edges
    _squiggle(d, 640, 52, 190, 12, c3, n=3)
    _zigzag(d, W0 - 150, 210, 110, 26, acc)
    _tri(d, W0 - 250, 270, 24, 20, ink)
    _dots(d, 20, 330, 3, 4, c3)
    d.pieslice(P(W0 - 60, 560, W0 + 60, 680), 90, 270, fill=c2)
    _squiggle(d, 30, 700, 150, 14, acc, n=2, vert=True)
    d.ellipse(P(W0 - 70, 360, W0 - 30, 400), fill=acc)
    logo_chip(img, 44, 30, 110, fill=WHITE); d = ImageDraw.Draw(img)
    tf = f("Poppins-Bold.ttf", 21); tw = d.textlength(p["tag"], font=tf) / S
    d.rounded_rectangle(P(W0 - 44 - tw - 40 + 5, 38 + 5, W0 - 44 + 5, 84 + 5), radius=23 * S, fill=ink)
    d.rounded_rectangle(P(W0 - 44 - tw - 40, 38, W0 - 44, 84), radius=23 * S, fill=c2, outline=ink, width=3 * S)
    d.text(P(W0 - 64 - tw, 61), p["tag"], font=tf, fill=ink, anchor="lm")
    # headline: line 1 plain, line 2 on a highlight block
    h1, h2 = p["head"]; hf = f("Poppins-Bold.ttf", p.get("hsize", 70))
    for l in (h1, h2): hf = fit(d, l, "Poppins-Bold.ttf", hf.size / S, W0 - 150)
    lh = hf.size / S * 1.1
    d.text(P(56, 112), h1, font=hf, fill=ink)
    w2 = d.textlength(h2, font=hf) / S; y2 = 112 + lh
    d.rectangle(P(42, y2 + 8, 70 + w2, y2 + lh + 2), fill=acc)
    d.text(P(56, y2), h2, font=hf, fill=_on(acc))
    # window
    x0, y0, x1, y1 = 70, p.get("win_y0", 330), W0 - 70, p.get("win_y1", 860)
    d.rounded_rectangle(P(x0 + 16, y0 + 16, x1 + 16, y1 + 16), radius=44 * S, fill=ink)
    d.rounded_rectangle(P(x0, y0, x1, y1), radius=44 * S, fill=win, outline=ink, width=6 * S)
    _dots(d, x1 - 150, y0 + 40, 5, 3, mix(win, WHITE, 0.45), step=26, r=5)
    _squiggle(d, x0 + 40, y1 - 60, 140, 10, mix(win, WHITE, 0.5), n=2, width=6)
    items = p.get("items"); mx = (x0 + x1) / 2; my = (y0 + y1) / 2
    if items:
        n = len(items); xs = p.get("xs", [x0 + (x1 - x0) * (k + .5) / n for k in range(n)])
        for k, it in enumerate(items):
            cx = xs[k]; cy = it.get("cy", my - 20); r = it.get("r", 165)
            d.ellipse(P(cx - r, cy - r, cx + r, cy + r), fill=it.get("circ", [circ, mix(acc, WHITE, 0.35), c2][k % 3]))
            _put(img, it["img"], cx + it.get("dx", 0), cy + it.get("dy", 0), it.get("mw", r * 1.5), it.get("mh", r * 1.9), it.get("ang", 0)); d = ImageDraw.Draw(img)
            nm = it["name"]; nf = fit(d, nm, "Poppins-Bold.ttf", 23, (x1 - x0) / n - 40); nw = d.textlength(nm, font=nf) / S + 36
            ny = y1 - 78
            d.rounded_rectangle(P(cx - nw / 2 + 5, ny - 24 + 5, cx + nw / 2 + 5, ny + 24 + 5), radius=24 * S, fill=ink)
            d.rounded_rectangle(P(cx - nw / 2, ny - 24, cx + nw / 2, ny + 24), radius=24 * S, fill=WHITE, outline=ink, width=3 * S)
            d.text(P(cx, ny), nm, font=nf, fill=ink, anchor="mm")
    else:
        r = p.get("r", 220); cx, cy = p.get("dcx", mx + 60), p.get("dcy", my)
        d.ellipse(P(cx - r, cy - r, cx + r, cy + r), fill=circ)
        _put(img, p["img"], cx + p.get("dx", 0), cy + p.get("dy", 0), p.get("maxw", 440), p.get("maxh", 440), p.get("ang", 0)); d = ImageDraw.Draw(img)
    if p.get("spec"):   # round sticker over the top-left window corner
        big_, lab = p["spec"]; sx, sy, sr = p.get("sx", x0 + 70), p.get("sy", y0 + 70), 92
        d.ellipse(P(sx - sr + 6, sy - sr + 6, sx + sr + 6, sy + sr + 6), fill=ink)
        d.ellipse(P(sx - sr, sy - sr, sx + sr, sy + sr), fill=c3, outline=ink, width=4 * S)
        d.text(P(sx, sy - 12), big_, font=fit(d, big_, "Poppins-Bold.ttf", 46, 2 * sr - 30), fill=WHITE, anchor="mm")
        d.text(P(sx, sy + 34), lab, font=fit(d, lab, "Poppins-Bold.ttf", 17, 2 * sr - 36), fill=c2, anchor="mm")
    # capsule price pill over the bottom edge (two tone)
    lab = p.get("plabel", "ONLY"); pt = tk(p["price"])
    lf = f("Poppins-Bold.ttf", 24); pf = f("Poppins-Bold.ttf", 50)
    lw = d.textlength(lab, font=lf) / S + 50; pw = d.textlength(pt, font=pf) / S + 56; ch_ = 88
    cw = lw + pw; pad = 30
    L = Image.new("RGBA", P(cw + 2 * pad + 12, ch_ + 2 * pad + 12), (0, 0, 0, 0)); ld = ImageDraw.Draw(L)
    ld.rounded_rectangle(P(pad + 10, pad + 10, pad + cw + 10, pad + ch_ + 10), radius=ch_ / 2 * S, fill=ink)
    ld.rounded_rectangle(P(pad, pad, pad + cw, pad + ch_), radius=ch_ / 2 * S, fill=acc, outline=ink, width=4 * S)
    ld.rounded_rectangle(P(pad, pad, pad + lw + ch_ / 2, pad + ch_), radius=ch_ / 2 * S, fill=c2, outline=ink, width=4 * S)
    ld.rectangle(P(pad + lw, pad + 4, pad + lw + ch_ / 2 + 2, pad + ch_ - 4), fill=acc)
    ld.line(P(pad + lw, pad + 2, pad + lw, pad + ch_ - 2), fill=ink, width=4 * S)
    ld.text(P(pad + lw / 2 + 4, pad + ch_ / 2), lab, font=lf, fill=ink, anchor="mm")
    ld.text(P(pad + lw + pw / 2, pad + ch_ / 2 + 2), pt, font=pf, fill=_on(acc), anchor="mm")
    L = L.rotate(p.get("cap_ang", 4), expand=True, resample=Image.BICUBIC)
    pcx, pcy = p.get("pcx", x1 - cw / 2 - 10), p.get("pcy", y1 + 4)
    _paste_c(img, L, pcx, pcy); d = ImageDraw.Draw(img)
    if p.get("regular") and p["regular"] > p["price"]:
        rt = "Regular " + tk(p["regular"]); rfo = f("Poppins-Medium.ttf", 22); rw_ = d.textlength(rt, font=rfo) / S
        strike(d, pcx - rw_ / 2 + 10, pcy + 68, rt, rfo, mix(ink, bg, 0.3))
    if p.get("sub"):
        d.text(P(x0 + 10, y1 + 48), p["sub"], font=f("Poppins-Bold.ttf", 26), fill=ink, anchor="lm")
    by = p.get("bn_y", y1 + 132)
    _bnq(d, 56, by, p["bn"], 34, W0 - 120, ink)
    ftt, tl = wrap(d, p["title"], "Poppins-Bold.ttf", 31, W0 - 112, 1)
    d.text(P(56, by + 36), tl[0], font=ftt, fill=c3 if _lum(c3) < 150 else ink)
    # outlined feature boxes with offset shadow
    feats = p.get("feats", [])[:4]; fy0 = by + 96; fy1 = H0 - 76; gap = 18; bw = (W0 - 112 - gap) / 2
    rows = (len(feats) + 1) // 2; rh = min(62, (fy1 - fy0 - gap * (rows - 1)) / max(1, rows))
    cols_ = [acc, c2, mix(c3, WHITE, 0.55), circ]
    for i, fe in enumerate(feats):
        x = 56 + (i % 2) * (bw + gap); y = fy0 + (i // 2) * (rh + gap)
        d.rounded_rectangle(P(x + 6, y + 6, x + bw + 6, y + rh + 6), radius=14 * S, fill=ink)
        d.rounded_rectangle(P(x, y, x + bw, y + rh), radius=14 * S, fill=WHITE, outline=ink, width=3 * S)
        d.rounded_rectangle(P(x + 10, y + 10, x + rh - 10, y + rh - 10), radius=10 * S, fill=cols_[i % 4], outline=ink, width=2 * S)
        d.text(P(x + rh / 2, y + rh / 2), str(i + 1), font=f("Poppins-Bold.ttf", 22), fill=ink, anchor="mm")
        d.text(P(x + rh + 8, y + rh / 2), fe, font=fit(d, fe, "Poppins-Medium.ttf", 24, bw - rh - 22), fill=ink, anchor="lm")
    d.text(P(W0 / 2, H0 - 34), FOOT, font=f("Poppins-Bold.ttf", 23), fill=ink, anchor="mm")
    return rf.finish(img, p["out"])


TEMPLATES19 = {"AM": template_am, "AN": template_an}
