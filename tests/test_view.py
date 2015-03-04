#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of paynova-api-django.
# https://github.com/akolpakov/paynova-api-django

# Licensed under the MIT license:
# http://www.opensource.org/licenses/MIT-license
# Copyright (c) 2015, Andrey Kolpakov <aakolpakov@gmail.com>

from preggy import expect
from tests.base import TestCase
from httmock import HTTMock
from datetime import datetime
from django.http import HttpResponse, HttpRequest, HttpResponseBadRequest, HttpResponseNotFound
from django.conf import settings
from paynova_api_django import create_order
from paynova_api_django.views import *
from paynova_api_django.models import PaynovaPayment
from .mock import paynova_mock

import hashlib


class ViewTestCase(TestCase):
    def _get_checksum(self, data):

        h = hashlib.sha1()
        h.update(data.get('EVENT_TYPE'))
        h.update(';')
        h.update(data.get('EVENT_TIMESTAMP'))
        h.update(';')
        h.update(data.get('DELIVERY_TIMESTAMP'))
        h.update(';')
        h.update(data.get('MERCHANT_ID'))
        h.update(';')
        h.update(settings.PAYNOVA_SECRET)

        return h.hexdigest()

    def setUp(self):
        PaynovaPayment.objects.all().delete()

        self.ehn_common_data_fields = {
            'EVENT_TYPE': 'PAYMENT',
            'EVENT_TIMESTAMP': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'DELIVERY_TIMESTAMP': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'MERCHANT_ID': settings.PAYNOVA_MERCHANT_ID,
            'ORDER_ID': TestCase.ORDER_ID,
            'ORDER_NUMBER': 'order-001',
            'SESSION_ID': TestCase.ORDER_SESSION_ID,
            'PAYMENT_STATUS': 'COMPLETED',
            'PAYMENT_STATUS_REASON': 'NONE',
            'AMOUNT': '10.00',
            'CURRENCY_CODE': 'EUR',
        }

        self.ehn_common_data_fields['DIGEST'] = self._get_checksum(self.ehn_common_data_fields)

    def tearDown(self):
        pass

    def test_view(self):
        request = HttpRequest()
        expect(paynova_success(request)).to_be_instance_of(HttpResponse)
        expect(paynova_cancel(request)).to_be_instance_of(HttpResponse)
        expect(paynova_pending(request)).to_be_instance_of(HttpResponse)

    def test_callback_checksum(self):
        request = HttpRequest()
        self.ehn_common_data_fields['DIGEST'] = 'wrong-digest'
        request.POST = self.ehn_common_data_fields

        expect(paynova_callback(request)).to_be_instance_of(HttpResponseBadRequest)

    def test_callback_event_type(self):
        request = HttpRequest()
        self.ehn_common_data_fields['EVENT_TYPE'] = 'UNKNOWN_EVENT_TYPE'
        self.ehn_common_data_fields['DIGEST'] = self._get_checksum(self.ehn_common_data_fields)
        request.POST = self.ehn_common_data_fields

        expect(paynova_callback(request)).to_be_instance_of(HttpResponseBadRequest)

    def test_callback_not_found(self):
        request = HttpRequest()
        request.POST = self.ehn_common_data_fields

        expect(paynova_callback(request)).to_be_instance_of(HttpResponseNotFound)

    def test_callback(self):
        with HTTMock(paynova_mock):
            create_order(self.create_order_params)

        request = HttpRequest()
        request.POST = self.ehn_common_data_fields
        expect(paynova_callback(request)).to_be_instance_of(HttpResponse)

        pp = PaynovaPayment.objects.filter().first()
        expect(pp.status).to_equal(self.ehn_common_data_fields.get('PAYMENT_STATUS'))
        expect(pp.status_reason).to_equal(self.ehn_common_data_fields.get('PAYMENT_STATUS_REASON'))
        expect(pp.params_ehn).to_equal(self.ehn_common_data_fields)