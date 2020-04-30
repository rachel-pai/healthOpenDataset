#!/usr/bin/env bash

scrapy runspider craw_data.py -o data/org/caretype_links.json
scrapy runspider craw_data_sublinks.py -o data/org/caretype_sub_links.json
scrapy runspider craw_detail_links.py -o data/org/detail_links.json
scrapy runspider craw_org_detail.py -o data/org/detail_infos.json

# remove the org in Linux system
sed -i.org 's/https:\/\/www.zorgkaartnederland.nl\/overzicht\/organisatietypes/https:\/\/www.zorgkaartnederland.nl\/overzicht\/beroepen/g' craw_data.py
sed -i.org 's/healthCare_type/job/g' craw_data.py

sed -i.org 's/data\/org\/caretype_links.json/data\/doc\/jobtype_links.json/g' craw_data_sublinks.py
sed -i.org 's/healthCare_type/job/g' craw_data_sublinks.py

sed -i.org 's/data\/org\/caretype_links.json/data\/doc\/jobtype_links.json/g' craw_detail_links.py
sed -i.org 's/data\/org\/caretype_sub_links.json/data\/doc\/jobtype_sub_links.json/g' craw_detail_links.py
sed -i.org 's/organization_name/doc_name/g' craw_detail_links.py

scrapy runspider craw_data.py -o data/doc/jobtype_links.json
scrapy runspider craw_data_sublinks.py -o data/doc/jobtype_sub_links.json
scrapy runspider craw_detail_links.py -o data/doc/doc_detail_links.json
scrapy runspider craw_doc_detail.py -o data/doc/doc_detail_infos.json

## convert the file back
#sed -i.org 's/https:\/\/www.zorgkaartnederland.nl\/overzicht\/beroepen/https:\/\/www.zorgkaartnederland.nl\/overzicht\/organisatietypes/g' craw_data.py
#sed -i.org 's/job/healthCare_type/g' craw_data.py
#
#sed -i.org 's/data\/doc\/jobtype_links.json/data\/org\/caretype_links.json/g' craw_data_sublinks.py
#sed -i.org 's/job/healthCare_type/g' craw_data_sublinks.py
#
sed -i.org 's/data\/doc\/jobtype_links.json/data\/org\/caretype_links.json/g' craw_detail_links.py
sed -i.org 's/data\/doc\/jobtype_sub_links.json/data\/org\/caretype_sub_links.json/g' craw_detail_links.py
sed -i.org 's/doc_name/organization_name/g' craw_detail_links.py
