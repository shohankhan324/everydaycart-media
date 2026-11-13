"""Everyday Cart daily batch, 13 Nov 2026. NEW style set 8 (render_styles8: Q magazine cover, R sticker sheet).
5 image posts + 1 Reel."""
import os, sys
import render_flat as rf
from render_flat import im, HQ, FL
from render_styles8 import TEMPLATES8 as T
rf.OUTDIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "posts", "batch-2026-11-13")) + "/"
os.makedirs(rf.OUTDIR, exist_ok=True)

POSTS = [
    ("Q", dict(out="01_oraimo_spacebuds_neo_plus", img=HQ + "12.png", tag="EARBUDS", word="SOUND", kicker="OFFICIAL ORAIMO",
               title="Oraimo SpaceBuds Neo+ (Official)", bn="সারাদিনের গান আর গেমের জন্য ইয়ারবাড",
               feats=[["Sound360", "spatial audio"], ["Up to 30 hours", "battery life"], ["Low latency", "game mode"]],
               price=1940, regular=2189, bg=(22, 40, 74), acc=(255, 196, 64), maxw=460, maxh=500, cx=670, cy=710, r=290, sy=970)),
    ("R", dict(out="02_bluetooth_speakers", tag="SPEAKERS", head=["Weekend plans?", "Bring the sound!"],
               items=[(HQ + "01.png", "Oraimo SpaceBox", 1841, 2299, (206, 226, 255)), (HQ + "14.png", "Awei KA5 20W", 2525, 2849, (255, 232, 160))],
               scales=[0.62, 1.0], cy=640, bg=(236, 242, 255), acc=(48, 76, 200), pfill=(48, 76, 200), acc2=(255, 116, 76),
               stickers=[(840, 340, "IPX5 waterproof", 6, (255, 116, 76)), (250, 370, "Light show", -5, (48, 76, 200))],
               bn="বাড়ির আড্ডায় ব্লুটুথ স্পিকার", bny=1182, tape=(255, 116, 76))),
    ("Q", dict(out="03_kodomo_lotion_powder", img=FL + "kodomo_lotion.png", tag="BABY CARE", word="SOFT", kicker="FOR LITTLE ONES",
               title="Kodomo Baby Lotion Powder 180 ml", bn="শিশুর নরম ত্বকের জন্য লোশন পাউডার",
               feats=[["Extra mild", "formula"], ["Lotion that dries", "to soft powder"], ["Suitable from", "0+ months"]],
               price=720, regular=880, bg=(78, 150, 210), acc=(255, 214, 226), maxw=290, maxh=540, cx=640, cy=720, r=280, sx=930, sy=980)),
    ("R", dict(out="04_have_good_time_tumbler", img=FL + "hgt_tumbler.png", tag="TUMBLER", head=["Your warm sip buddy", "for winter mornings"],
               title="Have Good Time Insulated Tumbler 750 ml", feats=["750 ml", "Carry handle", "Secure lid"],
               spos=[(190, 470, -6), (900, 560, 5), (200, 930, -3)],
               price=1000, regular=1200, bg=(255, 236, 240), acc=(232, 84, 120), acc2=(40, 48, 66), disc=(255, 205, 216),
               scol=[(40, 48, 66), (232, 84, 120), (120, 150, 120)], maxw=520, maxh=470, cx=560, cy=700, r=290,
               px=860, py=960, bn="শীতের সকালে গরম চায়ের টাম্বলার", tape=(40, 48, 66))),
    ("Q", dict(out="05_portable_bbq_grill", img=HQ + "27.png", tag="BBQ GRILL", word="GRILL", kicker="WINTER NIGHTS",
               title="Portable BBQ Grill Machine", bn="শীতের রাতে ছাদে বারবিকিউ পার্টি",
               feats=[["Durable", "steel body"], ["Adjustable", "charcoal tray"], ["Manual air", "blower"]],
               price=5500, regular=9500, bg=(34, 34, 38), acc=(255, 120, 48), maxw=520, maxh=500, cx=670, cy=730, r=290)),
]

if __name__ == "__main__":
    keys = sys.argv[1:]
    for kind, p in POSTS:
        if keys and p["out"][:2] not in keys: continue
        if "items" in p: p["items"] = [(im(a) if isinstance(a, str) else a, *rest) for a, *rest in p["items"]]
        elif isinstance(p["img"], str): p["img"] = im(p["img"])
        T[kind](p)
