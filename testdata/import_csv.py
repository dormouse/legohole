# !/usr/bin/env python
# -*- coding: UTF-8 -*
import csv
import sqlite3 as sqlite
import glob
from datetime import datetime
def init_db():
    cx = sqlite.connect("test.db")
    cx.execute("drop table brickset")
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

def import_data():
    cx = sqlite.connect("test.db")
    for file in glob.glob('*.csv'):
        if file != 'brickset_20150319_date-added.csv':
            pro_data(cx, file)
    cx.commit()
    cx.close()

def pro_data(cx, filename):
    with file(filename, 'rb') as f:
        reader = csv.DictReader(f)
        try:
            for row in reader:
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

        except csv.Error as e:
            sys.exit('file %s, line %d: %s' % (filename, reader.line_num, e))

def test():
    print glob.glob('*.csv')

if __name__ == '__main__':
    init_db()
    import_data()
