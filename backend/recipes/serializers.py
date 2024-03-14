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
from shopping_cart.models import ShoppingCart
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

    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = (
            'id',
            'name',
            'image',
            'cooking_time'
        )
        read_only_fields = (
            'id',
            'name',
            'image',
            'cooking_time'
        )


class AllRecipesSerializer(serializers.ModelSerializer):
    '''Список рецептов.'''

    author = UserSerializer(read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    ingredients = IngredientRecipeSerializer(
        many=True,
        read_only=True,
        source='recipe_ingredients'
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
            and ShoppingCart.objects.filter(
                user=self.context['request'].user,
                recipe=obj
            ).exists()
        )


class RecipeCreateSerializer(serializers.ModelSerializer):
    '''Сериализатор используется для создания, изменения и удаления рецепта.'''

    tags = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Tag.objects.all()
    )
    author = UserSerializer(read_only=True)
    ingredients = IngredientRecipeCreateUpdateSerializer(many=True)
    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = (
            'id',
            'tags',
            'author',
            'ingredients',
            'image',
            'name',
            'text',
            'cooking_time'
        )
        extra_kwargs = {
            'name': {'required': True},
            'text': {'required': True},
            'cooking_time': {'required': True},
        }

    def validate_ingredients(self, value):
        ingredients = value
        if not ingredients:
            raise serializers.ValidationError('Нужен хотя бы один ингредиент!')
        ingredient_ids = [item['id'] for item in ingredients]
        existing_ingredient_ids = Ingredient.objects.filter(
            id__in=ingredient_ids
        ).values_list(
            'id',
            flat=True
        )
        non_existing_ids = set(ingredient_ids) - set(existing_ingredient_ids)
        if non_existing_ids:
            raise serializers.ValidationError(
                f'Ингредиенты с ID {non_existing_ids} не существуют.'
            )
        ingredients_list = []
        for item in ingredients:
            ingredient = Ingredient.objects.get(
                id=item['id']
            )
            if ingredient in ingredients_list:
                raise serializers.ValidationError(
                    'Ингридиенты не могут повторяться.'
                )
            if int(item['amount']) <= 0:
                raise serializers.ValidationError(
                    'Количество должно быть больше 0.'
                )
            ingredients_list.append(ingredient)
        return value

    def validate_tags(self, value):
        tags = value
        if not tags:
            raise serializers.ValidationError(
                {'tags': 'Нужно выбрать хотя бы один тег!'}
            )
        tags_list = []
        for tag in tags:
            if tag in tags_list:
                raise serializers.ValidationError(
                    {'tags': 'Теги должны быть уникальными!'}
                )
            tags_list.append(tag)
        return value

    def tags_and_ingredients_set(self, recipe, tags, ingredients):
        recipe.tags.set(tags)
        ingredient_objects = Ingredient.objects.filter(
            id__in=[i['id'] for i in ingredients]
        )
        if len(ingredient_objects) != len(ingredients):
            raise serializers.ValidationError(
                'Один или несколько ингредиентов не существуют.'
            )
        ingredient_map = {
            ingredient.id: ingredient for ingredient in ingredient_objects
        }
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
        recipe = Recipe.objects.create(
            author=self.context['request'].user, **validated_data
        )
        self.tags_and_ingredients_set(recipe, tags, ingredients)
        return recipe

    def update(self, instance, validated_data):
        tags = validated_data.get('tags')
        if tags is None:
            raise serializers.ValidationError(
                {'tags': 'Поле tags обязательно для обновления.'}
            )
        ingredients = validated_data.get('ingredients')
        if ingredients is None:
            raise serializers.ValidationError(
                {'ingredients': 'Поле ingredients обязательно для обновления.'}
            )
        instance.image = validated_data.get('image', instance.image)
        instance.name = validated_data.get('name', instance.name)
        instance.text = validated_data.get('text', instance.text)
        instance.cooking_time = validated_data.get(
            'cooking_time', instance.cooking_time
        )
        tags = validated_data.pop('tags', None)
        RecipeIngredient.objects.filter(
            recipe=instance
        ).delete()
        self.tags_and_ingredients_set(
            instance,
            tags,
            ingredients
        )
        instance.save()
        return instance

    def to_representation(self, instance):
        return AllRecipesSerializer(
            instance,
            context=self.context
        ).data
