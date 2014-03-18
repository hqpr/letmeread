# -*- coding: cp1251 -*-

"""
Пытаюсь сделать парс lxml.html
"""

import urllib
import lxml.html


page = urllib.urlopen("http://habrahabr.ru/")

doc = lxml.html.document_fromstring(page.read())

for topic in doc.cssselect('h2.entry-title a.topic'):
    print topic.text
