"""Real-people gadget Reel: licensed lifestyle photos + real product cards, beat-synced, original music."""
import os, sys, math, subprocess
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
sys.path.insert(0, "/home/claude/everydaycart-media/tools"); sys.path.insert(0, "/home/claude/viral")
from render_video import f, clamp, ease, back, product_sprite, pill_sprite
from viral import put, text_spr, LOGO, LOGO_CARD, PRODS, rgba, DARK, WHITE
from drive import drive, B, SR
from scipy.io import wavfile

W, H, FPS = 1080, 1920, 30
A = "/mnt/user-data/attachments/da0f4f16-de8b-599c-9c43-7f614620f3dd/"
HQ = "/home/claude/everydaycart-media/tools/cutouts/hq/"
OUT = "/home/claude/viral/out_photo/"; os.makedirs(OUT, exist_ok=True)
Z = 1.12  # pre-scale headroom for the slow zoom

def cover(path, fx, fy):
    """Crop to 9:16 around a focal point and scale to Z x output size; returns image + focal in that image."""
    im = Image.open(path).convert("RGB"); w, h = im.size
    cw, ch = (w, w * 16 / 9) if w / h < 9 / 16 else (h * 9 / 16, h)
    x0 = min(max(fx - cw / 2, 0), w - cw); y0 = min(max(fy - ch / 2, 0), h - ch)
    im = im.crop((int(x0), int(y0), int(x0 + cw), int(y0 + ch)))
    big = im.resize((int(W * Z), int(H * Z)), Image.LANCZOS).filter(ImageFilter.UnsharpMask(1.2, 60, 2))
    s = W * Z / cw; return big, ((fx - x0) * s, (fy - y0) * s)

def kenburns(big, foc, t, dur, punch=True):
    k = t / dur; zoom = 1.0 + 0.07 * k                       # slow push in
    if punch: zoom += 0.10 * (1 - ease(t / 0.35))            # beat punch at the cut
    cw, ch = W * Z / (Z * zoom) * Z / Z, H * Z / (Z * zoom)
    cw, ch = big.width / (Z * zoom) * 1.0, big.height / (Z * zoom)
    cx = big.width / 2 + (foc[0] - big.width / 2) * (zoom - 1) * 1.6
    cy = big.height / 2 + (foc[1] - big.height / 2) * (zoom - 1) * 1.6
    x0 = min(max(cx - cw / 2, 0), big.width - cw); y0 = min(max(cy - ch / 2, 0), big.height - ch)
    return big.resize((W, H), Image.BICUBIC, box=(x0, y0, x0 + cw, y0 + ch)).convert("RGBA")

def gradient(top, h, a0, a1):
    g = Image.new("RGBA", (W, h)); px = np.zeros((h, W, 4), np.uint8)
    px[..., 3] = np.linspace(a0, a1, h)[:, None].astype(np.uint8); g = Image.fromarray(px, "RGBA"); return g, top
GRAD_B = gradient(1150, 770, 0, 170); GRAD_T = gradient(0, 420, 120, 0)

