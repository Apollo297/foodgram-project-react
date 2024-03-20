from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models


class User(AbstractUser):
    """Кастомная модель пользователя."""

    email = models.EmailField(
        'Адрес электронной почты',
        help_text='Электронная почта',
        max_length=settings.MAX_LENGTH_EMAIL,
        unique=True,
    )
    username = models.CharField(
        'Имя пользователя',
        help_text='Имя пользователя',
        max_length=settings.MAX_LENGTH_USER_FIELDS,
        unique=True,
        validators=[
            RegexValidator(
                regex=r'^[\w.@+-]+\Z'
            )
        ],
    )
    first_name = models.CharField(
        'Имя',
        help_text='Имя',
        max_length=settings.MAX_LENGTH_USER_FIELDS,
    )
    last_name = models.CharField(
        'Фамилия',
        help_text='Фамилия',
        max_length=settings.MAX_LENGTH_USER_FIELDS,
    )
    password = models.CharField(
        'Пароль',
        help_text='Пароль',
        max_length=settings.MAX_LENGTH_USER_FIELDS,
    )
    is_subscribed = models.BooleanField(
        'Подписка',
        blank=True,
        default=False
    )
    role = models.CharField(
        max_length=max(
            len(role[0]) for role in settings.USER_ROLES
        ),
        verbose_name='Роль',
        choices=settings.USER_ROLES,
        default=settings.USER,
        help_text='Пользователь',
    )

    class Meta:
        ordering = ('username',)
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username[:settings.SYMBOL_LIMIT]

    @property
    def is_admin(self):
        return (
            self.role == settings.ADMIN
            or self.is_staff or self.is_superuser
        )

    @property
    def is_user(self):
        return self.role == settings.USER
