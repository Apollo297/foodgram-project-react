from django.db.models import Sum
from django_filters.rest_framework import DjangoFilterBackend
from django.http import (
    HttpResponse,
    Http404
)
from rest_framework import (
    status,
    viewsets
)
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

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
from shopping_cart.models import ShoppingCart


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    pagination_class = CustomResultsSetPagination
    permission_classes = (IsAuthorOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilter

    def get_serializer_class(self):
        if self.action in (
            'list',
            'retrieve'
        ):
            return AllRecipesSerializer
        return RecipeCreateSerializer

    def get_queryset(self):
       queryset = super().get_queryset()
       if self.action == 'favorite':
           queryset = RecipeFilter(
               self.request.GET,
               queryset=queryset,
               request=self.request
           ).qs
       return queryset

    @action(
        detail=True,
        methods=[
            'post',
            'delete'
        ],
        url_path='favorite',
        permission_classes=(IsAuthenticated,)
    )
    def favorite(self, request, **kwargs):
        if request.method == 'POST':
            try:
                recipe = self.get_object()
            except Http404:
                return Response(
                    {'errors': 'Рецепт не найден.'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            _, created = Favorite.objects.get_or_create(
                user=request.user,
                recipe=recipe
            )
            if created:
                serializer = SubscribingShoppingCartRecipeSerializer(
                    recipe,
                    context={'request': request}
                )
                return Response(
                    serializer.data,
                    status=status.HTTP_201_CREATED
                )
            return Response(
                {'errors': 'Рецепт уже добавлен в избранное.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        if request.method == 'DELETE':
            recipe = get_object_or_404(
                Recipe,
                pk=kwargs.get('pk')
            )
            favorite_instance = Favorite.objects.filter(
                user=request.user,
                recipe=recipe
            )
            if favorite_instance.exists():
                favorite_instance.delete()
                return Response(
                    status=status.HTTP_204_NO_CONTENT
                )
            return Response(
                {'errors': 'Рецепт не был добавлен в избранное.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        return Response(
            {'error': 'Метод запроса не поддерживается.'},
            status=status.HTTP_405_METHOD_NOT_ALLOWED
        )

    @action(
        detail=True,
        methods=[
            'post',
            'delete'
        ],
        permission_classes=[IsAuthenticated]
    )
    def shopping_cart(self, request, pk):
        recipe = Recipe.objects.filter(
            id=pk
        ).first()
        if not recipe and request.method == 'DELETE':
            return Response(
                {'errors': 'Рецепт не найден.'},
                status=status.HTTP_404_NOT_FOUND
            )
        if not recipe:
            return Response(
                {'errors': 'Рецепт не найден.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        if request.method == 'POST':
            _, created = ShoppingCart.objects.get_or_create(
                user=request.user,
                recipe=recipe
            )
            if created:
                serializer = SubscribingShoppingCartRecipeSerializer(recipe)
                return Response(
                    serializer.data,
                    status=status.HTTP_201_CREATED
                )
            return Response(
                {'errors': 'Рецепт уже добавлен в корзину покупок.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        cart_item = ShoppingCart.objects.filter(
            user=request.user,
            recipe=recipe
        ).first()
        if not cart_item:
            return Response(
                {'errors': 'Рецепт не был добавлен в корзину.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        cart_item.delete()
        return Response(
            status=status.HTTP_204_NO_CONTENT
        )

    @action(
        detail=False,
        methods=['get'],
        permission_classes=(IsAuthenticated,)
    )
    def download_shopping_cart(self, request, **kwargs):
        ingredients = (RecipeIngredient.objects.filter(
            recipe__shopping_recipe__user=request.user)
            .values('ingredient__name', 'ingredient__measurement_unit')
            .annotate(total_amount=Sum('amount'))
            .order_by('ingredient__name')
        )

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
