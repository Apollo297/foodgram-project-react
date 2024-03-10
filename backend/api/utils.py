from rest_framework.pagination import PageNumberPagination


class CustomResultsSetPagination(PageNumberPagination):
    page_size_query_param = 'limit'
    max_page_size = 50


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