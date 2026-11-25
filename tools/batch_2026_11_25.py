"""Everyday Cart daily batch, 25 Nov 2026. NEW style set 20 (render_styles20: AO shopping bag poster, AP flat landscape scene).
4 image posts + 1 Reel."""
import os, sys
import render_flat as rf
from render_flat import im, HQ, FL
from render_styles20 import TEMPLATES20 as T
rf.OUTDIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "posts", "batch-2026-11-25")) + "/"
os.makedirs(rf.OUTDIR, exist_ok=True)

POSTS = [
    ("AO", dict(out="01_awei_t108_earbuds", img=HQ + "10.png", tag="WIRELESS EARBUDS", head=["ENC earbuds for", "clear calls"],
                title="Awei T108 Wireless Earbuds (Official), Black", bn="কল হবে ক্লিয়ার এই ইয়ারবাডে",
                feats=["ENC for clear calls", "13mm drivers", "6h buds, 20h with case", "Bluetooth 5.3, Type C"],
                price=950, regular=1199, spec=("20h", "WITH CASE"), maxw=360, maxh=380,
                bg=(36, 64, 190), bag=(252, 248, 240), acc=(255, 138, 40), circ=(255, 226, 196))),
    ("AP", dict(out="02_baby_care_kit", img=HQ + "21.png", tag="NEWBORN CARE", head=["Newborn care,", "all in one box"],
                title="10 Pc Baby Care Kit (Pink and Sky Blue)", bn="নবজাতকের যত্নে বেবি কেয়ার কিট",
                feats=["Nail care tools", "Hair brush and comb", "Thermometer", "Nasal aspirator"],
                price=480, regular=650, spec=("10", "PIECES"), maxw=690, maxh=330, pcx=410, sign_x=915,
                sky=(198, 230, 252), sun=(255, 214, 90), hill_b=(190, 232, 200), hill_f=(128, 200, 156), acc=(236, 88, 132),
                clouds=[(60, 330, 1.0), (560, 520, 0.7)])),
    ("AO", dict(out="03_winter_tea_pot_bottle", tag="WINTER TEA TIME", head=["Tea at home,", "tea on the go"],
                title="Stainless Steel Water Pot + Smart LED Temperature Bottle", bn="শীতে গরম চায়ের জন্য স্টিলের জগ আর ফ্লাস্ক",
                feats=["Pot: double wall insulated", "Pot: leak proof lid", "Bottle: LED temperature lid", "Bottle: Black or White"],
                items=[dict(img=HQ + "32.png", name="Steel Water Pot", price=1000, r=145, mw=220, mh=290, cy=650),
                       dict(img=HQ + "19.png", name="Smart LED Bottle 500 ml", price=350, r=145, mw=240, mh=285, cy=650)],
                price=350, plabel="FROM", seal_r=96, seal_x=905, seal_y=470, seal_ang=8,
                bg=(196, 82, 56), bag=(232, 198, 148), band=(40, 104, 108), acc=(40, 104, 108), circ=(250, 236, 214), sealc=(255, 210, 80),
                h2c=(255, 214, 120))),
    ("AP", dict(out="04_oraimo_spacebox_speaker", img=HQ + "01.png", tag="BLUETOOTH SPEAKER", head=["Winter night adda,", "light show on"],
                title="Oraimo SpaceBox Portable Bluetooth Speaker (Official)", bn="আড্ডা জমাতে লাইট শো ব্লুটুথ স্পিকার",
                feats=["Personalized light show", "Thumping bass", "8W output, 45mm driver", "1800mAh battery"],
                price=1841, regular=2299, spec=("8W", "AUDIO OUTPUT"), maxw=560, maxh=320, pcx=400, sign_x=895, night=True,
                sky=(38, 34, 98), sun=(255, 240, 196), hill_b=(66, 58, 150), hill_f=(22, 98, 110), acc=(255, 84, 160),
                cloud=(70, 64, 140), clouds=[(60, 360, 0.9), (520, 560, 0.6)], board=(255, 214, 90))),
]

if __name__ == "__main__":
    keys = sys.argv[1:]
    for kind, p in POSTS:
        if keys and p["out"][:2] not in keys: continue
        if "img" in p and isinstance(p["img"], str): p["img"] = im(p["img"])
        for it in p.get("items", []):
            if isinstance(it["img"], str): it["img"] = im(it["img"])
        T[kind](p)
