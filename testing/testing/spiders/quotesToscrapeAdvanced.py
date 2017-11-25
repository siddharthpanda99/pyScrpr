# -*- coding: utf-8 -*-
import scrapy
from scrapy import Spider


class QuotestoscrapeSpider(Spider):
    name = 'quotesToscrape'
    allowed_domains = ['toscrape.com']
    start_urls = ['http://quotes.toscrape.com/']

    def parse(self, response):
        urls = response.css('div.quote > span > a::attr(href)').extract()
        for url in urls:
            url = response.urljoin(url)
            yield scrapy.Request(url=url, callback=self.parseDetails)
        # self.log('I just visited : ' + response.url)
        # for quote in response.css('div.quote'):
        #     item = {
        #         'author': quote.css('small.author::text').extract()[0],
        #         'text': quote.css('span.text::text').extract()[0],
        #         'tags': quote.css('a.tag::text').extract()
        #     }
        #     yield item
        #Follow pagination
        nextPage = response.css('li.next > a::attr(href)').extract()[0]
        if nextPage:
            nextPage = response.urljoin(nextPage)
            yield scrapy.Request(url=nextPage, callback=self.parse)
    def parseDetails(self, response):
        yield {
                'name': response.css('h3.author-title::text').extract()[0],
                'birth_date': response.css('span.author-born-date::text').extract()[0]
              }
