from django.db import models
from django.contrib.auth.models import AbstractUser

from mailes.models import Mail


# Create your models here.
class User(AbstractUser):
    picture = models.ImageField(upload_to='images', verbose_name='عکس')
