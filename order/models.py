from django.db import models
import random
import string
from django.db import models
from django.core.serializers.json import  DjangoJSONEncoder
from django.contrib.auth.models import User as Base_user
import  uuid
from django.contrib.postgres.fields import JSONField
from datetime import datetime, timedelta
import time

from rest_framework import request

from  store.models import  Stock
from  UserCustom.models import  Users
from product.models import Producte, DiscountOffer




TIME_NOW=str(int(round(time.time())*1000))


def generate_code():

        key = ''.join(random.choices(string.digits, k=16))
        return 'OR' + key



class Order(models.Model):
    id=models.UUIDField(primary_key=True,editable=False,default=uuid.uuid4)
    order_code=models.CharField(max_length=18,blank=True,editable=False)
    buyer=models.ForeignKey(Users,on_delete=models.PROTECT,null=True)
    product=models.ForeignKey(Producte,on_delete=models.PROTECT,null=True)
    price=models.DecimalField(max_digits=20,decimal_places=2,default=0)
    quantity=models.DecimalField(max_digits=20,decimal_places=2,null=True)
    total_price=models.DecimalField(max_digits=20,decimal_places=2,default=0)
    created_at = models.DateField(auto_now_add=True,editable=False,null=True)
    finished_at = models.DateField(auto_now_add=False,editable=True,null=True, blank=True)
    comment=models.TextField(null=True,blank=True)


    statuses = [
        ('NEW', 'NEW'),
        ('ACTIVE', 'ACTIVE'),
        ('FINISHED', 'FINISHED')
    ]

    status = models.CharField(max_length=50, choices=statuses, default='NEW')

    def __str__(self):
        self.order_code=generate_code()
        return str(self.order_code)

    def save(self,*args,**kwargs):

        statuses = ( 'NEW',  'ACTIVE','FINISHED' )
        if self.status not in statuses:
            raise Exception("The status is not valid")

        if self.status == 'NEW':
            self.reference_code = generate_code()
            self.order_code = generate_code()
            self.auto_cancels_at = datetime.now() + timedelta(seconds=180)


        #if  self.status=="ACTIVE":
            #raise Exception("actvated")

        #if self.status=="FINISHED":
         #   raise Exception("finished")


        else:
          self.auto_cancels_at = None

        if self.price<0:
            raise Exception("unit price can't be zero")


        if self.price and self.quantity:
            self.sub_total=float(self.price *self.quantity)
        super(Order,self).save(*args,**kwargs)
