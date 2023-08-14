from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.utils import timezone
import datetime
from django.urls import reverse
from django.views import generic
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

from .forms import FlightForm, FlightFormPart, CommercialFlightForm, CommercialDaySummaryForm, CommercialMonthSummaryForm

from .models import Flight, FlightBook, CommercialFlight, Site, Wing, Company


@login_required
def add_flight(request):
    if request.method == "POST":
        form = FlightForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("finance:home"))
    else:
        initial = {"date": timezone.now().strftime("%Y-%m-%d")}
        form = FlightForm(initial=initial)

    return render(request, "flightbook/add_flight.html", {"form": form})

@login_required
def add_commercial_flight(request):
    if request.method == "POST":
        flight_form = FlightFormPart(request.POST)
        commercial_flight_form = CommercialFlightForm(request.POST)
        if flight_form.is_valid() and commercial_flight_form.is_valid():
            flight = flight_form.save(commit=False)
            flight.duration = 12
            flight.tandemflight = True
            flight.flightbook = FlightBook.objects.get(pilot='Rafael')
            flight.save()
            commercial_flight = commercial_flight_form.save(commit=False)
            commercial_flight.flight = flight
            commercial_flight.save()
            flight.comment = 'PGI Nr. {commercial_flight.id}'
            flight.save()
            return HttpResponseRedirect(reverse("finance:home"))
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


class FlightList(LoginRequiredMixin, generic.ListView):
    model = Flight

    def get_queryset(self):
        return Flight.objects.order_by("-date").filter(flightbook__pilot=self.kwargs['pilot'])
    

@login_required
def commercial_day_summary(request):
    flight_list = None
    da_number = 0
    desk_photo_number = 0
    card_photo_number = 0
    cash_photo_number = 0
    total_cash = 0
    total_card = 0
    total_income = 0
    if request.method == "POST":
        form = CommercialDaySummaryForm(request.POST)
        if form.is_valid():
            date = form.cleaned_data['date']
            flight_list = CommercialFlight.objects.filter(flight__date=date)
            
            for f in flight_list:
                if f.double_airtime:
                    da_number += 1
                if f.photo_payment == CommercialFlight.DESK:
                    desk_photo_number += 1
                if f.photo_payment == CommercialFlight.CARD:
                    card_photo_number += 1
                if f.photo_payment == CommercialFlight.CASH:
                    cash_photo_number += 1
                if f.tip_payment == CommercialFlight.CASH:
                    total_cash = total_cash + float(f.tip)
                if f.tip_payment == CommercialFlight.CARD:
                    total_card = total_card + float(f.tip)

            total_cash += cash_photo_number * 40
            total_card += card_photo_number * 40

            total_income = flight_list.count() * 100 + da_number * 70 + desk_photo_number * 33 + total_cash + total_card
    else:
        initial = {"date": timezone.now().strftime("%Y-%m-%d")}
        form = CommercialDaySummaryForm(initial=initial)

    return render(
        request, "flightbook/commercial_day_summary.html", 
        {"form": form, "flight_list": flight_list, "total_income": total_income, "total_cash": total_cash, "total_card": total_card})
    