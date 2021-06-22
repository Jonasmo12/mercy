from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from main.utils import randomNumber

from .managers import AccountManager


class Account(AbstractBaseUser, PermissionsMixin):
    schoolID = models.BigIntegerField(_('schoolID'), default=randomNumber, unique=True, null=True)
    email = models.EmailField(_('Email Address'), unique=True)
    firstName = models.CharField(max_length=100, verbose_name='First Name')
    lastName = models.CharField(max_length=100, verbose_name='Last Name')
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_student = models.BooleanField(default=False)
    is_teacher = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = 'schoolID'
    REQUIRED_FIELDS = ['email']

    objects = AccountManager()

    def __str__(self):
        return f"{self.firstName} {self.lastName}, {self.schoolID}"