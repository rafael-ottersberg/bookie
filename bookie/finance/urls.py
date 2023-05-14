from django.urls import path

from . import views

app_name = "finance"
urlpatterns = [
    path("", views.home, name="home"),
    path("overview/", views.overview, name="overview"),
    path("add-expense/", views.add_expense, name="addexpense"),
    path("add-income/", views.add_income, name="addincome"),
    path("category/<int:pk>/", views.CategoryDetail.as_view(), name="category-detail"),
]
