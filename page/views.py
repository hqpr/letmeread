#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.shortcuts import render_to_response
from .models import News
from .models import Book, Slider, Author, Quote, Tag, Publishers
from django.shortcuts import render
from django.shortcuts import HttpResponseRedirect
from django .http import Http404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .forms import ProposeForm
from django.core.mail import send_mail
import urllib
import re
from datetime import date
import MySQLdb
from xml.dom.minidom import *

# Books


def index(request):
    p = Book.objects.all()  # [:12]
    paginator = Paginator(p, 3)
    page = request.GET.get('page')
    try:
        p = paginator.page(page)
    except PageNotAnInteger:
        p = paginator.page(1)
    except EmptyPage:
        p = paginator.page(paginator.num_pages)
    s = Slider.objects.all()
    pub = Publishers.objects.all()
    # по категориям
    tv = Book.objects.filter(category='Экранизации')[:8]
    popular = Book.objects.filter(category='Самые популярные')[:8]
    best_of_2013 = Book.objects.filter(category='Best of 2013')[:8]
    best_of_2012 = Book.objects.filter(category='Best of 2012')[:8]
    best_of_2014 = Book.objects.filter(category='Best of 2014')[:8]
    top100 = Book.objects.filter(category='TOP 100')[:8]
    q = Quote.objects.all()
    n = News.objects.filter(category=u'Новости')[:2]
    context = {'p': p, 's': s, 'tv': tv, 'popular': popular, 'best_of_2013': best_of_2013, 'best_of_2012': best_of_2012, 'best_of_2014': best_of_2014, 'top100': top100, 'q': q, 'pub': pub, 'n': n}
    return render(request, 'index.html', context)


def book(request, id):
    d = Book.objects.get(id=id)
    g = Tag.objects.filter(book=id)
    a = Author.objects.get(name=d.author)
    data = {'d': d, 'g': g, 'a': a}
    return render(request, 'book.html', data)


def author(request, id):
    a = Author.objects.get(id=id)
    b = Book.objects.filter(author=id)
    data = {'a': a, 'b': b}
    return render(request, 'author.html', data)


def year(request, year):
    y = Book.objects.filter(year=year)
    data = {'y': y}
    return render(request, 'year.html', data)


def publisher(request, id):
    p = Publishers.objects.filter(id=id)
    b = Book.objects.filter(publisher=publisher)
    data = {'p': p, 'b': b}
    return render(request, 'publisher.html', data)


def tag(request, tag, id):
    b = Book.objects.filter(book_id=id)
    g = Tag.objects.filter(tag=tag)
    b = Book.objects.filter(book_id=id)
    data = {'g': g, 'b': b}
    return render(request, 'tag.html', data)


def category(request, category):
    c = Book.objects.filter(category=category)
    paginator = Paginator(c, 10)
    page = request.GET.get('page')
    try:
        c = paginator.page(page)
    except PageNotAnInteger:
        c = paginator.page(1)
    except EmptyPage:
        c = paginator.page(paginator.num_pages)
    data = {'c': c}
    return render(request, 'category.html', data)


def blog(request):
    n = News.objects.all().order_by('-date')
    data = {'n': n}
    return render(request, 'blog.html', data)


def blog_post(request, id):
    p = News.objects.get(id=id)
    n = News.objects.all()
    data = {'p': p, 'n': n}
    return render(request, 'post.html', data)


def blog_category(request, category):
    p = News.objects.filter(category=category)
    data = {'p': p}
    return render(request, 'blog_category.html', data)


def search_form(request):
    return render(request, 'base.html')


def search(request):
    errors = []
    if 'q' in request.GET:
        q = request.GET['q']
        if not q:
            errors.append('Вы не ввели в строку запрос')
        elif q == u'Поиск книг':
            errors.append('Ищите книги по запросу "Поиск книг"? Интересно...')
        else:
            books = Book.objects.filter(name__icontains=q)
            return render(request, 'search_results.html',
                {'books': books, 'query': q})
    return render(request, 'index.html',
        {'errors': errors})


def rating(request):
    p = Book.objects.order_by('-rating')
    paginator = Paginator(p, 10)
    page = request.GET.get('page')
    try:
        p = paginator.page(page)
    except PageNotAnInteger:
        p = paginator.page(1)
    except EmptyPage:
        p = paginator.page(paginator.num_pages)
    data = {'p': p}
    return render(request, 'rating.html', data)


def series(request, series):
    s = Book.objects.filter(series=series)
    data = {'s': s}
    return render(request, 'series.html', data)


def series_all(request):
    s = Book.objects.order_by('series')
    data = {'s': s}
    return render(request, 'series_all.html', data)


def books_by_word(request, letter):
    letter = Book.objects.filter(name__startswith=letter.upper())
    r = ["а", "б", "в", "г", "д", "е", "ё", "ж", "з", "и", "к", "л", "м", "н", "о", "п", "р", "с", "т", "у", "ф", "х", "ц", "ч", "ш", "щ", "э", "ю", "я"]
    e = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"]
    d = ["1", "2", "3", "4", "5", "6", "7", "8", "9"]
    data = {'letter': letter, 'r': r, 'e': e, 'd': d}
    return render(request, 'books_by_word.html', data)


def all_books(request):
    c = Book.objects.all()
    r = ["а", "б", "в", "г", "д", "е", "ё", "ж", "з", "и", "к", "л", "м", "н", "о", "п", "р", "с", "т", "у", "ф", "х", "ц", "ч", "ш", "щ", "э", "ю", "я"]
    e = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"]
    d = ["1", "2", "3", "4", "5", "6", "7", "8", "9"]
    paginator = Paginator(c, 10)
    page = request.GET.get('page')
    try:
        c = paginator.page(page)
    except PageNotAnInteger:
        c = paginator.page(1)
    except EmptyPage:
        c = paginator.page(paginator.num_pages)
    data = {'c': c, 'r': r, 'e': e, 'd': d}
    return render(request, 'all_books.html', data)


def all_author(request):
    c = Author.objects.all()
    r = ["а", "б", "в", "г", "д", "е", "ё", "ж", "з", "и", "к", "л", "м", "н", "о", "п", "р", "с", "т", "у", "ф", "х", "ц", "ч", "ш", "щ", "э", "ю", "я"]
    e = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"]
    paginator = Paginator(c, 10)
    page = request.GET.get('page')
    try:
        c = paginator.page(page)
    except PageNotAnInteger:
        c = paginator.page(1)
    except EmptyPage:
        c = paginator.page(paginator.num_pages)
    data = {'c': c, 'r': r, 'e': e}
    return render(request, 'all_authors.html', data)


def author_by_word(request, letter):
    letter = Author.objects.filter(name__startswith=letter.upper())
    r = ["а", "б", "в", "г", "д", "е", "ё", "ж", "з", "и", "к", "л", "м", "н", "о", "п", "р", "с", "т", "у", "ф", "х", "ц", "ч", "ш", "щ", "э", "ю", "я"]
    e = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"]
    data = {'letter': letter, 'r': r, 'e': e}
    return render(request, 'author_by_word.html', data)


#def allnews(request):
#    p = News.objects.filter(week=request)
#    context  = {'p':p}
#    return render(request, 'add.html', context)

# testing
