"""Style set 17 (added 22 Nov 2026):
AI Swiss grid poster (warm paper background, thin ink grid rules, big left aligned headline, product on a solid colour
block that it overlaps, spec numbers stacked in the left column, a solid price block, numbered feature cells;
collection mode gives each product its own colour cell with name and price block),
AJ torn paper poster (solid colour top half with flat confetti shapes, a jagged torn paper edge with a white paper
fibre strip, product breaking over the tear, price and Bangla line on flat masking tape strips, ticked features on the
paper half; collection mode puts each product over the tear with its own name chip and price tape).
Flat only (no gradients, no blur, no 3D), Poppins + Hind Siliguri, small logo chip in a corner."""
import random
from PIL import Image, ImageDraw
import render_flat as rf
from render_flat import P, f, fit, wrap, tk, S, W, H, W0, H0
from render_styles4 import logo_chip, mix, strike
from render_styles8 import _scaled
from render_styles16 import _bnq, _paste_c

WHITE = (255, 255, 255)
FOOT = "everydaycart.online  |  Inbox us to order"


def _put(img, prod, cx, cy, maxw, maxh, ang=0):
    pr = _scaled(prod, maxw, maxh)
    if ang: pr = pr.rotate(ang, expand=True, resample=Image.BICUBIC)
    img.alpha_composite(pr, (int(cx * S - pr.width / 2), int(cy * S - pr.height / 2)))
    return pr.width / S, pr.height / S


def _lum(c): return 0.299 * c[0] + 0.587 * c[1] + 0.114 * c[2]


