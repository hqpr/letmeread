# -*- coding: cp1251 -*-

""" парс полного текста биографии с литреса """
#from lxml.html import fromstring
#import urllib
#c = urllib.urlopen('http://www.litres.ru/dzhoan-rouling/')
#data = c.read()
#page = fromstring(data)
#el = page.find(".//*/div[@id='author-left']/div[@class='right']/div[@id='auth_text']/div[@id='auth_annot']")
#e = el.text_content()

from lxml.html import fromstring
import urllib
import MySQLdb
import time

sleep_sec = 3

db = MySQLdb.connect(host="localhost", # coonect to DB
    user="root",
    passwd="",
    db="news",
    charset='utf8')

cur = db.cursor()

cur.execute("SELECT name, authorslink FROM page_book")
for row in cur.fetchall():
    authorslink = row[1]
    name = row[1]
    bio = '' # saves results here
    if not authorslink:
        pass # delete link if its blank
    else:
        domain = 'http://www.livelib.ru'
        source = '%s%s' % (domain, authorslink)

        c = urllib.urlopen(source) # full url with domain
        time.sleep(sleep_sec) # sleep
        data = c.read()
        page = fromstring(data)
        el = page.find(".//*/div[@id='inner']/div[@id='leftsidewrap']/div[@id='leftside']/div[3]/div[1]")
        bio += el.text_content() # grab bio

    sql = "UPDATE page_author SET bio = '%s' WHERE name = '%s'" % (bio, name)

    try:
        cur.execute(sql)
        db.commit()
        print 'Author\'s bio is successfully updated '
    except:
        db.rollback()
        print 'fail'





