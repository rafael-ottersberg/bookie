from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.utils import timezone
import datetime
from django.urls import reverse
from django.views import generic
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

from .forms import FlightForm, FlightFormPart, CommercialFlightForm, CommercialDaySummaryForm, CommercialMonthSummaryForm, CommercialYearSummaryForm

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


@login_required
def commercial_month_summary(request):
    number_of_normal_flights = 0
    number_of_da_flights = 0
    number_of_photo_video_desk = 0

    photo_card = 0
    photo_cash = 0

    tip_card = 0
    tip_cash = 0


    if request.method == "POST":
        form = CommercialMonthSummaryForm(request.POST)
        if form.is_valid():
            date = form.cleaned_data['date']
            print(date)
            flight_list = CommercialFlight.objects.filter(flight__date__month=date.month, flight__date__year=date.year)

            for f in flight_list:
                if f.double_airtime:
                    number_of_da_flights += 1
                else:
                    number_of_normal_flights += 1
                if f.photo_payment == CommercialFlight.DESK:
                    number_of_photo_video_desk += 1
                if f.tip_payment == CommercialFlight.CASH:
                    tip_cash += float(f.tip)
                if f.tip_payment == CommercialFlight.CARD:
                    tip_card += float(f.tip)
                if f.photo_payment == CommercialFlight.CASH:
                    photo_cash += 40
                if f.photo_payment == CommercialFlight.CARD:
                    photo_card += 40

        
    else:
        initial = {"date": timezone.now().strftime("%Y-%m-%d")}
        form = CommercialMonthSummaryForm(initial=initial)

    return render(
    request, "flightbook/commercial_month_summary.html", 
    {
        "form": form, "number_of_normal_flights": number_of_normal_flights, 
        "number_of_da_flights": number_of_da_flights, "number_of_photo_video_desk": number_of_photo_video_desk, 
        "photo_card": photo_card, "photo_cash": photo_cash, "tip_card": tip_card, "tip_cash": tip_cash
    })


@login_required
def commercial_year_summary(request):
    number_of_normal_flights = 0
    number_of_da_flights = 0
    number_of_photo_video_desk = 0

    number_of_flights_chalet = 0
    number_of_flights_vkpi = 0

    photo_card = 0
    photo_cash = 0

    tip_card = 0
    tip_cash = 0


    if request.method == "POST":
        form = CommercialYearSummaryForm(request.POST)
        if form.is_valid():
            date = form.cleaned_data['date']
            flight_list = CommercialFlight.objects.filter(flight__date__year=date.year)

            for f in flight_list:
                if f.double_airtime:
                    number_of_da_flights += 1
                else:
                    number_of_normal_flights += 1

                if f.flight.takeoff.name == 'Chalet':
                    number_of_flights_chalet += 1
                else:
                    number_of_flights_vkpi += 1
                
                if f.photo_payment == CommercialFlight.DESK:
                    number_of_photo_video_desk += 1
                if f.tip_payment == CommercialFlight.CASH:
                    tip_cash += float(f.tip)
                if f.tip_payment == CommercialFlight.CARD:
                    tip_card += float(f.tip)
                if f.photo_payment == CommercialFlight.CASH:
                    photo_cash += 40
                if f.photo_payment == CommercialFlight.CARD:
                    photo_card += 40

        
    else:
        initial = {"date": timezone.now().strftime("%Y-%m-%d")}
        form = CommercialMonthSummaryForm(initial=initial)

    return render(
    request, "flightbook/commercial_year_summary.html", 
    {
        "form": form, "number_of_normal_flights": number_of_normal_flights,
        "flight_chalet": number_of_flights_chalet, "flight_vkpi": number_of_flights_vkpi,
        "number_of_da_flights": number_of_da_flights, "number_of_photo_video_desk": number_of_photo_video_desk, 
        "photo_card": photo_card, "photo_cash": photo_cash, "tip_card": tip_card, "tip_cash": tip_cash
    })
