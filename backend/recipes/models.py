# from django.conf import settings
# from django.contrib.auth import get_user_model
# from django.core.validators import MinValueValidator
# from django.db import models

# from ingredients.models import Ingredient
# from tags.models import Tag

# User = get_user_model()


# class Recipe(models.Model):
#     author = models.ForeignKey(
#         'User', on_delete=models.CASCADE
#     )
#     name = models.CharField(
#         max_length=settings.MAX_TAG_INGRIDIENT_LENGTH
#     )
#     image = models.TextField(
#         blank=False
#     )
#     text = models.TextField(
#         blank=False
#     )
#     cooking_time = models.IntegerField(
#         validators=[
#             MinValueValidator(1)
#         ],
#         blank=False
#     )
#     tags = models.ManyToManyField(
#         Tag,
#         through='RecipeTag',
#         blank=False
#     )
#     ingredients = models.ManyToManyField(
#         Ingredient,
#         through='RecipeIngredient',
#         blank=False
#     )
#     is_favorited = models.BooleanField(
#         default=False
#     )
#     is_in_shopping_cart = models.BooleanField(
#         default=False
#     )


# class RecipeTag(models.Model):
#     recipe = models.ForeignKey(
#         Recipe,
#         on_delete=models.CASCADE
#     )
#     tag = models.ForeignKey(
#         Tag,
#         on_delete=models.CASCADE
#     )


# class RecipeIngredient(models.Model):
#     recipe = models.ForeignKey(
#         Recipe,
#         on_delete=models.CASCADE
#     )
#     ingredient = models.ForeignKey(
#         Ingredient,
#         on_delete=models.CASCADE
#     )
