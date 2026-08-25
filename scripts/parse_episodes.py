"""
Parses raw Spotify episode data and tags each episode with the Parsha(s)
or holiday it covers, using the canonical alias table in parsha_data.py.

Input:  data/episodes_raw.json  (raw Spotify API episode objects)
Output: data/episodes.json      (grouped + tagged data for the dashboard)
        data/unmatched.json     (episodes that couldn't be confidently tagged)
"""
import json
import re
import unicodedata
from datetime import datetime, timezone
from html.parser import HTMLParser
from pathlib import Path

from parsha_data import (
    PARSHIYOT,
    HOLIDAYS,
    MANUAL_OVERRIDES,
    MANUAL_HOLIDAY_OVERRIDES,
    EXCLUDED_EPISODES,
)

ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data"

EXTRA_HOLIDAY_KEYWORDS = {
    "etrog": "Sukkot",
    "lulav": "Sukkot",
    "shofar": "Rosh Hashanah",
}


class DescriptionSanitizer(HTMLParser):
    """Allowlist-based sanitizer: keeps only <a href="http(s)://...">,
    <p>, and <br> tags from Spotify's html_description field; everything
    else is stripped or HTML-escaped."""

    ALLOWED_TAGS = {"a", "p", "br"}

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.out = []

    def handle_starttag(self, tag, attrs):
        if tag not in self.ALLOWED_TAGS:
            return
        if tag == "a":
            href = dict(attrs).get("href", "")
            if href.startswith("http://") or href.startswith("https://"):
                safe_href = href.replace('"', "%22")
                self.out.append(f'<a href="{safe_href}" target="_blank" rel="noopener noreferrer">')
        elif tag == "p":
            self.out.append("<p>")
        elif tag == "br":
            self.out.append("<br>")

    def handle_endtag(self, tag):
        if tag in self.ALLOWED_TAGS and tag != "br":
            self.out.append(f"</{tag}>")

    def handle_data(self, data):
        escaped = (data.replace("&", "&amp;").replace("<", "&lt;")
                   .replace(">", "&gt;"))
        self.out.append(escaped)

    def get_html(self):
        return "".join(self.out).strip()


def sanitize_description(html_description: str, plain_fallback: str) -> str:
    if not html_description:
        escaped = (plain_fallback or "").replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
        return escaped
    parser = DescriptionSanitizer()
    parser.feed(html_description)
    result = parser.get_html()
    return result or (plain_fallback or "")


