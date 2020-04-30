# Web Crawler for [zorgkaartnederland](https://www.zorgkaartnederland.nl/)

This website provide infomations about 129,758 healthcare providers.

## Steps:
1. run run.sh to crawl data from [zorgkaartnederland](https://www.zorgkaartnederland.nl/)
2. run [insert_bq.py](insert_bq.py) to insert data into bigqeury
3. in biquery,
    - run [correct_wrong_data.sql](data/correct_wrong_data.sql)
    - run [add_GIS_org.sql](data/add_GIS_org.sql) and save results into new table named  original_table_name+ '_GIS'
    - [add_GIS_doc.sql](data/add_GIS_doc.sql) and save results into new table named  original_table_name+ '_GIS'


