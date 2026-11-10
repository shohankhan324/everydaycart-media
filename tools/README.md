# Everyday Cart design toolkit

Scripts used to make Everyday Cart social posts. Output goes to /mnt/user-data/outputs/.

- `render_flat.py`: flat post templates A (split panel), B (colour card), C (collection grid). Edit POSTS, run with post numbers.
- `render_styles.py`: extra styles D (arch poster), E (scalloped header + feature tiles), F (list menu); `TEMPLATES` maps A to F.
- Daily batches (`batch_YYYY_MM_DD.py`) must use a DIFFERENT style set from the previous day. Check and update `posts/style_log.json`.
- `render_carousel.py`: 7-card square carousel.
- `render_video.py` + `make_music.py`: 1080x1920 Reels with original synthesized music (mux with ffmpeg).
- `prep_hq.py`: high-quality product cutouts (rembg isnet-general-use, EDSR upscaling for small photos, edge cleanup).
- `cutouts/hq`, `cutouts/flat`: ready cutouts. `assets/logo.png`: brand logo, the "everydaycart" wordmark (dark green + green) adopted 10 Nov 2026, transparent PNG; corner placement, small, on a white chip. The old bag logo is kept as `assets/logo_old.png` and must not be used.

Brand: sage (98,120,92), rose (165,112,111), cream (251,246,242), Poppins font. User prefers flat designs (no 3D),
logo in a corner, in-stock colours only, top-notch image quality (inspect every image close up), no em dashes in captions.
Posts are published by scheduler/ (add entries to scheduler/queue.json and push).
