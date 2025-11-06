# Rabbit & Wolf — Static Website Starter

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
Run the script
python new_post.py "title" --summary "summary" --tags "tags,tags"

## Style
- Edit `/assets/style.css` to tweak look and spacing.

## Why no generator?
- Zero dependencies, zero build. You can add Hugo/Jekyll later if you want auto indexes and Markdown.
