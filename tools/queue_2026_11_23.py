"""Queue 23 Nov 2026 posts (5 images, NEW style set 18, + 1 Reel). Exactly 5 hashtags each, no dashes."""
import json, re, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from hashtags import pick, retag
CTA = "⚡ Limited stock available!\n🛒 Order now: everydaycart.online\n📩 Or inbox us to place your order"
D = "2026-11-23"
B = "posts/batch-2026-11-23/"
POSTS = [
 dict(slug="oraimo-necklace-lite-30-hours-neckband", time="11:30", type="image", media=[B + "01_oraimo_necklace_lite.jpg"], cat="neckband", brand="oraimo", cap=
"""🎧 Wireless neckband with up to 30 hours playtime, ENC for clear calls and dual device connectivity, 1,300৳

Oraimo Necklace Lite ENC Wireless Neckband (Official)
সারাদিন গান আর কলের জন্য হালকা নেকব্যান্ড।

✔️ Up to 30 hours playtime
✔️ ENC noise cancellation in calls
✔️ Dual device connectivity
✔️ Call vibration alert

💰 Price: 1,300৳ (regular 1,485৳)

Office call, gym or bus ride: where would you wear it most? 👇
"""),
 dict(slug="kodomo-baby-care-trio-lotion-toothpaste-brush", time="13:30", type="image", media=[B + "02_kodomo_baby_care_trio.jpg"], cat="baby", brand="kodomo", cap=
"""🧴 Baby lotion powder, kids toothpaste and baby toothbrush from Kodomo: gentle everyday baby care from 200৳

Bath time to brush time, Kodomo has it
বাচ্চার যত্নে কোডোমো বেবি লোশন পাউডার, টুথপেস্ট আর টুথব্রাশ।

1️⃣ Kodomo Baby Lotion Powder, Extra Mild 180 ml
✔️ Goes on as lotion, dries to soft powder
✔️ Dust free, absorbs moisture, from 0+ months
💰 720৳ (regular 880৳)

2️⃣ Kodomo Baby Toothpaste
✔️ 1000 ppm fluoride + xylitol, sugar free
✔️ Orange cream flavour, for kids 0.5+ years
💰 280৳ (regular 400৳)

3️⃣ Kodomo Toothbrush
✔️ Soft, gentle bristles
✔️ For 0.5 to 3 years, child friendly handle
💰 200৳ (regular 400৳)

Which one is on your list: 1, 2 or 3? 👇
"""),
 dict(slug="insulated-lunch-box-cold-office-warm-lunch", time="16:30", type="image", media=[B + "03_insulated_lunch_box.jpg"], cat="lunchbox", brand=None, cap=
"""🍱 Insulated lunch box 2.6L with 3 stainless steel layers, keeps meals hot or cold for up to 12 hours, 3,000৳

Premium 3 Layer Stainless Steel Insulated Lunch Box
শীতে অফিসে গরম খাবারের জন্য লাঞ্চ বক্স।

✔️ Keeps meals hot or cold for up to 12 hours
✔️ 2.6L large capacity
✔️ Food grade stainless steel interior
✔️ Leak proof design
✔️ Easy carry handle

💰 Price: 3,000৳ (regular 4,500৳)

Winter office lunch: bhuna khichuri or rice and curry? 👇
"""),
 dict(slug="reel-proove-intro-pro-traffic-clear-calls", time="18:30", type="reel", media=["videos/2026-11-23/1830_reel-proove-intro-pro-traffic-clear-calls.mp4"],
      cover_ms=2100, cat="earbuds", brand="proove", cap=
"""🎧 Wireless earbuds with Transparent ENC for clear calls and an LED display charging case, 2,300৳

Stuck in Dhaka traffic? Keep the music on and calls clear
জ্যামে বসেও পরিষ্কার কল, স্টাইলিশ এই ইয়ারবাডে।

Proove Intro Pro (APP) Black TWS (Official)
✔️ 13mm driver, powerful sound
✔️ Transparent ENC for clear calls
✔️ Bluetooth 5.4, touch control
✔️ LED display charging case
✔️ Up to 6 hours playback

💰 Price: 2,300৳

In a jam: music or podcast? 👇
"""),
 dict(slug="minitree-duckbill-mumpot-first-sips", time="20:00", type="image", media=[B + "05_minitree_mumpot.jpg"], cat="babyfeed", brand="minitree", cap=
"""🍼 Baby sippy cup with soft duckbill spout and two easy grip handles, Minitree Mumpot 280 ml, 400৳

Minitree Duckbill Mumpot 280 ml, Pink or Sky Blue
ছোট্ট সোনার প্রথম সিপি কাপ মাম্পট।

✔️ Soft duckbill spout
✔️ Two easy grip handles
✔️ For babies 3+ months
✔️ Pink or Sky Blue

💰 Price: 400৳ (regular 550৳)

Pink or Sky Blue for your little one? 👇
"""),
 dict(slug="forkan-trolley-luggage-weekend-trip", time="21:30", type="image", media=[B + "06_forkan_trolley_luggage.jpg"], cat="travel", brand=None, cap=
"""🧳 Hard shell trolley luggage with smooth 360° spinner wheels, 20 and 24 inch sizes, from 4,000৳

FORKAN Premium Hard Shell Trolley Luggage
শীতের ট্যুরে মজবুত ট্রলি ব্যাগ সাথে নিন।

✔️ Durable hard shell body
✔️ Smooth 360° spinner wheels
✔️ Spacious interior
✔️ Lightweight design
✔️ 20 inch and 24 inch sizes

💰 Price: from 4,000৳ (regular 5,500৳)
📩 Inbox us for available sizes and colours

Who are you taking on your next winter trip? Tag them 👇
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
