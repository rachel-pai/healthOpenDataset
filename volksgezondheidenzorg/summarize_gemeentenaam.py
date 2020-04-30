import pandas as pd
pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)
from google.cloud import bigquery
import os

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'your bq credential json path'
bq_client = bigquery.Client('your_project_name')

# read query
File_object = open('summary_gemeentenaam.sql',"r+")
q = File_object.readlines()
q = ''.join(q)

df = bq_client.query(q).to_dataframe()

# pivot table
df_pivot = df[['Sportenbewegen_Percentage','Sportenbewegen','Gemeente']]
df_pivot = df_pivot.pivot_table(values='Sportenbewegen_Percentage', columns='Sportenbewegen',index='Gemeente').reset_index()

df_remain = df.drop(columns = ['Sportenbewegen_Percentage','Sportenbewegen']).drop_duplicates()
assert df_remain.shape[0] == df_pivot.shape[0]

df = pd.merge(df_remain,df_pivot,on=['Gemeente'], how='inner')
assert df.shape[0] == df_pivot.shape[0]

df.columns = [col.replace(' ','_') for col in df.columns]
df.to_csv('summary_gemeentenaam.csv', index=False)

# insert results into  bigquery table
client = bigquery.Client()
datasetname = 'volksgezondheidenzorg'
gemeentenaam_tab = 'volksgezondheidenzorg_gemeentenaam'

dataset_id = "{}.{}".format(client.project,datasetname)

client.delete_table('{}.{}'.format(dataset_id,gemeentenaam_tab), not_found_ok=True)  # Make an API request.
print("Deleted table '{}'.".format(gemeentenaam_tab))

df.to_gbq('{}.{}'.format(datasetname,gemeentenaam_tab))
