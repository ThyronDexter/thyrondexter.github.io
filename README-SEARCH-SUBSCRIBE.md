
# Rabbit & Wolf — Search + Subscribe Add‑On

Adds:
- `/search.html` + `/assets/search.js` + `/assets/search.css`
- `/search_index.json`
- `/subscribe.html` with Buttondown/Substack

## Install
1) Upload all files to your repo (keep folders).
2) Add nav links in `index.html` (and `about.html` if you like):
   ```html
   <a href="/search.html">Search</a>
   <a href="/subscribe.html">Subscribe</a>
   ```

## Search index
Edit `/search_index.json` and add an entry per post:
```json
{
  "title": "My Post",
  "url": "/posts/2025-11-07-my-post.html",
  "date": "2025-11-07",
  "date_iso": "2025-11-07",
  "summary": "One‑sentence summary.",
  "tags": ["rpg","design"],
  "content": "Add 50–200 words excerpt for search."
}
```
Keep the JSON under ~2MB for speed.

## Email subscriptions
- **Buttondown**: replace `your-buttondown-username` in `/subscribe.html` (both places).
- **Substack**: replace `your-substack` in the iframe src.

## Tip
After edits, do a hard reload (Ctrl/Cmd+Shift+R) to bust cache.
