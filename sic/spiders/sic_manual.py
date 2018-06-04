# -*- coding: utf-8 -*-
import scrapy
import re


class SicManualSpider(scrapy.Spider):
    name = 'sic_manual'
    #allowed_domains = ['https://www.osha.gov/pls/imis/sic_manual.html']
    start_urls = [
        'https://www.osha.gov/pls/imis/sic_manual.html',
        ]

    page_links = lambda self,response: response.xpath('//div[@id="maincontain"]/div[@class="row-fluid"]//a[not(contains(@class, "btn"))]')
    a_href = lambda self,link: link.xpath('@href').extract_first()
    a_title = lambda self,link: link.xpath('@title').extract_first()
    parse_description = lambda self, response: " ".join(response.css('html body div#wrapper div#maincontain.container div.row-fluid div span.blueTen ::text').extract())

    def parse(self, response):
        print(self.a_title(self.page_links(response)[0]))
        for link in self.page_links(response):
            title = self.a_title(link)
            href = self.a_href(link)

            if "Division" in title:
                self.logger.info(f'Parsing {title}')
                #yield response.follow(href, self.parse_division)

            elif "Group" in title:
                self.logger.info(f'Parsing {title}')
                yield response.follow(href, self.parse_group)

    def parse_division(self, response):
        yield {
        'divsion_title': response.css('html body div#wrapper div#maincontain.container div.row-fluid h2 ::text').extract_first(),
        'division_description': " ".join(response.css('#maincontain > div:nth-child(1) > div:nth-child(2) ::text').extract())
        }

    def parse_group(self, response):
        yield {
        'major_group_title': response.css('html body div#wrapper div#maincontain.container div.row-fluid h2 ::text').extract_first(),
        'major_group_description': parse_description(response)
        }

        for link in self.page_links(response):
            self.logger.info(f'Parsing Industry {self.a_title(link)}')
            yield response.follow(self.a_href(link), self.parse_industry)

    def parse_industry(self, response):
        structure = response.css('html body div#wrapper div#maincontain.container div.row-fluid p a').xpath('@title')
        division = lambda s: re.search(r'Division\s([A-Z])\:\s(.*)', s[0].extract())
        major = lambda s: re.search(r'Major\sGroup\s([0-9]{2})\:\s(.*)', s[1].extract())

        def industry_group(response):
            return (re.search(r'Industry\sGroup\s(\d{3})\:\s(.*)',
            response.css('html body div#wrapper div#maincontain.container div.row-fluid p ::text')
            .extract()[-2])
            )

        def examples(response):
            return [ex.strip() for ex in response.css('html body div#wrapper div#maincontain.container div.row-fluid div ul li ::text').extract()]

        yield {
        'division': division(structure).group(1),
        'division_title': division(structure).group(2),
        'major_group': major(structure).group(1),
        'major_group_title': major(structure).group(2),
        'industry_group_number': industry_group(response).group(1),
        'industry_group_title': industry_group(response).group(2),
        'industry_group_description': self.parse_description(response),
        'industry_group_examples': examples(response)
        }
