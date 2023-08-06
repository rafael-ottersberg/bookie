from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.utils import timezone
import datetime
from django.urls import reverse
from django.views import generic
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

from .forms import FlightForm, FlightFormPart, CommercialFlightForm, SiteForm, WingForm

from .models import Flight, FlightBook, CommercialFlight, Site, Wing, Company


@login_required
def add_flight(request):
    if request.method == "POST":
        form = FlightForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("flightbook:home"))
    else:
        initial = {"date": timezone.now().strftime("%Y-%m-%d")}
        form = FlightForm(initial=initial)

    return render(request, "flightbook/add_flight.html", {"form": form})

@login_required
def add_commercial_flight(request):
    if request.method == "POST":
        flight_form = FlightForm(request.POST)
        commercial_flight_form = CommercialFlightForm(request.POST)
        if flight_form.is_valid() and commercial_flight_form.is_valid():
            flight = flight_form.save(commit=False)
            flight.duration = 12
            flight.flightbook = FlightBook.objects.get(name='Rafael')
            flight.save()
            commercial_flight = commercial_flight_form.save(commit=False)
            commercial_flight.flight = flight
            commercial_flight.save()
            return HttpResponseRedirect(reverse("flightbook:home"))
    else:
        initial = {"date": timezone.now().strftime("%Y-%m-%d"), 'wing': Wing.objects.get(callsign='WorkingBee')}
        flight_form = FlightFormPart(initial=initial)

        initial_commercial = {"company": Company.objects.get(name="Paragliding Interlaken")}
        commercial_flight_form = CommercialFlightForm(initial=initial_commercial)

    return render(
        request, "flightbook/add_commercial_flight.html", 
        {
            "flight_form": flight_form,
            "commercial_flight_form": commercial_flight_form,
            })
"""
class CategoryDetail(LoginRequiredMixin, generic.DetailView):
    model = Category
    template_name = "finance/category.html"

    def get_context_data(self, **kwargs):
        show_last = 10
        context = super().get_context_data(**kwargs)
        context["expenses"] = self.object.expense_set.order_by("-date")[:show_last]
        context["incomes"] = self.object.income_set.order_by("-date")[:show_last]
        return context
"""

class FlightList(LoginRequiredMixin, generic.ListView):
    model = Flight

    def get_queryset(self):
        return Flight.objects.order_by("-date").filter(flightbook__pilot=self.kwargs['pilot'])
    