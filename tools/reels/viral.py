"""'Wear Your Vibe' gadget Reel: flat silhouettes of women and men wearing in-stock Oraimo / Awei gadgets."""
import io, os, sys, math, subprocess
import numpy as np
import cairosvg
from PIL import Image, ImageDraw, ImageFilter
sys.path.insert(0, "/home/claude/everydaycart-media/tools"); sys.path.insert(0, "/home/claude/viral")
from render_video import f, clamp, ease, back, product_sprite, pill_sprite
from render_flat import load_logo
from shapes import WOMAN, MAN, ARM
from drive import drive, B, SR
from scipy.io import wavfile

W, H, FPS = 1080, 1920, 30
HQ = "/home/claude/everydaycart-media/tools/cutouts/hq/"
OUT = "/home/claude/viral/out/"; os.makedirs(OUT, exist_ok=True)
DARK = (22, 23, 28); WHITE = (255, 255, 255)

# ---------- silhouettes + accessories (SVG in the 1000x1200 box) ----------
def svg_img(body, scale, mirror=False):
    t = 'transform="translate(1000,0) scale(-1,1)"' if mirror else ""
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{int(1000*scale)}" height="{int(1200*scale)}" '
           f'viewBox="0 0 1000 1200"><g {t}>{body}</g></svg>')
    return Image.open(io.BytesIO(cairosvg.svg2png(bytestring=svg.encode()))).convert("RGBA")

def bud(x, y, col, edge, rot=-14):
    return (f'<g transform="translate({x},{y}) rotate({rot})">'
            f'<rect x="-12" y="0" width="24" height="80" rx="12" fill="{col}" stroke="{edge}" stroke-width="3"/>'
            f'<ellipse cx="0" cy="0" rx="30" ry="27" fill="{col}" stroke="{edge}" stroke-width="3"/>'
            f'<ellipse cx="8" cy="-8" rx="9" ry="6" fill="#ffffff" opacity="0.35"/></g>')

EAR = {"woman": (506, 476), "man": (526, 494)}
NECKBAND = ('<path d="M 418 842 C 470 905, 580 935, 668 922" fill="none" stroke="#17181c" stroke-width="30" stroke-linecap="round"/>'
            '<path d="M 640 930 L 700 1075" stroke="#17181c" stroke-width="46" stroke-linecap="round"/>'
            '<path d="M 652 935 C 600 770, 566 620, 532 530" fill="none" stroke="#17181c" stroke-width="7" stroke-linecap="round"/>'
            '<circle cx="700" cy="1075" r="6" fill="#4a4d55"/>')

# ---------- scene data (in-stock gadgets only) ----------
SCENES = [
    dict(who="woman", sil=DARK, bg=(255, 104, 92), ink=WHITE, acc="bud", acc_col="#f4efe6", acc_edge="#c9c2b6",
         img="12.png", tag="EARBUDS", title=["Oraimo", "SpaceBuds Neo+"], price=1940, regular=2189, feat="Sound360  •  30H Battery"),
    dict(who="arm", sil=(255, 236, 214), bg=(46, 98, 255), ink=WHITE, acc="watch",
         img="02.png", tag="SMART WATCH", title=["Oraimo", "Watch 5 Lite"], price=1650, regular=1870, feat="Bluetooth Calling  •  IP68"),
    dict(who="man", sil=WHITE, bg=(255, 196, 46), ink=DARK, acc="neckband",
         img="04.png", tag="NECKBAND", title=["Oraimo", "Necklace Lite"], price=1300, regular=1485, feat="30H Playtime  •  ENC Calls"),
    dict(who="woman", mirror=True, sil=WHITE, bg=(132, 84, 255), ink=WHITE, acc="bud", acc_col="#17181c", acc_edge="#17181c",
         img="13.png", tag="EARBUDS", title=["Oraimo", "SpaceBuds Lite"], price=1310, regular=1496, feat="Spatial Audio  •  40H Battery"),
    dict(who="man", sil=WHITE, bg=(18, 184, 134), ink=WHITE, acc="bud", acc_col="#17181c", acc_edge="#17181c",
         img="10.png", tag="EARBUDS", title=["Awei", "T108"], price=950, regular=1199, feat="13mm Drivers  •  ENC Calls"),
]
INTRO_D = 4 * B; SCENE_D = 5 * B; END_D = 7 * B