def normalize(text: str) -> str:
    text = unicodedata.normalize("NFKD", text)
    text = text.replace("’", "'").replace("‘", "'")
    text = text.lower()
    text = text.replace("'", "").replace('"', "")
    text = re.sub(r"[^a-z0-9]+", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def build_alias_index():
    index = {}
    for canonical, aliases in PARSHIYOT:
        for a in [canonical] + aliases:
            index[normalize(a)] = ("parsha", canonical)
    for canonical, aliases in HOLIDAYS:
        for a in [canonical] + aliases:
            index[normalize(a)] = ("holiday", canonical)
    return index


ALIAS_INDEX = build_alias_index()
PARSHA_ORDER = [name for name, _ in PARSHIYOT]
HOLIDAY_ORDER = [name for name, _ in HOLIDAYS]

EDITION_NOISE_WORDS = {
    "full", "bonus", "edition", "devash", "uncut", "special", "remix", "retold",
}


def lookup(token: str):
    norm = normalize(token)
    if not norm:
        return None
    if norm in ALIAS_INDEX:
        return ALIAS_INDEX[norm]
    # try trimming trailing noise words one at a time (e.g. "vayeshev full bonus edition")
    words = norm.split(" ")
    while words and words[-1] in EDITION_NOISE_WORDS:
        words = words[:-1]
        trimmed = " ".join(words)
        if trimmed in ALIAS_INDEX:
            return ALIAS_INDEX[trimmed]
    return None


def extract_head(name: str) -> str:
    """Return the portion of the title likely to contain the Parsha/holiday name."""
    m = re.match(r"^Parsha Stories\s*\((.*)\)\s*$", name.strip(), re.IGNORECASE)
    if m:
        inner = m.group(1).strip()
        m2 = re.match(r"^Sefer\s+\S+-(.*)$", inner, re.IGNORECASE)
        if m2:
            return m2.group(1).strip()
        # Some episodes drop the word "Sefer" but keep the book name as a
        # prefix (e.g. "Shemot-Ki Tisa" meaning "[Sefer] Shemot: Ki Tisa",
        # not a Shemot+Ki Tisa combo reading). Strip a leading book name.
        book_names = r"(bereishit|bereshit|bereisheit|shemot|shmot|vayikra|bamidbar|bemidbar|devarim)"
        m3 = re.match(rf"^{book_names}-(.+)$", inner, re.IGNORECASE)
        if m3:
            return m3.group(2).strip()
        return inner

    # Split off a catchy subtitle after " - ", ": ", or "*"
    for sep in [" - ", ": ", " * "]:
        if sep in name:
            return name.split(sep, 1)[0].strip()
    return name.strip()


def split_combo(head: str):
    # combiners used across the dataset
    for combiner in ["/", " and ", " & ", "-"]:
        if combiner in head:
            parts = [p.strip() for p in head.split(combiner) if p.strip()]
            if len(parts) > 1:
                return parts
    return [head]


def tag_episode(ep: dict):
    name = ep["name"]

    if name in MANUAL_OVERRIDES:
        return [("parsha", p) for p in MANUAL_OVERRIDES[name]]

    if name in MANUAL_HOLIDAY_OVERRIDES:
        return [MANUAL_HOLIDAY_OVERRIDES[name]]

    head = extract_head(name)
    parts = split_combo(head)

    tags = []
    all_matched = True
    for part in parts:
        result = lookup(part)
        if result:
            tags.append(result)
        else:
            all_matched = False
            break

    if all_matched and tags:
        return tags

    # Fallback: search the whole title for any known alias or holiday keyword,
    # in case the head-based split failed but a name is present in the subtitle.
    norm_full = normalize(name)
    for keyword, holiday in EXTRA_HOLIDAY_KEYWORDS.items():
        if keyword in norm_full:
            return [("holiday", holiday)]

    for alias_norm, (kind, canonical) in ALIAS_INDEX.items():
        if len(alias_norm) > 3 and re.search(rf"\b{re.escape(alias_norm)}\b", norm_full):
            return [(kind, canonical)]

    return []


def main():
    episodes = json.loads((DATA_DIR / "episodes_raw.json").read_text())

    parshiot = {name: [] for name in PARSHA_ORDER}
    holidays = {name: [] for name in HOLIDAY_ORDER}
    unmatched = []

    for ep in episodes:
        if ep["name"] in EXCLUDED_EPISODES:
            continue
        tags = tag_episode(ep)
        record = {
            "title": ep["name"],
            "description": sanitize_description(ep.get("html_description"), ep.get("description")),
            "release_date": ep["release_date"],
            "url": ep["url"],
            "id": ep["id"],
        }
        if not tags:
            unmatched.append(record)
            continue
        for kind, canonical in tags:
            if kind == "parsha":
                parshiot[canonical].append(record)
            else:
                holidays[canonical].append(record)

    # sort each group's episodes newest first
    for group in list(parshiot.values()) + list(holidays.values()):
        group.sort(key=lambda r: r["release_date"], reverse=True)

    output = {
        "parshiot": {k: v for k, v in parshiot.items() if v},
        "parsha_order": PARSHA_ORDER,
        "holidays": {k: v for k, v in holidays.items() if v},
        "holiday_order": HOLIDAY_ORDER,
        "generated_at": datetime.now(timezone.utc).isoformat(),
    }

    (DATA_DIR / "episodes.json").write_text(json.dumps(output, indent=2, ensure_ascii=False))
    (DATA_DIR / "unmatched.json").write_text(json.dumps(unmatched, indent=2, ensure_ascii=False))

    total_tagged = sum(len(v) for v in parshiot.values()) + sum(len(v) for v in holidays.values())
    print(f"Tagged {total_tagged} episode-tags across {len(output['parshiot'])} parshiot "
          f"and {len(output['holidays'])} holidays.")
    print(f"Unmatched: {len(unmatched)}")
    for u in unmatched:
        print("  -", u["title"])


if __name__ == "__main__":
    main()
