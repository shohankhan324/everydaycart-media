"""Style set 6 (added 11 Nov 2026): M orbit poster (product on flat concentric rings, round price sticker,
Bangla pill, white bottom card with feature chips), N checklist note (graph-paper background, tilted photo card,
sticky-note price, ticked checklist, dark footer bar). Flat only, Poppins + Hind Siliguri, small logo chip in a corner."""
import os
from PIL import Image, ImageDraw, ImageFont
import render_flat as rf
from render_flat import P, f, fit, wrap, tk, S, W, H, W0, H0, INK, MUTE, check_icon
from render_styles4 import logo_chip, mix, strike
from render_styles5 import _place_many

BN = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets", "fonts", "hind-siliguri-bengali-%d-normal.woff")
WHITE = (255, 255, 255)


def fbn(size, w=700):
    return ImageFont.truetype(BN % w, int(size * S), layout_engine=ImageFont.Layout.RAQM)


def bn_text(d, x, y, text, size, col, anchor="la", w=700):
    ft = fbn(size, w); d.text(P(x, y), text, font=ft, fill=col, anchor=anchor); return d.textlength(text, font=ft) / S


def _layer(img, box, draw_fn, angle):
    """Draw onto a transparent layer the size of box, rotate it and paste centred on the box (flat, no shadow blur)."""
    x0, y0, x1, y1 = box; w, h = x1 - x0, y1 - y0
    L = Image.new("RGBA", P(w, h), (0, 0, 0, 0)); draw_fn(L)
    R = L.rotate(angle, expand=True, resample=Image.BICUBIC)
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
    img.alpha_composite(R, (int(cx * S - R.width / 2), int(cy * S - R.height / 2)))


# ---------------- Template M: orbit poster ----------------
def template_m(p):
    bg = p.get("bg", (22, 84, 96)); acc = p.get("acc", (255, 186, 60)); hl = p.get("hl", acc); ink = p.get("ink", INK)
    img = Image.new("RGBA", (W, H), bg + (255,)); d = ImageDraw.Draw(img)
    # tiny star sparkles
    for (sx, sy, r) in [(120, 300, 5), (960, 620, 6), (90, 820, 4), (980, 210, 4), (200, 160, 3)]:
        d.ellipse(P(sx - r, sy - r, sx + r, sy + r), fill=mix(bg, WHITE, 0.35))
    logo_chip(img, 44, 44, 120); d = ImageDraw.Draw(img)
    tf = f("Poppins-Medium.ttf", 21); tt = p["tag"]; tw = d.textlength(tt, font=tf) / S
    d.rounded_rectangle(P(W0 - 44 - tw - 42, 52, W0 - 44, 98), radius=23 * S, outline=WHITE, width=2 * S)
    d.text(P(W0 - 44 - tw - 21, 59), tt, font=tf, fill=WHITE)
    # rings
    cx, cy = p.get("cx", 540), p.get("cy", 560)
    for r, t in ((390, 0.10), (320, 0.20), (250, 0.34)):
        d.ellipse(P(cx - r, cy - r, cx + r, cy + r), fill=mix(bg, WHITE, t))
    d.ellipse(P(cx - 455, cy - 455, cx + 455, cy + 455), outline=mix(bg, WHITE, 0.18), width=2 * S)
    img = _place_many(img, p["img"], cx, cy + 10, p.get("maxw", 520), p.get("maxh", 560), p.get("gap", 30)); d = ImageDraw.Draw(img)
    # price sticker
    px, py, pr = p.get("px", 860), p.get("py", 290), 128
    d.ellipse(P(px - pr - 8, py - pr - 8, px + pr + 8, py + pr + 8), fill=WHITE)
    d.ellipse(P(px - pr, py - pr, px + pr, py + pr), fill=acc)
    lab = p.get("label", "ONLY"); lf = f("Poppins-Medium.ttf", 22)
    d.text(P(px, py - 58), lab, font=lf, fill=p.get("acc_ink", ink), anchor="mm")
    pt = tk(p["price"]); pf = fit(d, pt, "Poppins-Bold.ttf", 52, 210)
    d.text(P(px, py - 6), pt, font=pf, fill=p.get("acc_ink", ink), anchor="mm")
    if p.get("regular", 0) > p["price"]:
        rt = tk(p["regular"]); rf_ = f("Poppins-Regular.ttf", 24); rw = d.textlength(rt, font=rf_) / S
        strike(d, px - rw / 2, py + 34, rt, rf_, mix(acc, ink, 0.55))
    # Bangla pill
    if p.get("bn"):
        bw = d.textlength(p["bn"], font=fbn(34)) / S
        by = p.get("bny", 948)
        d.rounded_rectangle(P(cx - bw / 2 - 34, by, cx + bw / 2 + 34, by + 66), radius=33 * S, fill=hl)
        bn_text(d, cx, by + 33, p["bn"], 34, p.get("bn_ink", ink), anchor="mm")
    # bottom card
    CY = 1040
    d.rounded_rectangle(P(34, CY, W0 - 34, H0 - 34), radius=36 * S, fill=WHITE)
    ft, lines = wrap(d, p["title"], "Poppins-Bold.ttf", 44, 940, 1)
    d.text(P(W0 / 2, CY + 56), lines[0], font=ft, fill=ink, anchor="mm")
    chf = f("Poppins-Medium.ttf", 23); feats = p["feats"][:3]
    ws = [d.textlength(t, font=chf) / S + 58 for t in feats]; gap = 14
    while sum(ws) + gap * (len(ws) - 1) > 960 and chf.size > 30:
        chf = f("Poppins-Medium.ttf", chf.size / S - 1); ws = [d.textlength(t, font=chf) / S + 58 for t in feats]
    x = W0 / 2 - (sum(ws) + gap * (len(ws) - 1)) / 2; yy = CY + 104
    for t, w_ in zip(feats, ws):
        d.rounded_rectangle(P(x, yy, x + w_, yy + 52), radius=26 * S, fill=mix(bg, WHITE, 0.88))
        check_icon(d, x + 26, yy + 26, 12, bg, WHITE)
        d.text(P(x + 46, yy + 26), t, font=chf, fill=ink, anchor="lm"); x += w_ + gap
    d.line(P(74, H0 - 112, W0 - 74, H0 - 112), fill=(236, 234, 232), width=2 * S)
    uf = f("Poppins-Bold.ttf", 28); d.text(P(74, H0 - 74), "everydaycart.online", font=uf, fill=bg, anchor="lm")
    nf = f("Poppins-Bold.ttf", 24); nt = "Inbox us to order"; nw = d.textlength(nt, font=nf) / S
    d.rounded_rectangle(P(W0 - 74 - nw - 44, H0 - 100, W0 - 74, H0 - 48), radius=26 * S, fill=acc)
    d.text(P(W0 - 74 - nw - 22, H0 - 74), nt, font=nf, fill=p.get("acc_ink", ink), anchor="lm")
    return rf.finish(img, p["out"])


