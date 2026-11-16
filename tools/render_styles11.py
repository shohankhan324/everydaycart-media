"""Style set 11 (added 16 Nov 2026): W shop shelf (flat striped awning with scalloped edge, wallpaper stripes,
product standing on a wooden shelf with a supermarket style shelf-edge price label, chalkboard sign with the Bangla
line and ticked features; collection mode puts several products on the shelf, each with its own label),
X neo brutal (pastel background, thick ink outlines with solid offset shadows: highlighted headline, outlined
product card with a tilted sticker, chunky price button, outlined Bangla bar, 2x2 feature chips, ink footer bar;
collection mode puts two products on the card with outlined mini price tags).
Flat only (no gradients, no blur), Poppins + Hind Siliguri, small logo chip in a corner."""
from PIL import Image, ImageDraw
import render_flat as rf
from render_flat import P, f, fit, wrap, tk, S, W, H, W0, H0, INK, check_icon
from render_styles4 import logo_chip, mix, strike
from render_styles6 import fbn, _layer
from render_styles8 import _scaled, _center, _tag, _bn_fit

WHITE = (255, 255, 255)


def _bottom(img, prod, cx, by, maxw, maxh):
    """Place a product so its bottom edge sits on y=by (shelf top)."""
    pr = _scaled(prod, maxw, maxh)
    img.alpha_composite(pr, (int(cx * S - pr.width / 2), int(by * S - pr.height)))
    return pr.width / S, pr.height / S


