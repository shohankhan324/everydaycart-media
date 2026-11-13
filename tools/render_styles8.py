"""Style set 8 (added 13 Nov 2026): Q magazine cover (giant masthead word across the top, product overlapping it,
numbered cover lines on the left, round price sticker, white bottom band with title and Bangla line),
R sticker sheet (dotted pastel background, product on a die-cut circle, tilted feature stickers with white borders,
tilted price sticker, Bangla tape strip; collection mode puts each product on its own circle with a price sticker).
Flat only (no gradients, no blur), Poppins + Hind Siliguri, small logo chip in the top-left corner."""
from PIL import Image, ImageDraw
import render_flat as rf
from render_flat import P, f, fit, wrap, tk, S, W, H, W0, H0, INK
from render_styles4 import logo_chip, mix, strike
from render_styles6 import fbn, _layer

WHITE = (255, 255, 255)


def _scaled(prod, maxw, maxh):
    s = min(maxw * S / prod.width, maxh * S / prod.height)
    return prod.resize((max(1, int(prod.width * s)), max(1, int(prod.height * s))), Image.LANCZOS)


def _center(img, prod, cx, cy, maxw, maxh):
    pr = _scaled(prod, maxw, maxh)
    img.alpha_composite(pr, (int(cx * S - pr.width / 2), int(cy * S - pr.height / 2)))
    return pr.width / S, pr.height / S


def _tag(img, d, text, fill, col):
    tf = f("Poppins-Bold.ttf", 21); tw = d.textlength(text, font=tf) / S
    d.rounded_rectangle(P(W0 - 44 - tw - 40, 52, W0 - 44, 98), radius=23 * S, fill=fill)
    d.text(P(W0 - 44 - tw - 20, 75), text, font=tf, fill=col, anchor="lm")


def _bn_fit(d, text, size, maxw):
    ft = fbn(size)
    while d.textlength(text, font=ft) / S > maxw and size > 16:
        size -= 1; ft = fbn(size)
    return ft


# ---------------- Template Q: magazine cover ----------------
def template_q(p):
    bg = p.get("bg", (232, 84, 60)); acc = p.get("acc", (255, 214, 90)); ink = p.get("ink", INK)
    mast = p.get("mast", mix(bg, WHITE, 0.82))
    img = Image.new("RGBA", (W, H), bg + (255,)); d = ImageDraw.Draw(img)
    BAND = p.get("band", 1060)
    # masthead word
    word = p["word"]; wf = fit(d, word, "Poppins-Bold.ttf", 300, 980)
    d.text(P(W0 / 2, p.get("mast_y", 360)), word, font=wf, fill=mast, anchor="ms")
    # thin rule + issue line under the masthead
    ry = p.get("mast_y", 360) + 26
    d.line(P(50, ry, W0 - 50, ry), fill=mix(bg, WHITE, 0.45), width=2 * S)
    d.text(P(52, ry + 30), p.get("kicker", "THIS WEEK'S PICK"), font=f("Poppins-Bold.ttf", 22), fill=acc, anchor="lm")
    d.text(P(W0 - 52, ry + 30), p.get("issue", "NOV 2026 EDITION"), font=f("Poppins-Medium.ttf", 22), fill=mix(bg, WHITE, 0.75), anchor="rm")
    # flat circle behind product
    cx, cy = p.get("cx", 650), p.get("cy", 720); r = p.get("r", 300)
    d.ellipse(P(cx - r, cy - r, cx + r, cy + r), fill=mix(bg, WHITE, 0.14))
    d.ellipse(P(cx - r + 34, cy - r + 34, cx + r - 34, cy + r - 34), fill=mix(bg, WHITE, 0.22))
    _center(img, p["img"], cx + p.get("dx", 0), cy + p.get("dy", 0), p.get("maxw", 560), p.get("maxh", 560))
    d = ImageDraw.Draw(img)
    # cover lines on the left
    y = p.get("lines_y", 520)
    for i, t in enumerate(p["feats"][:3]):
        d.text(P(60, y), f"{i + 1:02d}", font=f("Poppins-Bold.ttf", 30), fill=acc, anchor="lm")
        d.line(P(112, y, 150, y), fill=acc, width=3 * S)
        lines = t if isinstance(t, (list, tuple)) else [t]
        yy = y + 40
        for l in lines:
            d.text(P(60, yy), l, font=fit(d, l, "Poppins-Bold.ttf", 31, p.get("lines_w", 270)), fill=WHITE, anchor="lm"); yy += 38
        y = yy + 34
    # bottom white band: title + Bangla line
    d.rectangle(P(0, BAND, W0, H0), fill=WHITE)
    d.rectangle(P(0, BAND, W0, BAND + 10), fill=acc)
    ft, tl = wrap(d, p["title"], "Poppins-Bold.ttf", 46, 960, 1)
    d.text(P(60, BAND + 74), tl[0], font=ft, fill=ink, anchor="lm")
    if p.get("bn"):
        fb = _bn_fit(d, p["bn"], 34, 960)
        d.text(P(60, BAND + 146), p["bn"], font=fb, fill=bg, anchor="lm")
    d.text(P(60, H0 - 44), "Inbox us to order", font=f("Poppins-Medium.ttf", 24), fill=mix(WHITE, ink, 0.6), anchor="lm")
    d.text(P(W0 - 60, H0 - 44), "everydaycart.online", font=f("Poppins-Bold.ttf", 26), fill=ink, anchor="rm")
    # price sticker (flat circle with ring)
    sx, sy, sr = p.get("sx", 900), p.get("sy", 930), 118
    d.ellipse(P(sx - sr, sy - sr, sx + sr, sy + sr), fill=acc)
    d.ellipse(P(sx - sr + 10, sy - sr + 10, sx + sr - 10, sy + sr - 10), outline=ink, width=2 * S)
    d.text(P(sx, sy - 52), p.get("label", "ONLY"), font=f("Poppins-Bold.ttf", 20), fill=ink, anchor="mm")
    pt = tk(p["price"]); d.text(P(sx, sy - 6), pt, font=fit(d, pt, "Poppins-Bold.ttf", 46, 190), fill=ink, anchor="mm")
    if p.get("regular", 0) > p["price"]:
        rt = tk(p["regular"]); rfo = f("Poppins-Regular.ttf", 23); rw = d.textlength(rt, font=rfo) / S
        strike(d, sx - rw / 2, sy + 30, rt, rfo, mix(acc, ink, 0.6))
    # logo + tag last so nothing covers them
    logo_chip(img, 44, 44, 120); d = ImageDraw.Draw(img)
    _tag(img, d, p["tag"], acc, ink)
    return rf.finish(img, p["out"])


