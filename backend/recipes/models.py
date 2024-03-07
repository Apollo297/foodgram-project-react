from django.conf import settings
from django.core.validators import MinValueValidator
from django.db import models

from ingredients.models import Ingredient
from tags.models import Tag


class Recipe(models.Model):
    ''''Модель рецептов.'''

    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name='Автор',
        related_name='recipes'
    )
    name = models.CharField(
        'Название',
        max_length=settings.MAX_TAG_INGRIDIENT_LENGTH,
        blank=False
    )
    image = models.ImageField(
        'Ссылка на картинку на сайте',
        blank=False
    )
    text = models.TextField(
        'Описание',
        blank=False
    )
    cooking_time = models.PositiveIntegerField(
        'Время приготовления (в минутах)',
        validators=[
            MinValueValidator(1)
        ],
        blank=False
    )
    tags = models.ManyToManyField(
        Tag,
        verbose_name='Теги',
        related_name='recipes',
        blank=False
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        through='RecipeIngredient',
        blank=False
    )
    is_favorited = models.BooleanField(
        'Находится ли в избранном',
        default=False
    )
    is_in_shopping_cart = models.BooleanField(
        'Находится ли в корзине',
        default=False
    )
    pub_date = models.DateTimeField(
        'Дата публикации',
        auto_now_add=True,
        editable=False
    )

    class Meta:
        ordering = ('-pub_date',)
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return self.name


class RecipeIngredient(models.Model):
    '''Модель, связывающая Recipe и Ingredient.'''

    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='recipe_ingredients'
    )
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        related_name='ingredient_recipes'
    )
    amount = models.PositiveIntegerField('Количество')

    class Meta:
        ordering = ('id',)
        verbose_name = 'Ингредиент в рецепте'
        verbose_name_plural = 'Ингредиенты в рецептах'
        unique_together = (
            'recipe',
            'ingredient'
        )

    def __str__(self):
        return f'{self.ingredient.name} в рецепте "{self.recipe.name}"'
