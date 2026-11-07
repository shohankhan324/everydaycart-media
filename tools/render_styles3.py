"""Style set 3: G slanted colour block, H framed label card. Flat, Poppins, small corner logo, brand palette."""
from PIL import Image, ImageDraw
import render_flat as rf
from render_flat import P, f, fit, wrap, tk, S, W, H, W0, H0, SAGE, SAGE_L, ROSE, INK, MUTE, CREAM, load_logo


def logo_chip(img, x1, y0, width=150, fill=(255, 255, 255)):
    d = ImageDraw.Draw(img); lg = load_logo(width)
    w, h = lg.width / S, lg.height / S
    d.rounded_rectangle(P(x1 - w - 28, y0, x1, y0 + h + 22), radius=16 * S, fill=fill)
    img.alpha_composite(lg, (int((x1 - w - 14) * S), int((y0 + 11) * S)))


# ---------------- Template G: slanted colour block ----------------
def template_g(p):
    col = p.get("col", SAGE); bg = p.get("bg", (255, 255, 255)); ink_top = p.get("ink_top", (255, 255, 255))
    img = Image.new("RGBA", (W, H), bg + (255,)); d = ImageDraw.Draw(img)
    d.polygon([P(0, 0), P(W0, 0), P(W0, 690), P(0, 860)], fill=col)
    d.ellipse(P(560, 300, 1000, 740), fill=p.get("disc", (255, 255, 255)))
    logo_chip(img, W0 - 48, 44); d = ImageDraw.Draw(img)
    d.text(P(64, 64), p["tag"], font=f("Poppins-Bold.ttf", 24), fill=p.get("tagc", (255, 236, 200)))
    ft, lines = wrap(d, p["title"], "Poppins-Bold.ttf", 68, 520, 3)
    y = 120
    for l in lines: d.text(P(64, y), l, font=ft, fill=ink_top); y += ft.size / S * 1.08
    sf = fit(d, p["sub"], "Poppins-Regular.ttf", 28, 500); d.text(P(64, y + 16), p["sub"], font=sf, fill=p.get("subc", (236, 240, 232)))
    img = rf.place(img, p["img"], 780, 540, p.get("maxw", 400), p.get("maxh", 470)); d = ImageDraw.Draw(img)
    # features as a row of outlined pills
    x, yy = 64, 930
    for t in p["feats"][:4]:
        tf = f("Poppins-Medium.ttf", 26); tw = d.textlength(t, font=tf) / S
        if x + tw + 48 > W0 - 64: x = 64; yy += 76
        d.rounded_rectangle(P(x, yy, x + tw + 48, yy + 60), radius=30 * S, outline=col, width=3 * S)
        d.text(P(x + 24, yy + 12), t, font=tf, fill=INK); x += tw + 64
    # price block
    pf = f("Poppins-Bold.ttf", 84); pt = tk(p["price"])
    if p.get("label"): d.text(P(64, 1108), p["label"], font=f("Poppins-Medium.ttf", 26), fill=MUTE)
    d.text(P(64, 1130), pt, font=pf, fill=p.get("pricec", ROSE))
    if p.get("regular", 0) > p["price"]:
        px = 64 + d.textlength(pt, font=pf) / S + 24; of = f("Poppins-Regular.ttf", 32); o = tk(p["regular"])
        ow = d.textlength(o, font=of) / S; d.text(P(px, 1182), o, font=of, fill=MUTE)
        d.line(P(px - 2, 1203, px + ow + 2, 1203), fill=MUTE, width=3 * S)
    bf = f("Poppins-Bold.ttf", 28); bt = "Inbox to order"; bw = d.textlength(bt, font=bf) / S
    d.rounded_rectangle(P(W0 - 64 - bw - 64, 1150, W0 - 64, 1222), radius=36 * S, fill=col)
    d.text(P(W0 - 64 - bw - 32, 1166), bt, font=bf, fill="white")
    d.text(P(64, 1268), "everydaycart.online", font=f("Poppins-Medium.ttf", 26), fill=MUTE)
    return rf.finish(img, p["out"])


