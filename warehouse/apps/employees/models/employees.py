from django.db import models
from django.contrib.auth.models import User
from phonenumber_field.modelfields import PhoneNumberField

class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name=models.CharField(blank=False, null=False, max_length=255)
    last_name=models.CharField(blank=False, null=False, max_length=255)
    job_title=models.CharField(blank=False, null=False, max_length=255)
    phone=PhoneNumberField(blank=True)

    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name} ({self.job_title})"
    