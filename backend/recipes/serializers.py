import base64

from django.core.files.base import ContentFile
from rest_framework import serializers

from favourites.models import Favorite
from ingredients.models import Ingredient
from ingredients.serializers import (
    IngredientRecipeCreateUpdateSerializer,
    IngredientRecipeSerializer
)
from recipes.models import (
    Recipe,
    RecipeIngredient
)
from shopping_cart.models import Shopping_cart
from tags.models import Tag
from tags.serializers import TagSerializer
from users.serializers import UserSerializer


class Base64ImageField(serializers.ImageField):
    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image'):
            format, imgstr = data.split(';base64,')
            ext = format.split('/')[-1]
            data = ContentFile(
                base64.b64decode(imgstr),
                name='temp.' + ext
            )
        return super().to_internal_value(data)


class SubscribingShoppingCartRecipeSerializer(serializers.ModelSerializer):
    '''
    Сериализатор используется для логики подписок.
    Сериализатор возвращает из списка покупок конкретные данные рецепта.
    Не включает ингридиенты.
    '''

    class Meta:
        model = Recipe
        fields = (
            'id',
            'name',
            'image',
            'cooking_time'
        )
        read_only_fields = '__all__'


class AllRecipesSerializer(serializers.ModelSerializer):
    '''Список рецептов.'''

    author = UserSerializer(read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    ingredients = IngredientRecipeSerializer(
        many=True,
        read_only=True,
        source='recipes'
    )
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()
    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = (
            'id',
            'tags',
            'author',
            'ingredients',
            'is_favorited',
            'is_in_shopping_cart',
            'name',
            'image',
            'text',
            'cooking_time'
        )

    def get_is_favorited(self, obj):
        return (
            self.context.get(
                'request'
            ).user.is_authenticated
            and Favorite.objects.filter(
                user=self.context['request'].user,
                recipe=obj
            ).exists()
        )

    def get_is_in_shopping_cart(self, obj):
        return (
            self.context.get(
                'request'
            ).user.is_authenticated
            and Shopping_cart.objects.filter(
                user=self.context['request'].user,
                recipe=obj
            ).exists()
        )


class RecipeCreateSerializer(serializers.ModelSerializer):
    '''Сериализатор используется для создания, изменения и удаления рецепта.'''

    tags = serializers.PrimaryKeyRelatedField(many=True, queryset=Tag.objects.all())
    author = UserSerializer(read_only=True)
    ingredients = IngredientRecipeCreateUpdateSerializer(many=True)
    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = (
            'id', 'tags', 'author', 'ingredients', 'image',
            'name', 'text', 'cooking_time'
        )
        extra_kwargs = {
            'name': {'required': True},
            'text': {'required': True},
            'cooking_time': {'required': True},
        }

    def validate(self, data):
        if not data.get('tags'):
            raise serializers.ValidationError('Установите тег.')
        if not data.get('ingredients'):
            raise serializers.ValidationError('Нужно выбрать минимум один ингредиент.')
        ingredient_ids = [item['id'] for item in data['ingredients']]
        if len(ingredient_ids) != len(set(ingredient_ids)):
            raise serializers.ValidationError('Ингредиенты должны быть уникальными.')
        return data

    def tags_and_ingredients_set(self, recipe, tags, ingredients):
        recipe.tags.set(tags)
        ingredient_objects = Ingredient.objects.filter(id__in=[i['id'] for i in ingredients])
        ingredient_map = {ingredient.id: ingredient for ingredient in ingredient_objects}
        recipe_ingredients = [
            RecipeIngredient(
                recipe=recipe,
                ingredient=ingredient_map[ingredient['id']],
                amount=ingredient['amount']
            ) for ingredient in ingredients
        ]
        RecipeIngredient.objects.bulk_create(recipe_ingredients)

    def create(self, validated_data):
        tags = validated_data.pop('tags')
        ingredients = validated_data.pop('ingredients')
        recipe = Recipe.objects.create(author=self.context['request'].user, **validated_data)
        self.tags_and_ingredients_set(recipe, tags, ingredients)
        return recipe

    def update(self, instance, validated_data):
        instance.image = validated_data.get('image', instance.image)
        instance.name = validated_data.get('name', instance.name)
        instance.text = validated_data.get('text', instance.text)
        instance.cooking_time = validated_data.get('cooking_time', instance.cooking_time)
        tags = validated_data.pop('tags', None)
        ingredients = validated_data.pop('ingredients', None)
        if tags is not None:
            instance.tags.set(tags)
        if ingredients is not None:
            RecipeIngredient.objects.filter(recipe=instance).delete()
            self.tags_and_ingredients_set(instance, tags, ingredients)

        instance.save()
        return instance

    def to_representation(self, instance):
        return AllRecipesSerializer(instance, context=self.context).data
