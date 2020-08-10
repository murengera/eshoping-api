
from django.db import models
from django.contrib.postgres.fields import ArrayField, JSONField
import uuid

import string
import random
from UserCustom.models import Users
from productCategory.models import  *
from  store.models import *




def generate_code():
    key = ''.join(random.choices(string.digits, k=12))

    return 'pr' + key



#items  conditions(ex used,news )
class ConditionItems(models.Model):
    id=models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    title=models.CharField(max_length=100,unique=True)
    description=models.TextField()
    created_at=models.DateTimeField(auto_now_add=True, editable=False)
    def __str__(self):
        return self.title

class DiscountOffer(models.Model):
    name = models.CharField(max_length=100, default='discount')
    discount_value = models.IntegerField(default=0)
    quantity = models.IntegerField(default=0)

    def save(self, *args, **kwargs):
        if self.discount_value < 0 and self.quantity<5:
            raise Exception("discount must be greater than 0 and for ones who bought above 5 items")

        super(DiscountOffer, self).save(*args, **kwargs)


class Producte(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    product_code = models.CharField(max_length=14, blank=True, editable=False)
    title = models.CharField(max_length=500,default="")
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="images")
    discount = models.ForeignKey(DiscountOffer, on_delete=models.PROTECT,null=True)
    description = models.TextField()
    total_quantity_in_stock = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    item_condition = models.ForeignKey(ConditionItems, on_delete=models.PROTECT)
    category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE)
    price=models.IntegerField(null=True)
    quantity=models.DecimalField(max_digits=20, decimal_places=2, default=0)
    is_deleted = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    delivery_fee = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    quantity_to_sell = models.DecimalField(max_digits=20, decimal_places=2,default=1)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    stock=models.ForeignKey(Stock,on_delete=models.PROTECT,null=True)



    def __str__(self):
        return str((self.title))





# STORE RATINGS (REVIEWS)
class ProductReviewers(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    review_title = models.CharField(max_length=50)
    review_text = models.TextField()
    stars = models.IntegerField(default=1)
    reviewer = models.ForeignKey(Users, on_delete=models.SET_NULL, null=True)
    product=models.ForeignKey(Producte,on_delete=models.CASCADE,null=True)


    def __str__(self):
        return str(self.id)

    def save(self, *args, **kwargs):
        if 0 > self.stars > 5:
            raise Exception('Rating out of range')

        super(ProductReviewers, self).save(*args, **kwargs)
