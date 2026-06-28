#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generic Xueqiu scraper: traverse a given user's full timeline, filter the user's
own original posts by keyword.

Features:
  - Playwright login-state reuse: first run is headful for manual login, state persisted locally
  - Dual-channel fetch: prefer in-page JS fetch, fall back to context.request (APIRequestContext)
  - Resumable crawl: save progress every 10 pages; re-running after an interruption auto-continues
  - Anti-rate-limit: 2-4s random jitter + 30s long rest every 50 pages + auto-exit (saving progress) after 5 consecutive timeouts
  - Pure-repost filter: only collect content the scraped user wrote themselves (non-empty text, not a "repost")

Credentials are passed via environment variables and **never enter the repo**:
  export XQ_PHONE=13xxxxxxxxx
  export XQ_PASSWORD=xxx
They are optional; on the first run a headful browser pops up for manual login (QR/SMS/password, your choice).

Usage examples:
  # Duan Yongping on Pinduoduo
  python3 xueqiu_scraper.py \\
      --user-id 1247347556 \\
      --keywords 拼多多,PDD,Temu,黄峥 \\
      --output ../reports/拼多多/段永平雪球发言-PDD相关.md

  # Other users + other keywords
  python3 xueqiu_scraper.py --user-id 6784593966 --keywords 茅台 --output /tmp/out.md

