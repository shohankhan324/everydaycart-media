"""Everyday Cart daily batch, 18 Nov 2026. NEW style set 13 (render_styles13: AA airmail stamp, AB callout diagram).
5 image posts + 1 Reel."""
import os, sys
import render_flat as rf
from render_flat import im, HQ, FL
from render_styles13 import TEMPLATES13 as T
rf.OUTDIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "posts", "batch-2026-11-18")) + "/"
os.makedirs(rf.OUTDIR, exist_ok=True)

POSTS = [
    ("AB", dict(out="01_oraimo_spacebuds_neo_plus", img=HQ + "12.png", tag="WIRELESS EARBUDS", head=["Built for music,", "ready for gaming"],
                title="Oraimo SpaceBuds Neo+ (Official), Off-White", bn="গান আর গেমের জন্য অফিসিয়াল ইয়ারবাড",
                feats=["Sound360 spatial audio", "Low latency game mode", "2 noise reducing mics", "Up to 30 hours battery"],
                tg=[(470, 500), (650, 470), (462, 600), (676, 776)],
                price=1940, regular=2189, sticker="BLUETOOTH 5.4  |  IPX4", maxw=400, maxh=430,
                bg=(232, 228, 248), acc=(104, 74, 206), dark=(40, 30, 84), ink=(36, 30, 64))),
    ("AA", dict(out="02_minitree_bottles", tag="BABY FEEDING", head=["Bottles little hands", "can hold on their own"],
                title="Minitree Baby Bottles with Easy Grip Handles", bn="ছোট্ট হাতের জন্য হ্যান্ডেলওয়ালা বেবি ফিডার",
                feats=["Tritan 210 ml: BPA free", "Tritan: for 3+ months", "120 ml: for 6+ months", "Easy grip handles on both"],
                items=[dict(img=HQ + "08.png", cx=290, w=440, ang=-3, mw=360, mh=330, name="Minitree Tritan 7oz", price=450, regular=650,
                            photo=(255, 226, 234)),
                       dict(img=HQ + "22.png", cx=790, w=440, ang=3, mw=360, mh=330, name="Minitree 120 ml Bottle", price=450, regular=600,
                            photo=(214, 236, 250), vcol=(40, 110, 190), oy=12)],
                bg=(252, 230, 236), acc=(214, 64, 112), acc2=(48, 120, 200), ink=(64, 30, 54))),
    ("AB", dict(out="03_have_good_time_tumbler", img=FL + "hgt_tumbler.png", tag="WINTER PICK", head=["Morning tea that", "stays with you"],
                title="Have a Good Time Insulated Steel Tumbler, 750 ml", bn="শীতের সকালে গরম চায়ের টাম্বলার",
                feats=["Secure travel lid", "Easy carry handle", "750 ml capacity", "Insulated stainless steel"],
                tg=[(388, 492), (724, 560), (384, 720), (640, 730)],
                price=1000, regular=1200, sticker="FOR WORK  |  CAMPUS  |  TRAVEL", maxw=440, maxh=440, dy=10,
                bg=(253, 234, 218), acc=(222, 92, 56), dark=(70, 36, 26), ink=(60, 34, 26))),
    ("AA", dict(out="04_elephant_plush", img=HQ + "25.png", tag="SOFT TOYS", head=["Send a hug", "they can keep"],
                title="Elephant Plush Soft Toy, 18 inch", bn="নরম তুলতুলে হাতির সফট টয়",
                feats=["18 inch size", "Super soft and huggable", "Sweet gift for kids", "Gift for loved ones"],
                price=750, regular=1100, sticker="18 INCH  |  SUPER SOFT", maxw=380, maxh=410,
                bg=(222, 240, 232), acc=(226, 72, 80), acc2=(36, 86, 160), photo=(255, 232, 214), ink=(28, 52, 64))),
    ("AB", dict(out="05_portable_bbq_grill", img=HQ + "27.png", tag="WINTER BBQ", head=["Rooftop BBQ night?", "Bring the grill"],
                title="Portable BBQ Grill Machine", bn="শীতের রাতে ছাদে বারবিকিউ পার্টির গ্রিল",
                feats=["Manual air blower", "Adjustable charcoal tray", "Durable steel body", "For picnics and camping"],
                tg=[(372, 545), (676, 490), (484, 700), (676, 776)],
                price=5500, regular=9500, sticker="WINTER NIGHTS", maxw=470, maxh=430, dy=6,
                bg=(250, 238, 200), acc=(214, 82, 34), dark=(34, 34, 38), ink=(40, 34, 28), disc=(255, 250, 236))),
]

if __name__ == "__main__":
    keys = sys.argv[1:]
    for kind, p in POSTS:
        if keys and p["out"][:2] not in keys: continue
        if "img" in p and isinstance(p["img"], str): p["img"] = im(p["img"])
        for it in p.get("items", []):
            if isinstance(it["img"], str): it["img"] = im(it["img"])
        T[kind](p)
