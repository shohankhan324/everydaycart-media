"""Queue 21 Nov 2026 posts (5 images, NEW style set 16, + 1 Reel). Exactly 5 hashtags each, no dashes."""
import json, re, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from hashtags import pick, retag
CTA = "⚡ Limited stock available!\n🛒 Order now: everydaycart.online\n📩 Or inbox us to place your order"
D = "2026-11-21"
B = "posts/batch-2026-11-21/"
POSTS = [
 dict(slug="colmi-p81-calling-smartwatch", time="11:30", type="image", media=[B + "01_colmi_p81_watch.jpg"], cat="smartwatch", brand="colmi", extra="#CallingSmartwatch", cap=
"""⌚ Calling smart watch under 1,500৳ with 1.9 inch HD display, 100+ sports modes and IP68, 1,350৳

COLMI P81 Calling Smartwatch
হাতের স্মার্ট ওয়াচেই কল ধরুন আর ফিটনেস ট্র্যাক করুন।

✔️ 1.9 inch HD display
✔️ Bluetooth calling
✔️ 100+ sports modes
✔️ IP68 water resistance
✔️ 300mAh battery

💰 Price: 1,350৳ (regular 1,540৳)

Walking, cricket or gym: which sports mode would you use most? 👇
"""),
 dict(slug="baby-care-kit-newborn", time="13:30", type="image", media=[B + "02_baby_care_kit.jpg"], cat="baby", brand=None, cap=
"""👶 10 piece baby care kit for newborns: nail care tools, hair brush, comb, thermometer and nasal aspirator, 480৳

10 Pc Baby Care Kit (Pink and Sky Blue)
নবজাতকের যত্নে দরকারি সব এক বক্সে, বেবি কেয়ার কিট।

✔️ Nail care tools
✔️ Hair brush and comb
✔️ Thermometer
✔️ Nasal aspirator
✔️ Compact box, a lovely gift for new parents 🎁

💰 Price: 480৳ (regular 650৳)

Pink or Sky Blue: which one would you pick? 👇
"""),
 dict(slug="winter-flasks-thermal-and-led-bottle", time="16:30", type="image", media=[B + "03_winter_bottles.jpg"], cat="bottle", brand=None, cap=
"""☕ Thermal water bottle 600 ml 800৳ and smart LED temperature bottle 500 ml 350৳ for hot winter tea and coffee

Hot tea on the go? Pick your flask
শীতে গরম চা কফি সাথে রাখতে পছন্দের ফ্লাস্ক বেছে নিন।

1️⃣ Premium Thermal Water Bottle, 600 ml
✔️ Leak proof flip top lid
✔️ Built in straw
✔️ Comfortable side handle
💰 800৳ (regular 1,250৳)

2️⃣ Smart LED Temperature Bottle, 500 ml
✔️ LED temperature display on the lid
✔️ Double wall insulation, stainless steel
✔️ Black and White
💰 350৳ (regular 700৳)

Straw sipper or slim smart flask? Comment 1 or 2 👇
"""),
 dict(slug="reel-oraimo-spacebox-lights-off-music-on", time="18:30", type="reel", media=["videos/2026-11-21/1830_reel-oraimo-spacebox-lights-off-music-on.mp4"], cover_ms=2000, cat="speaker", brand="oraimo", extra="#BluetoothSpeaker", cap=
"""🔊 Portable Bluetooth speaker with a personalized light show and thumping bass: lights off, music on! 1,841৳

Oraimo SpaceBox Portable Bluetooth Speaker (Official)
আড্ডা, পিকনিক বা রুমে পার্টি, আলো জ্বলে গানের তালে এই ব্লুটুথ স্পিকারে।

✔️ Personalized light show
✔️ Thumping bass
✔️ 8W audio output, 45mm driver
✔️ 1800mAh battery

💰 Price: 1,841৳ (regular 2,299৳)

What is the first song you would play on it? 👇
"""),
 dict(slug="auto-folding-umbrella-sun-rain", time="20:00", type="image", media=[B + "04_auto_umbrella.jpg"], cat="umbrella", brand=None, cap=
"""☂️ Full automatic folding umbrella for sun and rain: one press to open and close, compact size, 900৳

Full Automatic Folding Umbrella
রোদ বা বৃষ্টিতে ব্যাগে রাখুন অটো ছাতা, এক চাপেই খোলে।

✔️ One press to open and close
✔️ Dual purpose for sun and rain
✔️ Strong frame
✔️ Compact folding size

💰 Price: 900৳ (regular 1,400৳)

Do you keep an umbrella in your bag every day? 👇
"""),
 dict(slug="oraimo-spacebuds-lite-40-hours", time="21:30", type="image", media=[B + "05_oraimo_spacebuds_lite.jpg"], cat="earbuds", brand="oraimo", cap=
"""🎧 Wireless earbuds with up to 40 hours playtime, Sound360 spatial audio and AI call noise cancellation, 1,310৳

Oraimo SpaceBuds Lite (Official)
কেসসহ ৪০ ঘণ্টা পর্যন্ত গান শুনুন এই ইয়ারবাডে।

✔️ Sound360 spatial audio
✔️ AI call noise cancellation
✔️ Up to 40 hours playtime with case
✔️ Bluetooth 5.4
✔️ IPX4 water resistant
✔️ 10 mm driver

💰 Price: 1,310৳ (regular 1,496৳)

What is on your late night playlist? 👇
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
