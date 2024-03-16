from django.contrib.auth import get_user_model
from rest_framework import serializers

from recipes.models import Recipe
from recipes.serializers import SubscribingShoppingCartRecipeSerializer
from subscriptions.models import Subscription

User = get_user_model()


class MySubscriptionsSerializer(serializers.ModelSerializer):
    '''Возвращает пользователей, на которых подписан текущий пользователь.'''

    is_subscribed = serializers.SerializerMethodField()
    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
            'recipes',
            'recipes_count'
        )

    def get_is_subscribed(self, obj):
        return (
            self.context.get(
                'request'
            ).user.is_authenticated
            and Subscription.objects.filter(
                # user=self.context['request'].user,
                author=obj
            ).exists()
        )
    
    def get_recipes(self, obj):
        request = self.context.get('request')
        limit = request.GET.get('recipes_limit')
        if limit is not None:
            try:
                limit = int(limit)
            except ValueError:
                limit = None
        else:
            limit = None
        if limit is not None:
            all_recipes = obj.recipes.all()[:limit]
        else:
            all_recipes = obj.recipes.all()
        recipes = all_recipes
        serializer = SubscribingShoppingCartRecipeSerializer(
            recipes,
            many=True,
            read_only=True
        )
        return serializer.data

    def get_recipes_count(self, obj):
        return obj.recipes.count()


class SubscribingSerializer(serializers.ModelSerializer):
    '''Подписаться на автора или отказаться от подписки.'''

    email = serializers.ReadOnlyField()
    username = serializers.ReadOnlyField()
    is_subscribed = serializers.SerializerMethodField()
    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
            'recipes',
            'recipes_count'
        )

    def get_recipes(self, obj):
        recipe_limit = self.context.get(
            'request'
        ).query_params.get(
            'recipes_limit'
        )
        recipes = Recipe.objects.filter(author=obj)
        if recipe_limit:
            recipes = recipes[:int(recipe_limit)]
        return SubscribingShoppingCartRecipeSerializer(
            recipes,
            many=True,
            context=self.context
        ).data

    def get_is_subscribed(self, obj):
        return (
            self.context.get(
                'request'
            ).user.is_authenticated
            and Subscription.objects.filter(
                user=self.context['request'].user,
                author=obj
            ).exists()
        )

    def get_recipes_count(self, obj):
        return obj.recipes.count()
