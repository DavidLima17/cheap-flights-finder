class FlightData:
    # This class is responsible for structuring the flight data.
    def __init__(self, price, origin_city, origin_airport, destination_city,
                 destination_airport, out_date, return_date, stop_overs=0, via_city=""):
        """
        Object of flight data
        :param price: string price of the trip
        :param origin_city: string origin city name
        :param origin_airport: string origin airport iata code
        :param destination_city: string destination city name
        :param destination_airport: string destination iata code
        :param out_date: string start trip date
        :param return_date: string return trip date
        :param stop_overs: int for trip stop-overs default 0
        :param via_city: string for stop over city default empty string
        """
        self.price = price
        self.origin_city = origin_city
        self.origin_airport = origin_airport
        self.destination_city = destination_city
        self.destination_airport = destination_airport
        self.out_date = out_date
        self.return_date = return_date
        self.stop_overs = stop_overs
        self.via_city = via_city
