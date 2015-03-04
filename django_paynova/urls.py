#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of django-paynova.
# https://github.com/akolpakov/django-paynova

# Licensed under the MIT license:
# http://www.opensource.org/licenses/MIT-license
# Copyright (c) 2015, Andrey Kolpakov <aakolpakov@gmail.com>

from django.conf.urls import patterns, url

from . import views

urlpatterns = patterns('',
    url('^success/$', views.paynova_success, name='paynova_success'),
    url('^cancel/$', views.paynova_cancel, name='paynova_cancel'),
    url('^pending/$', views.paynova_pending, name='paynova_pending'),
    url('^callback/$', views.paynova_callback, name='paynova_callback'),
)