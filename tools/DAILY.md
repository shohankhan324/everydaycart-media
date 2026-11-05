# Everyday Cart daily posting runbook

The owner (Engr Md Shohan Khan) wants Everyday Cart's Facebook Page and Instagram (@everydaycart.bd) to get
**8 to 10 image posts every day, plus 2 or 3 Reels on some days (about every other day)**, prepared and scheduled
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
  `⚡ Limited stock available!\n🛒 Order now: everydaycart.online\n📩 Or inbox us to place your order`, then hashtags ending
  `#OnlineShoppingBD #Dhaka #Bangladesh`. **No em dashes or en dashes anywhere** (assert this in code).
- Never invent features, claims (e.g. hours a bottle keeps heat), reviews, discounts or offers. Use only what the store
  listing or earlier captions in `scheduler/queue.json` say. Offers, discounts, coupons and sale posts (e.g. the 11.11 draft in
  `posts/drafts/`) need the owner's approval: never queue them yourself.
- **No posts for Hindu festivals or observances.** Bangladesh national days and international days are fine; the
  weekly occasion reminder task handles those separately.
- Original music only (the synth tracks in `tools/make_music.py` and `tools/reels/drive.py`). No copyrighted songs, no
  stock photos of real people, no AI-generated people.

## Daily procedure

1. `git pull`. Check `scheduler/queue.json` for entries already dated today; if today already has 8+ posts, stop.
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
5. Reels (about every other day, 2 or 3): reuse and vary the engines in `tools/reels/` (`reels9.py`: guess the price,
   this or that, Bangla POV, unboxing, under 1,000, gift guide, top 5, good night; `anim.py`: day story, cart fill,
   product drop, Bangla winter). Change products, colours and hooks every time. Bangla text uses `TB()` (Hind Siliguri).
   1080x1920, 30 fps, 10 to 25 s, music muxed. Check sample frames before queueing. Save to `videos/YYYY-MM-DD/`.
6. Schedule from about 11:00 to 21:30 Dhaka time (+06:00), roughly every 75 to 90 minutes, alternating categories,
   Reels between image posts. Queue entry: `{"id": "YYYY-MM-DD-slug", "time": "YYYY-MM-DDTHH:MM:00+06:00",
   "type": "image"|"carousel"|"reel", "media": ["repo/path"], "caption": "...", "networks": ["facebook","instagram"]}`
   plus `"cover_ms"` for Reels. If the run starts late, start the first slot at least 20 minutes from now.
7. Commit (images, videos, queue, style log, new scripts) and push to `main`. Wait about a minute, `git pull`, and read
   `scheduler/last_run.log`: it must say `Upcoming: N` and name today's first post. If a post from yesterday shows an
   error in `scheduler/state.json`, note it in the summary.
8. Finish with a short summary for the owner: a table of today's times and posts, any Reels, and anything that needs
   his attention (e.g. a product out of stock, a price that changed, a failed post).
