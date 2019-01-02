from django.contrib import admin

from .models import City, State, Country, Area, BuildingComplex


class CountryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name', )


class StateAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'country')
    list_filter = ('country', )
    search_fields = ('name', 'country')


class CityAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'state')
    list_filter = ('state', )
    search_fields = ('name', 'state')


admin.site.register(Country, CountryAdmin)
admin.site.register(State, StateAdmin)
admin.site.register(City, CityAdmin)
admin.site.register(Area)
admin.site.register(BuildingComplex)
