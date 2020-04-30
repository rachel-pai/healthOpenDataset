from google.cloud import bigquery
import os
import pgeocode

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'your bq credential json path'

bq_client = bigquery.Client('your_project_name')
# regular expression grammaer:https://github.com/google/re2/wiki/Syntax

q_extract_org = '''
SELECT
REGEXP_EXTRACT(other_info , r'^Adres\s*(.*?)\s\d{4}\s*[a-zA-Z]{2}\s.+?\s*(?:Telefoon|Website|Locatie|$)') AS address,
REGEXP_EXTRACT(other_info , r'^Adres\s*.*?\s(\d{4}\s*[a-zA-Z]{2})\s.+?\s*(?:Telefoon|Website|Locatie|$)') AS postcode,
REGEXP_EXTRACT(other_info , r'^Adres\s*.*?\s\d{4}\s*[a-zA-Z]{2}\s(.+?)\s*(?:Telefoon|Website|Locatie|$)') AS city,
REGEXP_EXTRACT(other_info , r'^.*Telefoon\s([\d-]*)') AS tel,
REGEXP_EXTRACT(other_info , r'^.*\sWebsite\s(.*nl)') AS web,
REGEXP_EXTRACT(other_info , r'.*\sLocatie(.*)') AS remark,
organization_name_x as organization_name, healthCare_type, link, other_info
from your_project_name.zorgkaartnederland.care_provider_organization
'''

df_zorg = bq_client.query(q_extract_org).to_dataframe()
df_zorg = df_zorg[df_zorg['postcode'].notnull()]

# change Bergen in Limburg into Bergen (l.), Bergen in NoordHolland into Bergen (nh.)
df_zorg.loc[(df_zorg['postcode'].str.startswith('5', na=False)) & (df_zorg['city']=='Bergen'),'city'] = 'Bergen L'
df_zorg.loc[(df_zorg['postcode'].str.startswith('1', na=False)) & (df_zorg['city']=='Bergen'),'city'] = 'Bergen (NH)'

df_zorg['postcode_ext'] = df_zorg['postcode'].str.extract('^(\d{4})\s\w*$', expand=False)
# remove 66 records where poscode is null
df_zorg = df_zorg[df_zorg['postcode_ext'].notnull()]

post_list = df_zorg['postcode_ext'].values.tolist()

nomi = pgeocode.Nominatim('NL')
res = nomi.query_postal_code([str(postcode) for postcode in post_list])
print(res.shape)

res['city'] = df_zorg['city'].to_numpy()
res['postcode'] = df_zorg['postcode'].to_numpy()
res['address'] = df_zorg['address'].to_numpy()
res['tel'] = df_zorg['tel'].to_numpy()
res['web'] = df_zorg['web'].to_numpy()
res['remark'] = df_zorg['remark'].to_numpy()
res['organization_name'] = df_zorg['organization_name'].to_numpy()
res['healthCare_type'] = df_zorg['healthCare_type'].to_numpy()
res['link'] = df_zorg['link'].to_numpy()
res['other_info'] = df_zorg['other_info'].to_numpy()

res.drop(columns=['postal_code','country code','accuracy'],inplace=True)

print(res.columns)
print(res.head(5))

datasetname = 'zorgkaartnederland'
med_org_table = 'care_provider_organization_GIS'

res.to_gbq('{}.{}'.format(datasetname,med_org_table),if_exists = 'replace')
