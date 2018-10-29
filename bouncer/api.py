from rest_framework import status, views
from rest_framework.response import Response
from .models import User, UserData, Product
from django.db import DatabaseError
from .helpers import send_verification_email
from .serializers import ProductSerializer
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect

class FetchRegistrationForm(views.APIView):
    def get(self, request, **kwargs):
        return render(request, 'signupform.html')

class RegisterUser(views.APIView):

    def post(self, request, **kwargs):
        try:
            email = request.data['email']
        except KeyError as e:
            return Response({"Error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        user, created = User.objects.get_or_create(email=request.data['email'])
        user.save()
        msg = send_verification_email(email)
        if msg[0] == 0:
            return Response({"Success" : "Email sent"}, status=status.HTTP_200_OK)
        elif msg[0] == 1:
            return Response({"Error": msg[0]}, status=status.HTTP_404_NOT_FOUND)
        elif msg[0] == 2:
            return Response({"Error": msg[1]}, status=status.HTTP_409_CONFLICT)
        elif msg[0] == 3:
            return Response({"Error": msg[0]}, status=status.HTTP_400_BAD_REQUEST)

class VerifyEmailRegisterUser(views.APIView):

    def get(self, request, **kwargs):
        try:
            user = User.objects.get(id=kwargs.get('user_id'))
            user_data = UserData.objects.get(user=user)
            key = kwargs.get('key')
        except (KeyError, User.DoesNotExist, UserData.DoesNotExist) as e:
            return Response({"Error": str(e)}, status=status.HTTP_404_NOT_FOUND)
        try:
            if user_data.is_key_expired:
                return Response({"Error": "Link expired. Unable to login"}, status=status.HTTP_204_NO_CONTENT)
            if key == user_data.activation_key:
                user_data.is_key_expired = True
                user.is_active = True
                user.save()
                user_data.save()
                return render(request, 'products.html')
            else:
                return Response({"Error": "Activation code invalid or expired"}, status=status.HTTP_304_NOT_MODIFIED)
        except DatabaseError as e:
            return Response({"Error": str(e)}, status=status.HTTP_304_NOT_MODIFIED)

class FetchProducts(views.APIView):

    def get(self, request, **kwargs):
        try:
            start = int(kwargs.get('start'))
            stop = int(kwargs.get('stop'))
        except KeyError as e:
            return Response({"Error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        try:
            products = Product.objects.all()[start:stop]
            return Response([ProductSerializer(product).data for product in products], status=status.HTTP_200_OK)
        except DatabaseError as e:
            return Response({"Error": str(e)}, status=status.HTTP_304_NOT_MODIFIED)