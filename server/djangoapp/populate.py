from .models import CarMake, CarModel
from datetime import datetime


def initiate():
    """Initialize the database with sample car makes and models."""
    # Create car makes
    toyota = CarMake.objects.create(
        name="Toyota",
        description="Japanese multinational automotive manufacturer",
        founded_date=datetime(1937, 8, 28)
    )

    honda = CarMake.objects.create(
        name="Honda",
        description="Japanese public multinational conglomerate manufacturer",
        founded_date=datetime(1948, 9, 24)
    )

    ford = CarMake.objects.create(
        name="Ford",
        description="American multinational automobile manufacturer",
        founded_date=datetime(1903, 6, 16)
    )

    # Create car models
    CarModel.objects.create(
        car_make=toyota,
        name="Camry",
        dealer_id=1,
        type="Sedan",
        year=2021
    )

    CarModel.objects.create(
        car_make=toyota,
        name="Corolla",
        dealer_id=2,
        type="Sedan",
        year=2021
    )

    CarModel.objects.create(
        car_make=honda,
        name="Civic",
        dealer_id=3,
        type="Sedan",
        year=2021
    )

    CarModel.objects.create(
        car_make=honda,
        name="CR-V",
        dealer_id=4,
        type="SUV",
        year=2021
    )

    CarModel.objects.create(
        car_make=ford,
        name="F-150",
        dealer_id=5,
        type="Truck",
        year=2021
    )

    CarModel.objects.create(
        car_make=ford,
        name="Mustang",
        dealer_id=6,
        type="Coupe",
        year=2021
    )
