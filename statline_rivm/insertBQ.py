from google.cloud import bigquery
import os
import pandas as pd

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'your bq credential json path'
import glob

# def insert_bq(filepath, prefix=''):
file_list = glob.glob("./dataset/metadata/*.csv")

client = bigquery.Client()
datasetname = 'statline_rivm'

for file_path in file_list:
    print(file_path)

    df = pd.read_csv(file_path,skipinitialspace=True,delimiter=';')
    df.columns = df.columns.str.replace('"','')
    df.columns = df.columns.str.replace(' ','')
    df.columns = df.columns.str.replace('\(','_')
    df.columns = df.columns.str.replace('\)','')
    df.columns = df.columns.str.replace('/','_')
    df.columns = df.columns.str.replace('>','more_than_')
    df.columns = df.columns.str.replace('<','less_than_')
    df.columns = df.columns.str.replace('+','above')

    thesis_tab = 'metadata_'+file_path.split('/')[-1].strip().replace('.csv','')
    thesis_tab = thesis_tab.replace(' ','_')
    thesis_tab = thesis_tab.replace('-','')
    thesis_tab = thesis_tab.replace('\(','')
    thesis_tab = thesis_tab.replace('\)','')

    dataset_id = "{}.{}".format(client.project,datasetname)
    client.delete_table('{}.{}'.format(dataset_id,thesis_tab), not_found_ok=True)  # Make an API request.
    print("Deleted table '{}'.".format(thesis_tab))

    df.to_gbq('{}.{}'.format(datasetname,thesis_tab),)
