#!/usr/bin/env python3
"""
Create a new post and update:
- posts/ (HTML file)
- index.html (prepends to Latest posts list)
- feed.xml (appends an <item>)
- search_index.json (adds an entry)

Usage:
  python new_post.py "My Title"
  python new_post.py "My Title" --summary "One line." --tags rpg,design --date 2025-11-06

Notes:
- Brand is set to "Rabbit & Wolf"
- Edit DEFAULT_TIME if you want a different RSS publish time
"""

import sys, os, re, json, datetime
from pathlib import Path
from html import escape

ROOT   = Path(__file__).parent
POSTS  = ROOT / "posts"
INDEX  = ROOT / "index.html"
FEED   = ROOT / "feed.xml"
SEARCH = ROOT / "search_index.json"

BRAND = "Rabbit & Wolf"
DEFAULT_TIME = "12:00:00 +0000"  # RSS time component

POST_TEMPLATE = """<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{brand} — {title}</title>
  <link rel="stylesheet" href="/assets/style.css">
  <meta name="date" content="{date_iso}">
  <!-- Uncomment to enable MathJax on this post
  <script id="MathJax-script" async
    src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"></script>
  -->
</head>
<body>
  <div class="container">
    <header class="header">
      <div class="brand">{brand_esc}</div>
      <nav class="nav">
        <a href="/">Home</a>
        <a href="/about.html">About</a>
        <a href="/search.html">Search</a>
        <a href="/subscribe.html">Subscribe</a>
        <a href="/feed.xml">RSS</a>
      </nav>
    </header>

    <article class="card">
      <p class="meta">Published {date_human}</p>
      <h1>{title}</h1>

      <p>Write here.</p>

    </article>

    <footer class="footer">© <span id="year"></span> {brand_esc}</footer>
    <script>document.getElementById('year').textContent = new Date().getFullYear();</script>
  </div>
</body>
</html>
"""

def slugify(s: str) -> str:
    s = s.strip().lower()
    s = re.sub(r"[—–]", "-", s)           # em/en dash to hyphen
    s = re.sub(r"[^a-z0-9\- _]+", "", s)  # drop punctuation
    s = s.replace(" ", "-")
    s = re.sub(r"-+", "-", s)             # collapse dashes
    return s.strip("-") or "post"

def parse_args(argv):
    import argparse
    p = argparse.ArgumentParser(description="Create a new post and update index/feed/search.")
    p.add_argument("title", help="Post title")
    p.add_argument("--summary", default=None, help="One-line summary for RSS/search (optional)")
    p.add_argument("--tags", default=None, help="Comma-separated tags, e.g. 'rpg,design'")
    p.add_argument("--date", default=None, help="Override date YYYY-MM-DD (optional)")
    return p.parse_args(argv)

def ensure_files_exist():
    if not INDEX.exists():
        sys.exit("ERROR: index.html not found at repo root.")
    if not FEED.exists():
        sys.exit("ERROR: feed.xml not found at repo root.")
    POSTS.mkdir(exist_ok=True)

def make_post_file(title: str, date_iso: str, filename: str):
    html = POST_TEMPLATE.format(
        brand=BRAND,
        brand_esc=escape(BRAND),
        title=escape(title),
        date_iso=date_iso,
        date_human=date_iso
    )
    path = POSTS / filename
    path.write_text(html, encoding="utf-8")
    return path

def prepend_post_to_index(index_path: Path, post_url: str, title: str, date_iso: str):
    """
    Inserts a new <li> at the top of <ul class="post-list"> ... </ul>
    If the UL is not found, exits with an error.
    """
    idx = index_path.read_text(encoding="utf-8")
    ul_open_re = re.compile(r'(<ul\s+class="post-list"\s*>)', re.IGNORECASE)
    m = ul_open_re.search(idx)
    if not m:
        sys.exit('ERROR: Could not find <ul class="post-list"> in index.html.')
    insert_pos = m.end()
    li = f'\n          <li><a href="{post_url}">{escape(title)}</a> <span class="meta">— {date_iso}</span></li>'
    new_idx = idx[:insert_pos] + li + idx[insert_pos:]
    index_path.write_text(new_idx, encoding="utf-8")

def append_item_to_feed(feed_path: Path, title: str, link: str, date_iso: str, summary: str):
    """
    Appends an <item> before </channel>.
    """
    feed = feed_path.read_text(encoding="utf-8")
    if "</channel>" not in feed:
        sys.exit("ERROR: feed.xml missing </channel>.")
    # Compute RFC-822-ish pubDate line
    dt = datetime.datetime.strptime(date_iso, "%Y-%m-%d")
    pub = dt.strftime("%a, %d %b %Y ") + DEFAULT_TIME
    item = f"""
    <item>
      <title>{escape(title)}</title>
      <link>{link}</link>
      <pubDate>{pub}</pubDate>
      <guid>{link}</guid>
      <description><![CDATA[{summary}]]></description>
    </item>"""
    feed = feed.replace("</channel>", item + "\n  </channel>")
    feed_path.write_text(feed, encoding="utf-8")

def update_search_index(search_path: Path, title: str, url: str, date_iso: str, summary: str, tags_list):
    data = []
    if search_path.exists():
        try:
            data = json.loads(search_path.read_text(encoding="utf-8"))
            if not isinstance(data, list):
                data = []
        except Exception:
            data = []
    entry = {
        "title": title,
        "url": url,
        "date": date_iso,
        "date_iso": date_iso,
        "summary": summary,
        "tags": tags_list,
        # keep content minimal; you can expand later or generate from the post
        "content": summary
    }
    # If an entry for this URL exists, replace it
    data = [e for e in data if e.get("url") != url]
    data.append(entry)
    # Sort newest first
    try:
        data.sort(key=lambda e: e.get("date_iso", ""), reverse=True)
    except Exception:
        pass
    search_path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")

def main():
    args = parse_args(sys.argv[1:])
    title = args.title.strip()
    if not title:
        sys.exit("ERROR: Title cannot be empty.")
    date_iso = args.date or datetime.date.today().isoformat()
    slug = slugify(title)
    filename = f"{date_iso}-{slug}.html"
    url = f"/posts/{filename}"

    summary = (args.summary or title).strip()
    tags_list = []
    if args.tags:
        tags_list = [t.strip() for t in args.tags.split(",") if t.strip()]

    ensure_files_exist()
    post_path = make_post_file(title, date_iso, filename)
    prepend_post_to_index(INDEX, url, title, date_iso)
    # FEED: set absolute link for GitHub Pages (adjust username if needed)
    # If you later move to a custom domain, the GUID can stay stable or be updated.
    username = ROOT.name.replace(".github.io", "")  # best guess if repo is yourname.github.io
    link = f"https://{username}.github.io{url}"
    append_item_to_feed(FEED, title, link, date_iso, summary)
    update_search_index(SEARCH, title, url, date_iso, summary, tags_list)

    print(f"✅ Created {post_path}")
    print(f"🔗 Linked on index.html and feed.xml")
    print(f"🔎 Updated search_index.json")

if __name__ == "__main__":
    main()
