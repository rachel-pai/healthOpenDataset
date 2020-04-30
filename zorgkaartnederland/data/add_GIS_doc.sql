SELECT
REGEXP_EXTRACT(per_gis.other_info , r"^Geslacht\s([a-zA-Z]+\s)") AS Geslacht,
REGEXP_EXTRACT(per_gis.other_info , r"^[\w\s]*Specialisme\s(.+)\sWerkzaam") AS Specialisme,
REGEXP_EXTRACT(per_gis.other_info , r"^.*Werkzaam\sbij\s(.*)+") AS Werkplaats,
per_gis.other_info,
per_gis.doc_name_x as doc_nam, per_gis.job_x as job, org_gis.address as org_address,
org_gis.postcode as org_postcode, org_gis.city as org_city, org_gis.tel as org_tel,
org_gis.web as org_web, org_gis.remark as org_remark, org_gis.organization_name as org_name,
org_gis.healthCare_type as org_type, org_gis.place_name as org_place_name,
org_gis.state_name as org_state_name, org_gis.county_name as org_county_name,
org_gis.latitude as org_latitude, org_gis.longitude as org_longitude
from `your_project_name.zorgkaartnederland.care_provider_person` per_gis
inner join `your_project_name.zorgkaartnederland.care_provider_organization_GIS` org_gis
on org_gis.link = per_gis.org_link
