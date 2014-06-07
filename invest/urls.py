from django.conf.urls.defaults import patterns, url
import sys

from mysite.invest import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^(?P<num>\d+)/$', views.account, name='account')
)