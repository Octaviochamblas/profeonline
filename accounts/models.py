from django.contrib.auth.models import User
from django.db import models


class Profile(models.Model):
    ROLE_CHOICES = [
        ("alumno", "Alumno"),
        ("profesor", "Profesor"),
        ("apoderado", "Apoderado"),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    phone = models.CharField(max_length=30, blank=True)
    city = models.CharField(max_length=100, blank=True)
    institution = models.CharField(max_length=150, blank=True)
    education_level = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.get_role_display()}"