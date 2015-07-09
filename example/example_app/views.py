from django.http import HttpResponse, HttpResponseRedirect
from django.dispatch import receiver
from django_paynova import create_order, PaynovaException
from django_paynova.signals import paynova_payment


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


@receiver(paynova_payment)
def paynova_payment_signal(sender, status, params, **kwargs):
    # TODO: handle paynova payment notification
    # sender - PaynovaPayment model
    # status - status of a payment
    # params - params of notification (see http://docs.paynova.com/display/EVENTHOOKS/EHN%3A+Payment)
    pass
