import json
import pandas as pd
from google.cloud import bigquery
import os

def create_df(file_path,col_names,rename_cols=''):

    temp_list = [[],[],[],[],[]]
    temp_list = temp_list[:len(col_names)]
    with open(file_path) as json_file:
        org_link_list = json.load(json_file)
        for org_link in org_link_list:
            for idx in range(len(col_names)):
                temp_list[idx].append(org_link[col_names[idx]])


    if rename_cols:
        col_new_names = rename_cols
    else:
        col_new_names = col_names

    data = {}
    for idx in range(len(col_names)):
        data[col_new_names[idx]] = temp_list[idx]

    df = pd.DataFrame(data=data)

    return df

# medical organization
pd.options.display.max_rows = None
pd.options.display.max_columns = None
pd.set_option('display.max_colwidth', -1)

di = create_df('data/org/detail_infos.json',['organization_name','other_info','link'])
cl = create_df('data/org/caretype_links.json',['healthCare_type','link'],['healthCare_type','parent_link'])
dl = create_df('data/org/detail_links.json',['organization_name','parent_link','link'])

# remove pagina in parent url
dl['parent_link'] = dl['parent_link'].replace({r'^(https:\/\/www\.[a-zA-Z\d\.\/-]+)\/pagina\d+$':'\\1'}, regex=True)

hct = pd.merge(dl, cl, on='parent_link',how='left')
df = pd.merge(di, hct, on='link',how='left') #organization_name

# df.to_csv('data/org/medic_org.csv',index=False)

# # medical operators
ddi = create_df('data/doc/doc_detail_infos.json',['doc_name','job','other_info','link','org_link'])
ddi['org_link'] = ddi['org_link'].apply(lambda x:'https://www.zorgkaartnederland.nl'+x[0])
ddi.drop_duplicates(inplace=True)

dcl = create_df(file_path='data/doc/jobtype_links.json',col_names = ['job','link'],rename_cols = ['job','parent_link'])
ddl = create_df('data/doc/doc_detail_links.json',['doc_name','parent_link','link'])
# remove pagina_number
ddl['parent_link'] = ddl['parent_link'].replace({r'^(https:\/\/www\.[a-zA-Z\d\.\/-]+)\/pagina\d+$':'\\1'}, regex=True)
dhct = pd.merge(ddl, dcl, on='parent_link',how='left')
ddf = pd.merge(ddi, dhct, on=['link'],how='left') #'doc_name','job'

# print(ddf[ddf['parent_link'].isnull()].head(5))
# print(ddf[ddf['parent_link'].isnull()].shape)

ddf = ddf[ddf['parent_link'].notnull()]

ddf.to_csv('data/doc/medical_doc.csv',index=False)

##===================
# Insert data into BQ
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'your bq credential json path'

client = bigquery.Client()
datasetname = 'zorgkaartnederland'
med_org_table = 'care_provider_organization'
med_doc_table = 'care_provider_person'

# TODO(developer): Set table_id to the ID of the table to fetch.
dataset_id = "{}.{}".format(client.project,datasetname)

client.delete_table('{}.{}'.format(dataset_id,med_org_table), not_found_ok=True)  # Make an API request.
print("Deleted table '{}'.".format(med_org_table))

client.delete_table('{}.{}'.format(dataset_id,med_doc_table), not_found_ok=True)  # Make an API request.
print("Deleted table '{}'.".format(med_doc_table))

df.to_gbq('{}.{}'.format(datasetname,med_org_table))
ddf.to_gbq('{}.{}'.format(datasetname,med_doc_table))
