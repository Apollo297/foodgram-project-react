from rest_framework import serializers

from recipes.models import Recipe


class SubscribingRecipeSerializer(serializers.ModelSerializer):
    '''Сериализатор используется для логики подписок.'''

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')
        read_only_fields = '__all__'
