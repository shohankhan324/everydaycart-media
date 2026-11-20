"""Style set 15 (added 20 Nov 2026):
AE Bauhaus geometric poster (paper background, big solid circle + half circle + quarter circle + bar composition behind
the product, bold two-line headline, solid circle price badge, ink info band with Bangla line and square-bullet features;
collection mode puts each product on its own circle with a price chip),
AF file folder card (solid background, kraft-style folder with a labelled tab, a paper sheet peeking out, a clipped photo
card holding the product, sticky note with the Bangla line, dashed price stamp, checkbox feature list, coloured index tabs).
Flat only (no gradients, no blur, no 3D), Poppins + Hind Siliguri, small logo chip in a corner."""
from PIL import Image, ImageDraw
import render_flat as rf
from render_flat import P, f, fit, wrap, tk, S, W, H, W0, H0, INK
from render_styles4 import logo_chip, mix, strike
from render_styles8 import _scaled, _bn_fit
from render_styles6 import fbn

WHITE = (255, 255, 255)
FOOT = "everydaycart.online  |  Inbox us to order"


def _place(img, prod, cx, cy, mw, mh):
    pr = _scaled(prod, mw, mh)
    img.alpha_composite(pr, (int(cx * S - pr.width / 2), int(cy * S - pr.height / 2)))
    return pr.width / S, pr.height / S


def _bn_wrap(d, text, size, maxw, lines=2):
    """Wrap a Bangla line into up to `lines` lines (no commas: the Bengali font has no comma glyph)."""
    while size > 18:
        ft = fbn(size); out = [""]
        for w_ in text.split():
            t = (out[-1] + " " + w_).strip()
            if d.textlength(t, font=ft) <= maxw * S: out[-1] = t
            else: out.append(w_)
        if len(out) <= lines: return ft, out
        size -= 1
    return ft, out


def _pill(d, x1, y, text, fill, col):
    tf = f("Poppins-Bold.ttf", 21); tw = d.textlength(text, font=tf) / S
    d.rounded_rectangle(P(x1 - tw - 40, y, x1, y + 46), radius=23 * S, fill=fill)
    d.text(P(x1 - tw - 20, y + 23), text, font=tf, fill=col, anchor="lm")


def _price_lines(d, cx, cy, r, col, sub, price, regular, label):
    d.text(P(cx, cy - r * 0.42), label, font=f("Poppins-Bold.ttf", max(18, r * 0.17)), fill=col, anchor="mm")
    pt = tk(price); pf = fit(d, pt, "Poppins-Bold.ttf", r * 0.44, r * 1.6)
    d.text(P(cx, cy + r * 0.02), pt, font=pf, fill=col, anchor="mm")
    if regular and regular > price:
        rt = "Regular " + tk(regular); rfo = fit(d, rt, "Poppins-Medium.ttf", max(16, r * 0.16), r * 1.4)
        rw = d.textlength(rt, font=rfo) / S
        strike(d, cx - rw / 2, cy + r * 0.32, rt, rfo, sub)


