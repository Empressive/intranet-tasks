from django.db import models

from .constants import CATEGORIES_CHOICES


class Term(models.Model):
    name = models.CharField(max_length=255)
    category = models.CharField(max_length=255, choices=CATEGORIES_CHOICES)
    description = models.TextField()
