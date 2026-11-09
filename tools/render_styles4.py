"""Style set 4: I big-word poster (giant tinted word behind the product, scalloped price stamp),
J ticket card (perforated ticket with product stage and spec stub). Flat, Poppins, small corner logo."""
import math
from PIL import Image, ImageDraw
import render_flat as rf
from render_flat import P, f, fit, wrap, tk, S, W, H, W0, H0, INK, MUTE, load_logo, check_icon


def logo_chip(img, x0, y0, width=140, fill=(255, 255, 255)):
    d = ImageDraw.Draw(img); lg = load_logo(width)
    w, h = lg.width / S, lg.height / S
    d.rounded_rectangle(P(x0, y0, x0 + w + 28, y0 + h + 22), radius=16 * S, fill=fill)
    img.alpha_composite(lg, (int((x0 + 14) * S), int((y0 + 11) * S)))


def mix(a, b, t): return tuple(int(round(a[i] * (1 - t) + b[i] * t)) for i in range(3))


def strike(d, x, y, text, font, col):
    w = d.textlength(text, font=font) / S; d.text(P(x, y), text, font=font, fill=col)
    hh = font.size / S; d.line(P(x - 2, y + hh * 0.62, x + w + 2, y + hh * 0.62), fill=col, width=2 * S)


def stamp(d, cx, cy, r, col, price, regular, label="ONLY"):
    """Flat scalloped price stamp."""
    n = 22
    for i in range(n):
        a = 2 * math.pi * i / n; x = cx + r * math.cos(a); y = cy + r * math.sin(a); rr = r * 0.17
        d.ellipse(P(x - rr, y - rr, x + rr, y + rr), fill=col)
    d.ellipse(P(cx - r, cy - r, cx + r, cy + r), fill=col)
    d.ellipse(P(cx - r + 12, cy - r + 12, cx + r - 12, cy + r - 12), outline=(255, 255, 255), width=2 * S)
    lf = f("Poppins-Medium.ttf", 21); lw = d.textlength(label, font=lf) / S
    has_old = regular and regular > price
    top = cy - (58 if has_old else 44)
    d.text(P(cx - lw / 2, top), label, font=lf, fill=(255, 240, 232))
    pt = tk(price); pf = fit(d, pt, "Poppins-Bold.ttf", 44, r * 1.6); pw = d.textlength(pt, font=pf) / S
    d.text(P(cx - pw / 2, top + 26), pt, font=pf, fill="white")
    if has_old:
        of = f("Poppins-Regular.ttf", 23); o = tk(regular); ow = d.textlength(o, font=of) / S
        strike(d, cx - ow / 2, top + 84, o, of, (255, 230, 222))


# ---------------- Template I: big-word poster ----------------
def template_i(p):
    bg = p.get("bg", (238, 234, 226)); col = p.get("col", (60, 80, 120)); ink = p.get("ink", INK)
    img = Image.new("RGBA", (W, H), bg + (255,)); d = ImageDraw.Draw(img)
    # giant word behind the product
    word = p["word"]; wc = p.get("wordc", mix(bg, col, 0.16))
    wf = fit(d, word, "Poppins-Bold.ttf", 250, 960); ww = d.textlength(word, font=wf) / S
    bb = d.textbbox((0, 0), word, font=wf); wh = (bb[3] - bb[1]) / S; oy = bb[1] / S
    wy = p.get("wordy", 262); d.text(P(540 - ww / 2, wy - wh / 2 - oy), word, font=wf, fill=wc)
    # thin frame line
    d.rounded_rectangle(P(34, 34, W0 - 34, H0 - 150), radius=30 * S, outline=mix(bg, col, 0.35), width=2 * S)
    logo_chip(img, 64, 64, 140); d = ImageDraw.Draw(img)
    tf = f("Poppins-Medium.ttf", 22); tt = p["tag"]; tw = d.textlength(tt, font=tf) / S
    d.rounded_rectangle(P(W0 - 64 - tw - 44, 70, W0 - 64, 118), radius=24 * S, fill=col)
    d.text(P(W0 - 64 - tw - 22, 79), tt, font=tf, fill="white")
    img = rf.place(img, p["img"], p.get("cx", 540), p.get("cy", 590), p.get("maxw", 560), p.get("maxh", 560)); d = ImageDraw.Draw(img)
    stamp(d, 870, 800, 112, p.get("stampc", col), p["price"], p.get("regular", 0), p.get("label", "ONLY"))
    # title + features
    ft, lines = wrap(d, p["title"], "Poppins-Bold.ttf", 60, 690, 2)
    y = 896 if len(lines) == 1 else 846
    for l in lines: d.text(P(72, y), l, font=ft, fill=ink); y += ft.size / S * 1.2
    sf = fit(d, p["sub"], "Poppins-Regular.ttf", 28, 690); d.text(P(72, y + 10), p["sub"], font=sf, fill=MUTE)
    x, yy = 72, 1048
    chip = p.get("chip", mix(bg, (255, 255, 255), 0.7))
    for t in p["feats"][:4]:
        cf = f("Poppins-Medium.ttf", 25); cw = d.textlength(t, font=cf) / S
        if x + cw + 70 > W0 - 72: break
        d.rounded_rectangle(P(x, yy, x + cw + 62, yy + 58), radius=29 * S, fill=chip)
        d.ellipse(P(x + 18, yy + 23, x + 30, yy + 35), fill=col)
        d.text(P(x + 40, yy + 12), t, font=cf, fill=ink); x += cw + 76
    # footer band
    d.rectangle(P(0, H0 - 116, W0, H0), fill=col)
    uf = f("Poppins-Bold.ttf", 30); d.text(P(72, H0 - 80), "everydaycart.online", font=uf, fill="white")
    bf = f("Poppins-Medium.ttf", 27); bt = "Inbox us to order"; bw = d.textlength(bt, font=bf) / S
    d.rounded_rectangle(P(W0 - 72 - bw - 52, H0 - 90, W0 - 72, H0 - 30), radius=30 * S, fill="white")
    d.text(P(W0 - 72 - bw - 26, H0 - 79), bt, font=bf, fill=col)
    return rf.finish(img, p["out"])


