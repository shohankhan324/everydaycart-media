"""Queue 10 Nov 2026 posts (4 images, style set 5, + 1 Reel). Exactly 5 hashtags each, no dashes."""
import json, re, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from hashtags import pick, retag
CTA = "⚡ Limited stock available!\n🛒 Order now: everydaycart.online\n📩 Or inbox us to place your order"
D = "2026-11-10"
POSTS = [
 dict(slug="awei-t108", time="13:30", type="image", media=["posts/batch-2026-11-10/01_awei_t108.jpg"], cat="earbuds", brand="awei", cap=
"""🎧 Wireless earbuds under 1,000৳ with ENC for clear calls

Awei T108 Wireless Earbuds (Official)
কম দামে ভালো সাউন্ডের ইয়ারবাড খুঁজছেন? এটা আপনার জন্য!

✔️ 13mm drivers for rich sound
✔️ ENC for clear calls
✔️ Up to 6 hours playback, 20 hours with the case
✔️ Bluetooth 5.3 with USB Type C charging

💰 Price: 950৳ (regular 1,199৳)

"""),
 dict(slug="kodomo-oral-care", time="16:30", type="image", media=["posts/batch-2026-11-10/02_kodomo_oral_care.jpg"], cat="baby", brand="kodomo", cap=
"""🦷 Kids toothpaste and baby toothbrush from Kodomo, gentle on tiny teeth

Kodomo Baby Toothpaste + Kodomo Toothbrush
বাচ্চার প্রথম টুথপেস্ট আর টুথব্রাশ, এক জায়গায়।

✔️ Toothpaste: 1000 ppm fluoride + xylitol, sugar free
✔️ Toothpaste: orange cream flavour, for kids 0.5+ years
✔️ Toothbrush: soft, gentle bristles
✔️ Toothbrush: for 0.5 to 3 years, child friendly handle

💰 Toothpaste: 280৳ (regular 400৳)
💰 Toothbrush: 200৳ (regular 400৳)

Is your little one brushing yet? Tell us in the comments 👇

"""),
 dict(slug="reel-proove-guess-price", time="18:30", type="reel", media=["videos/2026-11-10/1830_proove-guess-price.mp4"], cover_ms=2500, cat="earbuds", brand="proove", cap=
"""🎧 Guess the price of these TWS earbuds with an LED display case! Watch till the end 👀

Proove Intro Pro (APP) Black TWS (Official)
এই ইয়ারবাডের দাম কত হতে পারে? কমেন্টে আপনার উত্তর দিন!

✔️ 13mm driver, powerful sound
✔️ Transparent ENC for clear calls
✔️ Bluetooth 5.4, touch control
✔️ LED display charging case
✔️ Up to 6 hours playback

💰 Price: 2,300৳

💬 Comment your guess before the reveal!

"""),
 dict(slug="316-thermal-bottle", time="20:00", type="image", media=["posts/batch-2026-11-10/03_316_thermal_bottle.jpg"], cat="bottle", brand=None, cap=
"""☕ 700 ml stainless steel thermal bottle with a safety lock lid

316 Stainless Steel Thermal Bottle
শীতে সাথে রাখুন নিজের থার্মাল ফ্লাস্ক বোতল।

✔️ 316 stainless steel
✔️ 700 ml water capacity
✔️ Safety lock lid
✔️ Easy carry handle

💰 Price: 800৳ (regular 1,100৳)

"""),
 dict(slug="steel-water-pot", time="21:30", type="image", media=["posts/batch-2026-11-10/04_steel_water_pot.jpg"], cat="kitchen", brand=None, cap=
"""🫖 Insulated stainless steel water pot for tea, coffee, milk and water

Stainless Steel Water Pot
চা, কফি বা পানি রাখার জন্য সুন্দর স্টিলের জগ।

✔️ Double wall insulated interior
✔️ Leak-proof lid
✔️ Ergonomic handle
✔️ Modern matte finish
✔️ For home, office or gatherings

💰 Price: 1,000৳ (regular 1,400৳)

Tea or coffee, what goes in yours? Tell us 👇

"""),
]
q = json.load(open("scheduler/queue.json")); ids = {e["id"] for e in q}; sets = []
for p in POSTS:
    pid = f"{D}-{p['slug']}"; assert pid not in ids, pid
    tags = pick(p["cat"], brand=p["brand"], seed=pid); sets.append(tuple(sorted(tags)))
    cap = retag(p["cap"].rstrip() + "\n\n" + CTA, tags)
    assert len(re.findall(r"#\w+", cap)) == 5, cap
    assert "—" not in cap and "–" not in cap and "#EverydayCart" not in cap
    for m in p["media"]: assert os.path.exists(m), m
    e = {"id": pid, "time": f"{D}T{p['time']}:00+06:00", "type": p["type"], "media": p["media"], "caption": cap, "networks": ["facebook", "instagram"]}
    if "cover_ms" in p: e["cover_ms"] = p["cover_ms"]
    q.append(e); print(pid, tags)
assert len(set(sets)) == len(sets)
q.sort(key=lambda e: e["time"])
json.dump(q, open("scheduler/queue.json", "w"), ensure_ascii=False, indent=2)
