from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class CustomResultsSetPagination(PageNumberPagination):
    page_query_param = 'page'
    page_size_query_param = 'limit'
    max_page_size = 50

    def get_paginated_response(self, data):
        return Response({
            'count': self.page.paginator.count,
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'results': data
        })


def my_max_length(data):
    '''
    Функция вычисляет количество символов в
    самом длинном слове.
    '''
    mylist = [i for i, _ in data]
    return (
        max(
            [len(i) for i in mylist]
        )
    )
