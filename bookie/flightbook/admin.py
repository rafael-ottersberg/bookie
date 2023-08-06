from django.contrib import admin

from .models import FlightBook, Flight, CommercialFlight, Company, Site, Wing

@admin.register(Flight)
class FlightAdmin(admin.ModelAdmin):
    list_display = ('date', 'flightbook', 'takeoff', 'landing', 'wing', 'duration', 'distance', 'tandemflight')
    list_filter = ('flightbook', 'date', 'takeoff', 'landing', 'wing', 'tandemflight')
    list_per_page = 100
    ordering = ('-date', '-flightbook')

@admin.register(CommercialFlight)
class CommercialFlightAdmin(admin.ModelAdmin):
    list_display = ('flight', 'company', 'trip_time', 'double_airtime', 'photos_sold', 'photo_payment', 'tip', 'tip_payment')
    list_filter = ('flight__date',)
    list_per_page = 100
    ordering = ('-flight__date',)
    
admin.site.register(FlightBook)
admin.site.register(Company)
admin.site.register(Site)
admin.site.register(Wing)