# -*- coding: utf-8 -*-
import scrapy


class Bb9800Spider(scrapy.Spider):
    name = "bb9800"
    allowed_domains = ["www.nphoto.net"]
    start_urls = (
        'http://www.nphoto.net/news/',
    )

    def parse(self, response):

        print "========================="
        articles = response.xpath('//div[@class="article"]')
        for article in articles:
            link = article.xpath('table/tr/td/a/@href')[0].extract()
            title = article.xpath('table//span/text()')[0].extract()
            print title
            print link

