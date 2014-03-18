# -*- coding: utf-8 -*-
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
    cur.execute("SELECT id, name FROM page_book") # достаю из базы названия книг

    for row in cur.fetchall() :
        name = row[1]
        name = name.encode('cp1251')
        id = row[0]

        conn = httplib.HTTPConnection("www.e-reading-lib.org")
        f = {'query': '%s' % (name,)}  #поиск по названию книг
        conn.request("GET", "/?%s" % urllib.urlencode(f) )
        res = conn.getresponse()
        data =  res.read()

        match = re.findall(r"[<]script[>]\w+\.\w+.\w+[(]\'book.php\?book\=(\d+)\&", data) # поиск первой ссылки результата поиска httplib
        for m in match:
            pass
        domain = 'http://www.e-reading-lib.org/book.php?book='
        furl = '%s%s' % (domain, m) # Ссылка на книгу с е-ридинг
        down = 'http://www.e-reading-lib.org/download.php?book='
        fb2 = '%s%s' % (down, m) # fb2 download link

        conn = urllib.urlopen(furl)
        genre = ''
        txt= ''
        html = ''
        erating = ''

        matchfull = re.findall(r'[<]tr[>][<]td[>][<]b[>].*itemprop\=\"category\"[>](.*)[<]\/a[>]|[<]span.itemprop\=\"average\"[>](\d\.\d)|[<]a.href\=\"(download.php\?book\=\d+)|[<]a.href\=\"txt.php(.*)\".rel\=\"\w+\".title\=\".*[>]txt|[<]a.href\=\"(bookreader.php\/save\/.*)\".rel', conn.read())

        for mfull in matchfull:
            erating += mfull[1] # рейтинг е-ридинг
            genre += mfull[0] # жанр (косяк с кодировкой)
            txt += mfull[3] # txt
            html += mfull[4] # html

        # mfull[2] - ссылка на фб2

        sql = "UPDATE page_book SET link = '%s', genre = '%s', erating = '%s', txtlink ='%s', htmllink = '%s' WHERE name = '%s'" % (fb2, genre, erating, txt, html, name)

        try:
            cur.execute(sql)
            db.commit()
            print 'Book id # %s successfuly updated ' % id
        except:
            db.rollback()
            print 'fail'

        time.sleep(sleep_sec)
if __name__ == '__main__':
    main()