"""Queue 24 Nov 2026 posts (5 images, NEW style set 19, + 1 Reel). Exactly 5 hashtags each, no dashes."""
import json, re, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from hashtags import pick, retag
CTA = "⚡ Limited stock available!\n🛒 Order now: everydaycart.online\n📩 Or inbox us to place your order"
D = "2026-11-24"
B = "posts/batch-2026-11-24/"
POSTS = [
 dict(slug="oraimo-watch-5-lite-gift-that-takes-calls", time="11:30", type="image", media=[B + "01_oraimo_watch_5_lite.jpg"], cat="smartwatch", brand="oraimo", cap=
"""⌚ Calling smart watch with 2.01" HD display, HD voice calls, IP68 and up to 7 days battery, 1,650৳

Oraimo Watch 5 Lite Smart Watch (Official)
প্রিয়জনকে উপহার দিন কলিং স্মার্ট ওয়াচ, ফোন পকেটেই থাকুক।

✔️ 2.01" HD display
✔️ HD voice in calls
✔️ AI generated watch faces
✔️ IP68 dust and water resistance
✔️ 105+ sports modes
✔️ Up to 7 days battery life

💰 Price: 1,650৳ (regular 1,870৳)

Who would you gift a smart watch to? Tag them 👇
"""),
 dict(slug="baby-toilet-seat-potty-time-made-comfy", time="13:30", type="image", media=[B + "02_baby_toilet_seat.jpg"], cat="baby", brand=None, cap=
"""🚽 Baby toilet seat reducer with soft cushion, secure handles and splash guard for comfy potty training, 800৳

Soft Cushioned Baby Toilet Seat Reducer with Handles
বাচ্চার পটি ট্রেনিং সহজ করতে নরম টয়লেট সিট।

✔️ Soft cushioned seat
✔️ Secure handles to hold on
✔️ Splash guard
✔️ Waterproof, easy to clean
✔️ For 18 months and above

💰 Price: 800৳ (regular 1,000৳)

Parents, at what age did potty training start at your home? 👇
"""),
 dict(slug="winter-flask-duo-hot-cha-800-each", time="16:30", type="image", media=[B + "03_winter_flask_duo.jpg"], cat="bottle", brand=None, cap=
"""☕ Thermal bottle 700 ml and thermal tumbler 860 ml for hot winter tea and coffee, 800৳ each

Hot cha all day, 800৳ each
শীতের সকালে গরম চায়ের জন্য পছন্দের ফ্লাস্ক বেছে নিন।

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

Bottle for the bag or tumbler for the desk? Comment 1 or 2 👇
"""),
 dict(slug="reel-massage-gun-after-office-relax", time="18:30", type="reel", media=["videos/2026-11-24/1830_reel-massage-gun-after-office-relax.mp4"],
      cover_ms=2000, cat="massage", brand=None, cap=
"""💆 Portable rechargeable massage gun with 4 massage heads and a quiet motor, 850৳

Tired after office? Relax at home
অফিস শেষে ক্লান্ত? ঘরেই ম্যাসাজ গানে আরাম নিন।

Portable Rechargeable Massage Gun
✔️ 4 interchangeable massage heads
✔️ Powerful yet quiet motor
✔️ Lightweight, ergonomic design
✔️ Rechargeable and portable

💰 Price: 850৳ (regular 1,200৳)

Shoulders, back or legs: where would you use it first? 👇
"""),
 dict(slug="awei-t88-earbuds-under-1000-anc", time="20:00", type="image", media=[B + "04_awei_t88_earbuds.jpg"], cat="earbuds", brand="awei", cap=
"""🎧 Wireless earbuds under 1,000৳ with ANC support, IPX6 water resistance and Bluetooth 5.4, 990৳

Awei T88 Wireless Earbuds, Black
কম দামে ভালো ইয়ারবাড খুঁজছেন? দাম মাত্র ৯৯০ টাকা।

✔️ ANC support
✔️ 10mm driver unit
✔️ IPX6 water resistant
✔️ Bluetooth 5.4, touch control
✔️ 1 hour fast charging

💰 Price: 990৳ (regular 1,450৳)

Music, calls or movies: what do you use earbuds for most? 👇
"""),
 dict(slug="good-night-gifts-teddy-bear-silent-clock", time="21:30", type="image", media=[B + "05_good_night_gifts.jpg"], cat="gift", brand=None, extra="#TeddyBear", cap=
"""🧸 Good night gift ideas: 22 inch big teddy bear 1,150৳ and silent alarm clock 500৳

Two sweet gift picks for someone special
প্রিয়জনকে উপহার দিন টেডি বিয়ার আর অ্যালার্ম ঘড়ি।

1️⃣ 22" Big Teddy Bear
✔️ Super soft premium plush
✔️ Perfect for cuddling and decorating
✔️ A lovely gift for any special occasion
💰 1,150৳ (regular 2,000৳)

2️⃣ Silent Alarm Clock
✔️ Non ticking, silent operation
✔️ Precise quartz movement
✔️ Classic twin bell design
💰 500৳ (regular 800৳)

Teddy or clock: which one would you gift? Comment 1 or 2 🌙
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
