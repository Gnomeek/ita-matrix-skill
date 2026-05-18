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

Turn a natural-language flight request into a working ITA Matrix search link by constructing a `Params` object, encoding it as base64, and appending it to the base URL.

---

## Params Type

```typescript
type Bool = "true" | "false";

type Params = {
  type: "one-way" | "round-trip";
  slice: FlightSegment[];
  options: SearchOption;
  pax: Pax;
};

type FlightSegment = {
  origin: string[];        // IATA codes, e.g. ["PVG"]
  dest: string[];          // IATA codes, e.g. ["LAX"]
  routing: string;         // routing code for outward trip — see Routing Code reference
  routingRet: string;      // routing code for return trip — see Routing Code reference
  extRet: string;          // extension code for return trip — see Extension Code reference
  dates: FlightDate;
};

type FlightDate =
  | (FlightDateBase & {
      searchDateType: "calendar";
      duration: string;    // e.g. "7 - 10" (min-max nights)
    })
  | (FlightDateBase & {
      searchDateType: "specific";
      returnDate: string;  // YYYY-MM-DD
    });

type FlightDateBase = {
  departureDate: string;              // YYYY-MM-DD
  departureDateType: "depart" | "arrival";
  departureDateModifier: "11";        // fixed value
  departureDatePreferredTimes: [];    // always empty array
  returnDateType: "depart" | "arrival";
  returnDateModifier: "10";           // fixed value
  returnDatePreferredTimes: [];       // always empty array
};

type SearchOption = {
  cabin: "COACH" | "PREMIUM-COACH" | "BUSINESS" | "FIRST";
  stops: "-1" | "0" | "1" | "2";      // -1: no limit, 0: nonstop, 1: up to 1 stop, 2: up to 2 stops
  extraStops: "-1" | "0" | "1" | "2";
  allowAirportChanges: Bool;
  showOnlyAvailable: Bool;
};

type Pax = {
  // age ranges: adult 18-61, senior 62+, youth 12-17, children 2-11, infant <2
  adults: string;
  seniors: string;
  youth: string;
  infantsInLap: string;
  infantsInSeat: string;
  children: string;
};
```

---

## Workflow

### Step 1: Extract parameters

From the user's request, determine:
- Origin / destination (IATA codes; if city has multiple airports use main international hub and mention it, search online for IATA codes if user provides city names, e.g., Shanghai, 上海)
- Departure date; return date or flexible duration
- Trip type: `one-way` or `round-trip`
- Cabin class (default: `COACH`)
- Passengers (default: 1 adult, all others `"0"`)
- Any routing / extension constraints (nonstop, preferred airline, avoid connections, etc.)

If critical fields are missing or ambiguous, ask once covering all gaps before proceeding.

### Step 2: Build the routing / extension codes

Consult the references when the user specifies constraints:

- **`references/routing_code_manual.md`** — controls which flights/airlines/connections are allowed on each segment.
  Common patterns:
  - Nonstop only: `N`
  - Specific carrier: `C:AA`
  - Any carrier, up to one stop: `X?`
  - Leave empty (`""`) for no constraint

- **`references/extension_code_manual.md`** — itinerary-level constraints (max stops, max duration, prohibited cities, cabin requirements, fare basis, etc.).
  Common patterns:
  - Max 1 stop: `MAXSTOPS 1`
  - No redeyes: `-REDEYES`
  - Alliance only: `ALLIANCE star-alliance`
  - Leave empty (`""`) for no constraint

#### Hidden Tricks
- It's possible that `PVG -> ICN -> PVG -> FRA` cheaper than `PVG -> FRA`, always consider adjust origin/destination. 
- If it's acceptable, construct search params with varied origin/destination. For instance, user can depart from a nearby airport. Searching online for nearby airport IATA code.

### Step 3: Construct the Params object and encode

Assemble the `Params` object following the type above, then encode:

```typescript
function generateMatrixSearchUrl(params: Params): string {
  const jsonString = JSON.stringify(params);
  const base64String = btoa(
    encodeURIComponent(jsonString).replace(/%([0-9A-F]{2})/g, (_, p1) => {
      return String.fromCharCode(parseInt(p1, 16));
    }),
  );
  const encodedBase64 = encodeURIComponent(base64String);
  return `https://matrix.itasoftware.com/search?search=${encodedBase64}`;
}
```

### Step 4: Return the link

Present the URL to the user. If any airport was inferred from a city name (e.g. "上海" → PVG), mention it so they can correct if needed.
