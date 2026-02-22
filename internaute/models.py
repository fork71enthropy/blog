from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db import models

class Internaute(AbstractUser):
    pseudo = models.CharField(max_length=100, unique=True)
    creation_date = models.DateTimeField(auto_now_add=True)
    subscriber = models.BooleanField(default=False)
# Create your models here.
