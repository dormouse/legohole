# !/usr/bin/env python
# -*- coding: UTF-8 -*
import time, sys, random
import os
import json
import urllib2
import urllib
from bs4 import BeautifulSoup
import sqlite3 as sqlite
from datetime import datetime

from database import LegoDb

def down_thumbs(set_numbers):
    random.seed()
    time.sleep(random.random()*10)
    thumb_urls = [make_thumb_url(set_number) for set_number in set_numbers]
    thumb_target_path = "/home/dormouse/project/legohole/web/static/pic/thumb"
    image_urls = [make_image_url(set_number) for set_number in set_numbers]
    image_target_path = "/home/dormouse/project/legohole/web/static/pic/image"
    for url in image_urls:
        download(url, image_target_path)
    #http://images.brickset.com/sets/images/70706-1.jpg
    #http://images.brickset.com/sets/large/70706-1.jpg

def make_thumb_url(set_number):
    imgurl = ''.join(
        ('http://images.brickset.com/sets',
         '/thumbs/tn_%s_jpg.jpg'%set_number))
    return imgurl

def make_image_url(set_number):
    imgurl = ''.join((
        'http://images.brickset.com/sets',
        '/images/%s.jpg'%set_number))
    return imgurl

def download(url, target_path):
    fname = os.path.join(target_path, url.split('/')[-1])
    if not os.path.exists(fname):
        os.system("wget -nv -P %s %s"%(target_path, url))

def download_pics():
    db = LegoDb()
    db.connect_db()
    rows = db.query_brickset(False, 'number')
    numbers = [row['number'] for row in rows]
    db.disconnect_db()
    down_thumbs(numbers)

if __name__ == '__main__':
    download_pics()
