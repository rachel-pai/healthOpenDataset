from google.cloud import bigquery
import os
import pandas as pd
import re
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'your bq credential json path'

import glob
file_list = glob.glob("./data/*.csv")

client = bigquery.Client()
datasetname = 'about_nl'

for file_path in file_list:
    print(file_path)
    df = pd.read_csv(file_path,skipinitialspace=True,delimiter=',')

    df.columns = df.columns.str.replace(' ','')
    df.columns = df.columns.str.replace('\(%\)','_percentage')
    df.columns = df.columns.str.replace('-','')

    tab_name = file_path.split('/')[-1].strip().replace('.csv','')
    tab_name = tab_name.replace('-','_')

    dataset_id = "{}.{}".format(client.project,datasetname)
    client.delete_table('{}.{}'.format(dataset_id,tab_name), not_found_ok=True)  # Make an API request.
    print("Deleted table '{}'.".format(tab_name))

    df.to_gbq('{}.{}'.format(datasetname,tab_name),)


## concate all dataframe and insert summary info into BQ
df_all = []
for file_path in file_list:
    province = file_path.split('/')[-1].replace('.csv','').split('_')[-1]
    df = pd.read_csv(file_path,skipinitialspace=True,delimiter=',')
    df['province'] = province
    df_all.append(df)

df = pd.concat(df_all)
tab_name = 'city_list_summary'

dataset_id = "{}.{}".format(client.project,datasetname)
client.delete_table('{}.{}'.format(dataset_id,tab_name), not_found_ok=True)  # Make an API request.
print("Deleted table '{}'.".format(tab_name))

df.to_gbq('{}.{}'.format(datasetname,tab_name),)

##### ==============================================
##### check how many duplicted cities
##### ==============================================
# '''
# select lower(name) as name, count(*) as app_count
# from your_project_name.about_nl.city_list_summary
# group by name
# having count(*) >2
# order by 2 DESC
# '''
#### ===============================================
