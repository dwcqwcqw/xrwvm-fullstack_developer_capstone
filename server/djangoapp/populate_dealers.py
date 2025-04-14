from .models import Dealer

def populate_dealers():
    """
    Populate the database with sample dealer data
    """
    # Sample dealer data
    dealers_data = [
        {
            'full_name': 'Best Deal Auto',
            'city': 'New York',
            'state': 'NY',
            'address': '123 Main Street',
            'zip': '10001',
            'web': 'http://www.bestdealauto.com',
            'lat': 40.7128,
            'long': -74.0060,
        },
        {
            'full_name': 'Premium Cars',
            'city': 'Los Angeles',
            'state': 'CA',
            'address': '456 Hollywood Blvd',
            'zip': '90028',
            'web': 'http://www.premiumcars.com',
            'lat': 34.0522,
            'long': -118.2437,
        },
        {
            'full_name': 'Luxury Auto Gallery',
            'city': 'Miami',
            'state': 'FL',
            'address': '789 Ocean Drive',
            'zip': '33139',
            'web': 'http://www.luxuryautogallery.com',
            'lat': 25.7617,
            'long': -80.1918,
        },
        {
            'full_name': 'Elite Motors',
            'city': 'Chicago',
            'state': 'IL',
            'address': '321 Michigan Ave',
            'zip': '60601',
            'web': 'http://www.elitemotors.com',
            'lat': 41.8781,
            'long': -87.6298,
        },
        {
            'full_name': 'Star Auto Sales',
            'city': 'Houston',
            'state': 'TX',
            'address': '555 Texas Ave',
            'zip': '77002',
            'web': 'http://www.starautosales.com',
            'lat': 29.7604,
            'long': -95.3698,
        }
    ]

    # Create dealer objects
    for dealer_data in dealers_data:
        dealer = Dealer.objects.create(**dealer_data)
        print(f"Created dealer: {dealer.full_name}") 