class ErrorCode:
    """
    Константы для описания конкретных исключений.
    """
    RouteNotExist = "The route does not exist even with transfers, try change data"
    NotAvailableTickets = "There are no tickets available for the current date"
    AirportNotExist = "There is no airport with such ICAO CODE!! Try again"
