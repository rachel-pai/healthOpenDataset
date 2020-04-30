WITH ORG_CITY AS (select city, count(*) AS org_count
from your_project_name.zorgkaartnederland.care_provider_organization_GIS
group by city),

DOC_CIRTY AS (
select org_city, count(*) AS doc_count
from your_project_name.zorgkaartnederland.care_provider_person_GIS
group by org_city),

DOC_ORG_CITY AS (
select ORG_CITY.*, DOC_CIRTY.* EXCEPT (org_city)
from ORG_CITY
inner join DOC_CIRTY
on ORG_CITY.city = DOC_CIRTY.org_city)

select cm.*,DOC_ORG_CITY.* EXCEPT (city)
from `your_project_name.coronvirus_NL.coron_municipality` cm
inner join DOC_ORG_CITY
on cm.Gemeentenaam = DOC_ORG_CITY.city

