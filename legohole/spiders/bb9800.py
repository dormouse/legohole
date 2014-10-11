# -*- coding: utf-8 -*-
import scrapy


class Bb9800Spider(scrapy.Spider):
    name = "bb9800"
    allowed_domains = ["bb9800.diandian.com"]
    start_urls = (
        'http://bb9800.diandian.com/',
    )
    def _get_text(self, res, path):
        strings = res.xpath(path).extract()
        return ''.join(strings).strip()

    def parse(self, response):
        #get all posts
        posts = response.xpath('//div[starts-with(@class,"post")]')
        for post in posts:
            h1 = post.xpath('div[@class="entry"]/h1')
            if len(h1) == 1:
                #we have title!
                title = self._get_text(h1, 'a/text()')
                link = self._get_text(h1, 'a/@href')
                print title
                print link
            else:
                #we have no title
                #get date
                day = self._get_text(post, 'div[@class="date"]/span/text()')
                month = self._get_text(post, 'div[@class="date"]/text()')
                print day
                print month



            #for entry in entries:
                #yield scrapy.Request(link, callback=self.parse_single_page)

    def parse_single_page(self, response):
        title = response.xpath('//h1/text()').extract()
        texts = response.xpath('//div[@id="byline"]/text()')
        publish_time = (texts.extract()[0].split("\r\n")[1]).strip()
        contents = response.xpath('//div[@class="content"]/p')

        print title
        print publish_time


