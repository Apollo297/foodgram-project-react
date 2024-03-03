from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

from subscriptions.models import (
    Subscription
)

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    '''Общий сериализатор пользователя.'''

    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
        )
        extra_kwargs = {'password': {'write_only': True}}
        read_only_fields = ('id',)

    def get_is_subscribed(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return Subscription.objects.filter(
                subscriber=request.user,
                author=obj
            ).exists()
        return False


class UserRegistrationSerializer(serializers.ModelSerializer):
    '''Сериализатор для регистрации пользователя.'''

    class Meta:
        model = User
        fields = (
            'email',
            'username',
            'first_name',
            'last_name',
            'password'
        )
        extra_kwargs = {'password': {'write_only': True}}

    def validate_password(self, value):
        validate_password(value)
        return value

    def validate_username(self, value):
        if value.lower() == 'me':
            raise serializers.ValidationError(
                'Недопустимое имя пользователя.'
            )
        return value


class ChangePasswordSerializer(serializers.Serializer):
    '''Сериализатор для изменения пароля текущего пользователя.'''

    new_password = serializers.CharField(
        required=True
    )
    current_password = serializers.CharField(
        required=True
    )

    def validate_new_password(self, value):
        validate_password(value)
        return value

    def validate(self, data):
        user = self.context['request'].user
        if not user.check_password(data.get('current_password')):
            raise serializers.ValidationError(
                {'current_password': ['Действующий пароль указан неверно.']}
            )
        return data

    def update(self, instance, validated_data):
        instance.set_password(
            validated_data['new_password']
        )
        instance.save()
        return instance


class TokenSerializer(serializers.Serializer):
    '''Сериализатор для авторизации пользователя.'''

    password = serializers.CharField(
        required=True
    )
    email = serializers.EmailField(
        required=True
    )
