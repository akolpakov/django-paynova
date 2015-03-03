#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of paynova-api-django.
# https://github.com/akolpakov/paynova-api-django

# Licensed under the MIT license:
# http://www.opensource.org/licenses/MIT-license
# Copyright (c) 2015, Andrey Kolpakov <aakolpakov@gmail.com>

from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render_to_response


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
    pass