# -*- coding: utf-8 -*-
import scrapy
import re


class SicManualSpider(scrapy.Spider):
    name = 'sic_manual'
    #allowed_domains = ['https://www.osha.gov/pls/imis/sic_manual.html']
    start_urls = ['https://www.osha.gov/pls/imis/sic_manual.html/']

    a_href = lambda self,link: link.xpath('@href').extract_first()
    a_title = lambda self,link: link.xpath('@title').extract_first()

    def page_links(self, response):
        return response.xpath('//div[@id="maincontain"]/div[@class="row-fluid"]//a[not(contains(@class, "btn"))]')

    def parse(self, response):
        for link in self.page_links(response):
            title = self.a_title(link)
            href = self.a_href(link)

            if "Division" in title:
                self.logger.info(f'Parsing {title}')
                yield response.follow(href, self.parse_division)

            elif "Group" in title:
                self.logger.info(f'Parsing {title}')
                yield response.follow(href, self.parse_group)

    def parse_division(self, response):
        yield {
        'divsion_title': response.css('html body div#wrapper div#maincontain.container div.row-fluid h2 ::text').extract_first(),
        #'division_description': " ".join(response.css('#maincontain > div:nth-child(1) > div:nth-child(2) ::text').extract())
        }

    def parse_group(self, response):
        yield {
        'major_group_title': response.css('html body div#wrapper div#maincontain.container div.row-fluid h2 ::text').extract_first()
        #'major_group_description': " ".join(response.css('html body div#wrapper div#maincontain.container div.row-fluid div span.blueTen ::text').extract())
        }

        for link in self.page_links(response):
            yield {
            'industry_title' : self.a_title(link)
            }
