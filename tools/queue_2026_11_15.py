"""Queue 15 Nov 2026 posts (5 images, NEW style set 10, + 1 Reel). Exactly 5 hashtags each, no dashes."""
import json, re, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from hashtags import pick, retag
CTA = "⚡ Limited stock available!\n🛒 Order now: everydaycart.online\n📩 Or inbox us to place your order"
D = "2026-11-15"
B = "posts/batch-2026-11-15/"
POSTS = [
 dict(slug="oraimo-necklace-lite", time="11:30", type="image", media=[B + "01_oraimo_necklace_lite.jpg"], cat="neckband", brand="oraimo", cap=
"""🎧 Wireless neckband with up to 30 hours playtime, ENC for clear calls and dual device connectivity, 1,300৳

Oraimo Necklace Lite ENC Wireless Neckband (Official)
সারাদিন গান শোনার জন্য হালকা ও আরামদায়ক নেকব্যান্ড।

✔️ Up to 30 hours playtime
✔️ ENC noise cancellation in calls
✔️ Dual device connectivity
✔️ Call vibration alert

💰 Price: 1,300৳ (regular 1,485৳)
"""),
 dict(slug="baby-toilet-seat", time="13:30", type="image", media=[B + "02_baby_toilet_seat.jpg"], cat="baby", brand=None, extra="#PottyTraining", cap=
"""🚽 Baby toilet seat reducer with soft cushion, handles and splash guard for potty training, 800৳

Soft Cushioned Baby Toilet Seat Reducer with Handles
পটি ট্রেনিং সহজ করতে বাচ্চার নরম টয়লেট সিট।

✔️ Soft cushioned seat
✔️ Secure handles
✔️ Splash guard
✔️ Waterproof, easy to clean
✔️ For 18 months and above

💰 Price: 800৳ (regular 1,000৳)

Has your little one started potty training yet? 👇
"""),
 dict(slug="insulated-lunch-box", time="16:30", type="image", media=[B + "03_insulated_lunch_box.jpg"], cat="lunchbox", brand=None, cap=
"""🍱 Insulated lunch box 2.6L, 3 layers, keeps meals hot or cold for up to 12 hours

Premium 3 Layer Stainless Steel Insulated Lunch Box
অফিস বা স্কুলে গরম খাবার নিতে মজবুত লাঞ্চ বক্স।

✔️ Keeps meals hot or cold for up to 12 hours
✔️ 2.6L large capacity
✔️ Food grade stainless steel interior
✔️ Leak proof design
✔️ Easy carry handle

💰 Price: 3,000৳ (regular 4,500৳)

Who packs lunch from home at your office? 👇
"""),
 dict(slug="reel-teddy-guess-price", time="18:30", type="reel", media=["videos/2026-11-15/1830_reel-teddy-guess-price.mp4"], cover_ms=2600, cat="toys", brand=None, cap=
"""🧸 22 inch big teddy bear, super soft premium plush: can you guess the price?

22" Big Teddy Bear
এই বড় টেডি বিয়ারের দাম কত হতে পারে? কমেন্টে বলুন!

✔️ 22 inch size
✔️ Super soft premium plush
✔️ Perfect for cuddling and decorating
✔️ A lovely gift for loved ones and kids

💰 Price: 1,150৳ (regular 2,000৳)

Did you guess A, B or C? 👇
"""),
 dict(slug="awei-t88", time="20:00", type="image", media=[B + "04_awei_t88.jpg"], cat="earbuds", brand="awei", cap=
"""🎧 Wireless earbuds under 1,000৳ with ANC support, IPX6 water resistance and Bluetooth 5.4

Awei T88 Wireless Earbuds, Black
কম দামে ভালো ইয়ারবাড খুঁজছেন? দাম মাত্র ৯৯০ টাকা।

✔️ ANC support
✔️ IPX6 water resistant
✔️ Bluetooth 5.4, touch control
✔️ 1 hour fast charging

💰 Price: 990৳ (regular 1,450৳)
"""),
 dict(slug="kodomo-oral-care", time="21:30", type="image", media=[B + "05_kodomo_oral_care.jpg"], cat="baby", brand="kodomo", cap=
"""🦷 Kids toothpaste and baby toothbrush from Kodomo, gentle on tiny teeth, from 200৳

Kodomo Baby Toothpaste + Kodomo Toothbrush
বাচ্চার টুথপেস্ট আর টুথব্রাশ, এক জায়গায়।

✔️ Toothpaste: 1000 ppm fluoride + xylitol, sugar free
✔️ Toothpaste: orange cream flavour, for kids 0.5+ years
✔️ Toothbrush: soft, gentle bristles
✔️ Toothbrush: for 0.5 to 3 years, child friendly handle

💰 Toothbrush: 200৳ (regular 400৳)
💰 Toothpaste: 280৳ (regular 400৳)
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
