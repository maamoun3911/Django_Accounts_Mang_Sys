from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
class CustomUser(AbstractUser):
    
    email = models.EmailField(max_length=256, unique=True)

    def __str__(self) -> str:
        return self.username
