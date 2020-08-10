from django.db import models
import uuid
from UserCustom.models import Users
class ProductCategory(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    title = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True, editable=False,null=True)
    created_by=models.ForeignKey(Users,on_delete=models.PROTECT,default="")

    def __str__(self):
        return self.title

class Brand(models.Model):
    id= models.UUIDField(editable=False,primary_key=True,default=uuid.uuid4)
    title=models.CharField(max_length=50)
    image=models.ImageField(upload_to="images/brandsImage")
    description=models.TextField()
    rank=models.CharField(max_length=100)
    created_by=models.ForeignKey(Users,on_delete=models.PROTECT)
    def __str__(self):
        return self.title
