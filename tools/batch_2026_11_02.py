"""Everyday Cart daily batch, 2 Nov 2026 (render_flat templates)."""
import os, sys
import render_flat as rf
from render_flat import template_a, template_b, template_c, im, HQ
rf.OUTDIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "posts", "batch-2026-11-02")) + "/"
os.makedirs(rf.OUTDIR, exist_ok=True)

POSTS = [
    ("A", dict(out="01_oraimo_spacebox_speaker", img=HQ + "01.png", tag="SPEAKER", title="Oraimo SpaceBox Speaker",
               sub="Official  •  Portable Bluetooth", feats=["Personalized Light Show", "Thumping Bass", "8W Audio Output", "1800mAh Battery"],
               price=1841, regular=2299, accent=(230, 236, 242))),
    ("B", dict(out="02_colmi_p81_smartwatch", img=HQ + "09.png", tag="SMART WATCH", title="COLMI P81 Calling Smartwatch",
               sub="Bluetooth Calling  •  1.9\" HD Display", feats=["Bluetooth Calling", "100+ Sports Modes", "IP68", "300mAh Battery"],
               price=1350, regular=1540, bg=(234, 240, 232), circle=(247, 250, 245), chip=(236, 243, 234), maxw=520, maxh=580)),
    ("C", dict(out="03_earbuds_neckband_lineup", tag="AUDIO", title="Earbuds & Neckband Lineup", sub="Official Awei & Oraimo  •  Best prices in Dhaka",
               items=[dict(img=HQ + "11.png", name="Awei T88 Earbuds", price=990, regular=1450),
                      dict(img=HQ + "10.png", name="Awei T108 Earbuds", price=950, regular=1199),
                      dict(img=HQ + "13.png", name="Oraimo SpaceBuds Lite", price=1310, regular=1496),
                      dict(img=HQ + "04.png", name="Oraimo Necklace Lite", price=1300, regular=1485)],
               accent=(236, 242, 233))),
    ("A", dict(out="04_22in_big_teddy_bear", img=HQ + "06.png", tag="GIFT", title="22\" Big Teddy Bear",
               sub="Super Soft Premium Plush", feats=["22 Inch Big Size", "Super Soft Plush", "Perfect Gift", "Cute Room Decor"],
               price=1150, regular=2000, accent=(246, 230, 232))),
    ("B", dict(out="05_awei_ka5_speaker", img=HQ + "14.png", tag="SPEAKER", title="Awei KA5 20W Speaker",
               sub="Stereo Sound  •  IPX5 Waterproof", feats=["10W x 2 Output", "Bluetooth 5.3", "Up to 8 Hrs Play", "IPX5"],
               price=2525, regular=2849, bg=(244, 240, 226), circle=(252, 250, 242), chip=(246, 242, 230), maxw=420, maxh=600, badge=(880, 400))),
    ("A", dict(out="06_forkan_trolley_luggage", img=HQ + "05.png", tag="TRAVEL", title="Forkan Trolley Luggage",
               sub="Hard Shell  •  20\" & 24\" Sizes", feats=["Durable Hard Shell", "360° Spinner Wheels", "Spacious Interior", "Lightweight"],
               label="FROM", price=4000, regular=5500, accent=(246, 230, 228))),
    ("B", dict(out="07_silent_alarm_clock", img=HQ + "07.png", tag="HOME", title="Silent Alarm Clock",
               sub="Non-Ticking  •  Quartz Movement", feats=["No Ticking Sound", "Precise Quartz", "Classic Twin Bell", "Bedside Decor"],
               price=500, regular=800, bg=(242, 234, 226), circle=(251, 247, 242), chip=(245, 238, 231), maxw=520, maxh=580)),
    ("B", dict(out="08_proove_intro_pro_earbuds", img=HQ + "03.png", tag="EARBUDS", title="Proove Intro Pro Earbuds",
               sub="Official  •  LED Display Charging Case", feats=["13mm Driver", "Clear Calls (ENC)", "Bluetooth 5.4", "Touch Control"],
               price=2300, regular=2300, bg=(236, 238, 242), circle=(248, 249, 251), chip=(238, 240, 244), maxw=520, maxh=580)),
]

if __name__ == "__main__":
    keys = sys.argv[1:]
    for kind, p in POSTS:
        if keys and p["out"][:2] not in keys: continue
        if "img" in p: p["img"] = im(p["img"])
        for it in p.get("items", []): it["img"] = im(it["img"])
        {"A": template_a, "B": template_b, "C": template_c}[kind](p)
