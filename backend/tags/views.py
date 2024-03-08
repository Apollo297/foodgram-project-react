from rest_framework import viewsets

from tags.models import Tag
from tags.serializers import TagSerializer


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    '''Представление для просмотра тегов.'''

    queryset = Tag.objects.all()
    serializer_class = TagSerializer

    def get_queryset(self):
        queryset = Tag.objects.all()
        return queryset
