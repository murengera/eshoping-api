from django.conf import  settings
import africastalking
from  django.core.mail import  EmailMessage


def send_email(subject,message,user=None,email=None):

    if subject is not None and message is not None:
        pass
    elif  user is  not  None:
        em=EmailMessage(subject,message,to=[user.email])
        em.send()

    elif email is not None:
        em=EmailMessage(subject,message,to=[email])
        em.send()
    else:
        raise  Exception("Email content is not  valid")