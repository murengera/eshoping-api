import  random
import string
import time
import uuid
from django.db import  models
from  django.conf import settings
from django.contrib.auth.models import  AbstractUser,Group
from django.db.models.signals import  post_save
from  django.dispatch import receiver
from django.utils import timezone
from rest_framework.authtoken.models import  Token
from UserCustom.manager import  UserManager
from UserCustom.utils.fields_utils import NullableCharField




#CUSTOM USER
class  Users(AbstractUser):
    id = models.UUIDField(primary_key=True,editable=False,default=uuid.uuid4)
    name = models.CharField(max_length=255)
    username = NullableCharField(max_length=50, unique=True, null=True, blank=True)  # Overriding Abstract user username
    phone_number = models.CharField(max_length=15,unique=True,null=True)
    email = models.EmailField(max_length=255,unique=True,null=True)
    USERNAME_FIELD ='phone_number'
    objects = UserManager()

    def is_from_stock(self):
        group = self.groups.first()

        store_manager = Group.objects.get(name=' Manager')
        store_worker = Group.objects.get(name=' Worker')


        if group == store_manager or \
                group == store_worker:
            return True

        return False

    def save(self, *args, **kwargs):

        if not str(self.phone_number).startswith('+'):
            raise Exception("Phone number must start with a '+'")

        super(Users, self).save(*args, **kwargs)

    def __str__(self):
        return self.phone_number


def generate_code():
    key = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
    return key


class Verification(models.Model):
    code = models.CharField(max_length=8, blank=True)
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    time_created = models.DateTimeField(auto_now=True)
    categories = {
        ('Activation', 'Activation'),
        ('Reset', 'Reset')
    }
    category = models.CharField(max_length=100, choices=categories, default='Activation')
    is_used = models.BooleanField(default=False)

    def __str__(self):
        return self.code

    def save(self, *args, **kwargs):
        # Create Verification access_code, if it exists generate another one
        while not self.code:
            code = generate_code()
            same_access_code = Verification.objects.filter(code=code)

            if not same_access_code:
                self.code = code

        super(Verification, self).save(*args, **kwargs)

#person who sell product
class Seller(models.Model):
    user = models.OneToOneField(to=Users, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class DeliveryInfo(models.Model):
    user = models.OneToOneField(to=Users, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    phone = models.CharField(max_length=31)