def card(sc):
    cw, chh = 940, 410; acc = sc["acc"]
    c = Image.new("RGBA", (cw, chh), (0, 0, 0, 0)); d = ImageDraw.Draw(c)
    sh = Image.new("RGBA", (cw + 80, chh + 80), (0, 0, 0, 0))
    ImageDraw.Draw(sh).rounded_rectangle((40, 50, cw + 40, chh + 40), radius=44, fill=(0, 0, 0, 90))
    sh = sh.filter(ImageFilter.GaussianBlur(18))
    d.rounded_rectangle((0, 0, cw - 1, chh - 1), radius=44, fill=(255, 255, 255, 246))
    d.ellipse((30, 45, 350, 365), fill=rgba(sc["tint"]))
    p = product_sprite(HQ + sc["img"], 280, 280); c.alpha_composite(p, (190 - p.width // 2, 205 - p.height // 2))
    x = 385
    tag = pill_sprite(sc["tag"], f("Poppins-Bold.ttf", 24), rgba(acc), (255, 255, 255, 255), padx=22); c.alpha_composite(tag, (x, 42))
    d.text((x, 100), sc["brand"], font=f("Poppins-Medium.ttf", 36), fill=(110, 112, 120))
    nf = f("Poppins-Bold.ttf", 50 if f("Poppins-Bold.ttf", 50).getlength(sc["name"]) < 520 else 42)
    d.text((x, 142), sc["name"], font=nf, fill=DARK)
    pf = f("Poppins-Bold.ttf", 72); ptxt = f"Tk {sc['price']:,}"
    d.text((x, 205), ptxt, font=pf, fill=rgba(acc))
    rf = f("Poppins-Medium.ttf", 32); rx = x + pf.getlength(ptxt) + 22; rt = f"Tk {sc['regular']:,}"
    d.text((rx, 240), rt, font=rf, fill=(150, 150, 156)); d.line((rx - 3, 262, rx + rf.getlength(rt) + 3, 262), fill=(150, 150, 156), width=4)
    d.text((x, 315), sc["feat"], font=f("Poppins-Medium.ttf", 29), fill=(90, 92, 100))
    out = Image.new("RGBA", sh.size, (0, 0, 0, 0)); out.alpha_composite(sh); out.alpha_composite(c, (40, 40)); return out

SCENES = [
    dict(photo="d52f53df-image.jpg", foc=(1327, 520), img="12.png", tag="EARBUDS", brand="Oraimo", name="SpaceBuds Neo+",
         price=1940, regular=2189, feat="Sound360 Audio  •  30H Battery", acc=(232, 84, 72), tint=(253, 236, 232), pos="bottom",
         hook="Her everyday sound"),
    dict(photo="a252c7b5-image.jpg", foc=(900, 1150), img="02.png", tag="SMART WATCH", brand="Oraimo", name="Watch 5 Lite",
         price=1650, regular=1870, feat="Bluetooth Calling  •  IP68", acc=(46, 98, 255), tint=(232, 239, 255), pos="top",
         hook="Smart on every wrist"),
    dict(photo="e43fe08a-image.jpg", foc=(900, 1095), img="13.png", tag="EARBUDS", brand="Oraimo", name="SpaceBuds Lite",
         price=1310, regular=1496, feat="Spatial Audio  •  40H Battery", acc=(124, 76, 245), tint=(240, 234, 255), pos="bottom",
         hook="His daily soundtrack"),
    dict(photo="04e8674c-image.jpg", foc=(980, 880), img="10.png", tag="EARBUDS", brand="Awei", name="T108 Earbuds",
         price=950, regular=1199, feat="13mm Drivers  •  ENC Calls", acc=(16, 160, 116), tint=(228, 247, 240), pos="bottom",
         hook="Big sound, small price"),
]
INTRO_D = 4 * B; SCENE_D = 6 * B; END_D = 7 * B

def hook_spr(text):
    ft = f("Poppins-Bold.ttf", 64); w = int(ft.getlength(text)) + 60
    s = Image.new("RGBA", (w, 110), (0, 0, 0, 0)); d = ImageDraw.Draw(s)
    d.text((32, 14), text, font=ft, fill=(255, 255, 255, 255), stroke_width=0)
    sh = s.filter(ImageFilter.GaussianBlur(8)); a = sh.split()[3].point(lambda v: int(v * 0.55))
    shadow = Image.new("RGBA", s.size, (0, 0, 0, 255)); shadow.putalpha(a)
    o = Image.new("RGBA", s.size, (0, 0, 0, 0)); o.alpha_composite(shadow); o.alpha_composite(s); return o

def prep(sc):
    sc["big"], sc["focal"] = cover(A + sc["photo"], *sc["foc"]); sc["card"] = card(sc); sc["hook_spr"] = hook_spr(sc["hook"])
    return sc

def scene_frame(sc, t):
    img = kenburns(sc["big"], sc["focal"], t, SCENE_D)
    g, top = GRAD_B if sc["pos"] == "bottom" else (gradient(0, 820, 175, 0)[0], 0)
    img.alpha_composite(g, (0, top)); img.alpha_composite(GRAD_T[0], (0, 0))
    # white flash on the cut
    if t < 0.18:
        fl = Image.new("RGBA", (W, H), (255, 255, 255, int(200 * (1 - t / 0.18)))); img.alpha_composite(fl)
    c = sc["card"]; kc = back((t - 0.35) / 0.45)
    if kc > 0:
        if sc["pos"] == "bottom": y = 1430 + (1 - kc) * 500
        else: y = 470 - (1 - kc) * 500
        put(img, c, W / 2, y, a=clamp((t - 0.35) / 0.15))
    kh = ease((t - 0.2) / 0.4)
    if kh > 0:
        hy = 1110 if sc["pos"] == "bottom" else 860
        put(img, sc["hook_spr"], W / 2, hy + 40 * (1 - kh), a=kh)
    img.alpha_composite(LOGO_CARD, (W - LOGO_CARD.width - 50, 60))
    return img.convert("RGB")

INTRO_BIG, INTRO_F = cover(A + "de10ea92-image.png", 470, 520)
COLS = [(255, 104, 92), (46, 98, 255), (255, 196, 46)]
def intro_frame(t):
    img = kenburns(INTRO_BIG, INTRO_F, t, INTRO_D, punch=False)
    img.alpha_composite(Image.new("RGBA", (W, H), (10, 12, 20, 95)))
    big = f("Poppins-Bold.ttf", 210)
    for i, wd in enumerate(["WEAR", "YOUR", "VIBE"]):
        kk = (t - i * B) / 0.2
        if kk <= 0: continue
        col = WHITE if i < 2 else COLS[2]
        put(img, hook_spr_big(wd, big, col), W / 2, 620 + i * 250, scale=1.5 - 0.5 * ease(kk), a=clamp(kk * 2))
    kk = (t - 3 * B) / 0.3
    if kk > 0: put(img, hook_spr_small("Smart gadgets for her & him"), W / 2, 1420 + 30 * (1 - ease(kk)), a=clamp(kk))
    img.alpha_composite(LOGO_CARD, (W - LOGO_CARD.width - 50, 60))
    return img.convert("RGB")

_cache = {}
def hook_spr_big(text, ft, col):
    k = (text, col)
    if k not in _cache:
        w = int(ft.getlength(text)) + 80; s = Image.new("RGBA", (w, int(ft.size * 1.45)), (0, 0, 0, 0))
        ImageDraw.Draw(s).text((40, 0), text, font=ft, fill=rgba(col))
        sh = Image.new("RGBA", s.size, (0, 0, 0, 255)); sh.putalpha(s.filter(ImageFilter.GaussianBlur(14)).split()[3].point(lambda v: int(v * .6)))
        o = Image.new("RGBA", s.size, (0, 0, 0, 0)); o.alpha_composite(sh); o.alpha_composite(s); _cache[k] = o
    return _cache[k]
def hook_spr_small(text):
    if text not in _cache: _cache[text] = pill_sprite(text, f("Poppins-Bold.ttf", 46), (255, 255, 255, 255), rgba(DARK), padx=44)
    return _cache[text]

END_BG = cover(A + "180290f7-image.jpg", 773, 1000)
def end_frame(t):
    img = kenburns(END_BG[0], END_BG[1], t, END_D)
    img = img.filter(ImageFilter.GaussianBlur(min(14, 3 + t * 20))) if t < 0.6 else END_BLUR
    img = img.copy(); img.alpha_composite(Image.new("RGBA", (W, H), (12, 13, 18, int(150 * ease(t / 0.4)))))
    for i, p in enumerate(PRODS):
        kk = (t - 0.2 - i * 0.08) / 0.4; ang = math.radians(-150 + i * 30)
        put(img, p, W / 2 + 400 * math.cos(ang), 760 + 380 * math.sin(ang) + 10 * math.sin(t * 3 + i), scale=0.62 * back(kk), a=clamp(kk * 3))
    lc = LOGO.resize((380, int(LOGO.height * 380 / LOGO.width)), Image.LANCZOS)
    cd = Image.new("RGBA", (lc.width + 70, lc.height + 50), (0, 0, 0, 0))
    ImageDraw.Draw(cd).rounded_rectangle((0, 0, cd.width - 1, cd.height - 1), radius=36, fill=(255, 255, 255, 255)); cd.alpha_composite(lc, (35, 25))
    put(img, cd, W / 2, 900, scale=back((t - 0.35) / 0.4))
    def line(text, ft, col, y, st):
        kk = (t - st) / 0.35
        if kk > 0: put(img, text_spr(text, ft, col), W / 2, y + 40 * (1 - ease(kk)), a=clamp(kk))
    line("Wear your vibe.", f("Poppins-Bold.ttf", 84), rgba(WHITE), 1130, 0.6)
    line("Earbuds  •  Smart Watch  •  Neckband", f("Poppins-Medium.ttf", 42), rgba(WHITE, 220), 1240, 0.75)
    kk = back((t - 0.95) / 0.4)
    if kk > 0: put(img, pill_sprite("Order: everydaycart.online", f("Poppins-Bold.ttf", 48), rgba((255, 196, 46)), rgba(DARK), padx=50), W / 2, 1400, scale=kk)
    line("Limited stock  •  Inbox us to order", f("Poppins-Medium.ttf", 40), rgba(WHITE, 210), 1530, 1.15)
    return img.convert("RGB")
END_BLUR = kenburns(END_BG[0], END_BG[1], 0.6, END_D).filter(ImageFilter.GaussianBlur(14))

def encode(name, fn, dur):
    tmp = OUT + name + ".tmp.mp4"; n = int(round(dur * FPS))
    p = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
                          "-c:v", "libx264", "-preset", "veryfast", "-crf", "18", "-pix_fmt", "yuv420p", tmp], stdin=subprocess.PIPE)
    for k in range(n): p.stdin.write(fn(k / FPS).tobytes())
    p.stdin.close()
    if p.wait() == 0: os.replace(tmp, OUT + name + ".mp4")

