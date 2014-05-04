from django.conf.urls import patterns, url

from tapmanager import views

urlpatterns = patterns(
    '',
    url(r'^$', views.taps, name='taps'),
    url(r'^logout/$', views.logout_view, name='logout_view'),
    url(r'^login/$', views.login_view, name='login'),
    url(r'^tapadmin/$', views.tapadmin, name='tapadmin'),
    url(r'^register/$', views.register, name='register'),
    url(r'^settings/$', views.settings, name='settings'),
    url(r'^log/$', views.log, name='log'),
    url(r'^tapadmin/$', views.tapadmin, name='tapadmin'),
    url(r'^stats/$', views.stats, name='stats'),
    url(
        r'^log/(?P<page_num>\w+)/(?P<filter_log>\w+)/$',
        views.log, name='log'),
)
