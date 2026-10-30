"""Everyday Cart free scheduler: publishes due posts in scheduler/queue.json to the
Facebook Page and its linked Instagram account through Meta's Graph API.

Run by .github/workflows/publish.yml every 15 minutes. Modes (env MODE):
  run      publish due posts (default)
  check    verify the token, Page and Instagram link, publish nothing
  dry-run  list what would be published, needs no token
"""
import datetime as dt
import json
import os
import sys
import time
from pathlib import Path

import requests

ROOT = Path(__file__).resolve().parent.parent
QUEUE = ROOT / "scheduler" / "queue.json"
STATE = ROOT / "scheduler" / "state.json"

GRAPH = "https://graph.facebook.com/" + os.environ.get("GRAPH_VERSION", "v23.0")
TOKEN = os.environ.get("META_PAGE_TOKEN", "").strip()
PAGE_ID = os.environ.get("FB_PAGE_ID", "1155560334313168")
REPO = os.environ.get("GITHUB_REPOSITORY", "shohankhan324/everydaycart-media")
SHA = os.environ.get("GITHUB_SHA", "main")
PAGES_BASE = os.environ.get("PAGES_BASE", "").rstrip("/")
MODE = os.environ.get("MODE", "run").strip() or "run"

MAX_POSTS_PER_RUN = 1          # one post per 15 min run keeps catch-up posting spaced out
MAX_ATTEMPTS = 3               # per network, then the post is marked failed
MAX_OVERDUE_HOURS = 12         # never publish something more than 12 hours late
REEL_WAIT_SECONDS = 240        # wait this long for Instagram to process a Reel, else resume next run

SUMMARY = []


def log(msg):
    print(msg, flush=True)
    SUMMARY.append(msg)


class GraphError(Exception):
    pass


def graph(method, path, **params):
    params["access_token"] = TOKEN
    url = f"{GRAPH}/{path}"
    if method == "GET":
        r = requests.get(url, params=params, timeout=120)
    else:
        r = requests.post(url, data=params, timeout=300)
    try:
        body = r.json()
    except ValueError:
        raise GraphError(f"HTTP {r.status_code}: {r.text[:300]}")
    if r.status_code >= 400 or (isinstance(body, dict) and "error" in body):
        err = body.get("error", {}) if isinstance(body, dict) else {}
        raise GraphError(f"{err.get('message', r.text[:300])} (code {err.get('code')}, subcode {err.get('error_subcode')})")
    return body


def media_url(path):
    """Public URL for a repo file. Prefer GitHub Pages (correct content types), else raw."""
    if path.startswith("http://") or path.startswith("https://"):
        return path
    if PAGES_BASE:
        url = f"{PAGES_BASE}/{path}"
        try:
            if requests.head(url, timeout=20, allow_redirects=True).status_code == 200:
                return url
        except requests.RequestException:
            pass
    return f"https://raw.githubusercontent.com/{REPO}/{SHA}/{path}"


def load(path, default):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError):
        return default


def now_utc():
    return dt.datetime.now(dt.timezone.utc)


def parse_time(s):
    t = dt.datetime.fromisoformat(s)
    if t.tzinfo is None:
        t = t.replace(tzinfo=dt.timezone(dt.timedelta(hours=6)))   # Dhaka
    return t.astimezone(dt.timezone.utc)


