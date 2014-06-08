from django.conf.urls.defaults import patterns, url
import sys

from mysite.invest import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^(?P<num>\d+)/$', views.account, name='account'),
    url(r'^login/$', views.login),
    url(r'^loginAction/$', views.request_login),
    url(r'^account/$', views.display_home),
    url(r'^profile/$', views.edit_account),
    url(r'browse.html$', views.display_home),
    url(r'profile.html$', views.edit_account),
    url(r'index.html$', views.login)
)
