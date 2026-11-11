"""Everyday Cart daily batch, 11 Nov 2026. NEW style set 6 (render_styles6: M orbit poster, N checklist note).
4 image posts + 1 Reel (the owner-approved 11.11 deals repost is already queued at 11:11)."""
import os, sys
import render_flat as rf
from render_flat import im, HQ, FL
from render_styles6 import TEMPLATES6 as T
rf.OUTDIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "posts", "batch-2026-11-11")) + "/"
os.makedirs(rf.OUTDIR, exist_ok=True)

POSTS = [
    ("M", dict(out="01_oraimo_necklace_lite", img=HQ + "04.png", tag="WIRELESS NECKBAND", title="Oraimo Necklace Lite ENC Neckband",
               bn="সারাদিনের গানের সাথী নেকব্যান্ড", feats=["30H Playtime", "ENC for Calls", "Dual Device"], price=1300, regular=1485,
               bg=(28, 46, 92), acc=(255, 196, 64), hl=(255, 236, 190), maxw=430, maxh=560)),
    ("N", dict(out="02_baby_care_kit", img=FL + "baby_kit_stack.png", tag="PINK  •  SKY BLUE", title="10 Pc Baby Care Kit",
               bn=["নবজাতকের যত্নের সব", "এক বক্সে বেবি কেয়ার কিট"], feats=["Nail care tools", "Hair brush and comb", "Thermometer", "Nasal aspirator"],
               price=480, regular=650, card=(255, 214, 222), note=(178, 230, 214), acc=(236, 96, 128), dark=(48, 52, 86), maxw=510, maxh=610)),
    ("M", dict(out="03_insulated_lunch_box", img=HQ + "26.png", tag="LUNCH BOX  •  2.6L", title="3 Layer Stainless Steel Insulated Lunch Box",
               bn="অফিসে ঘরের গরম খাবার লাঞ্চ বক্সে", feats=["Hot or cold up to 12H", "2.6L Capacity", "Leak Proof"], price=3000, regular=4500,
               bg=(150, 70, 52), acc=(255, 214, 140), hl=(255, 232, 206), maxw=470, maxh=540)),
    ("N", dict(out="04_big_teddy_bear", img=HQ + "06.png", tag="22 INCH TEDDY BEAR", title="22\" Big Teddy Bear",
               bn=["প্রিয়জনের জন্য", "নরম টেডি বিয়ার উপহার"], feats=["Super soft plush", "22 inch size", "Cuddle and decorate", "Gift for any occasion"],
               price=1150, regular=2000, card=(176, 210, 240), note=(255, 196, 206), acc=(70, 120, 200), dark=(60, 44, 52),
               paper=(252, 248, 242), maxw=440, maxh=520, tilt=-3, note_tilt=4)),
]

if __name__ == "__main__":
    keys = sys.argv[1:]
    for kind, p in POSTS:
        if keys and p["out"][:2] not in keys: continue
        if isinstance(p["img"], str): p["img"] = im(p["img"])
        T[kind](p)