Login-state cache defaults to /tmp/xueqiu_state.json, override with --state-path.
"""

import argparse
import asyncio
import json
import os
import random
import re
from datetime import datetime
from pathlib import Path
from playwright.async_api import async_playwright


def is_match(text, keywords):
    t = (text or '').lower()
    return any(k.lower() in t for k in keywords)


def parse_ts(ts):
    try:
        return datetime.fromtimestamp(int(ts) / 1000).strftime('%Y-%m-%d %H:%M')
    except Exception:
        return str(ts)


def clean(s):
    if not s: return ''
    s = re.sub(r'<[^>]+>', '', s)
    for ent, rep in [('&amp;', '&'), ('&lt;', '<'), ('&gt;', '>'), ('&nbsp;', ' ')]:
        s = s.replace(ent, rep)
    return re.sub(r'&#\d+;', '', s).strip()


async def browser_fetch_json(page, url, timeout_s=15):
    """Prefer in-page JS fetch; fall back to context.request on failure."""
    js = f"""
        async () => {{
            const ctl = new AbortController();
            const to = setTimeout(() => ctl.abort(), {int(timeout_s*1000)});
            try {{
                const r = await fetch({json.dumps(url)}, {{
                    headers: {{'Accept':'application/json','X-Requested-With':'XMLHttpRequest'}},
                    credentials: 'include', signal: ctl.signal
                }});
                const text = await r.text();
                clearTimeout(to);
                try {{ return JSON.parse(text); }}
                catch(e) {{ return {{_raw: text.substring(0, 300)}}; }}
            }} catch(e) {{
                clearTimeout(to);
                return {{_error: e.toString()}};
            }}
        }}
    """
    try:
        result = await asyncio.wait_for(page.evaluate(js), timeout=timeout_s + 5)
        if result and not result.get('_error') and not result.get('_raw'):
            return result
    except Exception:
        pass
    try:
        resp = await page.context.request.get(url, headers={
            'Accept': 'application/json',
            'X-Requested-With': 'XMLHttpRequest',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36',
            'Referer': 'https://xueqiu.com/',
        }, timeout=timeout_s * 1000)
        if resp.ok:
            return await resp.json()
    except Exception:
        return None
    return None


async def verify_login(page, user_id):
    test = await browser_fetch_json(
        page,
        f'https://xueqiu.com/v4/statuses/user_timeline.json?user_id={user_id}&page=2&count=1'
    )
    return bool(test and test.get('statuses') is not None)


async def interactive_login(pw, state_path, user_id):
    phone = os.environ.get('XQ_PHONE', '')
    print("\n[Login required] A headful browser will open, please complete the Xueqiu login in it")
    if phone:
        print(f"        Environment variable XQ_PHONE = {phone}   (password via XQ_PASSWORD)")
    else:
        print("        XQ_PHONE/XQ_PASSWORD not set, please scan the QR code or enter login info manually in the browser")
    browser = await pw.chromium.launch(
        headless=False,
        args=['--disable-blink-features=AutomationControlled'],
    )
    context = await browser.new_context(
        user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        locale='zh-CN',
        viewport={'width': 1280, 'height': 800},
    )
    await context.add_init_script(
        "Object.defineProperty(navigator,'webdriver',{get:()=>undefined})"
    )
    page = await context.new_page()
    await page.goto('https://xueqiu.com/', wait_until='domcontentloaded')
    print(">>> Please complete the login in the browser; the script polls every 5s and auto-continues on success (up to 10 minutes)")
    ok = False
    for i in range(120):
        await asyncio.sleep(5)
        try:
            if await verify_login(page, user_id):
                ok = True
                print(f"  ✓ Login successful (poll #{i+1})")
                break
        except Exception as e:
            print(f"  Poll exception (ignored): {e}")
        if (i + 1) % 6 == 0:
            print(f"  ...still waiting for login (waited {(i+1)*5}s)")
    if not ok:
        print("Login not detected within 10 minutes, exiting")
        await browser.close()
        return None
    await context.storage_state(path=state_path)
    print(f"Login state saved → {state_path}")
    return browser, context, page


async def load_with_state(pw, state_path, user_id):
    if not os.path.exists(state_path):
        return None
    browser = await pw.chromium.launch(
        headless=True,
        args=['--no-sandbox', '--disable-blink-features=AutomationControlled'],
    )
    context = await browser.new_context(
        storage_state=state_path,
        user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        locale='zh-CN',
        viewport={'width': 1280, 'height': 800},
    )
    await context.add_init_script(
        "Object.defineProperty(navigator,'webdriver',{get:()=>undefined})"
    )
    page = await context.new_page()
    loaded = False
    for attempt in range(3):
        try:
            await page.goto('https://xueqiu.com/', wait_until='domcontentloaded', timeout=15000)
            loaded = True
            break
        except Exception as e:
            print(f"  Home page load failed (#{attempt+1}): {e}")
            await asyncio.sleep(5)
    if not loaded:
        try:
            await page.goto('about:blank')
        except Exception:
            pass
    await asyncio.sleep(2)
    if await verify_login(page, user_id):
        print("✓ Reused saved login state")
        return browser, context, page
    print("Saved state has expired")
    await browser.close()
    return None


async def fetch_all_timeline(page, user_id, keywords, progress_path, dump_all_path=''):
    collected = {}
    # all_posts: store all of the user's original posts (no keyword filter), for offline multi-topic analysis
    all_posts = {}
    if dump_all_path and os.path.exists(dump_all_path):
        try:
            for e in json.load(open(dump_all_path)):
                all_posts[e['id']] = e
            print(f"  ↪ Loaded existing full cache: {len(all_posts)} items")
        except Exception as e:
            print(f"  Full-cache read failed: {e}")
    print("\n=== Traversing the full timeline ===")
    data = await browser_fetch_json(
        page,
        f'https://xueqiu.com/v4/statuses/user_timeline.json?user_id={user_id}&page=1&count=20'
    )
    if not data or data.get('error_code'):
        print(f"  Page 1 failed: {data}")
        return collected
    max_page = data.get('maxPage', 600)
    total = data.get('total', '?')
    print(f"  User ID: {user_id} | total posts: {total} | total pages: {max_page}")

    total_posts = 0
    found = 0

    def process(d):
        nonlocal total_posts, found
        for post in d.get('statuses', []):
            total_posts += 1
            text = clean(post.get('text', '') or post.get('description', ''))
            title = clean(post.get('title', ''))
            rt = post.get('retweeted_status') or {}
            rt_text = clean(rt.get('text', ''))
            own_text = (text or '').strip()
            if own_text in ('', '转发微博', '轉發微博', 'Repost'):
                continue
            pid = str(post.get('id', ''))
            date = parse_ts(post.get('created_at', 0))
            entry = {'id': pid, 'date': date, 'title': title, 'text': own_text,
                     'url': f'https://xueqiu.com/{user_id}/{pid}'}
            if rt:
                rt_user = (rt.get('user') or {}).get('screen_name', '')
                entry['retweet_of'] = f'@{rt_user}: {rt_text}'
            # full cache (no filter)
            if dump_all_path and pid not in all_posts:
                all_posts[pid] = entry
            # collect by keyword filter
            if keywords and is_match(title + ' ' + own_text, keywords):
                if pid not in collected:
                    collected[pid] = entry
                    found += 1
                    preview = own_text[:80] if own_text else (rt_text[:80] if rt_text else title[:80])
                    print(f"  ✓ [{date}] {preview}...")

    process(data)
    start_page = 2
    if os.path.exists(progress_path):
        try:
            with open(progress_path) as f:
                prev = json.load(f)
            start_page = max(2, prev.get('next_page', 2))
            for e in prev.get('collected', []):
                collected[e['id']] = e
                found += 1
            print(f"  ↪ Resuming: starting from page {start_page}, already have {found} items")
        except Exception as e:
            print(f"  Progress file read failed: {e}")

    def save_progress(next_page):
        with open(progress_path, 'w', encoding='utf-8') as f:
            json.dump({'next_page': next_page, 'collected': list(collected.values())},
                      f, ensure_ascii=False)
        if dump_all_path:
            with open(dump_all_path, 'w', encoding='utf-8') as f:
                json.dump(list(all_posts.values()), f, ensure_ascii=False)

    consec_fail = 0
    for p in range(start_page, max_page + 1):
        try:
            data = await browser_fetch_json(
                page,
                f'https://xueqiu.com/v4/statuses/user_timeline.json?user_id={user_id}&page={p}&count=20',
                timeout_s=15,
            )
        except Exception as e:
            print(f"  Page {p} exception: {e}")
            data = None
        if not data:
            consec_fail += 1
            print(f"  Page {p} no response/timeout (consecutive {consec_fail})")
            if consec_fail >= 5:
                print("  5 consecutive failures, saving progress and exiting (re-run to auto-resume)")
                save_progress(p)
                break
            await asyncio.sleep(5 * consec_fail)
            continue
        consec_fail = 0
        if data.get('error_code'):
            print(f"  Page {p} error: {data.get('error_code')} {data.get('error_description')}")
            save_progress(p)
            break
        statuses = data.get('statuses', [])
        if not statuses:
            print(f"  Page {p} empty, finishing")
            break
        prev_found = found
        process(data)
        if p % 10 == 0 or found > prev_found:
            print(f"  Page {p}/{max_page} | scanned {total_posts} items | hits {found}")
        if p % 10 == 0:
            save_progress(p + 1)
        if p % 50 == 0:
            print(f"  ⏸ Resting 30s after page {p}")
            await asyncio.sleep(30)
        else:
            await asyncio.sleep(random.uniform(2.0, 4.0))
    else:
        if os.path.exists(progress_path):
            os.remove(progress_path)

    # final flush of the full cache to disk
    if dump_all_path:
        with open(dump_all_path, 'w', encoding='utf-8') as f:
            json.dump(list(all_posts.values()), f, ensure_ascii=False)
        print(f"  Full cache → {dump_all_path} ({len(all_posts)} items)")
    print(f"\nDone: scanned {total_posts} items, {found} hits")
    return collected


def format_md(collected, user_id, keywords):
    posts = sorted(collected.values(), key=lambda x: x.get('date', ''))
    lines = [
        f"# Xueqiu posts compilation: user {user_id}",
        "",
        f"> **Source**: Xueqiu https://xueqiu.com/u/{user_id}",
        f"> **Compiled on**: {datetime.now().strftime('%Y-%m-%d')}",
        f"> **Items collected**: {len(posts)}",
        f"> **Keyword filter**: {', '.join(keywords)}",
        f"> **Collection method**: Playwright login state + full traversal of user_timeline.json (own original posts only)",
        "",
        "---",
        "",
    ]
    for i, p in enumerate(posts, 1):
        lines.append(f"## {i}. {p.get('date','?')}")
        lines.append("")
        if p.get('title'):
            lines += [f"**[{p['title']}]**", ""]
        if p.get('retweet_of'):
            lines += [f"> Reposted original: {p['retweet_of']}", ""]
        if p.get('text'):
            lines.append(p['text'])
            lines.append("")
        lines += [f"Source: {p.get('url','')}", "", "---", ""]
    return '\n'.join(lines)


def parse_args():
    ap = argparse.ArgumentParser(description="Xueqiu user timeline scraper (filter own original posts by keyword)")
    ap.add_argument('--user-id', type=int, help='Xueqiu user ID (the numeric part of the profile URL)')
    ap.add_argument('--keywords', type=str, default='',
                    help='comma-separated keyword list. e.g.: 拼多多,PDD,黄峥,Temu')
    ap.add_argument('--output', type=str, default='', help='markdown output path')
    ap.add_argument('--raw-json', type=str, default='', help='(optional) raw JSON output path for matched items')
    ap.add_argument('--state-path', type=str, default='/tmp/xueqiu_state.json',
                    help='login-state cache file (default /tmp/xueqiu_state.json)')
    ap.add_argument('--dump-all', type=str, default='',
                    help='full-cache path: while crawling, also write all of the user\'s original posts here, for later offline multi-topic analysis')
    ap.add_argument('--from-cache', type=str, default='',
                    help='skip crawling, generate markdown by filtering an existing full-cache JSON (requires --keywords and --output)')
    return ap.parse_args()


def filter_from_cache(cache_path, keywords, user_id):
    posts = json.load(open(cache_path))
    out = []
    for p in posts:
        if is_match((p.get('title','') + ' ' + p.get('text','')), keywords):
            out.append(p)
    return {p['id']: p for p in out}


async def main():
    args = parse_args()
    keywords = [k.strip() for k in args.keywords.split(',') if k.strip()]

    # Offline filter mode
    if args.from_cache:
        if not (keywords and args.output):
            print("--from-cache requires both --keywords and --output")
            return
        user_id = args.user_id or 0
        collected = filter_from_cache(args.from_cache, keywords, user_id)
        print(f"Filtered {len(collected)} items from cache {args.from_cache} (keywords: {keywords})")
        if not collected:
            return
        Path(args.output).parent.mkdir(parents=True, exist_ok=True)
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(format_md(collected, user_id, keywords))
        print(f"Markdown → {args.output}")
        return

    if not args.user_id:
        print("--user-id is required")
        return

    progress_path = args.state_path + f'.progress.{args.user_id}'
    raw_json = args.raw_json or f'/tmp/xueqiu_{args.user_id}_raw.json'

    print("=" * 60)
    print(f"Xueqiu scraper | user_id={args.user_id} | keywords={keywords} | dump_all={args.dump_all}")
    print("=" * 60)

    async with async_playwright() as pw:
        session = await load_with_state(pw, args.state_path, args.user_id)
        if not session:
            session = await interactive_login(pw, args.state_path, args.user_id)
        if not session:
            print("Could not log in, exiting")
            return
        browser, _, page = session
        collected = await fetch_all_timeline(page, args.user_id, keywords, progress_path, args.dump_all)
        await browser.close()

    print(f"\n=== Final: {len(collected)} hits ===")
    if not collected:
        return
    with open(raw_json, 'w', encoding='utf-8') as f:
        json.dump(list(collected.values()), f, ensure_ascii=False, indent=2)
    print(f"Raw JSON → {raw_json}")
    if args.output:
        Path(args.output).parent.mkdir(parents=True, exist_ok=True)
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(format_md(collected, args.user_id, keywords))
        print(f"Markdown  → {args.output}")


if __name__ == '__main__':
    asyncio.run(main())
