"""Everyday Cart daily batch, 22 Nov 2026. NEW style set 17 (render_styles17: AI Swiss grid poster, AJ torn paper poster).
5 image posts + 1 Reel."""
import os, sys
import render_flat as rf
from render_flat import im, HQ, FL
from render_styles17 import TEMPLATES17 as T
rf.OUTDIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "posts", "batch-2026-11-22")) + "/"
os.makedirs(rf.OUTDIR, exist_ok=True)

POSTS = [
    ("AJ", dict(out="01_oraimo_spacebuds_neo_plus", img=HQ + "12.png", tag="WIRELESS EARBUDS", head=["Games, music, calls?", "One pair for all"],
                title="Oraimo SpaceBuds Neo+ (Official), Off-White", bn="গান আর গেম দুটোর জন্যই ওরাইমো ইয়ারবাড",
                feats=["Sound360 spatial audio", "Low latency game mode", "2 noise reducing mics", "Bluetooth 5.4, IPX4"],
                price=1940, regular=2189, spec=("30H", "BATTERY LIFE"), sx=190, sy=560, maxw=520, maxh=560, cx=545, cy=640, avoid=[(870, 520), (190, 560)],
                px=870, py=520, top=(34, 40, 112), acc=(198, 240, 84), acc2=(255, 104, 112), tape=(255, 228, 120))),
    ("AI", dict(out="02_baby_feeders_450", tag="BABY FEEDING", head=["Three baby feeders,", "Tk 450 each"],
                title="Minitree Tritan 7 oz, Minitree 120 ml and Wide Neck Feeder", bn="ছোট্ট সোনার জন্য পছন্দের বেবি ফিডার বেছে নিন",
                feats=["BPA free bottles", "Easy grip handles (Minitree)", "Anti colic nipple (wide neck)", "For 3+ and 6+ months"],
                items=[dict(img=HQ + "08.png", name="Minitree Tritan 7 oz", sub="210 ml, 3+ months", price=450, regular=650, mw=290, fill=(240, 120, 160)),
                       dict(img=HQ + "22.png", name="Minitree 120 ml", sub="Training bottle, 6+ months", price=450, regular=600, mw=290, fill=(120, 176, 236)),
                       dict(img=HQ + "30.png", name="Wide Neck Feeder", sub="Soft anti colic nipple", price=450, regular=700, mw=280, fill=(132, 206, 170))],
                acc=(226, 72, 120), code="BABY/450")),
    ("AJ", dict(out="03_winter_tumblers", tag="WINTER TUMBLERS", head=["Big winter sips,", "Tk 1,000 each"],
                title="Big Mac Thermos Cup + Have a Good Time Tumbler", bn="শীতে গরম চা কফির জন্য বড় টাম্বলার",
                feats=["Big Mac: 1000 ml, handle", "Big Mac: 316 steel, straw", "Good Time: 750 ml", "Good Time: secure travel lid"],
                items=[dict(img=HQ + "15.png", cx=290, cy=705, mw=310, mh=470, ang=-3, name="Big Mac 1000 ml", price=1000, regular=1300, px=230, py=385, pang=-5),
                       dict(img=FL + "hgt_tumbler.png", cx=740, cy=720, mw=470, mh=410, ang=2, name="Have a Good Time 750 ml", price=1000, regular=1200, px=830, py=400, pang=5)],
                avoid=[(230, 395), (830, 395)], top=(186, 78, 56), acc=(255, 214, 120), acc2=(80, 140, 220), tape=(255, 240, 200))),
    ("AI", dict(out="04_elephant_plush", img=HQ + "25.png", tag="SOFT TOY", head=["The softest hug", "for little ones"],
                title="Elephant Plush Soft Toy (18 inch)", bn="নরম তুলতুলে হাতির সফট টয় উপহার দিন",
                feats=["18 inch size", "Super soft plush", "Easy to hug", "A sweet gift for kids"],
                specs=[("18 in", "plush size"), ("SOFT", "super huggable"), ("GIFT", "for kids and loved ones")],
                price=750, regular=1100, maxw=520, maxh=560, block=(178, 160, 236), acc=(232, 88, 128), code="GIFT/18")),
    ("AJ", dict(out="05_awei_ka5_speaker", img=HQ + "14.png", tag="BLUETOOTH SPEAKER", head=["Picnic playlist ready?", "Bring 20W sound"],
                title="Awei KA5 20W Portable Bluetooth Speaker", bn="পিকনিক আর আড্ডায় গান বাজুক এই ব্লুটুথ স্পিকারে",
                feats=["2400mAh battery", "7.5 to 8 hours (70% vol)", "IPX5 waterproof", "Bluetooth 5.3"],
                price=2525, regular=2849, spec=("20W", "10W X 2 OUTPUT"), sx=200, sy=560, maxw=360, maxh=620, cx=560, cy=620, ang=-8, avoid=[(880, 560), (200, 560)],
                px=880, py=560, top=(0, 122, 116), acc=(255, 214, 60), acc2=(255, 120, 80), tape=(255, 232, 140))),
]

if __name__ == "__main__":
    keys = sys.argv[1:]
    for kind, p in POSTS:
        if keys and p["out"][:2] not in keys: continue
        if "img" in p and isinstance(p["img"], str): p["img"] = im(p["img"])
        for it in p.get("items", []):
            if isinstance(it["img"], str): it["img"] = im(it["img"])
        T[kind](p)
