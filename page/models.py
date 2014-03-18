# -*- coding: utf-8 -*-
from django.db import models
from django.utils.encoding import smart_unicode

class News(models.Model):
    title = models.CharField(max_length=100, verbose_name='Заголовок новости')
    text = models.TextField(verbose_name='Текст новости')
    description = models.TextField(verbose_name='Краткая новость')
    comment = models.TextField(verbose_name='Комментарии', null=True, blank=True, help_text='Не обязательное поле' )
    image = models.FileField(upload_to='img/blog/', help_text='682x200 px')
    date = models.DateField(verbose_name='Дата')
    CAT_CHOICES = (
    (u'Рецензии', 'Рецензии'),
    (u'Новости', 'Новости'),
    (u'Обсуждения', 'Обсуждения'),
    (u'Работа сайта', 'Работа сайта'),
    )
    category = models.CharField(max_length=255, verbose_name='Категория', choices=CAT_CHOICES, blank=True)

    class Meta:
        verbose_name = 'Новость'
        verbose_name_plural = 'новости'

    def __unicode__(self):
        return self.title


class Book(models.Model):
    name = models.CharField(max_length=255, verbose_name='Книга')
    author = models.ForeignKey(u'Author', verbose_name='Автор')
    isbn = models.CharField(max_length=255, verbose_name='ISBN', blank=True, null=True)
    text = models.TextField(verbose_name='Аннотация', blank=True, null=True)
    source = models.URLField(verbose_name='Ссылка на оригинал', blank=True, null=True)
    genre = models.ManyToManyField('Tag', verbose_name='Жанр книги', blank=True, null=True)
    year = models.IntegerField(max_length=2, verbose_name='Год', blank=True, null=True)
    publisher = models.ForeignKey('Publishers', verbose_name='Издательство', blank=True, null=True)
    image = models.FileField(upload_to='img/book/', verbose_name='Изображение', blank=True, null=True)
    rating = models.CharField(max_length=255, verbose_name='Рейтинг', blank=True, null=True)
    series = models.CharField(max_length=255, verbose_name='Серия книг', blank=True, null=True)
    link = models.CharField(max_length=255, verbose_name='FB2 link', blank=True, null=True)
    erating = models.CharField(max_length=255, verbose_name='Rating e-reading', blank=True, null=True)
    litrating = models.CharField(max_length=255, verbose_name='Rating litres', blank=True, null=True)
    txtlink = models.CharField(max_length=255, verbose_name='txt link', blank=True, null=True)
    htmllink = models.CharField(max_length=255, verbose_name='html link', blank=True, null=True)
    epublink = models.CharField(max_length=255, verbose_name='epub link', blank=True, null=True)
    mobilink = models.CharField(max_length=255, verbose_name='mobi link', blank=True, null=True)
    authorslink = models.CharField(max_length=255, verbose_name='Ссылка на страницу автора', blank=True, null=True)
    yakaboo = models.CharField(max_length=255, verbose_name='Ссылка Yakaboo', blank=True, null=True)
    screening = models.BooleanField(verbose_name='Экранизация')
    movie = models.CharField(max_length=255, verbose_name='Название фильма', blank=True, null=True)
    release = models.CharField(max_length=255, verbose_name='Год выхода', blank=True, null=True)

    CAT_CHOICES = (
        (u'Самые популярные', 'Популярные'),
        ('TOP 100', 'Топ 100'),
        ('Best of 2014', 'Топ 2014'),
        ('Best of 2013', 'Топ 2013'),
        ('Best of 2012', 'Топ 2012'),
        (u'Экранизации', 'Экранизации'),
                )
    category = models.CharField(max_length=255, verbose_name='Категория', choices=CAT_CHOICES, blank=True)

    class Meta:
        verbose_name = 'Книга'
        verbose_name_plural = 'книги'

    def __unicode__(self):
        return '%s - %s' % (self.name, self.author)


class Author(models.Model):
    name = models.CharField(max_length=255, verbose_name='Имя')
    engname = models.CharField(max_length=255, verbose_name='Полное имя (англ)', blank=True, null=True)
    bio = models.TextField(verbose_name='Биография')
    image = models.FileField(upload_to='img/author/', verbose_name='Изображение', blank=True, null=True)
    website = models.CharField(max_length=255, verbose_name='Web Site', blank=True, null=True)
    twitter = models.CharField(max_length=255, verbose_name='Twitter', blank=True, null=True)
    rating = models.IntegerField(max_length=2, verbose_name='Рейтинг автора', blank=True, null=True)
    bookid = models.IntegerField(max_length=100, verbose_name='book id', blank=True, null=True, help_text='Вообще не помню нахера это поле')

    class Meta:
        verbose_name = 'Автор'
        verbose_name_plural = 'авторы'

    def __unicode__(self):
        return u'%s' % self.name


class Slider(models.Model):
    title = models.CharField(max_length=100, verbose_name='Название слайда')
    image = models.FileField(upload_to='img/slider/', help_text='960x400 px')
    book_id = models.IntegerField(max_length=100, verbose_name='book id')
    annotation = models.TextField(verbose_name='Аннотация')

    class Meta:
        verbose_name = 'Слайдер'
        verbose_name_plural = 'слайды'

    def __unicode__(self):
        return self.title


class Quote(models.Model):
    text = models.TextField(verbose_name='Текст')
    author = models.CharField(max_length=255, verbose_name='authors name')
    image = models.FileField(upload_to='img/quote/', help_text='126x126 px')

    class Meta:
        verbose_name = 'Цитата'
        verbose_name_plural = 'цитаты'

    def __unicode__(self):
        return self.author


class Tag(models.Model):
    tag = models.CharField(max_length=255, verbose_name='Жанр или тэг')

    class Meta:
        verbose_name = 'Метка'
        verbose_name_plural = 'метки'

    def __unicode__(self):
        return self.tag


class Publishers(models.Model):
    publisher = models.CharField(max_length=255, verbose_name='Издатель')
    image = models.FileField(upload_to='img/publishers/', help_text='120x88 px')

    class Meta:
        verbose_name = 'Издатель'
        verbose_name_plural = 'издатели'

    def __unicode__(self):
        return self.publisher


