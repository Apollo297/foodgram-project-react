from rest_framework import (
    filters,
    viewsets
)
from rest_framework.permissions import AllowAny

from ingredients.models import Ingredient
from ingredients.serializers import IngredientRecipeSerializer


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    '''Представление для просмотра ингредиентов.'''

    queryset = Ingredient.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = IngredientRecipeSerializer
    pagination_class = None
    filter_backends = (filters.SearchFilter, )
    search_fields = ('^name', )
