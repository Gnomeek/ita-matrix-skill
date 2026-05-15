type Bool = "true" | "false"

type Params = {
	type: "one-way" | "round-trip"
	slice: FlightSegement[]
	options: SearchOption
	pax: Pax
}

type FlightSegement = {
	origin: string[] // list of IATA code for destination, e.g., PVG
	dest: string[] // list of IATA code for destination, e.g., LAX
	routing: string // routing code for outward trip
	ext: string // extension code for outward trip
	routingRet: string // routing code for return trip
	extRet: string // extension code for return trip
	dates: FlightDate
}

type FlightDate =
	| FlightDateBase & {
		searchDateType: "calendar",
		duration: string, // 7 - 10
	}
	| FlightDateBase & {
		searchDateType: "specific",
		returnDate: string
	}

type FlightDateBase = {
	departureDate: string,
	departureDateType: "depart" | "arrival", 
	departureDateModifier: "11",
	departureDatePreferredTimes: [],
	returnDateType: "depart" | "arrival",
	returnDateModifier: "10",
	returnDatePreferredTimes: []
}

type SearchOption = {
	cabin: "COACH" | "PREMIUM-COACH" | "BUSINESS" | "FIRST",
	stops: string,
	extraStops: string,
	allowAirportChanges: Bool,
	showOnlyAvailable: Bool
}

type Pax = {
	// adult: 18-61, senior: 62+, youth: 12-17, children: 2-11, infant: <2
	adults: string // number in string fmt
	seniors: string // number in string fmt
	youth: string // number in string fmt
	infantsInLap: string // number in string fmt
	infantsInSeat: string // number in string fmt
	children: string // number in string fmt
}