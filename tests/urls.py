from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^(?i)payments/paynova/', include('django_paynova.urls'))
)