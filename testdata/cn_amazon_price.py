# !/usr/bin/env python
# -*- coding: UTF-8 -*
from bs4 import BeautifulSoup
from urllib import urlopen
from datetime import datetime
import re
import mechanize
import cookielib
import urllib2
import urllib

import parse_brickset
from waihui import get_huilv

from database import LegoDb
"""
http://www.amazon.cn/s/ref=sr_pg_1?fst=as%3Aoff&rh=n%3A647070051%2Cn%3A1982062051%2Ck%3Alego%2Cp_89%3ALEGO+%E4%B9%90%E9%AB%98&keywords=lego&ie=UTF8&qid=1429923502

base_url = 'http://brickset.com'
buy_uk_url = '/buy/vendor-amazon/country-uk/order-percentdiscount/page-1'
text = urlopen(base_url + buy_uk_url).read()
soup = BeautifulSoup(text)
divs = soup.find_all('div', class_='tags hideonmediumscreen')
for div in divs:
    set_url = base_url + div.a['href']
"""
def test_url():
    base_url = "http://www.amazon.cn"
    url = "http://www.amazon.cn/s/keywords=lego&ie=UTF8"

    html = request_ajax_data(url)
    obj = parse_html(html)
    np = obj['next_page']
    print np
    html = request_ajax_data(base_url + np)
    obj = parse_html(html)
    np = obj['next_page']
    print np

    
    """
    while url:
        print url
        url = parse_url(url)
    """
def request_ajax_data(url):
    req = urllib2.Request(url)
    req.add_header('Content-Type',
                   'application/x-www-form-urlencoded; charset=UTF-8')
    req.add_header('X-Requested-With','XMLHttpRequest')
    req.add_header('User-Agent',
                   'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 \
                   (KHTML, like Gecko) Chrome/27.0.1453.116')
    response = urllib2.urlopen(req)
    jsonText = response.read()
    return jsonText

def parse_url(url):
    html = urlopen(url).read()
    obj = parse_html(html)
    #write_db(obj['prices'])
    return obj['next_page']

def test_text():
    """测试本地文档"""
    with open('amazon_cn.html') as f:
        obj = parse_html(f.read())
    #write_db(obj['prices'])

def parse_html(html):
    """分析中国亚马逊搜索页面"""

    soup = BeautifulSoup(html)
    divs = soup.find_all('div', class_='s-item-container')
    if len(divs) != 24:
        print "warning:number of item is %d not 24"%len(divs)
    prices = [parse_div(div) for div in divs]
    for p in prices:
        p['discount'] = calc_disc(p)

    #next page
    links = soup.find_all('a', title=u'下一页')
    print links
    if len(links) == 1:
        link = links[0]['href']
    else:
        link = None

    obj={"prices":prices, "next_page":link}
    return obj

def calc_disc(price):
    """ calc discount"""
    number = price.get('set_number')
    if number:
        set_number = number + '-1'
    else:
        return None

    rmb_p = price.get('price')
    if rmb_p:
        db = LegoDb()
        db.connect_db()
        row = db.query_brickset(True, 'usprice', number=set_number)
        us_rate = db.query_huilv()['usd']
        db.disconnect_db()
        if row and row['usprice']:
            us_p = float(row['usprice']) * float(us_rate) /100
            disc = round(float(rmb_p) / us_p * 100, 2)
        else:
            return None
    return disc 


def parse_div(div):
    """
    function:
        parse single div of item
    return:
        dict like {
            'set_number': u'60044',
            'vendor': u'amazon_cn',
            'price': u'254.00',
            'datetime': '20150425103635'
        }
    """
    # get set number
    h2 = div.find_all('h2')
    if len(h2) != 1:
        print "warning:number of name not 1"
    name = h2[0].text
    m = re.search("\d+", name)
    if m:
        set_number = m.group()
    else:
        try:
            print "error:can not get set number, name is %s"%name
        except:
            print "error:can not get set number!"
        return {}

    # get price
    spans = div.find_all(
        'span', class_='a-size-base a-color-price s-price a-text-bold'
    )
    if len(spans) != 1:
        print "warning:number of price not 1"
    price = spans[0].text[1:]
    # check price (float)
    if not re.search('[0-9]*\.?[0-9]*$', price):
        try:
            print "error:price is %s"%set_number
        except:
            print "error:prince is not float!"
        return {}

    # init return obj 
    obj = {'set_number':set_number, 'price':price }
    obj['datetime'] = datetime.now().strftime("%Y%m%d%H%M%S")
    obj['vendor'] = u'amazon_cn'

    return obj

def parse_buy_uk_tr(tr):

    obj = {}
    tds = tr.find_all('td')
    obj['set_number'] = tds[1].div.a.text

    if tds[2].text == u'(Marketplace)':
        obj['vendor'] = u'amazon_uk_MP'
    else:
        obj['vendor'] = u'amazon_uk'

    price_span = tr.find_all('span', class_='price')[0]
    price = price_span.text
    obj['price'] = price[1:] 

    obj['datetime'] = datetime.now().strftime("%Y%m%d%H%M%S")

    return obj

def write_db(prices):
    """把价格写入数据库"""
    obj = {}
    db = LegoDb()
    db.connect_db()
    obj['start'] = datetime.now().strftime("%Y%m%d%H%M%S")
    db.append_prices(prices)
    obj['end'] = datetime.now().strftime("%Y%m%d%H%M%S")
    obj['content'] = 'amazon_cn'
    db.append_update_log(obj)
    db.disconnect_db()


    
if __name__ == "__main__":
    test_url()
