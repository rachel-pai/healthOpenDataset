# ============================================
# get the main page and substract the sublinks
# ============================================
import json
import os
from pathlib import Path

# scrapy runspider craw_doc_detail.py -o data/doc/doc_detail_infos.json

url_list = []
org_list = []
with open('data/doc/doc_detail_links.json') as json_file:
    org_link_list = json.load(json_file)
    for org_link in org_link_list:
        url_list.append(org_link['link'])

import scrapy

class QuotesSpider(scrapy.Spider):
    name = 'quotes'
    start_urls = url_list
    def parse(self, response):

        doc_name = response.css('div.organization_title_holder').xpath('h1/text()').extract()
        job = response.css('div.organization_title_holder').xpath('p/text()').extract()

        assert len(doc_name) == 1
        assert len(job) == 1

        other_info = response.xpath('//address//text()').extract()
        other_info = [val.replace("\n","").strip() for val in other_info]
        other_info = ' '.join([val for val in other_info if val])

        org_link = response.xpath('//address//@href').extract()

        job = job[0].strip()
        yield{
            'doc_name': doc_name[0].strip().replace(job,'').strip(),
            'job':job,
            'other_info':other_info,
            'link': response.url,
            'org_link':org_link
        }


