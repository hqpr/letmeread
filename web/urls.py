# -*- coding: utf-8 -*-

from django.conf.urls import patterns, include, url
from django.contrib import admin
admin.autodiscover()
from page import views
from django.conf import settings
from page import forms
from django.conf.urls import patterns, url
from django.conf.urls.static import static
from django.conf.urls import *
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = patterns('page.views',
    url(r'^$', views.index),
    url(r'^book/(\d+)/$', views.book),
    url(r'^author/(\d+)/$', views.author, name='author'),
    url(r'^year/(\d+)/$', views.year),
    url(r'^publisher/(.*)/$', views.publisher),
    url(r'^tag/(.*)/$', views.tag),
    url(r'^category/(.*)/$', views.category),
    url(r'^blog/$', views.blog),
    url(r'^blog/(\d+)/$', views.blog_post),
    url(r'^blog/category/(.*)/$', views.blog_category),
    url(r'^search-form/$', views.search_form),
    url(r'^search/$', views.search),
    url(r'^rating/$', views.rating),
    url(r'^book/series/(.*)/$', views.series),
    url(r'^book/series/$', views.series_all),
    url(r'^books/(.)/$', views.books_by_word),
    url(r'^books/$', views.all_books),
    url(r'^authors/$', views.all_author),
    url(r'^authors/(.)/$', views.author_by_word),

#    url(r'^genre/(.*)/$', views.genre),
#    url(r'^propose/$', views.contact),
#    url(r'^\d+/$', views.allnews),

    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
) #+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.LOCAL_DEVELOPMENT:
    urlpatterns += patterns("django.views",
        url(r"%s(?P<path>.*)$" % settings.STATIC_URL[1:], "static.serve", {
            "document_root": settings.STATIC_ROOT,
            'show_indexes': True,
        }),
        url(r"%s(?P<path>.*)$" % settings.MEDIA_URL[1:], "static.serve", {
            "document_root": settings.MEDIA_ROOT,
            'show_indexes': True,
        }),
    )



#if settings.DEBUG:
#    urlpatterns += patterns('',
#        url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {
#            'document_root': settings.MEDIA_ROOT,
#            }),
#        url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {
#            'document_root': settings.STATIC_ROOT,
#            }),
#    )
