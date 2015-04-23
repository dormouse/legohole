# !/usr/bin/env python
# -*- coding: UTF-8 -*
import sqlite3 as sqlite
DATABASE = 'test.db'
class LegoDb():
    """LEGO 数据库"""

    def __init__(self,cx=None):
        if cx:
            self.cx = cx
        else:
            self.db_name = 'test.db'

    def connect_db(self):
        self.cx = sqlite.connect(DATABASE)

    def disconnect_db(self):
        self.cx.close()

    def tran(self):
        self.connect_db()

        sql = 'select * from brickset_old order by id'
        rows = self.query_db(sql)
        for row in rows:
            self.write_db(row)
        self.cx.commit()
        self.disconnect_db()

    def write_db(self, row):
        datas = (row['setid'], row['number'] + '-' +row['variant'],
            row['theme'], row['subtheme'], row['year'], row['name'],
            row['minifigs'], row['pieces'], row['ukprice'],
            row['usprice'], row['caprice'], row['euprice'],
            row['imageurl'], row['owned'], row['wanted'],
            row['qtyowned'], row['add_time'], row['modi_time'],
            row['data_source'])

        sql = u"insert into brickset (id,brickset_id,number,theme,\
            subtheme,year,name,minifigs,pieces,ukprice,\
            usprice,caprice,euprice,imageurl,owned,wanted,qtyowned,\
            add_time,modi_time,data_source)\
            values (null,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)"
        self.query_db(sql, datas)



    def query_db(self, sql, args=(), one=False):
        cur = self.cx.execute(sql, args)
        rv = [dict((cur.description[idx][0], value)
                   for idx, value in enumerate(row)) for row in cur.fetchall()]
        return (rv[0] if rv else None) if one else rv

if __name__ == '__main__':
    LegoDb().tran()
