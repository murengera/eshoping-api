from django.conf import settings
import africastalking

from eShoping import settings
"""

AFRICA'S TALKING SETUP

"""

username = settings.AFRICASTALKING_USERNAME
api_key = settings.AFRICASTALKING_APIKEY

africastalking.initialize(username, api_key)
sms_backend = africastalking.SMS

