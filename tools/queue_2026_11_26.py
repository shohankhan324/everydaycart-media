"""Queue 26 Nov 2026 posts (5 images, NEW style set 21, + 1 Reel). Exactly 5 hashtags each, no dashes."""
import json, re, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from hashtags import pick, retag
CTA = "⚡ Limited stock available!\n🛒 Order now: everydaycart.online\n📩 Or inbox us to place your order"
D = "2026-11-26"
B = "posts/batch-2026-11-26/"
POSTS = [
 dict(slug="oraimo-spacebuds-lite-40-hours-music", time="11:30", type="image", media=[B + "01_oraimo_spacebuds_lite.jpg"], cat="earbuds", brand="oraimo", cap=
"""🎧 Wireless earbuds with up to 40 hours of music in one small case: Oraimo SpaceBuds Lite with Sound360 and AI call noise cancellation, 1,310৳

Oraimo SpaceBuds Lite (Official)
কেসসহ ৪০ ঘণ্টা পর্যন্ত গান, অফিসিয়াল ওরাইমো ইয়ারবাড।

✔️ Up to 40 hours playtime with case
✔️ Sound360 spatial audio
✔️ AI call noise cancellation
✔️ Bluetooth 5.4, 10 mm driver
✔️ IPX4 water resistant

💰 Price: 1,310৳ (regular 1,496৳)

How many hours of music do you listen to in a day? 👇
"""),
 dict(slug="wide-neck-baby-feeder-easy-clean", time="13:30", type="image", media=[B + "02_wide_neck_baby_feeder.jpg"], cat="babyfeed", brand=None, cap=
"""🍼 Wide neck baby feeder, BPA free, with soft anti colic silicone nipple: easy to fill, easy to clean, 450৳

Wide Neck Baby Feeder
নরম নিপলের বেবি ফিডার, ভরা আর পরিষ্কার করা দুটোই সহজ।

✔️ Soft anti colic silicone nipple
✔️ BPA free, food grade PP
✔️ Wide neck for easy filling and cleaning

💰 Price: 450৳ (regular 700৳)

Tag a mom or dad who would like this 💕
"""),
 dict(slug="winter-flasks-thermal-bottle-big-mac-cup", time="16:30", type="image", media=[B + "03_winter_flasks_duo.jpg"], cat="bottle", brand=None, extra="#ThermosCup", cap=
"""☕ Thermal water bottle 600 ml (800৳) and Big Mac 1000 ml thermos cup (1,000৳) for hot tea and coffee all winter

Hot sips all day, pick your size
শীতে গরম চা কফির জন্য পছন্দের ফ্লাস্ক বেছে নিন।

1️⃣ Premium Thermal Water Bottle, 600 ml
✔️ Leak proof flip top lid
✔️ Built in straw
✔️ Comfortable side handle
💰 800৳ (regular 1,250৳)

2️⃣ Big Mac 316 Stainless Steel Thermos Cup, 1000 ml
✔️ 316 stainless steel
✔️ Handle and straw
✔️ Leak resistant lid
💰 1,000৳ (regular 1,300৳)

600 ml or 1000 ml: which size fits your day? Comment 1 or 2 👇
"""),
 dict(slug="reel-elephant-plush-gift-box-surprise", time="18:30", type="reel", media=["videos/2026-11-26/1830_reel-elephant-plush-gift-box-surprise.mp4"], cat="toys", brand=None, extra="#KidsGift", cover_ms=4200, cap=
"""🎁 Elephant plush soft toy, 18 inch, super soft and huggable: a sweet gift for kids, 750৳

617 Elephant Plush Soft Toy (18 inch)
ছোট্ট সোনার জন্য নরম তুলতুলে হাতির সফট টয়, মিষ্টি একটা উপহার।

✔️ 18 inch size
✔️ Super soft and huggable
✔️ A sweet gift for kids and loved ones

💰 Price: 750৳ (regular 1,100৳)

Who would you surprise with this? Tag them 👇
"""),
 dict(slug="portable-bbq-grill-rooftop-winter-night", time="20:00", type="image", media=[B + "04_portable_bbq_grill.jpg"], cat="bbq", brand=None, cap=
"""🔥 Portable BBQ grill machine with adjustable charcoal tray and manual air blower for rooftop BBQ nights this winter, 5,500৳

Portable BBQ Grill Machine
শীতের রাতে ছাদে বারবিকিউ পার্টির জন্য পোর্টেবল বারবিকিউ গ্রিল।

✔️ Durable steel body
✔️ Adjustable charcoal tray
✔️ Manual air blower for heat control
✔️ For picnics, camping and rooftop BBQ

💰 Price: 5,500৳ (regular 9,500৳)

Who is coming to your rooftop BBQ? Tag your BBQ squad 🍢👇
"""),
 dict(slug="awei-ka5-20w-speaker-adda-night", time="21:30", type="image", media=[B + "05_awei_ka5_speaker.jpg"], cat="speaker", brand="awei", cap=
"""🔊 20W portable Bluetooth speaker with IPX5 waterproofing and a 2400mAh battery: Awei KA5 for every adda night, 2,525৳

Awei KA5 20W Portable Bluetooth Speaker
আড্ডা জমাতে ২০ ওয়াটের ব্লুটুথ স্পিকার।

✔️ 10W x 2 output power
✔️ 2400mAh battery
✔️ 7.5 to 8 hours playback (at 70% volume)
✔️ IPX5 waterproof
✔️ Bluetooth 5.3

💰 Price: 2,525৳ (regular 2,849৳)

Which song plays first at your adda? 🎶👇
"""),
]
q = json.load(open("scheduler/queue.json")); ids = {e["id"] for e in q}; sets = []
for p in POSTS:
    pid = f"{D}-{p['slug']}"; assert pid not in ids, pid
    tags = pick(p["cat"], brand=p["brand"], seed=pid, extra=p.get("extra")); sets.append(tuple(sorted(tags)))
    cap = retag(p["cap"].rstrip() + "\n\n" + CTA, tags)
    assert len(re.findall(r"#\w+", cap)) == 5, cap
    assert "—" not in cap and "–" not in cap and "#EverydayCart" not in cap and "#Reels" not in cap
    for m in p["media"]: assert os.path.exists(m), m
    e = {"id": pid, "time": f"{D}T{p['time']}:00+06:00", "type": p["type"], "media": p["media"], "caption": cap, "networks": ["facebook", "instagram"]}
    if "cover_ms" in p: e["cover_ms"] = p["cover_ms"]
    q.append(e); print(pid, tags)
assert len(set(sets)) == len(sets)
q.sort(key=lambda e: e["time"])
json.dump(q, open("scheduler/queue.json", "w"), ensure_ascii=False, indent=2)
