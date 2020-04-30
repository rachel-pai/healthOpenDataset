# pip install geolocation-python

# -- coding: utf-8 --

import googlemaps
from datetime import datetime, timedelta
import pandas as pd
pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)
from google.cloud import bigquery
import os

gmaps = googlemaps.Client(key='your api key here')
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'your bq credential json path'


bq_client = bigquery.Client('your_project_name')

q_insurer_gem = '''
SELECT *
from your_project_name.vetkis.VektisOpenDatabestandZorgverzekeringswet2017gemeente
'''
insuer_gemeente = bq_client.query(q_insurer_gem).to_dataframe()


print("starting geocoding....")
df = pd.DataFrame(data = {'GEMEENTENAAM':insuer_gemeente['GEMEENTENAAM'].unique()})
df['address'] = df['GEMEENTENAAM'].str.lower() + ', Netherlands'
df = df[df.notna()]
# Geocoding an address
df['location'] = df['address'].apply(lambda x: gmaps.geocode(x))
## for the geoencoding, you could also use another method:
# from geopy.geocoders import Nominatim
# geolocator = Nominatim(user_agent="GEMEENTENAAM location")
# df['city_coord'] = df['address'].apply(geolocator.geocode)


# save back into the bigqeury table
df.to_gbq('vetkis.coordiantion2017gemeente',if_exists = 'replace')
