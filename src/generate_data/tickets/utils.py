from random import randint


def create_random_available_tickets_in_flight():
    probability = randint(0, 100)
    if probability >= 95:
        passengers = randint(1, 2)
    elif probability >= 70:
        passengers = randint(4, 5)
    elif probability >= 20:
        passengers = randint(5, 8)
    else:
        passengers = randint(8, 12)

    return passengers


def create_random_price_for_ticket():
    price = randint(3500, 7500)
    probability = randint(0, 100)
    if probability >= 95:
        return "first", price * 4
    if probability >= 80:
        return "business", price * 2
    else:
        return "economy", price



