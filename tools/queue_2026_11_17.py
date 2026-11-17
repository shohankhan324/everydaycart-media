"""Queue 17 Nov 2026 posts (5 images, NEW style set 12, + 1 Reel). Exactly 5 hashtags each, no dashes."""
import json, re, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from hashtags import pick, retag
CTA = "⚡ Limited stock available!\n🛒 Order now: everydaycart.online\n📩 Or inbox us to place your order"
D = "2026-11-17"
B = "posts/batch-2026-11-17/"
POSTS = [
 dict(slug="oraimo-spacebuds-lite", time="11:30", type="image", media=[B + "01_oraimo_spacebuds_lite.jpg"], cat="earbuds", brand="oraimo", cap=
"""🎧 Wireless earbuds with up to 40 hours playtime, AI call noise cancellation and Bluetooth 5.4, 1,310৳

Oraimo SpaceBuds Lite (Official)
কেসসহ ৪০ ঘণ্টা পর্যন্ত গান শুনুন এই ইয়ারবাডে।

✔️ Sound360 spatial audio
✔️ AI call noise cancellation
✔️ Up to 40 hours playtime with case
✔️ Bluetooth 5.4
✔️ IPX4 water resistant
✔️ 10 mm driver

💰 Price: 1,310৳ (regular 1,496৳)

Music, calls or both: what do you use earbuds for most? 👇
"""),
 dict(slug="wide-neck-baby-feeder", time="13:30", type="image", media=[B + "02_wide_neck_feeder.jpg"], cat="babyfeed", brand=None, cap=
"""🍼 Wide neck baby feeder, BPA free, with soft anti colic silicone nipple, 450৳

Wide Neck Baby Feeder
নরম নিপলের বেবি ফিডার, ভরা আর পরিষ্কার করা দুটোই সহজ।

✔️ Soft anti colic silicone nipple
✔️ BPA free, food grade PP
✔️ Wide neck for easy filling and cleaning

💰 Price: 450৳ (regular 700৳)

Tag a mom or dad who would like this 👇
"""),
 dict(slug="smart-led-temperature-bottle", time="16:30", type="image", media=[B + "03_smart_led_bottle.jpg"], cat="bottle", brand=None, cap=
"""🌡️ Smart thermal bottle with LED temperature display, 500 ml stainless steel, Black and White, 350৳

Smart LED Temperature Bottle (500 ml)
তাপমাত্রা দেখায় এমন স্মার্ট ফ্লাস্ক, শীতে গরম চা কফি সাথে রাখুন।

✔️ LED temperature display on the lid
✔️ Double wall insulation
✔️ 500 ml stainless steel
✔️ Slim and travel friendly
✔️ Colours: Black and White

💰 Price: 350৳ (regular 700৳)

Black or White? Comment your pick 👇
"""),
 dict(slug="reel-winter-flask-this-or-that", time="18:30", type="reel", media=["videos/2026-11-17/1830_reel-winter-flask-this-or-that.mp4"], cover_ms=1900, cat="tumbler", brand=None, cap=
"""☕ Thermos cup or thermal water bottle? Two winter flasks compared: 1000 ml vs 600 ml, from 800৳

This or that: winter flask edition
শীতে কোন ফ্লাস্কটা নেবেন? কমেন্টে লিখুন ১ না ২?

1️⃣ Big Mac 316 Stainless Steel Thermos Cup (Blue)
✔️ 1000 ml capacity
✔️ 316 stainless steel
✔️ Handle and straw
💰 1,000৳ (regular 1,300৳)

2️⃣ Premium Thermal Water Bottle
✔️ 600 ml capacity
✔️ Leak proof flip top lid
✔️ Built in straw and side handle
💰 800৳ (regular 1,250৳)

Team 1 or Team 2? 👇
"""),
 dict(slug="gadget-gift-duo", time="20:00", type="image", media=[B + "04_gadget_gift_duo.jpg"], cat="gadgets", brand=None, extra="#BluetoothSpeaker", cap=
"""🎁 Gadget gift ideas: COLMI P81 calling smartwatch 1,350৳ and Oraimo SpaceBox Bluetooth speaker 1,841৳

Gift a gadget they will use every day
প্রিয়জনের জন্য স্মার্ট ওয়াচ আর ব্লুটুথ স্পিকার।

⌚ COLMI P81 Calling Smartwatch
✔️ Bluetooth calling
✔️ 1.9 inch HD display
✔️ 100+ sports modes, IP68
💰 1,350৳ (regular 1,540৳)

🔊 Oraimo SpaceBox Portable Bluetooth Speaker
✔️ Personalized light show
✔️ Thumping bass, 8W output, 45 mm driver
✔️ 1800mAh battery
💰 1,841৳ (regular 2,299৳)

Which one would you gift? 👇
"""),
 dict(slug="kodomo-lotion-powder", time="21:30", type="image", media=[B + "05_kodomo_lotion_powder.jpg"], cat="baby", brand="kodomo", cap=
"""🧴 Baby lotion powder, extra mild and dust free, Kodomo 180 ml for babies 0+ months, 720৳

Kodomo Baby Lotion Powder Extra Mild (180 ml)
শিশুর নরম ত্বকের যত্নে কোডোমো লোশন পাউডার।

✔️ Extra mild formula
✔️ Applies as lotion, dries to soft powder
✔️ Dust free, absorbs moisture
✔️ Helps prevent rash
✔️ Suitable from 0+ months

💰 Price: 720৳ (regular 880৳)

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
