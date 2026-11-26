"""Everyday Cart daily batch, 26 Nov 2026. NEW style set 21 (render_styles21: AQ checkerboard blob poster, AR crossing tape banners).
5 image posts + 1 Reel."""
import os, sys
import render_flat as rf
from render_flat import im, HQ, FL
from render_styles21 import TEMPLATES21 as T
rf.OUTDIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "posts", "batch-2026-11-26")) + "/"
os.makedirs(rf.OUTDIR, exist_ok=True)

POSTS = [
    ("AQ", dict(out="01_oraimo_spacebuds_lite", img=HQ + "13.png", tag="WIRELESS EARBUDS", head=["40 hours of music", "in one small case"],
                title="Oraimo SpaceBuds Lite Wireless Earbuds (Official)", bn="কেসসহ ৪০ ঘণ্টা গান শুনুন এই ইয়ারবাডে",
                feats=["Sound360 spatial audio", "AI call noise cancellation", "Bluetooth 5.4", "IPX4 water resistant"],
                price=1310, regular=1496, spec=("40h", "WITH CASE"), maxw=430, maxh=420, r=290,
                c1=(150, 196, 255), c2=(196, 222, 255), acc=(255, 92, 120), panel=(28, 40, 110), h2c=(255, 196, 70), specc=(255, 214, 90))),
    ("AR", dict(out="02_wide_neck_baby_feeder", img=HQ + "30.png", tag="BABY FEEDER", head=["Easy to fill,", "easy to clean"],
                title="Wide Neck Baby Feeder, BPA Free", bn="নরম নিপলের বেবি ফিডার",
                feats=["Soft anti colic nipple", "BPA free, food grade PP", "Wide neck, easy filling", "Easy cleaning"],
                tape1="BPA FREE", tape2="ANTI COLIC NIPPLE", price=450, regular=700, maxw=440, maxh=520, pcx=400, base=880, ly=250, lx1=1036, tcy=640, disc=(255, 250, 240),
                bg=(255, 196, 206), t1=(255, 255, 255), t2=(120, 200, 180), acc=(36, 60, 120), h2c=(200, 50, 100), tick=(220, 70, 120),
                floor=(240, 168, 182), bnc=(200, 50, 100))),
    ("AQ", dict(out="03_winter_flasks_duo", tag="WINTER FLASKS", head=["Hot sips all day,", "pick your size"],
                title="Premium Thermal Water Bottle + Big Mac 316 Thermos Cup", bn="শীতে গরম চা কফির জন্য ফ্লাস্ক বেছে নিন",
                feats=["Bottle: 600 ml, built in straw", "Bottle: leak proof flip lid", "Cup: huge 1000 ml", "Cup: 316 steel, handle, straw"],
                items=[dict(img=HQ + "18.png", name="Thermal Bottle 600 ml", price=800, r=205, mw=240, mh=370, cy=605),
                       dict(img=HQ + "15.png", name="Big Mac Cup 1000 ml", price=1000, r=205, mw=290, mh=370, cy=605, blob=(232, 240, 255))],
                price=800, c1=(214, 112, 70), c2=(232, 146, 104), acc=(30, 90, 170), panel=(250, 238, 220), h2c=(255, 206, 120), bnc=(180, 70, 40))),
    ("AR", dict(out="04_portable_bbq_grill", img=HQ + "27.png", tag="BBQ GRILL", head=["Rooftop BBQ night,", "grill at home"],
                title="Portable BBQ Grill Machine", bn="শীতের রাতে ছাদে বারবিকিউ পার্টি",
                feats=["Durable steel body", "Adjustable charcoal tray", "Manual air blower", "Picnic, camping, rooftop"],
                tape1="ROOFTOP BBQ", tape2="WINTER NIGHT PARTY", price=5500, regular=9500, maxw=580, maxh=460, pcx=420, base=930, ly=330, tcy=640,
                bg=(34, 30, 60), t1=(255, 140, 40), t2=(255, 214, 80), acc=(255, 214, 80), h2c=(255, 150, 60), tick=(240, 110, 40), bnc=(200, 80, 30))),
    ("AQ", dict(out="05_awei_ka5_speaker", img=HQ + "14.png", tag="BLUETOOTH SPEAKER", head=["20W sound for", "every adda night"],
                title="Awei KA5 20W Portable Bluetooth Speaker", bn="আড্ডায় গান বাজুক এই ব্লুটুথ স্পিকারে",
                feats=["10W x 2 output power", "2400mAh battery", "IPX5 waterproof", "Bluetooth 5.3"],
                price=2525, regular=2849, spec=("20W", "OUTPUT"), maxw=470, maxh=400, r=290, seed=1,
                c1=(150, 220, 120), c2=(196, 238, 170), acc=(120, 60, 200), panel=(20, 70, 60), h2c=(170, 240, 120), specc=(255, 214, 90))),
]

if __name__ == "__main__":
    keys = sys.argv[1:]
    for kind, p in POSTS:
        if keys and p["out"][:2] not in keys: continue
        if "img" in p and isinstance(p["img"], str): p["img"] = im(p["img"])
        for it in p.get("items", []):
            if isinstance(it["img"], str): it["img"] = im(it["img"])
        T[kind](p)
