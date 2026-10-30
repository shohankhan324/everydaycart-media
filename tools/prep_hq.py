"""High-quality product cutouts: optional EDSR upscale, matting, colour-variant cleanup, edge decontamination."""
import os, sys, glob
import numpy as np, cv2
from PIL import Image, ImageFilter
from scipy import ndimage
from rembg import remove, new_session

D = os.path.dirname(os.path.abspath(__file__)) + "/"
SRC = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + "/products/source/"
OUT = D + "cutouts/hq/"; os.makedirs(OUT, exist_ok=True)
_sess = {}
def sess(name):
    if name not in _sess: _sess[name] = new_session(name)
    return _sess[name]
_sr = {}
def upscale(img, k):
    if k == 1: return img
    if k not in _sr:
        sr = cv2.dnn_superres.DnnSuperResImpl_create(); sr.readModel(D + f"models/EDSR_x{k}.pb"); sr.setModel("edsr", k); _sr[k] = sr
    bgr = cv2.cvtColor(np.asarray(img.convert("RGB")), cv2.COLOR_RGB2BGR)
    H, W = bgr.shape[:2]; T, O = 160, 16
    out = np.zeros((H * k, W * k, 3), np.float32); wsum = np.zeros((H * k, W * k, 1), np.float32)
    for y in range(0, H, T):
        for x in range(0, W, T):
            y0, x0 = max(0, y - O), max(0, x - O); y1, x1 = min(H, y + T + O), min(W, x + T + O)
            up = _sr[k].upsample(np.ascontiguousarray(bgr[y0:y1, x0:x1])).astype(np.float32)
            # keep only the core of the tile, drop the overlap margins
            cy0, cx0 = (y - y0) * k, (x - x0) * k
            ch, cw = (min(y + T, H) - y) * k, (min(x + T, W) - x) * k
            out[y * k:y * k + ch, x * k:x * k + cw] = up[cy0:cy0 + ch, cx0:cx0 + cw]
    return Image.fromarray(cv2.cvtColor(np.clip(out, 0, 255).astype(np.uint8), cv2.COLOR_BGR2RGB))

def src(name): return Image.open(glob.glob(SRC + name + ".*")[0]).convert("RGB")
def sat(rgb):
    mx = rgb.max(axis=2).astype(float); mn = rgb.min(axis=2).astype(float)
    return np.where(mx > 0, (mx - mn) / np.maximum(mx, 1), 0)

def matte(img, model="isnet-general-use"):
    return np.asarray(remove(img, session=sess(model), only_mask=True)).astype(float) / 255

def flood_alpha(img, tol=16):
    a = np.asarray(img).astype(int)
    border = np.concatenate([a[0], a[-1], a[:, 0], a[:, -1]]); bgc = np.median(border, axis=0)
    near = np.abs(a - bgc).max(axis=2) <= tol
    lab, _ = ndimage.label(near)
    bl = set(np.unique(np.concatenate([lab[0], lab[-1], lab[:, 0], lab[:, -1]]))) - {0}
    fg = ~np.isin(lab, list(bl))
    # enclosed background pockets (e.g. inside a cable loop): large, flat, background coloured
    for i, sl in enumerate(ndimage.find_objects(lab), 1):
        if sl is None or i in bl: continue
        reg = lab == i
        if reg.sum() > 400 and np.abs(a[reg] - bgc).max(axis=1).mean() < 8:
            fg[reg] = False
    return ndimage.gaussian_filter(fg.astype(float), 0.8)

def keep_largest(alpha, frac=0.06):
    fg = alpha > 0.5
    lab, n = ndimage.label(fg)
    if n > 1:
        sizes = ndimage.sum(fg, lab, range(1, n + 1))
        keep = [i + 1 for i, s in enumerate(sizes) if s >= frac * sizes.max()]
        m = np.isin(lab, keep)
        m = ndimage.binary_dilation(m, iterations=3)
        alpha = alpha * m
    return alpha

def refine(img, alpha, choke=0.10, erode=0):
    """Edge decontamination: replace fringe colours with nearby solid foreground colour, then choke alpha."""
    I = np.asarray(img).astype(float)
    a = alpha.copy()
    if erode:
        a = np.minimum(a, ndimage.grey_erosion(a, size=(2 * erode + 1, 2 * erode + 1)))
    w = (a > 0.97).astype(float)
    F = I.copy()
    num = np.zeros_like(I); den = np.zeros(a.shape)
    for sigma in (2, 5, 12):
        den = ndimage.gaussian_filter(w, sigma)
        num = np.stack([ndimage.gaussian_filter(I[..., c] * w, sigma) for c in range(3)], -1)
        est = num / np.maximum(den[..., None], 1e-6)
        fill = (a < 0.97) & (den > 1e-3) & (F is not None)
        F = np.where(fill[..., None] & (den[..., None] > 0.02), est, F)
    mix = np.clip((0.97 - a) / 0.97, 0, 1)[..., None]
    rgb = I * (1 - mix) + F * mix
    a = np.clip((a - choke) / (1 - choke), 0, 1)
    out = np.dstack([np.clip(rgb, 0, 255), a * 255]).astype(np.uint8)
    im = Image.fromarray(out, "RGBA")
    return im.crop(im.getbbox())

def orig_grid(shape, x0, y0, k):
    H, W = shape[:2]
    yy, xx = np.mgrid[0:H, 0:W].astype(float)
    return xx / k + x0, yy / k + y0

