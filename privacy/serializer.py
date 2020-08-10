from rest_framework import serializers

from privacy.models import *


class PrivacyPoliciesOrTermsOfUseSerializer(serializers.ModelSerializer):

    class Meta:
        model = PrivacyPoliciesAndTermsOfUse
        fields = '__all__'
