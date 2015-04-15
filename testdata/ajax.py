# !/usr/bin/env python
# -*- coding: UTF-8 -*

import json
import urllib2
import urllib
from bs4 import BeautifulSoup

def request_ajax_data(url,data,referer=None,**headers):
    req = urllib2.Request(url)
    req.add_header('Content-Type',
                   'application/x-www-form-urlencoded; charset=UTF-8')
    req.add_header('X-Requested-With','XMLHttpRequest')
    req.add_header('User-Agent',
                   'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 \
                   (KHTML, like Gecko) Chrome/27.0.1453.116')
    if referer:
        req.add_header('Referer',referer)
    if headers:
        for k in headers.keys():
            req.add_header(k,headers[k])

    params = urllib.urlencode(data)
    response = urllib2.urlopen(req, params)
    jsonText = response.read()
    return jsonText
    #return json.loads(jsonText)

def get_brickset_price_by_setid(set_id):
    base_url = 'http://brickset.com'
    price_ajax_url = base_url+'/ajax/sets/buy'
    ajax_request_body = {"set":set_id}
    ajax_response = request_ajax_data(price_ajax_url, ajax_request_body)
    return parse_price(ajax_response)

def float_cur(s):
    """货币文字转换为浮点数"""
    return float(s.strip()[1:])

def parse_price(html):
    """分析HTML"""

    bs = BeautifulSoup(html)
    trs =  bs.find_all('tr')[1:]
    prices = {}
    for tr in bs.find_all('tr')[1:]:
        tds = tr.find_all('td')
        #当前价格
        current_price = float_cur(tds[2].span.string)
        #零售价格
        retail_price = float_cur(tds[3].string)
        #最低价格
        min_price = float_cur(tds[4].contents[0])
        #购买链接
        amazon_url = tds[6].a['href']
        #amazon 网站货物编号
        amazon_asin = amazon_url.split('=')[-1]
        #国家
        country = tds[0].img['src'].split('/')[-1].split('.')[0].upper()
        
        #列表内容
        contents = ('cp', 'rp', 'mp', 'asin')
        prices[country] = dict(zip(contents,
                (current_price, retail_price, min_price, amazon_asin)))

    #货币简称
    currencies = ('GBP', 'CAD', 'EUR', 'EUR', 'EUR', 'EUR', 'USD')
    #货币符号
    currency_symbols = (u'£', u'$', u'€', u'€', u'€', u'€', u'$')
    #列表内容
    contents = ('cp', 'rp', 'mp', 'asin')
    #计算折扣
    gbp_rate = 9.2042
    usd_rate = 6.2209
    if prices.has_key('UK') and prices.has_key('US'):
        #英镑退税后人民币当前价格
        prices['UK']['cp_rmb'] = prices['UK']['cp'] * gbp_rate / 1.2
        #美元人民币当前价格
        prices['US']['cp_rmb'] = prices['US']['cp'] * usd_rate
        #美元人民币零售价格
        prices['US']['rp_rmb'] = prices['US']['rp'] * usd_rate
        #英镑退税后人民币当前价格折扣
        prices['UK']['cp_disc'] = prices['UK']['cp_rmb']/prices['US']['rp_rmb']
        #美元人民币当前价格折扣
        prices['US']['cp_disc'] = prices['US']['cp_rmb']/prices['US']['rp_rmb']

    return prices

def test1():
    with open('ajax.txt') as f:
        parse_price(f.read())

    set_id = '70161-1'
    prices = get_brickset_price_by_setid(set_id)
    #format output
    print set_id,
    print u'£%s'%prices['UK']['cp'],
    print u'￥%.2f'%prices['UK']['cp_rmb'],
    print u'%.2f%%'%(prices['UK']['cp_disc']*100)

    print set_id,
    print u'$%s'%prices['US']['cp'],
    print u'￥%.2f'%prices['US']['cp_rmb'],
    print u'%.2f%%'%(prices['US']['cp_disc']*100)

def test2():
    base_url = 'http://brickset.com'
    buy_uk_url = '/buy/vendor-amazon/country-uk/order-percentdiscount/page-1'
    text = urlopen(base_url + buy_uk_url).read()
    soup = BeautifulSoup(text)
    divs = soup.find_all('div', class_='tags hideonmediumscreen')
    for div in divs:
        set_url = base_url + div.a['href']

def test():
    with open('buy_uk.html') as f:
        parse_buy_UK(f.read())

def parse_buy_UK(html):
    base_url = 'http://brickset.com'
    soup = BeautifulSoup(html)
    divs = soup.find_all('div', class_='tags hideonmediumscreen')
    set_ids = [div.a.string for div in divs]
    for set_id in set_ids:
        output(set_id)

def output(set_id):
    prices = get_brickset_price_by_setid(set_id)
    if prices.has_key('UK') and prices.has_key('US'):
        #format output
        print set_id,
        print u'£%s'%prices['UK']['cp'],
        print u'￥%.2f'%prices['UK']['cp_rmb'],
        print u'%.2f%%'%(prices['UK']['cp_disc']*100),

        print u'$%s'%prices['US']['cp'],
        print u'￥%.2f'%prices['US']['cp_rmb'],
        print u'%.2f%%'%(prices['US']['cp_disc']*100)

if __name__ == '__main__':
    test()

