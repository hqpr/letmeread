# -*- coding: cp1251 -*-

import httplib
import urllib
from lxml.html import fromstring
import lxml.html
import re
import MySQLdb

def main():



    db = MySQLdb.connect(host="localhost",
        user="root",
        passwd="",
        db="news",
        charset='utf8')

    cur = db.cursor()
    cur.execute("SELECT isbn FROM page_book")

    c = urllib.urlopen('http://www.livelib.ru/books/top')
    text = re.findall(r'[<]a.\w+\=\"(.*)\".title\=\"(.*)\"[>][<]\w+.\w+\=\"(.*)\".alt', c.read())
    domain = 'http://www.livelib.ru'

    rating = ''

    for t in text:
        fullstoryUrl = '%s%s' % (domain, t[0])
        name = t[1]
        smallimg = t[2]

        c1 = urllib.urlopen (fullstoryUrl)
        book = re.findall(r'\w+\:.[<]\w+.\w+\=\"isbn\"[>](\d+.\d+.\d+.\d+.\d)[<]\/span[>][<]br[>]....\S+.\S+.(\d+)[<]br[>]....\S+.[<]\w+.\w+\=\"publisher\"[>](.*)[<]\/span[>][<]br[>]', c1.read())
        isbn = ''
        for b in book:
            isbn += b[0]
            year = b[1]
            publisher = b[2]

        page = urllib.urlopen(fullstoryUrl)

        doc = lxml.html.document_fromstring(page.read())
        rat = doc.xpath('/html/body[@id="body"]/div[@id="content"]/div[@id="inner"]/div[@id="leftsidewrap"]/div[@id="leftside"]/div[2]/div[2]/div[@class="actionbar mpad"][1]/span/a[@class="action underlined"]/span[2]/text()[1]')
        for rating in rat:
            sql = "UPDATE page_book SET rating = '%s' WHERE isbn = '%s'" % (rating, isbn)

            try:
                cur.execute(sql)
                db.commit()
                print '%s - rating is updated' % rating
            except:
                db.rollback()
                print 'fail'

if __name__ == '__main__':
    main()