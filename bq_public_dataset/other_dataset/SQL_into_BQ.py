# -*- coding: utf-8 -*-
'''
Search data in 'bigquery-public-data' dataset and save the result into a new table
N.B. the new table should be the same location as bigquery-public-data, which is 'US'
'''
from google.cloud import bigquery
import os
import google
import glob

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'your bq credential json path'

client = bigquery.Client()
datasetname = 'public_dataset_NL'
dataset_id = "{}.{}".format(client.project,datasetname)

try:
    # Construct a full Dataset object to send to the API.
    dataset = bigquery.Dataset(dataset_id)
    # dataset.location = "europe-west2" ## should be the same location with the query dataset
    dataset = client.create_dataset(dataset)  # Make an API request.
    print("Created dataset {}.{}".format(client.project, dataset.dataset_id))
except google.api_core.exceptions.Conflict:
    pass

file_list = glob.glob("./SQL_scripts/*.sql")

for file_obj in file_list:
    tabname = file_obj.split('/')[-1].replace('.sql','').strip()

    table_id = '{}.{}'.format(dataset_id,tabname)
    client.delete_table(table_id, not_found_ok=True)  # Make an API request.
    print("Deleted table '{}'.".format(tabname))

    # create table
    # schema = [bigquery.SchemaField(colnames[idx],datatype_bq[idx],mode =model_bq[idx]) for idx,val in enumerate(datatype_bq)]
    # table = bigquery.Table(table_id, schema=schema)
    # table = client.create_table(table)  # Make an API request.
    # print("Created table {}.{}.{}".format(table.project, table.dataset_id, table.table_id))

    # Set the destination table and use_legacy_sql to True to use
    job_config = bigquery.QueryJobConfig(
        allow_large_results=True,
        destination=table_id)

    File_object = open(file_obj,"r+")
    sql_content = File_object.readlines()
    sql_content = ''.join(sql_content)

    # Start the query, passing in the extra configuration.
    query_job = client.query(sql_content, job_config=job_config)  # Make an API request.
    query_job.result()  # Wait for the job to complete.

    print("Query results loaded to the table {}".format(table_id))
