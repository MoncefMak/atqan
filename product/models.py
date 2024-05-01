from django.db import models

from core.abstract_class import AuditModel


class Product(AuditModel):
    name = models.CharField(max_length=255, unique=True)
    price = models.FloatField()


