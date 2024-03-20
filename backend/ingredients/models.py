from django.conf import settings
from django.db import models


class Ingredient(models.Model):
    """Модель ингредиентов."""

    name = models.CharField(
        'Название',
        max_length=settings.MAX_TAG_INGRIDIENT_LENGTH,
    )
    measurement_unit = models.CharField(
        'Единицы измерения',
        max_length=settings.MAX_TAG_INGRIDIENT_LENGTH,
    )

    class Meta:
        ordering = ('name',)
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'

    def __str__(self):
        return f'{self.name} ({self.measurement_unit})'
