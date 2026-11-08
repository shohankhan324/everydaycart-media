# Everyday Cart daily posting runbook

The owner (Engr Md Shohan Khan) wants Everyday Cart's Facebook Page and Instagram (@everydaycart.bd) to get
**4 to 5 high-quality image posts plus 1 Reel every day** (reduced from 8 to 10 on 8 Nov 2026 because too many posts a day
were splitting reach; fewer, more attractive posts reach more people), prepared and scheduled
automatically without waiting for his approval. Posts publish themselves through `scheduler/` (GitHub Actions + Meta
Graph API): adding entries to `scheduler/queue.json` and pushing to `main` is all that is needed.

## Hard rules (from the owner)

- **Flat designs only**, no 3D. Top-notch, clean finishing: look at every rendered image close up before queueing.
- **Logo on every post and Reel**, small, in a corner (the toolkit templates already do this).
- **A different design every day**: never reuse the previous day's style set (see `posts/style_log.json`).
- **Only in-stock products** (`is_in_stock` true in `products/products.json`), and only colours that are in stock.
- **Prices exactly as on the store.** Run the `sync-products.yml` workflow first (`gh workflow run sync-products.yml`,
  wait for it, `git pull`). Show a regular (struck) price only when it is known from earlier captions or the store.
- **Captions**: hook line with an emoji, product name, ✔️ feature lines, `💰 Price: X৳ (regular Y৳)`, then exactly
  `⚡ Limited stock available!\n🛒 Order now: everydaycart.online\n📩 Or inbox us to place your order`, then the hashtag
  line. **No em dashes or en dashes anywhere** (assert this in code).
- **Hashtags: exactly 5 per post, from `tools/hashtags.py`** (`pick(category, brand=..., seed=post_id)` then
  `retag(caption, tags)`; assert `len(re.findall(r'#\w+', caption)) == 5`). Instagram caps captions at 5 hashtags since
  Dec 2025 and posts with more lose reach; Facebook also works best with 3 to 5. Mix: 1 BD shopping tag + 1 BD category
  tag + 2 product/brand tags people search + 1 location tag. Rotate (seeded by post id) so no two posts share the same set.
  No #EverydayCart, #Reels, #Explore or other generic tags. For a product type not in the library, add it to `CAT`.
- **Reach**: the first line is what people see before "more", so make it a keyword-rich hook naming the product type
  (e.g. "🎧 Wireless earbuds under 1,000৳ with clear calls"), not just a generic line. Add one short, natural Bangla line
  that uses the Bangla search word for the product (e.g. ইয়ারবাড, স্মার্ট ওয়াচ, ফ্লাস্ক, বেবি ফিডার). Ask a question
  or give a reason to comment on some posts. Reels get the most reach: hook in the first 1 to 2 seconds.
- Never invent features, claims (e.g. hours a bottle keeps heat), reviews, discounts or offers. Use only what the store
  listing or earlier captions in `scheduler/queue.json` say. Offers, discounts, coupons and sale posts (e.g. the 11.11 draft in
  `posts/drafts/`) need the owner's approval: never queue them yourself.
- **No posts for Hindu festivals or observances.** Bangladesh national days and international days are fine; the
  weekly occasion reminder task handles those separately.
- Original music only (the synth tracks in `tools/make_music.py` and `tools/reels/drive.py`). No copyrighted songs, no
  stock photos of real people, no AI-generated people.

## Daily procedure

1. `git pull`. Check `scheduler/queue.json` for entries already dated today; if today already has 5+ posts, stop.
2. Refresh product data (sync workflow above). Pick products **not featured in the last 2 to 3 days** (check queue ids),
   mixing categories: gadgets (earbuds, watches, speakers, neckband), thermal bottles, baby care, home and gifts.
   One or two collection posts (several products in one image) per day are good.
3. Cutouts live in `tools/cutouts/hq/NN.png` (and `cutouts/flat/`). For a product without a cutout, add a job to
   `tools/prep_hq.py` (rembg `isnet-general-use`; `big()` for small photos) and run it. Inspect the cutout on a dark
   background before using it.
4. Images: write `tools/batch_YYYY_MM_DD.py` following the latest one. Style sets:
   set 1 = `render_flat` A/B/C, set 2 = `render_styles` D/E/F, set 3 = `render_styles3` G/H. Rotate so today differs
   from yesterday; log it in `posts/style_log.json`. Add a new set when the owner may be tired of these.
   Output to `posts/batch-YYYY-MM-DD/`. Render, then view a contact sheet and fix any overflow, tiny product or clash.
5. Reels (1 every day): reuse and vary the engines in `tools/reels/` (`reels9.py`: guess the price,
   this or that, Bangla POV, unboxing, under 1,000, gift guide, top 5, good night; `anim.py`: day story, cart fill,
   product drop, Bangla winter). Change products, colours and hooks every time. Bangla text uses `TB()` (Hind Siliguri).
   1080x1920, 30 fps, 10 to 25 s, music muxed. Check sample frames before queueing. Save to `videos/YYYY-MM-DD/`.
6. Schedule at peak times, Dhaka time (+06:00): about 11:30, 13:30, 16:30, 18:30 (Reel), 20:00 and 21:30 (skip one
   image slot on 4-post days), alternating categories,
   Reels between image posts. Queue entry: `{"id": "YYYY-MM-DD-slug", "time": "YYYY-MM-DDTHH:MM:00+06:00",
   "type": "image"|"carousel"|"reel", "media": ["repo/path"], "caption": "...", "networks": ["facebook","instagram"]}`
   plus `"cover_ms"` for Reels. If the run starts late, start the first slot at least 20 minutes from now.
7. Commit (images, videos, queue, style log, new scripts) and push to `main`. Wait about a minute, `git pull`, and read
   `scheduler/last_run.log`: it must say `Upcoming: N` and name today's first post. If a post from yesterday shows an
   error in `scheduler/state.json`, note it in the summary.
8. Finish with a short summary for the owner: a table of today's times and posts, any Reels, and anything that needs
   his attention (e.g. a product out of stock, a price that changed, a failed post).
