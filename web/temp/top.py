# -*- coding: utf-8 -*-
"""
Парсер книжек с лайвлиб ТОП100
"""

import urllib
import re


def main():


    c = urllib.urlopen('http://www.livelib.ru/books/top')
    text = re.findall(r'[<]a.\w+\=\"(.*)\".title\=\"(.*)\"[>][<]\w+.\w+\=\"(.*)\".alt', c.read())
    domain = 'http://www.livelib.ru'
    for t in text:
        fullstoryUrl = '%s%s' % (domain, t[0])
        name = t[1]
        smallimg = t[2]



        c1 = urllib.urlopen (fullstoryUrl)
        book = re.findall(r'\w+\:.[<]\w+.\w+\=\"isbn\"[>](\d+.\d+.\d+.\d+.\d)[<]\/span[>][<]br[>]....\S+.\S+.(\d+)[<]br[>]....\S+.[<]\w+.\w+\=\"publisher\"[>](.*)[<]\/span[>][<]br[>]', c1.read())

        for b in book:
            isbn = b[0]
            year = b[1]
            publisher = b[2]

        story = ''
        images = ''
        author = ''
        bookname = ''

        c2 = urllib.urlopen (fullstoryUrl)
        newbook = re.findall(r'[<]img.src\=\"(.*)\".alt\=(.*).\"image\"|[<]\w.style=\"\w+\-\w+\:.\d+\%\;.\w+\-\w+\:.\d+\%\;\".itemprop\=\"about\"[>](.*)[<]|class=\"tag\"(.*)[<]\/a[>]{0,1}|itemprop\=\"author\"[>][<]a.\w+\w=\"\/\w+\/\d+\".\w+\=\".*[>](.*)[<]\/\w[>]|[<]span.\w+\=\"book\".\w+\=\"(.*)\"[>][<]a|\S+.\!\w+\".\w+\=\"....100\"[>].(\d+)[<]\/a[>]', c2.read())

        for n in newbook:
            image = n[0]
            text = n[2]
            # n[3] - tags with shit
            story += text
            images += image
            authors = n[4]
            author += authors
            bookname += n[5]
            rating = n[6]

            print rating

if __name__ == '__main__':
    main()