if __name__ == "__main__":
    for sc in SCENES: prep(sc)
    if sys.argv[1:] == ["preview"]:
        shots = [intro_frame(INTRO_D - 0.05)] + [scene_frame(sc, 2.0) for sc in SCENES] + [end_frame(2.5)]
        for i, s in enumerate(shots): s.save(f"/tmp/ph{i}.jpg", quality=92)
        sheet = Image.new("RGB", (len(shots) * 360, 640))
        for i, s in enumerate(shots): sheet.paste(s.resize((360, 640), Image.LANCZOS), (i * 360, 0))
        sheet.save("/tmp/ph_sheet.jpg", quality=90)
    else:
        parts = [("s0", intro_frame, INTRO_D)] + [(f"s{i+1}", (lambda sc: (lambda t: scene_frame(sc, t)))(sc), SCENE_D) for i, sc in enumerate(SCENES)] + [("s9", end_frame, END_D)]
        for name, fn, dur in parts: encode(name, fn, dur); print(name, flush=True)
        open(OUT + "list.txt", "w").write("".join(f"file '{n}.mp4'\n" for n, _, _ in parts))
        total = INTRO_D + len(SCENES) * SCENE_D + END_D
        cuts = [INTRO_D + i * SCENE_D for i in range(1, len(SCENES) + 1)]
        mix = drive(total, INTRO_D, cuts, cuts[-1])
        wavfile.write(OUT + "music.wav", SR, (np.stack([mix, mix], 1) * 32767).astype(np.int16))
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", OUT + "list.txt", "-i", OUT + "music.wav",
                        "-map", "0:v", "-map", "1:a", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-shortest", "-movflags", "+faststart",
                        OUT + "06_wear_your_vibe_real.mp4"], check=True)
        print("done", total)
