# List of cities in Netherlandsdown
##  Steps:
1. Load data from [List of cities, towns and villages in the Netherlands by province](https://en.wikipedia.org/wiki/List_of_cities,_towns_and_villages_in_the_Netherlands_by_province)
2. Pre-processing:
replace ? with 'unknown'
replace 'Hengelo (o)' with 'Hengelo'
replace `([a-zA-Z\-()\[\]\'ëöéúâ\s\.]*),([a-zA-Z\-()\[\]\'ëöéúâ\s\.]*),.*` with `$1,$2`
replace 'Bergen' in [city_list_Limburg.csv](data/city_list_Limburg.csv) with 'Bergen (l.)'
replace 'Bergen' in [city_list_NoordHolland.csv](data/city_list_NoordHolland.csv) with 'Bergen (nh.)'
3. Insert into bigquery
