from django.db import models
from django.contrib.auth.models import AbstractUser


# Best practice we have to create our custom user model at the beginning of the project
class User(AbstractUser):
    email = models.EmailField(unique=True)
