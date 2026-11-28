"""Queue 28 Nov 2026 posts (5 images, NEW style set 23, + 1 Reel). Exactly 5 hashtags each, no dashes."""
import json, re, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from hashtags import pick, retag
CTA = "⚡ Limited stock available!\n🛒 Order now: everydaycart.online\n📩 Or inbox us to place your order"
D = "2026-11-28"
B = "posts/batch-2026-11-28/"
POSTS = [
 dict(slug="oraimo-watch-5-lite-calls-from-your-wrist", time="11:30", type="image", media=[B + "01_oraimo_watch_5_lite.jpg"], cat="smartwatch", brand="oraimo", cap=
"""⌚ Calling smart watch with 2.01" HD display, HD voice in calls, IP68 and up to 7 days battery: Oraimo Watch 5 Lite, 1,650৳

Oraimo Watch 5 Lite Smart Watch (Official)
ফোন পকেটেই থাকুক, কল ধরুন স্মার্ট ওয়াচে।

✔️ 2.01" HD display
✔️ HD voice in calls
✔️ AI generated watch faces
✔️ IP68 dust and water resistance
✔️ 105+ sports modes
✔️ Up to 7 days battery life

💰 Price: 1,650৳ (regular 1,870৳)

Calls, steps or sports modes: what would you use most? 👇
"""),
 dict(slug="minitree-baby-bottles-mumpot-first-sips", time="13:30", type="image", media=[B + "02_minitree_baby_trio.jpg"], cat="babyfeed", brand="minitree", cap=
"""🍼 Minitree baby feeding bottles and duckbill sippy cup from 400৳: Tritan bottle 7 oz, 120 ml training bottle and Mumpot 280 ml

First bottles and first sips
ছোট্ট সোনার জন্য মিনিট্রি বেবি ফিডার আর মাম্পট।

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

3️⃣ Minitree Duckbill Mumpot 280 ml
✔️ Soft duckbill spout, two easy grip handles
✔️ For babies 3+ months, Pink or Sky Blue
💰 400৳ (regular 550৳)

Which one is right for your little one now? Comment 1, 2 or 3 👇
"""),
 dict(slug="massage-gun-long-day-relax-at-home", time="16:30", type="image", media=[B + "03_massage_gun.jpg"], cat="massage", brand=None, extra="#MassageGun", cap=
"""💆 Portable rechargeable massage gun with 4 massage heads and a quiet motor for after office and gym, 850৳

Portable Rechargeable Massage Gun
লম্বা অফিসের পর ক্লান্ত শরীরে ঘরেই ম্যাসাজ গানে আরাম নিন।

✔️ 4 interchangeable massage heads
✔️ Powerful yet quiet motor
✔️ Lightweight, ergonomic design
✔️ Rechargeable and portable

💰 Price: 850৳ (regular 1,200৳)

Neck, shoulders or legs: where do you feel the long day most? 👇
"""),
 dict(slug="reel-awei-t88-earbuds-under-1000", time="18:30", type="reel", media=["videos/2026-11-28/1830_reel-awei-t88-earbuds-under-1000.mp4"], cat="earbuds", brand="awei", cover_ms=2300, cap=
"""🎧 Wireless earbuds under 1,000৳ with ANC support, 10mm driver, IPX6 and Bluetooth 5.4: Awei T88, 990৳

Awei T88 Wireless Earbuds
১০০০ টাকার নিচে ভালো ইয়ারবাড খুঁজছেন? দাম মাত্র ৯৯০ টাকা।

✔️ ANC support
✔️ 10mm driver unit
✔️ IPX6 water resistant
✔️ Bluetooth 5.4, touch control
✔️ 1 hour fast charging

💰 Price: 990৳ (regular 1,450৳)

Music, calls or movies? Comment 1, 2 or 3 👇
"""),
 dict(slug="big-teddy-bear-22-inch-soft-hug-gift", time="20:00", type="image", media=[B + "04_big_teddy_bear.jpg"], cat="toys", brand=None, cap=
"""🧸 22 inch big teddy bear, super soft premium plush gift for someone special, 1,150৳

22" Big Teddy Bear
প্রিয়জনের জন্য বড় টেডি বিয়ার উপহার দিন।

✔️ 22 inch big size
✔️ Super soft premium plush
✔️ Perfect for cuddling and decorating
✔️ A lovely gift for any special occasion

💰 Price: 1,150৳ (regular 2,000৳)

Who deserves a big hug this week? Tag them 👇
"""),
 dict(slug="silent-alarm-clock-no-tick-sweet-sleep", time="21:30", type="image", media=[B + "05_silent_alarm_clock.jpg"], cat="clock", brand=None, cap=
"""⏰ Silent alarm clock with no ticking sound, quartz movement and classic twin bell design, 500৳

Silent Alarm Clock
টিকটিক শব্দ ছাড়া অ্যালার্ম ঘড়ি, রাতে শান্তির ঘুম।

✔️ Non ticking, silent operation
✔️ Precise quartz movement
✔️ Classic twin bell design
✔️ Elegant bedside decor

💰 Price: 500৳ (regular 800৳)

What time is your alarm set for tomorrow? Good night 🌙
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
