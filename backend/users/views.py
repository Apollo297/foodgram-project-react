from django.contrib.auth import (
    authenticate,
    get_user_model,
    login,
    logout
)
from django.db import IntegrityError
from rest_framework import (
    generics,
    permissions
)
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, viewsets

from users.serializers import (
    ChangePasswordSerializer,
    TokenSerializer,
    UserRegistrationSerializer,
    UserSerializer,
)

User = get_user_model()


# class UserListView(generics.ListAPIView):
#     '''Список всех пользователей.'''

#     queryset = User.objects.all()
#     serializer_class = UserSerializer

class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserProfileView(generics.RetrieveAPIView):
    '''Подробная информация о пользователе по ID.'''

    queryset = User.objects.all()
    serializer_class = UserSerializer


class CurrentUserView(generics.RetrieveAPIView):
    '''Подробная информация о текущем пользователе.'''

    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user


class UserRegistrationView(generics.CreateAPIView):
    '''Регистрация пользователя.'''

    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            username = serializer.validated_data['username']
            try:
                user, created = User.objects.get_or_create(
                    email=email,
                    username=username,
                    defaults={
                        'first_name': serializer.validated_data.get(
                            'first_name', ''
                        ),
                        'last_name': serializer.validated_data.get(
                            'last_name', ''
                        ),
                    }
                )
                if created:
                    user.set_password(
                        serializer.validated_data['password']
                    )
                    user.save()
                    return Response(
                        serializer.data, status=status.HTTP_201_CREATED
                    )
                return Response(
                    'Такое username или email уже существует.',
                    status=status.HTTP_400_BAD_REQUEST
                )
            except IntegrityError:
                return Response(
                    'Такое username или email уже существует.',
                    status=status.HTTP_400_BAD_REQUEST
                )
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )


class ChangePasswordView(generics.UpdateAPIView):
    '''Изменение пароля текущим пользователем.'''

    serializer_class = ChangePasswordSerializer
    model = User
    permission_classes = [permissions.IsAuthenticated,]

    def get_object(self):
        return self.request.user


class LoginView(APIView):
    '''Представление для логина.'''

    def post(self, request, *args, **kwargs):
        serializer = TokenSerializer(data=request.data)
        if serializer.is_valid():
            user = authenticate(
                request,
                password=serializer.validated_data['password'],
                username=serializer.validated_data['email']
            )
            if user is not None:
                login(request, user)
                token, _ = Token.objects.get_or_create(
                    user=user
                )
                return Response(
                    {'auth_token': token.key},
                    status=status.HTTP_201_CREATED
                )
            return Response(
                {'error': 'Учётные данные неверны'},
                status=status.HTTP_400_BAD_REQUEST
            )
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


class LogoutView(APIView):
    '''Представление для логаута.'''

    def post(self, request, *args, **kwargs):
        request.user.auth_token.delete()
        logout(request)
        return Response(
            status=status.HTTP_204_NO_CONTENT
        )
