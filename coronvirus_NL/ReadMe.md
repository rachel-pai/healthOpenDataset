# CoronaVirus info in NL
## Aim:
Combinding other info( such as the each city weather info, healthcare oraganization amount in each city, population info etc) to find which info is important in influencing infected number.

## Method:
1. Linear relationship (correlation) between features and infected number
2. Non-linear relation (randomforest feature importance and permutation feature importance for predicting infected number

## Data explation:
coron_municipality.csv is download from [CoronaWatchNL](https://github.com/J535D165/CoronaWatchNL/blob/master/data/rivm_NL_covid19_total_municipality.csv)

## steps:
1. Insert coron_municipality,csv into BQ: `python insertBQ.py`
2. Combining other healthcare-related info into a temp.csv file: `python comvined_all_data.py`
3. Run RF_importance.ipynb
