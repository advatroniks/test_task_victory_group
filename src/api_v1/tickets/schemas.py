from datetime import date

from pydantic import BaseModel


class TicketsOptionsSchema(BaseModel):
    date: date
