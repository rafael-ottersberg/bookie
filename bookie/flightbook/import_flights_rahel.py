import re
from datetime import datetime
from flightbook.models import Site, Wing, Flight, FlightBook

fb = FlightBook.objects.get(pilot='Roli')
tony = Wing.objects.create(callsign='Fat Tony', manufacturer='Advance', model='Alpha 6', size='22', color='Grün')
wonda = Wing.objects.create(callsign='Wonky Wonda', manufacturer='Niviuk', model='Kode P', size='22', color='Türkis')


with open('./flightbook/import/rahel_flights.txt') as f:

    last_date = None
    i = 0
    for line in f.readlines():
        if re.findall(r'[0-9]+\.[0-9]+', line):
            if line.count('.') == 2:
                d_str = re.findall(r'[0-9]+\.[0-9]+\.[0-9]+', line)[0]

                d = datetime.strptime(d_str, '%d.%m.%y')

                last_date = d
            
            if line.count('.') == 1:
                d_str = re.findall(r'[0-9]+\.[0-9]+', line)[0]
                d_str += '.22'
                d = datetime.strptime(d_str, '%d.%m.%y')

                last_date = d

        
        elif line.startswith('-'):
            line_s = line.split('. ', maxsplit=1)[1]

            takeoff, rest = line_s.split(' - ', maxsplit=1)
            landing, rest = rest.split(', ', maxsplit=1)
            duration, rest = rest.split(' Min., ', maxsplit=1)
            comment = rest.strip('\n')

            duration = int(duration)
            if not comment.strip():
                comment = ''

            takeoff = Site.objects.get(name=takeoff)
            landing = Site.objects.get(name=landing)

            if i < 20:
                wing = wonda
            else:
                wing = tony

            i += 1

            Flight.objects.create(
                flightbook=fb,
                takeoff=takeoff,
                landing=landing,
                date=last_date,
                duration=duration,
                wing=wing,
                comment=comment,
                tandemflight=False,
                distance=0
            )

