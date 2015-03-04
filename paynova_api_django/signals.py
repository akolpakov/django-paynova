from django.dispatch import Signal

"""
    Signal fired when Event Hook Notification from paynova comes
"""
paynova_payment = Signal(providing_args=["status", "params", ])