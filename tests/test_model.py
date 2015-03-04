#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of paynova-api-django.
# https://github.com/akolpakov/paynova-api-django

# Licensed under the MIT license:
# http://www.opensource.org/licenses/MIT-license
# Copyright (c) 2015, Andrey Kolpakov <aakolpakov@gmail.com>

from preggy import expect
from tests.base import TestCase
from paynova_api_django.models import PaynovaPayment


class ModelTestCase(TestCase):
    test_object = {
        'test_string': 'test',
        'test_int': 1,
        'test_array': [
            'test1', 'test2', 'test3'
        ],
        'test_object': {
            'test1': 1,
            'test2': 2
        }
    }

    def setUp(self):
        PaynovaPayment.objects.all().delete()

    def tearDown(self):
        pass

    def test_save_empty_model(self):
        pp = PaynovaPayment()
        pp.save()
        expect(pp).to_be_instance_of(PaynovaPayment)

    def test_params_create_order(self):
        pp = PaynovaPayment()
        pp.params_create_order = self.test_object
        pp.save()

        pp2 = PaynovaPayment.objects.filter().first()

        expect(pp2.params_create_order).to_equal(self.test_object)

    def test_params_init_payment(self):
        pp = PaynovaPayment()
        pp.params_init_payment = self.test_object
        pp.save()

        pp2 = PaynovaPayment.objects.filter().first()

        expect(pp2.params_init_payment).to_equal(self.test_object)

    def test_params_ehn(self):
        pp = PaynovaPayment()
        pp.params_ehn = self.test_object
        pp.save()

        pp2 = PaynovaPayment.objects.filter().first()

        expect(pp2.params_ehn).to_equal(self.test_object)