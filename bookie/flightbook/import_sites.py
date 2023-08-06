import pandas as pd
from flightbook.models import Site

def import_sites():
    df = pd.read_csv('./flightbook/import/sites.csv', sep=';')
    print(df)
    for index, row in df.iterrows():
        site = Site.objects.create(name=row['name'], altitude=row['altitude'])

        print(f"Created site {site.name} with altitude {site.altitude}m")

import_sites()