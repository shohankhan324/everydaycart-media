"""Queue 13 Nov 2026 posts (5 images, NEW style set 8, + 1 Reel). Exactly 5 hashtags each, no dashes."""
import json, re, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from hashtags import pick, retag
CTA = "⚡ Limited stock available!\n🛒 Order now: everydaycart.online\n📩 Or inbox us to place your order"
D = "2026-11-13"
B = "posts/batch-2026-11-13/"
POSTS = [
 dict(slug="oraimo-spacebuds-neo-plus", time="11:30", type="image", media=[B + "01_oraimo_spacebuds_neo_plus.jpg"], cat="earbuds", brand="oraimo", cap=
"""🎧 Wireless earbuds with Sound360 spatial audio, game mode and up to 30 hours battery

Oraimo SpaceBuds Neo+ (Official), Off-White
সারাদিন গান আর গেমের জন্য অফিসিয়াল ইয়ারবাড।

✔️ Sound360 spatial audio
✔️ Low latency game mode
✔️ 2 noise reducing mics for clear calls
✔️ Up to 30 hours battery life
✔️ Bluetooth 5.4, IPX4 water resistant

💰 Price: 1,940৳ (regular 2,189৳)

Music or gaming, what do you use earbuds for most? 👇
"""),
 dict(slug="bluetooth-speakers-duo", time="13:30", type="image", media=[B + "02_bluetooth_speakers.jpg"], cat="speaker", brand=None, extra="#BluetoothSpeaker", cap=
"""🔊 Portable Bluetooth speakers for home addas and weekend trips, from 1,841৳

Weekend plans? Bring the sound!
বাড়ির আড্ডা বা পিকনিকে সঙ্গী হোক ব্লুটুথ স্পিকার।

1️⃣ Oraimo SpaceBox Portable Bluetooth Speaker
✔️ 8W output, 45mm driver
✔️ Personalized light show, thumping bass
✔️ 1800mAh battery
💰 1,841৳ (regular 2,299৳)

2️⃣ Awei KA5 20W Portable Bluetooth Speaker
✔️ 10W x 2 output power
✔️ 2400mAh battery, 7.5 to 8 hours playback (at 70% volume)
✔️ IPX5 waterproof, Bluetooth 5.3
💰 2,525৳ (regular 2,849৳)

Team 1 or Team 2? Comment below 👇
"""),
 dict(slug="kodomo-lotion-powder", time="16:30", type="image", media=[B + "03_kodomo_lotion_powder.jpg"], cat="baby", brand="kodomo", cap=
"""🧴 Kodomo baby lotion powder 180 ml, extra mild and dust free, for babies 0+ months

Kodomo Baby Lotion Powder Extra Mild (180 ml)
শিশুর নরম ত্বকের যত্নে কোডোমো লোশন পাউডার।

✔️ Extra mild formula
✔️ Applies as lotion, dries to soft powder
✔️ Dust free, absorbs moisture
✔️ Helps prevent rash
✔️ Suitable from 0+ months

💰 Price: 720৳ (regular 880৳)
"""),
 dict(slug="reel-colmi-p81-call-on-wrist", time="18:30", type="reel", media=["videos/2026-11-13/1830_reel-colmi-p81-call-on-wrist.mp4"], cover_ms=5600, cat="smartwatch", brand="colmi", cap=
"""⌚ Calling smartwatch under 1,500৳: phone in the bag? Take the call on your wrist

COLMI P81 Calling Smartwatch
ফোন ব্যাগে থাকলেও কল ধরুন হাতের স্মার্ট ওয়াচ থেকে।

✔️ Bluetooth calling
✔️ 1.9 inch HD display
✔️ 100+ sports modes
✔️ IP68 waterproof
✔️ 300mAh battery

💰 Price: 1,350৳ (regular 1,540৳)

Has this ever happened to you? Tell us 👇
"""),
 dict(slug="have-good-time-tumbler", time="20:00", type="image", media=[B + "04_have_good_time_tumbler.jpg"], cat="tumbler", brand=None, cap=
"""☕ Insulated steel tumbler 750 ml with carry handle and secure lid, in Pink and White

Have Good Time Insulated Steel Thermal Tumbler
শীতের সকালে গরম চা কফির জন্য স্টাইলিশ টাম্বলার।

✔️ 750 ml capacity
✔️ Insulated stainless steel
✔️ Secure travel lid
✔️ Easy carry handle
✔️ For work, university and travel

💰 Price: 1,000৳ (regular 1,200৳)

Pink or White? Which one is yours? 🩷🤍
"""),
 dict(slug="portable-bbq-grill", time="21:30", type="image", media=[B + "05_portable_bbq_grill.jpg"], cat="bbq", brand=None, cap=
"""🔥 Portable BBQ grill machine with charcoal tray and air blower for winter rooftop BBQ

Portable BBQ Grill Machine
শীতের রাতে ছাদে বারবিকিউ পার্টির জন্য পোর্টেবল বারবিকিউ গ্রিল।

✔️ Durable steel body
✔️ Adjustable charcoal tray
✔️ Manual air blower for heat control
✔️ For picnics, camping and rooftop BBQ

💰 Price: 5,500৳ (regular 9,500৳)

Who is hosting the first BBQ night this winter? Tag your BBQ squad 👇
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
