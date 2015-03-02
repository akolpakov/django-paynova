#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of paynova-api-django.
# https://github.com/akolpakov/paynova-api-django

# Licensed under the MIT license:
# http://www.opensource.org/licenses/MIT-license
# Copyright (c) 2015, Andrey Kolpakov <aakolpakov@gmail.com>

from preggy import expect
from tests.base import TestCase
from django.conf import settings
from paynova_api_django import settings as my_settings


class SettingsTestCase(TestCase):
    def test_settings(self):
        expect(my_settings.PAYNOVA_USERNAME).to_equal(settings.PAYNOVA_USERNAME)
        expect(my_settings.PAYNOVA_PASSWORD).to_equal(settings.PAYNOVA_PASSWORD)
        expect(my_settings.PAYNOVA_LIVE).to_equal(False)
        expect(my_settings.PAYNOVA_ENDPOINT).to_be_null()