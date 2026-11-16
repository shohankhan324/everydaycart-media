"""Everyday Cart daily batch, 16 Nov 2026. NEW style set 11 (render_styles11: W shop shelf, X neo brutal).
5 image posts + 1 Reel."""
import os, sys
import render_flat as rf
from render_flat import im, HQ, FL
from render_styles11 import TEMPLATES11 as T
rf.OUTDIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "posts", "batch-2026-11-16")) + "/"
os.makedirs(rf.OUTDIR, exist_ok=True)

POSTS = [
    ("X", dict(out="01_oraimo_watch_5_lite", img=HQ + "02.png", tag="SMART WATCH", head=["Take calls right", "from your wrist"],
               title="Oraimo Watch 5 Lite Smart Watch (Official)", bn="কল ধরুন হাতের স্মার্ট ওয়াচ থেকেই",
               feats=['2.01" HD display', "HD voice calling", "IP68 dust and water resistant", "105+ sports modes"],
               price=1650, regular=1870, sticker="7 DAYS BATTERY", maxw=470, maxh=500, pcx=330,
               bg=(226, 232, 255), acc=(196, 255, 84), acc2=(255, 176, 128))),
    ("W", dict(out="02_baby_care_kit", img=FL + "baby_kit_stack.png", tag="NEWBORN CARE", head=["Everything for", "newborn care"],
               title="10 Pc Baby Care Kit, Pink and Sky Blue", bn="নবজাতকের যত্নে ১০ পিসের বেবি কেয়ার কিট",
               feats=["Nail care tools", "Hair brush and comb", "Thermometer", "Nasal aspirator"],
               price=480, regular=650, cx=500, maxw=400, maxh=430, lx=800,
               bg=(255, 232, 238), acc=(232, 96, 140), board=(48, 66, 92))),
    ("X", dict(out="03_winter_flask_duo", tag="WINTER PICKS", head=["Hot tea on the go?", "Pick your flask"],
               title="316 Thermal Bottle 700 ml + Premium Thermal Tumbler 860 ml", bn="শীতে গরম চা কফির জন্য ফ্লাস্ক",
               feats=["316 stainless steel bottle", "Bottle: safety lock lid", "Tumbler: straw and handle", "Double wall vacuum tumbler"],
               items=[dict(img=HQ + "17.png", cx=300, mw=230, mh=440, dy=-55, name="Bottle 700 ml", price=800),
                      dict(img=HQ + "16.png", cx=700, mw=460, mh=440, dy=-55, name="Tumbler 860 ml", price=800)],
               pcx=515, bg=(255, 240, 214), acc=(255, 140, 76), acc2=(130, 214, 200))),
    ("W", dict(out="04_steel_water_pot", img=HQ + "32.png", tag="HOME AND KITCHEN", head=["Tea time for", "the whole family"],
               title="Stainless Steel Water Pot, Insulated", bn="চা কফি আর পানি রাখার স্টিলের ওয়াটার পট",
               feats=["Double wall insulated", "Leak-proof lid", "Ergonomic handle", "Modern matte finish"],
               price=1000, regular=1400, cx=500, maxw=360, maxh=430, lx=800,
               bg=(222, 238, 246), acc=(34, 92, 160), board=(38, 58, 50))),
    ("X", dict(out="05_silent_alarm_clock", img=HQ + "07.png", tag="BEDSIDE", head=["No ticking sound,", "just sweet sleep"],
               title="Silent Alarm Clock, Twin Bell Design", bn="টিকটিক শব্দ ছাড়া অ্যালার্ম ঘড়ি",
               feats=["Non ticking, silent", "Precise quartz movement", "Classic twin bell design", "Elegant bedside decor"],
               price=500, regular=800, sticker="NO TICKING", maxw=440, maxh=480, pcx=330,
               bg=(214, 244, 230), acc=(255, 206, 84), acc2=(160, 150, 255))),
]

if __name__ == "__main__":
    keys = sys.argv[1:]
    for kind, p in POSTS:
        if keys and p["out"][:2] not in keys: continue
        if "img" in p and isinstance(p["img"], str): p["img"] = im(p["img"])
        for it in p.get("items", []):
            if isinstance(it["img"], str): it["img"] = im(it["img"])
        T[kind](p)
