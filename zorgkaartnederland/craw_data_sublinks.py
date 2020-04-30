# ============================================
# get the main page and substract the sublinks
# ============================================
import json
import os
from pathlib import Path

# scrapy runspider craw_data_sublinks.py -o data/org/caretype_sub_links.json
# scrapy runspider craw_data_sublinks.py -o data/doc/healthCare_typetype_sub_links.json

url_list = []
org_list = []

# with open('data/org/caretype_links.json') as json_file:
with open('data/org/caretype_links.json') as json_file:
    org_link_list = json.load(json_file)
    for org_link in org_link_list:
        # org_list.append(org_link['healthCare_type'])
        org_list.append(org_link['healthCare_type'])
        url_list.append(org_link['link'])

import scrapy

class QuotesSpider(scrapy.Spider):
    name = 'quotes'
    start_urls = url_list
    def parse(self, response):
        try:
            max_pag_no = response.css('ul.pagination').xpath('li/a//text()')[-1].get().strip()
            if int(max_pag_no):
                yield {
                    'parent_link':response.url,
                    'max_pag':int(max_pag_no)
                }
        except:
            pass


