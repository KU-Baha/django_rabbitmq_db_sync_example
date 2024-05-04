from django.db import models


class Product(models.Model):
    id = models.PositiveIntegerField(
        primary_key=True
    )
    title = models.CharField(
        max_length=255
    )
    image = models.URLField()


class User(models.Model):
    products = models.ManyToManyField(
        Product,
        related_name="users"
    )
