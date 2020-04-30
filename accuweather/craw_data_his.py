# -*- coding: utf-8 -*-
# pip install scrapy==1.8.0
# scrapy runspider craw_data.py -o weather_info_feb.json

import scrapy
from scrapy import Request
import pandas as pd
weather_df = pd.read_csv('accuweather_links.csv')

weather_df['link']=weather_df['link'].apply(lambda x:x.replace('march','february')) #february
links_list = weather_df['link'].values.tolist()

class QuotesSpider(scrapy.Spider):
    name = 'quotes'
    start_urls = links_list
    # to avoid 403 return
    def start_requests(self):
        # headers= {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:48.0) Gecko/20100101 Firefox/48.0'}
        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            # 'Accept-Language': 'en-US,en;q=0.8',
            # 'Connection': 'keep-alive',
            # 'DNT': '1',
            'origin': 'https://www.accuweather.com',
            'referer': 'https://www.accuweather.com/',
            # 'Host': 'www5.apply2jobs.com',
            # 'Referer': 'https://www5.apply2jobs.com/jupitermed/ProfExt/index.cfm?fuseaction=mExternal.showJob&RID=2524&CurrentPage=2',
            'Upgrade-Insecure-Requests': '1',
           'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36'
        }
        for url in self.start_urls:
                yield Request(url, headers=headers,callback=self.parse)

    def parse(self, response):
        for quote in response.css('a.is-past'):
            res = quote.xpath('div//text()').extract()
            res = [res[0]]+ [res[2]] + [res[4]]+[res[7]]+[res[9]]
            res = [val.replace('\n','').replace('\t','').replace('\u00b0','degree') for val in res]

            yield {
                # '2020-'+res[0].split('/')[1]+'-'+res[0].split('/')[0] if '/' in res[0] else '2020-4-'+res[0].strip(),
                    'date':res[0],
                    'highest temp':res[1].strip(),
                    'lowest temp':res[2].strip(),
                    'Hist.Gemiddeld':res[4].replace('degree/','-').strip(),
                    'link':response.url
                }
