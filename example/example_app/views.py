from django.http import HttpResponse, HttpResponseRedirect
from paynova_api_django import create_order, PaynovaException


def payment(request):
    try:
        pp = create_order({
            'orderNumber': '0005',
            'currencyCode': 'EUR',
            'totalAmount': 10
        })
        return HttpResponseRedirect(pp.url)
    except PaynovaException as e:
        html = "<html><body>Error %s. %s %s. %s.</body></html>" % (e.errorNumber, e.statusKey, e.statusMessage, e.errors,)
        return HttpResponse(html)
    except Exception as e:
        html = "<html><body>Error %s.</body></html>" % e
        return HttpResponse(html)