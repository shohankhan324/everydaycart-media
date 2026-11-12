"""Everyday Cart daily batch, 12 Nov 2026. NEW style set 7 (render_styles7: O spotlight stage, P seam poster).
5 image posts + 1 Reel."""
import os, sys
import render_flat as rf
from render_flat import im, HQ, FL
from render_styles7 import TEMPLATES7 as T
rf.OUTDIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "posts", "batch-2026-11-12")) + "/"
os.makedirs(rf.OUTDIR, exist_ok=True)

POSTS = [
    ("O", dict(out="01_oraimo_watch_5_lite", img=HQ + "02.png", tag="SMART WATCH", head=["Take calls right", "from your wrist"],
               title="Oraimo Watch 5 Lite Smart Watch (Official)", bn=["স্মার্ট ওয়াচে কথা বলুন", "সরাসরি কব্জি থেকে"],
               feats=['2.01" HD Display', "Bluetooth Calling", "Up to 7 Days Battery"], price=1650, regular=1870,
               bg=(16, 66, 76), acc=(255, 138, 92), maxw=430, maxh=520)),
    ("P", dict(out="02_winter_sip_collection", tag="THERMAL BOTTLES", word="WINTER", head=["Warm sips all winter", "Pick your flask!"],
               items=[(HQ + "15.png", "Big Mac 1000ml Cup", 1000, 1300), (HQ + "16.png", "Thermal Tumbler 860ml", 800, 1200),
                      (HQ + "19.png", "Smart LED Bottle", 350, 700), (HQ + "18.png", "Thermal Bottle 600ml", 800, 1250)],
               scales=[1.0, 0.9, 0.9, 0.95], maxh=460, seam=620, sink=330, bn="শীতে গরম চা কফির সঙ্গী ফ্লাস্ক", bny=1215,
               top=(122, 52, 96), acc=(122, 52, 96))),
    ("P", dict(out="03_wide_neck_baby_feeder", img=FL + "wide_neck_feeder_bottle.png", tag="BABY FEEDER", word="BABY", head=["Gentle feeding for", "happy little tummies"],
               title="Wide Neck Baby Feeder", bn=["নরম নিপলের", "বেবি ফিডার"], feats=["Anti colic nipple", "BPA free PP", "Wide neck"],
               price=450, regular=700, top=(104, 170, 226), acc=(36, 54, 104), maxw=360, maxh=560, cx=540, sink=170, bny=780, px=860, pdy=70, ty=1030)),
    ("O", dict(out="04_massage_gun", img=HQ + "31.png", tag="MASSAGE GUN", head=["Tired after work", "or the gym?"],
               title="Portable Rechargeable Massage Gun", bn=["ম্যাসাজ গান দিয়ে", "ক্লান্তি দূর করুন ঘরেই"],
               feats=["4 Massage Heads", "Quiet Motor", "Rechargeable"], price=850, regular=1200,
               bg=(28, 30, 40), acc=(196, 232, 76), maxw=500, maxh=460)),
    ("P", dict(out="05_silent_alarm_clock", img=HQ + "07.png", tag="ALARM CLOCK", word="QUIET", head=["Silent nights", "On time mornings"],
               title="Silent Alarm Clock", bn=["নিঃশব্দ অ্যালার্ম ঘড়ি", "শান্তির ঘুম প্রতিরাতে"], feats=["No ticking sound", "Quartz movement", "Twin bell design"],
               price=500, regular=800, top=(64, 58, 124), acc=(204, 104, 52), maxw=470, maxh=600, cx=540, sink=170, bny=780, px=860, pdy=70, ty=1030)),
]

if __name__ == "__main__":
    keys = sys.argv[1:]
    for kind, p in POSTS:
        if keys and p["out"][:2] not in keys: continue
        if "items" in p: p["items"] = [(im(a) if isinstance(a, str) else a, b, c, d) for a, b, c, d in p["items"]]
        elif isinstance(p["img"], str): p["img"] = im(p["img"])
        T[kind](p)
