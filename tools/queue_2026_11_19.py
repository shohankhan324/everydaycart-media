"""Queue 19 Nov 2026 posts (5 images, NEW style set 14, + 1 Reel). Exactly 5 hashtags each, no dashes."""
import json, re, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from hashtags import pick, retag
CTA = "⚡ Limited stock available!\n🛒 Order now: everydaycart.online\n📩 Or inbox us to place your order"
D = "2026-11-19"
B = "posts/batch-2026-11-19/"
POSTS = [
 dict(slug="proove-intro-pro-led-case", time="11:30", type="image", media=[B + "01_proove_intro_pro.jpg"], cat="earbuds", brand="proove", cap=
"""🎧 Wireless earbuds with LED display charging case, Transparent ENC for clear calls and Bluetooth 5.4, 2,300৳

Proove Intro Pro (APP) Black TWS (Official)
চার্জ কত আছে দেখুন কেসের ডিসপ্লেতেই, স্টাইলিশ এই ইয়ারবাড।

✔️ 13mm driver, powerful sound
✔️ Transparent ENC for clear calls
✔️ Bluetooth 5.4, touch control
✔️ LED display charging case
✔️ Up to 6 hours playback

💰 Price: 2,300৳

Case display or app check: how do you track battery? 👇
"""),
 dict(slug="mumpot-kodomo-baby-picks", time="13:30", type="image", media=[B + "02_minitree_kodomo_baby_picks.jpg"], cat="baby", brand="minitree", cap=
"""🍼 Baby sippy mumpot, kids toothpaste and baby toothbrush: Minitree and Kodomo baby care picks from 200৳

Sip time and brush time sorted
বাচ্চার মাম্পট, টুথপেস্ট আর টুথব্রাশ এক জায়গায়।

1️⃣ Minitree Duckbill Mumpot 280 ml
✔️ Soft duckbill spout, two easy grip handles
✔️ For babies 3+ months
✔️ Pink or Sky Blue
💰 400৳ (regular 550৳)

2️⃣ Kodomo Baby Toothpaste
✔️ 1000 ppm fluoride + xylitol, sugar free
✔️ Orange cream flavour, for kids 0.5+ years
💰 280৳ (regular 400৳)

3️⃣ Kodomo Toothbrush
✔️ Soft, gentle bristles
✔️ For 0.5 to 3 years, child friendly handle
💰 200৳ (regular 400৳)

Which one is on your list first: 1, 2 or 3? 👇
"""),
 dict(slug="insulated-lunch-box-office", time="16:30", type="image", media=[B + "03_insulated_lunch_box.jpg"], cat="lunchbox", brand=None, cap=
"""🍱 Insulated lunch box 2.6L with 3 stainless steel layers, keeps meals hot or cold for up to 12 hours, 3,000৳

Premium 3 Layer Stainless Steel Insulated Lunch Box
শীতে অফিসে গরম ভাত খেতে চাইলে এই লাঞ্চ বক্স।

✔️ Keeps meals hot or cold for up to 12 hours
✔️ 2.6L large capacity
✔️ Food grade stainless steel interior
✔️ Leak proof design
✔️ Easy carry handle

💰 Price: 3,000৳ (regular 4,500৳)

What goes in your tiffin tomorrow: rice and curry or khichuri? 👇
"""),
 dict(slug="reel-earbuds-under-1000-spot-difference", time="18:30", type="reel", media=["videos/2026-11-19/1830_reel-earbuds-under-1000-spot-difference.mp4"], cover_ms=2300, cat="earbuds", brand="awei", cap=
"""🎧 Two wireless earbuds under 1,000৳ compared: Awei T108 vs Awei T88, spot the difference

Spot the difference: budget earbuds edition
১০০০ টাকার নিচে কোন ইয়ারবাড নেবেন? কমেন্টে লিখুন ১ না ২।

1️⃣ Awei T108 Wireless Earbuds (Official)
✔️ 13mm drivers for rich sound
✔️ ENC for clear calls
✔️ Up to 6 hours playback, 20 hours with the case
✔️ Bluetooth 5.3 with USB Type C charging
💰 950৳ (regular 1,199৳)

2️⃣ Awei T88 Wireless Earbuds, Black
✔️ ANC support
✔️ IPX6 water resistant
✔️ Bluetooth 5.4, touch control
💰 990৳ (regular 1,450৳)

Team 1 or Team 2? 👇
"""),
 dict(slug="oraimo-necklace-lite-neckband", time="20:00", type="image", media=[B + "04_oraimo_necklace_lite.jpg"], cat="neckband", brand="oraimo", cap=
"""🎧 Wireless neckband with up to 30 hours playtime, ENC for clear calls and dual device connectivity, 1,300৳

Oraimo Necklace Lite ENC Wireless Neckband (Official)
সারাদিন গান আর কলের জন্য হালকা ও আরামদায়ক নেকব্যান্ড।

✔️ Up to 30 hours playtime
✔️ ENC noise cancellation in calls
✔️ Dual device connectivity
✔️ Call vibration alert

💰 Price: 1,300৳ (regular 1,485৳)

Neckband or earbuds: which do you trust on a rickshaw ride? 👇
"""),
 dict(slug="forkan-trolley-luggage-winter-trip", time="21:30", type="image", media=[B + "05_forkan_trolley_luggage.jpg"], cat="travel", brand=None, cap=
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

Sajek, Sylhet or Cox's Bazar: where is your winter trip? 👇
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
