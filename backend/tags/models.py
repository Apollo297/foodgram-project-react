from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.validators import RegexValidator
from django.db import models

User = get_user_model()


class Tag(models.Model):
    name = models.CharField(
        max_length=settings.MAX_TAG_INGRIDIENT_LENGTH,
        unique=True,
        blank=False
    )
    color = models.CharField(
        max_length=settings.HEX_LENGTH,
        unique=True,
        blank=False
    )
    slug = models.SlugField(
        max_length=settings.MAX_TAG_INGRIDIENT_LENGTH,
        unique=True,
        blank=False,
        validators=[
            RegexValidator(
                regex=r'^[-a-zA-Z0-9_]+$'
            ),
        ]
    )
