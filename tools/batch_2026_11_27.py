"""Everyday Cart daily batch, 27 Nov 2026. NEW style set 22 (render_styles22: AS vinyl record poster, AT pillar timeline).
5 image posts + 1 Reel."""
import os, sys
import render_flat as rf
from render_flat import im, HQ, FL
from render_styles22 import TEMPLATES22 as T
rf.OUTDIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "posts", "batch-2026-11-27")) + "/"
os.makedirs(rf.OUTDIR, exist_ok=True)

POSTS = [
    ("AS", dict(out="01_oraimo_spacebuds_neo_plus", img=HQ + "12.png", tag="WIRELESS EARBUDS", head=["Game mode on,", "music never stops"],
                title="Oraimo SpaceBuds Neo+ Wireless Earbuds (Official)", bn="গান আর গেম দুটোর জন্যই ওরাইমো ইয়ারবাড",
                feats=["Low latency game mode", "Sound360 spatial audio", "Up to 30 hours battery", "Bluetooth 5.4, IPX4"],
                price=1940, regular=2189, maxw=450, maxh=460, dy=6,
                bg=(118, 92, 240), ink=(22, 20, 44), acc=(255, 120, 170), label=(255, 214, 80), arm=(255, 255, 255),
                h2c=(255, 214, 80), pricec=(255, 214, 80), tick=(118, 92, 240), bnc=(118, 92, 240))),
    ("AT", dict(out="02_kodomo_baby_care_trio", tag="BABY CARE", head=["Gentle care for", "little ones, from Tk 200"],
                title="Kodomo Lotion Powder, Kids Toothpaste and Toothbrush", bn="বাচ্চার যত্নে কোডোমো লোশন পাউডার ও টুথপেস্ট",
                items=[dict(img=FL + "kodomo_lotion.png", name="Lotion Powder 180 ml", price=720, regular=880, mh=300, pillar=(150, 206, 255)),
                       dict(img=FL + "kodomo_paste.png", name="Kids Toothpaste", price=280, regular=400, mw=290, mh=300, ang=90, pillar=(255, 176, 196)),
                       dict(img=FL + "kodomo_brush.png", name="Kids Toothbrush", price=200, regular=400, mh=320, pillar=(170, 226, 190))],
                chips=["Extra mild", "0.5+ years", "Soft bristles"],
                bg=(255, 248, 236), ink=(30, 40, 90), acc=(255, 210, 80), h2c=(230, 70, 120), strip=(30, 40, 90), bnc=(255, 210, 80))),
    ("AS", dict(out="03_winter_tumbler_duo", tag="WINTER TUMBLERS", head=["Your winter sip,", "two ways"],
                title="Have a Good Time 750 ml + Premium Thermal Tumbler 860 ml", bn="শীতে গরম চা কফির জন্য টাম্বলার বেছে নিন",
                feats=["Insulated steel, 750 ml", "Double wall vacuum, 860 ml", "Secure lids, carry handles", "Reusable straw (860 ml)"],
                items=[dict(img=FL + "hgt_tumbler.png", name="Have a Good Time 750 ml", price=1000, mw=420, mh=380, label=(255, 140, 90)),
                       dict(img=HQ + "16.png", name="Premium Tumbler 860 ml", price=800, mw=400, mh=400, label=(140, 200, 255))],
                r=228, rcy=590, xs=[290, 790],
                bg=(232, 92, 60), ink=(36, 26, 30), acc=(232, 92, 60), h2c=(255, 228, 150), tick=(232, 92, 60), bnc=(200, 70, 40))),
    ("AS", dict(out="04_insulated_lunch_box", img=HQ + "26.png", tag="LUNCH BOX", head=["Hot lunch at the", "office desk"],
                title="Premium 3 Layer Stainless Steel Insulated Lunch Box", bn="শীতে অফিসে গরম খাবারের জন্য লাঞ্চ বক্স",
                feats=["Hot or cold up to 12 hours", "2.6L large capacity", "Food grade stainless steel", "Leak proof, carry handle"],
                price=3000, regular=4500, maxw=470, maxh=470, dy=-4,
                bg=(46, 140, 110), ink=(20, 34, 30), acc=(255, 196, 64), label=(255, 196, 64), arm=(255, 244, 226),
                h2c=(255, 214, 110), pricec=(255, 244, 226), tick=(46, 140, 110), bnc=(46, 140, 110))),
    ("AT", dict(out="05_forkan_trolley_luggage", img=HQ + "05.png", tag="TROLLEY LUGGAGE", headline="Pack light for the winter trip",
                title="FORKAN Premium Hard Shell Trolley Luggage", bn="শীতের ট্যুরে মজবুত ট্রলি ব্যাগ সাথে নিন",
                feats=["Durable hard shell body", "Smooth 360° spinner wheels", "Spacious, lightweight", "20 and 24 inch sizes"],
                chips=["20 inch", "24 inch", "Inbox for colours"], price=4000, regular=5500, maxh=640, pre="From",
                bg=(28, 46, 92), ink=(14, 20, 40), pillar=(255, 200, 190), num=(255, 200, 190), acc=(255, 206, 90), h2c=(255, 206, 90),
                strip=(14, 20, 40), bnc=(255, 200, 190))),
]

if __name__ == "__main__":
    keys = sys.argv[1:]
    for kind, p in POSTS:
        if keys and p["out"][:2] not in keys: continue
        if "img" in p and isinstance(p["img"], str): p["img"] = im(p["img"])
        for it in p.get("items", []):
            if isinstance(it["img"], str): it["img"] = im(it["img"])
        T[kind](p)
