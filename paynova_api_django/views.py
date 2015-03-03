from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def paynova_success(request):
    pass


@csrf_exempt
def paynova_cancel(request):
    pass


@csrf_exempt
def paynova_pending(request):
    pass


@csrf_exempt
def paynova_callback(request):
    pass