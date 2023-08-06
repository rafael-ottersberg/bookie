from django.db import models


class FlightBook(models.Model):
    pilot = models.CharField(max_length=64, verbose_name="Pilot:In")
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
    altitude = models.FloatField(default=None)

    class Meta:
        verbose_name = "Fluggebiet"
        verbose_name_plural = "Fluggebiete"

    def __str__(self):
        return f"{self.name} ({self.altitude:.0f}m)"


class Wing(models.Model):
    callsign = models.CharField(max_length=64)
    manufacturer = models.CharField(max_length=64)
    model = models.CharField(max_length=64)
    size = models.IntegerField(default=0)
    color = models.CharField(max_length=64)

    number_of_flights = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.callsign} - {self.manufacturer} {self.model} {self.size}"
    
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
    duration = models.FloatField(default=None, null=True, blank=True)
    distance = models.FloatField(default=None, null=True, blank=True)
    wing = models.ForeignKey(Wing, on_delete=models.CASCADE)

    tandemflight = models.BooleanField(default=False)

    comment = models.CharField(max_length=256, null=True, blank=True)

    def __str__(self):
        return f"{self.date}: {self.takeoff} - {self.landing}"
    
    class Meta:
        verbose_name = "Flug"
        verbose_name_plural = "Flüge"


class CommercialFlight(models.Model):
    flight = models.OneToOneField(Flight, on_delete=models.CASCADE)

    company = models.ForeignKey('Company', on_delete=models.CASCADE)

    double_airtime = models.BooleanField(default=False)

    TRIP_CHOICES = (
        ('07:15', '07:15'),
        ('08:15', '08:15'),
        ('09:30', '09:30'),
        ('10:40', '10:40'),
        ('11:50', '11:50'),
        ('13:00', '13:00'),
        ('14:15', '14:15'),
        ('15:30', '15:30'),
        ('16:45', '16:45'),
        ('18:00', '18:00'),
    )

    trip_time = models.CharField(max_length=16, choices=TRIP_CHOICES)

    photos_sold = models.BooleanField(default=False)

    CASH = 'Bar'
    DESK = 'Desk'
    CARD = 'Kreditkarte'
    PAYMENT_CHOICES = (
        (None, 'Keine Fotos'),
        (CASH, 'Bar'),
        (DESK, 'Desk'),
        (CARD, 'Kreditkarte'),
    )
    photo_payment = models.CharField(
        max_length=16,
        choices=PAYMENT_CHOICES,
        default=None, 
        null=True, 
        blank=True
    )

    tip = models.FloatField(default=None, null=True, blank=True)
    TIP_CHOICES = (
        (None, 'Kein Trinkgeld'),
        (CASH, 'Bar'),
        (CARD, 'Kreditkarte'),
    )
    tip_payment = models.CharField(
        max_length=16,
        choices=TIP_CHOICES,
        default=None,
        null=True, 
        blank=True
    )

    def __str__(self):
        return f"{self.company} - {self.flight.date}:  + {self.trip_time}"
    
    class Meta:
        verbose_name = "Kommerzieller Flug"
        verbose_name_plural = "Kommerzielle Flüge"


class Company(models.Model):
    name = models.CharField(max_length=64)
    
    earnings_per_flight = models.FloatField(default=0)
    earnings_da_bonus = models.FloatField(default=0)
    earnings_photos_desk = models.FloatField(default=0)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Firma"
        verbose_name_plural = "Firmen"
