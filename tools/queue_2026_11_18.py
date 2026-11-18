"""Queue 18 Nov 2026 posts (5 images, NEW style set 13, + 1 Reel). Exactly 5 hashtags each, no dashes."""
import json, re, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from hashtags import pick, retag
CTA = "⚡ Limited stock available!\n🛒 Order now: everydaycart.online\n📩 Or inbox us to place your order"
D = "2026-11-18"
B = "posts/batch-2026-11-18/"
POSTS = [
 dict(slug="oraimo-spacebuds-neo-plus", time="11:30", type="image", media=[B + "01_oraimo_spacebuds_neo_plus.jpg"], cat="earbuds", brand="oraimo", cap=
"""🎧 Wireless gaming earbuds with low latency game mode, Sound360 spatial audio and up to 30 hours battery, 1,940৳

Oraimo SpaceBuds Neo+ (Official), Off-White
গান আর গেম দুটোর জন্যই অফিসিয়াল ওরাইমো ইয়ারবাড।

✔️ Sound360 spatial audio
✔️ Low latency game mode
✔️ 2 noise reducing mics for clear calls
✔️ Up to 30 hours battery life
✔️ Bluetooth 5.4, IPX4 water resistant

💰 Price: 1,940৳ (regular 2,189৳)

Which game do you play the most? Tell us below 👇
"""),
 dict(slug="minitree-baby-bottles", time="13:30", type="image", media=[B + "02_minitree_bottles.jpg"], cat="babyfeed", brand="minitree", cap=
"""🍼 Baby feeding bottles with easy grip handles: Minitree Tritan 210 ml and Minitree 120 ml training bottle, 450৳ each

Bottles little hands can hold on their own
ছোট্ট হাতে ধরার মতো হ্যান্ডেলওয়ালা বেবি ফিডার।

1️⃣ Minitree Tritan Baby Bottle with Handles (7 oz)
✔️ BPA free Tritan, 210 ml
✔️ Soft nipple, easy grip handles
✔️ For babies 3+ months
💰 450৳ (regular 650৳)

2️⃣ Minitree 120 ml Baby Feeding Bottle
✔️ Training bottle for 6 months and up
✔️ Ergonomic handles, easy grip textured body
✔️ Protective nipple cover
💰 450৳ (regular 600৳)

How old is your little one? Comment and we will help you pick 👇
"""),
 dict(slug="have-good-time-tumbler", time="16:30", type="image", media=[B + "03_have_good_time_tumbler.jpg"], cat="tumbler", brand=None, cap=
"""☕ Insulated steel tumbler 750 ml with secure travel lid and carry handle for winter tea and coffee, 1,000৳

Have a Good Time Insulated Steel Thermal Tumbler
শীতের সকালে গরম চা কফির জন্য স্টাইলিশ টাম্বলার।

✔️ 750 ml capacity
✔️ Insulated stainless steel
✔️ Secure travel lid
✔️ Easy carry handle
✔️ For work, university and travel

💰 Price: 1,000৳ (regular 1,200৳)

Tea or coffee: what goes in yours? ☕👇
"""),
 dict(slug="reel-awei-ka5-rooftop-volume", time="18:30", type="reel", media=["videos/2026-11-18/1830_reel-awei-ka5-rooftop-volume.mp4"], cover_ms=2600, cat="speaker", brand="awei", cap=
"""🔊 20W portable Bluetooth speaker with IPX5 waterproofing and up to 8 hours playback: Awei KA5, 2,525৳

Rooftop adda volume check
ছাদের আড্ডায় গান চাই? সাথে রাখুন এই ব্লুটুথ স্পিকার।

✔️ 10W x 2 output power
✔️ 2400mAh battery
✔️ 7.5 to 8 hours playback (at 70% volume)
✔️ IPX5 waterproof
✔️ Bluetooth 5.3

💰 Price: 2,525৳ (regular 2,849৳)

Which song plays first at your rooftop adda? 🎶👇
"""),
 dict(slug="elephant-plush-soft-toy", time="20:00", type="image", media=[B + "04_elephant_plush.jpg"], cat="toys", brand=None, cap=
"""🐘 Elephant plush soft toy, 18 inch, super soft and huggable gift for kids, 750৳

Elephant Plush Soft Toy (18 inch)
নরম তুলতুলে হাতির সফট টয়, ছোটদের জন্য মিষ্টি উপহার।

✔️ 18 inch size
✔️ Super soft and huggable
✔️ A sweet gift for kids and loved ones

💰 Price: 750৳ (regular 1,100৳)

Who would you send this hug to? Tag them 👇
"""),
 dict(slug="portable-bbq-grill", time="21:30", type="image", media=[B + "05_portable_bbq_grill.jpg"], cat="bbq", brand=None, cap=
"""🔥 Portable BBQ grill machine with adjustable charcoal tray and manual air blower for winter rooftop BBQ, 5,500৳

Portable BBQ Grill Machine
শীতের রাতে ছাদে বারবিকিউ পার্টির জন্য পোর্টেবল বারবিকিউ গ্রিল।

✔️ Durable steel body
✔️ Adjustable charcoal tray
✔️ Manual air blower for heat control
✔️ For picnics, camping and rooftop BBQ

💰 Price: 5,500৳ (regular 9,500৳)

Chicken or beef on the grill first? 🍢👇
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
