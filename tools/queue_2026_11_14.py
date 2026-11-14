"""Queue 14 Nov 2026 posts (5 images, NEW style set 9, + 1 Reel). Exactly 5 hashtags each, no dashes."""
import json, re, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from hashtags import pick, retag
CTA = "⚡ Limited stock available!\n🛒 Order now: everydaycart.online\n📩 Or inbox us to place your order"
D = "2026-11-14"
B = "posts/batch-2026-11-14/"
POSTS = [
 dict(slug="proove-intro-pro", time="11:30", type="image", media=[B + "01_proove_intro_pro.jpg"], cat="earbuds", brand="proove", cap=
"""🎧 Wireless earbuds with an LED display charging case and ENC for clear calls, 2,300৳

Proove Intro Pro (APP) Black TWS (Official)
এলইডি ডিসপ্লে চার্জিং কেসসহ স্টাইলিশ ইয়ারবাড।

✔️ 13mm driver, powerful sound
✔️ Transparent ENC for clear calls
✔️ Bluetooth 5.4, touch control
✔️ LED display charging case
✔️ Up to 6 hours playback

💰 Price: 2,300৳

Would you check the battery on the case display every day? 👇
"""),
 dict(slug="minitree-bottle-mumpot", time="13:30", type="image", media=[B + "02_minitree_bottle_mumpot.jpg"], cat="babyfeed", brand="minitree", cap=
"""🍼 Baby feeding bottle and sippy mumpot with easy grip handles, from 400৳

Minitree picks for little hands
ছোট্ট হাতে ধরার মতো বেবি ফিডার আর মাম্পট।

1️⃣ Minitree 120 ml Baby Feeding Bottle
✔️ Training bottle for 6 months and up
✔️ Ergonomic handles, easy grip textured body
✔️ Protective nipple cover
💰 450৳ (regular 600৳)

2️⃣ Minitree Duckbill Mumpot 280 ml
✔️ Soft duckbill spout, two easy grip handles
✔️ For babies 3+ months
✔️ Pink or Sky Blue
💰 400৳ (regular 550৳)

Which one does your little one need first? 👇
"""),
 dict(slug="home-helpers-gloves-umbrella", time="16:30", type="image", media=[B + "03_home_helpers.jpg"], cat="home", brand=None, extra="#CleaningGloves", cap=
"""🧤 Cleaning gloves 200৳ and a full automatic folding umbrella 900৳: small helpers for every day

Small helpers, big difference
রোজকার কাজে গ্লাভস আর ছাতা, দুটোই হাতের কাছে রাখুন।

1️⃣ Premium Cleaning Gloves
✔️ Waterproof soft rubber
✔️ Long floral cuffs keep sleeves dry
✔️ Comfortable and reusable
💰 200৳ (regular 400৳)

2️⃣ Full Automatic Folding Umbrella
✔️ One press to open and close
✔️ Dual purpose for sun and rain
✔️ Compact folding size
💰 900৳ (regular 1,400৳)
"""),
 dict(slug="reel-elephant-bedtime-buddy", time="18:30", type="reel", media=["videos/2026-11-14/1830_reel-elephant-bedtime-buddy.mp4"], cover_ms=1900, cat="toys", brand=None, extra="#PlushToy", cap=
"""🐘 Elephant plush soft toy, 18 inch and super soft: meet the bedtime buddy

Elephant Plush Soft Toy
ঘুমের নতুন বন্ধু, নরম তুলতুলে হাতির সফট টয়।

✔️ 18 inch size
✔️ Super soft and huggable
✔️ A sweet gift for kids and loved ones

💰 Price: 750৳ (regular 1,100৳)

Who would you gift this to? Tag them 👇
"""),
 dict(slug="forkan-trolley-luggage", time="20:00", type="image", media=[B + "04_forkan_trolley_luggage.jpg"], cat="travel", brand=None, extra="#Suitcase", cap=
"""🧳 Hard shell trolley luggage with 360° spinner wheels, 20 and 24 inch, from 4,000৳

FORKAN Premium Hard Shell Trolley Luggage
শীতের ভ্রমণে মজবুত ট্রলি ব্যাগ, লাগেজ নিয়ে আর চিন্তা নেই।

✔️ Durable hard shell body
✔️ Smooth 360° spinner wheels
✔️ Spacious interior
✔️ Lightweight design
✔️ 20 inch and 24 inch sizes

💰 Price: from 4,000৳ (regular 5,500৳)
📩 Inbox us for available sizes and colours

Where is your next winter trip? Cox's Bazar, Sylhet or Sajek? 👇
"""),
 dict(slug="awei-t108", time="21:30", type="image", media=[B + "05_awei_t108.jpg"], cat="earbuds", brand="awei", cap=
"""🎧 Wireless earbuds under 1,000৳: Awei T108 with ENC and 20 hours with the case

Awei T108 Wireless Earbuds (Official)
কম দামে ভালো সাউন্ডের ইয়ারবাড খুঁজছেন? এটা দেখুন।

✔️ 13mm drivers for rich sound
✔️ ENC for clear calls
✔️ Up to 6 hours playback, 20 hours with the case
✔️ Bluetooth 5.3 with USB Type C charging

💰 Price: 950৳ (regular 1,199৳)
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
