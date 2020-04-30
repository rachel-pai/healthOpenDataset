# -*- coding: utf-8 -*-
'''
Insert results from saved openstreet_plante_node_nl.sql into new table
'''
from google.cloud import bigquery
import os
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'your bq credential json path'

client = bigquery.Client()
datasetname = 'public_dataset_NL'
table_name ='planet_node_NL'
dataset_id = "{}.{}".format(client.project,datasetname)
client.delete_table('{}.{}'.format(dataset_id,table_name), not_found_ok=True)  # Make an API request.
print("Deleted table '{}'.".format(table_name))

dataset_ref = client.dataset(datasetname)
job_config = bigquery.LoadJobConfig()

job_config.schema = [
    bigquery.SchemaField("id", "INT64",mode="NULLABLE",description="Object unique ID."),
    bigquery.SchemaField("version", "INT64",mode="NULLABLE",description="Version number for this object."),
    bigquery.SchemaField("username", "STRING",mode="NULLABLE",description="Name of user who created this version of the object."),
    bigquery.SchemaField("changeset", "INT64",mode="NULLABLE", description="Changeset number for this object."),
    bigquery.SchemaField("visible", "Boolean",mode="NULLABLE",description="Is this version of the object visible?"),
    bigquery.SchemaField("osm_timestamp", "Timestamp",mode="NULLABLE",description="Last-modified timestamp for this object."),
    bigquery.SchemaField("geometry", "GEOGRAPHY",mode="NULLABLE",description="GEOGRAPHY-encoded point"),
    bigquery.SchemaField(
        "all_tags",
        "RECORD",
        mode="REPEATED",
        description="Unstructured key=value attributes for this object.",
        fields=[
            bigquery.SchemaField("key", "STRING", mode="NULLABLE",description="Attribute key."),
            bigquery.SchemaField("value", "STRING", mode="NULLABLE",description="Attribute value.")
        ],
    )
]
job_config.source_format = bigquery.SourceFormat.NEWLINE_DELIMITED_JSON
uri = "gs://your json file path"

load_job = client.load_table_from_uri(
    uri,
    dataset_ref.table('planet_node_NL'),
    location='europe-west2',  # Location must match that of the destination dataset.
    job_config=job_config,
)  # API request
print("Starting job {}".format(load_job.job_id))

load_job.result()  # Waits for table load to complete.
print("Job finished.")

destination_table = client.get_table(dataset_ref.table("planet_node_NL"))
print("Loaded {} rows.".format(destination_table.num_rows))
