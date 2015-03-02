from django.conf.urls import patterns, url

from . import views

urlpatterns = patterns('',
    url('^success/$', views.paynova_success, name='paynova_success'),
    url('^cancel/$', views.paynova_cancel, name='paynova_cancel'),
    url('^pending/$', views.paynova_pending, name='paynova_pending'),
    url('^callback/$', views.paynova_callback, name='paynova_callback'),
)