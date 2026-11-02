"""Everyday Cart daily batch, 2 Nov 2026. Style set 2 (D arch poster, E header ribbon, F list menu)."""
import os, sys
import render_flat as rf
from render_flat import im, HQ
from render_styles import TEMPLATES
rf.OUTDIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "posts", "batch-2026-11-02")) + "/"
os.makedirs(rf.OUTDIR, exist_ok=True)

POSTS = [
    ("D", dict(out="01_oraimo_spacebox_speaker", img=HQ + "01.png", tag="SPEAKER", title="Oraimo SpaceBox Speaker",
               feats=["Light Show", "Thumping Bass", "8W Output", "1800mAh"], price=1841, regular=2299,
               bg=(226, 232, 238), rule=(196, 206, 216), maxw=640, maxh=420)),
    ("E", dict(out="02_colmi_p81_smartwatch", img=HQ + "09.png", tag="SMART WATCH", title="COLMI P81 Smartwatch",
               sub="Bluetooth Calling  •  1.9\" HD Display", feats=["Bluetooth Calling", "100+ Sports Modes", "IP68 Water Resistant", "300mAh Battery"],
               price=1350, regular=1540, accent=(232, 238, 229), maxw=440, maxh=470)),
    ("F", dict(out="03_earbuds_neckband_lineup", tag="AUDIO", title="Earbuds & Neckband Lineup", sub="Official Awei & Oraimo  •  Best prices in Dhaka",
               items=[dict(img=HQ + "11.png", name="Awei T88 Earbuds", note="ANC Support  •  IPX6", price=990, regular=1450, accent=(236, 242, 233)),
                      dict(img=HQ + "10.png", name="Awei T108 Earbuds", note="Wireless  •  Bluetooth", price=950, regular=1199, accent=(232, 238, 244)),
                      dict(img=HQ + "13.png", name="Oraimo SpaceBuds Lite", note="Official Oraimo", price=1310, regular=1496, accent=(246, 236, 232)),
                      dict(img=HQ + "04.png", name="Oraimo Necklace Lite", note="ENC Neckband", price=1300, regular=1485, accent=(240, 236, 246))])),
    ("D", dict(out="04_22in_big_teddy_bear", img=HQ + "06.png", tag="GIFT IDEA", title="22\" Big Teddy Bear",
               feats=["22 Inch", "Super Soft Plush", "Perfect Gift"], price=1150, regular=2000,
               bg=(244, 226, 228), rule=(226, 200, 202), ink=ROSE if False else (165, 112, 111), maxw=560, maxh=580)),
    ("E", dict(out="05_awei_ka5_speaker", img=HQ + "14.png", tag="SPEAKER", title="Awei KA5 20W Speaker",
               sub="Stereo Sound  •  IPX5 Waterproof", feats=["10W x 2 Output", "Bluetooth 5.3", "Up to 8 Hrs Play", "IPX5 Waterproof"],
               price=2525, regular=2849, head=(165, 112, 111), accent=(246, 240, 226), maxw=340, maxh=480)),
    ("D", dict(out="06_forkan_trolley_luggage", img=HQ + "05.png", tag="TRAVEL", title="Forkan Trolley Luggage",
               feats=["Hard Shell", "360° Wheels", "20\" & 24\""], price=4000, regular=5500, label="FROM",
               bg=(222, 232, 222), rule=(196, 210, 194), maxw=420, maxh=600)),
    ("E", dict(out="07_silent_alarm_clock", img=HQ + "07.png", tag="HOME", title="Silent Alarm Clock",
               sub="Non-Ticking  •  Quartz Movement", feats=["No Ticking Sound", "Precise Quartz", "Classic Twin Bell", "Bedside Decor"],
               price=500, regular=800, accent=(244, 234, 226), maxw=420, maxh=470)),
    ("D", dict(out="08_proove_intro_pro_earbuds", img=HQ + "03.png", tag="EARBUDS", title="Proove Intro Pro Earbuds",
               feats=["13mm Driver", "ENC Clear Calls", "Bluetooth 5.4"], price=2300, regular=2300,
               bg=(232, 230, 238), rule=(206, 204, 216), maxw=500, maxh=560)),
]

if __name__ == "__main__":
    keys = sys.argv[1:]
    for kind, p in POSTS:
        if keys and p["out"][:2] not in keys: continue
        if "img" in p: p["img"] = im(p["img"])
        for it in p.get("items", []): it["img"] = im(it["img"])
        TEMPLATES[kind](p)
