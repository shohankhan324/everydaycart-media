"""Queue 12 Nov 2026 posts (5 images, NEW style set 7, + 1 Reel). Exactly 5 hashtags each, no dashes."""
import json, re, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from hashtags import pick, retag
CTA = "⚡ Limited stock available!\n🛒 Order now: everydaycart.online\n📩 Or inbox us to place your order"
D = "2026-11-12"
POSTS = [
 dict(slug="oraimo-watch-5-lite", time="11:30", type="image", media=["posts/batch-2026-11-12/01_oraimo_watch_5_lite.jpg"], cat="smartwatch", brand="oraimo", cap=
"""⌚ Calling smart watch with 2.01" HD display, IP68 and up to 7 days battery

Oraimo Watch 5 Lite Smart Watch (Official)
কল ধরুন সরাসরি হাতের স্মার্ট ওয়াচ থেকে।

✔️ 2.01" HD display
✔️ HD voice Bluetooth calling
✔️ IP68 dust and water resistance
✔️ 105+ sports modes
✔️ Up to 7 days battery life

💰 Price: 1,650৳ (regular 1,870৳)

Do you take calls on your watch? Tell us 👇

"""),
 dict(slug="winter-thermal-bottles", time="13:30", type="image", media=["posts/batch-2026-11-12/02_winter_sip_collection.jpg"], cat="bottle", brand=None, cap=
"""☕ Thermal bottles and tumblers for winter, from 350৳

Warm sips all winter, pick your flask!
শীতে গরম চা কফির জন্য পছন্দের ফ্লাস্ক বেছে নিন।

✔️ Big Mac 316 Stainless Steel Thermos Cup, 1000 ml, Blue: 1,000৳ (regular 1,300৳)
✔️ Premium Thermal Tumbler, 860 ml, with straw: 800৳ (regular 1,200৳)
✔️ Smart LED Temperature Bottle, 500 ml, Black or White: 350৳ (regular 700৳)
✔️ Premium Thermal Water Bottle, 600 ml, with straw: 800৳ (regular 1,250৳)

Which one is your pick? Comment 1, 2, 3 or 4 👇

"""),
 dict(slug="wide-neck-baby-feeder", time="16:30", type="image", media=["posts/batch-2026-11-12/03_wide_neck_baby_feeder.jpg"], cat="babyfeed", brand=None, cap=
"""🍼 Wide neck baby feeder with soft anti colic nipple, BPA free

Wide Neck Baby Feeder
নরম নিপলের বেবি ফিডার, খাওয়ানো আর পরিষ্কার দুটোই সহজ।

✔️ Soft anti colic silicone nipple
✔️ BPA free, food grade PP
✔️ Wide neck for easy filling and cleaning

💰 Price: 450৳ (regular 700৳)

"""),
 dict(slug="reel-oraimo-spacebuds-lite-specs", time="18:30", type="reel", media=["videos/2026-11-12/1830_reel-oraimo-spacebuds-lite-specs.mp4"], cover_ms=3000, cat="earbuds", brand="oraimo", cap=
"""🎧 Wireless earbuds with up to 40 hours playtime with case and AI call noise cancellation

Oraimo SpaceBuds Lite (Official)
কেসসহ ৪০ ঘণ্টা পর্যন্ত গান, দেখে নিন এই ইয়ারবাডের স্পেকস!

✔️ Sound360 spatial audio
✔️ AI call noise cancellation
✔️ Up to 40 hours playtime with case
✔️ Bluetooth 5.4
✔️ IPX4 water resistant

💰 Price: 1,310৳ (regular 1,496৳)

Which spec matters most to you? Comment below 👇

"""),
 dict(slug="portable-massage-gun", time="20:00", type="image", media=["posts/batch-2026-11-12/04_massage_gun.jpg"], cat="massage", brand=None, cap=
"""💆 Portable rechargeable massage gun with 4 massage heads, for gym and office tiredness

Portable Rechargeable Massage Gun
ঘরে বসেই ম্যাসাজ গান দিয়ে ক্লান্তি দূর করুন।

✔️ 4 interchangeable massage heads
✔️ Powerful yet quiet motor
✔️ Lightweight, ergonomic design
✔️ Rechargeable and portable

💰 Price: 850৳ (regular 1,200৳)

Who needs this after a long day? Tag them 👇

"""),
 dict(slug="silent-alarm-clock", time="21:30", type="image", media=["posts/batch-2026-11-12/05_silent_alarm_clock.jpg"], cat="clock", brand=None, extra="#AlarmClock", cap=
"""⏰ Silent alarm clock with no ticking sound, twin bell design for your bedside

Silent Alarm Clock
টিকটিক শব্দ ছাড়া অ্যালার্ম ঘড়ি, রাতে শান্তির ঘুম।

✔️ Non ticking, silent operation
✔️ Precise quartz movement
✔️ Classic twin bell design
✔️ Elegant bedside decor

💰 Price: 500৳ (regular 800৳)

Good night from Everyday Cart 🌙

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