# ---------------- Facebook ----------------
def fb_publish(post):
    kind, caption, media = post["type"], post.get("caption", ""), post["media"]
    if kind == "image":
        r = graph("POST", f"{PAGE_ID}/photos", url=media_url(media[0]), caption=caption, published="true")
        pid = r.get("post_id") or r["id"]
        return {"id": pid, "url": f"https://www.facebook.com/{pid}"}
    if kind == "carousel":
        ids = [graph("POST", f"{PAGE_ID}/photos", url=media_url(m), published="false")["id"] for m in media]
        r = graph("POST", f"{PAGE_ID}/feed", message=caption,
                  attached_media=json.dumps([{"media_fbid": i} for i in ids]))
        return {"id": r["id"], "url": f"https://www.facebook.com/{r['id']}"}
    if kind == "reel":
        start = graph("POST", f"{PAGE_ID}/video_reels", upload_phase="start")
        vid, up = start["video_id"], start["upload_url"]
        r = requests.post(up, headers={"Authorization": f"OAuth {TOKEN}", "file_url": media_url(media[0])}, timeout=600)
        if r.status_code >= 400 or not r.json().get("success"):
            raise GraphError(f"reel upload failed: {r.text[:300]}")
        graph("POST", f"{PAGE_ID}/video_reels", upload_phase="finish", video_id=vid,
              video_state="PUBLISHED", description=caption)
        return {"id": vid, "url": f"https://www.facebook.com/reel/{vid}"}
    raise GraphError(f"unknown post type {kind}")


# ---------------- Instagram ----------------
def ig_user_id(state):
    meta = state.setdefault("_meta", {})
    if not meta.get("ig_user_id"):
        r = graph("GET", PAGE_ID, fields="name,instagram_business_account")
        acct = r.get("instagram_business_account")
        if not acct:
            raise GraphError("this Facebook Page has no linked Instagram business account")
        meta["ig_user_id"] = acct["id"]
    return meta["ig_user_id"]


def ig_wait(container, seconds):
    t0 = time.time()
    while time.time() - t0 < seconds:
        s = graph("GET", container, fields="status_code,status")
        code = s.get("status_code")
        if code in ("FINISHED", "PUBLISHED"):
            return True
        if code in ("ERROR", "EXPIRED"):
            raise GraphError(f"Instagram could not process the media: {s.get('status')}")
        time.sleep(5)
    return False


def ig_publish(post, entry, state):
    ig = ig_user_id(state)
    container = entry.get("container")
    if not container:
        kind, caption, media = post["type"], post.get("caption", ""), post["media"]
        if kind == "image":
            container = graph("POST", f"{ig}/media", image_url=media_url(media[0]), caption=caption)["id"]
        elif kind == "carousel":
            kids = [graph("POST", f"{ig}/media", image_url=media_url(m), is_carousel_item="true")["id"] for m in media]
            for k in kids:
                ig_wait(k, 60)
            container = graph("POST", f"{ig}/media", media_type="CAROUSEL", children=",".join(kids), caption=caption)["id"]
        elif kind == "reel":
            params = dict(media_type="REELS", video_url=media_url(media[0]), caption=caption, share_to_feed="true")
            if post.get("cover_ms") is not None:
                params["thumb_offset"] = str(int(post["cover_ms"]))
            container = graph("POST", f"{ig}/media", **params)["id"]
        else:
            raise GraphError(f"unknown post type {kind}")
        entry["container"] = container
    wait = REEL_WAIT_SECONDS if post["type"] == "reel" else 90
    if not ig_wait(container, wait):
        return None                                  # still processing, resume next run
    mid = graph("POST", f"{ig}/media_publish", creation_id=container)["id"]
    link = graph("GET", mid, fields="permalink").get("permalink", "")
    return {"id": mid, "url": link}


PUBLISHERS = {"facebook": fb_publish, "instagram": ig_publish}


def publish_post(post, state):
    pst = state.setdefault(post["id"], {})
    for net in post.get("networks", ["facebook", "instagram"]):
        entry = pst.setdefault(net, {})
        if entry.get("status") in ("published", "failed", "skipped"):
            continue
        try:
            res = ig_publish(post, entry, state) if net == "instagram" else fb_publish(post)
            if res is None:
                entry["status"] = "processing"
                log(f"  {net}: still processing, will finish next run")
                continue
            entry.update(status="published", id=res["id"], url=res["url"],
                         at=now_utc().isoformat(timespec="seconds"), error=None)
            entry.pop("container", None)
            log(f"  {net}: published {res['url']}")
        except (GraphError, requests.RequestException, KeyError) as e:
            entry["attempts"] = entry.get("attempts", 0) + 1
            entry["error"] = str(e)[:500]
            entry["status"] = "failed" if entry["attempts"] >= MAX_ATTEMPTS else "retry"
            if "container" in entry and entry["status"] == "failed":
                entry.pop("container")
            log(f"  {net}: ERROR ({entry['attempts']}/{MAX_ATTEMPTS}) {e}")


