from django.db import models

# Create your models here.

class Settings(models.Model):
    key = models.CharField(
        max_length=50,
        unique=True,
        null=False,
        blank=False,
    )
    value = models.JSONField(
        null=True,
        blank=True,
    )
    name = models.CharField(
        max_length=30,
        null=False
    )

class Currency(models.Model):
    name = models.CharField(
        max_length=50,
    )
    symbol = models.CharField(
        max_length=15,
    )