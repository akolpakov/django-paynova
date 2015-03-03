#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of paynova-api-django.
# https://github.com/akolpakov/paynova-api-django

# Licensed under the MIT license:
# http://www.opensource.org/licenses/MIT-license
# Copyright (c) 2015, Andrey Kolpakov <aakolpakov@gmail.com>

from preggy import expect
from tests.base import TestCase
from httmock import all_requests, HTTMock
from django.test.utils import override_settings
from paynova_api_django import create_order, initialize_payment
from paynova_api_django.models import PaynovaPayment
from paynova_api_django.payment import _get_url_params, _get_params_for_initialize_payment
from paynova_api_python_client import PaynovaException

import json


@all_requests
def paynova_mock(url, request):
    def success(content=None):
        if not content:
            content = {}

        content['status'] = {
            'isSuccess': True,
            'errorNumber': 0,
            'statusKey': 'SUCCESS',
        }

        return {'status_code': 200, 'content': content}

    def fail(content=None, errorNumber=None, statusKey=None):
        if not content:
            content = {}

        content['status'] = {
            'isSuccess': False,
            'errorNumber': errorNumber,
            'statusKey': statusKey,
        }

        return {'status_code': 200, 'content': content}

    if url[2] == '/api/orders/create':
        params = json.loads(request.body)
        if params.get('orderNumber') == '0001':
            return success({
                'orderId': TestCase.ORDER_ID
            })
        else:
            return fail()

    elif url[2] == ('/api/orders/%s/initializePayment' % TestCase.ORDER_ID):
        params = json.loads(request.body)
        if params.get('should_fail'):
            return fail()
        else:
            return success({
                'sessionId': TestCase.ORDER_SESSION_ID,
                'url': TestCase.ORDER_URL
            })

    return {'status_code': 404}


class PaymentTestCase(TestCase):
    create_order_params = {
        'orderNumber': '0001',
        'currencyCode': 'EUR',
        'totalAmount': 10
    }

    def setUp(self):
        PaynovaPayment.objects.all().delete()

    def tearDown(self):
        pass

    def test_create_order_success(self):
        with HTTMock(paynova_mock):
            pp = create_order(self.create_order_params, init_payment=False)
            expect(pp).to_be_instance_of(PaynovaPayment)
            expect(pp.order_id).to_equal(TestCase.ORDER_ID)
            expect(pp.status).to_equal(PaynovaPayment.STATUS_CREATE)
            expect(pp.params_create_order).to_equal(self.create_order_params)

    def test_create_order_fail(self):
        with HTTMock(paynova_mock):
            params = self.create_order_params.copy()
            params['orderNumber'] = '0002'

            with expect.error_to_happen(PaynovaException):
                create_order(params, init_payment=False)

            pp = PaynovaPayment.objects.filter().first()
            expect(pp).to_be_instance_of(PaynovaPayment)
            expect(pp.order_id).to_be_null()
            expect(pp.status).to_equal(PaynovaPayment.STATUS_FAIL)
            expect(pp.params_create_order).to_equal(params)

    def test_get_url_params(self):
        url_params = _get_url_params()
        expect(url_params).to_length(4)

    @override_settings(PAYNOVA_CALLBACK_URL=None)
    def test_get_url_params_fail(self):
        with expect.error_to_happen(PaynovaException):
            _get_url_params()

    def test_get_params_for_initialize_payment(self):
        with expect.error_to_happen(PaynovaException):
            _get_params_for_initialize_payment({})

        with expect.error_to_happen(PaynovaException):
            _get_params_for_initialize_payment({'orderId': 'not-exists'})

        with HTTMock(paynova_mock):
            pp = create_order(self.create_order_params, init_payment=False)
            params, pp = _get_params_for_initialize_payment({
                'orderId': pp.order_id,
                'test': 'test'
            })
            expect(pp).to_be_instance_of(PaynovaPayment)
            expect(params).to_be_instance_of(dict)
            expect(params.get('test')).to_equal('test')
            expect(params.get('orderId')).to_equal(pp.order_id)
            expect(params.get('totalAmount')).to_equal(pp.params_create_order.get('totalAmount'))
            expect(params).to_include('interfaceOptions')
            expect(params['interfaceOptions']).to_length(6)

    def test_initialize_payment_success(self):
        with HTTMock(paynova_mock):
            pp = create_order(self.create_order_params, init_payment=False)
            pp = initialize_payment({'orderId': pp.order_id})

            expect(pp).to_be_instance_of(PaynovaPayment)
            expect(pp.order_id).to_equal(TestCase.ORDER_ID)
            expect(pp.session_id).to_equal(TestCase.ORDER_SESSION_ID)
            expect(pp.url).to_equal(TestCase.ORDER_URL)
            expect(pp.status).to_equal(PaynovaPayment.STATUS_INIT)
            expect(pp.params_create_order).to_equal(self.create_order_params)
            expect(pp.params_init_payment).not_to_be_null()

    def test_initialize_payment_fail(self):
        with HTTMock(paynova_mock):
            pp = create_order(self.create_order_params, init_payment=False)

            with expect.error_to_happen(PaynovaException):
                initialize_payment({'orderId': pp.order_id, 'should_fail': True})

            pp = PaynovaPayment.objects.filter().first()
            expect(pp).to_be_instance_of(PaynovaPayment)
            expect(pp.order_id).to_equal(TestCase.ORDER_ID)
            expect(pp.session_id).to_be_null()
            expect(pp.url).to_be_null()
            expect(pp.status).to_equal(PaynovaPayment.STATUS_FAIL)
            expect(pp.params_create_order).to_equal(self.create_order_params)
            expect(pp.params_init_payment).not_to_be_null()

    def test_create_and_init(self):
        with HTTMock(paynova_mock):
            pp = create_order(self.create_order_params, init_payment=True)
            expect(pp).to_be_instance_of(PaynovaPayment)
            expect(pp.order_id).to_equal(TestCase.ORDER_ID)
            expect(pp.session_id).to_equal(TestCase.ORDER_SESSION_ID)
            expect(pp.url).to_equal(TestCase.ORDER_URL)
            expect(pp.status).to_equal(PaynovaPayment.STATUS_INIT)
            expect(pp.params_create_order).to_equal(self.create_order_params)
            expect(pp.params_init_payment).not_to_be_null()