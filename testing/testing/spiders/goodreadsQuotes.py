# -*- coding: utf-8 -*-
import scrapy
from scrapy import Spider


class QuotestoscrapeSpider(Spider):
    name = 'quotesToscrape'
    allowed_domains = ['goodreads.com']
    start_urls = ['https://www.goodreads.com/quotes/']

    def parse(self, response):
        self.log('I just visited : ' + response.url)
        for quote in response.css('div.quoteDetails'):
            item = {
                'author': quote.css('a.authorOrTitle::text').extract()[0],
                'text': quote.css('div.quoteText::text').extract()[0]
            }
            yield item
        #Follow pagination
        nextPage = response.css('div > a.next_page::attr(href)').extract()[0]
        if nextPage:
            nextPage = response.urljoin(nextPage)
            yield scrapy.Request(url=nextPage, callback=self.parse)
