"""Everyday Cart daily batch, 14 Nov 2026. NEW style set 9 (render_styles9: S order slip, T app card).
5 image posts + 1 Reel."""
import os, sys
import render_flat as rf
from render_flat import im, HQ, FL
from render_styles9 import TEMPLATES9 as T
rf.OUTDIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "posts", "batch-2026-11-14")) + "/"
os.makedirs(rf.OUTDIR, exist_ok=True)

POSTS = [
    ("S", dict(out="01_proove_intro_pro", img=HQ + "03.png", tag="EARBUDS", head=["Earbuds with an", "LED display case"],
               title="Proove Intro Pro (APP) Black TWS (Official)",
               feats=["13mm driver, powerful sound", "Transparent ENC for clear calls", "Bluetooth 5.4, touch control",
                      "LED display charging case", "Up to 6 hours playback"],
               price=2300, bg=(14, 84, 72), acc=(255, 214, 92), maxw=470, maxh=520, cx=310, cy=760, r=260,
               slipno="PROOVE  |  OFFICIAL", bn="এলইডি ডিসপ্লে কেসের ইয়ারবাড এখন এভরিডে কার্টে")),
    ("T", dict(out="02_minitree_bottle_mumpot", tag="BABY FEEDING", hook="First sips made easy",
               items=[(HQ + "22.png", "120 ml Bottle", 450, 600, 360, 270), (HQ + "20.png", "Mumpot 280 ml", 400, 550, 380, 255)], dy=14,
               title="Minitree Feeding Bottle and Duckbill Mumpot", bn="ছোট্ট হাতে ধরার মতো বেবি ফিডার আর মাম্পট",
               feats=["Easy grip handles", "Bottle for 6+ months", "Mumpot for 3+ months", "Mumpot in Pink or Sky Blue"],
               price=400, py1=700, **{"from": "From "}, bg=(234, 226, 255), acc=(120, 86, 214), acc2=(236, 92, 140), panel=(244, 238, 255))),
    ("S", dict(out="03_home_helpers", tag="HOME", head=["Small helpers,", "big difference"],
               items=[("Premium Cleaning Gloves", 200), ("Full Automatic Folding Umbrella", 900)],
               ifeats={"Premium Cleaning Gloves": ["Waterproof soft rubber", "Long floral cuffs"],
                       "Full Automatic Folding Umbrella": ["Auto open and close", "For sun and rain"]},
               place=[(HQ + "29.png", -75, 10, 340, 440), (HQ + "23.png", 140, 0, 120, 500)],
               bg=(20, 104, 118), acc=(255, 176, 196), cx=300, cy=770, r=250, slipno="UNDER TK 1,000",
               bn="রোজকার কাজে গ্লাভস আর ছাতা")),
    ("T", dict(out="04_forkan_trolley_luggage", img=HQ + "05.png", tag="TRAVEL", hook="Winter trip coming up?",
               title="FORKAN Premium Hard Shell Trolley Luggage", bn="শীতের ভ্রমণে মজবুত ট্রলি ব্যাগ",
               feats=["Hard shell body", "360° spinner wheels", "Spacious interior", "Lightweight", "20 and 24 inch"],
               price=4000, regular=5500, **{"from": "From "}, maxw=360, maxh=372, py1=700, dx=90, dy=4,
               bg=(208, 232, 250), acc=(226, 88, 112), acc2=(28, 56, 104), panel=(255, 236, 238))),
    ("T", dict(out="05_awei_t108", img=HQ + "10.png", tag="EARBUDS", hook="Under Tk 1,000",
               title="Awei T108 Wireless Earbuds (Official)", bn="কম দামে ভালো সাউন্ডের ইয়ারবাড",
               feats=["13mm drivers", "ENC for clear calls", "20 hours with case", "Bluetooth 5.3", "USB Type C"],
               price=950, regular=1199, maxw=440, maxh=420, dx=40, dy=18,
               bg=(255, 232, 160), acc=(32, 32, 40), acc2=(232, 84, 48), panel=(255, 244, 214))),
]

if __name__ == "__main__":
    keys = sys.argv[1:]
    for kind, p in POSTS:
        if keys and p["out"][:2] not in keys: continue
        if "place" in p: p["place"] = [(im(a), *rest) for a, *rest in p["place"]]
        if "items" in p and kind == "T": p["items"] = [(im(a), *rest) for a, *rest in p["items"]]
        if "img" in p and isinstance(p["img"], str): p["img"] = im(p["img"])
        T[kind](p)
