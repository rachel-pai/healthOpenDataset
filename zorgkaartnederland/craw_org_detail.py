# ============================================
# get the main page and substract the sublinks
# ============================================
import json
import os
from pathlib import Path

# scrapy runspider craw_org_detail.py -o data/org/detail_infos.json

url_list = []
org_list = []
with open('data/org/detail_links.json') as json_file:
    org_link_list = json.load(json_file)
    for org_link in org_link_list:
        url_list.append(org_link['link'])

import scrapy

class QuotesSpider(scrapy.Spider):
    name = 'quotes'
    start_urls = url_list
    def parse(self, response):

        org_name = response.css('div.organization_title_holder').xpath('h1/span/text()').extract()
        assert len(org_name) == 1
        other_info = response.xpath('//address//text()').extract()
        other_info = [val.replace("\n","").strip() for val in other_info]
        other_info = ' '.join([val for val in other_info if val])

        yield{
            'organization_name': org_name[0],
            'other_info':other_info,
            'link': response.url
        }


