"""Everyday Cart daily batch, 20 Nov 2026. NEW style set 15 (render_styles15: AE Bauhaus geometric poster, AF file folder card).
5 image posts + 1 Reel."""
import os, sys
import render_flat as rf
from render_flat import im, HQ, FL
from render_styles15 import TEMPLATES15 as T
rf.OUTDIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "posts", "batch-2026-11-20")) + "/"
os.makedirs(rf.OUTDIR, exist_ok=True)

POSTS = [
    ("AE", dict(out="01_oraimo_watch_5_lite", img=HQ + "02.png", tag="CALLING SMART WATCH", head=["Take the call", "right from your wrist"],
                title="Oraimo Watch 5 Lite Smart Watch (Official)", bn="হাতের স্মার্ট ওয়াচ থেকেই কল ধরুন",
                feats=["2.01\" HD display", "HD voice in calls", "IP68, 105+ sports modes", "Up to 7 days battery"],
                price=1650, regular=1870, sticker="AI WATCH FACES", maxw=400, maxh=460,
                paper=(246, 242, 232), c1=(36, 72, 200), c2=(236, 84, 52), c3=(246, 190, 40))),
    ("AF", dict(out="02_baby_toilet_seat", img=HQ + "28.png", tag="POTTY TRAINING", head=["Big toilet,", "little hero"],
                title="Soft Cushioned Baby Toilet Seat Reducer with Handles", bn="পটি ট্রেনিং সহজ করতে নরম টয়লেট সিট",
                feats=["Soft cushioned seat", "Secure handles", "Splash guard", "Waterproof, easy to clean"],
                price=800, regular=1000, sticker="FOR 18 MONTHS+",
                bg=(196, 226, 246), folder=(255, 214, 178), acc=(232, 86, 104), note=(255, 236, 130),
                tabs=[(232, 86, 104), (72, 150, 220), (120, 196, 140)])),
    ("AE", dict(out="03_winter_flask_duo", tag="WINTER TEA TIME", head=["Morning cha,", "your way"],
                title="316 Steel Thermal Bottle + Premium Thermal Tumbler", bn="শীতের সকালে গরম চা রাখুন পছন্দের ফ্লাস্কে",
                feats=["Bottle: 700 ml, 316 stainless steel", "Bottle: safety lock lid", "Tumbler: 860 ml, double wall",
                       "Tumbler: handle and reusable straw"],
                items=[dict(img=HQ + "17.png", cx=290, cy=560, r=200, mw=230, mh=330, name="Thermal Bottle 700 ml", price=800, regular=1100),
                       dict(img=HQ + "16.png", cx=790, cy=560, r=200, mw=300, mh=340, name="Thermal Tumbler 860 ml", price=800, regular=1200)],
                price=800, paper=(250, 244, 234), c1=(32, 110, 82), c2=(222, 112, 44), c3=(244, 196, 186), ink=(30, 34, 30), band_y=930)),
    ("AF", dict(out="04_massage_gun", img=HQ + "31.png", tag="AFTER GYM AND OFFICE", head=["Sore shoulders?", "Relax at home"],
                title="Portable Rechargeable Massage Gun", bn="ক্লান্ত শরীরে ঘরেই আরাম দিন ম্যাসাজ গানে",
                feats=["4 interchangeable heads", "Powerful yet quiet motor", "Lightweight, ergonomic", "Rechargeable, portable"],
                price=850, regular=1200, sticker="4 MASSAGE HEADS",
                bg=(44, 48, 64), folder=(206, 230, 110), back=(150, 176, 60), acc=(112, 62, 204), note=(255, 255, 255),
                photo_bg=(236, 230, 252), tabs=[(255, 120, 90), (120, 200, 255), (255, 210, 60)], ink=(26, 28, 38), foot=(255, 255, 255))),
    ("AE", dict(out="05_home_helpers_pot_gloves", tag="HOME HELPERS", head=["Tea is hot,", "hands stay dry"],
                title="Stainless Steel Water Pot + Premium Cleaning Gloves", bn="ঘরের কাজে স্টিলের জগ আর ক্লিনিং গ্লাভস",
                feats=["Pot: double wall insulated", "Pot: leak proof lid", "Gloves: waterproof soft rubber", "Gloves: long cuffs, reusable"],
                items=[dict(img=HQ + "32.png", cx=300, cy=560, r=205, mw=280, mh=330, name="Stainless Water Pot", price=1000, regular=1400),
                       dict(img=HQ + "29.png", cx=790, cy=560, r=205, mw=300, mh=330, name="Cleaning Gloves", price=200, regular=400)],
                price=200, paper=(240, 244, 250), c1=(110, 170, 232), c2=(30, 52, 112), c3=(255, 206, 60), ink=(24, 30, 56), band_y=930)),
]

if __name__ == "__main__":
    keys = sys.argv[1:]
    for kind, p in POSTS:
        if keys and p["out"][:2] not in keys: continue
        if "img" in p and isinstance(p["img"], str): p["img"] = im(p["img"])
        for it in p.get("items", []):
            if isinstance(it["img"], str): it["img"] = im(it["img"])
        T[kind](p)
