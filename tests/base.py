#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of django-paynova.
# https://github.com/akolpakov/django-paynova

# Licensed under the MIT license:
# http://www.opensource.org/licenses/MIT-license
# Copyright (c) 2015, Andrey Kolpakov <aakolpakov@gmail.com>

from django.test import TestCase


class TestCase(TestCase):
    ORDER_ID = '70bf60e7-cc9b-4321-bb32-a449010f45a5'
    ORDER_SESSION_ID = 'test-session-id'
    ORDER_URL = 'http://test.com'

    create_order_params = {
        'orderNumber': '0001',
        'currencyCode': 'EUR',
        'totalAmount': 10
    }