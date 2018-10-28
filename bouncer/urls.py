from django.conf.urls import url
from .api import *
from django.views.generic import TemplateView

urlpatterns = [
    url(r'^user/register$', RegisterUser.as_view(), name='register_user'),
    url(r'^user/signup$', FetchRegistrationForm.as_view(), name='signup_form'),
    url(r'^user/email/verify/(?P<user_id>[\w.-]+)/(?P<key>[\w.-]+)$', VerifyEmailRegisterUser.as_view(),
        name='verify_email'),
    url(r'^products/(?P<start>[\w.-]+)/(?P<stop>[\w.-]+)$', FetchProducts.as_view(), name='products'),
]
