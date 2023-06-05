from django.contrib import admin

from .models import FlightBook, Flight, CommercialFlight, Company, Site, Wing


@admin.register(Flight)
class FlightAdmin(admin.ModelAdmin):
    list_display = ('date', 'takeoff', 'landing', 'wing', 'duration', 'distance', 'tandemflight', 'vkpi')
    list_filter = ('date', 'takeoff', 'landing', 'wing', 'tandemflight', 'vkpi')
    list_per_page = 30


admin.site.register(FlightBook)
admin.site.register(CommercialFlight)
admin.site.register(Company)
admin.site.register(Site)
admin.site.register(Wing)


