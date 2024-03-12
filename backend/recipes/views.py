from django.db.models import Sum
from django_filters.rest_framework import DjangoFilterBackend
from django.http import HttpResponse
from rest_framework import (
    status,
    viewsets
)
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from api.filters import RecipeFilter
from api.permissions import IsAuthorOrReadOnly
from api.utils import CustomResultsSetPagination
from favourites.models import Favorite
from recipes.models import (
    Recipe,
    RecipeIngredient
)
from recipes.serializers import (
    AllRecipesSerializer,
    RecipeCreateSerializer,
    SubscribingShoppingCartRecipeSerializer
)
from shopping_cart.models import Shopping_cart


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    pagination_class = CustomResultsSetPagination
    permission_classes = (IsAuthorOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilter
    http_method_names = [
        'get',
        'post',
        'patch',
        'delete'
    ]

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return AllRecipesSerializer
        return RecipeCreateSerializer

    @action(
        detail=True,
        methods=['post'],
        permission_classes=(IsAuthenticated,)
    )
    def add_to_favorite(self, request, **kwargs):
        recipe = self.get_object()
        if request.method == 'POST':
            serializer = SubscribingShoppingCartRecipeSerializer(
                recipe,
                context={'request': request}
            )
            serializer.is_valid(raise_exception=True)
        _, created = Favorite.objects.get_or_create(
            user=request.user,
            recipe=recipe
        )
        if created:
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )
        return Response(
            {'errors': 'Рецепт уже добавлен в избранное.'},
            status=status.HTTP_400_BAD_REQUEST
        )

    @action(
        detail=True,
        methods=['delete'],
        permission_classes=(IsAuthenticated,)
    )
    def remove_from_favorite(self, request, **kwargs):
        recipe = self.get_object()
        removed = Favorite.objects.filter(
            user=request.user,
            recipe=recipe
        ).delete()
        if removed:
            return Response(
                {'detail': 'Рецепт успешно удален из избранного.'},
                status=status.HTTP_204_NO_CONTENT
            )
        return Response(
            {'errors': 'Рецепт не найден в избранном.'},
            status=status.HTTP_400_BAD_REQUEST
        )

    @action(
        detail=True,
        methods=['post'],
        permission_classes=(IsAuthenticated,)
    )
    def add_to_shopping_cart(self, request, **kwargs):
        recipe = self.get_object()
        serializer = SubscribingShoppingCartRecipeSerializer(
            recipe,
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        _, created = Shopping_cart.objects.get_or_create(
            user=request.user,
            recipe=recipe
        )
        if created:
            return Response(
                {'detail': 'Рецепт успешно добавлен в список покупок.'},
                status=status.HTTP_201_CREATED
            )
        return Response(
            {'errors': 'Ошибка добавления в список покупок.'},
            status=status.HTTP_400_BAD_REQUEST
        )

    @action(
        detail=True,
        methods=['delete'],
        permission_classes=(IsAuthenticated,)
    )
    def remove_from_shopping_cart(self, request, **kwargs):
        recipe = self.get_object()
        removed = Shopping_cart.objects.filter(
            user=request.user,
            recipe=recipe
        ).delete()
        if removed:
            return Response(
                {'detail': 'Рецепт успешно удален из списка покупок.'},
                status=status.HTTP_204_NO_CONTENT
            )
        return Response(
            {'errors': 'Ошибка удаления из списка покупок.'},
            status=status.HTTP_400_BAD_REQUEST
        )

    @action(
        detail=False,
        methods=['get'],
        permission_classes=(IsAuthenticated,)
    )
    def download_shopping_cart(self, request, **kwargs):
        ingredients = RecipeIngredient.objects\
            .filter(recipe__shopping_recipe__user=request.user)\
            .values('ingredient__name', 'ingredient__measurement_unit')\
            .annotate(total_amount=Sum('amount'))\
            .order_by('ingredient__name')

        file_list = [
            '{} - {} {}.'.format(
                ingredient['ingredient__name'],
                ingredient['total_amount'],
                ingredient['ingredient__measurement_unit']
            ) for ingredient in ingredients
        ]
        file_content = 'Список покупок:\n' + '\n'.join(file_list)
        response = HttpResponse(
            file_content,
            content_type='text/plain'
        )
        response[
            'Content-Disposition'
        ] = 'attachment; filename="shopping_list.txt"'
        return response
