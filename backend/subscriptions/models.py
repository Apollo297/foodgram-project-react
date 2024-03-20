from django.conf import settings
from django.db import models


class Subscription(models.Model):
    """Модель подписок."""

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name='Подписчик',
        related_name='subscribed_to',
        on_delete=models.CASCADE,
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name='Автор',
        related_name='subscription_authors',
        on_delete=models.CASCADE,
    )
    created_at = models.DateTimeField(
        'Дата оформления подписки',
        auto_now_add=True,
        editable=False
    )

    class Meta:
        ordering = ('-author_id',)
        verbose_name = 'Подписчик'
        verbose_name_plural = 'Подписчики'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'author'],
                name='unique_subscription'
            )
        ]

    def __str__(self):
        return f'{self.user.username} - {self.author.username}'
