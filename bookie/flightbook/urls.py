from django.urls import path

from . import views

app_name = "flightbook"
urlpatterns = [
    #path("", views.home, name="home"),
    #path("overview/", views.overview, name="overview"),
    path("add-flight/", views.add_flight, name="addflight"),
    path("add-commercial-flight/", views.add_commercial_flight, name="addcommercialflight"),
    #path("category/<int:pk>/", views.CategoryDetail.as_view(), name="category-detail"),
]
