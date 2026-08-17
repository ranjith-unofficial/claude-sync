#!/usr/bin/env python3
"""
wger_search.py — Search wger's exercise database by name.

Usage:
  python3 wger_search.py "bench press"
  python3 wger_search.py "squat"

The API's old /api/v2/exercise/search/?term= endpoint returns 404 on the
current wger API (confirmed dead, not a typo — there's no route left named
"search" in the API root listing). There is also no working server-side
fuzzy-search filter on any list endpoint: `?name=` on exercise-translation
is an exact, case-sensitive full-string match (returns 0 results for a
partial query), and unsupported query params like `?search=` or `?term=`
are silently ignored rather than erroring, which looks like it worked but
just returns the unfiltered full list.

The only correct approach left is to paginate the full exercise-translation
list (wger caps at 999 results/page regardless of requested limit — a
`limit=5000` request still returns exactly 999) and filter client-side.
~3,300 entries total = 4 requests, a few seconds.

No external dependencies — stdlib only.
"""
import sys
import json
import urllib.request

BASE = "https://wger.de/api/v2"


def fetch(url):
    req = urllib.request.Request(url, headers={"Accept": "application/json"})
    with urllib.request.urlopen(req, timeout=15) as r:
        return json.loads(r.read())


def search(term, language=2, max_matches=200):
    term_lower = term.lower()
    matches = []
    url = f"{BASE}/exercise-translation/?language={language}&limit=999&format=json"
    while url and len(matches) < max_matches:
        data = fetch(url)
        for item in data.get("results", []):
            name = item.get("name", "")
            if term_lower in name.lower():
                matches.append({"exercise_id": item["exercise"], "name": name})
        url = data.get("next")
    return matches


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    term = sys.argv[1]
    matches = search(term)

    if not matches:
        print(f"No exercises found matching '{term}'.")
        return

    # Same exercise can have multiple language/regional-name translations —
    # de-dupe by exercise_id, keeping the first (usually canonical) name.
    seen = set()
    deduped = []
    for m in matches:
        if m["exercise_id"] not in seen:
            seen.add(m["exercise_id"])
            deduped.append(m)

    print(f"Found {len(deduped)} exercises matching '{term}' (showing up to 10):")
    for m in deduped[:10]:
        print(f"  exercise ID {m['exercise_id']:>5} | {m['name']}")

    if deduped:
        print(f"\nFor full details on any result: GET {BASE}/exerciseinfo/{{exercise_id}}/?format=json")


if __name__ == "__main__":
    main()
