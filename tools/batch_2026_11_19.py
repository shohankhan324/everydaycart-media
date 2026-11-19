"""Everyday Cart daily batch, 19 Nov 2026. NEW style set 14 (render_styles14: AC sunburst retro poster, AD comic panel).
5 image posts + 1 Reel."""
import os, sys
import render_flat as rf
from render_flat import im, HQ, FL
from render_styles14 import TEMPLATES14 as T
rf.OUTDIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "posts", "batch-2026-11-19")) + "/"
os.makedirs(rf.OUTDIR, exist_ok=True)

POSTS = [
    ("AC", dict(out="01_proove_intro_pro", img=HQ + "03.png", tag="WIRELESS EARBUDS", head=["Battery check?", "Just look at the case"],
                title="Proove Intro Pro (APP) Black TWS (Official)", bn="এলইডি ডিসপ্লে চার্জিং কেসসহ ইয়ারবাড",
                feats=["13mm driver", "Transparent ENC for calls", "Bluetooth 5.4, touch control", "LED display charging case"],
                price=2300, sticker="UP TO 6 HOURS PLAYBACK", maxw=400, maxh=420, dy=6,
                bg=(150, 208, 238), band=(24, 40, 92), acc=(238, 84, 66), hl=(255, 214, 90))),
    ("AD", dict(out="02_minitree_kodomo_baby_picks", tag="BABY CARE PICKS", head=["Sip time and", "brush time sorted"],
                title="Minitree Duckbill Mumpot + Kodomo Toothpaste + Toothbrush", bn="বাচ্চার মাম্পট টুথপেস্ট আর টুথব্রাশ এক জায়গায়",
                feats=["Mumpot 280 ml: soft duckbill spout", "Mumpot: Pink or Sky Blue, 3+ months", "Toothpaste: sugar free, orange flavour",
                       "Toothbrush: soft bristles, 0.5 to 3 years"],
                items=[dict(img=HQ + "20.png", cx=230, cy=520, mw=340, mh=200, name="Duckbill Mumpot", price=400, regular=550),
                       dict(img=FL + "kodomo_paste.png", cx=560, cy=540, mw=290, mh=100, name="Kodomo Toothpaste", price=280, regular=400),
                       dict(img=FL + "kodomo_brush.png", cx=868, cy=500, mw=250, mh=260, name="Kodomo Toothbrush", price=200, regular=400)],
                price=200, label="FROM", bx=300, bw=380,
                paper=(253, 244, 238), panel=(248, 176, 196), acc=(214, 44, 100), yel=(255, 218, 92))),
    ("AC", dict(out="03_insulated_lunch_box", img=HQ + "26.png", tag="OFFICE LUNCH", head=["Hot rice at 1 pm,", "packed at 8 am"],
                title="Premium 3 Layer Stainless Steel Insulated Lunch Box", bn="অফিসে গরম খাবার নিতে লাঞ্চ বক্স",
                feats=["Hot or cold up to 12 hours", "2.6L large capacity", "Food grade steel interior", "Leak proof, easy carry handle"],
                price=3000, regular=4500, sticker="3 LAYERS  |  2.6L", maxw=430, maxh=440, dy=4,
                bg=(46, 150, 138), ray=(70, 170, 156), band=(18, 66, 66), acc=(244, 128, 36), hl=(255, 222, 120), disc=(214, 240, 232))),
    ("AD", dict(out="04_oraimo_necklace_lite", img=HQ + "04.png", tag="WIRELESS NECKBAND", head=["Calls clear,", "music all day"],
                title="Oraimo Necklace Lite ENC Wireless Neckband (Official)", bn="সারাদিন গান শোনার আরামদায়ক নেকব্যান্ড",
                feats=["Up to 30 hours playtime", "ENC noise cancellation in calls", "Dual device connectivity", "Call vibration alert"],
                price=1300, regular=1485, sticker="UP TO 30 HOURS PLAYTIME", maxw=420, maxh=520, cx=700, cy=500, bw=360,
                paper=(246, 248, 236), panel=(176, 226, 150), acc=(112, 58, 200), yel=(255, 214, 72))),
    ("AC", dict(out="05_forkan_trolley_luggage", img=HQ + "05.png", tag="WINTER TRAVEL", head=["Sajek, Sylhet or", "Cox's Bazar next?"],
                title="FORKAN Premium Hard Shell Trolley Luggage", bn="শীতের ভ্রমণে মজবুত ট্রলি ব্যাগ",
                feats=["Durable hard shell body", "Smooth 360° spinner wheels", "Spacious interior", "20 inch and 24 inch sizes"],
                price=4000, regular=5500, label="FROM", sticker="LIGHTWEIGHT DESIGN", maxw=330, maxh=450, dy=4,
                bg=(204, 194, 242), ray=(222, 214, 250), band=(64, 38, 98), acc=(20, 150, 140), hl=(255, 200, 220))),
]

if __name__ == "__main__":
    keys = sys.argv[1:]
    for kind, p in POSTS:
        if keys and p["out"][:2] not in keys: continue
        if "img" in p and isinstance(p["img"], str): p["img"] = im(p["img"])
        for it in p.get("items", []):
            if isinstance(it["img"], str): it["img"] = im(it["img"])
        T[kind](p)
