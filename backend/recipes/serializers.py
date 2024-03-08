import base64

from django.core.files.base import ContentFile
from rest_framework import serializers

from recipes.models import Recipe


class Base64ImageField(serializers.ImageField):
    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image'):
            format, imgstr = data.split(';base64,')
            ext = format.split('/')[-1]
            data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)
        return super().to_internal_value(data)


class SubscribingRecipeSerializer(serializers.ModelSerializer):
    '''Сериализатор используется для логики подписок.'''

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')
        read_only_fields = '__all__'


# class RecipeSerializer(serializers.ModelSerializer):
#     """Serializer модели Recipe"""
#     tags = TagSerializer(many=True)
#     ingredients = RecipeIngredientSerializer(many=True,
#                                              source='recipe_ingredients')
#     image = Base64ImageField()
#     author = CustomUserSerializer(read_only=True)
#     is_favorited = serializers.SerializerMethodField()
#     is_in_shopping_cart = serializers.SerializerMethodField()

#     class Meta:
#         model = Recipe
#         exclude = ('pub_date',)

    # def get_is_favorited(self, obj):
    #     user = self.context['request'].user
    #     if user.is_authenticated:
    #         return Favorite.objects.filter(user=user, recipe=obj).exists()
    #     return False

    # def get_is_in_shopping_cart(self, obj):
    #     user = self.context['request'].user
    #     if user.is_authenticated:
    #         return ShoppingCart.objects.filter(user=user, recipe=obj).exists()
    #     return False