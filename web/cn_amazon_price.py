# !/usr/bin/env python
# -*- coding: UTF-8 -*
from bs4 import BeautifulSoup
from urllib import urlopen
from datetime import datetime
import re
import cookielib
import urllib2
import urllib
import requests
from Crypto.Hash import SHA256
from datetime import datetime
from dateutil import tz
import hmac
import hashlib
import base64

import parse_brickset
from waihui import get_huilv

from database import LegoDb

class Amazon():
    """查询 amazon 网站"""

    def __init__(self):
        pass
  
    def get_aws_keys(self):
        with open('/home/dormouse/project/legohole/web/rootkey.csv') as f:
            texts = f.read().split()
            keys = dict(zip(
                ('associate_tag', 'AWS_access_key_id', 'AWS_secret_key'),
                texts
            ))
        return keys

    def get_utctime(self):
        """
        function:
            get utc time for amazon.com
        return:
            string like 2014-08-18T12:00:00Z
        """
        from_zone = tz.tzutc()
        to_zone = tz.tzlocal()
        utc = datetime.utcnow().replace(tzinfo=from_zone)
        central = utc.astimezone(to_zone)
        formated_time = central.strftime('%Y-%m-%dT%H:%M:%SZ')
        return formated_time

    def get_url(self,**args):
        """ get url for query amazon"""

        utc_time = self.get_utctime()
        keys = self.get_aws_keys()
        accept_args = (
            'AWSAccessKeyId',
            'AssociateTag',
            'Keywords',
            'Operation',
            'ResponseGroup',
            'SearchIndex',
            'Service',
            'Timestamp',
            'Version'
        )
        pars = {
            'AWSAccessKeyId':keys['AWS_access_key_id'],
            'AssociateTag':keys['associate_tag'],
            'Keywords':'lego toy',
            'Operation':'ItemSearch',
            'ResponseGroup':'ItemAttributes,Offers',
            'SearchIndex':'All',
            'Service':'AWSECommerceService',
            'Timestamp':utc_time,
            'Version':'2011-08-01'
        }
        #check args

        if args:
            for key in args.keys():
                if key not in accept_args:
                    print "error:key:%s is not acceptable,\
                        use default keys"%key
                else:
                    pars.update(args)

        print pars

        str_pars = '&'.join(
            ["%s=%s"%(k,urllib.quote(pars[k])) for k in sorted(pars.keys())]
        )
        str_unsign = '\n'.join([
            "GET",
            "webservices.amazon.cn",
            "/onca/xml",
            str_pars
        ])
        dig = hmac.new(keys['AWS_secret_key'],
                       msg=str_unsign,
                       digestmod=hashlib.sha256).digest()
        sig = base64.b64encode(dig).decode()
        sig_pre = urllib.urlencode({'Signature':sig})
        head = 'http://webservices.amazon.cn/onca/xml?'
        url = head + str_pars + '&' + sig_pre
        print url
        return url

    def get_lego_price(self, number):
        keyword = "lego %s"%number
        query_url = self.get_url(Keywords=keyword)
        xml = urlopen(query_url).read()
        price = self.parse_xml(xml)
        return price

    def save_get_lego_price(self, fname, number):
        """for test"""
        keyword = "lego %s"%number
        query_url = self.get_url(Keywords=keyword)
        print query_url
        html = urlopen(query_url).read()
        with open(fname, 'w') as f:
            f.write(html)
            
    def test_text(self, fname):
        """测试本地文档"""
        with open(fname) as f:
            price = self.parse_xml(f.read())
        print price

    def parse_xml(self, xml):
        """分析中国亚马逊搜索页面"""
        soup = BeautifulSoup(xml, "xml")
        items = soup.find_all('Item')
        if items:
            item = items[0]
            amount = item.OfferSummary.LowestNewPrice.Amount
            return amount.text if amount else None
        else:
            return None
        """
        for item in items:
            print item.ASIN.text,
            print item.Amount.text if item.Amount else '',
            print item.Model.text if item.Model else ''
        print len(items)
        """

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
    print Amazon().get_lego_price('60044')
    #Amazon().save_get_lego_price('60044')
    #test_url()
    #fname = '/home/dormouse/project/legohole/testdata/amazon_cn.xml'
    #Amazon().test_text(fname)
