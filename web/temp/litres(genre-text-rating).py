# -*- coding: utf-8 -*-

"""
Парс по isbn http://www.litres.ru/
рабочий

Тащит рейтинг, аннотацию и жанр.
"""

import httplib
import urllib
from lxml.html import fromstring
import MySQLdb
import time
import re

sleep_sec = 4

def main():
    db = MySQLdb.connect(host="localhost",
        user="root",
        passwd="",
        db="news",
        charset='utf8')

    cur = db.cursor()
    cur.execute("SELECT id, isbn FROM page_book") # достаю из базы isbn

    for row in cur.fetchall() :
        isbn = row[1]
        id = row[0]

        d = 'http://www.litres.ru'
        domain = 'http://www.litres.ru/pages/biblio_search/?q='
        source = '%s%s' % (domain, isbn)

        c = urllib.urlopen(source)
        time.sleep(sleep_sec)
        match = re.findall(r'[<]a.class\=\"bookpage-cover\".href\=\"(.*)\"[>][<]img.|[<]div.class\=\"nothing_found\"[>][<]h2[>](.*)[<]\/h2', c.read()) # поиск первой ссылки результата поиска httplib

        book = ''

        for m in match[0]:
            if m == 'По вашему запросу ничего найти не удалось':
                continue
            elif len(m) == 153:
                book += source
            else:
                book += m

        if book.startswith('http') or book == []:
            pass
        else:
            book = 'http://www.litres.ru%s' % book


        c1 = urllib.urlopen(book)
        text = re.findall(r'class\=\"book_annotation\"[>][<]p[>](.*)[<]\/p[>]|itemprop\=\"description\"[>][<]p[>](.*)[<]\/p[>]|mid_vote\:(\d+.\d+)|[<]dt[>]Жанр\:[<]\/dt[>][<]dd[>][<]a.href.*\"[>](.*)[<]\/a[>]\,.[<]a.', c1.read())


        genre = ''
        litrating = ''
        littext = ''
        for t in text:
            genre +=  t[3] # жанр
            litrating += t[2] # рейтинг litres.ru
            if len(litrating) > 5: # косяк какой-то!!!!!!!!!
                litrating = '0'
            elif litrating == '03.50':
                litrating = '?'
            else:
                pass
            littext += t[0] # book annotation
            if littext:
                littext += t[0]
            else:
                littext += t[1]

        print '%s -- %s' % (id, litrating)



#        sql = "UPDATE page_book SET genre = '%s', text = '%s', litrating = '%s'  WHERE id = '%s'" % (genre, littext, litrating, id)
#        try:
#            cur.execute(sql)
#            db.commit()
#            print 'Book %s successfuly updated ' % id
#            time.sleep(sleep_sec)
#        except:
#            db.rollback()
#            print 'fail'



#        if len(match[0]) > 100:
#            if match[1] == '\xd0\x9f\xd0\xbe \xd0\xb2\xd0\xb0\xd1\x88\xd0\xb5\xd0\xbc\xd1\x83 \xd0\xb7\xd0\xb0\xd0\xbf\xd1\x80\xd0\xbe\xd1\x81\xd1\x83 \xd0\xbd\xd0\xb8\xd1\x87\xd0\xb5\xd0\xb3\xd0\xbe \xd0\xbd\xd0\xb0\xd0\xb9\xd1\x82\xd0\xb8 \xd0\xbd\xd0\xb5 \xd1\x83\xd0\xb4\xd0\xb0\xd0\xbb\xd0\xbe\xd1\x81\xd1\x8c':
#                print 'found 404'
#        else:
#            print match[0]


#        match = re.findall(r'[<]a.class\=\"bookpage-cover\".href\=\"(.*)\"[>][<]img.', c.read()) # поиск первой ссылки результата поиска httplib

#        if len(book) > 100:
#            print 'Sorry, but book with that ISBN No. %s not found :(' % isbn
#            time.sleep(sleep_sec)
#            continue

if __name__ == '__main__':
    main()


