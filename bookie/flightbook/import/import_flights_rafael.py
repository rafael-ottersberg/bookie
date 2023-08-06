# move script to flightbook folder and run with:
# python manage.py shell < import_flights_rafael.py

import pandas as pd
from datetime import datetime
from flightbook.models import Site, Wing, Flight, FlightBook, CommercialFlight, Company

df = pd.read_csv('./flightbook/import/rafael_flights.csv', sep=';')

fb = FlightBook.objects.get(pilot='Rafael')

print(df.columns)

for row in df.iterrows():
    row = row[1]

    if Wing.objects.filter(callsign=row['Gleitschirm']).exists():
        wing = Wing.objects.get(callsign=row['Gleitschirm'])
    else:
        wing = Wing.objects.create(callsign=row['Gleitschirm'])
    

    if not Site.objects.filter(name=row['Start']).exists():
        print(f"Site {row['Start']} does not exist")

    if not Site.objects.filter(name=row['Landung']).exists():
        print(f"Site {row['Landung']} does not exist")

    takeoff = Site.objects.get(name=row['Start'])
    landing = Site.objects.get(name=row['Landung'])

    tandem = row['Tandem'] == 'x'

    flight = Flight.objects.create(
        flightbook=fb,
        takeoff=takeoff,
        landing=landing,
        date=datetime.strptime(row['Datum'], '%d.%m.%Y'),
        duration=None,
        distance=row['Distanz'],
        wing=wing,
        comment=row['Bemerkungen'],
        tandemflight=tandem
    )

    if str(row['Bemerkungen']).__contains__('PGI'):
        CommercialFlight.objects.create(
            flight=flight,
            company=Company.objects.get(name='Paragliding Interlaken'),
        )