# ---------------- Template J: ticket card ----------------
def template_j(p):
    bg = p.get("bg", (44, 62, 108)); stage = p.get("stage", (232, 238, 248)); acc = p.get("acc", (226, 120, 80))
    img = Image.new("RGBA", (W, H), bg + (255,))
    # subtle flat dots on background
    d = ImageDraw.Draw(img); dot = mix(bg, (255, 255, 255), 0.08)
    for yy in range(30, H0, 44):
        for xx in range(22 if (yy // 44) % 2 else 44, W0, 44): d.ellipse(P(xx - 3, yy - 3, xx + 3, yy + 3), fill=dot)
    X0, Y0, X1, Y1, PY = 60, 60, W0 - 60, H0 - 60, 830
    d.rounded_rectangle(P(X0, Y0, X1, Y1), radius=34 * S, fill=(255, 255, 255))
    d.ellipse(P(X0 - 34, PY - 34, X0 + 34, PY + 34), fill=bg); d.ellipse(P(X1 - 34, PY - 34, X1 + 34, PY + 34), fill=bg)
    for xx in range(X0 + 50, X1 - 50, 28): d.line(P(xx, PY, xx + 14, PY), fill=(206, 206, 210), width=3 * S)
    # product stage
    d.rounded_rectangle(P(X0 + 30, Y0 + 30, X1 - 30, PY - 40), radius=26 * S, fill=stage)
    ring = mix(stage, bg, 0.10)
    for r in (300, 230): d.ellipse(P(540 - r, 450 - r, 540 + r, 450 + r), outline=ring, width=3 * S)
    d.ellipse(P(540 - 160, 450 - 160, 540 + 160, 450 + 160), fill=mix(stage, (255, 255, 255), 0.55))
    img = rf.place(img, p["img"], 540, p.get("cy", 455), p.get("maxw", 520), p.get("maxh", 560)); d = ImageDraw.Draw(img)
    logo_chip(img, X0 + 54, Y0 + 52, 130); d = ImageDraw.Draw(img)
    tf = f("Poppins-Medium.ttf", 22); tt = p["tag"]; tw = d.textlength(tt, font=tf) / S
    d.rounded_rectangle(P(X1 - 54 - tw - 44, Y0 + 56, X1 - 54, Y0 + 104), radius=24 * S, fill=bg)
    d.text(P(X1 - 54 - tw - 22, Y0 + 65), tt, font=tf, fill="white")
    # stub: title, features, price
    ft, lines = wrap(d, p["title"], "Poppins-Bold.ttf", 52, 600, 2)
    y = 872
    for l in lines: d.text(P(110, y), l, font=ft, fill=INK); y += ft.size / S * 1.15
    y += 12
    step = min(52, (1180 - y) / 4)
    for t in p["feats"][:4]:
        check_icon(d, 126, y + 17, 15, acc, (255, 255, 255))
        d.text(P(156, y), t, font=fit(d, t, "Poppins-Medium.ttf", 25, 470), fill=INK); y += step
    # price column
    d.line(P(700, 880, 700, 1150), fill=(226, 226, 230), width=2 * S)
    lf = f("Poppins-Medium.ttf", 22); d.text(P(740, 900), p.get("label", "PRICE"), font=lf, fill=MUTE)
    pt = tk(p["price"]); pf = fit(d, pt, "Poppins-Bold.ttf", 66, 250); d.text(P(740, 930), pt, font=pf, fill=bg)
    if p.get("regular", 0) > p["price"]:
        of = f("Poppins-Regular.ttf", 28); strike(d, 742, 1022, tk(p["regular"]), of, MUTE)
    bf = f("Poppins-Bold.ttf", 25); bt = "Inbox to order"; bw = d.textlength(bt, font=bf) / S
    d.rounded_rectangle(P(740, 1082, 740 + bw + 48, 1140), radius=29 * S, fill=acc)
    d.text(P(764, 1094), bt, font=bf, fill="white")
    uf = f("Poppins-Medium.ttf", 25); u = "everydaycart.online"; uw = d.textlength(u, font=uf) / S
    d.line(P(110, 1196, X1 - 50, 1196), fill=(236, 236, 240), width=2 * S)
    d.text(P(540 - uw / 2, 1216), u, font=uf, fill=MUTE)
    return rf.finish(img, p["out"])


TEMPLATES4 = {"I": template_i, "J": template_j}
