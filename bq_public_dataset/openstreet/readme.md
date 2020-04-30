Search dutch planet node in bigquery-public-data.geo_openstreetmap table.

Steps:
1. run [openstreet_plante_node_nl.sql](openstreet_plante_node_nl.sql) on BQ console
2. save result json file locally, converted into newline delimited json, save into google storage
```bash
cat bq-results-20200420-161910-9gf3j6oy9gil.json | jq -c '.[]' > bq-results-20200420-161910-9gf3j6oy9gil_NDJSON.json
```
3. run [insertBQ.py](insertBQ.py)
   - change uri into your gs path
   - change GOOGLE_APPLICATION_CREDENTIALS path
