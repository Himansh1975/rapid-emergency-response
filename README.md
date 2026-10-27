# Rapid Emergency Response Plumbing website

Live at https://rapidemergencyresponse.co.uk. Runs as the Cloudflare Worker `rapid-emergency-response`.

## What's where

| Path | What it is |
|---|---|
| `public/index.html` | The home page |
| `public/privacy.html` | Privacy policy, served at `/privacy` |
| `public/plumber-*.html` | One page per area (Batley, Morley…), served at `/plumber-morley` etc. |
| `public/*-repair.html`, `emergency-plumber.html`, `sink-plumbing.html` | One page per service |
| `public/styles.css` | Styles shared by every page |
| `tools/build_pages.py` | Generates the area and service pages and `sitemap.xml`. Edit the wording there, then run `python3 tools/build_pages.py` |
| `public/img/` | Photos and logo. Keep these file names: the page refers to them |
| `public/robots.txt`, `public/sitemap.xml` | For Google |
| `src/index.js` | Tiny Worker that sends `www.` and `http://` visitors to `https://rapidemergencyresponse.co.uk` |
| `wrangler.jsonc` | Cloudflare settings |

## Making a change

1. Edit the file (usually `public/index.html`).
2. Push to a branch other than `main`. Cloudflare builds a preview link you can send Ryan.
3. When it looks right, merge into `main`. That deploys to the live site within a minute or two.

To undo a change, revert the commit on `main`, or roll back to an earlier version in Cloudflare (Workers & Pages → rapid-emergency-response → Deployments).

## Deploying by hand (fallback)

```
npx wrangler deploy
```

## Notes

- The contact form doesn't send anything to a server. It opens WhatsApp with the message filled in. That's deliberate: nothing to break, and no data stored.
- The privacy page mentions Cloudflare Web Analytics. It's switched on in the Cloudflare dashboard, not in this code.
- Rebuilt on 27 Oct 2026 from the version that was live, because the original files had been lost.
