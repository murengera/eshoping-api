from UserCustom.models import Verification, Users
from notifications.utils import sms_backend



def send_verification_code(user):
    instance = Verification.objects.filter(user=user).first()
    phone_number = user.phone_number

    if instance is None:
        instance = Verification(
            user=user
        )
    instance.save()
    code = instance.code
    print("Verification code for user {} is {}".format(user.phone_number, code))

    try:
        sms_backend.send("Nexmarket verification code is {}".format(code), [phone_number])

    except:
        send_verification_code(user)
