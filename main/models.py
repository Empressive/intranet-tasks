from django.db import models

from .constants import CATEGORIES_CHOICES, PRIORITY_CHOICES


class Term(models.Model):
    name = models.CharField(max_length=255)
    category = models.CharField(max_length=255, choices=CATEGORIES_CHOICES)
    description = models.TextField()


class ToDo(models.Model):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    is_done = models.BooleanField()
    priority = models.CharField(choices=PRIORITY_CHOICES, max_length=255)
    parent = models.ForeignKey('ToDo', on_delete=models.CASCADE, null=True)
