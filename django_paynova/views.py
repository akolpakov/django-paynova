#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of django-paynova.
# https://github.com/akolpakov/django-paynova

# Licensed under the MIT license:
# http://www.opensource.org/licenses/MIT-license
# Copyright (c) 2015, Andrey Kolpakov <aakolpakov@gmail.com>

from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render_to_response
from django.http import HttpResponseBadRequest, HttpResponseNotFound, HttpResponse
from .models import PaynovaPayment
from .signals import paynova_payment

import hashlib
import logging
import sys

log = logging.getLogger(__name__)
_ver = sys.version_info


@csrf_exempt
def paynova_success(request):
    return render_to_response('paynova/success.html', {'data': request.POST})


@csrf_exempt
def paynova_cancel(request):
    return render_to_response('paynova/cancel.html', {'data': request.POST})


@csrf_exempt
def paynova_pending(request):
    return render_to_response('paynova/pending.html', {'data': request.POST})


@csrf_exempt
def paynova_callback(request):
    """
        Handle Event Hook Notifications from Paynova
    """

    # check DIGEST

    if not _ehn_checksum(request.POST):
        log.error('EHN DIGEST hash is not verified. %s' % request.POST)
        return HttpResponseBadRequest()

    # check EVENT_TYPE

    if request.POST.get('EVENT_TYPE') != 'PAYMENT':
        log.error('Unexpected EVENT_TYPE. %s' % request.POST)
        return HttpResponseBadRequest()

    # get PaynovaPayment from model

    try:
        pp = PaynovaPayment.objects.get(order_id=request.POST.get('ORDER_ID'), session_id=request.POST.get('SESSION_ID'))
    except PaynovaPayment.DoesNotExist:
        log.error('Unknown ORDER_ID. %s' % request.POST)
        return HttpResponseNotFound()

    pp.status = request.POST.get('PAYMENT_STATUS')
    pp.status_reason = request.POST.get('PAYMENT_STATUS_REASON')
    pp.params_ehn = request.POST
    pp.save()

    # send signal

    paynova_payment.send(sender=pp, params=request.POST, status=request.POST.get('PAYMENT_STATUS'))

    return HttpResponse()


def _ehn_checksum(data):
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

    return data.get('DIGEST') == h.hexdigest()