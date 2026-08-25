"""
Fetches all episodes for the show from Spotify's public Web API using the
client-credentials flow (no user login required, since the show is public).

Requires SPOTIFY_CLIENT_ID and SPOTIFY_CLIENT_SECRET as environment
variables. Writes data/episodes_raw.json.
"""
import json
import os
import time
import urllib.parse
import urllib.request
from pathlib import Path

SHOW_ID = "7Ds6zNqDJBLRcWucjkXALj"
ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data"


def get_token():
    client_id = os.environ["SPOTIFY_CLIENT_ID"]
    client_secret = os.environ["SPOTIFY_CLIENT_SECRET"]
    data = urllib.parse.urlencode({
        "grant_type": "client_credentials",
        "client_id": client_id,
        "client_secret": client_secret,
    }).encode()
    req = urllib.request.Request("https://accounts.spotify.com/api/token", data=data)
    with urllib.request.urlopen(req) as resp:
        return json.load(resp)["access_token"]


def fetch_all_episodes(token):
    episodes = []
    offset = 0
    limit = 50
    while True:
        url = (f"https://api.spotify.com/v1/shows/{SHOW_ID}/episodes"
               f"?market=US&limit={limit}&offset={offset}")
        req = urllib.request.Request(url, headers={"Authorization": f"Bearer {token}"})
        with urllib.request.urlopen(req) as resp:
            data = json.load(resp)
        episodes.extend(data.get("items", []))
        if data.get("next") is None:
            break
        offset += limit
        time.sleep(0.1)
    return episodes


def main():
    token = get_token()
    episodes = fetch_all_episodes(token)

    out = []
    for ep in episodes:
        out.append({
            "name": ep.get("name"),
            "description": ep.get("description"),
            "html_description": ep.get("html_description"),
            "release_date": ep.get("release_date"),
            "url": ep.get("external_urls", {}).get("spotify"),
            "id": ep.get("id"),
            "duration_ms": ep.get("duration_ms"),
        })

    DATA_DIR.mkdir(exist_ok=True)
    (DATA_DIR / "episodes_raw.json").write_text(json.dumps(out, indent=2, ensure_ascii=False))
    print(f"Fetched {len(out)} episodes.")


if __name__ == "__main__":
    main()
