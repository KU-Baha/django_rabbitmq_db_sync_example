from django.db import models


class Product(models.Model):
    title = models.CharField(
        max_length=255
    )
    image = models.URLField()
    likes = models.PositiveIntegerField(
        default=0
    )


class User(models.Model):
    pass
