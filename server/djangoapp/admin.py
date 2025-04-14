from django.contrib import admin
from .models import CarMake, CarModel, Dealer


@admin.register(CarMake)
class CarMakeAdmin(admin.ModelAdmin):
    list_display = ['name', 'description', 'founded_date']
    search_fields = ['name']


@admin.register(CarModel)
class CarModelAdmin(admin.ModelAdmin):
    list_display = ['car_make', 'name', 'dealer_id', 'type', 'year']
    search_fields = ['name', 'type']
    list_filter = ['car_make', 'year']


@admin.register(Dealer)
class DealerAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'city', 'state', 'address']
    search_fields = ['full_name', 'city', 'state']
