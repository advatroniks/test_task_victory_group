from random import randint, choice
from datetime import datetime, timedelta


MOST_POPULAR_AIRPORTS = [
    "URSS",
    "UUDD",
    "UUEE",
    "UUWW",
    "UUDD",
    "UUEE",
    "UUWW",
    "UUDD",
    "UUEE",
    "UUWW",
    "UUDD",
    "UUEE",
    "UUWW",
    "USSS",
    "UWWW",
    "ULLI",
    "ULLI",
    "ULLI",
    "UNNT",
]


def get_random_airport():
    return choice(MOST_POPULAR_AIRPORTS)


def create_flight_no():
    icao_airlines_code = [
        "AFL",  # Aeroflot (Россия)
        "SBI",  # S7 Airlines (Россия)
        "UTA",  # UTair (Россия)
        "AUI",  # International Airlines of Ukraine (Украина)
        "WRC",  # Windrose Airlines (Украина)
        "MSI",  # Motor Sich Airlines (Украина)
        "KZR",  # Air Astana (Казахстан)
        "VSV",  # SCAT Airlines (Казахстан)
        "KZQ",  # Qazaq Air (Казахстан)
        "BRU",  # Belavia (Беларусь)
        "NGT",  # Aircompany Armenia (Армения)
        "TGZ",  # Georgian Airways (Грузия)
        "SMR",  # Somon Air (Таджикистан)
        "UZB",  # Uzbekistan Airways (Узбекистан)
        "TUA",  # Turkmenistan Airlines (Туркменистан)
        "BAW",  # British Airways (Великобритания)
        "LH",   # Lufthansa (Германия)
        "AFR",  # Air France (Франция)
        "RYR",  # Ryanair (Ирландия)
        "AEA",  # Aer Lingus (Ирландия)
        "DLH",  # Condor (Германия)
        "ETD",  # Etihad Airways (ОАЭ)
        "QTR",  # Qatar Airways (Катар)
        "EK",   # Emirates (ОАЭ)
    ]

    random_airline_code = icao_airlines_code[randint(0, len(icao_airlines_code) - 1)]
    random_flight_number = randint(1, 2000)

    return f"{random_airline_code}{random_flight_number}"


def create_random_flight_time():
    probability = randint(0, 100)
    minutes = randint(0, 60)
    if probability >= 95:
        hours = randint(5, 8)
    elif probability >= 70:
        hours = randint(2, 4)
    elif probability >= 20:
        hours = 1
    else:
        hours = 0
        minutes = randint(40, 59)

    flight_time = timedelta(hours=hours, minutes=minutes)

    scheduled_departure = datetime.utcnow() + timedelta(
        days=randint(1, 365),
        hours=randint(0, 23),
        minutes=randint(0, 60)
    )

    scheduled_arrival = scheduled_departure + flight_time

    return scheduled_departure, scheduled_arrival
