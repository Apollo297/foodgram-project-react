from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Ingredient(models.Model):
    name = models.CharField(
        max_length=settings.MAX_TAG_INGRIDIENT_LENGTH,
        blank=False,
    )
    measure_unit = models.CharField(
        max_length=settings.MAX_TAG_INGRIDIENT_LENGTH,
        blank=False,
    )
    amount = models.FloatField()
