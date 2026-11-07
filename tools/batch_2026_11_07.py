"""Everyday Cart daily batch, 7 Nov 2026. Style set 3 (G slanted colour block, H framed label card), new colourways,
struck regular price added to both templates."""
import os, sys
import render_flat as rf
from render_flat import im, HQ, FL
from render_styles3 import TEMPLATES3
rf.OUTDIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "posts", "batch-2026-11-07")) + "/"
os.makedirs(rf.OUTDIR, exist_ok=True)
FOREST = (52, 98, 78); INDIGO = (64, 72, 140); BERRY = (150, 60, 96); OCHRE = (184, 128, 52); SLATE = (58, 74, 92)
CORAL = (226, 108, 92); MINT = (70, 150, 130)

POSTS = [
    ("H", dict(out="01_insulated_lunch_box", img=HQ + "26.png", tag="KITCHEN  •  OFFICE LUNCH", title="Insulated Lunch Box",
               feats=["3 Layer Steel", "2.6L Capacity", "Leak Proof"], price=3000, regular=4500,
               acc=OCHRE, edge=FOREST, halo=(236, 244, 238), bg=(232, 238, 232), maxw=430, maxh=400)),
    ("G", dict(out="02_oraimo_necklace_lite", img=HQ + "04.png", tag="NECKBAND  •  OFFICIAL", title="Oraimo Necklace Lite",
               sub="ENC wireless neckband", feats=["30 Hrs Playtime", "ENC Calls", "Dual Device", "Call Vibration"],
               price=1300, regular=1485, col=INDIGO, maxw=440, maxh=440)),
    ("H", dict(out="03_kodomo_lotion_powder", img=FL + "kodomo_lotion.png", tag="BABY  •  SKIN CARE", title="Kodomo Lotion Powder",
               feats=["180 ml", "Extra Mild", "0+ Months"], price=720, regular=880,
               acc=CORAL, edge=(90, 140, 190), halo=(234, 243, 252), bg=(236, 242, 248), maxw=280, maxh=360)),
    ("G", dict(out="04_baby_toilet_seat", img=HQ + "28.png", tag="BABY  •  POTTY TRAINING", title="Baby Toilet Seat Reducer",
               sub="Soft cushioned  •  18+ months", feats=["Secure Handles", "Splash Guard", "Easy to Clean"],
               price=800, regular=1000, col=MINT, tagc=(255, 240, 200), maxw=440, maxh=400)),
    ("H", dict(out="05_smart_led_bottle", img=HQ + "19.png", tag="THERMAL  •  BLACK & WHITE", title="Smart LED Temperature Bottle",
               feats=["500 ml", "LED Display", "Hot or Cold"], price=350, regular=700,
               acc=BERRY, edge=SLATE, halo=(236, 238, 244), bg=(230, 232, 238), maxw=360, maxh=390)),
    ("G", dict(out="06_portable_bbq_grill", img=HQ + "27.png", tag="WINTER BBQ NIGHTS", title="Portable BBQ Grill Machine",
               sub="Picnics, camping & rooftop BBQ", feats=["Durable Steel Body", "Charcoal Tray", "Air Blower"],
               price=5500, regular=9500, col=(150, 62, 44), tagc=(255, 206, 150), maxw=460, maxh=430)),
    ("H", dict(out="07_baby_care_kit", img=HQ + "21.png", tag="BABY  •  NEWBORN CARE", title="10 Pc Baby Care Kit",
               feats=["Nail Care", "Hair Brush & Comb", "Thermometer"], price=480, regular=650,
               acc=(214, 96, 140), edge=(120, 100, 160), halo=(246, 238, 250), bg=(242, 236, 246), maxw=520, maxh=420)),
    ("G", dict(out="08_awei_t88_earbuds", img=HQ + "11.png", tag="EARBUDS", title="Awei T88 Wireless Earbuds",
               sub="Wireless  •  Bluetooth", feats=["ANC Support", "IPX6"], price=990, regular=1450,
               col=SLATE, tagc=(170, 220, 255), maxw=420, maxh=420)),
    ("H", dict(out="09_automatic_umbrella", img=HQ + "23.png", tag="EVERYDAY  •  SUN & RAIN", title="Full Automatic Umbrella",
               feats=["Auto Open & Close", "Strong Frame", "Compact Fold"], price=900, regular=1400,
               acc=INDIGO, edge=OCHRE, halo=(250, 242, 228), bg=(246, 238, 226), maxw=200, maxh=370)),
    ("G", dict(out="10_cleaning_gloves", img=HQ + "29.png", tag="HOME  •  KITCHEN", title="Premium Cleaning Gloves",
               sub="Waterproof  •  Reusable", feats=["Waterproof", "Long Floral Cuff", "Reusable"],
               price=200, regular=400, col=BERRY, maxw=380, maxh=440)),
]

if __name__ == "__main__":
    keys = sys.argv[1:]
    for kind, p in POSTS:
        if keys and p["out"][:2] not in keys: continue
        p["img"] = im(p["img"]); TEMPLATES3[kind](p)
