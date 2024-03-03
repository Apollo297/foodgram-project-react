from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Subscription(models.Model):
    ''''Модель подписок.'''

    user = models.ForeignKey(
        User,
        verbose_name='Подписчик',
        on_delete=models.CASCADE,
        related_name='subscribed_to'
    )
    author = models.ForeignKey(
        User,
        verbose_name='Автор',
        on_delete=models.CASCADE,
        related_name='subscription_authors'
    )
    created_at = models.DateTimeField(
        'Дата оформления подписки',
        auto_now_add=True,
        editable=False
    )

    class Meta:
        ordering = ('id',)
        verbose_name = 'Подписчик'
        verbose_name_plural = 'Подписчики'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'author'],
                name='unique_subscription'
            )
        ]