LOGO = load_logo(150); LOGO = LOGO.resize((150, int(LOGO.height * 150 / LOGO.width)), Image.LANCZOS)
def logo_card():
    pad = 16; c = Image.new("RGBA", (LOGO.width + 2 * pad, LOGO.height + 2 * pad), (0, 0, 0, 0))
    ImageDraw.Draw(c).rounded_rectangle((0, 0, c.width - 1, c.height - 1), radius=22, fill=(255, 255, 255, 240))
    c.alpha_composite(LOGO, (pad, pad)); return c
LOGO_CARD = logo_card()

def rgba(c, a=255): return tuple(c) + (a,)
def hexc(c): return "#%02x%02x%02x" % tuple(c)

def put(img, spr, cx, cy, scale=1.0, a=1.0, rot=0):
    if a <= 0.01 or scale <= 0.01: return
    s = spr
    if abs(scale - 1) > 1e-3: s = s.resize((max(1, int(s.width * scale)), max(1, int(s.height * scale))), Image.BICUBIC)
    if rot: s = s.rotate(rot, Image.BICUBIC, expand=True)
    if a < 0.999: s = s.copy(); s.putalpha(s.split()[3].point(lambda v: int(v * a)))
    img.alpha_composite(s, (int(cx - s.width / 2), int(cy - s.height / 2)))

def text_spr(text, font, col):
    w = int(font.getlength(text)) + 8; h = int(font.size * 1.4)
    s = Image.new("RGBA", (w, h), (0, 0, 0, 0)); ImageDraw.Draw(s).text((4, 0), text, font=font, fill=col); return s

