# ============================================
# get the main page and substract the sublinks
# ============================================
import json
import scrapy

# scrapy runspider craw_detail_links.py -o data/org/detail_links.json
# scrapy runspider craw_detail_links.py -o data/doc/doc_detail_links.json

url_list = []

with open('data/org/caretype_links.json') as json_file:
# with open('data/org/caretype_links.json') as json_file:
    org_link_list = json.load(json_file)
    for org_link in org_link_list:
        url_list.append(org_link['link'])

with open('data/org/caretype_sub_links.json') as json_file:
# with open('data/org/caretype_sub_links.json') as json_file:
    org_link_list = json.load(json_file)
    for org_link in org_link_list:
        max_pag_no = org_link['max_pag']
        for pag_no in range(1,max_pag_no+1):
            url_list.append(org_link['parent_link']+'/pagina'+str(pag_no))

# remove duplicates
url_list = list(set(url_list))

class QuotesSpider(scrapy.Spider):
    name = 'quotes'
    start_urls = url_list
    def parse(self, response):
        for quote in response.xpath('//ul[@id="results"]//li'):
            for lis in quote.css('div.media-body').xpath('h4'):
                link = lis.xpath('a/@href').get().strip()
                yield {
                    'organization_name': lis.xpath('a/text()').get(),
                    # 'organization_name': lis.xpath('a/text()').get(),
                    'parent_link':response.url,
                    'link':'https://www.zorgkaartnederland.nl'+link
                }



