from django.contrib.auth.models import AbstractUser
from django.core.validators import FileExtensionValidator
from django.db import models

from utils.choices import (
    JOB_TYPE_CHOICES,
    JOB_WORKPLACE_CHOICES,
    JOB_EXPERIENCE_LEVEL,
    JOB_STATUS_CHOICES,
    USER_ROLE_CHOICES
)
from utils.custom_manager import UserManager


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)


class Job(BaseModel):
    title = models.CharField(max_length=255)
    type = models.CharField(max_length=50, choices=JOB_TYPE_CHOICES)
    location = models.CharField(max_length=50)
    salary = models.IntegerField(blank=True, null=True)
    company_name = models.CharField(max_length=50)
    workplace = models.CharField(max_length=50, choices=JOB_WORKPLACE_CHOICES)
    description = models.TextField()
    experience_level = models.CharField(max_length=50, choices=JOB_EXPERIENCE_LEVEL)
    status = models.CharField(max_length=50, choices=JOB_STATUS_CHOICES)


class User(AbstractUser):
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=50, default="job_hunter", choices=USER_ROLE_CHOICES)
    is_active = models.BooleanField(default=True)
    objects = UserManager()
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []


class Application(models.Model):
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.EmailField(unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_in_application")
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name="job_in_application")
    resume = models.FileField(upload_to="resume", validators=[FileExtensionValidator(["pdf", "doc", "docx"])])
