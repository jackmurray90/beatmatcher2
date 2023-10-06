from django.db import models
from django.contrib.auth.models import User
import re


def is_valid_username(username):
    return re.fullmatch("[a-zA-Z0-9_@+.-]*", username) and len(username) > 0 and len(username) <= 150


class SignUp(models.Model):
    email = models.EmailField()
    code = models.CharField(max_length=23)
    expiry = models.DateTimeField()


class Language(models.Model):
    code = models.CharField(max_length=2, primary_key=True)
    name = models.CharField(max_length=200)


class String(models.Model):
    english = models.TextField()
    language = models.ForeignKey(Language, on_delete=models.CASCADE)
    translation = models.TextField()
    in_use = models.BooleanField()


class Settings(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    language = models.ForeignKey(Language, on_delete=models.SET_NULL, null=True)


class DJ(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=200)
    description = models.TextField()
    picture = models.BooleanField()
    booking_url = models.CharField(max_length=200, null=True)
    soundcloud_url = models.CharField(max_length=200, null=True)
    rate = models.IntegerField()


class BankDetails(models.Model):
    REGIONS = [
        ("us", "United States"),
        ("australia", "Australia"),
        ("europe", "Europe"),
    ]
    ACCOUNT_TYPES = [
        ("checking", "Checking"),
        ("savings", "Savings"),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    region = models.CharField(max_length=100, choices=REGIONS)
    # All regions
    account_holder = models.CharField(max_length=500)
    # Australia
    bsb = models.CharField(max_length=20, null=True)
    # US
    ach = models.CharField(max_length=100, null=True)
    account_type = models.CharField(max_length=20, choices=ACCOUNT_TYPES, null=True)
    # Europe, US, and Australia:
    account_number = models.CharField(max_length=100, null=True)
