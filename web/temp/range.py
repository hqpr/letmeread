# -*- coding: utf-8 -*-
"""
Парсер книжек с лайвлиб
"""

import urllib
import re
import MySQLdb


def main():

    db = MySQLdb.connect(host="localhost", # coonect to DB
        user="root",
        passwd="",
        db="news",
        charset='utf8')

    cur = db.cursor()

    #    c = urllib.urlopen('http://www.livelib.ru/books/movers-and-shakers/') # открываем 50 самых популярных
    #    c = urllib.urlopen('http://www.livelib.ru/selection/1431') # экранизации
    a = 'http://www.livelib.ru/books/movers-and-shakers/'
    c = urllib.urlopen(a) # экранизации
    text = re.findall(r'[<]a.\w+\=\"(.*)\".title\=\"(.*)\"[>][<]\w+.\w+\=\"(.*)\".alt', c.read())
    domain = 'http://www.livelib.ru'
    category = 'tv'

    for t in text:
        fullstoryUrl = '%s%s' % (domain, t[0])
        name = t[1] # автор + заголовок
        smallimg = t[2] # маленькая картинка (не скачивается)
        fullstoryid = t[0].split('/')

        c1 = urllib.urlopen (fullstoryUrl)
        book = re.findall(r'\w+\:.[<]\w+.\w+\=\"isbn\"[>](\d+.\d+.\d+.\d+.\d)[<]\/span[>][<]br[>]....\S+.\S+.(\d+)[<]br[>]....\S+.[<]\w+.\w+\=\"publisher\"[>](.*)[<]\/span[>][<]br[>]', c1.read())

        for b in book:
            isbn = b[0]
            year = b[1]
            publisher = b[2]

            sql = "INSERT INTO page_book (title, smallimage, isbn, year, publisher, source, category) VALUES ('%s','%s','%s','%s','%s','%s','%s')" % (name, smallimg, isbn, year, publisher, fullstoryUrl, category)
            try:
                cur.execute(sql)
                db.commit()
                print 'updated'
            except:
                db.rollback()
                print 'fail'


    # Парс полной информации
    cur.execute("SELECT id, source FROM page_book")
    for row in cur.fetchall():
        id = row[0]
        source = row[1]

        story = '' # аннотация
        images = ''
        author = ''
        bookname = ''
        rating = ''
        image = ''
        local_pic = ''
        authorslink = ''

        c2 = urllib.urlopen (source)
        newbook = re.findall(r'[<]img.src\=\"(.*)\".alt\=(.*).\"image\"|[<]\w.style=\"\w+\-\w+\:.\d+\%\;.\w+\-\w+\:.\d+\%\;\".itemprop\=\"about\"[>](.*)[<]|class=\"tag\"(.*)[<]\/a[>]{0,1}|itemprop\=\"author\"[>][<]a.\w+\w=\"(\/\w+\/\d+)\".\w+\=\".*[>](.*)[<]\/\w[>]|[<]span.\w+\=\"book\".\w+\=\"(.*)\"[>][<]a|[<]span.title\=\"\S+.(\d+\.\d+).[(]\d+..\S+[)]', c2.read())
        for n in newbook:
            image += n[0] # главная картинка
            text = n[2]
            # n[3] - tags with
            story += text
            images += image
            authorslink += n[4]
            authors = n[5]
            author += authors
            bookname += n[6]
            rating = n[7]

        local_pic += '%s.jpg' % id
#            urllib.urlretrieve(image, local_pic) # сохраняю картинки вида айди.джпег
        print 'Book picture with id # %s successfully downloaded ' % id


        sql = "UPDATE page_book SET name = '%s', author = '%s', image = '%s', text ='%s', rating = '%s', authorslink = '%s' WHERE id = '%s'" % (bookname, author, local_pic, story, rating, authorslink, id)

        try:
            cur.execute(sql)
            db.commit()
            print 'Fullstory is successfully updated '
        except:
            db.rollback()
            print 'fail'

if __name__ == '__main__':
    main()