# ---------------- Template R: sticker sheet ----------------
def _sticker(img, cx, cy, text, fill, col, angle, size=28, pad=26, border=7, font="Poppins-Bold.ttf", bn=False):
    d0 = ImageDraw.Draw(img)
    ft = fbn(size) if bn else f(font, size)
    tw = d0.textlength(text, font=ft) / S; hh = size * 1.9
    w = tw + pad * 2 + border * 2; h = hh + border * 2
    def draw(L):
        dl = ImageDraw.Draw(L)
        dl.rounded_rectangle(P(0, 0, w, h), radius=h / 2 * S, fill=WHITE)
        dl.rounded_rectangle(P(border, border, w - border, h - border), radius=(h / 2 - border) * S, fill=fill)
        dl.text(P(w / 2, h / 2 + (2 if bn else 0)), text, font=ft, fill=col, anchor="mm")
    _layer(img, (cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2), draw, angle)


def _price_sticker(img, cx, cy, price, regular, fill, ink, angle, label="ONLY", w=270, h=170):
    def draw(L):
        dl = ImageDraw.Draw(L)
        dl.rounded_rectangle(P(0, 0, w, h), radius=34 * S, fill=WHITE)
        dl.rounded_rectangle(P(8, 8, w - 8, h - 8), radius=28 * S, fill=fill)
        dl.text(P(w / 2, 42), label, font=f("Poppins-Bold.ttf", 20), fill=mix(fill, ink, 0.75), anchor="mm")
        pt = tk(price); dl.text(P(w / 2, 88), pt, font=fit(dl, pt, "Poppins-Bold.ttf", 50, w - 40), fill=ink, anchor="mm")
        if regular and regular > price:
            rt = tk(regular); rfo = f("Poppins-Regular.ttf", 22); rw = dl.textlength(rt, font=rfo) / S
            strike(dl, w / 2 - rw / 2, 118, rt, rfo, mix(fill, ink, 0.55))
    _layer(img, (cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2), draw, angle)


