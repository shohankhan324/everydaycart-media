"""Queue 22 Nov 2026 posts (5 images, NEW style set 17, + 1 Reel). Exactly 5 hashtags each, no dashes."""
import json, re, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from hashtags import pick, retag
CTA = "⚡ Limited stock available!\n🛒 Order now: everydaycart.online\n📩 Or inbox us to place your order"
D = "2026-11-22"
B = "posts/batch-2026-11-22/"
POSTS = [
 dict(slug="oraimo-spacebuds-neo-plus-game-music-calls", time="11:30", type="image", media=[B + "01_oraimo_spacebuds_neo_plus.jpg"], cat="earbuds", brand="oraimo", cap=
"""🎧 Wireless earbuds for games, music and calls: low latency game mode, Sound360 spatial audio and up to 30 hours battery, 1,940৳

Oraimo SpaceBuds Neo+ (Official), Off-White
গান আর গেম দুটোর জন্যই অফিসিয়াল ওরাইমো ইয়ারবাড।

✔️ Sound360 spatial audio
✔️ Low latency game mode
✔️ 2 noise reducing mics for clear calls
✔️ Up to 30 hours battery life
✔️ Bluetooth 5.4, IPX4 water resistant

💰 Price: 1,940৳ (regular 2,189৳)

Games, music or calls: what would you use them for most? 👇
"""),
 dict(slug="baby-feeding-bottles-450-each", time="13:30", type="image", media=[B + "02_baby_feeders_450.jpg"], cat="babyfeed", brand="minitree", cap=
"""🍼 Baby feeding bottles at 450৳ each: Minitree Tritan 7 oz, Minitree 120 ml training bottle and wide neck feeder, all BPA free

Three baby feeders, 450৳ each
ছোট্ট সোনার জন্য পছন্দের বেবি ফিডার বেছে নিন।

1️⃣ Minitree Tritan Baby Bottle (7 oz)
✔️ BPA free Tritan, 210 ml
✔️ Soft nipple and easy grip handles
✔️ For babies 3+ months
💰 450৳ (regular 650৳)

2️⃣ Minitree 120 ml Baby Feeding Bottle
✔️ Training bottle with ergonomic handles
✔️ Easy grip textured body, nipple cover
✔️ For babies 6+ months
💰 450৳ (regular 600৳)

3️⃣ Wide Neck Baby Feeder
✔️ Soft anti colic silicone nipple
✔️ BPA free, food grade PP
✔️ Wide neck for easy filling and cleaning
💰 450৳ (regular 700৳)

Which one suits your little one: 1, 2 or 3? 👇
"""),
 dict(slug="winter-tumblers-1000-each", time="16:30", type="image", media=[B + "03_winter_tumblers.jpg"], cat="tumbler", brand=None, cap=
"""☕ Insulated winter tumblers at 1,000৳ each: Big Mac 1000 ml thermos cup with handle and straw, and Have a Good Time 750 ml steel tumbler

Big winter sips, 1,000৳ each
শীতে গরম চা কফির জন্য বড় টাম্বলার বেছে নিন।

1️⃣ Big Mac 316 Stainless Steel Thermos Cup
✔️ Huge 1000 ml capacity
✔️ 316 stainless steel
✔️ Handle and straw
💰 1,000৳ (regular 1,300৳)

2️⃣ Have a Good Time Insulated Steel Thermal Tumbler
✔️ 750 ml capacity
✔️ Insulated stainless steel
✔️ Secure travel lid and carry handle
💰 1,000৳ (regular 1,200৳)

1000 ml or 750 ml: which size is your winter sip? Comment 1 or 2 👇
"""),
 dict(slug="reel-rooftop-bbq-grill-winter-night", time="18:30", type="reel", media=["videos/2026-11-22/1830_reel-rooftop-bbq-grill-winter-night.mp4"], cover_ms=2000, cat="bbq", brand=None, cap=
"""🔥 Portable BBQ grill for winter rooftop nights, picnics and camping: durable steel body, adjustable charcoal tray and manual air blower, 5,500৳

Portable BBQ Grill Machine
শীতের রাতে ছাদে বারবিকিউ পার্টি? সাথে রাখুন পোর্টেবল বারবিকিউ গ্রিল।

✔️ Durable steel body
✔️ Adjustable charcoal tray
✔️ Manual air blower for heat control
✔️ For picnics, camping and rooftop BBQ

💰 Price: 5,500৳ (regular 9,500৳)

Chicken, beef or vegetables: what goes on the grill first? 🍢👇
"""),
 dict(slug="elephant-plush-soft-toy-gift", time="20:00", type="image", media=[B + "04_elephant_plush.jpg"], cat="toys", brand=None, cap=
"""🐘 Elephant plush soft toy, 18 inch, super soft and huggable: a sweet gift for kids, 750৳

Elephant Plush Soft Toy (18 inch)
নরম তুলতুলে হাতির সফট টয়, ছোটদের জন্য মিষ্টি উপহার।

✔️ 18 inch size
✔️ Super soft and huggable
✔️ A sweet gift for kids and loved ones

💰 Price: 750৳ (regular 1,100৳)

Who would you give this hug to? Tag them 👇
"""),
 dict(slug="awei-ka5-speaker-picnic-playlist", time="21:30", type="image", media=[B + "05_awei_ka5_speaker.jpg"], cat="speaker", brand="awei", cap=
"""🔊 20W portable Bluetooth speaker with IPX5 waterproofing, 2400mAh battery and up to 8 hours playback: Awei KA5, 2,525৳

Awei KA5 20W Portable Bluetooth Speaker
পিকনিক আর আড্ডায় গান বাজুক এই ব্লুটুথ স্পিকারে।

✔️ 10W x 2 output power
✔️ 2400mAh battery
✔️ 7.5 to 8 hours playback (at 70% volume)
✔️ IPX5 waterproof
✔️ Bluetooth 5.3

💰 Price: 2,525৳ (regular 2,849৳)

What is the first song on your picnic playlist? 🎶👇
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
