# Syntax
| Format Syntax | Definition |
| :--- | :--- |
| **`C:AA`** | Direct flight on specific carrier |
| **`C:AA+`** | One or more flights on specific carrier (see examples tab for other options) |
| **`AA,UA,DL`** | Direct flight on one of carriers specified (`C:` is optional) |
| **`O:AA`** | Direct flight on a specific operating carrier (as opposed to a codeshare or subsidiary carrier) |
| **`O:AA,UA,DL`** | Direct flight operated by AA, UA, or DL |
| **`N`** | Any single nonstop flight |
| **`N:AA`** | Nonstop flight on specific carrier |
| **`X`** | Any single connection point |
| **`X:NYC`** | Connection point |
| **`DFW,STL`** | Connection in one of specified points |
| **`F`** | Any single flight |
| **`F:AA151`** | Specific flight |
| **`?`** | Zero or one flights |
| **`+`** | One or more flights |
| **`*`** | Zero or more flights |
| **`~`** | Negation |

> The `F:`, `C:`, and `X:` prefixes are optional.

# Examples
| Example | Results |
| :--- | :--- |
| **`N`** | Non-stop flight only |
| **`NYC`** | Single stop in New York |
| **`~NYC`** | Single stop, not in New York |
| **`DEN?`** | Direct flight or one stop in Denver |
| **`X?`** | Direct flight or one stop anywhere |
| **`~DEN?`** | Direct flight or one stop anywhere but Denver |
| **`EWR CVG SLC`** | Stops in Newark, Cincinnati, and Salt Lake City |
| **`AA`** | Direct flight on AA (American Airlines) |
| **`AA+`** | Any number of flights on AA |
| **`AA,UA`** | Direct flight on either AA (American) or UA (United Airlines) |
| **`~AA`** | Direct flight, not on AA |
| **`~AA,UA,DL`** | Direct flight, not on AA, UA, or DL |
| **`~AA,UA,DL+`** | Any number of flights not on AA, UA, or DL |
| **`AA+ DL+`** | One or more flights on AA, followed by one or more flights on DL (Delta) |
| **`AA DL,AF`** | Flight on AA followed by flight on either DL or AF |
| **`AA UA?`** | One AA flight, optionally followed by another flight on UA |
| **`AA N?`** | One AA flight, optionally followed by a nonstop flight on any airline |
| **`AA25 UA814`** | Flight AA25 followed by UA814 |
| **`AA25 UA+`** | Flight AA25 followed by one or more flights on UA |
| **`AA25 F+`** | Flight AA25 followed by one or more flights on any airline |
| **`DL CHI DL`** | Two DL flights with a connection in Chicago |
| **`O:UA`** | Single flight, operated by UA (and not any other airline or UA subsidiary carriers) |
| **`~UA882`** | Single flight, but not UA882 |
| **`UA1000-2000+`** | One or more flights on UA with flight numbers in the range 1000-2000 |
| **`~UA5000-9999,AA,DL+`** | One or more flights that are NOT on AA or on DL or on UA with flight numbers between 5000 and 9999 |

# Glossary
| Term | Definition |
| :--- | :--- |
| **Trip** | Your entire travel plan. For a round trip, for example, a trip contains both the outbound and return portions. |
| **Leg** | One takeoff and landing |
| **Flight/Direct flight** | One or more legs, on the same airline, in which each leg has the same flight number |
| **Non-stop flight** | A flight with only one leg |
| **Itinerary** | One or more flights from a passenger-requested origin to a passenger-requested destination |
| **Marketing carrier** | The carrier whose flight number is displayed |
| **Operating carrier** | The carrier whose plane actually operates the flight |