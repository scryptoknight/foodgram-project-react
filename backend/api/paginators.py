from rest_framework.pagination import PageNumberPagination


class PageNumberPaginatorModified(PageNumberPagination):
    page_size_query_param = 'limit'


class PageNumberPaginatorModified2(PageNumberPagination):
    page_size = 100
