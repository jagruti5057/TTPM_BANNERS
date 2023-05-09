
from django.core.mail import send_mail
import random
from django.conf import settings
from rest_framework.permissions import IsAuthenticated,IsAdminUser
from rest_framework.pagination import PageNumberPagination
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model

from django.core.mail import send_mail, BadHeaderError
import logging
import secrets
logger = logging.getLogger(__name__)

def send_otp_via_email(email):
    subject = 'OTP Verification'
    otp = secrets.randbelow(9000) + 1000
    message = f'Your OTP is {otp}. Please use this to verify your email.'
    email_from = settings.EMAIL_HOST
    try:
        send_mail(subject, message, email_from, [email])
    except BadHeaderError as e:
        logger.error(f"Failed to send OTP email: {str(e)}")
    except Exception as e:
        logger.error(f"Failed to send OTP email: {str(e)}")
    
    return otp


def send_otp(phone):
        if phone:
            key = random.randint(1000, 9999)    
            print(key)
            return key
        
        else:
            return False
        
        
#
class IsAuthenticatedOrCreate(IsAdminUser):
    def has_permission(self, request, view):
        if request.user.is_admin == True:
            return True
        return super(IsAuthenticatedOrCreate, self).has_permission(request, view)
    
    
    
class PermissionPolicyMixin:
    def check_permissions(self, request):
        try:
            # This line is heavily inspired from `APIView.dispatch`.
            # It returns the method associated with an endpoint.
            handler = getattr(self, request.method.lower())
        except AttributeError:
            handler = None

        if (
            handler
            and self.permission_classes_per_method
            and self.permission_classes_per_method.get(handler.__name__)
        ):
            self.permission_classes = self.permission_classes_per_method.get(handler.__name__)

        super().check_permissions(request)


class Custom_Pagination(PageNumberPagination):
    def get_paginated_response(self, data):
        data={
        'next': self.get_next_link(),
        'previous': self.get_previous_link(),
        'results': data
        }
        return data
    


class EmailPhoneBackend(ModelBackend):
    def authenticate(self, request, email=None, password=None):
        UserModel = get_user_model()

        # Check if either email or phone_number is provided
        if email is None and password is None:
            return None

        # Authenticate based on email
        if email is not None:
            try:
                user = UserModel.objects.get(email=email)
            except UserModel.DoesNotExist:
                return None
        # Authenticate based on phone_number
        else:
            try:
                user = UserModel.objects.get(password=password)
            except UserModel.DoesNotExist:
                return None

        # Return the authenticated user if found
        return user

    def get_user(self, user_id):
        UserModel = get_user_model()
        try:
            return UserModel.objects.get(pk=user_id)
        except UserModel.DoesNotExist:
            return None