# ---------------- Template N: checklist note ----------------
def template_n(p):
    paper = p.get("paper", (250, 247, 240)); grid = p.get("grid", (232, 228, 218)); card = p.get("card", (120, 170, 220))
    note = p.get("note", (255, 214, 92)); acc = p.get("acc", (226, 84, 70)); dark = p.get("dark", (34, 40, 56)); ink = p.get("ink", INK)
    img = Image.new("RGBA", (W, H), paper + (255,)); d = ImageDraw.Draw(img)
    for x in range(0, W0, 45): d.line(P(x, 0, x, H0), fill=grid, width=S)
    for y in range(0, H0, 45): d.line(P(0, y, W0, y), fill=grid, width=S)
    logo_chip(img, 40, 40, 120); d = ImageDraw.Draw(img)
    # tilted photo card
    CB = (58, 170, 640, 900)
    def draw_card(L):
        dd = ImageDraw.Draw(L); w, h = L.width / S, L.height / S
        dd.rounded_rectangle(P(0, 0, w, h), radius=26 * S, fill=WHITE)
        dd.rounded_rectangle(P(22, 22, w - 22, h - 22), radius=18 * S, fill=card)
        for i in range(5):
            r = 60 + i * 70; dd.ellipse(P(w / 2 - r, h / 2 - r, w / 2 + r, h / 2 + r), outline=mix(card, WHITE, 0.22), width=2 * S)
    _layer(img, CB, draw_card, p.get("tilt", 3))
    # tape strip
    def draw_tape(L):
        ImageDraw.Draw(L).rectangle(P(0, 0, L.width / S, L.height / S), fill=mix(note, WHITE, 0.45) + (215,))
    _layer(img, (270, 136, 430, 184), draw_tape, -6)
    img = _place_many(img, p["img"], (CB[0] + CB[2]) / 2, (CB[1] + CB[3]) / 2 + 6, p.get("maxw", 470), p.get("maxh", 520), p.get("gap", 28))
    d = ImageDraw.Draw(img)
    # sticky-note price
    NB = (676, 200, 1026, 520)
    def draw_note(L):
        dd = ImageDraw.Draw(L); w, h = L.width / S, L.height / S
        dd.rectangle(P(0, 0, w, h), fill=note)
        dd.polygon([P(w - 56, h), P(w, h - 56), P(w, h)], fill=paper)
        dd.polygon([P(w - 56, h), P(w, h - 56), P(w - 56, h - 56)], fill=mix(note, dark, 0.18))
        dd.text(P(34, 40), p.get("label", "ONLY"), font=f("Poppins-Medium.ttf", 26), fill=mix(note, dark, 0.6))
        pt = tk(p["price"]); pf = fit(dd, pt, "Poppins-Bold.ttf", 64, w - 68)
        dd.text(P(34, 80), pt, font=pf, fill=dark)
        if p.get("regular", 0) > p["price"]:
            strike(dd, 36, 180, tk(p["regular"]), f("Poppins-Regular.ttf", 30), mix(note, dark, 0.55))
        cf = f("Poppins-Bold.ttf", 23); ct = "Inbox to order"; cw = dd.textlength(ct, font=cf) / S
        dd.rounded_rectangle(P(34, h - 92, 34 + cw + 40, h - 42), radius=25 * S, fill=dark)
        dd.text(P(54, h - 67), ct, font=cf, fill=WHITE, anchor="lm")
    _layer(img, NB, draw_note, p.get("note_tilt", -4))
    d = ImageDraw.Draw(img)
    # tag + Bangla line under note
    tf = f("Poppins-Bold.ttf", 22); tt = p["tag"]; tw = d.textlength(tt, font=tf) / S
    d.rounded_rectangle(P(690, 584, 690 + tw + 40, 630), radius=10 * S, fill=acc)
    d.text(P(710, 607), tt, font=tf, fill=WHITE, anchor="lm")
    if p.get("bn"):
        bf_, y = p["bn"], 660
        lines = bf_ if isinstance(bf_, (list, tuple)) else [bf_]
        for l in lines:
            ft = fbn(p.get("bn_size", 34))
            while d.textlength(l, font=ft) / S > 330: ft = fbn(ft.size / S - 1)
            d.text(P(690, y), l, font=ft, fill=dark); y += ft.size / S * 1.45
    # title + checklist
    ft, lines = wrap(d, p["title"], "Poppins-Bold.ttf", 54, 960, 2)
    y = 985
    for l in lines: d.text(P(60, y), l, font=ft, fill=dark); y += ft.size / S * 1.12
    d.rectangle(P(60, y + 20, 200, y + 28), fill=acc)
    y += 52
    feats = p["feats"][:4]; colw = 480
    for i, t in enumerate(feats):
        x = 60 + (i % 2) * colw; yy = y + (i // 2) * 70
        d.rounded_rectangle(P(x, yy, x + 36, yy + 36), radius=8 * S, outline=dark, width=3 * S)
        d.line([P(x + 8, yy + 18), P(x + 16, yy + 27), P(x + 40, yy - 2)], fill=acc, width=5 * S, joint="curve")
        d.text(P(x + 54, yy + 18), t, font=fit(d, t, "Poppins-Medium.ttf", 29, colw - 70), fill=ink, anchor="lm")
    # footer bar
    d.rectangle(P(0, H0 - 96, W0, H0), fill=dark)
    uf = f("Poppins-Bold.ttf", 30); d.text(P(60, H0 - 48), "everydaycart.online", font=uf, fill=WHITE, anchor="lm")
    nf = f("Poppins-Medium.ttf", 24); nt = "Limited stock available"; nw = d.textlength(nt, font=nf) / S
    d.ellipse(P(W0 - 60 - nw - 26, H0 - 55, W0 - 60 - nw - 12, H0 - 41), fill=note)
    d.text(P(W0 - 60 - nw, H0 - 48), nt, font=nf, fill=mix(dark, WHITE, 0.75), anchor="lm")
    return rf.finish(img, p["out"])


TEMPLATES6 = {"M": template_m, "N": template_n}
