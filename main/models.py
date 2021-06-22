from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _
from accounts.models import Account
import datetime

# student number 1067036209

class Teacher(Account):
    TITLES = (
        ('Ms', 'Ms'),
        ('Mr', 'Mr'),
        ('Dr', 'Dr'),
        ('Sir', 'Sir'),
        ('Prof', 'Prof')
    )
    title = models.CharField(max_length=10, null=True, choices=TITLES)
    subject = models.ManyToManyField("Subject")
    bio = models.TextField(null=True, default=None)

    def __str__(self):
        return f"{self.firstName} {self.lastName}, {self.schoolID}"


class Student(Account):
    slug = models.SlugField(null=True, default=None)

    def __str__(self):
        return f"{self.firstName} {self.lastName}, {self.schoolID}"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.email)
        return super().save(*args, **kwargs)
        
    def get_absolute_url(self):
        return reverse("main:student", kwargs={"student": self.slug})


class Subject(models.Model):
    students = models.ManyToManyField(
        Student, through='Enrol', related_name='subjects'
    )
    name = models.CharField(max_length=100)
    LEVELS = (
        ('10', '10'),
        ('11', '11'),
        ('12', '12'),
    )
    level = models.CharField(max_length=10, null=True, default=None, choices=LEVELS)
    # slug = models.SlugField(unique=True, default=None)

    def get_absolute_url(self):
        return reverse('main:subject', kwargs={'slug': self.id})

    def __str__(self):
        return f"{self.name} - {self.level}"


class Enrol(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, null=True)
    subject = models.ForeignKey(Subject, on_delete=models.SET_NULL, null=True)
    created = models.DateTimeField(auto_now_add=True, null=True)
    active = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = 'Enrolment'

    def __str__(self):
        return f'{self.student} - {self.subject}'
