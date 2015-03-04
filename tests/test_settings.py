#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of django-paynova.
# https://github.com/akolpakov/django-paynova

# Licensed under the MIT license:
# http://www.opensource.org/licenses/MIT-license
# Copyright (c) 2015, Andrey Kolpakov <aakolpakov@gmail.com>

from preggy import expect
from tests.base import TestCase
from django.conf import settings
from django_paynova import settings as my_settings


class SettingsTestCase(TestCase):
    def test_settings(self):
        expect(my_settings.PAYNOVA_MERCHANT_ID).to_equal(settings.PAYNOVA_MERCHANT_ID)
        expect(my_settings.PAYNOVA_PASSWORD).to_equal(settings.PAYNOVA_PASSWORD)
        expect(my_settings.PAYNOVA_LIVE).to_equal(False)
        expect(my_settings.PAYNOVA_ENDPOINT).to_be_null()
        expect(my_settings.PAYNOVA_DEFAULT_LANGUAGE).to_length(3)
        expect(my_settings.PAYNOVA_CALLBACK_URL).not_to_be_null()