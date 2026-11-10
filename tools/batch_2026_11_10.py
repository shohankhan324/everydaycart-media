"""Everyday Cart daily batch, 10 Nov 2026. NEW style set 5 (render_styles5: K bento grid, L headline pop).
4 image posts + 1 Reel (the owner-approved 11.11 deals post is already queued at 10:00)."""
import os, sys
import render_flat as rf
from render_flat import im, HQ, FL
from render_styles5 import TEMPLATES5 as T
rf.OUTDIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "posts", "batch-2026-11-10")) + "/"
os.makedirs(rf.OUTDIR, exist_ok=True)

POSTS = [
    ("K", dict(out="01_awei_t108", img=HQ + "10.png", tag="WIRELESS EARBUDS", title="Awei T108 Wireless Earbuds",
               sub="Official  •  Bluetooth 5.3  •  USB Type C", stats=[("20H", "playback with the case"), ("ENC", "for clear calls")],
               feats=["13mm Drivers", "6H Playback", "Type C"], price=950, regular=1199,
               bg=(244, 241, 236), tile=(216, 226, 242), acc=(238, 98, 70), dark=(30, 40, 72), maxw=470, maxh=520, cy=470)),
    ("L", dict(out="02_kodomo_oral_care", img=[im(FL + "kodomo_brush.png"), im(FL + "kodomo_paste.png").rotate(90, expand=True)],
               tag="BABY ORAL CARE", head=("Tiny teeth,", "big smiles!"), title="Kodomo Baby Toothpaste + Toothbrush",
               feats=["1000 ppm Fluoride + Xylitol", "Sugar free orange cream", "Soft bristles", "Brush for 0.5 to 3 years"],
               prices=[("TOOTHPASTE", 280, 400), ("TOOTHBRUSH", 200, 400)],
               bg=(244, 128, 52), hl=(255, 226, 120), acc=(30, 92, 170), blob=(255, 236, 214), maxw=500, maxh=540, gap=24,
               cx=440, cy=680, r=265, bx=752, by=640)),
    ("L", dict(out="03_316_thermal_bottle", img=HQ + "17.png", tag="THERMAL BOTTLE  •  700 ML",
               head=("Warm sips,", "on the go."), title="316 Stainless Steel Thermal Bottle",
               feats=["316 stainless steel", "700 ml capacity", "Safety lock lid", "Easy carry handle"], price=800, regular=1100,
               bg=(120, 82, 70), hl=(246, 196, 150), acc=(226, 92, 76), blob=(246, 232, 220), maxw=320, maxh=560,
               cx=470, cy=700, r=270, bx=770, by=700)),
    ("K", dict(out="04_steel_water_pot", img=HQ + "32.png", tag="HOME  •  TEA & COFFEE", title="Stainless Steel Water Pot",
               sub="Tea, coffee, milk, juice or water  •  Ask for colours", stats=[("Double wall", "insulated body"), ("Leak-proof", "lid")],
               feats=["Insulated", "Ergonomic Handle", "Matte Finish"], price=1000, regular=1400,
               bg=(247, 240, 234), tile=(250, 222, 206), acc=(84, 120, 176), dark=(70, 52, 60), maxw=430, maxh=600, cy=480)),
]

if __name__ == "__main__":
    keys = sys.argv[1:]
    for kind, p in POSTS:
        if keys and p["out"][:2] not in keys: continue
        if isinstance(p["img"], str): p["img"] = im(p["img"])
        T[kind](p)
