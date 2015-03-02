from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^(?i)payments/paynova/', include('paynova_api_django.urls'))
)