# !/usr/bin/env python
# -*- coding: UTF-8 -*
from bs4 import BeautifulSoup
from urllib import urlopen
from datetime import datetime
import re
import time, sys, random
from selenium import webdriver
from waihui import get_huilv

from database import LegoDb

START = """
http://www.amazon.cn/s/ref=sr_nr_p_n_fulfilled_by_ama_0?fst=as%3Aoff&rh=i%3Aaps%2Ck%3Alego%2Cp_89%3ALEGO+%E4%B9%90%E9%AB%98%2Cp_n_fulfilled_by_amazon%3A326314071&keywords=lego&ie=UTF8
"""

def test_url():
    url = START
    while url:
        print url
        url = parse_url(url)
        random.seed()
        time.sleep(random.random()*20)

def parse_url(url):
    browser = webdriver.Firefox()
    browser.get(url)
    html = browser.page_source
    obj = parse_html(html)
    return obj

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
    prices = filter(None, [parse_div(div) for div in divs])
    for p in prices:
        p['discount'] = calc_disc(p)
    #next page
    links = soup.find_all('a', title=u'下一页')
    print links
    if len(links) == 1:
        link = links[0]['href']
        url = "http://www.amazon.cn"+link
    else:
        url = None

    obj={"prices":prices, "next_page":url}
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
    try:
        txt = spans[0].text[1:]
        price = ''.join(txt.split(','))
        
    except:
        print "error:can not get price!set number is %s"%set_number
        return {}

    # check price (float)
    if not re.search('[0-9]*\.?[0-9]*$', price):
        try:
            print "error:price is %s"%set_number
        except:
            print "error:prince is not float!"
        return {}

    # init return obj 
    obj = {'vendor':u'amazon_cn', 'price':price }
    obj['set_number'] = set_number+'-1'
    obj['datetime'] = datetime.now().strftime("%Y%m%d%H%M%S")

    return obj

def write_db():
    """把价格写入数据库"""
    obj = {}
    prices = []
    obj['start'] = datetime.now().strftime("%Y%m%d%H%M%S")
    url = START
    while url:
        print url
        result = parse_url(url)
        url = result['next_page']
        prices += result['prices']
        random.seed()
        time.sleep(random.random()*20)
    obj['end'] = datetime.now().strftime("%Y%m%d%H%M%S")
    db = LegoDb()
    db.connect_db()
    db.append_prices(prices)
    obj['content'] = 'amazon_cn'
    db.append_update_log(obj)
    db.disconnect_db()
    
if __name__ == "__main__":
    #test_url()
    write_db()
