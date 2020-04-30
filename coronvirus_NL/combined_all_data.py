from datetime import datetime, timedelta
import pandas as pd
pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)
from google.cloud import bigquery
import os
import numpy as np

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'your bq credential json path'
bq_client = bigquery.Client('your_project_name')

df_infected = pd.read_csv('data/coron_municipality.csv')

df_infected = df_infected[df_infected['Gemeentenaam'].notnull()]
df_infected['Datum'] = pd.to_datetime(df_infected['Datum'],format='%Y-%m-%d')

prov_aantal = df_infected.groupby(['Provincienaam'])['Aantal'].agg('sum').reset_index(name='Provincie_aantal')
df_infected = pd.merge(df_infected,prov_aantal, on=['Provincienaam'],how='left')

# combine yesterday data
df_infected['Datum_yes'] = pd.to_datetime(df_infected['Datum']- timedelta(1),format='%Y-%m-%d')
df_infected = pd.merge(df_infected,df_infected,
                       left_on=['Datum_yes','Gemeentenaam','Provincienaam','Gemeentecode'],
                       right_on=['Datum','Gemeentenaam','Provincienaam','Gemeentecode'],
                       how='left')
df_infected.drop(columns = ['Datum_yes_x','Datum_yes_y'],inplace = True)
df_infected.rename(columns={'Datum_x': 'Datum', 'Aantal_x': 'Aantal','Provincie_aantal_x':'Provincie_aantal',
                            'Datum_y':'Datum_yes','Aantal_y':'Aantal_yes','Provincie_aantal_y':'Provincie_aantal_yes'},
                   inplace=True)
df_infected = df_infected.fillna(0)
#
# combine the day before yesterday data
df_infected['Datum_yes2'] = pd.to_datetime(df_infected['Datum']- timedelta(2),format='%Y-%m-%d')
df_infected = pd.merge(df_infected,df_infected,
                       left_on=['Datum_yes2','Gemeentenaam','Provincienaam','Gemeentecode'],
                       right_on=['Datum','Gemeentenaam','Provincienaam','Gemeentecode'],
                       how='left')

df_infected.drop(columns = ['Datum_yes_x','Datum_yes2_x','Datum_yes_y','Datum_yes2_y'],inplace = True)
df_infected.rename(columns={'Datum_x': 'Datum', 'Aantal_x': 'Aantal','Provincie_aantal_x':'Provincie_aantal',
                            'Aantal_yes_x':'Aantal_yes','Provincie_aantal_yes_x':'Provincie_aantal_yes',
                            'Datum_y':'Datum_yes2','Provincie_aantal_y':'Provincie_aantal_yes2',
                            'Aantal_yes_y':'Aantal_yes3','Provincie_aantal_yes_y':'Provincie_aantal_yes3'},
                   inplace=True)
df_infected = df_infected.fillna(0)
print("columns after merging:",df_infected.columns)

df_infected['Gemeentenaam'] = df_infected['Gemeentenaam'].str.lower()
df_infected['Provincienaam'] = df_infected['Provincienaam'].str.lower()

df_infected['outbreak_days'] = (df_infected['Datum']-df_infected['Datum'].min() ).dt.days

print("the shape of data:",df_infected.shape)

### =====================
### combine weather data
### =====================

# regular expression grammaer:https://github.com/google/re2/wiki/Syntax
q_march = '''
select date, high_temp_degree, low_temp_degree, hist_Gemiddeld_degree_low, hist_Gemiddeld_degree_high, link,
LOWER(Gemeentenaam) AS Gemeentenaam,
LOWER(Provincienaam) AS Provincienaam
from your_project_name.accuweather.accuweather_march
'''
q_feb = '''
select date, high_temp_degree, low_temp_degree, hist_Gemiddeld_degree_low, hist_Gemiddeld_degree_high, link,
LOWER(Gemeentenaam) AS Gemeentenaam,
LOWER(Provincienaam) AS Provincienaam
from your_project_name.accuweather.accuweather_feb
'''
q_april = '''
select date, high_temp_degree, low_temp_degree, hist_Gemiddeld_degree_low, hist_Gemiddeld_degree_high, link,
LOWER(Gemeentenaam) AS Gemeentenaam,
LOWER(Provincienaam) AS Provincienaam
from your_project_name.accuweather.accuweather_april
'''
q_today = '''
select date, high_temp_degree, low_temp_degree, hist_Gemiddeld_degree_low, hist_Gemiddeld_degree_high, link,
LOWER(Gemeentenaam) AS Gemeentenaam,
LOWER(Provincienaam) AS Provincienaam
from your_project_name.accuweather.accuweather_current
'''

