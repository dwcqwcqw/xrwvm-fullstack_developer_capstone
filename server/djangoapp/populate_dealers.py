import json
from .models import CarDealer


def populate():
    """Populate the database with dealer data."""
    dealers_data = [
        {
            "id": 1,
            "city": "Toronto",
            "state": "ON",
            "st": "ON",
            "address": "27 Queens Quay E",
            "zip": "M5E 1B4",
            "lat": 43.6426166,
            "long": -79.3740268,
            "short_name": "Toronto Dealer",
            "full_name": "Toronto Car Dealership"
        },
        {
            "id": 2,
            "city": "Markham",
            "state": "ON",
            "st": "ON",
            "address": "8111 Kennedy Road",
            "zip": "L3R 0C4",
            "lat": 43.8561,
            "long": -79.3047,
            "short_name": "Markham Dealer",
            "full_name": "Markham Car Dealership"
        },
        {
            "id": 3,
            "city": "Vancouver",
            "state": "BC",
            "st": "BC",
            "address": "701 W Georgia St",
            "zip": "V7Y 1G5",
            "lat": 49.2827,
            "long": -123.1207,
            "short_name": "Vancouver Dealer",
            "full_name": "Vancouver Car Dealership"
        }
    ]

    for dealer in dealers_data:
        CarDealer.objects.create(**dealer)

    print("Database populated with dealer data successfully.") 