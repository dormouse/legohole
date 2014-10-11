# -*- coding: utf-8 -*-

# Scrapy settings for legohole project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'legohole'

SPIDER_MODULES = ['legohole.spiders']
NEWSPIDER_MODULE = 'legohole.spiders'
# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'legohole (+http://www.yourdomain.com)'
#BOT_NAME = 'manta'
 
DOWNLOAD_TIMEOUT = 15
DOWNLOAD_DELAY = 2
COOKIES_ENABLED = True
COOKIES_DEBUG = True
RETRY_ENABLED = False
 
USER_AGENT = "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.22 (KHTML, like Gecko) Chrome/25.0.1364.97 Safari/537.22 AlexaToolbar/alxg-3.1"
 
DEFAULT_REQUEST_HEADERS={
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en',
    'X-JAVASCRIPT-ENABLED': 'true',
}
 
DOWNLOADER_MIDDLEWARES = {
    'scrapy.contrib.downloadermiddleware.useragent.UserAgentMiddleware': 400,
    'scrapy.contrib.downloadermiddleware.cookies.CookiesMiddleware':700,
}
