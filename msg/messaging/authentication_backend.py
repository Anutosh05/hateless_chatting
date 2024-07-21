# authentication_backend.py
from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.models import User
from .models import Customer


class PhoneNumberBackend(BaseBackend):
    def authenticate(self, request, phone_number=None, password=None):
        try:
            customer = Customer.objects.get(phone_number=phone_number)
            if customer.check_password(password):
                user, created = User.objects.get_or_create(username=customer.user)
                if created:
                    user.set_password(password)
                    user.save()
                return user
        except Customer.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
