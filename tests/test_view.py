#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of django-paynova.
# https://github.com/akolpakov/django-paynova

# Licensed under the MIT license:
# http://www.opensource.org/licenses/MIT-license
# Copyright (c) 2015, Andrey Kolpakov <aakolpakov@gmail.com>

from preggy import expect
from tests.base import TestCase
from httmock import HTTMock
from datetime import datetime
from django.http import HttpResponse, HttpRequest, HttpResponseBadRequest, HttpResponseNotFound
from django.conf import settings
from django.dispatch import receiver
from django_paynova import create_order
from django_paynova.views import paynova_callback, paynova_cancel, paynova_pending, paynova_success
from django_paynova.models import PaynovaPayment
from django_paynova.signals import paynova_payment
from .mock import paynova_mock

import hashlib
import sys

_ver = sys.version_info


class ViewTestCase(TestCase):
    ehn_common_data_fields = None

    def _get_checksum(self, data):
        hash_string = '%s;%s;%s;%s;%s;' % (
            data.get('EVENT_TYPE'),
            data.get('EVENT_TIMESTAMP'),
            data.get('DELIVERY_TIMESTAMP'),
            data.get('MERCHANT_ID'),
            settings.PAYNOVA_SECRET
        )

        if _ver >= (3, 0):
            hash_string = hash_string.encode('ascii')

        h = hashlib.sha1()
        h.update(hash_string)

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

    def test_signal(self):
        with HTTMock(paynova_mock):
            create_order(self.create_order_params)

        @receiver(paynova_payment)
        def paynova_payment_signal(sender, status, params, **kwargs):
            pp = PaynovaPayment.objects.filter().first()
            expect(status).to_equal(self.ehn_common_data_fields.get('PAYMENT_STATUS'))
            expect(sender).to_equal(pp)
            expect(params).to_equal(self.ehn_common_data_fields)

        request = HttpRequest()
        request.POST = self.ehn_common_data_fields
        expect(paynova_callback(request)).to_be_instance_of(HttpResponse)