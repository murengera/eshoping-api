from django.db import models
from django.core.serializers.json import DjangoJSONEncoder
from django.contrib.auth.models import User as Base_user
import uuid
from django.contrib.postgres.fields import ArrayField, JSONField
from datetime import datetime
import time

from store.models import Stock
from UserCustom.models import Users

TIME_NOW = str(int(round(time.time()) * 1000))

#CAROUSEL ADS
class Carousel_ad(models.Model):
    id=models.UUIDField(primary_key=True,editable=False,default=uuid.uuid4)
    image=models.CharField(max_length=1000)
    title=models.CharField(max_length=500)
    description=models.TextField()
    is_active=models.BooleanField(default=False)
    expire_date=models.DateTimeField(null=True,blank=True)
    action_name=models.CharField(max_length=50)
    action=models.TextField()
    store=models.ForeignKey(Stock,on_delete=models.PROTECT,null=True)
    created_by=models.ForeignKey(Users,on_delete=models.PROTECT)
    is_deleted=models.BooleanField(default=False)
    def __str__(self):
        return  self.title


