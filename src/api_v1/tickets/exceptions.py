from src.exceptions import NotFound
from src.api_v1.tickets.constants import ErrorCode


class RouteNotExist(NotFound):
    DETAIL = ErrorCode.RouteNotExist
