from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    last_user_agent = models.CharField(max_length=32)