def pending_networks(post, state):
    pst = state.get(post["id"], {})
    return [n for n in post.get("networks", ["facebook", "instagram"])
            if pst.get(n, {}).get("status") not in ("published", "failed", "skipped")]


def run(dry=False):
    queue = load(QUEUE, [])
    state = load(STATE, {})
    now = now_utc()
    due = sorted((p for p in queue if parse_time(p["time"]) <= now and pending_networks(p, state)),
                 key=lambda p: parse_time(p["time"]))
    upcoming = sorted((p for p in queue if parse_time(p["time"]) > now), key=lambda p: parse_time(p["time"]))
    log(f"Now {now.isoformat(timespec='minutes')} UTC. Due: {len(due)}. Upcoming: {len(upcoming)}.")
    done = 0
    for post in due:
        late_h = (now - parse_time(post["time"])).total_seconds() / 3600
        if late_h > MAX_OVERDUE_HOURS:
            for n in pending_networks(post, state):
                state.setdefault(post["id"], {})[n] = {"status": "skipped", "error": f"{late_h:.1f}h overdue"}
            log(f"SKIP {post['id']}: {late_h:.1f}h overdue")
            continue
        if done >= MAX_POSTS_PER_RUN:
            break
        log(f"POST {post['id']} ({post['type']}, scheduled {post['time']})")
        if not dry:
            publish_post(post, state)
        done += 1
    if upcoming:
        log(f"Next: {upcoming[0]['id']} at {upcoming[0]['time']}")
    if not dry:
        STATE.write_text(json.dumps(state, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def check():
    me = graph("GET", PAGE_ID, fields="name,instagram_business_account{username,id}")
    log(f"Page: {me.get('name')} ({PAGE_ID})")
    acct = me.get("instagram_business_account")
    log(f"Instagram: @{acct.get('username')} ({acct.get('id')})" if acct else "Instagram: NOT LINKED to this Page")
    try:
        d = graph("GET", "debug_token", input_token=TOKEN).get("data", {})
        exp = d.get("expires_at", 0)
        log(f"Token type: {d.get('type')}, expires: {'never' if not exp else dt.datetime.fromtimestamp(exp, dt.timezone.utc).isoformat()}")
        log(f"Permissions: {', '.join(d.get('scopes', []))}")
    except GraphError as e:
        log(f"(could not read token details: {e})")


def main():
    code = 0
    try:
        if MODE == "dry-run":
            run(dry=True)
        elif not TOKEN:
            log("META_PAGE_TOKEN secret is not set yet, nothing published.")
        elif MODE == "check":
            check()
        else:
            run()
    except Exception as e:                       # keep the reason visible in last_run.log
        log(f"FATAL {type(e).__name__}: {e}")
        code = 1
    finally:
        stamp = now_utc().isoformat(timespec="seconds")
        (ROOT / "scheduler" / "last_run.log").write_text(f"{stamp} mode={MODE}\n" + "\n".join(SUMMARY) + "\n", encoding="utf-8")
        out = os.environ.get("GITHUB_STEP_SUMMARY")
        if out:
            with open(out, "a", encoding="utf-8") as fh:
                fh.write("### Everyday Cart publisher\n\n" + "\n".join(f"- {l}" for l in SUMMARY) + "\n")
    return code


if __name__ == "__main__":
    sys.exit(main())
