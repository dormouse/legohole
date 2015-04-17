# !/usr/bin/env python
# -*- coding: UTF-8 -*
import csv
import sqlite3 as sqlite
import glob
from datetime import datetime

DATABASE = 'test.db'

def init_db():
    cx = sqlite.connect(DATABASE)
    cx.execute("drop table if exists brickset")
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
    cx.execute(init_sql)
    cx.close()

def import_brickset_csv():
    cx = sqlite.connect(DATABASE)
    csv_file = 'brickset.csv'
    pro_data(cx, csv_file)
    cx.commit()
    cx.close()

def pro_data(cx, filename):
    with file(filename, 'rb') as f:
        reader = csv.DictReader(f)
        try:
            for row in reader:
                if query_by_setid(cx, row['SetID']):
                    pass
                else:
                    write_db(cx, row)
        except csv.Error as e:
            sys.exit('file %s, line %d: %s' % (filename, reader.line_num, e))

def write_db(cx, row):
    datas = (row['SetID'], row['Number'], row['Variant'],
        row['Theme'], row['Subtheme'], row['Year'], row['Name'],
        row['Minifigs'], row['Pieces'], row['UKPrice'],
        row['USPrice'], row['CAPrice'], row['EUPrice'],
        row['ImageURL'], row['Owned'], row['Wanted'],
        row['QtyOwned'])
    if row['Year'] == "Year":
        print filename
    data_db = [item.decode('utf-8') for item in datas]
    data_db.append(datetime.now().strftime('%Y-%m-%d %H:%M:%S %f') )
    data_db.append('brickset')
    data_clean = (data_db)

    sql = u"insert into brickset (id,setid,number,variant,theme,\
        subtheme,year,name,minifigs,pieces,ukprice,\
        usprice,caprice,euprice,imageurl,owned,wanted,qtyowned,\
        add_time,modi_time,data_source)\
        values (null,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,null,?)"
    cx.execute(sql, data_clean)

def query_by_setid(cx, setid):
    sql = 'select * from brickset where setid = ?'
    args = (setid,)
    rvs = query_db(cx, sql, args)
    found_rows = len(rvs)
    if found_rows == 1:
        return True
    if found_rows == 0:
        return False
    if found_rows > 1:
        print 'error:mulity setid:%s'%(args[0])
        return False

def query_db(cx, query, args=(), one=False):
    cur = cx.execute(query, args)
    rv = [dict((cur.description[idx][0], value)
               for idx, value in enumerate(row)) for row in cur.fetchall()]
    return (rv[0] if rv else None) if one else rv

if __name__ == '__main__':
    import_brickset_csv()
    #print glob.glob('*.csv')
