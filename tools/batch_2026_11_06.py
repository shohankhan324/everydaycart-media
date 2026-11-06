"""Everyday Cart daily batch, 6 Nov 2026. Style set 1 (A split panel, B colour card, C collection grid)."""
import os, sys
import render_flat as rf
from render_flat import im, HQ, template_a, template_b, template_c
rf.OUTDIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "posts", "batch-2026-11-06")) + "/"
os.makedirs(rf.OUTDIR, exist_ok=True)
TEMPLATES = {"A": template_a, "B": template_b, "C": template_c}

POSTS = [
    ("A", dict(out="01_oraimo_watch_5_lite", img=HQ + "02.png", tag="SMART WATCH", title="Oraimo Watch 5 Lite",
               sub="Official  •  HD Voice Calls", feats=["2.01\" HD Display", "AI Watch Faces", "105+ Sports Modes", "7 Days Battery"],
               price=1650, regular=1870, accent=(226, 234, 244))),
    ("C", dict(out="02_baby_feeding_picks", tag="BABY", title="Baby Feeding Picks", sub="Easy grip bottles & cups for little hands",
               items=[dict(img=HQ + "22.png", name="Minitree 120 ml Bottle", price=450, regular=600, accent=(232, 242, 250)),
                      dict(img=HQ + "20.png", name="Minitree Duckbill Mumpot", price=400, regular=550, accent=(253, 236, 240)),
                      dict(img=HQ + "08.png", name="Minitree Tritan Bottle", price=450, regular=650, accent=(238, 246, 234)),
                      dict(img=HQ + "30.png", name="Wide Neck Baby Feeder", price=450, regular=700, accent=(250, 240, 228))],
               foot="Limited stock  •  Inbox us to order")),
    ("A", dict(out="03_portable_massage_gun", img=HQ + "31.png", tag="WELLNESS", title="Portable Massage Gun",
               sub="Rechargeable  •  Portable", feats=["4 Massage Heads", "Powerful, Quiet Motor", "Lightweight", "Ergonomic Design"],
               price=850, regular=1200, accent=(240, 230, 220))),
    ("B", dict(out="04_forkan_trolley_luggage", img=HQ + "05.png", tag="TRAVEL", title="FORKAN Trolley Luggage",
               sub="Hard shell  •  20 inch & 24 inch", feats=["Durable Hard Shell", "360° Spinner Wheels", "Spacious Inside", "Lightweight"],
               price=4000, regular=5500, label="FROM", bg=(232, 236, 244), circle=(246, 248, 252), chip=(234, 238, 246), maxw=560, maxh=600, badge=(900, 400))),
    ("A", dict(out="05_colmi_p81", img=HQ + "09.png", tag="SMART WATCH", title="COLMI P81 Calling Smartwatch",
               sub="Bluetooth calling  •  Model P81", feats=["1.9\" HD Display", "100+ Sports Modes", "300mAh Battery", "IP68 Waterproof"],
               price=1350, regular=1540, accent=(236, 232, 226))),
    ("C", dict(out="06_gadget_picks", tag="GADGETS", title="Sound On: Gadget Picks", sub="Official Oraimo, Proove & Awei",
               items=[dict(img=HQ + "01.png", name="Oraimo SpaceBox Speaker", price=1841, regular=2299, accent=(226, 240, 250)),
                      dict(img=HQ + "12.png", name="Oraimo SpaceBuds Neo+", price=1940, regular=2189, accent=(244, 238, 230)),
                      dict(img=HQ + "03.png", name="Proove Intro Pro", price=2300, regular=2300, accent=(250, 232, 232)),
                      dict(img=HQ + "10.png", name="Awei T108 Earbuds", price=950, regular=1199, accent=(234, 242, 232))],
               accent=(236, 242, 233))),
    ("B", dict(out="07_awei_ka5_speaker", img=HQ + "14.png", tag="SPEAKER", title="Awei KA5 20W Speaker",
               sub="10W x 2 Output  •  Bluetooth 5.3", feats=["IPX5 Waterproof", "2400mAh Battery", "7.5 to 8 Hrs Play", "Portable"],
               price=2525, regular=2849, bg=(246, 236, 222), circle=(252, 247, 240), chip=(248, 238, 226), maxw=640, maxh=560)),
    ("B", dict(out="08_big_teddy_bear", img=HQ + "06.png", tag="GIFT", title="22\" Big Teddy Bear",
               sub="Super soft premium plush", feats=["22 Inch Size", "Super Soft", "Made for Cuddles", "Lovely Gift"],
               price=1150, regular=2000, bg=(250, 232, 236), circle=(255, 245, 247), chip=(252, 236, 240), maxw=560, maxh=580)),
]

if __name__ == "__main__":
    keys = sys.argv[1:]
    for kind, p in POSTS:
        if keys and p["out"][:2] not in keys: continue
        if "img" in p: p["img"] = im(p["img"])
        for it in p.get("items", []): it["img"] = im(it["img"])
        TEMPLATES[kind](p)
