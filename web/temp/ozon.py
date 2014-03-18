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

        conn = httplib.HTTPConnection("booklya.com.ua")
        f = {'search': '%s' % (name,)}  #поиск по названию книг
        conn.request("GET", "/products/search/?%s" % urllib.urlencode(f) )
        res = conn.getresponse()
        data =  res.read()

        match = re.findall(r"[<]a.href\=\"(\/books\/\d+\/)", data) # поиск первой ссылки результата поиска httplib

        print match


        time.sleep(sleep_sec)

if __name__ == '__main__':
    main()