from django.contrib import admin
from .models import CarMake, CarModel

# Register your models here.

class CarModelInline(admin.TabularInline):
    model = CarModel
    extra = 1

class CarMakeAdmin(admin.ModelAdmin):
    inlines = [CarModelInline]
    list_display = ('name', 'founded_date', 'headquarters')
    search_fields = ['name', 'headquarters']
    list_filter = ['founded_date']

class CarModelAdmin(admin.ModelAdmin):
    list_display = ('name', 'car_make', 'type', 'year', 'dealer_id')
    list_filter = ['car_make', 'type', 'year']
    search_fields = ['name', 'car_make__name']

admin.site.register(CarMake, CarMakeAdmin)
admin.site.register(CarModel, CarModelAdmin)
