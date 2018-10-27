from django.conf.urls import url
from .api import *

urlpatterns = [
    url(r'^user/register$', RegisterUser.as_view(), name='register_user'),
    url(r'^user/email/verify/(?P<user_id>[\w.-]+)/(?P<key>[\w.-]+)$', VerifyEmailRegisterUser.as_view(),
        name='verify_email'),
]
