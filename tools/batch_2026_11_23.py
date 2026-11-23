"""Everyday Cart daily batch, 23 Nov 2026. NEW style set 18 (render_styles18: AK diagonal split poster, AL fanned card stack).
5 image posts + 1 Reel."""
import os, sys
import render_flat as rf
from render_flat import im, HQ, FL
from render_styles18 import TEMPLATES18 as T
rf.OUTDIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "posts", "batch-2026-11-23")) + "/"
os.makedirs(rf.OUTDIR, exist_ok=True)

POSTS = [
    ("AK", dict(out="01_oraimo_necklace_lite", img=HQ + "04.png", tag="WIRELESS NECKBAND", head=["30 hours of music,", "right around your neck"],
                title="Oraimo Necklace Lite ENC Wireless Neckband", bn="সারাদিন গান আর কলের জন্য হালকা নেকব্যান্ড",
                feats=["Up to 30 hours playtime", "ENC for clear calls", "Dual device connectivity", "Call vibration alert"],
                price=1300, regular=1485, spec=("30H", "PLAYTIME"), maxw=440, maxh=450, ang=-6,
                top=(18, 78, 62), acc=(255, 154, 60), disc=(206, 236, 222), stripe=(255, 154, 60), code="GADGET/30H")),
    ("AL", dict(out="02_kodomo_baby_care_trio", tag="BABY CARE", head=["Bath time to brush time,", "Kodomo has it"],
                title="Kodomo Lotion Powder + Kids Toothpaste + Toothbrush", bn="বাচ্চার যত্নে কোডোমো বেবি লোশন আর টুথপেস্ট",
                feats=["Lotion powder: extra mild", "Lotion powder: dust free, 0+ months", "Toothpaste: sugar free, orange", "Toothbrush: soft, 0.5 to 3 years"],
                items=[dict(img=FL + "kodomo_lotion.png", name="Lotion Powder", price=720, mh=250),
                       dict(img=FL + "kodomo_paste.png", name="Kids Toothpaste", price=280, mw=236, mh=200),
                       dict(img=FL + "kodomo_brush.png", name="Kids Toothbrush", price=200, mh=250)],
                xs=[252, 540, 828], angs=[8, 0, -8], cw=282, ch=470, card_cy=630, bg=(222, 236, 252), acc=(230, 74, 70), c1=(255, 222, 130), c2=(255, 196, 176), card=(255, 255, 255))),
    ("AK", dict(out="03_insulated_lunch_box", img=HQ + "26.png", tag="OFFICE LUNCH", head=["Cold office,", "warm lunch"],
                title="Premium 3 Layer Stainless Steel Insulated Lunch Box", bn="শীতে অফিসে গরম খাবারের জন্য লাঞ্চ বক্স",
                feats=["Hot or cold up to 12 hours", "2.6L large capacity", "Food grade steel inside", "Leak proof, easy carry"],
                price=3000, regular=4500, spec=("2.6L", "3 STEEL LAYERS"), maxw=450, maxh=440,
                top=(112, 28, 52), acc=(255, 208, 104), disc=(252, 228, 214), stripe=(255, 208, 104), code="KITCHEN/2.6L")),
    ("AL", dict(out="05_minitree_mumpot", img=HQ + "20.png", tag="BABY SIPPY CUP", head=["Little hands,", "first sips"],
                title="Minitree Duckbill Mumpot 280 ml, Pink or Sky Blue", bn="ছোট্ট সোনার প্রথম সিপি কাপ মাম্পট",
                feats=["Soft duckbill spout", "Two easy grip handles", "For babies 3+ months", "Pink or Sky Blue"],
                price=400, regular=550, spec=("280 ml", "3+ MONTHS"), maxw=520, maxh=380, dy=0, cw=600, ch=480, card_cy=660,
                bg=(214, 240, 228), acc=(226, 70, 132), c1=(255, 196, 214), c2=(150, 206, 236))),
    ("AK", dict(out="06_forkan_trolley_luggage", img=HQ + "05.png", tag="WINTER TRAVEL", head=["Weekend trip?", "Roll, don't carry"],
                title="FORKAN Premium Hard Shell Trolley Luggage, 20 and 24 inch", bn="শীতের ট্যুরে মজবুত ট্রলি ব্যাগ সাথে নিন",
                feats=["Durable hard shell body", "Smooth 360° spinner wheels", "Spacious, lightweight", "20 and 24 inch sizes"],
                price=4000, regular=5500, plabel="FROM", spec=("360°", "SPINNER WHEELS"), maxw=360, maxh=500, ang=4,
                top=(34, 40, 60), acc=(255, 150, 160), disc=(255, 228, 230), stripe=(255, 150, 160), code="TRAVEL/360")),
]

if __name__ == "__main__":
    keys = sys.argv[1:]
    for kind, p in POSTS:
        if keys and p["out"][:2] not in keys: continue
        p.pop("from_", None)
        if "img" in p and isinstance(p["img"], str): p["img"] = im(p["img"])
        for it in p.get("items", []):
            if isinstance(it["img"], str): it["img"] = im(it["img"])
        T[kind](p)
