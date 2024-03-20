from django.conf import settings
from django.db import models

from recipes.models import Recipe


class ShoppingCart(models.Model):
    """Модель списка покупок."""

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='shopping_user',
        verbose_name='Пользователь',
        on_delete=models.CASCADE,
    )
    recipe = models.ForeignKey(
        Recipe,
        related_name='shopping_recipe',
        verbose_name='Рецепт',
        on_delete=models.CASCADE,
    )

    class Meta:
        ordering = ('-id',)
        verbose_name = 'Список покупок'
        verbose_name_plural = 'Список покупок'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'],
                name='unique_shopping_cart'
            )
        ]

    def __str__(self):
        return f'{self.user.username} - {self.recipe.name}'
