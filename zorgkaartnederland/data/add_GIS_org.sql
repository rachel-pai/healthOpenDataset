SELECT
REGEXP_EXTRACT(other_info , r"^Adres\s*(.*?)\s\d{4}\s*[a-zA-Z]{2}\s.+?\s*\b(?:Telefoon|Website|Locatie|$)") AS address,
REGEXP_EXTRACT(other_info , r"^Adres\s*.*?\s(\d{4}\s*[a-zA-Z]{2})\s.+?\s*\b(?:Telefoon|Website|Locatie|$)") AS postcode,
REGEXP_EXTRACT(other_info , r"^Adres\s*.*?\s\d{4}\s*[a-zA-Z]{2}\s(.+?)\s*\b(?:Telefoon|Website|Locatie|$)") AS city,
REGEXP_EXTRACT(other_info , r"^.*Telefoon\s([\d-]*)") AS tel,
REGEXP_EXTRACT(other_info , r"^.*\sWebsite\s(.*nl)") AS web,
REGEXP_EXTRACT(other_info , r".*\sLocatie(.*)") AS remark,
organization_name_x as organization_name, healthCare_type, link, other_info
from your_project_name.zorgkaartnederland.care_provider_organization
