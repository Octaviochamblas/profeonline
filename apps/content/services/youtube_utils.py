import re
from urllib.parse import parse_qs, urlparse

def extract_playlist_id(value):
    """
    Normalizes a YouTube playlist input.
    - If it's a URL, tries to extract the 'list' query parameter.
    - If the URL doesn't contain a 'list' parameter, returns empty string.
    - If it's not a URL (no slashes, protocol or www prefix), validates and returns it as a manual ID.
    - Otherwise, returns an empty string.
    """
    if not value:
        return ""
    val = value.strip()
    # If it looks like a URL
    if "://" in val or val.startswith("www.") or "/" in val:
        try:
            if "://" not in val:
                url_to_parse = "https://" + val
            else:
                url_to_parse = val
            parsed = urlparse(url_to_parse)
            query = parse_qs(parsed.query)
            if query.get("list"):
                return query["list"][0]
            return ""  # URL without 'list' parameter is invalid
        except Exception:
            return ""
    # Manual ID (alphanumeric/dashes/underscores, no spaces, no slashes)
    if val and not re.search(r"[\s/]", val):
        return val
    return ""
