#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of paynova-api-django.
# https://github.com/akolpakov/paynova-api-django

# Licensed under the MIT license:
# http://www.opensource.org/licenses/MIT-license
# Copyright (c) 2015, Andrey Kolpakov <aakolpakov@gmail.com>

from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render_to_response
from django.http import HttpResponseBadRequest, HttpResponseNotFound, HttpResponse
from .models import PaynovaPayment

import hashlib
import logging

log = logging.getLogger(__name__)


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
    if not _ehn_checksum(request.POST):
        log.error('EHN DIGEST hash is not verified. %s' % request.POST)
        return HttpResponseBadRequest()

    if request.POST.get('EVENT_TYPE') != 'PAYMENT':
        log.error('Unexpected EVENT_TYPE. %s' % request.POST)
        return HttpResponseBadRequest()

    try:
        pp = PaynovaPayment.objects.get(order_id=request.POST.get('ORDER_ID'), session_id=request.POST.get('SESSION_ID'))
    except PaynovaPayment.DoesNotExist:
        log.error('Unknown ORDER_ID. %s' % request.POST)
        return HttpResponseNotFound()

    pp.status = request.POST.get('PAYMENT_STATUS')
    pp.status_reason = request.POST.get('PAYMENT_STATUS_REASON')
    pp.params_ehn = request.POST
    pp.save()

    # TODO send signal

    return HttpResponse()


def _ehn_checksum(data):
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

    return data.get('DIGEST') == h.hexdigest()