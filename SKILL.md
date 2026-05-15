---
name: ita-matrix-skill
description: >
  Build ITA Matrix flight search links from natural language requests.
  Use this skill whenever the user wants to search for flights, find airfare,
  or build an ITA Matrix search URL. Triggers include: any city-pair flight
  request ("Shanghai to LA", "上海到洛杉矶"), "find me a flight", "search flights",
  "ITA Matrix", "book a ticket", "查机票", "搜索机票", or any request mentioning
  departure/destination cities with travel dates. Always use this skill even if
  the user just names two cities without explicitly asking for a search link.
---

## Overview

Turn a natural-language flight request into a working ITA Matrix search link.

---

## Workflow

### Step 1: Extract parameters

Run `python3 scripts/parse_flight_request.py "<user request>"` to extract structured parameters.

If `missing` or `ambiguous` fields are non-empty in the output, ask the user to clarify before proceeding. Keep it to one question covering all missing fields at once.

Parameters needed:
- Origin and destination (IATA codes or city names)
- Departure date
- Return date (round trip only)
- Trip type: one-way / round-trip
- Cabin class (default: economy)
- Number of passengers (default: 1 adult)

If the user gives a city with multiple airports (e.g. New York = JFK/EWR/LGA, Shanghai = PVG/SHA), use the main international hub by default and mention it in the summary.

### Step 2: Build the link

Run `python3 scripts/build_ita_search.py` with the extracted parameters:

```bash
python3 scripts/build_ita_search.py \
  --origin <IATA> \
  --dest <IATA> \
  --date <YYYY-MM-DD> \
  [--return-date <YYYY-MM-DD>] \
  [--cabin economy|premium_economy|business|first] \
  [--passengers <N>]
```

### Step 3: Return the link

Present the output from the script directly. The script already formats a summary — just pass it through to the user.

If the user's city resolved to a specific airport (e.g. "上海" → PVG 浦东), mention it so they can correct if needed.
