#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of paynova-api-django.
# https://github.com/akolpakov/paynova-api-django

# Licensed under the MIT license:
# http://www.opensource.org/licenses/MIT-license
# Copyright (c) 2015, Andrey Kolpakov <aakolpakov@gmail.com>

from django.conf import settings


def setting_default(name, default_value):
    value = getattr(settings, name, default_value)
    setattr(settings, name, value)

setting_default('PAYNOVA_USERNAME', None)
setting_default('PAYNOVA_PASSWORD', None)
setting_default('PAYNOVA_LIVE', False)
setting_default('PAYNOVA_ENDPOINT', None)
setting_default('PAYNOVA_DEFAULT_LANGUAGE', 'eng')
setting_default('PAYNOVA_CALLBACK_URL', None)

from payment import create_order, initialize_payment