# ---------------- Template W: shop shelf ----------------
def template_w(p):
    bg = p.get("bg", (238, 226, 206)); acc = p.get("acc", (214, 74, 60)); ink = p.get("ink", INK)
    wood = p.get("wood", (196, 140, 90)); board = p.get("board", (40, 62, 54)); chalk = (246, 244, 236)
    hcol = p.get("hcol", ink)
    img = Image.new("RGBA", (W, H), bg + (255,)); d = ImageDraw.Draw(img)
    # wallpaper stripes
    sc = mix(bg, ink, 0.035)
    for x in range(0, W0, 72): d.rectangle(P(x, 0, x + 30, H0), fill=sc)
    # striped awning with scalloped edge
    AY = 130; n = 9; sw = W0 / n; stripe2 = p.get("stripe2", WHITE)
    for i in range(n):
        col = acc if i % 2 == 0 else stripe2
        d.rectangle(P(i * sw, 0, (i + 1) * sw, AY), fill=col)
        d.ellipse(P(i * sw, AY - sw / 2, (i + 1) * sw, AY + sw / 2), fill=col)
    d.rectangle(P(0, 0, W0, 16), fill=mix(acc, ink, 0.35))
    # headline
    hy = AY + sw / 2 + 34; head = p["head"]
    ft = f("Poppins-Bold.ttf", p.get("hsize", 64))
    for l in head: ft = fit(d, l, "Poppins-Bold.ttf", ft.size / S, p.get("hw", 700))
    for i, l in enumerate(head):
        d.text(P(60, hy + i * ft.size / S * 1.1), l, font=ft, fill=acc if i == len(head) - 1 else hcol)
    # shelf
    SY = p.get("shelf_y", 840)
    for bx in (150, W0 - 76):   # brackets
        d.polygon([P(bx - 14, SY + 36), P(bx + 14, SY + 36), P(bx + 14, SY + 110), P(bx - 14, SY + 70)], fill=mix(wood, ink, 0.45))
    items = p.get("items")
    if items:
        for it in items:
            w_, h_ = _bottom(img, it["img"], it["cx"], SY + 2, it["mw"], it["mh"])
    else:
        _bottom(img, p["img"], p.get("cx", 470), SY + 2 + p.get("dy", 0), p.get("maxw", 520), p.get("maxh", 470))
    d = ImageDraw.Draw(img)
    d.rectangle(P(40, SY, W0 - 40, SY + 16), fill=mix(wood, WHITE, 0.25))
    d.rectangle(P(40, SY + 16, W0 - 40, SY + 46), fill=wood)
    # shelf-edge price label(s)
    def label(cx, price, regular, name=None, wl=250, ang=-3):
        LH = 132 if not name else 150

        def draw(L):
            dl = ImageDraw.Draw(L)
            dl.rectangle(P(0, 0, wl, LH), fill=WHITE)
            dl.rectangle(P(0, 0, wl, 34), fill=acc)
            dl.text(P(wl / 2, 17), name or p.get("label", "PRICE"), font=fit(dl, name or p.get("label", "PRICE"), "Poppins-Bold.ttf", 20, wl - 24),
                    fill=WHITE, anchor="mm")
            pt = tk(price); pf = fit(dl, pt, "Poppins-Bold.ttf", 54 if not name else 46, wl - 30)
            dl.text(P(wl / 2, 34 + (LH - 34) * 0.42), pt, font=pf, fill=ink, anchor="mm")
            if regular and regular > price:
                rt = "Regular " + tk(regular); rfo = f("Poppins-Medium.ttf", 19); rw = dl.textlength(rt, font=rfo) / S
                strike(dl, wl / 2 - rw / 2, LH - 36, rt, rfo, mix(WHITE, ink, 0.55))
        _layer(img, (cx - wl / 2, SY + 30, cx + wl / 2, SY + 30 + LH), draw, ang)
    if items:
        for it in items: label(it["cx"], it["price"], it.get("regular"), it.get("name"), it.get("lw", 230), it.get("ang", -3))
    else:
        label(p.get("lx", 800), p["price"], p.get("regular"), None, 270, p.get("lang", -4))
    d = ImageDraw.Draw(img)
    # chalkboard sign
    BX0, BX1 = 60, W0 - 60; BY0 = p.get("board_y", SY + 200); BY1 = H0 - 96
    d.rounded_rectangle(P(BX0 - 14, BY0 - 14, BX1 + 14, BY1 + 14), radius=26 * S, fill=wood)
    d.rounded_rectangle(P(BX0, BY0, BX1, BY1), radius=16 * S, fill=board)
    y = BY0 + 26
    ftt, tl = wrap(d, p["title"], "Poppins-Bold.ttf", 32, BX1 - BX0 - 60, 1)
    d.text(P(BX0 + 30, y), tl[0], font=ftt, fill=chalk); y += ftt.size / S * 1.35
    if p.get("bn"):
        fb = _bn_fit(d, p["bn"], 28, BX1 - BX0 - 60)
        d.text(P(BX0 + 30, y), p["bn"], font=fb, fill=p.get("bncol", (255, 214, 120))); y += 52
    feats = p.get("feats", [])[:4]; cw = (BX1 - BX0 - 60) / 2
    for i, fe in enumerate(feats):
        fx = BX0 + 30 + (i % 2) * cw; fy = y + (i // 2) * 44
        check_icon(d, fx + 13, fy + 16, 13, chalk, board)
        d.text(P(fx + 38, fy + 16), fe, font=fit(d, fe, "Poppins-Medium.ttf", 23, cw - 50), fill=chalk, anchor="lm")
    d.text(P(W0 / 2, H0 - 46), "everydaycart.online  |  Inbox us to order", font=f("Poppins-Bold.ttf", 25),
           fill=ink, anchor="mm")
    logo_chip(img, 40, 30, 110); d = ImageDraw.Draw(img)
    # tag pill sits on the wall, right side, under the awning
    tf = f("Poppins-Bold.ttf", 21); tw = d.textlength(p["tag"], font=tf) / S
    ty = AY + sw / 2 + 80
    d.rounded_rectangle(P(W0 - 50 - tw - 40, ty - 60, W0 - 50, ty - 14), radius=23 * S, fill=ink)
    d.text(P(W0 - 50 - tw - 20, ty - 37), p["tag"], font=tf, fill=WHITE, anchor="lm")
    return rf.finish(img, p["out"])


# ---------------- Template X: neo brutal ----------------
def _bx(d, x0, y0, x1, y1, fill, ink, r=22, sh=10, bw=4):
    d.rounded_rectangle(P(x0 + sh, y0 + sh, x1 + sh, y1 + sh), radius=r * S, fill=ink)
    d.rounded_rectangle(P(x0, y0, x1, y1), radius=r * S, fill=fill, outline=ink, width=bw * S)


def template_x(p):
    bg = p.get("bg", (255, 236, 214)); acc = p.get("acc", (255, 214, 64)); acc2 = p.get("acc2", (120, 190, 255))
    ink = p.get("ink", (22, 22, 26)); card = p.get("card", WHITE)
    img = Image.new("RGBA", (W, H), bg + (255,)); d = ImageDraw.Draw(img)
    # flat grid paper
    gc = mix(bg, ink, 0.07)
    for x in range(0, W0, 60): d.line(P(x, 0, x, H0), fill=gc, width=S)
    for y in range(0, H0, 60): d.line(P(0, y, W0, y), fill=gc, width=S)
    # logo chip (top-left) with ink outline
    from render_flat import load_logo
    lg = load_logo(104); lw, lh = lg.width / S, lg.height / S
    _bx(d, 44, 36, 44 + lw + 28, 36 + lh + 22, WHITE, ink, r=14, sh=6, bw=3)
    img.alpha_composite(lg, (int(58 * S), int(47 * S))); d = ImageDraw.Draw(img)
    # tag (top-right)
    tf = f("Poppins-Bold.ttf", 21); tw = d.textlength(p["tag"], font=tf) / S
    _bx(d, W0 - 50 - tw - 40, 40, W0 - 50, 88, acc2, ink, r=24, sh=5, bw=3)
    d.text(P(W0 - 50 - tw - 20, 64), p["tag"], font=tf, fill=ink, anchor="lm")
    # headline: line 1 plain, line 2 on a highlight block
    h1, h2 = p["head"]; y = 132
    ft1 = fit(d, h1, "Poppins-Bold.ttf", p.get("hsize", 60), 960)
    d.text(P(60, y), h1, font=ft1, fill=ink); y += ft1.size / S * 1.32
    ft2 = fit(d, h2, "Poppins-Bold.ttf", p.get("hsize", 60), 900); w2 = d.textlength(h2, font=ft2) / S
    _bx(d, 50, y, 50 + w2 + 40, y + ft2.size / S * 1.3, acc, ink, r=12, sh=7, bw=4)
    d.text(P(70, y + ft2.size / S * 0.65), h2, font=ft2, fill=ink, anchor="lm")
    # product card
    CX0, CY0, CX1, CY1 = 50, p.get("card_y", 330), W0 - 60, p.get("card_y1", 935)
    _bx(d, CX0, CY0, CX1, CY1, card, ink, r=34, sh=14, bw=5)
    # flat dot behind product
    pcx, pcy = p.get("pcx", 430), (CY0 + CY1) / 2
    rr = min(CY1 - CY0, 600) * 0.42
    d.ellipse(P(pcx - rr, pcy - rr, pcx + rr, pcy + rr), fill=p.get("blob", mix(acc2, WHITE, 0.55)))
    items = p.get("items")
    if items:
        for it in items:
            _center(img, it["img"], it["cx"], pcy + it.get("dy", 0), it["mw"], it["mh"])
    else:
        _center(img, p["img"], pcx + p.get("dx", 0), pcy + p.get("dy", 0), p.get("maxw", 480), p.get("maxh", 440))
    d = ImageDraw.Draw(img)
    # price button (right side of the card) or mini tags for collections
    if items:
        for it in items:
            pt = tk(it["price"]); pf = f("Poppins-Bold.ttf", 34); pw = d.textlength(pt, font=pf) / S
            nm = it["name"]; nf = fit(d, nm, "Poppins-Bold.ttf", 20, 260); nw = d.textlength(nm, font=nf) / S
            bw_ = max(pw, nw) + 44; x0 = it["cx"] - bw_ / 2; y0 = CY1 - 128
            _bx(d, x0, y0, x0 + bw_, y0 + 96, acc, ink, r=16, sh=6, bw=3)
            d.text(P(it["cx"], y0 + 26), nm, font=nf, fill=ink, anchor="mm")
            d.text(P(it["cx"], y0 + 64), pt, font=pf, fill=ink, anchor="mm")
    else:
        pt = tk(p["price"]); pf = f("Poppins-Bold.ttf", 60); pw = d.textlength(pt, font=pf) / S
        BW = max(pw + 60, 290); bx1 = CX1 - 40; bx0 = bx1 - BW; by0 = p.get("price_y", CY0 + 70)
        _bx(d, bx0, by0, bx1, by0 + 150, acc, ink, r=26, sh=9, bw=4)
        d.text(P((bx0 + bx1) / 2, by0 + 30), p.get("label", "PRICE"), font=f("Poppins-Bold.ttf", 21), fill=ink, anchor="mm")
        d.text(P((bx0 + bx1) / 2, by0 + 80), pt, font=pf, fill=ink, anchor="mm")
        if p.get("regular", 0) > p["price"]:
            rt = "Regular " + tk(p["regular"]); rfo = f("Poppins-Medium.ttf", 20); rw = d.textlength(rt, font=rfo) / S
            strike(d, (bx0 + bx1) / 2 - rw / 2, by0 + 112, rt, rfo, mix(acc, ink, 0.6))
        # tilted sticker on the card (bottom-right)
        st = p.get("sticker")
        if st:
            sf = f("Poppins-Bold.ttf", 24)
            sw_ = ImageDraw.Draw(Image.new("RGBA", (10, 10))).textlength(st, font=sf) / S + 44

            def drs(L):
                dl = ImageDraw.Draw(L)
                dl.rounded_rectangle(P(6, 6, sw_ + 6, 60), radius=27 * S, fill=ink)
                dl.rounded_rectangle(P(0, 0, sw_, 54), radius=27 * S, fill=acc2, outline=ink, width=3 * S)
                dl.text(P(sw_ / 2, 27), st, font=sf, fill=ink, anchor="mm")
            sx1 = CX1 - 40; _layer(img, (sx1 - sw_ - 6, CY1 - 110, sx1, CY1 - 50), drs, p.get("sang", 6))
            d = ImageDraw.Draw(img)
    # title + Bangla bar
    y = CY1 + 40
    ftt, tl = wrap(d, p["title"], "Poppins-Bold.ttf", 32, W0 - 120, 1)
    d.text(P(60, y), tl[0], font=ftt, fill=ink); y += ftt.size / S * 1.4
    if p.get("bn"):
        fb = _bn_fit(d, p["bn"], 28, W0 - 170); bw2 = d.textlength(p["bn"], font=fb) / S
        _bx(d, 50, y, 50 + bw2 + 48, y + 58, card, ink, r=29, sh=5, bw=3)
        d.text(P(74, y + 29), p["bn"], font=fb, fill=ink, anchor="lm"); y += 82
    # 2x2 feature chips
    feats = p.get("feats", [])[:4]; cw = (W0 - 120 - 24) / 2
    for i, fe in enumerate(feats):
        fx = 50 + (i % 2) * (cw + 24); fy = y + (i // 2) * 66
        _bx(d, fx, fy, fx + cw, fy + 52, WHITE, ink, r=14, sh=4, bw=3)
        check_icon(d, fx + 28, fy + 26, 13, acc2 if i % 2 else acc, ink)
        d.text(P(fx + 52, fy + 26), fe, font=fit(d, fe, "Poppins-Medium.ttf", 23, cw - 66), fill=ink, anchor="lm")
    # ink footer bar
    d.rectangle(P(0, H0 - 70, W0, H0), fill=ink)
    d.text(P(W0 / 2, H0 - 35), "everydaycart.online  |  Inbox us to order", font=f("Poppins-Bold.ttf", 25),
           fill=acc, anchor="mm")
    return rf.finish(img, p["out"])


TEMPLATES11 = {"W": template_w, "X": template_x}
