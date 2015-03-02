#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of paynova-api-django.
# https://github.com/akolpakov/paynova-api-django

# Licensed under the MIT license:
# http://www.opensource.org/licenses/MIT-license
# Copyright (c) 2015, Andrey Kolpakov <aakolpakov@gmail.com>

from django.db import models

import json


class PaynovaPayment(models.Model):
    STATUS_CREATE = 'create'
    STATUS_INIT = 'init'
    STATUS_PENDING = 'pending'
    STATUS_SUCCESS = 'success'
    STATUS_CANCEL = 'cancel'
    STATUS_FAIL = 'fail'

    STATUSES = (
        (STATUS_CREATE, 'Create'),
        (STATUS_INIT, 'Init'),
        (STATUS_PENDING, 'Pending'),
        (STATUS_SUCCESS, 'Success'),
        (STATUS_CANCEL, 'Cancel'),
        (STATUS_FAIL, 'Fail'),
    )

    date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=STATUSES, null=True, blank=True)
    error = models.TextField(null=True, blank=True)

    order_id = models.CharField(max_length=255, null=True, blank=True, unique=True)
    session_id = models.CharField(max_length=255, null=True, blank=True, unique=True)
    url = models.CharField(max_length=255, null=True, blank=True)

    _params_create_order = models.TextField(null=True, blank=True)
    _params_init_payment = models.TextField(null=True, blank=True)

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