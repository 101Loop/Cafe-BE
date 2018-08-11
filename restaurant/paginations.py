from rest_framework.pagination import PageNumberPagination


class CustomPageSizePagination(PageNumberPagination):
    """
    A custom pagination class to set the page size.
    """
    page_size_query_param = 'pagesize'
