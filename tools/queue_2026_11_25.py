"""Queue 25 Nov 2026 posts (4 images, NEW style set 20, + 1 Reel). Exactly 5 hashtags each, no dashes."""
import json, re, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from hashtags import pick, retag
CTA = "⚡ Limited stock available!\n🛒 Order now: everydaycart.online\n📩 Or inbox us to place your order"
D = "2026-11-25"
B = "posts/batch-2026-11-25/"
POSTS = [
 dict(slug="awei-t108-enc-earbuds-clear-calls", time="11:30", type="image", media=[B + "01_awei_t108_earbuds.jpg"], cat="earbuds", brand="awei", cap=
"""🎧 ENC wireless earbuds for clear calls with 13mm drivers and 20 hours with the case, 950৳

Awei T108 Wireless Earbuds (Official), Black
কল হবে ক্লিয়ার, কম দামে ভালো ইয়ারবাড এটাই।

✔️ ENC for clear calls
✔️ 13mm drivers for rich sound
✔️ Up to 6 hours playback, 20 hours with the case
✔️ Bluetooth 5.3 with USB Type C charging

💰 Price: 950৳ (regular 1,199৳)

Office calls or music on the go: what do you need earbuds for? 👇
"""),
 dict(slug="baby-care-kit-newborn-all-in-one-box", time="13:30", type="image", media=[B + "02_baby_care_kit.jpg"], cat="baby", brand=None, cap=
"""👶 10 piece baby care kit for newborns with nail care tools, hair brush, comb, thermometer and nasal aspirator, 480৳

10 Pc Baby Care Kit (Pink and Sky Blue)
নবজাতকের যত্নে দরকারি সব এক বক্সে, বেবি কেয়ার কিট।

✔️ Nail care tools
✔️ Hair brush and comb
✔️ Thermometer
✔️ Nasal aspirator
✔️ Compact box, a lovely gift for new parents 🎁

💰 Price: 480৳ (regular 650৳)

Tag a new mom or dad who would love this 💕
"""),
 dict(slug="winter-tea-steel-water-pot-led-bottle", time="16:30", type="image", media=[B + "03_winter_tea_pot_bottle.jpg"], cat="kitchen", brand=None, extra="#ThermalBottle", cap=
"""☕ Insulated stainless steel water pot 1,000৳ and smart LED temperature bottle 500 ml 350৳ for winter tea

Tea at home, tea on the go
শীতে গরম চায়ের জন্য স্টিলের জগ আর ফ্লাস্ক, দুটোই কাজের।

1️⃣ Stainless Steel Water Pot
✔️ Double wall insulated interior
✔️ Leak proof lid
✔️ Ergonomic handle, modern matte finish
💰 1,000৳ (regular 1,400৳)

2️⃣ Smart LED Temperature Bottle, 500 ml
✔️ LED temperature display on the lid
✔️ Double wall insulation, stainless steel
✔️ Black and White
💰 350৳ (regular 700৳)

Tea at home or tea on the go? Comment 1 or 2 👇
"""),
 dict(slug="reel-colmi-p81-winter-morning-walk", time="18:30", type="reel", media=["videos/2026-11-25/1830_reel-colmi-p81-winter-morning-walk.mp4"],
      cover_ms=3600, cat="smartwatch", brand="colmi", cap=
"""⌚ Calling smart watch for winter morning walks: 1.9 inch HD display, Bluetooth calling, 100+ sports modes and IP68, 1,350৳

Phone in the pocket, calls on the wrist
শীতের সকালে হাঁটতে যান? কলিং স্মার্ট ওয়াচেই কল ধরুন।

COLMI P81 Calling Smartwatch
✔️ 1.9 inch HD display
✔️ Bluetooth calling
✔️ 100+ sports modes
✔️ IP68 water resistance
✔️ 300mAh battery

💰 Price: 1,350৳ (regular 1,540৳)

Which sport would you wear it for? Comment below 👇
"""),
 dict(slug="oraimo-spacebox-speaker-winter-night-adda", time="20:00", type="image", media=[B + "04_oraimo_spacebox_speaker.jpg"], cat="speaker", brand="oraimo", cap=
"""🔊 Portable Bluetooth speaker with a personalized light show and thumping bass for winter night adda, 1,841৳

Oraimo SpaceBox Portable Bluetooth Speaker (Official)
আড্ডা জমাতে লাইট শো সহ ব্লুটুথ স্পিকার।

✔️ Personalized light show
✔️ Thumping bass
✔️ 8W audio output, 45mm driver
✔️ 1800mAh battery

💰 Price: 1,841৳ (regular 2,299৳)

Rooftop adda or room party: where would you play it first? 👇
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
