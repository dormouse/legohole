# !/usr/bin/env python
# -*- coding: UTF-8 -*
from bs4 import BeautifulSoup
from datetime import datetime
import urllib
from dateutil import tz
import hmac
import hashlib
import base64

class Amazon():
    """查询 amazon 网站"""

    def __init__(self, key_file):
        self.key_file = key_file
  
    def get_aws_keys(self):
        with open(self.key_file) as f:
            texts = f.read().split()
            keys = dict(zip(
                ('AWS_access_key_id', 'AWS_secret_key'),
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

    def sign_url(self, local, pars):
        """
        function:
            sing url of amazon
        arguments:
            local: short name of Country
            pars:  query pars
        return:
            signed_url: signed url of amazon
        """

        associate_tags = {
            'BR':'',
            'CA':'',
            'CN':'mousecat-23',
            'DE':'',
            'ES':'',
            'FR':'',
            'IN':'',
            'IT':'bb98000c-21',
            'JP':'',
            'UK':'bb9800-21',
            'US':'mousecat-20'
        }

        #check tag
        if local not in associate_tags.keys():
            print "local %s not in associate_tags"%local
            return None

        keys = self.get_aws_keys()
        utc_time = self.get_utctime()
        signs = {
            'AWSAccessKeyId':keys['AWS_access_key_id'],
            'AssociateTag':associate_tags[local],
            'Service':'AWSECommerceService',
            'Timestamp':utc_time,
            'Version':'2011-08-01'
        }
        pars.update(signs)
        endpoints = {
            'BR':'webservices.amazon.com.br',
            'CA':'webservices.amazon.ca',
            'CN':'webservices.amazon.cn',
            'DE':'webservices.amazon.de',
            'ES':'webservices.amazon.es',
            'FR':'webservices.amazon.fr',
            'IN':'webservices.amazon.in',
            'IT':'webservices.amazon.it',
            'JP':'webservices.amazon.co.jp',
            'UK':'webservices.amazon.co.uk',
            'US':'webservices.amazon.com'
            }

        url_pars = '&'.join(
            ["%s=%s"%(k, urllib.quote(pars[k])) for k in sorted(pars.keys())]
        )
        str_unsign = '\n'.join(
            ["GET", endpoints[local], "/onca/xml", url_pars]
        )
        dig = hmac.new(keys['AWS_secret_key'],
                       msg=str_unsign,
                       digestmod=hashlib.sha256).digest()
        sig = base64.b64encode(dig).decode()
        url_sig = urllib.urlencode({'Signature':sig})
        signed_url = "http://%s/onca/xml?%s&%s"%(
            endpoints[local], url_pars, url_sig
        )
        return signed_url

    def get_lego_price(self, local, **args):

        # default pars
        pars = {
            'ResponseGroup':'ItemAttributes,OfferFull'
        }
        # search by ASIN
        if args.get('ASIN'):
            pars.update({
                'Operation':'ItemLookup',
                'ItemId':args.get('ASIN'),
                'IdType':'ASIN',
            })
        # search by lego number
        if args.get('number'):
            pars.update({
                'Operation':'ItemSearch',
                'Keywords':"lego %s"%(args.get('number')),
                'SearchIndex':'Toys',
            })

        if local != 'CN':
            pars['MerchantId'] = 'Amazon'

        url = self.sign_url(local, pars)
        print url
        xml = urllib.urlopen(url).read()
        price = self.parse_xml(xml)
        return price

    def save_xml(self, fname, xml):
        with open(fname, 'w') as f:
            f.write(xml)
            
    def test_text(self, fname):
        """测试本地文档"""
        with open(fname) as f:
            price = self.parse_xml(f.read())
        print price

    def parse_xml(self, xml):
        """分析中国亚马逊搜索页面"""
        soup = BeautifulSoup(xml, "xml")
        offers = soup.find_all('Offer')
        if offers:
            offer = offers[0]
            amount = offer.OfferListing.Price.Amount
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

if __name__ == "__main__":
    key_file = '/home/dormouse/project/legohole/web/rootkey.csv'
    amazon = Amazon(key_file)
    print amazon.get_lego_price('CN', number='60044')
    #print amazon.get_lego_price('US', number='60046')
    #print amazon.get_lego_price('US', ASIN='B00GSPF9QQ') 
    #print amazon.get_lego_price('UK', number='60044')
    #print amazon.get_lego_price('CN', ASIN='B00VG1X1JY') 
    #fname = '/home/dormouse/project/legohole/testdata/amazon_cn.xml'
    #Amazon().test_text(fname)
