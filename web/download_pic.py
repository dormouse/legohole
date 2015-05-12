# !/usr/bin/env python
# -*- coding: UTF-8 -*
import time
import random
import os

from database import LegoDb

def down_thumbs(set_numbers):
    random.seed()
    time.sleep(random.random()*10)
    thumb_urls = [make_thumb_url(set_number) for set_number in set_numbers]
    thumb_target_path = "/home/dormouse/project/legohole/web/static/pic/thumb"
    image_urls = [make_image_url(set_number) for set_number in set_numbers]
    image_target_path = "/home/dormouse/project/legohole/web/static/pic/image"
    large_urls = [make_large_url(set_number) for set_number in set_numbers]
    large_target_path = "/home/dormouse/project/legohole/web/static/pic/large"
    for url in large_urls:
        download(url, large_target_path)
    #http://images.brickset.com/sets/images/70706-1.jpg
    #http://images.brickset.com/sets/large/70706-1.jpg

def make_jobs(set_number):
    """make brickset url by set number"""
    jobs = []
    base_url = 'http://images.brickset.com/sets'
    thumb_url = base_url + '/thumbs/tn_%s_jpg.jpg'%set_number
    image_url = base_url + '/images/%s.jpg'%set_number
    large_url = base_url + '/large/%s.jpg'%set_number
    base_target_path =  "/home/dormouse/project/legohole/web/static/pic"
    thumb_target_path = base_target_path + "/thumb"
    image_target_path = base_target_path + "/image"
    large_target_path = base_target_path + "/large"
    jobs.append((thumb_url, thumb_target_path))
    jobs.append((image_url, image_target_path))
    jobs.append((large_url, large_target_path))
    return jobs

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

def make_large_url(set_number):
    imgurl = ''.join((
        'http://images.brickset.com/sets',
        '/large/%s.jpg'%set_number))
    return imgurl

def download(url, target_path):
    random.seed()
    #time.sleep(random.random()*10)
    fname = os.path.join(target_path, url.split('/')[-1])
    if not os.path.exists(fname):
        os.system("wget -nv -P %s %s"%(target_path, url))

def download_pics():
    db = LegoDb()
    db.connect_db()
    rows = db.query_brickset(False, 'number')
    numbers = [row['number'] for row in rows]
    db.disconnect_db()
    for number in numbers:
        jobs = make_jobs(number)
        for url, target in jobs:
            download(url, target)

if __name__ == '__main__':
    download_pics()
