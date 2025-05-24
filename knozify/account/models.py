import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


class User(AbstractUser):
    # Reference: https://tomharrisonjr.com/uuid-or-guid-as-primary-keys-be-careful-7b2aa3dcb439
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    contact = PhoneNumberField(blank=True, null=True)

    class meta:
        db_table = "User_Data"