march_weather = bq_client.query(q_march).to_dataframe()
feb_weather = bq_client.query(q_feb).to_dataframe()
april_weather = bq_client.query(q_april).to_dataframe()
today_weather = bq_client.query(q_today).to_dataframe()

march_weather['date'] = pd.to_datetime(march_weather['date'] ,format='%Y-%m-%d')
feb_weather['date'] = pd.to_datetime(feb_weather['date'] ,format='%Y-%m-%d')
april_weather['date'] = pd.to_datetime(april_weather['date'] ,format='%Y-%m-%d')
today_weather['date'] = pd.to_datetime(today_weather['date'] ,format='%Y-%m-%d')

df_infected['month'] = df_infected['Datum'].dt.month

assert list(set(df_infected['Gemeentenaam'].unique())- set(march_weather['Gemeentenaam'].unique())) == []
assert list(set(df_infected['Gemeentenaam'].unique())- set(feb_weather['Gemeentenaam'].unique())) == []
assert list(set(df_infected['Gemeentenaam'].unique())- set(april_weather['Gemeentenaam'].unique())) == []
assert list(set(df_infected['Gemeentenaam'].unique())- set(today_weather['Gemeentenaam'].unique())) == []

# today = datetime.today().strftime('%Y-%m-%d')
today = '2020-04-24'

df_march = pd.merge(df_infected[df_infected['month']==3], march_weather, left_on=['Datum','Gemeentenaam','Provincienaam'],
              right_on=['date','Gemeentenaam','Provincienaam'], how='left')
df_feb = pd.merge(df_infected[df_infected['month']==2], feb_weather, left_on=['Datum','Gemeentenaam','Provincienaam'],
              right_on=['date','Gemeentenaam','Provincienaam'], how='left')
df_apri = pd.merge(df_infected[(df_infected['month']==4) & (df_infected['Datum']!= today)],
                   april_weather,
                   left_on=['Datum','Gemeentenaam','Provincienaam'],
                   right_on=['date','Gemeentenaam','Provincienaam'], how='left')

df_today = pd.merge(df_infected[df_infected['Datum']== today], today_weather, left_on=['Datum','Gemeentenaam','Provincienaam'],
              right_on=['date','Gemeentenaam','Provincienaam'], how='left')

df = pd.concat([df_feb,df_march,df_apri,df_today])
df = df[df.notna()]
assert df.shape[0] == df_infected.shape[0]
assert df.isnull().any().any() == False

df.drop(columns = ['link','date','month'],inplace = True)
print("after merging weather info:",df.shape)


### =================
# combine other info
### =================
# combine rivm info

def merge_cities(rivm_df,city_list,new_city_name):
    temp = rivm_df.loc[rivm_df['Gemeentenaam'].isin(city_list)]
    temp = temp.drop(columns = ['Gemeentenaam']).sum(axis=0).to_frame().T
    temp['Gemeentenaam'] =new_city_name
    rivm_df = rivm_df.loc[~rivm_df['Gemeentenaam'].isin(city_list)]
    rivm_df = pd.concat([rivm_df,temp])

    return rivm_df


q_march = '''
select *
from your_project_name.rivm.summary_2016
'''
rivm_df = bq_client.query(q_march).to_dataframe()
# print(rivm_df.columns)
rivm_df.drop(columns = 'Gemeenten2016', inplace = True)
rivm_df.rename(columns={'Gemeenten2016_gemnaam': 'Gemeentenaam'}, inplace=True)
rivm_df['Gemeentenaam'] = rivm_df['Gemeentenaam'].str.lower()

