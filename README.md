# Forge & Quill — Static Site Starter

A tiny, no-build website for publishing essays, notes, and design work. Pure HTML/CSS so you can deploy anywhere (GitHub Pages recommended).

## Quick Start

1) Create a repo named **yourname.github.io** on GitHub.
2) Upload these files to the repo root (keep the structure).
3) In the repo: Settings → Pages → Build and deployment → **Deploy from a branch** → Branch: **main** (or master) → root `/`.
4) Wait ~1 minute. Your site will be live at **https://yourname.github.io**.

### Custom domain (optional)
- Buy a domain. In the repo root, create a file named `CNAME` with exactly your domain inside, e.g.
```
example.com
```
- Point DNS to GitHub Pages IPs (or use Cloudflare proxy + CNAME to yourname.github.io).

## Posting
- Copy `/posts/first-post.html` and rename it, e.g. `2025-11-06-my-topic.html`.
- Edit the title inside and the date in both the `<title>` and the `<meta name="date">` tag, and in the visible "Published" line.
- Update the posts list in `/index.html` and add a new `<li>` link.
- Optionally update `/feed.xml` with a new `<item>` so RSS readers pick it up.

## Style
- Edit `/assets/style.css` to tweak look and spacing.

## Why no generator?
- Zero dependencies, zero build. You can add Hugo/Jekyll later if you want auto indexes and Markdown.