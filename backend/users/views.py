from django.contrib.auth import (
    authenticate,
    get_user_model,
    login,
    logout
)
from django.http import Http404
from rest_framework import (
    generics,
    permissions
)
from rest_framework.authtoken.models import Token
from rest_framework.pagination import PageNumberPagination
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


class UsersPagination(PageNumberPagination):
    page_size = 6


class UserViewSet(viewsets.ViewSet):
    '''
    Вьюсет обрабатывает список пользователей, регистрацию пользователя и
    профиль пользователяю
    '''

    def list(self, request):
        queryset = User.objects.all().order_by('id')
        paginator = UsersPagination()
        page = paginator.paginate_queryset(
            queryset,
            request
        )
        if page is not None:
            serializer = UserSerializer(
                page,
                many=True,
                context={'request': request}
            )
            return paginator.get_paginated_response(serializer.data)
        serializer = UserSerializer(
            queryset, many=True,
            context={'request': request}
        )
        return Response(serializer.data)

    def create(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            user.set_password(
                serializer.validated_data['password']
            )
            user.save()
            response_serializer = UserRegistrationSerializer(
                user,
                context={'request': request}
            )
            return Response(
                response_serializer.data,
                status=status.HTTP_201_CREATED
            )
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

    def retrieve(self, request, pk=None):
        try:
            user = User.objects.get(pk=pk)
        except User.DoesNotExist:
            raise Http404
        serializer = UserSerializer(user, context={'request': request})
        return Response(serializer.data)


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
