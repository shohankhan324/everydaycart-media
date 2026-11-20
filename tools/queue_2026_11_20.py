"""Queue 20 Nov 2026 posts (5 images, NEW style set 15, + 1 Reel). Exactly 5 hashtags each, no dashes."""
import json, re, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from hashtags import pick, retag
CTA = "⚡ Limited stock available!\n🛒 Order now: everydaycart.online\n📩 Or inbox us to place your order"
D = "2026-11-20"
B = "posts/batch-2026-11-20/"
POSTS = [
 dict(slug="oraimo-watch-5-lite-calling", time="11:30", type="image", media=[B + "01_oraimo_watch_5_lite.jpg"], cat="smartwatch", brand="oraimo", cap=
"""⌚ Calling smart watch with 2.01" HD display, HD voice calls, IP68 and up to 7 days battery, 1,650৳

Oraimo Watch 5 Lite Smart Watch (Official)
ফোন পকেটে রেখেই হাতের স্মার্ট ওয়াচ থেকে কল ধরুন।

✔️ 2.01" HD display
✔️ HD voice in calls
✔️ AI generated watch faces
✔️ IP68 dust and water resistance
✔️ 105+ sports modes
✔️ Up to 7 days battery life

💰 Price: 1,650৳ (regular 1,870৳)

Which watch face would you set first: classic or sporty? 👇
"""),
 dict(slug="baby-toilet-seat-potty-training", time="13:30", type="image", media=[B + "02_baby_toilet_seat.jpg"], cat="baby", brand=None, extra="#PottyTraining", cap=
"""🚽 Baby toilet seat reducer with soft cushion, secure handles and splash guard for easy potty training, 800৳

Soft Cushioned Baby Toilet Seat Reducer with Handles
পটি ট্রেনিং সহজ করতে বাচ্চার নরম টয়লেট সিট।

✔️ Soft cushioned seat
✔️ Secure handles to hold on
✔️ Splash guard
✔️ Waterproof, easy to clean
✔️ For 18 months and above

💰 Price: 800৳ (regular 1,000৳)

Parents, what helped most in your potty training journey? 👇
"""),
 dict(slug="winter-tea-flask-pair", time="16:30", type="image", media=[B + "03_winter_flask_duo.jpg"], cat="bottle", brand=None, cap=
"""☕ Thermal bottle 700 ml and thermal tumbler 860 ml for hot winter tea and coffee, 800৳ each

Morning cha, your way
শীতের সকালে গরম চা কফি রাখুন পছন্দের ফ্লাস্কে।

1️⃣ 316 Stainless Steel Thermal Bottle, 700 ml
✔️ 316 stainless steel
✔️ Safety lock lid
✔️ Easy carry handle
💰 800৳ (regular 1,100৳)

2️⃣ Premium Thermal Tumbler, 860 ml
✔️ Double wall vacuum insulation
✔️ Comfortable handle and reusable straw
✔️ Leak resistant lid
💰 800৳ (regular 1,200৳)

Bottle for the bag or tumbler for the desk? 👇
"""),
 dict(slug="reel-good-night-silent-clock-teddy", time="18:30", type="reel", media=["videos/2026-11-20/1830_reel-good-night-silent-clock-teddy.mp4"], cover_ms=1900, cat="clock", brand=None, extra="#TeddyBear", cap=
"""⏰ Silent alarm clock with no ticking sound and a 22 inch soft teddy bear: your good night kit

Tick tock keeping you awake?
রাতে টিকটিক শব্দ ছাড়া অ্যালার্ম ঘড়ি আর নরম টেডি বিয়ার, শান্তির ঘুমের জন্য।

1️⃣ Silent Alarm Clock
✔️ Non ticking, silent operation
✔️ Precise quartz movement
✔️ Classic twin bell design
💰 500৳ (regular 800৳)

2️⃣ 22" Big Teddy Bear
✔️ 22 inch size
✔️ Super soft premium plush
✔️ A lovely gift for loved ones and kids
💰 1,150৳ (regular 2,000৳)

Tonight you pick: 1 or 2? 👇
"""),
 dict(slug="massage-gun-sore-shoulders", time="20:00", type="image", media=[B + "04_massage_gun.jpg"], cat="massage", brand=None, cap=
"""💆 Portable rechargeable massage gun with 4 massage heads and a quiet motor, for after office and gym, 850৳

Portable Rechargeable Massage Gun
অফিস বা জিমের পর ক্লান্ত শরীরে ঘরেই ম্যাসাজ গানে আরাম নিন।

✔️ 4 interchangeable massage heads
✔️ Powerful yet quiet motor
✔️ Lightweight, ergonomic design
✔️ Rechargeable and portable

💰 Price: 850৳ (regular 1,200৳)

Shoulders, back or legs: where do you feel it most after a long day? 👇
"""),
 dict(slug="home-helpers-water-pot-gloves", time="21:30", type="image", media=[B + "05_home_helpers_pot_gloves.jpg"], cat="home", brand=None, cap=
"""🫖 Insulated stainless steel water pot 1,000৳ and waterproof cleaning gloves 200৳: home helpers for winter

Tea is hot, hands stay dry
ঘরের কাজে স্টিলের জগ আর ক্লিনিং গ্লাভস, দুটোই কাজের।

1️⃣ Stainless Steel Water Pot
✔️ Double wall insulated interior
✔️ Leak proof lid
✔️ Ergonomic handle
💰 1,000৳ (regular 1,400৳)

2️⃣ Premium Cleaning Gloves
✔️ Waterproof soft rubber
✔️ Long floral cuffs keep sleeves dry
✔️ Comfortable and reusable
💰 200৳ (regular 400৳)

Which one does your home need first? 👇
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
