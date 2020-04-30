import pandas as pd
import json
import google
import re

from google.cloud import bigquery
import os
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'your bq credential json path'


class bq:
    def __init__(self,json_file,month,accuweather_link_file,bq_table_name):
        self.json_file = json_file
        self.month = month
        self.city_weather_links = pd.read_csv(accuweather_link_file)

        self._bq_table_name = bq_table_name
        self.client = bigquery.Client()
        self._datasetname = 'accuweather'
        self._dataset_id = "{}.{}".format(self.client.project,self._datasetname)
        self._table_id = '{}.{}'.format(self._dataset_id,self._bq_table_name)
        self.get_month_name()

    @property
    def datasetname(self):
        return self._datasetname
    @property
    def dataset_id(self):
        return self._dataset_id
    @property
    def table_id(self):
        return self._table_id
    @property 
    def bq_table_name(self):
        return self._bq_table_name
    @property
    def month_name(self):
        return self._month_name

    def get_month_name(self):
        month_num_name = ['january','february','march','april','may','june','july','august','september','october','november','december']
        self._month_name = month_num_name[int(self.month-1)]

    def read_weather_file(self):
        date_list,highest_temp,lowest_tempp,hist_Gemiddeld_low,hist_Gemiddeld_high,link_list = [],[],[],[],[],[]
        with open(self.json_file) as json_file:
        # with open('data/org/caretype_links.json') as json_file:
            weather_list = json.load(json_file)
            for weather_info in weather_list:
                if ('-' in weather_info['date']) or ('/' in weather_info['date']):
                    pass
                else:
                    date_list.append('2020-'+str(self.month)+'-'+weather_info['date'])
                    highest_temp.append(weather_info['highest temp'].replace('degree',''))
                    lowest_tempp.append(weather_info['lowest temp'].replace('degree',''))
                    hist_gemid = weather_info['Hist.Gemiddeld'].replace('degree','')
                    hist_Gemiddeld_low.append(re.search(r'(\d*)-{1}(-*\d*)', hist_gemid).group(2))
                    hist_Gemiddeld_high.append(re.search(r'(\d*)-{1}(-*\d*)', hist_gemid).group(1))
                    link_list.append(weather_info['link'])

        self.df = pd.DataFrame(data={'date':date_list,'high_temp_degree':highest_temp,'low_temp_degree':lowest_tempp,
                                'hist_Gemiddeld_degree_low':hist_Gemiddeld_low,'hist_Gemiddeld_degree_high':hist_Gemiddeld_high,
                                'link':link_list})

        self.df['date'] =  pd.to_datetime(self.df['date'],format='%Y-%m-%d')

        temp = self.city_weather_links.copy()
        temp['link']=temp['link'].apply(lambda x:x.replace('march',self._month_name))
        self.df = pd.merge(self.df,temp,on='link',how='left')

        self.df = self.df.astype({'high_temp_degree':int,'low_temp_degree':int,'hist_Gemiddeld_degree_low':int,
                            'hist_Gemiddeld_degree_high':int})

    def save_df(self):
        if 'today' in self.json_file:
            self.df.to_csv('df_current.csv', index=False)
        else:
            self.df.to_csv('df_'+self._month_name+'.csv', index=False)

    def bq_table_exist(self):
        try:
            self.client.get_table(self._table_id)
            return True
        except google.cloud.exceptions.NotFound:
            return False

    def bq_delete_table(self):
        self.client.delete_table(self._table_id, not_found_ok=True)

    def create_dataset(self):
        try:
            # Construct a full Dataset object to send to the API.
            dataset = bigquery.Dataset(self._dataset_id)
            dataset.location = "europe-west2"
            dataset = self.client.create_dataset(dataset)  # Make an API request.
            print("Created dataset {}.{}".format(self.client.project, dataset.dataset_id))
        except google.api_core.exceptions.Conflict:
            pass


    def insert_data(self):
        # dataset_ref = client.dataset(datasetname)
        job_config = bigquery.LoadJobConfig()

        job_config.schema = [
            bigquery.SchemaField("date", "DATE",mode="NULLABLE"),
            bigquery.SchemaField("high_temp_degree", "INT64",mode="NULLABLE",description="highest temperature during the day (degree)"),
            bigquery.SchemaField("low_temp_degree", "INT64",mode="NULLABLE",description="lowest temperature during the day (degree)"),
            bigquery.SchemaField("hist_Gemiddeld_degree_low", "INT64",mode="NULLABLE", description="Historical Average highest temperature (degree) "),
            bigquery.SchemaField("hist_Gemiddeld_degree_high", "INT64",mode="NULLABLE", description="Historical Average lowerst temperatire (degree)"),
            bigquery.SchemaField("link", "STRING",mode="NULLABLE",description="webpage link"),
            bigquery.SchemaField("Gemeentenaam", "STRING",mode="NULLABLE",description="Gemeentenaam"),
            bigquery.SchemaField("Provincienaam", "STRING",mode="NULLABLE",description="Provincienaam"),
        ]

        job = self.client.load_table_from_dataframe(self.df, self._table_id, job_config=job_config)
        # Wait for the load job to complete.
        job.result()

    def update_data(self,df,table_id = None):
        if table_id:
            df.to_gbq(table_id,if_exists = 'append')
        else:
            df.to_gbq(self._table_id,if_exists = 'append')

    def bq_execute_query(self,query):
        return self.client.query(query).to_dataframe()

    def save_archieved_data(self):
        print("reading files and generating dataframe...")
        self.read_weather_file()
        print("saving datframe into csv file")
        self.save_df()
        print("inserting data into bigquery tables...")
        self.bq_delete_table()
        self.insert_data()


april_bq = bq('weather_info_april.json',4,'accuweather_links.csv','accuweather_april')
april_bq.save_archieved_data()

march_bq = bq('weather_info_march.json',3,'accuweather_links.csv','accuweather_march')
march_bq.save_archieved_data()

feb_bq = bq('weather_info_february.json',2,'accuweather_links.csv','accuweather_feb')
feb_bq.save_archieved_data()

today_bq = bq('weather_info_today.json',int(pd.datetime.now().month),'accuweather_links.csv','accuweather_current')
today_bq.read_weather_file()
today_bq.save_df()

# if accuweather_current table already exist, transfer the data into corresponding month-archieved table
table_exist = today_bq.bq_table_exist()
if table_exist == True:
    q= 'select * from your_project_name.'+today_bq.datasetname+'.'+today_bq.bq_table_name
    df = today_bq.bq_execute_query(q)

    today_bq.update_data(df,'{}.{}'.format(today_bq.dataset_id,'accuweather_'+today_bq.month_name))

# delete table and update current date weather info
today_bq.bq_delete_table()
today_bq.insert_data()
