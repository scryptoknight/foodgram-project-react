from rest_framework.pagination import PageNumberPagination


class PageNumberPaginatorModified(PageNumberPagination):
    page_size_query_param = 'limit'


class PageLimitSetPagination(PageNumberPagination):
    page_size = 6
    page_size_query_param = 'limit'
