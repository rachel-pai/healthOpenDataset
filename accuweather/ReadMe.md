# Collecting weather info in Netherland

## accuweather_links.csv: each city corresponding weather link in [accuweather](https://www.accuweather.com/)
## Prerequest:
`pip install scrapy==1.8.0`
### Steps:
1. collect today weather info: `scrapy runspider craw_data_current.py -o weather_info_today_mis.json`
2. collect history weather info (feberary):  `scrapy runspider craw_data.py -o weather_info_feb.json`
    -  if you want to collect april weather info:
        change code
        ```
        weather_df['link']=weather_df['link'].apply(lambda x:x.replace('march','february'))
        ```
        into
        ```
        weather_df['link']=weather_df['link'].apply(lambda x:x.replace('march','april'))
        ```
        Then run:
        `scrapy runspider craw_data.py -o weather_info_april.json`

        so does march

3. Inserting data into bigquery tables: `python insertBQ.py'
