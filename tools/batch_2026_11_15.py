"""Everyday Cart daily batch, 15 Nov 2026. NEW style set 10 (render_styles10: U hang tag poster, V chat inbox).
5 image posts + 1 Reel."""
import os, sys
import render_flat as rf
from render_flat import im, HQ, FL
from render_styles10 import TEMPLATES10 as T
rf.OUTDIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "posts", "batch-2026-11-15")) + "/"
os.makedirs(rf.OUTDIR, exist_ok=True)

POSTS = [
    ("U", dict(out="01_oraimo_necklace_lite", img=HQ + "04.png", tag="NECKBAND", head=["30 hours of music,", "right around your neck"],
               word="NECKBAND", title="Oraimo Necklace Lite ENC Wireless Neckband (Official)",
               bn="সারাদিন গান শোনার হালকা নেকব্যান্ড",
               feats=["Up to 30 hours playtime", "ENC for clear calls", "Dual device connectivity", "Call vibration alert"],
               price=1300, regular=1485, maxw=440, maxh=600, cx=390, cy=705, r=285,
               bg=(22, 44, 88), band=(30, 60, 116), acc=(255, 196, 64))),
    ("V", dict(out="02_baby_toilet_seat", img=HQ + "28.png", tag="POTTY TRAINING", head=["Potty training,", "made easy"],
               title="Soft Cushioned Baby Toilet Seat Reducer with Handles",
               maxw=450, maxh=380, dx=0,
               chat=[("q", "দাম কত?"), ("price", None), ("q", "কী কী সুবিধা আছে?"),
                     ("feats", ["Soft cushioned seat", "Secure handles and splash guard", "Waterproof and easy to clean",
                                "For 18 months and above"]),
                     ("q", "অর্ডার করব কীভাবে?"), ("a", "Inbox us or visit everydaycart.online")],
               price=800, regular=1000, bg=(255, 226, 236), acc=(226, 64, 122), panel=(255, 244, 248))),
    ("U", dict(out="03_insulated_lunch_box", img=HQ + "26.png", tag="LUNCH BOX", head=["Hot homemade lunch,", "anywhere you go"],
               word="LUNCH", title="Premium 3 Layer Stainless Steel Insulated Lunch Box",
               bn="অফিস বা স্কুলে গরম খাবারের লাঞ্চ বক্স",
               feats=["Hot or cold up to 12 hours", "2.6L large capacity", "Food grade stainless steel", "Leak proof design"],
               price=3000, regular=4500, maxw=540, maxh=560, cx=390, cy=705, r=285, dy=6,
               bg=(196, 84, 52), band=(214, 104, 70), acc=(255, 226, 150))),
    ("V", dict(out="04_awei_t88", img=HQ + "11.png", tag="EARBUDS", head=["Earbuds under", "Tk 1,000"],
               title="Awei T88 Wireless Earbuds, Black",
               maxw=290, maxh=390, dx=0,
               chat=[("q", "দাম কত?"), ("price", None), ("q", "ইয়ারবাডে কী কী আছে?"),
                     ("feats", ["ANC support", "IPX6 water resistant", "Bluetooth 5.4, touch control", "1 hour fast charging"]),
                     ("q", "অর্ডার করব কীভাবে?"), ("a", "Inbox us or visit everydaycart.online")],
               price=990, regular=1450, bg=(220, 246, 232), acc=(18, 140, 96), panel=(240, 252, 245))),
    ("U", dict(out="05_kodomo_oral_care", tag="KIDS CARE", head=["Tiny teeth,", "happy brushing"],
               word="KODOMO", wy=372, title="Kodomo Baby Toothpaste and Kodomo Toothbrush",
               bn="বাচ্চার টুথপেস্ট আর টুথব্রাশ একসাথে",
               feats=["1000 ppm fluoride + xylitol", "Sugar free orange cream", "Soft gentle bristles", "Brush for 0.5 to 3 years"],
               items=[dict(img=FL + "kodomo_brush.png", ox=-70, oy=-30, mw=330, mh=440, name="Kodomo Toothbrush", price=200, regular=400),
                      dict(img=FL + "kodomo_paste.png", ox=10, oy=190, mw=460, mh=130, name="Kodomo Baby Toothpaste", price=280, regular=400)],
               cx=390, cy=700, r=285, bg=(64, 156, 214), band=(84, 172, 226), acc=(255, 140, 64), th=420)),
]

if __name__ == "__main__":
    keys = sys.argv[1:]
    for kind, p in POSTS:
        if keys and p["out"][:2] not in keys: continue
        if "img" in p and isinstance(p["img"], str): p["img"] = im(p["img"])
        for it in p.get("items", []):
            if isinstance(it["img"], str): it["img"] = im(it["img"])
        T[kind](p)