# ---------------- Template AI: Swiss grid poster ----------------
def template_ai(p):
    paper = p.get("paper", (246, 242, 234)); ink = p.get("ink", (20, 20, 24)); acc = p.get("acc", (236, 76, 52))
    acc2 = p.get("acc2", (40, 70, 200)); block = p.get("block", acc); rule = mix(paper, ink, 0.75)
    img = Image.new("RGBA", (W, H), paper + (255,)); d = ImageDraw.Draw(img)
    logo_chip(img, 44, 30, 110, fill=WHITE); d = ImageDraw.Draw(img)
    # tag: outlined pill top right
    tf = f("Poppins-Bold.ttf", 21); tw = d.textlength(p["tag"], font=tf) / S
    d.rounded_rectangle(P(W0 - 44 - tw - 40, 38, W0 - 44, 84), radius=23 * S, outline=ink, width=3 * S)
    d.text(P(W0 - 64 - tw, 61), p["tag"], font=tf, fill=ink, anchor="lm")
    d.line(P(44, 108, W0 - 44, 108), fill=ink, width=3 * S)
    # headline
    h1, h2 = p["head"]; hf = f("Poppins-Bold.ttf", p.get("hsize", 78))
    for l in (h1, h2): hf = fit(d, l, "Poppins-Bold.ttf", hf.size / S, W0 - 100)
    lh = hf.size / S * 1.04
    d.text(P(44, 124), h1, font=hf, fill=ink); d.text(P(44, 124 + lh), h2, font=hf, fill=acc)
    GY = 124 + 2 * lh + 26
    d.line(P(44, GY, W0 - 44, GY), fill=ink, width=2 * S)
    BY1 = p.get("block_bottom", 905)
    items = p.get("items")
    small = f("Poppins-Bold.ttf", 17)
    if items:
        n = len(items); gap = 16; cw = (W0 - 88 - gap * (n - 1)) / n
        for k, it in enumerate(items):
            x0 = 44 + k * (cw + gap); x1 = x0 + cw; y0 = GY + 22
            col = it.get("fill", [acc, acc2, block][k % 3])
            d.rectangle(P(x0, y0, x1, BY1 - 150), fill=col)
            d.text(P(x0 + 14, y0 + 12), f"{k + 1:02d}", font=f("Poppins-Bold.ttf", 34), fill=WHITE if _lum(col) < 150 else ink)
            _put(img, it["img"], (x0 + x1) / 2 + it.get("dx", 0), (y0 + BY1 - 150) / 2 + 24 + it.get("dy", 0), it.get("mw", cw - 50), it.get("mh", BY1 - 150 - y0 - 90), it.get("ang", 0))
            d = ImageDraw.Draw(img)
            nm = it["name"]; nf = fit(d, nm, "Poppins-Bold.ttf", 25, cw - 10)
            d.text(P(x0, BY1 - 128), nm, font=nf, fill=ink)
            if it.get("sub"):
                sf = fit(d, it["sub"], "Poppins-Medium.ttf", 20, cw - 10); d.text(P(x0, BY1 - 96), it["sub"], font=sf, fill=mix(ink, paper, 0.35))
            # price block
            pt = tk(it["price"]); pf = fit(d, pt, "Poppins-Bold.ttf", 40, cw - 40)
            d.rectangle(P(x0, BY1 - 62, x1, BY1), fill=ink)
            d.text(P(x0 + 16, BY1 - 31), pt, font=pf, fill=WHITE, anchor="lm")
            if it.get("regular") and it["regular"] > it["price"]:
                rt = tk(it["regular"]); rfo = f("Poppins-Medium.ttf", 19); rw = d.textlength(rt, font=rfo) / S
                if d.textlength(pt, font=pf) / S + rw + 60 < cw: strike(d, x1 - rw - 14, BY1 - 44, rt, rfo, mix(WHITE, ink, 0.4))
    else:
        LX = p.get("left_w", 330)
        bx0, by0, bx1 = LX + 30, GY + 22, W0 - 44
        d.rectangle(P(bx0, by0, bx1, BY1), fill=block)
        # big ghost number on the block
        if p.get("ghost"):
            gf = fit(d, p["ghost"], "Poppins-Bold.ttf", 260, bx1 - bx0 - 40)
            d.text(P(bx1 - 20, by0 - 20), p["ghost"], font=gf, fill=mix(block, WHITE, 0.18), anchor="ra")
        _put(img, p["img"], p.get("cx", (bx0 + bx1) / 2 - 30), p.get("cy", (by0 + BY1) / 2 + 10), p.get("maxw", 560), p.get("maxh", 520), p.get("ang", 0))
        d = ImageDraw.Draw(img)
        # left spec column
        specs = p.get("specs", [])[:3]; sy = by0
        ch = (BY1 - 175 - by0) / max(1, len(specs))
        for i, (big_, lab) in enumerate(specs):
            y = sy + i * ch
            d.text(P(44, y + 6), f"{i + 1:02d}", font=small, fill=acc)
            bf = fit(d, big_, "Poppins-Bold.ttf", min(66, ch * 0.42), LX - 10); d.text(P(44, y + 26), big_, font=bf, fill=ink)
            lf = fit(d, lab, "Poppins-Medium.ttf", 22, LX - 10); d.text(P(44, y + 30 + bf.size / S * 1.2), lab, font=lf, fill=mix(ink, paper, 0.3))
            d.line(P(44, y + ch - 6, LX, y + ch - 6), fill=rule, width=1 * S)
        # price block bottom-left
        py0 = BY1 - 160
        d.rectangle(P(44, py0, LX + 60, BY1), fill=ink)
        d.text(P(62, py0 + 26), p.get("plabel", "PRICE"), font=small, fill=acc, anchor="lm")
        pt = tk(p["price"]); pf = fit(d, pt, "Poppins-Bold.ttf", 66, LX)
        d.text(P(62, py0 + 82), pt, font=pf, fill=WHITE, anchor="lm")
        if p.get("regular") and p["regular"] > p["price"]:
            strike(d, 62, py0 + 116, "Regular " + tk(p["regular"]), f("Poppins-Medium.ttf", 21), mix(WHITE, ink, 0.4))
    # Bangla ink bar
    by = BY1 + 22
    d.rectangle(P(44, by, W0 - 44, by + 66), fill=acc)
    _bnq(d, 64, by + 33, p["bn"], 32, W0 - 130, WHITE if _lum(acc) < 170 else ink)
    # title
    ty = by + 84
    ftt, tl = wrap(d, p["title"], "Poppins-Bold.ttf", 34, W0 - 90, 1)
    d.text(P(44, ty), tl[0], font=ftt, fill=ink)
    # feature cells
    feats = p.get("feats", [])[:4]; fy0 = ty + 56; cw = (W0 - 88) / 2; rh = (H0 - 84 - fy0) / 2
    d.line(P(44, fy0, W0 - 44, fy0), fill=ink, width=2 * S)
    for i, fe in enumerate(feats):
        x = 44 + (i % 2) * cw; y = fy0 + (i // 2) * rh
        d.text(P(x + (18 if i % 2 else 0), y + rh / 2), f"{i + 1:02d}", font=f("Poppins-Bold.ttf", 22), fill=acc, anchor="lm")
        d.text(P(x + (66 if i % 2 else 48), y + rh / 2), fe, font=fit(d, fe, "Poppins-Medium.ttf", 25, cw - 80), fill=ink, anchor="lm")
        if i % 2: d.line(P(x, y + 8, x, y + rh - 8), fill=rule, width=1 * S)
        if i < 2: d.line(P(44, y + rh, W0 - 44, y + rh), fill=rule, width=1 * S)
    d.line(P(44, H0 - 74, W0 - 44, H0 - 74), fill=ink, width=3 * S)
    d.text(P(44, H0 - 40), FOOT, font=f("Poppins-Bold.ttf", 23), fill=ink, anchor="lm")
    d.text(P(W0 - 44, H0 - 40), p.get("code", "EC/17"), font=f("Poppins-Bold.ttf", 23), fill=acc, anchor="rm")
    return rf.finish(img, p["out"])


# ---------------- Template AJ: torn paper poster ----------------
def _torn(y, seed, amp=16, step=26):
    rnd = random.Random(seed); pts = []; x = -10
    while x < W0 + 30:
        pts.append((x, y + rnd.uniform(-amp, amp))); x += rnd.uniform(step * 0.6, step * 1.3)
    return pts


def _tape(img, cx, cy, w, h, ang, fill, draw_fn=None, seed=1):
    """Flat masking tape strip with zig-zag torn ends, rotated."""
    pad = 30; L = Image.new("RGBA", P(w + 2 * pad, h + 2 * pad), (0, 0, 0, 0)); d = ImageDraw.Draw(L)
    rnd = random.Random(seed); n = 7
    left = [(pad + rnd.uniform(0, 9), pad + h * i / n) for i in range(n + 1)]
    right = [(pad + w - rnd.uniform(0, 9), pad + h * (n - i) / n) for i in range(n + 1)]
    d.polygon([P(*q) for q in left + right], fill=fill)
    if draw_fn: draw_fn(d, pad, pad, w, h)
    L = L.rotate(ang, expand=True, resample=Image.BICUBIC); _paste_c(img, L, cx, cy)


def template_aj(p):
    top = p.get("top", (36, 60, 160)); paper = p.get("paper", (250, 246, 238)); ink = p.get("ink", (24, 24, 32))
    acc = p.get("acc", (255, 200, 60)); acc2 = p.get("acc2", (255, 110, 120)); tape = p.get("tape", (255, 226, 120))
    TY = p.get("tear_y", 830)
    img = Image.new("RGBA", (W, H), paper + (255,)); d = ImageDraw.Draw(img)
    pts = _torn(TY, p["out"]); fib = [(x, y + 14) for x, y in _torn(TY + 2, p["out"] + "f", amp=12, step=20)]
    d.polygon([P(-10, -10), P(W0 + 30, -10)] + [P(x, y) for x, y in reversed(fib)], fill=WHITE)
    d.polygon([P(-10, -10), P(W0 + 30, -10)] + [P(x, y) for x, y in reversed(pts)], fill=top)
    # flat confetti shapes on the colour half
    rnd = random.Random(p["out"] + "c"); hlt = WHITE if _lum(top) < 150 else ink
    for k in range(p.get("confetti", 9)):
        x = rnd.choice([rnd.uniform(40, 110), rnd.uniform(W0 - 110, W0 - 40)]); y = rnd.uniform(330, TY - 70)
        s = rnd.uniform(9, 15); c = [acc, acc2, mix(top, WHITE, 0.3)][k % 3]
        if any(abs(x - qx) < 170 and abs(y - qy) < 110 for qx, qy in p.get("avoid", [])): continue
        if k % 3 == 0: d.ellipse(P(x - s, y - s, x + s, y + s), fill=c)
        elif k % 3 == 1: d.polygon([P(x, y - s * 1.2), P(x + s * 1.1, y + s * .8), P(x - s * 1.1, y + s * .8)], fill=c)
        else: d.rectangle(P(x - s * 1.3, y - s * .45, x + s * 1.3, y + s * .45), fill=c)
    logo_chip(img, 44, 30, 110, fill=WHITE); d = ImageDraw.Draw(img)
    tf = f("Poppins-Bold.ttf", 21); tw = d.textlength(p["tag"], font=tf) / S
    d.rounded_rectangle(P(W0 - 44 - tw - 40, 38, W0 - 44, 84), radius=23 * S, fill=acc)
    d.text(P(W0 - 64 - tw, 61), p["tag"], font=tf, fill=ink, anchor="lm")
    h1, h2 = p["head"]; hf = f("Poppins-Bold.ttf", p.get("hsize", 74))
    for l in (h1, h2): hf = fit(d, l, "Poppins-Bold.ttf", hf.size / S, W0 - 110)
    lh = hf.size / S * 1.06
    d.text(P(W0 / 2, 128), h1, font=hf, fill=hlt, anchor="ma"); d.text(P(W0 / 2, 128 + lh), h2, font=hf, fill=acc, anchor="ma")
    items = p.get("items")
    if items:
        for k, it in enumerate(items):
            _put(img, it["img"], it["cx"], it["cy"], it["mw"], it["mh"], it.get("ang", 0)); d = ImageDraw.Draw(img)
            def pfn(dd, x, y, w, h, it=it):
                nm = it["name"]; nf = fit(dd, nm, "Poppins-Bold.ttf", 21, w - 40)
                dd.text(P(x + w / 2, y + 30), nm, font=nf, fill=mix(ink, tape, 0.2), anchor="mm")
                pt = tk(it["price"]); pf = fit(dd, pt, "Poppins-Bold.ttf", 50, w - 40)
                dd.text(P(x + w / 2, y + 76), pt, font=pf, fill=ink, anchor="mm")
                if it.get("regular") and it["regular"] > it["price"]:
                    rt = "Regular " + tk(it["regular"]); rfo = f("Poppins-Medium.ttf", 18); rw = dd.textlength(rt, font=rfo) / S
                    strike(dd, x + w / 2 - rw / 2, y + h - 38, rt, rfo, mix(ink, tape, 0.35))
            _tape(img, it["px"], it["py"], 290, 150, it.get("pang", 6), tape, pfn, seed=k + 3); d = ImageDraw.Draw(img)
    else:
        _put(img, p["img"], p.get("cx", W0 / 2), p.get("cy", 560), p.get("maxw", 560), p.get("maxh", 520), p.get("ang", 0)); d = ImageDraw.Draw(img)
        def pfn(dd, x, y, w, h):
            dd.text(P(x + w / 2, y + 30), "ONLY", font=f("Poppins-Bold.ttf", 20), fill=mix(ink, tape, 0.3), anchor="mm")
            pt = tk(p["price"]); pf = fit(dd, pt, "Poppins-Bold.ttf", 56, w - 40)
            dd.text(P(x + w / 2, y + h / 2 + 4), pt, font=pf, fill=ink, anchor="mm")
            if p.get("regular") and p["regular"] > p["price"]:
                rt = "Regular " + tk(p["regular"]); rfo = f("Poppins-Medium.ttf", 19); rw = dd.textlength(rt, font=rfo) / S
                strike(dd, x + w / 2 - rw / 2, y + h - 40, rt, rfo, mix(ink, tape, 0.35))
        _tape(img, p.get("px", 840), p.get("py", 470), 270, 150, p.get("pang", 8), tape, pfn, seed=7); d = ImageDraw.Draw(img)
        if p.get("spec"):   # round spec badge
            big_, small_ = p["spec"]; cx, cy, r = p.get("sx", 200), p.get("sy", 560), 88
            d.ellipse(P(cx - r, cy - r, cx + r, cy + r), fill=acc2)
            d.ellipse(P(cx - r + 7, cy - r + 7, cx + r - 7, cy + r - 7), outline=WHITE, width=2 * S)
            bf = fit(d, big_, "Poppins-Bold.ttf", 44, 130); d.text(P(cx, cy - 12), big_, font=bf, fill=WHITE, anchor="mm")
            sf = fit(d, small_, "Poppins-Bold.ttf", 16, 120); d.text(P(cx, cy + 28), small_, font=sf, fill=WHITE, anchor="mm")
    # Bangla tape
    by = p.get("bn_y", TY + 92)
    bw = min(W0 - 120, 120 + d.textlength(p["bn"], font=f("Poppins-Bold.ttf", 30)) / S * 0.9)
    def bfn(dd, x, y, w, h): _bnq(dd, x + w / 2, y + h / 2, p["bn"], 32, w - 60, ink, anchor="mm")
    _tape(img, W0 / 2, by, W0 - 130, 72, p.get("bang", -1.2), mix(acc2, WHITE, 0.62), bfn, seed=11); d = ImageDraw.Draw(img)
    ty = by + 62
    ftt, tl = wrap(d, p["title"], "Poppins-Bold.ttf", 34, W0 - 110, 1)
    d.text(P(W0 / 2, ty), tl[0], font=ftt, fill=ink, anchor="ma")
    feats = p.get("feats", [])[:4]; fy0 = ty + 66; cw = (W0 - 120) / 2; rh = min(78, (H0 - 96 - fy0) / 2)
    for i, fe in enumerate(feats):
        x = 60 + (i % 2) * cw; y = fy0 + (i // 2) * rh + rh / 2
        rf.check_icon(d, x + 14, y, 14, top, WHITE)
        d.text(P(x + 40, y), fe, font=fit(d, fe, "Poppins-Medium.ttf", 25, cw - 56), fill=ink, anchor="lm")
    d.rectangle(P(0, H0 - 68, W0, H0), fill=top)
    d.text(P(W0 / 2, H0 - 34), FOOT, font=f("Poppins-Bold.ttf", 24), fill=WHITE if _lum(top) < 150 else ink, anchor="mm")
    return rf.finish(img, p["out"])


TEMPLATES17 = {"AI": template_ai, "AJ": template_aj}
