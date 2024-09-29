from rest_framework import pagination


class CustomPaginator(pagination.PageNumberPagination):
    """ Пагинация для вывода уроков и курсов. """
    page_size = 10
    page_query_param = 'page_size'
    max_page_size = 100
