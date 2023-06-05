from django.db import models


class FlightBook(models.Model):
    pilot = models.CharField(max_length=64)
    number_of_flights = models.IntegerField(default=0)

    def __str__(self):
        return self.pilot
    
    def count_flights(self):
        return self.flight_set.count()
    
        
    class Meta:
        verbose_name = "Flugbuch"
        verbose_name_plural = "Flugbücher"
    

class Site(models.Model):
    name = models.CharField(max_length=64)
    height = models.FloatField(default=None)

    class Meta:
        verbose_name = "Fluggebiet"
        verbose_name_plural = "Fluggebiete"


class Wing(models.Model):
    callsign = models.CharField(max_length=64)
    brand = models.CharField(max_length=64)
    model = models.CharField(max_length=64)
    size = models.IntegerField(default=0)
    color = models.CharField(max_length=64)

    number_of_flights = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.callsign} - {self.brand} {self.model} {self.size}"
    
    def count_flights(self):
        return self.flight_set.count()
    
    class Meta:
        verbose_name = "Schirm"
        verbose_name_plural = "Schirme"
    

class Flight(models.Model):
    flightbook = models.ForeignKey(FlightBook, on_delete=models.CASCADE)

    takeoff = models.ForeignKey(Site, on_delete=models.CASCADE, related_name='takeoff')
    landing = models.ForeignKey(Site, on_delete=models.CASCADE, related_name='landing')
    date = models.DateField()
    duration = models.FloatField(default=0)
    distance = models.FloatField(default=0)
    wing = models.ForeignKey(Wing, on_delete=models.CASCADE)

    tandemflight = models.BooleanField(default=False)
    vkpi = models.BooleanField(default=False)

    comment = models.CharField(max_length=256)

    def __str__(self):
        return f"{self.date}: {self.takeoff} - {self.landing}"
    
    class Meta:
        verbose_name = "Flug"
        verbose_name_plural = "Flüge"


class CommercialFlight(models.Model):
    flight = models.OneToOneField(Flight, on_delete=models.CASCADE, primary_key=True)

    company = models.CharField(max_length=64)

    double_airtime = models.BooleanField(default=False)
    trip_time = models.CharField(max_length=64)

    photos_sold = models.BooleanField(default=False)
    cash_payment = models.BooleanField(default=False)
    desk_payment = models.BooleanField(default=False)
    credit_card_payment = models.BooleanField(default=False)

    tip = models.FloatField(default=0)

    def __str__(self):
        return f"{self.company} - {self.flight.date}:  + {self.trip_time}"
    
    class Meta:
        verbose_name = "Kommerzieller Flug"
        verbose_name_plural = "Kommerzielle Flüge"


class Company(models.Model):
    name = models.CharField(max_length=64)
    
    earnings_per_flight = models.FloatField(default=0)
    earnings_bonus = models.FloatField(default=0)
    earnings_photos_desk = models.FloatField(default=0)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Firma"
        verbose_name_plural = "Firmen"
