from django.conf import settings
from django.core.validators import RegexValidator
from django.db import models


class Tag(models.Model):
    '''Модель для тегов.'''

    name = models.CharField(
        'Название',
        max_length=settings.MAX_TAG_INGRIDIENT_LENGTH,
        unique=True,
    )
    color = models.CharField(
        'Цвет в HEX',
        max_length=settings.HEX_LENGTH,
        unique=True,
    )
    slug = models.SlugField(
        'Уникальный слаг',
        max_length=settings.MAX_TAG_INGRIDIENT_LENGTH,
        unique=True,
        validators=[
            RegexValidator(
                regex=r'^[-a-zA-Z0-9_]+$'
            ),
        ]
    )

    class Meta:
        ordering = ('name',)
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return self.name
