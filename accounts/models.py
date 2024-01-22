# accounts/models.py

from django.contrib.auth.models import AbstractUser
from django.db import models
from shortuuid.django_fields import ShortUUIDField
class CustomUser(AbstractUser):
    id = ShortUUIDField(primary_key=True,max_length=20,length=10,prefix="rest",alphabet="abcdefhgigklmnoqz93801 ", unique=True)
    email = models.EmailField(unique=True)
    otp = models.CharField(max_length=6, null=True, blank=True)  # Add the otp field here

    # Add custom fields here, if needed

    def __str__(self):
        return self.username
