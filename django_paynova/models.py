#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of django-paynova.
# https://github.com/akolpakov/django-paynova

# Licensed under the MIT license:
# http://www.opensource.org/licenses/MIT-license
# Copyright (c) 2015, Andrey Kolpakov <aakolpakov@gmail.com>

from django.db import models

import json


class PaynovaPayment(models.Model):
    """
        Model for storing all transactions to Paynova
        *status* shows current status of payment.
    """

    STATUS_ORDER_CREATED = 'ORDER_CREATED'
    STATUS_PAYMENT_INITED = 'PAYMENT_INITED'
    STATUS_CANCELLED = 'CANCELLED'
    STATUS_DECLINED = 'DECLINED'
    STATUS_ERROR = 'ERROR'
    STATUS_PENDING = 'PENDING'
    STATUS_COMPLETED = 'COMPLETED'
    STATUS_AUTHORIZED = 'AUTHORIZED'

    date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=255, null=True, blank=True)
    status_reason = models.TextField(null=True, blank=True)

    order_id = models.CharField(max_length=255, null=True, blank=True, unique=True)
    session_id = models.CharField(max_length=255, null=True, blank=True, unique=True)
    url = models.CharField(max_length=255, null=True, blank=True)

    _params_create_order = models.TextField(null=True, blank=True)
    _params_init_payment = models.TextField(null=True, blank=True)
    _params_ehn = models.TextField(null=True, blank=True)

    @property
    def params_create_order(self):
        return json.loads(self._params_create_order)

    @params_create_order.setter
    def params_create_order(self, value):
        self._params_create_order = json.dumps(value)

    @property
    def params_init_payment(self):
        return json.loads(self._params_init_payment)

    @params_init_payment.setter
    def params_init_payment(self, value):
        self._params_init_payment = json.dumps(value)

    @property
    def params_ehn(self):
        return json.loads(self._params_ehn)

    @params_ehn.setter
    def params_ehn(self, value):
        self._params_ehn = json.dumps(value)