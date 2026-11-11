"""Queue 11 Nov 2026 posts (4 images, NEW style set 6, + 1 Reel). Exactly 5 hashtags each, no dashes.
The owner-approved 11.11 deals repost is already queued at 11:11, so the first new slot is 13:30."""
import json, re, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from hashtags import pick, retag
CTA = "⚡ Limited stock available!\n🛒 Order now: everydaycart.online\n📩 Or inbox us to place your order"
D = "2026-11-11"
POSTS = [
 dict(slug="oraimo-necklace-lite", time="13:30", type="image", media=["posts/batch-2026-11-11/01_oraimo_necklace_lite.jpg"], cat="neckband", brand="oraimo", cap=
"""🎧 Wireless neckband with up to 30 hours playtime and ENC for clear calls

Oraimo Necklace Lite ENC Wireless Neckband (Official)
সারাদিন গান শোনার জন্য হালকা ও আরামদায়ক নেকব্যান্ড।

✔️ Up to 30 hours playtime
✔️ ENC noise cancellation in calls
✔️ Dual device connectivity
✔️ Call vibration alert

💰 Price: 1,300৳ (regular 1,485৳)

Neckband or earbuds, which do you prefer? Tell us 👇

"""),
 dict(slug="baby-care-kit", time="16:30", type="image", media=["posts/batch-2026-11-11/02_baby_care_kit.jpg"], cat="baby", brand=None, cap=
"""👶 10 piece baby care kit for newborn grooming, in Pink and Sky Blue

10 Pc Baby Care Kit
নবজাতকের যত্নের সব জিনিস এক বক্সে, বেবি কেয়ার কিট।

✔️ Nail care tools
✔️ Hair brush and comb
✔️ Thermometer
✔️ Nasal aspirator
✔️ Compact box, a lovely gift for new parents 🎁

💰 Price: 480৳ (regular 650৳)

"""),
 dict(slug="reel-awei-t88-budget-check", time="18:30", type="reel", media=["videos/2026-11-11/1830_awei-t88-budget-check.mp4"], cover_ms=3200, cat="earbuds", brand="awei", cap=
"""🎧 Wireless earbuds under 1,000৳ with ANC support and IPX6 water resistance

Awei T88 Wireless Earbuds, Black
১,০০০ টাকার নিচে ভালো ইয়ারবাড খুঁজছেন? দেখে নিন চেকলিস্ট!

✔️ ANC support
✔️ IPX6 water resistant
✔️ Bluetooth 5.4
✔️ Touch control

💰 Price: 990৳ (regular 1,450৳)

What matters most in earbuds for you? Comment below 👇

"""),
 dict(slug="insulated-lunch-box", time="20:00", type="image", media=["posts/batch-2026-11-11/03_insulated_lunch_box.jpg"], cat="lunchbox", brand=None, cap=
"""🍱 3 layer insulated lunch box, 2.6L, keeps meals hot or cold for up to 12 hours

Premium 3 Layer Stainless Steel Insulated Lunch Box
অফিসে বা স্কুলে ঘরের খাবার নিন এই লাঞ্চ বক্সে।

✔️ Keeps meals hot or cold for up to 12 hours
✔️ 2.6L large capacity
✔️ Food grade stainless steel interior
✔️ Leak proof design
✔️ Easy carry handle

💰 Price: 3,000৳ (regular 4,500৳)

"""),
 dict(slug="big-teddy-bear", time="21:30", type="image", media=["posts/batch-2026-11-11/04_big_teddy_bear.jpg"], cat="toys", brand=None, cap=
"""🧸 22 inch big teddy bear, super soft plush, a sweet gift for any occasion

22" Big Teddy Bear
প্রিয়জনকে উপহার দিন নরম তুলতুলে টেডি বিয়ার।

✔️ Super soft premium plush
✔️ 22 inch size
✔️ Perfect for cuddling and decorating
✔️ A lovely gift for any special occasion

Who would you gift this to? Tag them 👇

💰 Price: 1,150৳ (regular 2,000৳)

"""),
]
q = json.load(open("scheduler/queue.json")); ids = {e["id"] for e in q}; sets = []
for p in POSTS:
    pid = f"{D}-{p['slug']}"; assert pid not in ids, pid
    tags = pick(p["cat"], brand=p["brand"], seed=pid); sets.append(tuple(sorted(tags)))
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
