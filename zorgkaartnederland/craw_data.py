# -*- coding: utf-8 -*-
# pip install scrapy==1.8.0
# scrapy runspider craw_data.py -o data/org/caretype_links.json
# scrapy runspider craw_data.py -o data/doc/healthCare_typetype_links.json

import scrapy

class QuotesSpider(scrapy.Spider):
    name = 'quotes'
    start_urls = [
        "https://www.zorgkaartnederland.nl/overzicht/organisatietypes"
    ]
    def parse(self, response):
        for quote in response.css('div.content_section_inner').xpath('ul'):
            for lis in quote.css('li.list-group-item'):
                link = lis.xpath('a/@href').get().strip()
                yield {
                    'healthCare_type': lis.xpath('a/text()').get(),
                    'link':'https://www.zorgkaartnederland.nl'+link
                }

