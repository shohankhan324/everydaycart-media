"""Everyday Cart daily batch, 4 Nov 2026. Style set 3 (G slanted colour block, H framed label card)."""
import os, sys
import render_flat as rf
from render_flat import im, HQ
from render_styles3 import TEMPLATES3
rf.OUTDIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "posts", "batch-2026-11-04")) + "/"
os.makedirs(rf.OUTDIR, exist_ok=True)
TEAL = (44, 110, 120); PLUM = (120, 80, 120); CLAY = (176, 104, 80); NAVY = (40, 58, 96)

POSTS = [
    ("G", dict(out="01_insulated_lunch_box", img=HQ + "26.png", tag="KITCHEN", title="Insulated Lunch Box", sub="3 layer stainless steel  •  2.6L",
               feats=["Hot or Cold up to 12 Hrs", "Leak Proof", "Food Grade Steel", "Carry Handle"], price=3000, col=TEAL, maxw=430, maxh=430)),
    ("H", dict(out="02_elephant_plush_toy", img=HQ + "25.png", tag="SOFT TOY  •  GIFT", title="Elephant Plush Soft Toy",
               feats=["18 Inch", "Super Soft", "Cute Gift"], price=750, acc=ROSE_ if False else (196, 120, 140), edge=(150, 150, 165), halo=(240, 238, 246), maxw=420, maxh=420)),
    ("G", dict(out="03_portable_cooling_fan", img=HQ + "24.png", tag="GADGET", title="Portable Turbo Cooling Fan", sub="Handheld  •  High speed airflow",
               feats=["High Speed", "Fast Heat Dissipation", "Long Battery", "Pocket Size"], price=450, col=NAVY, maxw=300, maxh=460)),
    ("H", dict(out="04_baby_toilet_seat", img=HQ + "28.png", tag="BABY  •  POTTY TRAINING", title="Soft Cushioned Toilet Seat Reducer",
               feats=["Secure Handles", "Splash Guard", "18+ Months"], price=800, acc=(214, 90, 130), edge=(214, 90, 130), halo=(253, 236, 242), maxw=470, maxh=400)),
    ("G", dict(out="05_automatic_umbrella", img=HQ + "23.png", tag="EVERYDAY", title="Full Automatic Folding Umbrella", sub="Sun & rain  •  Strong frame",
               feats=["Auto Open & Close", "Dual Purpose", "Compact Fold"], price=900, col=CLAY, maxw=200, maxh=470)),
    ("H", dict(out="06_wide_neck_baby_feeder", img=HQ + "30.png", tag="BABY  •  FEEDING", title="Wide Neck Baby Feeder",
               feats=["Anti Colic Nipple", "BPA Free", "Easy to Clean"], price=450, acc=(230, 100, 120), edge=(110, 150, 120), halo=(253, 238, 240), maxw=470, maxh=380)),
    ("G", dict(out="07_portable_bbq_grill", img=HQ + "27.png", tag="OUTDOOR", title="Portable BBQ Grill Machine", sub="Picnics, camping & rooftop BBQ",
               feats=["Durable Steel Body", "Adjustable Charcoal Tray", "Manual Air Blower"], price=5500, col=(60, 60, 64), tagc=(255, 190, 120), maxw=460, maxh=430)),
    ("H", dict(out="08_cleaning_gloves", img=HQ + "29.png", tag="HOME  •  KITCHEN", title="Premium Cleaning Gloves",
               feats=["Waterproof", "Long Floral Cuff", "Reusable"], price=200, acc=(214, 90, 130), edge=SAGE_ if False else (98, 120, 92), halo=(253, 238, 244), maxw=400, maxh=420)),
]

if __name__ == "__main__":
    keys = sys.argv[1:]
    for kind, p in POSTS:
        if keys and p["out"][:2] not in keys: continue
        p["img"] = im(p["img"]); TEMPLATES3[kind](p)
