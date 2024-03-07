from django.contrib.auth import get_user_model
from rest_framework import serializers

from recipes.serializers import SubscribingRecipeSerializer
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
                user=self.context['request'].user,
                author=obj
            ).exists()
        )

    def get_recipes(self, obj):
        request = self.context.get('request')
        limit = request.GET.get(
            'recipes_limit',
            '10'
        )
        recipes = obj.recipes.all()[:int(limit)]
        serializer = SubscribingRecipeSerializer(
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
    recipes = SubscribingRecipeSerializer(
        many=True,
        read_only=True
    )
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

    def validate(self, attrs):
        request_user = self.context['request'].user
        if 'author' in attrs and request_user == attrs['author']:
            raise serializers.ValidationError(
                {'errors': 'Нельзя подписаться на самого себя'}
            )
        return attrs

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
