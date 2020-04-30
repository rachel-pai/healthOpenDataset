from google.cloud import bigquery
import os
import pandas as pd
import re
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'your bq credential json path'

import glob
file_list = glob.glob("./data/*.csv")

client = bigquery.Client()
datasetname = 'coronvirus_NL'

for file_path in file_list:
    df = pd.read_csv(file_path,skipinitialspace=True,delimiter=',')
    df.columns = df.columns.str.replace('-','_')

    thesis_tab = file_path.split('/')[-1].strip().replace('.csv','')

    dataset_id = "{}.{}".format(client.project,datasetname)
    client.delete_table('{}.{}'.format(dataset_id,thesis_tab), not_found_ok=True)  # Make an API request.
    print("Deleted table '{}'.".format(thesis_tab))

    df.to_gbq('{}.{}'.format(datasetname,thesis_tab),)
