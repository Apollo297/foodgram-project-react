from django.contrib.auth import (
    authenticate,
    get_user_model,
    login,
    logout
)
from django.contrib.auth.backends import ModelBackend
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import (
    permissions
)
from rest_framework.authtoken.models import Token
from rest_framework.decorators import action
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import (
    filters,
    status,
    viewsets
)

from users.serializers import (
    ChangePasswordSerializer,
    TokenSerializer,
    UserRegistrationSerializer,
    UserSerializer,
)


User = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    permission_classes = [permissions.AllowAny]
    filter_backends = (
        DjangoFilterBackend,
        filters.OrderingFilter
    )
    ordering_fields = ('id',)
    ordering = ('id',)
    # filterset_fields = ('id',)

    def get_serializer_class(self):
        if self.action == 'create':
            return UserRegistrationSerializer
        elif self.action == 'set_password':
            return ChangePasswordSerializer
        elif self.action in [
            'list',
            'retrieve',
            'me'
        ]:
            return UserSerializer
        return super().get_serializer_class()

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(
            self.get_queryset()
        )

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(
                page,
                many=True
            )
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(
            queryset,
            many=True
        )
        return Response(serializer.data)

    def create(
            self,
            request,
            *args,
            **kwargs
    ):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        user.set_password(
            serializer.validated_data['password']
        )
        user.save()
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED,
            headers=headers
        )

    @action(
        detail=False,
        methods=['post'],
        permission_classes=[permissions.IsAuthenticated]
    )
    def set_password(self, request):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            current_password = serializer.validated_data['current_password']
            new_password = serializer.validated_data['new_password']

            if request.user.check_password(current_password):
                request.user.set_password(new_password)
                request.user.save()
                return Response(status=status.HTTP_204_NO_CONTENT)
            else:
                return Response(
                    {'detail': 'Неверный текущий пароль.'},
                    status=status.HTTP_400_BAD_REQUEST
                )
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

    @action(
        detail=False,
        methods=['get'],
        permission_classes=[permissions.IsAuthenticated]
    )
    def me(self, request):
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)


class LoginView(APIView):
    '''Представление для логина.'''

    permission_classes = (permissions.AllowAny,)

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


class EmailBackend(ModelBackend):
    def authenticate(
            self,
            request,
            username=None,
            password=None,
            **kwargs
    ):
        try:
            user = User.objects.get(email=username)
            if user.check_password(password):
                return user
        except User.DoesNotExist:
            return None


class LogoutView(APIView):
    '''Представление для логаута.'''

    def post(self, request, *args, **kwargs):
        request.user.auth_token.delete()
        logout(request)
        return Response(
            status=status.HTTP_204_NO_CONTENT
        )