# ---------------- Template H: framed label card ----------------
def template_h(p):
    bg = p.get("bg", (238, 232, 224)); edge = p.get("edge", SAGE); acc = p.get("acc", ROSE)
    img = Image.new("RGBA", (W, H), bg + (255,))
    img = rf.card_shadow(img, (70, 70, W0 - 70, H0 - 150), 36, alpha=34, blur=20, dy=10); d = ImageDraw.Draw(img)
    d.rounded_rectangle(P(70, 70, W0 - 70, H0 - 150), radius=36 * S, fill=(255, 255, 255))
    d.rounded_rectangle(P(92, 92, W0 - 92, H0 - 172), radius=26 * S, outline=edge, width=2 * S)
    d.ellipse(P(235, 175, 845, 785), fill=p.get("halo", (246, 240, 234)))
    img = rf.place(img, p["img"], 540, 470, p.get("maxw", 440) * 1.3, p.get("maxh", 440) * 1.3); d = ImageDraw.Draw(img)
    tf = f("Poppins-Medium.ttf", 22); tt = p["tag"]; tw = d.textlength(tt, font=tf) / S
    d.text(P(540 - tw / 2, 130), tt, font=tf, fill=edge)
    ft, lines = wrap(d, p["title"], "Poppins-Bold.ttf", 58, 800, 2); y = 840 if len(lines) == 1 else 815
    for l in lines:
        lw = d.textlength(l, font=ft) / S; d.text(P(540 - lw / 2, y), l, font=ft, fill=INK); y += ft.size / S * 1.12
    d.line(P(440, y + 18, 640, y + 18), fill=edge, width=3 * S)
    fl = "  •  ".join(p["feats"][:3]); ff = fit(d, fl, "Poppins-Regular.ttf", 28, 820); fw = d.textlength(fl, font=ff) / S
    d.text(P(540 - fw / 2, y + 44), fl, font=ff, fill=MUTE)
    it = "Inbox us to order"; itf = f("Poppins-Medium.ttf", 26); iw = d.textlength(it, font=itf) / S
    d.rounded_rectangle(P(540 - iw / 2 - 30, y + 110, 540 + iw / 2 + 30, y + 168), radius=29 * S, outline=edge, width=2 * S)
    d.text(P(540 - iw / 2, y + 122), it, font=itf, fill=edge)
    # price badge overlapping the card's top right corner
    pr = tk(p["price"]); pf = fit(d, pr, "Poppins-Bold.ttf", 46, 200)
    d.ellipse(P(800, 40, 1040, 280), fill=acc)
    pw = d.textlength(pr, font=pf) / S; d.text(P(920 - pw / 2, 130), pr, font=pf, fill="white")
    lab = p.get("label", "ONLY"); lf = f("Poppins-Medium.ttf", 22); lw = d.textlength(lab, font=lf) / S
    d.text(P(920 - lw / 2, 96), lab, font=lf, fill=(255, 236, 230))
    if p.get("regular", 0) > p["price"]:
        of = f("Poppins-Regular.ttf", 24); o = tk(p["regular"]); ow = d.textlength(o, font=of) / S
        d.text(P(920 - ow / 2, 192), o, font=of, fill=(255, 236, 230))
        d.line(P(918 - ow / 2, 208, 922 + ow / 2, 208), fill=(255, 236, 230), width=2 * S)
    # footer under the card
    logo_chip(img, 330, H0 - 116, 150, fill=(255, 255, 255)); d = ImageDraw.Draw(img)
    bf = f("Poppins-Bold.ttf", 28); bt = "Order: everydaycart.online"; bw = d.textlength(bt, font=bf) / S
    d.rounded_rectangle(P(W0 - 70 - bw - 60, H0 - 112, W0 - 70, H0 - 44), radius=34 * S, fill=edge)
    d.text(P(W0 - 70 - bw - 30, H0 - 98), bt, font=bf, fill="white")
    return rf.finish(img, p["out"])


TEMPLATES3 = {"G": template_g, "H": template_h}
