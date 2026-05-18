# Itinerary
| Syntax | Example | Meaning |
| :--- | :--- | :--- |
| **`-CODESHARE`** | `-CODESHARE` | Disallow codeshares |
| **`MAXSTOPS n`** | `MAXSTOPS 2` | Set a limit on the number of stops on this portion of the trip. |
| **`MAXDUR hh:mm`** | `MAXDUR 6:45` | Set a limit on the duration of this portion of the trip. |
| **`MAXMILES n`** | `MAXMILES 2900` | Set a cap on the number of miles flown on this portion of the trip. |
| **`MINMILES n`** | `MINMILES 2600` | Set a floor on the number of miles flown on this portion of the trip. |
| **`MINCONNECT hh:mm`** | `MINCONNECT 1:00` | Set a minimum connection time. |
| **`MAXCONNECT hh:mm`** | `MAXCONNECT 2:00` | Set a maximum length of connection time. |
| **`ALLIANCE code1 code2 ...`** | `ALLIANCE star-alliance` | Permit only flights on these carriers in this alliance (or alliances). Separate multiple alliances with spaces. Supported alliances are `oneworld`, `skyteam`, and `star-alliance`. |
| **`-AIRLINES code1 code2 ...`** | `-AIRLINES AA BA` | Prohibit flights on the specified carriers. |
| **`AIRLINES code1 code2 ...`** | `AIRLINES BA AF` | Allow only flights on the specified carriers. |
| **`OPAIRLINES code1 code2 ...`** | `OPAIRLINES AA` | Allow only flights operated by these carriers (no matter the marketing carrier). |
| **`-OPAIRLINES code1 code2 ...`** | `-OPAIRLINES AA` | Prohibit flights operated by these carriers (no matter the marketing carrier). |
| **`-CITIES code1 code2 ...`** | `-CITIES DFW ORD` | Prohibit connections at these cities. |
| **`-REDEYES`** | `-REDEYES` | Prohibit overnight flights. |
| **`-OVERNIGHTS`** | `-OVERNIGHTS` | Prohibit solutions requiring overnight stops. |
| **`AIRCRAFT aircraft1 aircraft2`** | `AIRCRAFT T:737 C:PROP` | Allow flights on the listed equipment types (prefixed with `T:`) or categories (prefixed with `C:`). Categories include `C:JET`, `C:TURBOPROP`, `C:PISTON`, `C:TRAIN`, `C:HELICOPTER`, `C:AMPHIBIAN`, and `C:SURFACE`. For the list of equipment types see the Aircraft Types tab. This code may be negated to prohibit the listed aircraft types and categories. |
| **`-PROPS`** | `-PROPS` | Prohibit flights on propeller planes. |
| **`-NOFIRSTCLASS`** | `-NOFIRSTCLASS` | All flights must have a first class cabin (though flights may still be booked in another cabin) |

> Codes in this field apply only to this segment of this trip. Multiple commands can be separated with a semicolon.

# Faring
| Syntax | Example | Meaning |
| :--- | :--- | :--- |
| **`+CABIN code1 code2 ...`** | `+CABIN 1` | Require booking in the specified cabin classes. For first class, use `1`; for second (or business), use `2`; for premium economy, use `premium-coach` or `pe`; and for economy, use `3`. |
| **`-CABIN code1 code2 ...`** | `-CABIN 3` | Prohibit booking in the specified cabin classes. See `+CABIN` for what codes to use for each cabin class. |
| **`F BC=code`** | `F bc=y` | Use fares with the specified prime booking code. Note: the actual booking class used may be different due to being overridden by the carrier's booking code exception table. |
| **`F BC=code\|BC=code\|...`** | `F bc=y\|bc=b` | Specify that fares use one of several prime booking codes (e.g. book in either Y or B class). See the note on the above item. |
| **`F carrier.city1+city2.farebasis`** | | Specify which fares to use. Multiple alternate fare specifications can be separated by a vertical bar. See below for specific examples. |
| **`F CC.AAA+BBB.FFFFFFF`** | `F aa.lon+chi.yup` | Specify carrier, market (city pair), and fare basis code of the fares to use (e.g. only AA LON-CHI YUP fares). |
| **`F ..FFFFFFF`** | `F ..yup\|..f` | Specify the fare code (but not carrier or market) of the fare to use (e.g. either YUP or F fares on any airline and between any city pairs). |
| **`F .AAA+BBB.`** | `F .lon+chi.` | Specify the market (city pair) for the fares (e.g. use only LON-CHI through fares). |
| **`F CC..FFFFFFF`** | `F aa..yup\|aa..f` | Specify the carrier and fare basis code, but not the market (e.g. use either YUP or F fares on AA for any city pair). |
| **`F ..F-`** | `F ..y-\|..b-` | Specify the fare basis using "wildcards" (e.g. only use fare bases that start with either Y or B). |
> Codes in this field apply only to this segment of this trip. Multiple commands can be separated with a semicolon.