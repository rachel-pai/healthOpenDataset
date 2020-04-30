# Collecting data from [OpenData RIVM](https://statline.rivm.nl/#/RIVM/nl/)

## File Structure
- data: contain data download from [RIVM](https://statline.rivm.nl/#/RIVM/nl/)
- metadata: Explaining some variable
- metadata2: metadata downlaod from [RIVM](https://statline.rivm.nl/#/RIVM/nl/)
- sql_scripts: combining metadata into data
- insertBQ.py: insert downloaded files under data directory into bigquery. N.B table name is the download file name.

## Steps:
1. download files
2. run insertBQ.py
3. run sql scripts and save correpsonding table into 'combined_'+raw_table name. \
N.B. [kosten_van_ziekten2017_rivm.sql](dataset/sql_scripts/kosten_van_ziekten2017_rivm.sql) combined kosten_van_ziekten2017_rivm1 to kosten_van_ziekten2017_rivm33 since I downloaded 33 csv files for this tabke. Likewise, [gezondheid_per_wijk_en_buurt2016.sql](dataset/sql_scripts/gezondheid_per_wijk_en_buurt2016.sql) contains 3 files. Remeber to change to your corresponding file amounts.
