class FlightData:
    #This class is responsible for structuring the flight data.
    def __init__(self, price, origin, destination, out_date, return_date, stops):
        self.price = price
        self.origin_airport = origin
        self.destination_airport = destination
        self.out_date = out_date
        self.return_date = return_date
        self.stops = stops


def find_cheapest_flight(data, return_date):
    # Handle empty data if no flights is returned.
    if data is None or (not data.get("best_flights") and not data.get("other_flights")):
        print("No flight data")
        return FlightData("N/A", "N/A", "N/A", "N/A", "N/A","N/A")
    


    all_flights = data.get("best_flights", []) + data.get("other_flights", [])


    # DATA from the first flight in the list
    first_flight = all_flights[0]

    lowest_price = first_flight['price']
    origin_airport = first_flight['flights'][0]['departure_airport']['id']
    destination_airport = first_flight['flights'][-1]['arrival_airport']['id']
    out_date = first_flight['flights'][0]['departure_airport']['time'].split(" ")[0]


    # A flight with 2 segments will have 1 stop
    nr_stops = len(first_flight["flights"]) - 1

    # Create an Flight_data object with Initial data
    cheapest_flight = FlightData(lowest_price, origin_airport, destination_airport, out_date, return_date, nr_stops)


    for flight in all_flights:
        try:
            price = flight['price']
        except KeyError:
            print("-----No price available for flight.-----")
            continue
        if price < lowest_price:
            lowest_price = price
            origin_airport = flight['flights'][0]['departure_airport']['id']
            destination_airport = flight['flights'][-1]['arrival_airport']['id']
            out_date = flight['flights'][0]['departure_airport']['time'].split(" ")[0]
            cheapest_flight = FlightData(lowest_price, origin_airport, destination_airport, out_date, return_date, nr_stops)
            nr_stops =  len(first_flight["flights"]) - 1
    
    print(f"Lowest Price to {destination_airport} is INR {lowest_price}")
    return cheapest_flight
