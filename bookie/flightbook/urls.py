from django.urls import path

from . import views

app_name = "flightbook"
urlpatterns = [
    path("add-flight/", views.add_flight, name="addflight"),
    path("add-commercial-flight/", views.add_commercial_flight, name="addcommercialflight"),
    path("flights/<str:pilot>/", views.FlightList.as_view(), name="flightlist"),
    path("commercial-day-summary/", views.commercial_day_summary, name="commercialdaysummary"),
    path("commercial-month-summary/", views.commercial_month_summary, name="commercialmonthsummary"),
    path("commercial-year-summary/", views.commercial_year_summary, name="commercialyearsummary"),
]
