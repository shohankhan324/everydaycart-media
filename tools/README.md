# Everyday Cart design toolkit

Scripts used to make Everyday Cart social posts. Output goes to /mnt/user-data/outputs/.

- `render_flat.py`: flat post templates A (split panel), B (colour card), C (collection grid). Edit POSTS, run with post numbers.
- `render_carousel.py`: 7-card square carousel.
- `render_video.py` + `make_music.py`: 1080x1920 Reels with original synthesized music (mux with ffmpeg).
- `prep_hq.py`: high-quality product cutouts (rembg isnet-general-use, EDSR upscaling for small photos, edge cleanup).
- `cutouts/hq`, `cutouts/flat`: ready cutouts. `assets/logo.png`: brand logo (corner placement, small).

Brand: sage (98,120,92), rose (165,112,111), cream (251,246,242), Poppins font. User prefers flat designs (no 3D),
logo in a corner, in-stock colours only, top-notch image quality (inspect every image close up), no em dashes in captions.
Posts are published by scheduler/ (add entries to scheduler/queue.json and push).
