#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of django-paynova.
# https://github.com/akolpakov/django-paynova

# Licensed under the MIT license:
# http://www.opensource.org/licenses/MIT-license
# Copyright (c) 2015, Andrey Kolpakov <aakolpakov@gmail.com>

from django.dispatch import Signal

"""
    Signal fired when Event Hook Notification from paynova comes
"""
paynova_payment = Signal(providing_args=["status", "params", ])