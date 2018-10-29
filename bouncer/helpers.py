import random
from .constants import HOST, REGISTER_REDIRECT_URL
from supplyAI.settings import EMAIL_HOST_USER
from django.core.mail import send_mail
from .models import User, UserData

def send_verification_email(email):
    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        return 1, "User does not exist"
    user_data, created = UserData.objects.get_or_create(user=user)
    key = ''.join(random.choice('0123456789ABCDEF') for _ in range(32))
    subject = "Welcome to SupplyAI!"
    link = HOST + REGISTER_REDIRECT_URL + str(user.id) + '/' + key
    from_email = EMAIL_HOST_USER
    to_list = [user.email]
    message = 'Please use the following link to login.\n\n{}'.format(link)
    try:
        send_mail(subject, message, from_email, to_list, fail_silently=True)
    except KeyError as e:
        return 3, str(e)
    user_data.activation_key = key
    user_data.is_key_expired = False
    user_data.save()
    return 0, "Registration mail sent"