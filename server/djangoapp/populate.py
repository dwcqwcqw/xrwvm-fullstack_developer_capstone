from .models import CarMake, CarModel
from datetime import date

def initiate():
    # 先删除所有现有数据
    CarModel.objects.all().delete()
    CarMake.objects.all().delete()
    
    # 创建汽车品牌
    car_make_data = [
        {"name": "NISSAN", "description": "Great cars. Japanese technology", "founded_date": date(1933, 12, 26), "headquarters": "Yokohama, Japan", "website": "https://www.nissan-global.com"},
        {"name": "Mercedes", "description": "Great cars. German technology", "founded_date": date(1926, 6, 28), "headquarters": "Stuttgart, Germany", "website": "https://www.mercedes-benz.com"},
        {"name": "Audi", "description": "Great cars. German technology", "founded_date": date(1909, 7, 16), "headquarters": "Ingolstadt, Germany", "website": "https://www.audi.com"},
        {"name": "Kia", "description": "Great cars. Korean technology", "founded_date": date(1944, 12, 11), "headquarters": "Seoul, South Korea", "website": "https://www.kia.com"},
        {"name": "Toyota", "description": "Great cars. Japanese technology", "founded_date": date(1937, 8, 28), "headquarters": "Toyota City, Japan", "website": "https://www.toyota.com"},
    ]

    car_make_instances = []
    for data in car_make_data:
        car_make = CarMake.objects.create(
            name=data['name'],
            description=data['description'],
            founded_date=data['founded_date'],
            headquarters=data['headquarters'],
            website=data['website']
        )
        car_make_instances.append(car_make)

    # 创建汽车型号
    car_model_data = [
        {"name": "Pathfinder", "type": "SUV", "year": date(2023, 1, 1), "dealer_id": 1, "car_make": car_make_instances[0]},
        {"name": "Qashqai", "type": "SUV", "year": date(2023, 1, 1), "dealer_id": 2, "car_make": car_make_instances[0]},
        {"name": "XTRAIL", "type": "SUV", "year": date(2023, 1, 1), "dealer_id": 3, "car_make": car_make_instances[0]},
        {"name": "A-Class", "type": "SEDAN", "year": date(2023, 1, 1), "dealer_id": 4, "car_make": car_make_instances[1]},
        {"name": "C-Class", "type": "SEDAN", "year": date(2023, 1, 1), "dealer_id": 5, "car_make": car_make_instances[1]},
        {"name": "E-Class", "type": "SEDAN", "year": date(2023, 1, 1), "dealer_id": 6, "car_make": car_make_instances[1]},
        {"name": "A4", "type": "SEDAN", "year": date(2023, 1, 1), "dealer_id": 7, "car_make": car_make_instances[2]},
        {"name": "A5", "type": "COUPE", "year": date(2023, 1, 1), "dealer_id": 8, "car_make": car_make_instances[2]},
        {"name": "A6", "type": "SEDAN", "year": date(2023, 1, 1), "dealer_id": 9, "car_make": car_make_instances[2]},
        {"name": "Sorrento", "type": "SUV", "year": date(2023, 1, 1), "dealer_id": 10, "car_make": car_make_instances[3]},
        {"name": "Carnival", "type": "VAN", "year": date(2023, 1, 1), "dealer_id": 11, "car_make": car_make_instances[3]},
        {"name": "Cerato", "type": "SEDAN", "year": date(2023, 1, 1), "dealer_id": 12, "car_make": car_make_instances[3]},
        {"name": "Corolla", "type": "SEDAN", "year": date(2023, 1, 1), "dealer_id": 13, "car_make": car_make_instances[4]},
        {"name": "Camry", "type": "SEDAN", "year": date(2023, 1, 1), "dealer_id": 14, "car_make": car_make_instances[4]},
        {"name": "RAV4", "type": "SUV", "year": date(2023, 1, 1), "dealer_id": 15, "car_make": car_make_instances[4]},
    ]

    for data in car_model_data:
        CarModel.objects.create(
            name=data['name'],
            type=data['type'],
            year=data['year'],
            dealer_id=data['dealer_id'],
            car_make=data['car_make']
        )