def job(key):
    if key == "01":
        img = upscale(src("oraimo-spacebox-portable-bluetooth-speaker-0"), 4)
        return refine(img, keep_largest(matte(img)), erode=2)
    if key == "02":
        img = src("oraimo-watch-5-lite-smart-watch-0"); return refine(img, keep_largest(matte(img)))
    if key == "03":
        img = src("proove-intro-pro-app-black-tws-with-anc-0"); return refine(img, keep_largest(matte(img)))
    if key == "04":
        img = src("oraimo-necklace-lite-enc-wireless-neckband-0"); return refine(img, keep_largest(flood_alpha(img)), choke=0.05)
    if key == "05":
        img = src("forkan-premium-trolley-luggage-0"); return refine(img, keep_largest(matte(img)))
    if key == "06":
        img = upscale(src("22-big-teddy-bear-0"), 2); return refine(img, keep_largest(matte(img)), erode=4)
    if key == "07":
        img = src("silent-alarm-clock-1"); return refine(img, keep_largest(matte(img)))
    if key == "08":
        img = src("minitree-tritan-baby-bottle-with-handles-7oz-0"); return refine(img, keep_largest(matte(img)))
    if key == "09":
        img = upscale(src("colmi-p81-calling-smartwatch-0"), 4); return refine(img, keep_largest(matte(img)), erode=2)
    if key == "10":
        s = src("awei-t108-0").crop((60, 40, 460, 480)); img = upscale(s, 4); return refine(img, keep_largest(matte(img)), erode=2)
    if key == "11":
        img = upscale(src("awei-t88-wireless-earbuds-0"), 2); return refine(img, keep_largest(matte(img)), erode=1)
    if key == "12":
        img = src("oraimo-spacebuds-neo-0"); return refine(img, keep_largest(matte(img, "u2net")))
    if key == "13":
        img = src("oraimo-spacebuds-lite-0"); return refine(img, keep_largest(matte(img)))
    if key == "14":
        img = src("awei-ka5-20w-portable-bluetooth-speaker-0"); return refine(img, keep_largest(matte(img)))
    if key == "15":  # Mood the cup: blue only
        x0, y0, x1, y1 = 200, 240, 880, 1340; k = 2
        img = upscale(src("big-mac-316-stainless-steel-thermos-cup-0").crop((x0, y0, x1, y1)), k)
        a = matte(img); xx, yy = orig_grid(a.shape, x0, y0, k)
        I = np.asarray(img).astype(int); r, g, b = I[..., 0], I[..., 1], I[..., 2]
        blueish = (b > g + 8) & (b > r + 25); dark = (r + g + b) / 3 < 70
        a = np.where((xx > 822) | ((xx > 740) & ~blueish & ~dark & (yy < 1000)) | ((xx > 760) & (yy < 480)), 0, a)
        im = refine(img, keep_largest(a), erode=1)
        im = im.rotate(-7, expand=True, resample=Image.BICUBIC); return im.crop(im.getbbox())
    if key == "16":  # ThinkDifferent: purple + white
        img = src("premium-thermal-tumbler-0"); a = matte(img)
        xx, yy = orig_grid(a.shape, 0, 0, 1)
        I = np.asarray(img).astype(int); lum = I.mean(axis=2); whiteish = (lum > 160) & (sat(I) < 0.16)
        keep_handle = (xx >= 975) & (xx <= 1140) & (yy >= 560) & (yy <= 870) & whiteish
        a = np.where((xx > 980) & ~keep_handle, 0, a)
        a = np.where((xx >= 926) & (xx <= 980) & (yy >= 560) & (yy <= 905) & ~whiteish, 0, a)
        a = np.where((xx > 915) & (yy < 385), 0, a)
        return refine(img, keep_largest(a))
    if key == "17":  # Cow bottle: brown
        x0, y0, x1, y1 = 940, 260, 1320, 1200; k = 2
        img = upscale(src("316-stainless-steel-thermal-bottle-0").crop((x0, y0, x1, y1)), k)
        a = matte(img); I = np.asarray(img).astype(int); r, g, b = I[..., 0], I[..., 1], I[..., 2]
        red = (r > 140) & (g < 110) & (b < 110) & (r - g > 70)
        xx, yy = orig_grid(a.shape, x0, y0, k)
        a = np.where(red | (xx < 962), 0, a)
        return refine(img, keep_largest(a), erode=1)
    if key == "18":  # International: white only, stood upright
        x0, y0, x1, y1 = 195, 715, 870, 1095; k = 2
        full = src("premium-thermal-water-bottle-2")
        a_full = matte(full)
        img = upscale(full.crop((x0, y0, x1, y1)), k)
        a = np.asarray(Image.fromarray((a_full[y0:y1, x0:x1] * 255).astype(np.uint8)).resize(img.size, Image.LANCZOS)).astype(float) / 255
        I = np.asarray(img).astype(int)
        a = np.where(sat(I) > 0.16, 0, a)
        a = keep_largest(a)
        a = np.where(ndimage.binary_opening(a > 0.5, iterations=2), a, 0)
        im = refine(img, a, erode=1)
        im = im.rotate(-106.5, expand=True, resample=Image.BICUBIC); return im.crop(im.getbbox())
    if key == "19":
        s = src("custom-500ml-luxury-stainless-steel-thermal-mug-intelligent-led-digital-temperature-display-smart-insulation-2").crop((340, 60, 1050, 1040))
        img = s; return refine(img, keep_largest(matte(img)))
    if key == "20":
        img = src("minitree-baby-kettle-duck-bill-mumpot-0"); return refine(img, keep_largest(matte(img)))
    if key == "21":
        img = src("10-pc-baby-care-kit-2"); return refine(img, keep_largest(matte(img)))
    if key == "22":
        img = src("120-ml-minitree-baby-feeding-bottle-0"); return refine(img, keep_largest(matte(img)))

if __name__ == "__main__":
    keys = sys.argv[1:] or [f"{i:02d}" for i in range(1, 23)]
    for k in keys:
        im = job(k); im.save(OUT + k + ".png"); print(k, im.size, flush=True)
