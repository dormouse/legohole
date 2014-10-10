# -*- coding: utf-8 -*-
import scrapy


class Bb9800Spider(scrapy.Spider):
    name = "bb9800"
    allowed_domains = ["www.nphoto.net"]
    start_urls = (
        'http://www.nphoto.net/news/',
    )

    def parse(self, response):
        articles = response.xpath('//div[@class="article"]')
        for article in articles:
            link = article.xpath('table/tr/td/a/@href')[0].extract()
            title = article.xpath('table//span/text()')[0].extract()
            print title
            print link
            yield scrapy.Request(link, callback=self.parse_single_page)

    def parse_single_page(self, response):
        title = response.xpath('//h1/text()').extract()
        texts = response.xpath('//div[@id="byline"]/text()')
        publish_time = (texts.extract()[0].split("\r\n")[1]).strip()
        contents = response.xpath('//div[@class="content"]/p')

        print title
        print publish_time


