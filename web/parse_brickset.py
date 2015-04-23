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

def get_brickset_price_by_set_number(set_number):
    base_url = 'http://brickset.com'
    price_ajax_url = base_url+'/ajax/sets/buy'
    ajax_request_body = {"set":set_number}
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

    #print prices
    #{'FR': {'asin': 'B00546V9HI', 'cp': 19.99, 'rp': 31.9, 'mp': 19.48},
    # 'CA': {'asin': 'B004P957ZU', 'cp': 78.9, 'rp': 39.99, 'mp': 36.98},
    # 'DE': {'asin': 'B00546V9HI', 'cp': 31.4, 'rp': 29.99, 'mp': 17.75},
    # 'IT': {'asin': 'B00546V9HI', 'cp': 25.88, 'rp': 29.99, 'mp': 19.48},
    # 'US': {'asin': 'B004P957ZU', 'cp': 35.97, 'rp': 29.99, 'mp': 19.4},
    # 'UK': {'asin': 'B00546V9HI', 'cp': 14.49, 'rp': 25.99, 'mp': 13.98}}

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

    if u'Tags' in dt_strings:
        dd = dds[dt_strings.index('Tags')]
        alist = dd.find_all('a')
        tags = []
        for a in alist:
            tags.append({'link':a['href'],
                         'name':clean(a.string)})
        set_details['Tags'] = tags

    if u'Pieces' in dt_strings:
        dd = dds[dt_strings.index('Pieces')]
        set_details['Pieces'] = {'count':int(clean(dd.string)),
                                 'link':dd.a['href']}

    if u'Minifigs' in dt_strings:
        dd = dds[dt_strings.index('Minifigs')]
        set_details['Minifigs'] = {'count':int(clean(dd.string)),
                                 'link':dd.a['href']}

    if u'RRP' in dt_strings:
        #零售价格
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

    if u'Age range' in dt_strings:
        #年龄范围
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

    if u'Dimensions' in dt_strings:
        #体积
        dd = dds[dt_strings.index('Dimensions')]
        #厘米
        str_tmp = clean(dd.contents[0])[:-2]
        cms = [float(clean(i)) for i in str_tmp.split('x')]
        #英寸
        str_tmp = clean(dd.contents[2])[1:-3]
        ins = [float(clean(i)) for i in str_tmp.split('x')]
        set_details['Dimensions'] = { 'cm':cms, 'in':ins }
                    
    if u'Weight' in dt_strings:
        weight_str = dd_strings[dt_strings.index('Weight')]
        str_tmp = weight_str.split('Kg')
        kg = float(clean(str_tmp[0]))
        lb = float(clean(str_tmp[1].split('lb')[0])[1:])
        set_details['Weight'] = { 'kg':kg, 'lb':lb }

    if u'Barcodes' in dt_strings:
        dd = dds[dt_strings.index('Barcodes')]
        upc = clean(dd.contents[0])[5:]
        ean = clean(dd.contents[2])[5:]
        set_details['Barcodes'] = { 'upc':upc, 'ean':ean } 
    print set_details
    """
    print set_details

    {u'Set number': u'70155-1',
    u'Price per piece': u'13.500p / 17.554c / 20.257c',
    u'Name': u'Inferno Pit', u'Weight': {'lb': 0.33, 'kg': 0.15},
    u'Year released': u'2014',
    u'Minifigs': {
        'count': 1,
        'link': 'http://brickset.com/minifigs/inset-70155-1'
    },
    u'Subtheme': u'Speedorz',
    u'Tags': [
        {'link': 'http://brickset.com/sets/tag-Fluminox',
        'name': u'Fluminox'},
        {'link': 'http://brickset.com/sets/tag-Fire-And-Ice',
        'name': u'Fire And Ice'},
        {'link': 'http://brickset.com/sets/tag-Fire-Chi',
        'name': u'Fire Chi'},
        {'link': 'http://brickset.com/sets/tag-Phoenix-Tribe',
        'name': u'Phoenix Tribe'}
    ],
    u'Packaging': u'Box with backing card',
    u'Pieces': {'count': 74,
        'link': 'http://brickset.com/inventories/70155-1'
    },
    u'Set type': u'Normal', u'Theme': u'Legends of Chima',
    u'Age range': {'start': 7, 'end': 14},
    u'Dimensions': {'cm': [28.2, 24.2, 5.4], 'in': [11.1, 9.5, 2.1]},
    u'Theme group': u'Action/Adventure', u'Rating': None,
    u'Barcodes': {'upc': u'673419211024', 'ean': u'5702015124744'},
    u'Availability': u'Retail',
    u'RRP': {'usd': 12.99, 'gbp': 9.99, 'eur': 14.99}}
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



def test_price_txt():
    with open('ajax.txt') as f:
        prices = parse_price(f.read())

    set_id = '70161-1'
    #prices = get_brickset_price_by_set_number(set_id)

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
    buy_uk_url = '/buy/vendor-amazon/country-uk/order-percentdiscount/page-1'
    text = urllib.urlopen(base_url + buy_uk_url).read()
    parse_buy_UK(text)

def test_uk_text():
    with open('buy_uk.html') as f:
        parse_buy_UK(f.read())

def parse_buy_UK(html):
    soup = BeautifulSoup(html)
    divs = soup.find_all('div', class_='tags hideonmediumscreen')
    set_ids = [div.a.string for div in divs]
    for set_id in set_ids:
        output(set_id)

def output(set_id):
    prices = get_brickset_price_by_set_number(set_id)
    print set_id
    if prices.has_key('UK') and prices.has_key('US'):
        #format output
        print u'£%s'%prices['UK']['cp'],'\t',
        print u'￥%.2f'%prices['UK']['cp_rmb'],'\t',
        print u'%.2f%%'%(prices['UK']['cp_disc']*100),'\t',

        print u'$%s'%prices['US']['cp'],'\t',
        print u'￥%.2f'%prices['US']['cp_rmb'],'\t',
        print u'%.2f%%'%(prices['US']['cp_disc']*100),'\t'

if __name__ == '__main__':
    #test_set_txt()
    #test_uk_url()
    test_price_txt()

