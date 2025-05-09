from django.db import models
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField
import uuid

class User(AbstractUser):
    # Reference: https://tomharrisonjr.com/uuid-or-guid-as-primary-keys-be-careful-7b2aa3dcb439
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    contact = PhoneNumberField(blank=True, null=True)

    class meta:
        db_table = "User_Data"

