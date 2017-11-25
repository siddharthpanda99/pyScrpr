# -*- coding: utf-8 -*-
import scrapy
from scrapy import Spider


class QuotestoscrapeSpider(Spider):
    name = 'quotesToscrape'
    allowed_domains = ['toscrape.com']
    start_urls = ['http://quotes.toscrape.com/']

    def parse(self, response):
        self.log('I just visited : ' + response.url)
        for quote in response.css('div.quote'):
            item = {
                'author': quote.css('small.author::text').extract()[0],
                'text': quote.css('span.text::text').extract()[0],
                'tags': quote.css('a.tag::text').extract()
            }
            yield item
        #Follow pagination
        nextPage = response.css('li.next > a::attr(href)').extract()[0]
        if nextPage:
            nextPage = response.urljoin(nextPage)
            yield scrapy.Request(url=nextPage, callback=self.parse)
