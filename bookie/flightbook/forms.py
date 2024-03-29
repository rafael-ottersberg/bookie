from django import forms

from .models import Flight, CommercialFlight, Site, Wing

class FlightForm(forms.ModelForm):
    class Meta:
        model = Flight
        fields = [
            'flightbook',
            'takeoff',
            'landing',
            'date',
            'wing',
            'tandemflight',
            'duration',
            'distance',
            'comment',
        ]
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }

class FlightFormPart(forms.ModelForm):
    class Meta:
        model = Flight
        fields = [
            'takeoff',
            'landing',
            'date',
            'wing',
            'comment',
        ]
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }

class CommercialFlightForm(forms.ModelForm):
    class Meta:
        model = CommercialFlight
        fields = [
            'company',
            'trip_time',
            'double_airtime',
            'photos_sold',
            'photo_payment',
            'tip_payment',
            'tip',
        ]

class SiteForm(forms.ModelForm):
    class Meta:
        model = Site
        fields = [
            'name',
            'altitude',
        ]

class WingForm(forms.ModelForm):
    class Meta:
        model = Wing
        fields = [
            'callsign',
            'manufacturer',
            'model',
            'size',
            'color',
            'number_of_flights'
        ]

class CommercialDaySummaryForm(forms.Form):
    date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))

class CommercialMonthSummaryForm(forms.Form):
    date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))

class CommercialYearSummaryForm(forms.Form):
    date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))