from django.contrib import admin

from .models import FlightBook, Flight, CommercialFlight, Company, Site, Wing


@admin.register(Flight)
class FlightAdmin(admin.ModelAdmin):
    list_display = ('date', 'flightbook', 'takeoff', 'landing', 'wing', 'duration', 'distance', 'tandemflight')
    list_filter = ('flightbook', 'date', 'takeoff', 'landing', 'wing', 'tandemflight')
    list_per_page = 200


admin.site.register(FlightBook)
admin.site.register(CommercialFlight)
admin.site.register(Company)
admin.site.register(Site)
admin.site.register(Wing)


