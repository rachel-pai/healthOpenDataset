with org_gis as(
SELECT REPLACE(postcode, ' ', '') as postcode
from `your_project_name.zorgkaartnederland.care_provider_organization_GIS`
where postcode is not null
)

select *
from bigquery-public-data.geo_openstreetmap.planet_nodes,
UNNEST(all_tags) as all_tags_exp,org_gis
where all_tags_exp.key = 'addr:postcode' and all_tags_exp.value = org_gis.postcode

-- save into json for nested data
-- can not directly import into bigquery tale since location is different (US VS Europe (europe-west2 London))
-- run command: cat results-20200411-154759.json | jq -c '.[]' > results-20200411-154759NDJSON.json  (transfer json into newline delimited json (ndjson))
