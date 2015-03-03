from django.shortcuts import redirect
from django.http import HttpResponse
from paynova_api_django import create_order, PaynovaException
from paynova_api_django.models import PaynovaPayment


def payment(request):
    try:
        pp = create_order({
            'orderNumber': '0001',
            'currencyCode': 'EUR',
            'totalAmount': 10
        })
        return redirect(pp.url)
    except PaynovaException as e:
        html = "<html><body>Error %s. %s %s. %s.</body></html>" % (e.errorNumber, e.statusKey, e.statusMessage, e.errors,)
        return HttpResponse(html)