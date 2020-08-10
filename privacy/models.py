from django.db import models

# Create your models here.
import uuid

from django.db import models
from django.contrib.postgres.fields import ArrayField, JSONField

from UserCustom.models import Users


class PrivacyPoliciesAndTermsOfUse(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    title = models.CharField(max_length=200)
    text =models.TextField()
    created_by = models.ForeignKey(Users, on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True)
    edited_at = models.DateTimeField(auto_now=True)
    languages = {
        ('rwandese', 'rwandese'),
        ('english', 'english')
    }
    language = models.CharField(max_length=30, choices=languages)
    types = {
        ('privacy_policy', 'privacy_policy'),
        ('terms_of_use', 'terms_of_use')
    }
    _type = models.CharField(max_length=50, choices=types)

    class Meta:
        verbose_name_plural = "Privacy Policies and Terms Of Use"

    def __str__(self):
        return self.title


