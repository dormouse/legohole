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

def test_set_txt():
    with open('70155-1.html') as f:
        datas = parse_set(f.read())

def clean(txt):
    if txt:
        return txt.strip()
    else:
        return None

def parse_set(html):
    soup = BeautifulSoup(html)
    divs = soup.find_all('div', class_='text')
    # get set details
    dts = divs[0].find_all('dt')
    dds = divs[0].find_all('dd')
    dt_strings = [clean(dt.string) for dt in dts]
    dd_strings = [clean(dd.string) for dd in dds]
    set_details = dict(zip(dt_strings, dd_strings))
    print dt_strings.index('Minifigs')
    print 'price' in dt_strings
    if 'Tags' in dt_strings:
        dd = dds[dt_strings.index('Tags')]
        alist = dd.find_all('a')
        tags = []
        for a in alist:
            tags.append({'link':a['href'],
                         'name':clean(a.string)})
        set_details['Tags'] = tags

    if 'Pieces' in dt_strings:
        dd = dds[dt_strings.index('Pieces')]
        set_details['Pieces'] = {'count':int(clean(dd.string)),
                                 'link':dd.a['href']}

    if 'Minifigs' in dt_strings:
        dd = dds[dt_strings.index('Minifigs')]
        set_details['Minifigs'] = {'count':int(clean(dd.string)),
                                 'link':dd.a['href']}

    if 'RRP' in dt_strings:
        strings = dd_strings[dt_strings.index('RRP')].split('/')
        rrps = [clean(rrp) for rrp in strings]
        prieces = {}
        for rrp in rrps:
            if rrp[0] == u'£':
                prieces['gbp'] = float_cur(rrp)
            if rrp[0] == u'$':
                prieces['usd'] = float_cur(rrp)
            if rrp[0] == u'€':
                prieces['eur'] = float_cur(rrp)
        set_details['RRP'] = prieces

    if 'Age range' in dt_strings:
        age_str = dd_strings[dt_strings.index('Age range')]
        if u'-' in age_str:
            ages = age_str.split('-')
            set_details['Age range'] = {
                'start':int(clean(ages[0])),
                'end':int(clean(ages[1]))
            }
        else:
            if u'+' in age_str:
                set_details['Age range'] = {
                    'start':int(age_str[:-1]),
                    'end':99
                }
            else:
                set_details['Age range'] = {
                    'start':None,
                    'end':None
                }



    print set_details
    """
    print set_details

    {u'Set number': u'70155-1',
    u'Price per piece': u'13.500p / 17.554c / 20.257c',
    u'Name': u'Inferno Pit', u'Weight': u'0.15Kg (0.33 lb)',
    u'Year released': u'2014', u'Minifigs': u'1',
    u'Subtheme': u'Speedorz', u'Tags': None,
    u'Packaging': u'Box with backing card', u'Pieces': u'74',
    u'Set type': u'Normal', u'Theme': u'Legends of Chima',
    u'Age range': u'7 - 14', u'Dimensions': None, u'Theme group':
    u'Action/Adventure', u'Rating': None, u'Barcodes': None,
    u'Availability': u'Retail',
    u'RRP': u'\xa39.99 / $12.99 / \u20ac14.99'}
    None:Tags, Dimensions, Rating, Barcodes
    """
    data_names = (
        'number', 'name', 'type', 'theme_group', 'theme', 'sub_theme',
        'year', 'tags', 'pieces', 'pieces_link', 'minifigs',
        'minifigs_link' , 'rrp_gbp', 'rrp_usd', 'rrp_eur',
        'age_start', 'age_end', 'packaging',
        'dimensions_cm_l','dimensions_cm_w','dimensions_cm_h',
        'dimensions_in_l','dimensions_in_w','dimensions_in_h',
        'weight_kg', 'weight_lb', 'upc', 'ean', 'availability',
        'ava_at_lego'
    )
    datas = {}
    datas['number'] = set_details['Set number']
    datas['name'] = set_details['Name']
    datas['type'] = set_details['Name']



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

def test_uk_url():
    base_url = 'http://brickset.com'
    buy_uk_url = '/buy/vendor-amazon/country-uk/order-percentdiscount/page-3'
    text = urllib.urlopen(base_url + buy_uk_url).read()
    parse_buy_UK(text)

def test1():
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
    test_set_txt()

