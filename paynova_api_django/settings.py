from django.conf import settings

PAYNOVA_USERNAME = getattr(settings, 'PAYNOVA_USERNAME', None)
PAYNOVA_PASSWORD = getattr(settings, 'PAYNOVA_PASSWORD', None)
PAYNOVA_LIVE = getattr(settings, 'PAYNOVA_LIVE', False)
PAYNOVA_ENDPOINT = getattr(settings, 'PAYNOVA_ENDPOINT', None)