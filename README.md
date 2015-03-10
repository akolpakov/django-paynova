#Paynova Aero for Django

Implementation of [Paynova Aero](http://docs.paynova.com/display/AERO/Payment+Flow) work flow for Django.
Using [Paynova API](http://docs.paynova.com/display/API/Paynova+API+Home) python library: [paynova-api-python-client](https://github.com/akolpakov/paynova-api-python-client).


# Installation
1.  Install ``django-paynova``:
    ```
    pip install django-paynova
    ```
    Python 2.7, 3.3, 3.4, PyPy are supported
    Django 1.6, 1.7 are supported

2.  Add ``django-paynova`` to ``INSTALLED_APPS``:
    ```python
    INSTALLED_APPS = (
        ...
        'django_paynova',
        ...
    )
    ```

3.  Add urls to handle Paynova's callbacks:
    ```python
    urlpatterns = patterns('',
        url(r'^(?i)payments/paynova/', include('django_paynova.urls')),
    )
    ```

# Usage
1.  Create order and init payment with default params:
    ```python
    from django_paynova import create_order, PaynovaException
    try:
        pp = create_order({
            'orderNumber': '0001',
            'currencyCode': 'EUR',
            'totalAmount': 10
        })
        # TODO: redirect to pp.url
    except PaynovaException as e:
        # TODO: handle exception
    ```

    ``create_order`` takes dictionary with [Create Order parameters](http://docs.paynova.com/display/API/Create+Order)

2.  Handle [Event Hook Notifications](http://docs.paynova.com/display/EVENTHOOKS/Event+Hook+Notifications+Home):
    ```python
    from django.dispatch import receiver
    from django_paynova.signals import paynova_payment

    @receiver(paynova_payment)
    def paynova_payment_signal(sender, status, params, **kwargs):
        # TODO: handle paynova payment notification
    ```
    where
    *   ``sender`` - PaynovaPayment model
    *   ``status`` - status of payment
    *   ``params`` - [payment params](http://docs.paynova.com/display/EVENTHOOKS/EHN%3A+Payment) from Paynova


### Advanced
Also you can create order and initialize payment separately:
```python
from django_paynova import create_order, initialize_payment, PaynovaException
try:

    # create order

    pp = create_order({
        'orderNumber': '0005',
        'currencyCode': 'EUR',
        'totalAmount': 10
    }, init_payment=False)

    # init payment. http://docs.paynova.com/display/API/Initialize+Payment

    pp = initialize_payment({'orderId': pp.order_id})

    # TODO: redirect to pp.url

except PaynovaException as e:
    # TODO: handle exception
```

*   ``create_order`` takes dictionary with [Create Order parameters](http://docs.paynova.com/display/API/Create+Order)
*   ``initialize_payment`` takes dictionary with [Initialize Payment parameters](http://docs.paynova.com/display/API/Initialize+Payment)

### Errors
If Paynova return an error, ``PaynovaException`` will be raised
```python
from django-paynova import create_order, PaynovaException

try:
    pp = create_order()
except PaynovaException as e:
    # process exception
    # e.errorNumber, e.statusKey, e.statusMessage, e.errors
    pass
```

# Tests
At first make sure that you are in virtualenv.

Install all dependencies:
```
make setup
```
To run tests:
```
make tests
```

# License
[MIT licence](./LICENSE)