rivm_df = merge_cities(rivm_df,['bedum', 'de marne', 'eemsmond','winsum'],'het hogeland')
rivm_df = merge_cities(rivm_df,['schijndel','sint-oedenrode','veghel'],'meierijstad')
rivm_df = merge_cities(rivm_df, ['nuth','onderbanken','schinnen'],'beekdaelen')
rivm_df = merge_cities(rivm_df, ['Grootegast', 'Leek', 'Marum', 'Zuidhorn'] ,'westerkwartier') #partly winsum
rivm_df = merge_cities(rivm_df, ['hoogezand-sappemeer', 'slochteren','menterwolde'],'midden-groningen')
rivm_df = merge_cities(rivm_df, ['vianen', 'leerdam','zederik'],'vijfheerenlanden')
rivm_df = merge_cities(rivm_df, ['aalburg', 'werkendam', 'woudrichem'],'altena')
rivm_df = merge_cities(rivm_df, ['geldermalsen', 'neerijnen', 'lingewaal'], 'west betuwe')
rivm_df = merge_cities(rivm_df, ['dongeradeel', 'ferwerderadiel', 'kollumerland en nieuwkruisland'],'noardeast-fryslân')
rivm_df = merge_cities(rivm_df, ['bellingwedde','vlagtwedde'],'westerwolde')
rivm_df = merge_cities(rivm_df, ['franekeradeel', 'het bildt', 'menameradiel','littenseradiel'],'waadhoeke')
rivm_df = merge_cities(rivm_df, ['binnenmaas', 'cromstrijen', 'korendijk', 'oud-beijerland','strijen'],'hoeksche waard')
rivm_df = merge_cities(rivm_df, ['giessenlanden','molenwaard'],'molenlanden')

rivm_df['Gemeentenaam'] = rivm_df['Gemeentenaam'].replace('nuenen gerwen en nederwetten','nuenen, gerwen en nederwetten')

assert list(set(df['Gemeentenaam'].unique()) - set(rivm_df['Gemeentenaam'].unique())) == []
# print("======================")
# print(list(set(rivm_df['Gemeentenaam'].unique()) - set(df['Gemeentenaam'].unique())))

df = pd.merge(df,rivm_df, on=['Gemeentenaam'],how='left')

df = df[~df.isnull()]
assert df.shape[0] == df_infected.shape[0]
assert df.isnull().any().any() == False

### =================
# combine other info
### =================
# q_patient_info = '''
# select *
# from your_project_name.vetkis.VektisOpenDatabestandZorgverzekeringswet2017gemeente
# '''
# vetkis_df = bq_client.query(q_patient_info).to_dataframe()
# # print(vetkis_df.columns)
#
# vetkis_df.rename(columns={'GEMEENTENAAM': 'Gemeentenaam'}, inplace=True)
# vetkis_df['Gemeentenaam'] = vetkis_df['Gemeentenaam'].str.lower()
# vetkis_df['Gemeentenaam'] = vetkis_df['Gemeentenaam']\
#     .replace('s gravenhage','\'s-gravenhage')\
#     .replace('bergen lb','bergen (l.)')\
#     .replace('sudwest-fryslan','súdwest-fryslân')\
#     .replace('s hertogenbosch','\'s-hertogenbosch')\
#     .replace('noardeast-fryslan','noardeast-fryslân')\
#     .replace('bergen nh','bergen (nh.)')\
#     .replace('nuenen ca','nuenen, gerwen en nederwetten')
#
# print('vetikis')
# print(list(set(df['Gemeentenaam'].unique()) - set(vetkis_df['Gemeentenaam'].unique())))
# print(list(set(vetkis_df['Gemeentenaam'].unique()) - set(df['Gemeentenaam'].unique())))
#
# df = pd.merge(df,vetkis_df, on=['Gemeentenaam'],how='left')
# print("after merging VektisOpenDatabestandZorgverzekeringswet2017gemeente info:",df.shape)
#
# print(df.shape)

### =================
# combine other info
### =================

q_zorg_org = '''
WITH fill_na_place AS(
  SELECT IFNULL(place_name,"Slochteren, Schildwolde") as place_name,state_name,postcode,city,county_name
  FROM your_project_name.zorgkaartnederland.care_provider_organization_GIS
  where city = 'Slochteren'
  UNION ALL
  SELECT IFNULL(place_name, "'s-Gravenhage") as place_name,state_name,postcode,city,county_name
  FROM your_project_name.zorgkaartnederland.care_provider_organization_GIS
  where city = 'Den Haag'
  UNION ALL
  SELECT IFNULL(place_name, city) as place_name,state_name,postcode,city,county_name
  FROM your_project_name.zorgkaartnederland.care_provider_organization_GIS
  where city NOT IN ('Den Haag','Slochteren')
),

fill_na_state AS (
SELECT place_name, postcode,
       coalesce(state_name, max(state_name) OVER (PARTITION BY place_name)) AS state_name,
       coalesce(county_name, max(county_name) OVER (PARTITION BY place_name)) AS county_name
FROM fill_na_place
)

SELECT LOWER(county_name) AS Gemeentenaam, LOWER(state_name) AS Provincienaam,COUNT(*) AS record_count
FROM fill_na_state
GROUP BY state_name,county_name
'''

