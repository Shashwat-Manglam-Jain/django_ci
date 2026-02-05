from django.db import models
from .managers import UserManager
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    username = models.CharField(max_length=80,  null=False)
    email = models.EmailField(
        "Email Address",
        unique=True,
    )
    ROLES=(
        ('seller',"seller"),
        ('buyer','Buyer'),
    )
    roles = models.CharField(max_length=50, choices = ROLES, default='buyer')
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'roles']

    objects = UserManager()

    def __str__(self):
        return self.email