"""Everyday Cart daily batch, 8 Nov 2026. Style set 2 (D arch poster, E scalloped header + feature tiles, F list menu)
in new colourways (deep teal, plum, terracotta, navy heads; peach, mint, lilac, butter backgrounds)."""
import os, sys
import render_flat as rf
from render_flat import im, HQ, FL
from render_styles import TEMPLATES
rf.OUTDIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "posts", "batch-2026-11-08")) + "/"
os.makedirs(rf.OUTDIR, exist_ok=True)
TEAL = (30, 104, 110); PLUM = (110, 62, 110); TERRA = (178, 92, 64); NAVY = (44, 62, 108); BERRY = (150, 60, 96)

POSTS = [
    ("D", dict(out="01_oraimo_spacebuds_lite", img=HQ + "13.png", tag="EARBUDS  •  OFFICIAL", title="Oraimo SpaceBuds Lite",
               feats=["Sound360 Spatial Audio", "40 Hrs with Case", "IPX4"], price=1310, regular=1496,
               bg=(222, 236, 238), arch=(250, 252, 252), rule=(190, 214, 216), ink=TEAL, maxw=500, maxh=540)),
    ("E", dict(out="02_big_mac_thermos_cup", img=HQ + "15.png", tag="THERMAL  •  1000 ML", title="Big Mac 316 Thermos Cup",
               sub="316 Stainless Steel  •  Blue", feats=["1000 ml Capacity", "316 Stainless Steel", "Carry Handle", "Leak Resistant Lid"],
               price=1000, regular=1300, head=NAVY, ribbon=(214, 120, 70), bg=(244, 242, 236), accent=(226, 236, 248), maxw=300, maxh=500)),
    ("D", dict(out="03_minitree_duckbill_mumpot", img=HQ + "20.png", tag="BABY  •  PINK & SKY BLUE", title="Minitree Duckbill Mumpot",
               feats=["280 ml", "Two Easy Grip Handles", "3+ Months"], price=400, regular=550,
               bg=(250, 234, 226), arch=(255, 250, 246), rule=(232, 206, 194), ink=TERRA, maxw=700, maxh=420)),
    ("E", dict(out="04_portable_cooling_fan", img=HQ + "24.png", tag="GADGET  •  HANDHELD", title="Portable Turbo Cooling Fan",
               sub="Pocket friendly  •  High speed airflow", feats=["High Speed Airflow", "Fast Heat Dissipation", "Long Endurance", "Handheld Size"],
               price=450, regular=750, head=TEAL, ribbon=(232, 150, 60), bg=(240, 246, 244), accent=(226, 242, 238), maxw=260, maxh=500)),
    ("F", dict(out="05_little_ones_essentials", tag="BABY CARE", title="Little Ones' Essentials", sub="Gentle picks for feeding and brushing",
               bg=(242, 238, 248),
               items=[dict(img=FL + "kodomo_paste.png", name="Kodomo Baby Toothpaste", note="1000 ppm Fluoride  •  Sugar free", price=280, regular=400, accent=(255, 236, 222)),
                      dict(img=FL + "kodomo_brush.png", name="Kodomo Toothbrush", note="Soft bristles  •  0.5 to 3 yrs", price=200, regular=400, accent=(228, 240, 252)),
                      dict(img=HQ + "22.png", name="Minitree 120 ml Feeding Bottle", note="Ergonomic handles  •  6m+", price=450, regular=600, accent=(236, 246, 234)),
                      dict(img=HQ + "30.png", name="Wide Neck Baby Feeder", note="Anti colic nipple  •  BPA free", price=450, regular=700, accent=(250, 234, 240))])),
    ("D", dict(out="06_premium_thermal_water_bottle", img=HQ + "18.png", tag="THERMAL  •  600 ML", title="Premium Thermal Water Bottle",
               feats=["Leak Proof Flip Lid", "Built in Straw", "Side Handle"], price=800, regular=1250,
               bg=(236, 232, 246), arch=(252, 250, 255), rule=(212, 204, 230), ink=PLUM, maxw=330, maxh=560)),
    ("E", dict(out="07_silent_alarm_clock", img=HQ + "07.png", tag="HOME  •  BEDSIDE", title="Silent Alarm Clock",
               sub="Non ticking  •  Classic twin bell design", feats=["Silent, Non Ticking", "Quartz Movement", "Twin Bell Design", "Bedside Decor"],
               price=500, regular=800, head=TERRA, ribbon=NAVY, bg=(250, 244, 236), accent=(246, 232, 220), maxw=380, maxh=500)),
    ("D", dict(out="08_elephant_plush_toy", img=HQ + "25.png", tag="TOYS  •  18 INCH", title="Elephant Plush Soft Toy",
               feats=["18 Inch Size", "Soft & Huggable", "Sweet Gift"], price=750, regular=1100,
               bg=(250, 242, 218), arch=(255, 252, 244), rule=(232, 218, 180), ink=BERRY, maxw=470, maxh=560)),
]

if __name__ == "__main__":
    keys = sys.argv[1:]
    for kind, p in POSTS:
        if keys and p["out"][:2] not in keys: continue
        if "img" in p: p["img"] = im(p["img"])
        for it in p.get("items", []): it["img"] = im(it["img"])
        TEMPLATES[kind](p)
