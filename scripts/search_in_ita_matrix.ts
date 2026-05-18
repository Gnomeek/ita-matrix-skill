type Bool = "true" | "false";

type Params = {
  type: "one-way" | "round-trip";
  slice: FlightSegement[];
  options: SearchOption;
  pax: Pax;
};

type FlightSegement = {
  origin: string[]; // list of IATA code for destination, e.g., PVG
  dest: string[]; // list of IATA code for destination, e.g., LAX
  routing: string; // routing code for outward trip, refer to reference/routing_code_manual.md
  //   ext: string; // extension code for outward trip, refer to reference/extension_code_manual.md
  routingRet: string; // routing code for return trip, refer to reference/routing_code_manual.md
  extRet: string; // extension code for return trip, refer to reference/extension_code_manual.md
  dates: FlightDate;
};

type FlightDate =
  | (FlightDateBase & {
      searchDateType: "calendar";
      duration: string; // 7 - 10
    })
  | (FlightDateBase & {
      searchDateType: "specific";
      returnDate: string;
    });

type FlightDateBase = {
  departureDate: string;
  departureDateType: "depart" | "arrival";
  departureDateModifier: "11";
  departureDatePreferredTimes: [];
  returnDateType: "depart" | "arrival";
  returnDateModifier: "10";
  returnDatePreferredTimes: [];
};

type SearchOption = {
  cabin: "COACH" | "PREMIUM-COACH" | "BUSINESS" | "FIRST";
  stops: "-1" | "0" | "1" | "2"; // -1 for no limit, 0 for non stop, 1 for up to 1 stop, 2 for up to 2 stops
  extraStops: "-1" | "0" | "1" | "2"; // -1 for no limit, 0 for non stop, 1 for up to 1 stop, 2 for up to 2 stops
  allowAirportChanges: Bool;
  showOnlyAvailable: Bool;
};

type Pax = {
  // adult: 18-61, senior: 62+, youth: 12-17, children: 2-11, infant: <2
  adults: string; // number in string fmt
  seniors: string; // number in string fmt
  youth: string; // number in string fmt
  infantsInLap: string; // number in string fmt
  infantsInSeat: string; // number in string fmt
  children: string; // number in string fmt
};

function generateMatrixSearchUrl(params: Params): string {
  const jsonString = JSON.stringify(params);
  const base64String = btoa(
    encodeURIComponent(jsonString).replace(/%([0-9A-F]{2})/g, (_, p1) => {
      return String.fromCharCode(parseInt(p1, 16));
    }),
  );
  const encodedBase64 = encodeURIComponent(base64String);

  const baseUrl = "https://matrix.itasoftware.com/search?search=";
  return `${baseUrl}${encodedBase64}`;
}
