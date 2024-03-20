from rest_framework import viewsets
from rest_framework.permissions import AllowAny

from ingredients.models import Ingredient
from ingredients.serializers import IngredientSerializer


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    """Представление для просмотра ингредиентов."""

    queryset = Ingredient.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = IngredientSerializer
    pagination_class = None
    lookup_field = 'id'

    def get_queryset(self):
        query = self.request.query_params.get('name', '')
        return Ingredient.objects.filter(name__icontains=query)
