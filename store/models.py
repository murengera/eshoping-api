from django.db import models
from django.core.serializers.json import DjangoJSONEncoder
from django.contrib.auth.models import User as Base_user
import uuid
from django.contrib.postgres.fields import ArrayField, JSONField
from datetime import datetime
import time
from UserCustom.models import Users
from django.db import models
import random
import string



def generate_code():
    key=''.join(random.choices(string.digits,k=10))
    return 'ST'+key

class Stock(models.Model):
    id=models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    stock_code=models.CharField(max_length=12, blank=True, editable=False)
    name=models.CharField(max_length=100,default="clothes")
    description = models.TextField()
    icon = models.ImageField(upload_to='images/stores_icons')
    banner = models.ImageField(upload_to="images/stores_banners", null=True, blank=True)
    address = JSONField(default=dict)
    workers = models.ManyToManyField(Users)
    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    time_created = models.DateTimeField(auto_now_add=True)
    activated_by = models.ForeignKey(Users, on_delete=models.PROTECT, null=True, blank=True,  related_name='activated_by_user')
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return str(self.name)

    def save(self, *args, **kwargs):
        if self.is_active and not self.activated_by:
            raise Exception('Must provide who activated the store')

        if not self.stock_code:
            self.stock_code = generate_code()

        super(Stock, self).save(*args, **kwargs)


#STORE RATINGZ
class StockRating(models.Model):
    id=models.UUIDField(primary_key=True,editable=False,default=uuid.uuid4)
    review_title=models.CharField(max_length=50)
    review_text=models.TextField()
    stars=models.IntegerField()
    reviewer=models.ForeignKey(Users,on_delete=models.SET_NULL,null=True)
    store=models.ForeignKey(Stock,on_delete=models.CASCADE)

    def __str__(self):
        return  str(self.id)

    def save(self,*args,**kwargs):
        if self.stars<0 or self.stars > 5:
            raise  Exception('Rating out of range')
        super(StockRating,self).save(*args,**kwargs)
