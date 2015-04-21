# !/usr/bin/env python
# -*- coding: UTF-8 -*
import csv
import sqlite3 as sqlite
import glob
from datetime import datetime

DATABASE = 'test.db'

class LegoDb():
    """LEGO 数据库"""

    def __init__(self):
        self.db_name = 'test.db'

    def connect_db(self):
        self.cx = sqlite.connect(DATABASE)

    def disconnect_db(self):
        self.cx.close()
        
    def init_table(self, tablename):
        self.connect_db()
        if tablename == 'brickset':
            self.cx.execute("drop table if exists brickset")
            init_sql = """create table brickset (
                    id integer primary key,
                    setid text,
                    number text,
                    variant text,
                    theme text,
                    subtheme text,
                    year text,
                    name text,
                    minifigs text,
                    pieces text,
                    ukprice text,
                    usprice text,
                    caprice text,
                    euprice text,
                    imageurl text,
                    owned text,
                    wanted text,
                    qtyowned text,
                    add_time text,
                    modi_time text,
                    data_source text)"""
            self.cx.execute(init_sql)

        if tablename == 'huilv':
            self.cx.execute("drop table if exists huilv")
            init_sql = """create table huilv (
                    id integer primary key,
                    usd text,
                    gbp text,
                    eur text,
                    cad text,
                    date text,
                    time text
                    )"""
            self.cx.execute(init_sql)
        self.disconnect_db()

    def query_db(self, sql, args=(), one=False):
        cur = self.cx.execute(sql, args)
        rv = [dict((cur.description[idx][0], value)
                   for idx, value in enumerate(row)) for row in cur.fetchall()]
        return (rv[0] if rv else None) if one else rv

    def query_brickset_setid(self, setid):
        """查询 brickset 表中 setid 是否存在"""
        self.connect_db()
        sql = 'select * from brickset where setid = ?'
        args = (setid,)
        rvs = self.query_db(sql, args)
        found_rows = len(rvs)
        if found_rows == 1:
            return True
        if found_rows == 0:
            return False
        if found_rows > 1:
            print 'error:mulity setid:%s'%(args[0])
            return False
        self.disconnect_db()



if __name__ == '__main__':
    print LegoDb().query_brickset_setid('8088')

