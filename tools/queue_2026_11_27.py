"""Queue 27 Nov 2026 posts (5 images, NEW style set 22, + 1 Reel). Exactly 5 hashtags each, no dashes."""
import json, re, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from hashtags import pick, retag
CTA = "⚡ Limited stock available!\n🛒 Order now: everydaycart.online\n📩 Or inbox us to place your order"
D = "2026-11-27"
B = "posts/batch-2026-11-27/"
POSTS = [
 dict(slug="oraimo-spacebuds-neo-plus-game-mode-music", time="11:30", type="image", media=[B + "01_oraimo_spacebuds_neo_plus.jpg"], cat="earbuds", brand="oraimo", cap=
"""🎧 Wireless earbuds with low latency game mode, Sound360 spatial audio and up to 30 hours battery: Oraimo SpaceBuds Neo+, 1,940৳

Oraimo SpaceBuds Neo+ (Official)
গেম আর গান দুটোর জন্যই অফিসিয়াল ওরাইমো ইয়ারবাড।

✔️ Low latency game mode
✔️ Sound360 spatial audio
✔️ 2 noise reducing mics for clear calls
✔️ Up to 30 hours battery life
✔️ Bluetooth 5.4, IPX4 water resistant

💰 Price: 1,940৳ (regular 2,189৳)

Which game are you playing tonight? 🎮👇
"""),
 dict(slug="kodomo-baby-care-lotion-powder-toothpaste-brush", time="13:30", type="image", media=[B + "02_kodomo_baby_care_trio.jpg"], cat="baby", brand="kodomo", cap=
"""🧴 Kodomo baby lotion powder, kids toothpaste and baby toothbrush: gentle everyday baby care from 200৳

Gentle care for little ones
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

Tag a mom or dad who needs these 💕👇
"""),
 dict(slug="winter-tumblers-have-good-time-premium-860ml", time="16:30", type="image", media=[B + "03_winter_tumbler_duo.jpg"], cat="tumbler", brand=None, cap=
"""☕ Insulated winter tumblers for hot tea and coffee: Have a Good Time 750 ml (1,000৳) and Premium Thermal Tumbler 860 ml with straw (800৳)

Your winter sip, two ways
শীতে গরম চা কফির জন্য পছন্দের টাম্বলার বেছে নিন।

1️⃣ Have a Good Time Insulated Steel Thermal Tumbler
✔️ 750 ml capacity
✔️ Insulated stainless steel
✔️ Secure travel lid and carry handle
💰 1,000৳ (regular 1,200৳)

2️⃣ Premium Thermal Tumbler
✔️ 860 ml capacity
✔️ Double wall vacuum insulation
✔️ Reusable straw, leak resistant lid, side handle
💰 800৳ (regular 1,200৳)

750 ml or 860 ml: which one is yours? Comment 1 or 2 👇
"""),
 dict(slug="reel-oraimo-necklace-lite-all-day-battery", time="18:30", type="reel", media=["videos/2026-11-27/1830_reel-oraimo-necklace-lite-all-day-battery.mp4"], cat="neckband", brand="oraimo", cover_ms=4100, cap=
"""🎧 Wireless neckband with up to 30 hours playtime, ENC for clear calls and dual device connectivity: Oraimo Necklace Lite, 1,300৳

Oraimo Necklace Lite ENC Wireless Neckband (Official)
সারাদিন গান আর কলের জন্য হালকা নেকব্যান্ড।

✔️ Up to 30 hours playtime
✔️ ENC noise cancellation in calls
✔️ Dual device connectivity
✔️ Call vibration alert

💰 Price: 1,300৳ (regular 1,485৳)

Morning music, office calls or evening ride: where would you wear it most? 👇
"""),
 dict(slug="insulated-lunch-box-hot-office-lunch", time="20:00", type="image", media=[B + "04_insulated_lunch_box.jpg"], cat="lunchbox", brand=None, cap=
"""🍱 Insulated lunch box 2.6L with stainless steel layers, keeps meals hot or cold for up to 12 hours, 3,000৳

Premium 3 Layer Stainless Steel Insulated Lunch Box
শীতে অফিসে গরম খাবারের জন্য লাঞ্চ বক্স।

✔️ Keeps meals hot or cold for up to 12 hours
✔️ 2.6L large capacity
✔️ Food grade stainless steel interior
✔️ Leak proof design
✔️ Easy carry handle

💰 Price: 3,000৳ (regular 4,500৳)

What is in your lunch box tomorrow? 🍛👇
"""),
 dict(slug="forkan-trolley-luggage-pack-light-winter-trip", time="21:30", type="image", media=[B + "05_forkan_trolley_luggage.jpg"], cat="travel", brand=None, cap=
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

Weekend trip or a long holiday: which size do you need? 👇
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