# ---------------- Template AE: Bauhaus geometric poster ----------------
def template_ae(p):
    paper = p.get("paper", (246, 242, 232)); ink = p.get("ink", (22, 24, 36))
    c1 = p.get("c1", (36, 72, 200)); c2 = p.get("c2", (236, 84, 52)); c3 = p.get("c3", (246, 190, 40))
    img = Image.new("RGBA", (W, H), paper + (255,)); d = ImageDraw.Draw(img)
    # headline
    h1, h2 = p["head"]; hf = f("Poppins-Bold.ttf", p.get("hsize", 66))
    for l in (h1, h2): hf = fit(d, l, "Poppins-Bold.ttf", hf.size / S, 980)
    d.text(P(50, 122), h1, font=hf, fill=ink); d.text(P(50, 122 + hf.size / S * 1.08), h2, font=hf, fill=c2)
    TOP, BOT = 300, 900
    items = p.get("items")
    if items:
        # composition: bar + quarter circle corners, one circle per product
        d.rectangle(P(0, TOP + 250, W0, TOP + 330), fill=c3)
        d.pieslice(P(W0 - 200, TOP - 120, W0 + 200, TOP + 280), 90, 180, fill=c1)
        d.pieslice(P(-180, BOT - 200, 180, BOT + 160), 270, 360, fill=c2)
        for k, it in enumerate(items):
            cx, cy, rr = it["cx"], it.get("cy", 560), it.get("r", 190)
            d.ellipse(P(cx - rr, cy - rr, cx + rr, cy + rr), fill=it.get("disc", [c1, c2, c3][k % 3]))
            _place(img, it["img"], cx, cy + it.get("dy", 0), it["mw"], it["mh"]); d = ImageDraw.Draw(img)
            nm, pt = it["name"], tk(it["price"]); nf = fit(d, nm, "Poppins-Bold.ttf", 22, it.get("nmax", 300))
            pf = f("Poppins-Bold.ttf", 30)
            w = max(d.textlength(nm, font=nf), d.textlength(pt, font=pf)) / S + 44
            y = cy + rr + 22
            d.rectangle(P(cx - w / 2, y, cx + w / 2, y + 88), fill=ink)
            d.text(P(cx, y + 25), nm, font=nf, fill=WHITE, anchor="mm")
            d.text(P(cx, y + 62), pt, font=pf, fill=c3, anchor="mm")
            if it.get("regular") and it["regular"] > it["price"]:
                rt = "Regular " + tk(it["regular"]); rfo = f("Poppins-Medium.ttf", 19); rw = d.textlength(rt, font=rfo) / S
                strike(d, cx - rw / 2, y + 96, rt, rfo, mix(ink, paper, 0.35))
    else:
        CX, CY = p.get("cx", 470), p.get("cy", 600); R = p.get("r", 270)
        d.rectangle(P(0, CY + 120, W0, CY + 190), fill=c3)                       # horizon bar
        d.pieslice(P(W0 - 230, TOP - 130, W0 + 230, TOP + 330), 90, 180, fill=c2)  # quarter circle top right
        d.pieslice(P(CX + R - 40, BOT - 190, CX + R + 300, BOT + 150), 180, 360, fill=c2)  # half circle
        d.ellipse(P(CX - R, CY - R, CX + R, CY + R), fill=c1)
        for k in range(5): d.ellipse(P(70 + k * 34, TOP + 10, 88 + k * 34, TOP + 28), fill=ink)  # dot row
        _place(img, p["img"], CX + p.get("dx", 0), CY + p.get("dy", 0), p.get("maxw", 440), p.get("maxh", 470))
        d = ImageDraw.Draw(img)
        bx, by, br = p.get("bx", 850), p.get("by", 470), p.get("br", 135)
        d.ellipse(P(bx - br, by - br, bx + br, by + br), fill=ink)
        _price_lines(d, bx, by, br, WHITE, mix(WHITE, ink, 0.35), p["price"], p.get("regular"), p.get("label", "ONLY"))
        st = p.get("sticker")
        if st:
            sf = fit(d, st, "Poppins-Bold.ttf", 22, 360); sw = d.textlength(st, font=sf) / S + 40
            sx, sy = p.get("sx", W0 - 60 - sw), p.get("sy", by + br + 40)
            d.rectangle(P(sx, sy, sx + sw, sy + 52), fill=paper, outline=ink, width=4 * S)
            d.text(P(sx + sw / 2, sy + 26), st, font=sf, fill=ink, anchor="mm")
    # ink info band
    Y0, Y1 = p.get("band_y", BOT + 20), H0 - 70
    d.rectangle(P(0, Y0, W0, Y1), fill=ink)
    d.rectangle(P(0, Y0, 22, Y1), fill=c2)
    y = Y0 + 26
    ftt, tl = wrap(d, p["title"], "Poppins-Bold.ttf", 34, W0 - 120, 1)
    d.text(P(60, y), tl[0], font=ftt, fill=WHITE); y += ftt.size / S * 1.4
    if p.get("bn"):
        fb = _bn_fit(d, p["bn"], 30, W0 - 120)
        d.text(P(60, y + 18), p["bn"], font=fb, fill=c3, anchor="lm"); y += 50
    feats = p.get("feats", [])[:4]; cw = (W0 - 120) / 2; rowh = (Y1 - 14 - y) / 2
    for i, fe in enumerate(feats):
        fx = 60 + (i % 2) * cw; fy = y + (i // 2) * rowh + rowh / 2
        bc = [c1, c2, c3, WHITE][i]
        if sum(abs(a - b) for a, b in zip(bc, ink)) < 160: bc = WHITE
        d.rectangle(P(fx, fy - 9, fx + 18, fy + 9), fill=bc)
        d.text(P(fx + 34, fy), fe, font=fit(d, fe, "Poppins-Medium.ttf", 25, cw - 50), fill=WHITE, anchor="lm")
    d.text(P(W0 / 2, H0 - 35), FOOT, font=f("Poppins-Bold.ttf", 24), fill=ink, anchor="mm")
    logo_chip(img, 44, 32, 110, fill=WHITE); d = ImageDraw.Draw(img)
    _pill(d, W0 - 44, 40, p["tag"], ink, WHITE)
    return rf.finish(img, p["out"])


# ---------------- Template AF: file folder card ----------------
def _dashed_rect(d, box, col, dash=16, gap=10, w=3):
    x0, y0, x1, y1 = box
    x = x0
    while x < x1:
        d.line(P(x, y0, min(x + dash, x1), y0), fill=col, width=w * S); d.line(P(x, y1, min(x + dash, x1), y1), fill=col, width=w * S); x += dash + gap
    y = y0
    while y < y1:
        d.line(P(x0, y, x0, min(y + dash, y1)), fill=col, width=w * S); d.line(P(x1, y, x1, min(y + dash, y1)), fill=col, width=w * S); y += dash + gap


def template_af(p):
    bg = p.get("bg", (190, 232, 214)); folder = p.get("folder", (252, 200, 160)); back = p.get("back", mix(folder, (0, 0, 0), 0.18))
    ink = p.get("ink", (30, 32, 40)); acc = p.get("acc", (20, 130, 120)); note = p.get("note", (255, 226, 110))
    tabs = p.get("tabs", [(236, 84, 72), (60, 120, 220), (255, 196, 40)])
    img = Image.new("RGBA", (W, H), bg + (255,)); d = ImageDraw.Draw(img)
    FX0, FX1, FY1 = 56, W0 - 70, H0 - 92
    # back of folder with labelled tab
    tf = f("Poppins-Bold.ttf", 22); tw = d.textlength(p["tag"], font=tf) / S
    d.rounded_rectangle(P(FX0, 118, FX0 + tw + 90, 210), radius=20 * S, fill=back)
    d.text(P(FX0 + 45 + tw / 2, 150), p["tag"], font=tf, fill=WHITE, anchor="mm")
    d.rounded_rectangle(P(FX0, 170, FX1, FY1), radius=24 * S, fill=back)
    # paper sheet peeking out
    d.rectangle(P(FX0 + tw + 140, 134, FX1 - 40, 320), fill=WHITE)
    for k in range(3): d.line(P(FX0 + tw + 180, 168 + k * 26, FX1 - 80, 168 + k * 26), fill=mix(WHITE, bg, 0.6), width=3 * S)
    # index tabs on the right
    for k, col in enumerate(tabs):
        ty = 380 + k * 120
        d.rounded_rectangle(P(FX1 - 30, ty, FX1 + 34, ty + 96), radius=12 * S, fill=col)
    # front of folder
    FY0 = 236
    d.rounded_rectangle(P(FX0, FY0, FX1, FY1), radius=24 * S, fill=folder)
    d.line(P(FX0 + 30, FY0 + 24, FX1 - 30, FY0 + 24), fill=mix(folder, back, 0.5), width=3 * S)
    # headline (left)
    h1, h2 = p["head"]; hf = f("Poppins-Bold.ttf", p.get("hsize", 52))
    for l in (h1, h2): hf = fit(d, l, "Poppins-Bold.ttf", hf.size / S, p.get("hw", 440))
    hy = FY0 + 60
    d.text(P(FX0 + 44, hy), h1, font=hf, fill=ink); d.text(P(FX0 + 44, hy + hf.size / S * 1.1), h2, font=hf, fill=acc)
    # clipped photo card (right)
    PX0, PY0, PX1, PY1 = p.get("photo", (540, FY0 + 54, FX1 - 50, FY0 + 680))
    d.rectangle(P(PX0 + 10, PY0 + 10, PX1 + 10, PY1 + 10), fill=mix(folder, back, 0.7))
    d.rectangle(P(PX0, PY0, PX1, PY1), fill=WHITE)
    d.rectangle(P(PX0 + 18, PY0 + 18, PX1 - 18, PY1 - 18), fill=p.get("photo_bg", mix(bg, WHITE, 0.45)))
    _place(img, p["img"], (PX0 + PX1) / 2 + p.get("dx", 0), (PY0 + PY1) / 2 + p.get("dy", 0), p.get("maxw", PX1 - PX0 - 70), p.get("maxh", PY1 - PY0 - 80))
    d = ImageDraw.Draw(img)
    # paper clip (flat outline)
    cx = PX0 + 70; cw_ = 7
    d.rounded_rectangle(P(cx - 20, PY0 - 40, cx + 20, PY0 + 70), radius=20 * S, outline=ink, width=cw_ * S)
    d.rounded_rectangle(P(cx - 9, PY0 - 22, cx + 9, PY0 + 50), radius=9 * S, outline=ink, width=cw_ * S)
    # sticker on the photo
    st = p.get("sticker")
    if st:
        sf = fit(d, st, "Poppins-Bold.ttf", 21, PX1 - PX0 - 60); sw = d.textlength(st, font=sf) / S + 36
        d.rectangle(P(PX1 - 24 - sw, PY1 - 76, PX1 - 24, PY1 - 30), fill=ink)
        d.text(P(PX1 - 24 - sw / 2, PY1 - 53), st, font=sf, fill=WHITE, anchor="mm")
    # sticky note with Bangla line
    NX0, NY0, NX1 = FX0 + 44, hy + hf.size / S * 2.4 + 20, PX0 - 36
    fb, bl = _bn_wrap(d, p["bn"], 32, NX1 - NX0 - 50, 2)
    lh = fb.size / S * 1.5; NY1 = NY0 + 44 + lh * len(bl)
    d.rectangle(P(NX0, NY0, NX1, NY1), fill=note)
    d.rectangle(P((NX0 + NX1) / 2 - 50, NY0 - 14, (NX0 + NX1) / 2 + 50, NY0 + 14), fill=mix(WHITE, note, 0.4))  # tape
    for k, l in enumerate(bl):
        d.text(P(NX0 + 25, NY0 + 22 + lh * k + lh / 2), l, font=fb, fill=ink, anchor="lm")
    # dashed price stamp
    SY1 = PY1; SY0 = max(NY1 + 30, SY1 - 180)
    d.rectangle(P(NX0, SY0, NX1, SY1), fill=WHITE)
    _dashed_rect(d, (NX0 + 10, SY0 + 10, NX1 - 10, SY1 - 10), acc)
    scx = (NX0 + NX1) / 2
    d.text(P(scx, SY0 + 38), p.get("label", "PRICE"), font=f("Poppins-Bold.ttf", 22), fill=acc, anchor="mm")
    pt = tk(p["price"]); pf = fit(d, pt, "Poppins-Bold.ttf", 58, NX1 - NX0 - 60)
    d.text(P(scx, SY0 + 86), pt, font=pf, fill=ink, anchor="mm")
    if p.get("regular") and p["regular"] > p["price"]:
        rt = "Regular " + tk(p["regular"]); rfo = f("Poppins-Medium.ttf", 22); rw = d.textlength(rt, font=rfo) / S
        strike(d, scx - rw / 2, SY0 + 118, rt, rfo, mix(ink, WHITE, 0.4))
    # title label + checkbox features
    LY0 = max(PY1, SY1) + 36
    ftt, tl = wrap(d, p["title"], "Poppins-Bold.ttf", 32, FX1 - FX0 - 120, 1)
    th = ftt.size / S + 30
    d.rectangle(P(FX0 + 44, LY0, FX1 - 44, LY0 + th), fill=WHITE, outline=ink, width=3 * S)
    d.text(P(W0 / 2 - 7, LY0 + th / 2), tl[0], font=ftt, fill=ink, anchor="mm")
    y = LY0 + th + 14
    feats = p.get("feats", [])[:4]; cw = (FX1 - FX0 - 88) / 2; rowh = (FY1 - 20 - y) / 2
    for i, fe in enumerate(feats):
        fx = FX0 + 44 + (i % 2) * cw; fy = y + (i // 2) * rowh + rowh / 2
        d.rectangle(P(fx, fy - 15, fx + 30, fy + 15), fill=WHITE, outline=ink, width=3 * S)
        d.line([P(fx + 6, fy), P(fx + 13, fy + 8), P(fx + 26, fy - 10)], fill=acc, width=5 * S, joint="curve")
        d.text(P(fx + 46, fy), fe, font=fit(d, fe, "Poppins-Medium.ttf", 27, cw - 60), fill=ink, anchor="lm")
    d.text(P(W0 / 2, H0 - 46), FOOT, font=f("Poppins-Bold.ttf", 24), fill=p.get("foot", ink), anchor="mm")
    logo_chip(img, W0 - 44 - 110 * 1.5 - 28, 34, 110, fill=WHITE); d = ImageDraw.Draw(img)
    return rf.finish(img, p["out"])


TEMPLATES15 = {"AE": template_ae, "AF": template_af}
