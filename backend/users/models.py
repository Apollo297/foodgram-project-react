from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models

from users.utils import my_max_length
from users.validators import validate_username


class User(AbstractUser):
    '''Кастомная модель пользователя.'''

    email = models.EmailField(
        'Адрес электронной почты',
        help_text='Электронная почта',
        max_length=settings.MAX_LENGTH_EMAIL,
        blank=False,
        unique=True,
    )
    username = models.SlugField(
        'Имя пользователя',
        help_text='Имя пользователя',
        max_length=settings.MAX_LENGTH_USER_FIELDS,
        blank=False,
        unique=True,
        validators=[
            RegexValidator(
                regex=r'^[\w.@+-]+\Z'
            ),
            validate_username
        ],
    )
    first_name = models.CharField(
        'Имя',
        help_text='Имя',
        max_length=settings.MAX_LENGTH_USER_FIELDS,
        blank=False,
    )
    last_name = models.CharField(
        'Фамилия',
        help_text='Фамилия',
        max_length=settings.MAX_LENGTH_USER_FIELDS,
        blank=False,
    )
    password = models.CharField(
        'Пароль',
        help_text='Пароль',
        max_length=settings.MAX_LENGTH_USER_FIELDS,
        blank=False,
    )
    is_subscribed = models.BooleanField(
        'Подписка',
        blank=True,
        default=False
    )
    role = models.CharField(
        max_length=my_max_length(
            settings.USER_ROLES
        ),
        verbose_name='Роль',
        choices=settings.USER_ROLES,
        default=settings.USER,
        help_text='Пользователь',
    )

    class Meta:
        ordering = ('-username',)
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    @property
    def is_admin(self):
        return (
            self.role == settings.ADMIN
            or self.is_staff or self.is_superuser
        )

    @property
    def is_user(self):
        return self.role == settings.USER

    def __str__(self):
        return self.username[:settings.SYMBOL_LIMIT]

