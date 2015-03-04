from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^(?i)payments/paynova/', include('django_paynova_api.urls')),
    url(r'^.*', 'example_app.views.payment')
)