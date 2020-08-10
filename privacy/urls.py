from django.urls import path

from privacy.views import PrivacyPoliciesAndTermsOfUseList, PrivacyPoliciesAndTermsOfUseDetails

urlpatterns = [
    path('privacy/', PrivacyPoliciesAndTermsOfUseList.as_view(),  name='privacy'),
    path('privacy/<slug:pk>', PrivacyPoliciesAndTermsOfUseDetails.as_view(),
         name='privacy_policies_and_terms_of_use_details'),
]
