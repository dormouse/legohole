# !/usr/bin/env python
# -*- coding: UTF-8 -*
import time
import random
import os
import requests
from datetime import datetime
import logging

from database import LegoDb

class BSHtmlDownloader():
    """download brickset html"""

    def __init__(self):
        #setup logger
        log_file = 'bs_download.log'
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.DEBUG)
        fh = logging.FileHandler(log_file)
        fh.setLevel(logging.DEBUG)
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        ch.setFormatter(formatter)
        fh.setFormatter(formatter)
        self.logger.addHandler(ch)
        self.logger.addHandler(fh)
        random.seed()

    def init_db(self):
        db = LegoDb()
        db.connect_db()
        db.create_table('bshtml')
        db.disconnect_db()

    def download_bshtmls(self):
        # get all lego number
        db = LegoDb()
        db.connect_db()
        sql = "select number from brickset order by number"
        rows = db.query_db(sql)
        numbers = [row['number'] for row in rows]
        db.disconnect_db()
        for number in numbers:
            if self.need_download(number):
                self.download_bshtml(number)
                # wait ...
                time.sleep(random.random()*100)
            else:
                self.logger.debug("%s skipped"%number)

    def need_download(self, number):
        """ check number need to download
        if status_code is 200 or 404, then need not download.
        """

        sql = """
            select lego_number, status_code from bshtml
            where lego_number = ? and (
                status_code = ? or status_code = ?)
        """
        args = (number, 200, 404)
        db = LegoDb()
        db.connect_db()
        if db.query_db(sql, args, True):
            need_download = False
        else:
            need_download = True
        db.disconnect_db()
        return need_download 

    def download_bshtml(self, number):
        # download
        url = "http://brickset.com/sets/" + number
        not_ok = True
        while not_ok:
            try:
                r = requests.get(url)
                not_ok = False
            except requests.exceptions.ConnectionError:
                self.logger.debug(
                    "%s Connection aborted. Waiting..."%number
                )
                time.sleep(random.random()*1000)

        data = {
            'status_code': r.status_code,
            'lego_number': number,
            'url': url,
            'html': (r.content).decode('utf-8'),
            'datetime': datetime.now().strftime("%Y%m%d%H%M%S"),
        }
        self.write_db(data)

    def write_db(self, data):
        db = LegoDb()
        db.connect_db()
        table = 'bshtml'
        fields = ('status_code', 'lego_number', 'url', 'html',
                  'datetime')
        db.append_db(table, fields, data)
        db.disconnect_db()
        self.logger.debug(
            "%s status:%s"%(data['lego_number'],data['status_code'])
        )

if __name__ == '__main__':
    bsd = BSHtmlDownloader()
    bsd.download_bshtmls()

