from rest_framework import viewsets
from rest_framework.permissions import AllowAny

from tags.models import Tag
from tags.serializers import TagSerializer


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    '''Представление для просмотра тегов.'''

    queryset = Tag.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = TagSerializer
    pagination_class = None

    def get_queryset(self):
        queryset = Tag.objects.all()
        return queryset
