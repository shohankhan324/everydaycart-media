"""Everyday Cart hashtag library.

Instagram caps captions at 5 hashtags (announced Dec 2025, posts and Reels); more than that hurts reach.
Facebook also does best with 3 to 5. So every caption gets exactly 5 searchable tags:

  1 BD shopping tag (rotated) + 1 BD category tag + 2 product/brand tags + 1 location tag (rotated)

Rotate so no two posts in a day share the identical set (repeated identical sets look like spam).
Skip generic tags (#reels, #explore, #love) and our own #EverydayCart (nobody searches it to discover us;
the brand is already in the caption text).

Usage:
    from hashtags import pick, retag
    tags = pick("earbuds", brand="oraimo", seed="2026-11-09-slug")
    caption = retag(caption, tags)
Review the library every 2 to 4 weeks: search each tag on Instagram and drop any that show
"recent posts hidden" or very few recent posts.
"""
import hashlib, re

SHOP = ["#OnlineShoppingBD", "#OnlineShopBD", "#OnlineStoreBD", "#BDShop", "#ShoppingBD"]
PLACE = ["#Dhaka", "#Bangladesh", "#DhakaShopping", "#Dhaka", "#Bangladesh"]

# category -> (BD category tags, product-type tags people search)
CAT = {
    "earbuds":    (["#GadgetBD", "#EarbudsBD", "#TechBD"], ["#WirelessEarbuds", "#Earbuds", "#TWS", "#TWSEarbuds"]),
    "smartwatch": (["#GadgetBD", "#SmartWatchBD", "#TechBD"], ["#SmartWatch", "#CallingSmartwatch", "#FitnessWatch"]),
    "speaker":    (["#GadgetBD", "#TechBD"], ["#BluetoothSpeaker", "#PortableSpeaker", "#Speaker"]),
    "neckband":   (["#GadgetBD", "#TechBD"], ["#Neckband", "#WirelessNeckband", "#BluetoothEarphones"]),
    "gadgets":    (["#GadgetBD", "#GadgetsBD", "#TechBD"], ["#Gadgets", "#TechGadgets", "#WirelessEarbuds", "#SmartWatch"]),
    "bottle":     (["#WinterEssentialsBD", "#KitchenBD"], ["#ThermalBottle", "#WaterBottle", "#InsulatedBottle", "#ThermosFlask"]),
    "tumbler":    (["#WinterEssentialsBD", "#KitchenBD"], ["#Tumbler", "#ThermalTumbler", "#CoffeeTumbler", "#ThermosCup"]),
    "baby":       (["#BabyProductsBD", "#BabyShopBD", "#MomAndBabyBD"], ["#BabyCare", "#BabyEssentials", "#NewbornEssentials", "#MomAndBaby"]),
    "babyfeed":   (["#BabyProductsBD", "#BabyShopBD"], ["#BabyBottle", "#BabyFeeding", "#FeedingBottle", "#BabyEssentials"]),
    "toys":       (["#ToysBD", "#GiftShopBD"], ["#SoftToys", "#TeddyBear", "#KidsGift", "#GiftIdeas"]),
    "gift":       (["#GiftShopBD", "#GiftBD"], ["#GiftIdeas", "#GiftForHer", "#GiftForHim", "#BirthdayGift"]),
    "home":       (["#HomeEssentialsBD", "#KitchenBD"], ["#HomeEssentials", "#KitchenEssentials", "#HomeGadgets", "#SmartHome"]),
    "kitchen":    (["#KitchenBD", "#HomeEssentialsBD"], ["#KitchenEssentials", "#HomeEssentials", "#Thermos", "#KitchenTools"]),
    "lunchbox":   (["#KitchenBD", "#HomeEssentialsBD"], ["#LunchBox", "#InsulatedLunchBox", "#TiffinBox", "#OfficeLunch"]),
    "travel":     (["#TravelBD", "#HomeEssentialsBD"], ["#TrolleyBag", "#Luggage", "#TravelEssentials"]),
    "fan":        (["#GadgetBD", "#SummerEssentialsBD"], ["#PortableFan", "#MiniFan", "#RechargeableFan"]),
    "clock":      (["#HomeEssentialsBD", "#HomeDecorBD"], ["#AlarmClock", "#HomeDecor", "#BedroomDecor", "#TableClock"]),
    "bbq":        (["#WinterEssentialsBD", "#HomeEssentialsBD"], ["#BBQGrill", "#BBQ", "#RooftopBBQ", "#Picnic"]),
    "massage":    (["#GadgetBD", "#HealthGadgetBD"], ["#MassageGun", "#Fitness", "#GymLife"]),
}

BRANDS = {"oraimo": "#Oraimo", "awei": "#Awei", "proove": "#Proove", "colmi": "#Colmi",
          "kodomo": "#Kodomo", "minitree": "#Minitree"}

# occasion tags replace the category tag pair (still 5 total)
OCCASION = {
    "1111": ["#1111Sale", "#ElevenEleven"],
    "blackfriday": ["#BlackFriday", "#BlackFridaySale"],
    "1212": ["#1212Sale", "#DoubleTwelve"],
    "armedforces": ["#ArmedForcesDay", "#SashastraBahiniDibosh", "#21November", "#Bangladesh", "#BangladeshArmedForces"],
    "victory": ["#VictoryDay", "#BijoyDibosh", "#16December", "#Bangladesh", "#JoyBangla"],
}


def _h(seed, n):
    return int(hashlib.md5(seed.encode()).hexdigest(), 16) % n


def pick(category, brand=None, seed="", occasion=None, extra=None):
    """Return exactly 5 hashtags. `extra` = one specific tag you want included (e.g. '#OraimoWatch5Lite')."""
    if occasion and category is None:
        return OCCASION[occasion][:5]
    cat_tags, prod_tags = CAT[category]
    out = [SHOP[_h(seed + "s", len(SHOP))]]
    if occasion:
        out += OCCASION[occasion][:2]
    else:
        out.append(cat_tags[_h(seed + "c", len(cat_tags))])
    prods = prod_tags[_h(seed + "p", len(prod_tags)):] + prod_tags[:_h(seed + "p", len(prod_tags))]
    specific = [t for t in [extra, BRANDS.get((brand or "").lower())] if t]
    for t in specific + prods:
        if len(out) >= 4: break
        if t not in out: out.append(t)
    out.append(PLACE[_h(seed + "l", len(PLACE))])
    assert len(out) == 5 and len(set(out)) == 5, out
    return out


def retag(caption, tags):
    """Replace the trailing hashtag line(s) of a caption with `tags`."""
    body = re.sub(r"(\n\s*(#\w+\s*)+)+\s*$", "", caption.rstrip())
    return body + "\n\n" + " ".join(tags)


if __name__ == "__main__":
    for c in CAT:
        print(c, pick(c, seed=c))
