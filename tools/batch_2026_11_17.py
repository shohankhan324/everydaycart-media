"""Everyday Cart daily batch, 17 Nov 2026. NEW style set 12 (render_styles12: Y pinboard, Z wave poster).
5 image posts + 1 Reel."""
import os, sys
import render_flat as rf
from render_flat import im, HQ, FL
from render_styles12 import TEMPLATES12 as T
rf.OUTDIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "posts", "batch-2026-11-17")) + "/"
os.makedirs(rf.OUTDIR, exist_ok=True)

POSTS = [
    ("Z", dict(out="01_oraimo_spacebuds_lite", img=HQ + "13.png", tag="WIRELESS EARBUDS", head=["40 hours of music", "in your pocket"],
               title="Oraimo SpaceBuds Lite (Official)", bn="কেসসহ ৪০ ঘণ্টা পর্যন্ত গান শোনার ইয়ারবাড",
               feats=["Sound360 spatial audio", "AI call noise cancellation", "Bluetooth 5.4", "IPX4 water resistant"],
               price=1310, regular=1496, sticker="UP TO 40H PLAYTIME", maxw=460, maxh=400, pcx=400, pcy=545,
               top=(30, 46, 92), acc=(130, 236, 190), bncol=(30, 46, 92))),
    ("Y", dict(out="02_wide_neck_feeder", img=FL + "wide_neck_feeder_bottle.png", tag="BABY FEEDING", head=["Easy to fill,", "easy to clean"],
               title="Wide Neck Baby Feeder, BPA Free", bn="নরম নিপলের বেবি ফিডার",
               feats=["Soft anti colic nipple", "Food grade PP", "Wide neck opening", "Easy to clean"],
               price=450, regular=700, sticker="BPA FREE", maxw=330, maxh=420,
               bg=(250, 222, 228), acc=(214, 70, 120), acc2=(124, 196, 226), photo=(255, 244, 247),
               notes=[(255, 236, 140), (255, 255, 255), (196, 232, 250), (255, 200, 214)])),
    ("Z", dict(out="03_smart_led_bottle", img=HQ + "19.png", tag="WINTER PICK", head=["Tap the lid,", "see the temperature"],
               title="Smart LED Temperature Bottle, 500 ml", bn="তাপমাত্রা দেখায় এমন স্মার্ট ফ্লাস্ক",
               feats=["LED temperature display", "Double wall insulation", "500 ml stainless steel", "Black and White"],
               price=350, regular=700, sticker="BLACK  |  WHITE", maxw=420, maxh=520, pcx=400, pcy=570, r=270,
               top=(214, 84, 50), acc=(255, 214, 120), bncol=(190, 70, 40))),
    ("Y", dict(out="04_gadget_gift_duo", tag="GADGET GIFTS", head=["Gift a gadget", "they will use daily"],
               title="COLMI P81 Smartwatch + Oraimo SpaceBox Speaker", bn="প্রিয়জনের জন্য স্মার্ট ওয়াচ আর স্পিকার",
               feats=["Watch: Bluetooth calling", "Watch: IP68, 100+ sports", "Speaker: light show", "Speaker: 8W, thumping bass"],
               items=[dict(img=HQ + "09.png", cx=290, w=440, ang=-4, mw=270, mh=330, name="COLMI P81 Watch", price=1350, regular=1540,
                           tape=(255, 196, 64)),
                      dict(img=HQ + "01.png", cx=785, w=440, ang=3, mw=360, mh=250, name="Oraimo SpaceBox", price=1841, regular=2299,
                           tape=(120, 200, 190), oy=16)],
               py1=880, bg=(206, 222, 236), acc=(38, 70, 140), photo=(240, 244, 250),
               notes=[(255, 226, 110), (255, 226, 110), (170, 226, 200), (170, 226, 200)])),
    ("Z", dict(out="05_kodomo_lotion_powder", img=FL + "kodomo_lotion.png", tag="BABY SKIN CARE", head=["Goes on as lotion,", "dries to soft powder"],
               title="Kodomo Baby Lotion Powder, Extra Mild 180 ml", bn="শিশুর নরম ত্বকের যত্নে লোশন পাউডার",
               feats=["Extra mild formula", "Dust free", "Absorbs moisture", "Suitable from 0+ months"],
               price=720, regular=880, sticker="FROM 0+ MONTHS", maxw=330, maxh=500, pcx=400, pcy=570, r=260,
               top=(92, 150, 220), acc=(255, 226, 120), bncol=(52, 104, 180))),
]

if __name__ == "__main__":
    keys = sys.argv[1:]
    for kind, p in POSTS:
        if keys and p["out"][:2] not in keys: continue
        if "img" in p and isinstance(p["img"], str): p["img"] = im(p["img"])
        for it in p.get("items", []):
            if isinstance(it["img"], str): it["img"] = im(it["img"])
        T[kind](p)
