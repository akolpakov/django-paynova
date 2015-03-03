#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of paynova-api-django.
# https://github.com/akolpakov/paynova-api-django

# Licensed under the MIT license:
# http://www.opensource.org/licenses/MIT-license
# Copyright (c) 2015, Andrey Kolpakov <aakolpakov@gmail.com>

from preggy import expect
from tests.base import TestCase
from django.http import HttpResponse, HttpRequest
from paynova_api_django.views import *


class ViewTestCase(TestCase):
    def test_view(self):
        request = HttpRequest()
        expect(paynova_success(request)).to_be_instance_of(HttpResponse)
        expect(paynova_cancel(request)).to_be_instance_of(HttpResponse)
        expect(paynova_pending(request)).to_be_instance_of(HttpResponse)