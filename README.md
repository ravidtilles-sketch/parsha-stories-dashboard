# Parsha Stories Dashboard

A searchable dashboard for the [Parsha Stories podcast](https://open.spotify.com/show/7Ds6zNqDJBLRcWucjkXALj) — type in a Parsha (or holiday) and get every episode ever recorded about it, with its blurb and a direct Spotify link.

## How it stays up to date

A GitHub Action (`.github/workflows/update.yml`) runs daily, re-fetches the episode list from Spotify's public API, re-tags each episode by Parsha/holiday, and commits the refreshed `data/episodes.json`. GitHub Pages serves whatever is on `main`, so the live site updates automatically within a few minutes of a new episode going up on Spotify.

You can also trigger it manually from the repo's **Actions** tab → "Update episode data" → **Run workflow**.

## Local development

```bash
export SPOTIFY_CLIENT_ID=...
export SPOTIFY_CLIENT_SECRET=...
python3 scripts/fetch_episodes.py   # pulls data/episodes_raw.json from Spotify
python3 scripts/parse_episodes.py   # writes data/episodes.json
python3 -m http.server 8765         # then open http://localhost:8765
```

## Fixing a mis-tagged episode

Parsha/holiday tagging is inferred from episode titles using the alias table in `scripts/parsha_data.py`. If a new episode title doesn't match anything, `scripts/parse_episodes.py` will print it as unmatched and it won't appear on the dashboard — add an alias, a `MANUAL_OVERRIDES` entry, or a `MANUAL_HOLIDAY_OVERRIDES` entry there to fix it.

## Embedding on another website

Once the site is live at `https://<username>.github.io/<repo-name>/`, embed it anywhere with an iframe:

```html
<iframe src="https://<username>.github.io/<repo-name>/" style="width:100%; height:800px; border:none;"></iframe>
```
