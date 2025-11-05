#!/usr/bin/env python3
"""
Create a new post file and append to index and feed.
Usage:
  python new_post.py "My Title"
"""
import sys, os, datetime
from pathlib import Path

ROOT = Path(__file__).parent
POSTS = ROOT / "posts"
INDEX = ROOT / "index.html"
FEED = ROOT / "feed.xml"

TEMPLATE = """<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{title}</title>
  <link rel="stylesheet" href="/assets/style.css">
  <meta name="date" content="{date_iso}">
</head>
<body>
  <div class="container">
    <header class="header">
      <div class="brand">Forge &amp; Quill</div>
      <nav class="nav">
        <a href="/">Home</a>
        <a href="/about.html">About</a>
        <a href="/feed.xml">RSS</a>
      </nav>
    </header>

    <article class="card">
      <p class="meta">Published {date_human}</p>
      <h1>{title}</h1>
      <p>Write here.</p>
    </article>

    <footer class="footer">© <span id="year"></span> Forge &amp; Quill</footer>
    <script>document.getElementById('year').textContent = new Date().getFullYear();</script>
  </div>
</body>
</html>
"""

def main():
    if len(sys.argv) < 2:
        print("Usage: python new_post.py \"My Title\"")
        sys.exit(1)
    title = sys.argv[1].strip()
    today = datetime.date.today()
    slug = title.lower().replace(" ", "-").replace("—","-").replace("–","-")
    fname = f"{today.isoformat()}-{slug}.html"
    path = POSTS / fname

    date_iso = today.isoformat()
    date_human = today.strftime("%Y‑%m‑%d")

    path.write_text(TEMPLATE.format(title=title, date_iso=date_iso, date_human=date_human), encoding="utf-8")

    # Update index.html (naive append)
    idx = INDEX.read_text(encoding="utf-8")
    marker = "<ul class=\"post-list\">"
    li = f'          <li><a href="/posts/{fname}">{title}</a> <span class="meta">— {date_human}</span></li>\n'
    idx = idx.replace(marker, marker + "\n" + li)
    INDEX.write_text(idx, encoding="utf-8")

    # Update feed.xml (naive append before </channel>)
    feed = FEED.read_text(encoding="utf-8")
    item = f"""
    <item>
      <title>{title}</title>
      <link>https://yourname.github.io/posts/{fname}</link>
      <pubDate>{today.strftime("%a, %d %b %Y 12:00:00 +0000")}</pubDate>
      <guid>https://yourname.github.io/posts/{fname}</guid>
      <description><![CDATA[{title}]]></description>
    </item>"""
    feed = feed.replace("</channel>", item + "\n  </channel>")
    FEED.write_text(feed, encoding="utf-8")

    print(f"Created posts/{fname} and updated index/feed.")

if __name__ == "__main__":
    main()