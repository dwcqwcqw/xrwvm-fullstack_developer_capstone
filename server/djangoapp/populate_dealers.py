from .models import Dealer

def populate_dealers():
    # Clear existing dealers
    Dealer.objects.all().delete()
    
    # Sample dealer data
    dealers_data = [
        {
            "full_name": "Best Deal Auto NY",
            "city": "New York",
            "state": "NY",
            "address": "123 Broadway St",
            "zip": "10007",
            "web": "http://bestdealauto.com",
            "lat": 40.7128,
            "long": -74.0060
        },
        {
            "full_name": "California Cars",
            "city": "Los Angeles",
            "state": "CA",
            "address": "456 Hollywood Blvd",
            "zip": "90028",
            "web": "http://californiacars.com",
            "lat": 34.0522,
            "long": -118.2437
        },
        {
            "full_name": "Texas Auto Hub",
            "city": "Houston",
            "state": "TX",
            "address": "789 Main St",
            "zip": "77002",
            "web": "http://texasautohub.com",
            "lat": 29.7604,
            "long": -95.3698
        },
        {
            "full_name": "Florida Motors",
            "city": "Miami",
            "state": "FL",
            "address": "321 Ocean Drive",
            "zip": "33139",
            "web": "http://floridamotors.com",
            "lat": 25.7617,
            "long": -80.1918
        },
        {
            "full_name": "Chicago Auto Mall",
            "city": "Chicago",
            "state": "IL",
            "address": "555 Michigan Ave",
            "zip": "60611",
            "web": "http://chicagoautomall.com",
            "lat": 41.8781,
            "long": -87.6298
        }
    ]
    
    # Create dealer instances
    for data in dealers_data:
        Dealer.objects.create(**data)
    
    print("Dealers data has been populated successfully!") 