df_org = bq_client.query(q_zorg_org).to_dataframe()
# df_org = preprocess_zorg_gem(df_org)

# print(list(set(df['Gemeentenaam'].unique()) - set(df_org['Gemeentenaam'].unique())))
# print(list(set(df_org['Gemeentenaam'].unique()) - set(df['Gemeentenaam'].unique())))

df = pd.merge(df,df_org,on=['Gemeentenaam','Provincienaam'], how='left')

try:
    assert list(sorted(list(set(df['Gemeentenaam']) - set(df_org['Gemeentenaam'])))) == []
except:
    print(list(sorted(list(set(df['Gemeentenaam']) - set(df_org['Gemeentenaam'])))))

# does not contain any fale record
df = df[~df.isnull()]
assert df.shape[0] == df_infected.shape[0]
assert df.isnull().any().any() == False

# print(df.columns)

### =================
# combine other info
### =================
# patient
q_doc_org = '''
WITH fill_na_place AS(
  SELECT IFNULL(org_place_name,"Slochteren, Schildwolde") as org_place_name,org_state_name,org_postcode,org_city,org_county_name
  FROM your_project_name.zorgkaartnederland.care_provider_person_GIS
  where org_city = 'Slochteren'
  UNION ALL
  SELECT IFNULL(org_place_name, "'s-Gravenhage") as org_place_name,org_state_name,org_postcode,org_city,org_county_name
  FROM your_project_name.zorgkaartnederland.care_provider_person_GIS
  where org_city = 'Den Haag'
  UNION ALL
  SELECT IFNULL(org_place_name, org_city) as org_place_name,org_state_name,org_postcode,org_city,org_county_name
  FROM your_project_name.zorgkaartnederland.care_provider_person_GIS
  where org_city NOT IN ('Den Haag','Slochteren')
),

fill_na_state AS (
SELECT org_place_name, org_postcode,
       coalesce(org_state_name, max(org_state_name) OVER (PARTITION BY org_place_name)) AS org_state_name,
       coalesce(org_county_name, max(org_county_name) OVER (PARTITION BY org_place_name)) AS org_county_name
FROM fill_na_place
)

SELECT LOWER(org_county_name) AS Gemeentenaam, LOWER(org_state_name) AS Provincienaam,COUNT(*) AS doc_record_count
FROM fill_na_state
GROUP BY org_state_name,org_county_name
'''

df_doc = bq_client.query(q_doc_org).to_dataframe()
# df_org = preprocess_zorg_gem(df_org)

# print(list(set(df['Gemeentenaam'].unique()) - set(df_org['Gemeentenaam'].unique())))
# print(list(set(df_org['Gemeentenaam'].unique()) - set(df['Gemeentenaam'].unique())))

df = pd.merge(df,df_doc,on=['Gemeentenaam','Provincienaam'], how='left')
df.drop(columns ='Gemeentecode',inplace = True)

try:
    assert list(sorted(list(set(df['Gemeentenaam']) - set(df_doc['Gemeentenaam'])))) == []
except:
    print(list(sorted(list(set(df['Gemeentenaam']) - set(df_doc['Gemeentenaam'])))))

# does not contain any fale record
df = df[~df.isnull()]
assert df.shape[0] == df_infected.shape[0]
assert df.isnull().any().any() == False

print("after merging, the shape of the data",df.shape)
print("columns:",df.columns)
print("orginal dataframe size:",df_infected.shape)

# insert the final result into the biqgeury table
client = bigquery.Client()
datasetname = 'coronvirus_NL'
table_id = '{}.{}'.format(datasetname,'summary_rivm_NL_covid19_hosp_municipality')

df.to_gbq(table_id,if_exists = 'replace')
df.to_csv('temp.csv',index=False)



