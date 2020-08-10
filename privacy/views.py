from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from rest_framework import generics, mixins
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from privacy.models import PrivacyPoliciesAndTermsOfUse
from privacy.serializer import PrivacyPoliciesOrTermsOfUseSerializer


class PrivacyPoliciesAndTermsOfUseList(generics.GenericAPIView,
                                       mixins.ListModelMixin,
                                       mixins.CreateModelMixin):

    queryset = PrivacyPoliciesAndTermsOfUse.objects.all()
    serializer_class = PrivacyPoliciesOrTermsOfUseSerializer


    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        user = request.user
        #request.data['created_by'] = str(user.id)
        return self.create(request, *args, **kwargs)


class PrivacyPoliciesAndTermsOfUseDetails(generics.GenericAPIView,
                                          mixins.RetrieveModelMixin,
                                          mixins.UpdateModelMixin,
                                          mixins.DestroyModelMixin):

    queryset = PrivacyPoliciesAndTermsOfUse.objects.all()
    serializer_class = PrivacyPoliciesOrTermsOfUseSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

