"""Everyday Cart daily batch, 9 Nov 2026. NEW style set 4 (render_styles4: I big-word poster, J ticket card).
Reduced volume per DAILY.md: 4 image posts + 1 Reel (plus the owner-approved 11.11 teaser already queued at 19:00)."""
import os, sys
import render_flat as rf
from render_flat import im, HQ
from render_styles4 import TEMPLATES4 as T
rf.OUTDIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "posts", "batch-2026-11-09")) + "/"
os.makedirs(rf.OUTDIR, exist_ok=True)

POSTS = [
    ("I", dict(out="01_colmi_p81", img=HQ + "09.png", word="CALLS", tag="SMARTWATCH  •  CALLING", title="COLMI P81 Smartwatch",
               sub="Bluetooth calling  •  1.9 inch HD display", feats=["100+ Sports Modes", "IP68", "300mAh"],
               price=1350, regular=1540, bg=(232, 236, 242), col=(38, 52, 84), stampc=(222, 98, 64), maxw=470, maxh=470)),
    ("J", dict(out="02_minitree_tritan_bottle", img=HQ + "08.png", tag="BABY  •  3+ MONTHS", title="Minitree Tritan Baby Bottle",
               feats=["BPA Free Tritan", "210 ml (7 oz)", "Soft Nipple", "Easy Grip Handles"], price=450, regular=600,
               bg=(122, 84, 140), stage=(246, 236, 244), acc=(226, 108, 140), maxw=760, maxh=470, cy=470)),
    ("I", dict(out="03_forkan_trolley_luggage", img=HQ + "05.png", word="TRAVEL", tag="TRAVEL  •  20 & 24 INCH", title="FORKAN Trolley Luggage",
               sub="Premium hard shell  •  Ask for sizes and colours", feats=["Hard Shell", "360° Wheels", "Lightweight"],
               price=4000, regular=5500, label="FROM", bg=(244, 236, 222), col=(34, 96, 92), stampc=(196, 88, 60), maxw=400, maxh=500, cy=600)),
    ("J", dict(out="04_massage_gun", img=HQ + "31.png", tag="SELF CARE  •  RECHARGEABLE", title="Portable Massage Gun",
               feats=["4 Massage Heads", "Powerful, Quiet Motor", "Lightweight Design", "Rechargeable"], price=850, regular=1200,
               bg=(46, 70, 60), stage=(232, 242, 234), acc=(232, 140, 60), maxw=560, maxh=560)),
]

if __name__ == "__main__":
    keys = sys.argv[1:]
    for kind, p in POSTS:
        if keys and p["out"][:2] not in keys: continue
        p["img"] = im(p["img"])
        T[kind](p)
