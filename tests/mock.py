from tests.base import TestCase
from httmock import all_requests

import json

@all_requests
def paynova_mock(url, request):
    def success(content=None):
        if not content:
            content = {}

        content['status'] = {
            'isSuccess': True,
            'errorNumber': 0,
            'statusKey': 'SUCCESS',
        }

        return {'status_code': 200, 'content': content}

    def fail(content=None, errorNumber=None, statusKey=None):
        if not content:
            content = {}

        content['status'] = {
            'isSuccess': False,
            'errorNumber': errorNumber,
            'statusKey': statusKey,
        }

        return {'status_code': 200, 'content': content}

    if url[2] == '/api/orders/create':
        params = json.loads(request.body)
        if params.get('orderNumber') == '0001':
            return success({
                'orderId': TestCase.ORDER_ID
            })
        else:
            return fail()

    elif url[2] == ('/api/orders/%s/initializePayment' % TestCase.ORDER_ID):
        params = json.loads(request.body)
        if params.get('should_fail'):
            return fail()
        else:
            return success({
                'sessionId': TestCase.ORDER_SESSION_ID,
                'url': TestCase.ORDER_URL
            })

    return {'status_code': 404}