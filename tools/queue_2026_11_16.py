"""Queue 16 Nov 2026 posts (5 images, NEW style set 11, + 1 Reel). Exactly 5 hashtags each, no dashes."""
import json, re, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from hashtags import pick, retag
CTA = "⚡ Limited stock available!\n🛒 Order now: everydaycart.online\n📩 Or inbox us to place your order"
D = "2026-11-16"
B = "posts/batch-2026-11-16/"
POSTS = [
 dict(slug="oraimo-watch-5-lite", time="11:30", type="image", media=[B + "01_oraimo_watch_5_lite.jpg"], cat="smartwatch", brand="oraimo", cap=
"""⌚ Calling smart watch with 2.01" HD display, IP68 and 105+ sports modes, 1,650৳

Oraimo Watch 5 Lite Smart Watch (Official)
কল ধরুন সরাসরি হাতের স্মার্ট ওয়াচ থেকেই।

✔️ 2.01" HD display
✔️ HD voice in calls
✔️ AI generated watch faces
✔️ IP68 dust and water resistance
✔️ 105+ sports modes
✔️ Up to 7 days battery life

💰 Price: 1,650৳ (regular 1,870৳)

Calls on your wrist or phone in hand? Tell us 👇
"""),
 dict(slug="baby-care-kit", time="13:30", type="image", media=[B + "02_baby_care_kit.jpg"], cat="baby", brand=None, extra="#NewbornEssentials", cap=
"""👶 10 piece baby care kit for newborn grooming: nail care, hair brush, comb and thermometer, 480৳

10 Pc Baby Care Kit (Pink and Sky Blue)
নবজাতকের যত্নের দরকারি সব জিনিস এক বক্সে, বেবি কেয়ার কিট।

✔️ Nail care tools
✔️ Hair brush and comb
✔️ Thermometer
✔️ Nasal aspirator
✔️ Compact box, a lovely gift for new parents 🎁

💰 Price: 480৳ (regular 650৳)

Tag a new mom or dad who needs this 👇
"""),
 dict(slug="winter-flask-duo", time="16:30", type="image", media=[B + "03_winter_flask_duo.jpg"], cat="bottle", brand=None, cap=
"""☕ Thermal bottle and thermal tumbler for winter tea and coffee, 800৳ each

Hot tea on the go? Pick your flask!
শীতে গরম চা কফি সাথে রাখতে পছন্দের ফ্লাস্ক বেছে নিন।

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

Team 1 or Team 2? Comment below 👇
"""),
 dict(slug="reel-massage-gun-long-day", time="18:30", type="reel", media=["videos/2026-11-16/1830_reel-massage-gun-long-day.mp4"], cover_ms=4000, cat="massage", brand=None, cap=
"""💆 Portable massage gun with 4 massage heads, rechargeable, for after office and gym, 850৳

Portable Rechargeable Massage Gun
সারাদিন অফিসের পর ক্লান্ত? ঘরে বসেই ম্যাসাজ গান দিয়ে আরাম নিন।

✔️ 4 interchangeable massage heads
✔️ Powerful yet quiet motor
✔️ Lightweight, ergonomic design
✔️ Rechargeable and portable

💰 Price: 850৳ (regular 1,200৳)

Gym, office or home: where would you use it? 👇
"""),
 dict(slug="steel-water-pot", time="20:00", type="image", media=[B + "04_steel_water_pot.jpg"], cat="kitchen", brand=None, cap=
"""🫖 Insulated stainless steel water pot for tea, coffee, milk and water, 1,000৳

Stainless Steel Water Pot
চা, কফি আর পানি রাখার জন্য ইনসুলেটেড স্টিলের জগ।

✔️ Double wall insulated interior
✔️ Leak-proof lid
✔️ Ergonomic handle
✔️ Modern matte finish
✔️ For home, office or gatherings

💰 Price: 1,000৳ (regular 1,400৳)

Evening tea or coffee at your home? Tell us 👇
"""),
 dict(slug="silent-alarm-clock", time="21:30", type="image", media=[B + "05_silent_alarm_clock.jpg"], cat="clock", brand=None, cap=
"""⏰ Silent alarm clock with no ticking sound and twin bell design, 500৳

Silent Alarm Clock
টিকটিক শব্দ ছাড়া অ্যালার্ম ঘড়ি, রাতে শান্তির ঘুম।

✔️ Non ticking, silent operation
✔️ Precise quartz movement
✔️ Classic twin bell design
✔️ Elegant bedside decor

💰 Price: 500৳ (regular 800৳)

Alarm set for tomorrow? Good night from Everyday Cart 🌙
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
