"""Everyday Cart daily batch, 28 Nov 2026. NEW style set 23 (render_styles23: AU instant photo poster, AV ticket poster).
5 image posts + 1 Reel."""
import os, sys
import render_flat as rf
from render_flat import im, HQ, FL
from render_styles23 import TEMPLATES23 as T
rf.OUTDIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "posts", "batch-2026-11-28")) + "/"
os.makedirs(rf.OUTDIR, exist_ok=True)

POSTS = [
    ("AV", dict(out="01_oraimo_watch_5_lite", img=HQ + "02.png", tag="SMART WATCH", head=["Take calls", "right from your wrist"],
                title="Oraimo Watch 5 Lite Calling Smart Watch (Official)", bn="ফোন পকেটেই থাকুক কল ধরুন স্মার্ট ওয়াচে",
                feats=['2.01" HD display', "HD voice in calls", "IP68 dust and water", "Up to 7 days battery"],
                stub_top="OFFICIAL ORAIMO", stub_name="Watch 5 Lite", ptag="105+ SPORTS MODES", price=1650, regular=1870,
                bg=(14, 88, 96), ink=(16, 26, 32), acc=(255, 206, 86), panel=(255, 128, 102), ticket=(255, 248, 236),
                h2c=(255, 206, 86), tick=(14, 88, 96), bnc=(14, 88, 96), maxh=430)),
    ("AU", dict(out="02_minitree_baby_trio", tag="BABY FEEDING", head=["First bottles and", "first sips, from Tk 400"],
                title="Minitree Tritan 7 oz, 120 ml Training Bottle and Duckbill Mumpot", bn="ছোট্ট সোনার জন্য মিনিট্রি বেবি ফিডার ও মাম্পট",
                items=[dict(img=HQ + "08.png", name="Tritan Bottle 7 oz", price=450, inner=(255, 214, 226)),
                       dict(img=HQ + "22.png", name="120 ml Training Bottle", price=450, inner=(200, 236, 255), y=-24),
                       dict(img=HQ + "20.png", name="Duckbill Mumpot 280 ml", price=400, inner=(214, 244, 214))],
                feats=["BPA free Tritan, 210 ml", "Easy grip handles", "Soft duckbill spout", "For babies 3+ months"],
                pw=322, ph=430, angs=[-6, 3, -4], xs=[196, 540, 884], pcy=660,
                bg=(190, 172, 255), ink=(36, 28, 70), acc=(214, 56, 128), tape=(255, 236, 140), h2c=(214, 56, 128),
                tick=(214, 56, 128), bnc=(214, 56, 128), spark=(226, 216, 255))),
    ("AV", dict(out="03_massage_gun", img=HQ + "31.png", tag="MASSAGE GUN", head=["Long day at the desk?", "Relax at home"],
                title="Portable Rechargeable Massage Gun with 4 Heads", bn="অফিস শেষে ক্লান্ত শরীরে ম্যাসাজ গানে আরাম",
                feats=["4 massage heads", "Powerful yet quiet motor", "Lightweight, ergonomic", "Rechargeable, portable"],
                stub_top="AFTER OFFICE", stub_name="Massage Gun", ptag="4 HEADS INCLUDED", price=850, regular=1200,
                bg=(52, 30, 72), ink=(22, 14, 32), acc=(196, 236, 84), panel=(140, 214, 255), ticket=(250, 248, 255),
                h2c=(196, 236, 84), tick=(124, 70, 170), bnc=(124, 70, 170), maxh=440, ang=-8)),
    ("AU", dict(out="04_big_teddy_bear", img=HQ + "06.png", tag="GIFT IDEA", head=["A big hug that", "never ends"],
                title='22" Big Teddy Bear, Super Soft Premium Plush', bn="প্রিয়জনের জন্য বড় টেডি বিয়ার উপহার",
                feats=["22 inch big size", "Super soft premium plush", "Perfect for cuddling", "Lovely gift for any day"],
                cap="22 inch of soft hugs", price=1150, regular=2000, pricec=(255, 214, 80), ang=-4, pw=570, ph=630, pcx=500, pcy=655, sx=870, sy=850,
                bg=(255, 112, 140), ink=(48, 22, 34), acc=(214, 44, 90), inner=(255, 236, 200), tape=(130, 220, 255),
                h2c=(255, 240, 160), tick=(214, 44, 90), bnc=(214, 44, 90), spark=(255, 190, 204), maxh=470)),
    ("AV", dict(out="05_silent_alarm_clock", img=HQ + "07.png", tag="ALARM CLOCK", head=["No tick tock,", "just sweet sleep"],
                title="Silent Alarm Clock, Classic Twin Bell Design", bn="টিকটিক শব্দ ছাড়া অ্যালার্ম ঘড়ি রাতে শান্তির ঘুম",
                feats=["Non ticking, silent", "Precise quartz movement", "Classic twin bell design", "Elegant bedside decor"],
                stub_top="GOOD NIGHT PICK", stub_name="Silent Alarm Clock", ptag="NON TICKING", price=500, regular=800,
                bg=(22, 28, 66), ink=(14, 16, 36), acc=(120, 226, 196), panel=(255, 190, 120), ticket=(244, 246, 255),
                pricebox=(22, 28, 66), h2c=(120, 226, 196), tick=(22, 28, 66), bnc=(22, 28, 66), maxh=420)),
]

if __name__ == "__main__":
    keys = sys.argv[1:]
    for kind, p in POSTS:
        if keys and p["out"][:2] not in keys: continue
        if "img" in p and isinstance(p["img"], str): p["img"] = im(p["img"])
        for it in p.get("items", []):
            if isinstance(it["img"], str): it["img"] = im(it["img"])
        T[kind](p)