def price_spr(price, regular, ink, bg):
    big = f("Poppins-Bold.ttf", 104); sm = f("Poppins-Medium.ttf", 44)
    p = f"Tk {price:,}"; r = f"Tk {regular:,}"
    w = int(big.getlength(p) + sm.getlength(r) + 40) + 10; h = 150
    s = Image.new("RGBA", (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(s)
    d.text((0, 0), p, font=big, fill=rgba(ink))
    x = big.getlength(p) + 30; d.text((x, 52), r, font=sm, fill=rgba(ink, 170))
    d.line((x - 4, 82, x + sm.getlength(r) + 4, 82), fill=rgba(ink, 200), width=5)
    return s

def burst(img, cx, cy, k, col):
    if not 0 < k < 1: return
    ov = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(ov)
    r = 40 + 120 * ease(k); a = int(255 * (1 - k))
    d.ellipse((cx - r, cy - r, cx + r, cy + r), outline=rgba(col, a), width=max(2, int(10 * (1 - k))))
    for i in range(8):
        ang = i * math.pi / 4 + 0.3; r1 = r * 1.1; r2 = r * 1.1 + 40 * (1 - k)
        d.line((cx + r1 * math.cos(ang), cy + r1 * math.sin(ang), cx + r2 * math.cos(ang), cy + r2 * math.sin(ang)), fill=rgba(col, a), width=8)
    img.alpha_composite(ov)

# ---------- build scene assets ----------
def build(sc):
    mir = sc.get("mirror", False); who = sc["who"]
    if who == "arm":
        # forearm across the body in a "checking the watch" pose: watch upright, strap wraps around the wrist
        scale = 1.2
        body = (f'<g transform="rotate(90 500 600)"><path d="{ARM}" fill="{hexc(sc["sil"])}"/></g>'
                '<rect x="-40" y="470" width="190" height="290" rx="26" fill="#1d1f24"/>')
        arm = svg_img(body, scale)
        sc["sil_img"] = arm
        sc["sil_pos"] = (900 - 862 * scale, 1290 - 610 * scale)
        src = Image.open(HQ + "02.png").convert("RGBA")
        keep = Image.new("L", src.size, 0); dk = ImageDraw.Draw(keep)
        dk.rounded_rectangle((34, 116, 446, 776), radius=70, fill=255); dk.ellipse((425, 375, 505, 465), fill=255)
        from PIL import ImageChops
        src.putalpha(ImageChops.multiply(src.split()[3], keep.filter(ImageFilter.GaussianBlur(1.2))))
        case_img = src.crop((30, 110, 510, 782))
        th = int(0.86 * 236 * scale); k = th / 666
        case_img = case_img.resize((int(case_img.width * k), int(case_img.height * k)), Image.LANCZOS)
        cx, cy = int(430 * scale), int(610 * scale)
        cw = int(412 * k)
        m = arm.split()[3]
        # strap: straight band wrapping the wrist, clipped to the arm outline
        strap = Image.new("RGBA", arm.size, (0, 0, 0, 0)); ds = ImageDraw.Draw(strap)
        sw = int(cw * 0.78); x0 = cx - (case_img.width - cw) // 2 * 0 - cw // 2 + 2
        ds.rectangle((x0 + (cw - sw) // 2, cy - 400, x0 + (cw + sw) // 2, cy + 400), fill=(30, 31, 35, 255))
        ds.line((x0 + (cw - sw) // 2 + 6, cy - 400, x0 + (cw - sw) // 2 + 6, cy + 400), fill=(70, 72, 78, 255), width=3)
        strap.putalpha(ImageChops.multiply(strap.split()[3], m))
        sh = Image.new("RGBA", arm.size, (0, 0, 0, 0))
        ImageDraw.Draw(sh).rounded_rectangle((x0 - 8, cy - th // 2 - 4, x0 + cw + 10, cy + th // 2 + 14), radius=40, fill=(0, 0, 0, 90))
        sh = sh.filter(ImageFilter.GaussianBlur(9))
        full = Image.new("RGBA", arm.size, (0, 0, 0, 0)); full.alpha_composite(strap); full.alpha_composite(sh)
        full.alpha_composite(case_img, (x0 - 4, cy - case_img.height // 2))
        sc["acc_spr"] = full; sc["acc_at"] = (arm.width / 2, arm.height / 2); sc["watch_c"] = (cx, cy)
        sc["prod"] = None
    else:
        scale = 0.98; path = WOMAN if who == "woman" else MAN
        sc["sil_img"] = svg_img(f'<path d="{path}" fill="{hexc(sc["sil"])}"/>', scale, mir)
        x = -190 if not mir else W - 1000 * scale + 190
        sc["sil_pos"] = (x, H - 1200 * scale)
        ex, ey = EAR[who]
        if sc["acc"] == "bud":
            a = svg_img(bud(ex, ey, sc["acc_col"], sc["acc_edge"]), scale, mir)
        else:
            a = svg_img(NECKBAND + bud(ex, ey, "#17181c", "#17181c"), scale, mir)
        bb = a.getbbox(); sc["acc_spr"] = a.crop(bb)
        sc["acc_at"] = ((bb[0] + bb[2]) / 2, (bb[1] + bb[3]) / 2)
        sc["ear"] = ((1000 - ex if mir else ex) * scale, ey * scale)
        sc["prod"] = product_sprite(HQ + sc["img"], 400, 400)
        sc["prod_at"] = (845 if not mir else W - 845, 1060)
    ink = sc["ink"]
    sc["tag_spr"] = pill_sprite(sc["tag"], f("Poppins-Bold.ttf", 30), rgba(ink, 255) if ink == DARK else (255, 255, 255, 255),
                                rgba(sc["bg"]), padx=30)
    sc["t1"] = text_spr(sc["title"][0], f("Poppins-Medium.ttf", 64), rgba(ink))
    sc["t2"] = text_spr(sc["title"][1], f("Poppins-Bold.ttf", 96 if len(sc["title"][1]) < 15 else 86), rgba(ink))
    sc["price_spr"] = price_spr(sc["price"], sc["regular"], ink, sc["bg"])
    sc["feat_spr"] = text_spr(sc["feat"], f("Poppins-Medium.ttf", 40), rgba(ink, 225))
    return sc

def scene_frame(sc, prev_bg, t):
    img = Image.new("RGBA", (W, H), rgba(prev_bg))
    # circle wipe in the new colour
    k = ease(t / 0.38); ox, oy = W / 2, 1150
    r = k * math.hypot(W, H)
    ImageDraw.Draw(img).ellipse((ox - r, oy - r, ox + r, oy + r), fill=rgba(sc["bg"]))
    # soft background disc behind the product
    d = ImageDraw.Draw(img)
    mir = sc.get("mirror", False)
    # silhouette slides in
    sx, sy = sc["sil_pos"]; e = ease((t - 0.08) / 0.5)
    off = (1 - e) * (-520 if not mir else 520); drift = 14 * t
    if sc["who"] == "arm": off = (1 - e) * -800
    gx, gy = sx + off + (drift if not mir else -drift), sy
    if e > 0: img.alpha_composite(sc["sil_img"], (int(gx), int(gy)))
    # accessory
    ka = (t - 0.62) / 0.3
    ax, ay = sc["acc_at"]
    if sc["acc"] == "watch":
        put(img, sc["acc_spr"], gx + ax, gy + ay - (1 - ease(ka)) * 30, a=clamp(ka * 1.6))
    elif sc["acc"] == "neckband":
        put(img, sc["acc_spr"], gx + ax, gy + ay - (1 - ease(ka)) * 50, a=clamp(ka * 1.5))
    else:
        put(img, sc["acc_spr"], gx + ax, gy + ay, scale=back(ka))
    if sc["acc"] != "watch":
        ex, ey = sc["ear"]; burst(img, gx + ex, gy + ey, (t - 0.7) / 0.5, (255, 255, 255) if sc["sil"] == DARK else (255, 255, 255))
    else:
        wx, wy = sc["watch_c"]; burst(img, gx + wx, gy + wy, (t - 0.75) / 0.5, (255, 255, 255))
    # product pop + bob
    if sc["prod"] is not None:
        kp = (t - 0.3) / 0.42; px, py = sc["prod_at"]
        put(img, sc["prod"], px, py + 12 * math.sin(t * 3.2), scale=0.55 + 0.45 * back(kp), a=clamp(kp * 3), rot=(1 - ease(kp)) * 14)
    # text block
    x0 = 80
    def slide(spr, y, start, dx=0):
        kk = ease((t - start) / 0.4)
        if kk <= 0: return
        s = spr.copy(); s.putalpha(s.split()[3].point(lambda v: int(v * kk)))
        img.alpha_composite(s, (int(x0 + dx * (1 - kk)), int(y + 50 * (1 - kk))))
    slide(sc["tag_spr"], 190, 0.18); slide(sc["t1"], 275, 0.24); slide(sc["t2"], 345, 0.30)
    kp = back((t - 0.5) / 0.4)
    if kp > 0:
        put(img, sc["price_spr"], x0 + sc["price_spr"].width / 2 - 200 * (1 - kp), 560, a=clamp((t - 0.5) / 0.15))
    slide(sc["feat_spr"], 655, 0.82)
    img.alpha_composite(LOGO_CARD, (W - LOGO_CARD.width - 50, 60))
    return img.convert("RGB")

# ---------- intro & end ----------
PRODS = [product_sprite(HQ + n, 300, 300) for n in ("12.png", "02.png", "04.png", "13.png", "10.png")]
INTRO_COLS = [(255, 104, 92), (46, 98, 255), (255, 196, 46), (132, 84, 255)]

def intro_frame(t):
    beat = min(3, int(t / B)); bg = DARK
    img = Image.new("RGBA", (W, H), rgba(bg)); d = ImageDraw.Draw(img)
    # colour bars that flash on each beat
    for i in range(beat + 1):
        kk = ease((t - i * B) / 0.25); col = INTRO_COLS[i]
        y = 300 + i * 330; w = kk * W
        d.rectangle((0 if i % 2 == 0 else W - w, y, w if i % 2 == 0 else W, y + 26), fill=rgba(col))
    words = ["WEAR", "YOUR", "VIBE"]
    big = f("Poppins-Bold.ttf", 230)
    for i, wd in enumerate(words):
        kk = (t - i * B) / 0.22
        if kk <= 0: continue
        s = text_spr(wd, big, rgba(WHITE if i < 2 else INTRO_COLS[2]))
        put(img, s, W / 2, 470 + i * 330, scale=1.6 - 0.6 * ease(kk), a=clamp(kk * 2))
    kk = (t - 3 * B) / 0.3
    if kk > 0:
        s = text_spr("Smart gadgets for her & him", f("Poppins-Medium.ttf", 52), rgba(WHITE, 230))
        put(img, s, W / 2, 1520 + 40 * (1 - ease(kk)), a=clamp(kk))
    img.alpha_composite(LOGO_CARD, (W - LOGO_CARD.width - 50, 60))
    return img.convert("RGB")

def end_frame(t, prev_bg):
    img = Image.new("RGBA", (W, H), rgba(prev_bg))
    k = ease(t / 0.38); r = k * math.hypot(W, H); ox, oy = W / 2, 960
    ImageDraw.Draw(img).ellipse((ox - r, oy - r, ox + r, oy + r), fill=rgba(DARK))
    # product arc
    for i, p in enumerate(PRODS):
        kk = (t - 0.2 - i * 0.08) / 0.4
        ang = math.radians(-150 + i * 30)
        cx = W / 2 + 400 * math.cos(ang); cy = 760 + 380 * math.sin(ang)
        put(img, p, cx, cy + 10 * math.sin(t * 3 + i), scale=0.62 * back(kk), a=clamp(kk * 3))
    lc = LOGO.resize((380, int(LOGO.height * 380 / LOGO.width)), Image.LANCZOS)
    card = Image.new("RGBA", (lc.width + 70, lc.height + 50), (0, 0, 0, 0))
    ImageDraw.Draw(card).rounded_rectangle((0, 0, card.width - 1, card.height - 1), radius=36, fill=(255, 255, 255, 255))
    card.alpha_composite(lc, (35, 25))
    kk = (t - 0.35) / 0.4; put(img, card, W / 2, 900, scale=back(kk))
    def line(text, font, col, y, st):
        kk = (t - st) / 0.35
        if kk > 0: put(img, text_spr(text, font, col), W / 2, y + 40 * (1 - ease(kk)), a=clamp(kk))
    line("Wear your vibe.", f("Poppins-Bold.ttf", 84), rgba(WHITE), 1130, 0.6)
    line("Earbuds  •  Smart Watch  •  Neckband", f("Poppins-Medium.ttf", 42), rgba(WHITE, 210), 1240, 0.75)
    kk = back((t - 0.95) / 0.4)
    if kk > 0:
        pill = pill_sprite("Order: everydaycart.online", f("Poppins-Bold.ttf", 48), rgba((255, 196, 46)), rgba(DARK), padx=50)
        put(img, pill, W / 2, 1400, scale=kk)
    line("Limited stock  •  Inbox us to order", f("Poppins-Medium.ttf", 40), rgba(WHITE, 200), 1530, 1.15)
    return img.convert("RGB")

# ---------- render ----------
def encode(name, frames_fn, dur):
    tmp = OUT + name + ".tmp.mp4"; n = int(round(dur * FPS))
    cmd = ["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
           "-c:v", "libx264", "-preset", "veryfast", "-crf", "18", "-pix_fmt", "yuv420p", tmp]
    p = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    for k in range(n): p.stdin.write(frames_fn(k / FPS).tobytes())
    p.stdin.close()
    if p.wait() == 0: os.replace(tmp, OUT + name + ".mp4")

if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else "preview"
    for sc in SCENES: build(sc)
    if mode == "preview":
        shots = [intro_frame(INTRO_D - 0.05)]
        prev = DARK
        for sc in SCENES: shots.append(scene_frame(sc, prev, 1.6)); prev = sc["bg"]
        shots.append(end_frame(2.2, prev))
        for i, s in enumerate(shots): s.save(f"/tmp/pv{i}.jpg", quality=90)
        sheet = Image.new("RGB", (len(shots) * 360, 640))
        for i, s in enumerate(shots): sheet.paste(s.resize((360, 640), Image.LANCZOS), (i * 360, 0))
        sheet.save("/tmp/pv_sheet.jpg", quality=90)
    else:
        parts = [("s0", intro_frame, INTRO_D)]; prev = DARK
        for i, sc in enumerate(SCENES):
            parts.append((f"s{i+1}", (lambda sc, pb: (lambda t: scene_frame(sc, pb, t)))(sc, prev), SCENE_D)); prev = sc["bg"]
        parts.append(("s6", (lambda pb: (lambda t: end_frame(t, pb)))(prev), END_D))
        for name, fn, dur in parts: encode(name, fn, dur); print(name, flush=True)
        with open(OUT + "list.txt", "w") as fh:
            for name, _, _ in parts: fh.write(f"file '{name}.mp4'\n")
        total = INTRO_D + 5 * SCENE_D + END_D
        cuts = [INTRO_D + i * SCENE_D for i in range(1, 6)]
        mix = drive(total, INTRO_D, cuts, INTRO_D + 5 * SCENE_D)
        wavfile.write(OUT + "music.wav", SR, (np.stack([mix, mix], 1) * 32767).astype(np.int16))
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", OUT + "list.txt", "-i", OUT + "music.wav",
                        "-map", "0:v", "-map", "1:a", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-shortest", "-movflags", "+faststart",
                        OUT + "05_wear_your_vibe_reel.mp4"], check=True)
        print("done", total)
