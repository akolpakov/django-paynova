#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of django-paynova.
# https://github.com/akolpakov/django-paynova

# Licensed under the MIT license:
# http://www.opensource.org/licenses/MIT-license
# Copyright (c) 2015, Andrey Kolpakov <aakolpakov@gmail.com>

from django.conf import settings
from .models import PaynovaPayment
from paynova_api_python_client import Paynova, PaynovaException
from django.core.urlresolvers import reverse


def create_order(params, init_payment=True):
    """
        Create order
        :param params: See docs for params
        :param init_payment: If True - auto init payment.
        :return: PaynovaPayment model

        Docs: http://docs.paynova.com/display/API/Create+Order
    """

    # create a model

    model = PaynovaPayment()
    model.params_create_order = params
    model.save()

    # make request

    client = Paynova(settings.PAYNOVA_MERCHANT_ID, settings.PAYNOVA_PASSWORD,
                     live=settings.PAYNOVA_LIVE, endpoint=settings.PAYNOVA_ENDPOINT)

    try:
        response = client.create_order(params)
    except PaynovaException as e:
        model.status = PaynovaPayment.STATUS_ERROR
        model.status_reason = '%s' % e
        model.save()
        raise e

    model.order_id = response.get('orderId')
    model.status = PaynovaPayment.STATUS_ORDER_CREATED
    model.save()

    # make init with defaults

    if init_payment:
        return initialize_payment({'orderId': model.order_id})

    return model


def _get_url_params():
    """
        Build urls for callbacks
        Docs: http://docs.paynova.com/display/API/Initialize+Payment
    """
    if not settings.PAYNOVA_CALLBACK_URL:
        raise PaynovaException({'statusMessage': 'PAYNOVA_CALLBACK_URL should be defined in settings'})

    url = settings.PAYNOVA_CALLBACK_URL.strip('/')

    return {
        'urlRedirectSuccess': '%s%s' % (url, reverse('paynova_success')),
        'urlRedirectCancel': '%s%s' % (url, reverse('paynova_cancel')),
        'urlRedirectPending': '%s%s' % (url, reverse('paynova_pending')),
        'urlCallback': '%s%s' % (url, reverse('paynova_callback')),
    }


def _get_params_for_initialize_payment(params):
    """
        Get params and model
    """
    order_id = params.get('orderId')
    if not order_id:
        raise PaynovaException({'statusMessage': 'Parameter "orderId" must be defined'})
    try:
        model = PaynovaPayment.objects.get(order_id=order_id)
    except PaynovaPayment.DoesNotExist:
        raise PaynovaException({'statusMessage': 'Order with "orderId" = %s was not found in model' % order_id})

    # set default params

    return_params = {
        'orderId': order_id,
        'totalAmount': model.params_create_order.get('totalAmount'),
        'paymentChannelId': 1,
        'interfaceOptions': {
            'interfaceId': 5,
            'customerLanguageCode': settings.PAYNOVA_DEFAULT_LANGUAGE,
        }
    }

    return_params.update(params)
    return_params['interfaceOptions'].update(_get_url_params())

    return return_params, model


def initialize_payment(params):
    """
        Initializa payment
        :param params: See docs
        :return: PaynovaPayment model

        Docs: http://docs.paynova.com/display/API/Initialize+Payment
    """

    # get model and params based on passed data

    params, model = _get_params_for_initialize_payment(params)

    model.params_init_payment = params
    model.save()

    # make request

    client = Paynova(settings.PAYNOVA_MERCHANT_ID, settings.PAYNOVA_PASSWORD,
                     live=settings.PAYNOVA_LIVE, endpoint=settings.PAYNOVA_ENDPOINT)

    try:
        response = client.initialize_payment(params)
    except PaynovaException as e:
        model.status = PaynovaPayment.STATUS_ERROR
        model.status_reason = '%s' % e
        model.save()
        raise e

    model.session_id = response.get('sessionId')
    model.url = response.get('url')
    model.status = PaynovaPayment.STATUS_PAYMENT_INITED
    model.save()

    return model