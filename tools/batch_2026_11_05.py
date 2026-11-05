"""Everyday Cart daily batch, 5 Nov 2026. Style set 2 (D arch poster, E header ribbon, F list menu)."""
import os, sys
import render_flat as rf
from render_flat import im, HQ, FL
from render_styles import TEMPLATES
rf.OUTDIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "posts", "batch-2026-11-05")) + "/"
os.makedirs(rf.OUTDIR, exist_ok=True)
ROSE = (165, 112, 111)

POSTS = [
    ("D", dict(out="01_oraimo_spacebuds_lite", img=HQ + "13.png", tag="EARBUDS", title="Oraimo SpaceBuds Lite",
               feats=["Sound360 Audio", "40 Hrs with Case", "IPX4"], price=1310, regular=1496,
               bg=(230, 228, 240), rule=(206, 204, 220), maxw=520, maxh=520)),
    ("E", dict(out="02_premium_thermal_water_bottle", img=HQ + "18.png", tag="THERMAL", title="Premium Thermal Water Bottle",
               sub="Stainless Steel  •  Hot & Cold", feats=["Hot or Cold for Hours", "Stainless Steel", "Leak Resistant Lid", "Travel Friendly"],
               price=800, regular=1250, accent=(236, 240, 244), maxw=330, maxh=500)),
    ("F", dict(out="03_kodomo_baby_care", tag="BABY CARE", title="Kodomo Baby Care Picks", sub="Gentle, Japan quality care for little ones",
               items=[dict(img=FL + "kodomo_paste.png", name="Kodomo Baby Toothpaste", note="Fluoride 1000 ppm  •  6m+", price=280, regular=400, accent=(255, 238, 226)),
                      dict(img=FL + "kodomo_brush.png", name="Kodomo Toothbrush", note="Extra soft  •  6m to 3y", price=200, regular=400, accent=(232, 242, 250)),
                      dict(img=FL + "kodomo_lotion.png", name="Kodomo Lotion Powder", note="Extra mild  •  0m+", price=720, regular=880, accent=(236, 246, 236)),
                      dict(img=HQ + "21.png", name="10 Pc Baby Care Kit", note="Nail, hair & health care", price=480, regular=650, accent=(246, 236, 242))])),
    ("D", dict(out="04_awei_t88_earbuds", img=HQ + "11.png", tag="EARBUDS", title="Awei T88 Wireless Earbuds",
               feats=["ANC Support", "IPX6", "Touch Control"], price=990, regular=1450,
               bg=(226, 234, 222), rule=(196, 210, 194), maxw=480, maxh=520)),
    ("E", dict(out="05_smart_led_bottle", img=HQ + "19.png", tag="THERMAL", title="Smart LED Temperature Bottle",
               sub="500 ml  •  Black & White", feats=["LED Temp Display", "Hot or Cold for Hours", "Stainless Steel", "Slim Design"],
               price=350, regular=700, head=ROSE, accent=(244, 238, 234), maxw=420, maxh=500)),
    ("D", dict(out="06_minitree_tritan_bottle", img=HQ + "08.png", tag="BABY", title="Minitree Tritan Baby Bottle",
               feats=["BPA Free Tritan", "210 ml", "Easy Grip Handles"], price=450, regular=650,
               bg=(246, 230, 236), rule=(226, 204, 212), ink=ROSE, maxw=640, maxh=420)),
    ("E", dict(out="07_oraimo_necklace_lite", img=HQ + "04.png", tag="NECKBAND", title="Oraimo Necklace Lite",
               sub="Official  •  ENC Wireless Neckband", feats=["30 Hrs Playtime", "ENC Clear Calls", "Dual Device", "Call Vibration"],
               price=1300, regular=1485, accent=(236, 234, 244), maxw=400, maxh=500)),
    ("F", dict(out="08_thermal_lineup", tag="WINTER", title="Thermal Bottles for Winter", sub="Keep your tea and coffee hot all day",
               items=[dict(img=FL + "hgt_tumbler.png", name="Have Good Time Tumbler", note="750 ml  •  Pink & White", price=1000, regular=1200, accent=(250, 236, 238)),
                      dict(img=HQ + "16.png", name="Premium Thermal Tumbler", note="860 ml  •  With straw", price=800, regular=1200, accent=(240, 236, 248)),
                      dict(img=HQ + "15.png", name="Big Mac 316 Thermos Cup", note="1000 ml  •  Blue", price=1000, regular=1300, accent=(232, 240, 248)),
                      dict(img=HQ + "17.png", name="316 Steel Kids Bottle", note="Brown & Pink", price=800, regular=1100, accent=(246, 238, 232))])),
]

if __name__ == "__main__":
    keys = sys.argv[1:]
    for kind, p in POSTS:
        if keys and p["out"][:2] not in keys: continue
        if "img" in p: p["img"] = im(p["img"])
        for it in p.get("items", []): it["img"] = im(it["img"])
        TEMPLATES[kind](p)
