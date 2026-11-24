"""Everyday Cart daily batch, 24 Nov 2026. NEW style set 19 (render_styles19: AM gift ribbon poster, AN Memphis window poster).
5 image posts + 1 Reel."""
import os, sys
import render_flat as rf
from render_flat import im, HQ, FL
from render_styles19 import TEMPLATES19 as T
rf.OUTDIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "posts", "batch-2026-11-24")) + "/"
os.makedirs(rf.OUTDIR, exist_ok=True)

POSTS = [
    ("AM", dict(out="01_oraimo_watch_5_lite", img=HQ + "02.png", tag="CALLING SMART WATCH", head=["A gift that", "takes calls"],
                title="Oraimo Watch 5 Lite Calling Smart Watch (Official)", bn="প্রিয়জনকে উপহার দিন কলিং স্মার্ট ওয়াচ",
                feats=['2.01" HD display', "HD voice in calls", "IP68 dust and water resistant", "Up to 7 days battery"],
                price=1650, regular=1870, spec=("105+", "SPORTS MODES"), maxw=380, maxh=430, ang=-4,
                bg=(30, 44, 100), rib=(255, 204, 82), acc=(30, 44, 100))),
    ("AN", dict(out="02_baby_toilet_seat", img=HQ + "28.png", tag="POTTY TRAINING", head=["Potty time,", "made comfy"],
                title="Soft Cushioned Baby Toilet Seat Reducer with Handles", bn="বাচ্চার পটি ট্রেনিংয়ে নরম টয়লেট সিট",
                feats=["Soft cushioned seat", "Secure handles to hold", "Splash guard", "Waterproof, easy to clean"],
                price=800, regular=1000, spec=("18M+", "FOR AGES"), maxw=470, maxh=400, dx=-6,
                bg=(212, 242, 228), win=(186, 172, 250), circ=(255, 230, 120), acc=(255, 98, 78), c2=(255, 214, 70), c3=(56, 46, 150))),
    ("AN", dict(out="03_winter_flask_duo", tag="WINTER TEA TIME", head=["Hot cha all day,", "Tk 800 each"],
                title="316 Steel Thermal Bottle 700 ml + Thermal Tumbler 860 ml", bn="শীতের সকালে গরম চায়ের জন্য ফ্লাস্ক",
                feats=["Bottle: 316 steel, safety lock", "Bottle: easy carry handle", "Tumbler: double wall vacuum", "Tumbler: handle and straw"],
                items=[dict(img=HQ + "17.png", name="Thermal Bottle 700 ml", r=160, mw=190, mh=380, cy=575),
                       dict(img=HQ + "16.png", name="Thermal Tumbler 860 ml", r=160, mw=300, mh=360, cy=575)],
                price=800, plabel="EACH", pcx=540, cap_ang=-3,
                bg=(255, 232, 214), win=(40, 132, 130), circ=(255, 214, 90), acc=(232, 76, 60), c2=(255, 214, 90), c3=(28, 84, 96))),
    ("AM", dict(out="04_awei_t88_earbuds", img=HQ + "11.png", tag="EARBUDS UNDER 1,000", head=["Earbuds under", "1,000 taka"],
                title="Awei T88 Wireless Earbuds with ANC Support, Black", bn="কম দামে ভালো ইয়ারবাড খুঁজছেন?",
                feats=["ANC support", "IPX6 water resistant", "Bluetooth 5.4, touch control", "1 hour fast charging"],
                price=990, regular=1450, spec=("5.4", "BLUETOOTH"), maxw=330, maxh=430,
                bg=(14, 110, 84), rib=(255, 168, 196), acc=(14, 110, 84))),
    ("AM", dict(out="05_good_night_gifts", tag="GOOD NIGHT GIFTS", head=["Good night", "gift ideas"],
                title="22 inch Big Teddy Bear + Silent Alarm Clock", bn="প্রিয়জনকে দিন টেডি বিয়ার আর অ্যালার্ম ঘড়ি",
                feats=["22 inch super soft teddy", "Teddy: lovely gift idea", "Clock: silent, no ticking", "Clock: classic twin bell"],
                items=[dict(img=HQ + "06.png", name="22\" Teddy Bear", price=1150, cx=210, cy=590, r=165, mw=270, mh=280),
                       dict(img=HQ + "07.png", name="Silent Alarm Clock", price=500, cx=580, cy=590, r=165, mw=220, mh=280)],
                price=500, plabel="FROM", sub="2 sweet picks",
                bg=(88, 44, 110), rib=(150, 228, 196), acc=(88, 44, 110))),
]

if __name__ == "__main__":
    keys = sys.argv[1:]
    for kind, p in POSTS:
        if keys and p["out"][:2] not in keys: continue
        if "img" in p and isinstance(p["img"], str): p["img"] = im(p["img"])
        for it in p.get("items", []):
            if isinstance(it["img"], str): it["img"] = im(it["img"])
        T[kind](p)
