# -*- coding: utf-8 -*-
import scrapy


class SicManualSpider(scrapy.Spider):
    name = 'sic_manual'
    allowed_domains = ['https://www.osha.gov/pls/imis/sic_manual.html']
    start_urls = ['http://https://www.osha.gov/pls/imis/sic_manual.html/']

    def parse(self, response):
        pass
