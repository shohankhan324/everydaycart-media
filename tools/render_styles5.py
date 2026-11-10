"""Style set 5 (added 10 Nov 2026): K bento grid (rounded tiles: product, price, two stat tiles, title bar),
L headline pop (two-tone bold headline, flat colour blob with offset ring, speech-bubble price, white info panel).
Flat only, Poppins, small logo chip in a corner."""
from PIL import Image, ImageDraw
import render_flat as rf
from render_flat import P, f, fit, wrap, tk, S, W, H, W0, H0, INK, MUTE, check_icon
from render_styles4 import logo_chip, mix, strike


def _dots(d, box, col, step=36, r=3):
    x0, y0, x1, y1 = box
    for yy in range(int(y0) + step // 2, int(y1), step):
        off = step // 2 if ((yy - y0) // step) % 2 else 0
        for xx in range(int(x0) + step // 2 + off, int(x1) - 6, step):
            d.ellipse(P(xx - r, yy - r, xx + r, yy + r), fill=col)


def _place_many(img, imgs, cx, cy, maxw, maxh, gap=30):
    """Place one or more cutouts side by side, scaled to the same height, centred on (cx, cy)."""
    if not isinstance(imgs, (list, tuple)): imgs = [imgs]
    ratios = [i.width / i.height for i in imgs]
    hgt = min(maxh, (maxw - gap * (len(imgs) - 1)) / sum(ratios))
    total = sum(r * hgt for r in ratios) + gap * (len(imgs) - 1)
    x = cx - total / 2
    for i, r in zip(imgs, ratios):
        w = r * hgt; img = rf.place(img, i, x + w / 2, cy, w, hgt); x += w + gap
    return img


# ---------------- Template K: bento grid ----------------
def template_k(p):
    bg = p.get("bg", (246, 242, 236)); tile = p.get("tile", (214, 226, 240)); acc = p.get("acc", (232, 104, 72))
    dark = p.get("dark", (34, 44, 70)); ink = p.get("ink", INK)
    img = Image.new("RGBA", (W, H), bg + (255,)); d = ImageDraw.Draw(img)
    M, G = 40, 20; R = 34
    A = (M, M, 700, 900); B = (720, M, W0 - M, 420); C = (720, 440, W0 - M, 660); Dd = (720, 680, W0 - M, 900)
    E = (M, 920, W0 - M, 1200)
    # product tile
    d.rounded_rectangle(P(*A), radius=R * S, fill=tile)
    _dots(d, (A[0] + 20, A[1] + 120, A[2] - 20, A[3] - 20), mix(tile, (255, 255, 255), 0.45), 40, 3)
    cx, cy = (A[0] + A[2]) / 2, p.get("cy", 500)
    d.ellipse(P(cx - 250, cy - 250, cx + 250, cy + 250), fill=mix(tile, (255, 255, 255), 0.55))
    d.ellipse(P(cx - 284, cy - 284, cx + 284, cy + 284), outline=mix(tile, dark, 0.18), width=3 * S)
    img = _place_many(img, p["img"], cx, cy, p.get("maxw", 520), p.get("maxh", 600)); d = ImageDraw.Draw(img)
    logo_chip(img, A[0] + 26, A[1] + 26, 120); d = ImageDraw.Draw(img)
    tf = f("Poppins-Medium.ttf", 21); tt = p["tag"]; tw = d.textlength(tt, font=tf) / S
    d.rounded_rectangle(P(A[0] + 26, A[3] - 74, A[0] + 26 + tw + 40, A[3] - 28), radius=23 * S, fill=dark)
    d.text(P(A[0] + 46, A[3] - 66), tt, font=tf, fill="white")
    # price tile
    d.rounded_rectangle(P(*B), radius=R * S, fill=acc)
    bx = B[0] + 36
    d.text(P(bx, B[1] + 40), p.get("label", "ONLY"), font=f("Poppins-Medium.ttf", 24), fill=mix(acc, (255, 255, 255), 0.7))
    pt = tk(p["price"]); pf = fit(d, pt, "Poppins-Bold.ttf", 70, B[2] - bx - 30)
    d.text(P(bx, B[1] + 74), pt, font=pf, fill="white")
    if p.get("regular", 0) > p["price"]:
        strike(d, bx + 2, B[1] + 170, tk(p["regular"]), f("Poppins-Regular.ttf", 30), mix(acc, (255, 255, 255), 0.7))
    cf = f("Poppins-Bold.ttf", 24); ct = "Inbox to order"; cw = d.textlength(ct, font=cf) / S
    d.rounded_rectangle(P(bx, B[3] - 100, bx + cw + 46, B[3] - 44), radius=28 * S, fill="white")
    d.text(P(bx + 23, B[3] - 89), ct, font=cf, fill=acc)
    # stat tiles
    for box, (big, small), fill, fg, sub in ((C, p["stats"][0], dark, "white", mix(dark, (255, 255, 255), 0.65)),
                                             (Dd, p["stats"][1], (255, 255, 255), dark, MUTE)):
        d.rounded_rectangle(P(*box), radius=R * S, fill=fill)
        bf = fit(d, big, "Poppins-Bold.ttf", 76, box[2] - box[0] - 70)
        d.text(P(box[0] + 36, box[1] + 34), big, font=bf, fill=fg if fill != (255, 255, 255) else acc)
        sf, sl = wrap(d, small, "Poppins-Medium.ttf", 25, box[2] - box[0] - 70, 2)
        y = box[3] - 40 - len(sl) * sf.size / S * 1.2
        for l in sl: d.text(P(box[0] + 36, y), l, font=sf, fill=sub); y += sf.size / S * 1.2
    # title tile
    d.rounded_rectangle(P(*E), radius=R * S, fill=(255, 255, 255))
    ft, lines = wrap(d, p["title"], "Poppins-Bold.ttf", 54, E[2] - E[0] - 90, 2)
    y = E[1] + 34
    for l in lines: d.text(P(E[0] + 44, y), l, font=ft, fill=ink); y += ft.size / S * 1.15
    sf = fit(d, p["sub"], "Poppins-Regular.ttf", 27, E[2] - E[0] - 90)
    d.text(P(E[0] + 44, y + 4), p["sub"], font=sf, fill=MUTE)
    x, yy = E[0] + 44, E[3] - 86
    for t in p["feats"]:
        chf = f("Poppins-Medium.ttf", 24); cw = d.textlength(t, font=chf) / S
        if x + cw + 64 > E[2] - 40: break
        d.rounded_rectangle(P(x, yy, x + cw + 56, yy + 52), radius=26 * S, fill=mix(tile, (255, 255, 255), 0.35))
        d.ellipse(P(x + 17, yy + 20, x + 29, yy + 32), fill=acc)
        d.text(P(x + 38, yy + 10), t, font=chf, fill=ink); x += cw + 70
    # footer
    uf = f("Poppins-Bold.ttf", 30); d.text(P(M + 8, 1244), "everydaycart.online", font=uf, fill=dark)
    nf = f("Poppins-Medium.ttf", 25); nt = "Limited stock available"; nw = d.textlength(nt, font=nf) / S
    d.ellipse(P(W0 - M - 8 - nw - 30, 1259, W0 - M - 8 - nw - 16, 1273), fill=acc)
    d.text(P(W0 - M - 8 - nw, 1248), nt, font=nf, fill=MUTE)
    return rf.finish(img, p["out"])


# ---------------- Template L: headline pop ----------------
def template_l(p):
    bg = p.get("bg", (240, 120, 60)); hl = p.get("hl", (255, 222, 120)); acc = p.get("acc", (40, 60, 110))
    blob = p.get("blob", mix(bg, (255, 255, 255), 0.25)); ink = p.get("ink", INK)
    img = Image.new("RGBA", (W, H), bg + (255,)); d = ImageDraw.Draw(img)
    logo_chip(img, 48, 46, 124); d = ImageDraw.Draw(img)
    tf = f("Poppins-Medium.ttf", 21); tt = p["tag"]; tw = d.textlength(tt, font=tf) / S
    d.rounded_rectangle(P(W0 - 48 - tw - 42, 54, W0 - 48, 100), radius=23 * S, outline="white", width=2 * S)
    d.text(P(W0 - 48 - tw - 21, 61), tt, font=tf, fill="white")
    # two-tone headline
    l1, l2 = p["head"]
    hf = fit(d, max(l1, l2, key=len), "Poppins-Bold.ttf", 96, 960)
    d.text(P(56, 136), l1, font=hf, fill="white")
    d.text(P(56, 136 + hf.size / S * 1.02), l2, font=hf, fill=hl)
    # blob + offset ring
    cx, cy, r = p.get("cx", 520), p.get("cy", 700), p.get("r", 270)
    d.ellipse(P(cx - r + 26, cy - r + 22, cx + r + 26, cy + r + 22), outline=hl, width=4 * S)
    d.ellipse(P(cx - r, cy - r, cx + r, cy + r), fill=blob)
    img = _place_many(img, p["img"], cx, cy + 10, p.get("maxw", 480), p.get("maxh", 500), p.get("gap", 30)); d = ImageDraw.Draw(img)
    # speech-bubble price
    prices = p.get("prices") or [(p.get("label", "ONLY"), p["price"], p.get("regular", 0))]
    bx0, by0 = p.get("bx", 760), p.get("by", 820)
    rows = len(prices); bw = 270; bh = 40 + rows * 96
    d.polygon([P(bx0 + 40, by0 + 6), P(bx0 + 10, by0 - 44), P(bx0 + 100, by0 + 6)], fill=acc)
    d.rounded_rectangle(P(bx0, by0, bx0 + bw, by0 + bh), radius=30 * S, fill=acc)
    y = by0 + 22
    for lab, pr, reg in prices:
        lf = f("Poppins-Medium.ttf", 21); d.text(P(bx0 + 28, y), lab, font=lf, fill=mix(acc, (255, 255, 255), 0.7))
        pf = fit(d, tk(pr), "Poppins-Bold.ttf", 46, 150); d.text(P(bx0 + 28, y + 26), tk(pr), font=pf, fill="white")
        if reg and reg > pr:
            pw = d.textlength(tk(pr), font=pf) / S
            strike(d, bx0 + 28 + pw + 12, y + 44, f"{reg:,}", f("Poppins-Regular.ttf", 22), mix(acc, (255, 255, 255), 0.6))
        y += 96
    # white info panel
    PY = 1032
    d.rounded_rectangle(P(28, PY, W0 - 28, H0 + 60), radius=40 * S, fill=(255, 255, 255))
    ft, lines = wrap(d, p["title"], "Poppins-Bold.ttf", 46, 960, 1)
    d.text(P(64, PY + 30), lines[0], font=ft, fill=ink)
    feats = p["feats"][:4]; cols = 2; colw = 470
    for i, t in enumerate(feats):
        x = 64 + (i % cols) * colw; yy = PY + 112 + (i // cols) * 54
        check_icon(d, x + 15, yy + 17, 15, bg, (255, 255, 255))
        d.text(P(x + 44, yy), t, font=fit(d, t, "Poppins-Medium.ttf", 25, colw - 60), fill=ink)
    d.line(P(64, H0 - 92, W0 - 64, H0 - 92), fill=(236, 234, 232), width=2 * S)
    uf = f("Poppins-Bold.ttf", 28); d.text(P(64, H0 - 72), "everydaycart.online", font=uf, fill=acc)
    nf = f("Poppins-Bold.ttf", 24); nt = "Inbox us to order"; nw = d.textlength(nt, font=nf) / S
    d.text(P(W0 - 64 - nw, H0 - 70), nt, font=nf, fill=bg if p.get("cta_bg", True) else ink)
    return rf.finish(img, p["out"])


TEMPLATES5 = {"K": template_k, "L": template_l}
