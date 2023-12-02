from src.exceptions import NotFound
from src.api_v1.tickets.constants import ErrorCode


class RouteNotExist(NotFound):
    DETAIL = ErrorCode.RouteNotExist


class NotAvailableTickets(NotFound):
    DETAIL = ErrorCode.NotAvailableTickets


class AirportNameError(NotFound):
    DETAIL = ErrorCode.AirportNotExist
