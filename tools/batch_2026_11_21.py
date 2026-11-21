"""Everyday Cart daily batch, 21 Nov 2026. NEW style set 16 (render_styles16: AG die-cut sticker sheet, AH film strip).
5 image posts + 1 Reel."""
import os, sys
import render_flat as rf
from render_flat import im, HQ, FL
from render_styles16 import TEMPLATES16 as T
rf.OUTDIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "posts", "batch-2026-11-21")) + "/"
os.makedirs(rf.OUTDIR, exist_ok=True)

POSTS = [
    ("AG", dict(out="01_colmi_p81_watch", img=HQ + "09.png", tag="CALLING SMART WATCH", head=["Calls, steps, sports:", "all on your wrist"],
                title="COLMI P81 Calling Smartwatch", bn="হাতের স্মার্ট ওয়াচেই কল আর ফিটনেস",
                feats=["1.9 inch HD display", "Bluetooth calling", "100+ sports modes", "IP68, 300mAh battery"],
                price=1350, regular=1540, spec=("100+", "SPORTS MODES"), maxw=470, maxh=500, cx=420, cy=610,
                bg=(255, 208, 72), acc=(234, 66, 98), acc2=(46, 92, 214), ink=(26, 26, 38))),
    ("AH", dict(out="02_baby_care_kit", img=FL + "baby_kit_stack.png", tag="NEWBORN CARE", head=["Newborn care,", "all in one box"],
                title="10 Pc Baby Care Kit (Pink and Sky Blue)", bn="নবজাতকের যত্নে দরকারি সব এক বেবি কেয়ার কিটে",
                feats=["Nail care tools", "Hair brush and comb", "Thermometer", "Nasal aspirator"],
                side=[("10", "PIECES IN ONE KIT"), ("2", "PINK OR SKY BLUE")], price=480, regular=650,
                bg=(44, 52, 112), acc=(255, 156, 190), frames=[(255, 236, 242), (214, 236, 255), (255, 244, 214)])),
    ("AG", dict(out="03_winter_bottles", tag="WINTER FLASKS", head=["Hot tea on the go?", "Pick your flask"],
                title="Premium Thermal Water Bottle + Smart LED Bottle", bn="শীতে গরম চা কফির জন্য পছন্দের ফ্লাস্ক",
                feats=["600 ml, flip top lid, straw", "Comfortable side handle", "500 ml, LED temperature lid", "Double wall, Black or White"],
                items=[dict(img=HQ + "18.png", cx=270, cy=590, mw=300, mh=440, ang=-4, name="Thermal Bottle 600 ml", price=800, regular=1250, px=470, py=720, pang=-5),
                       dict(img=HQ + "19.png", cx=770, cy=610, mw=330, mh=400, ang=4, name="Smart LED Bottle 500 ml", price=350, regular=700, px=935, py=300, pang=7)],
                price=350, bg=(150, 204, 250), acc=(236, 80, 56), acc2=(30, 60, 150), ink=(20, 30, 60))),
    ("AG", dict(out="04_auto_umbrella", img=HQ + "23.png", tag="SUN AND RAIN", head=["Winter sun or rain?", "Open with one press"],
                title="Full Automatic Folding Umbrella", bn="রোদ বা বৃষ্টিতে সঙ্গী অটো ছাতা",
                feats=["One press to open and close", "Dual purpose: sun and rain", "Strong frame", "Compact folding size"],
                price=900, regular=1400, spec=("AUTO", "OPEN AND CLOSE"), maxw=300, maxh=540, cx=400, cy=600, ang=-12,
                bg=(255, 150, 120), acc=(36, 44, 110), acc2=(0, 150, 136), ink=(30, 26, 40))),
    ("AH", dict(out="05_oraimo_spacebuds_lite", img=HQ + "13.png", tag="WIRELESS EARBUDS", head=["Late night playlist?", "Up to 40 hours"],
                title="Oraimo SpaceBuds Lite (Official)", bn="কেসসহ ৪০ ঘণ্টা পর্যন্ত গান শুনুন এই ইয়ারবাডে",
                feats=["Sound360 spatial audio", "AI call noise cancellation", "Bluetooth 5.4, IPX4", "10 mm driver"],
                side=[("40H", "PLAYTIME WITH CASE"), ("5.4", "BLUETOOTH")], price=1310, regular=1496,
                bg=(20, 92, 84), acc=(196, 240, 90), frames=[(232, 246, 240), (255, 236, 200), (220, 230, 255)])),
]

if __name__ == "__main__":
    keys = sys.argv[1:]
    for kind, p in POSTS:
        if keys and p["out"][:2] not in keys: continue
        if "img" in p and isinstance(p["img"], str): p["img"] = im(p["img"])
        for it in p.get("items", []):
            if isinstance(it["img"], str): it["img"] = im(it["img"])
        T[kind](p)
