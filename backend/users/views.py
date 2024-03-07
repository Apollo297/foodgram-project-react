from django.contrib.auth import (
    authenticate,
    get_user_model,
    login,
    logout
)
from django.contrib.auth.backends import ModelBackend
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import (
    permissions
)
from rest_framework.authtoken.models import Token
from rest_framework.decorators import action
from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated
)
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import (
    filters,
    pagination,
    status,
    viewsets
)

from subscriptions.models import Subscription
from subscriptions.serializers import (
    SubscribingSerializer,
    MySubscriptionsSerializer
)
from users.serializers import (
    ChangePasswordSerializer,
    TokenSerializer,
    UserRegistrationSerializer,
    UserSerializer,
)


User = get_user_model()


class CustomPaginator(pagination.PageNumberPagination):
    page_size_query_param = 'limit'


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    permission_classes = [AllowAny]
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
        elif self.action == 'subscriptions':
            return MySubscriptionsSerializer
        elif self.action == 'subscribe':
            if self.request.method in ['POST']:
                return SubscribingSerializer
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
        permission_classes=[IsAuthenticated]
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
        permission_classes=[IsAuthenticated]
    )
    def me(self, request):
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)

    @action(
        detail=False,
        methods=['get'],
        permission_classes=[IsAuthenticated],
        pagination_class=CustomPaginator
    )
    def subscriptions(self, request):
        queryset = User.objects.filter(
            subscribed_to__user=request.user
        )
        page = self.paginate_queryset(queryset)
        serializer = MySubscriptionsSerializer(
            page,
            many=True,
            context={'request': request}
        )
        return self.get_paginated_response(serializer.data)

    @action(
        detail=True,
        methods=['post', 'delete'],
        permission_classes=[IsAuthenticated]
    )
    def subscribe(self, request, **kwargs):
        author = get_object_or_404(
            User,
            id=kwargs['pk']
        )
        if request.method == 'POST':
            serializer = SubscribingSerializer(
                author,
                data=request.data,
                context={"request": request}
            )
            serializer.is_valid(raise_exception=True)
            Subscription.objects.create(
                user=request.user,
                author=author
            )
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )
        if request.method == 'DELETE':
            get_object_or_404(
                Subscription,
                user=request.user,
                author=author
            ).delete()
            return Response(
                {'detail': 'Отписка произведена'},
                status=status.HTTP_204_NO_CONTENT
            )


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
    '''Кастомный обработчик аутентификации.'''

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