def template_r(p):
    bg = p.get("bg", (255, 236, 214)); acc = p.get("acc", (240, 96, 70)); acc2 = p.get("acc2", (60, 90, 200))
    ink = p.get("ink", INK); disc = p.get("disc", mix(bg, acc, 0.22))
    img = Image.new("RGBA", (W, H), bg + (255,)); d = ImageDraw.Draw(img)
    dot = mix(bg, ink, 0.09)
    for yy in range(140, 1200, 44):
        for xx in range(30, W0, 44):
            d.ellipse(P(xx - 2.2, yy - 2.2, xx + 2.2, yy + 2.2), fill=dot)
    # headline
    if isinstance(p["head"], (list, tuple)):
        lines = list(p["head"]); ft = f("Poppins-Bold.ttf", 62)
        for l in lines: ft = fit(d, l, "Poppins-Bold.ttf", ft.size / S, 960)
    else:
        ft, lines = wrap(d, p["head"], "Poppins-Bold.ttf", 62, 960, 2)
    y = 150
    for i, l in enumerate(lines):
        tw = d.textlength(l, font=ft) / S
        if i == len(lines) - 1:   # marker highlight under the last line
            d.rounded_rectangle(P(52, y + ft.size / S * 0.55, 68 + tw, y + ft.size / S * 1.12), radius=8 * S, fill=mix(bg, acc, 0.35))
        d.text(P(60, y), l, font=ft, fill=ink); y += ft.size / S * 1.1
    items = p.get("items")
    if items:   # collection: [(img, name, price, regular, disc_colour)]
        n = len(items); slot = (W0 - 60) / n; cy = p.get("cy", 690); r = min(slot / 2 - 26, 240)
        for i, (pi, name, price, reg, dc) in enumerate(items):
            cx = 30 + slot * (i + 0.5)
            d.ellipse(P(cx - r - 10, cy - r - 10, cx + r + 10, cy + r + 10), fill=WHITE)
            d.ellipse(P(cx - r, cy - r, cx + r, cy + r), fill=dc)
            _center(img, pi, cx, cy, r * 1.75, r * 1.65 * p.get("scales", [1] * n)[i]); d = ImageDraw.Draw(img)
            d.text(P(cx, cy + r + 62), name, font=fit(d, name, "Poppins-Bold.ttf", 32, slot - 40), fill=ink, anchor="mm")
            _price_sticker(img, cx, cy + r + 170, price, reg, p.get("pfill", acc), WHITE if p.get("pwhite", True) else ink,
                           [-4, 4, -3, 3][i], label="ONLY", w=250, h=172)
        d = ImageDraw.Draw(img)
        for (sx, sy, t, ang, col) in p.get("stickers", []):
            _sticker(img, sx, sy, t, col, WHITE, ang, size=24)
    else:
        cx, cy, r = p.get("cx", 560), p.get("cy", 700), p.get("r", 300)
        d.ellipse(P(cx - r - 12, cy - r - 12, cx + r + 12, cy + r + 12), fill=WHITE)
        d.ellipse(P(cx - r, cy - r, cx + r, cy + r), fill=disc)
        _center(img, p["img"], cx + p.get("dx", 0), cy + p.get("dy", 0), p.get("maxw", 520), p.get("maxh", 540))
        cols = p.get("scol", [acc2, acc, ink])
        pos = p.get("spos", [(240, 470, -6), (850, 640, 5), (250, 930, -3)])
        for (sx, sy, ang), t, c in zip(pos, p["feats"][:3], cols):
            _sticker(img, sx, sy, t, c, WHITE, ang, size=p.get("fsize", 27))
        _price_sticker(img, p.get("px", 850), p.get("py", 950), p["price"], p.get("regular"), p.get("pfill", acc),
                       WHITE if p.get("pwhite", True) else ink, 6)
        d = ImageDraw.Draw(img)
        # title under the circle
        ft2, tl = wrap(d, p["title"], "Poppins-Bold.ttf", 40, 960, 1)
        d.text(P(W0 / 2, p.get("ty", 1100)), tl[0], font=ft2, fill=ink, anchor="mm")
    d = ImageDraw.Draw(img)
    # Bangla tape strip
    if p.get("bn"):
        ty = p.get("bny", 1176)
        fb = _bn_fit(d, p["bn"], 32, 860); bw = d.textlength(p["bn"], font=fb) / S
        def draw(L, bw=bw, fb=fb):
            dl = ImageDraw.Draw(L); w = bw + 80
            dl.rectangle(P(0, 0, w, 64), fill=p.get("tape", acc2))
            for k in range(0, 64, 16):
                dl.polygon([P(0, k), P(8, k + 8), P(0, k + 16)], fill=bg)
                dl.polygon([P(w, k), P(w - 8, k + 8), P(w, k + 16)], fill=bg)
            dl.text(P(w / 2, 34), p["bn"], font=fb, fill=WHITE, anchor="mm")
        _layer(img, (W0 / 2 - bw / 2 - 40, ty - 32, W0 / 2 + bw / 2 + 40, ty + 32), draw, p.get("tape_ang", -1.5))
        d = ImageDraw.Draw(img)
    # footer
    d.rectangle(P(0, H0 - 84, W0, H0), fill=ink)
    d.text(P(60, H0 - 42), "everydaycart.online", font=f("Poppins-Bold.ttf", 28), fill=WHITE, anchor="lm")
    d.text(P(W0 - 60, H0 - 42), "Inbox us to order", font=f("Poppins-Medium.ttf", 24), fill=mix(ink, WHITE, 0.75), anchor="rm")
    logo_chip(img, 44, 44, 120); d = ImageDraw.Draw(img)
    _tag(img, d, p["tag"], ink, WHITE)
    return rf.finish(img, p["out"])


TEMPLATES8 = {"Q": template_q, "R": template_r}
