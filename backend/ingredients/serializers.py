from django.conf import settings

from rest_framework import serializers

from recipes.models import (
    Ingredient,
    RecipeIngredient
)


class IngredientSerializer(serializers.ModelSerializer):
    """Список ингредиентов."""

    class Meta:
        model = Ingredient
        fields = (
            'id',
            'name',
            'measurement_unit'
        )


class IngredientRecipeCreateUpdateSerializer(serializers.ModelSerializer):
    """
    Сериализатор используется для подготовки данных об ингредиентах,
    Гарантирует включение данных в рецепт согласно требованиям к формату.
    """

    id = serializers.IntegerField()
    amount = serializers.IntegerField(
        min_value=settings.MIN_VALUE,
        max_value=settings.MAX_VALUE
    )

    class Meta:
        model = RecipeIngredient
        fields = (
            'id',
            'amount'
        )


class IngredientRecipeSerializer(serializers.ModelSerializer):
    """
    Сериализатор используется для вывода списка ингредиентов в рецепте.
    Дополнительно выводятся сумма и количество.
    """

    id = serializers.ReadOnlyField(
        source='ingredient.id'
    )
    name = serializers.ReadOnlyField(
        source='ingredient.name'
    )
    measurement_unit = serializers.ReadOnlyField(
        source='ingredient.measurement_unit'
    )

    class Meta:
        model = RecipeIngredient
        fields = (
            'id',
            'name',
            'measurement_unit',
            'amount'
        )
