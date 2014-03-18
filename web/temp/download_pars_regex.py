# -*- coding: utf-8 -*-
import httplib
import urllib
import MySQLdb
import re


def main():
    db = MySQLdb.connect(host="localhost",
        user="root",
        passwd="",
        db="news",
        charset='utf8')

    cur = db.cursor()
    cur.execute("SELECT id FROM page_book")

    c = urllib.urlopen('http://www.livelib.ru/books/top')
    text = re.findall(r'[<]a.\w+\=\"(.*)\".title\=\"(.*)\"[>][<]\w+.\w+\=\"(.*)\".alt', c.read())
    domain = 'http://www.livelib.ru'
    for t in text:
        fullstoryUrl = '%s%s' % (domain, t[0])
        name = t[1]
        smallimg = t[2]

        fid = t[0].split('/')
        eid = fid[-1]

        sql = "UPDATE page_book SET link = 'http://www.e-reading-lib.org/download.php?book=%s' WHERE id = '%s'" % (eid, id)

        try:
            cur.execute(sql)
            db.commit()
            print '%s - link is updated' % id
        except:
            db.rollback()
            print 'fail'

if __name__ == '__main__':
    main()