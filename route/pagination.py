from rest_framework import pagination


class RouteListPagination(pagination.PageNumberPagination):
    page_size = 100
    page_size_query_param = 'page_size'

class AdminRouteListPagination(pagination.PageNumberPagination):
    page_size = 30
    page_size_query_param = 'page_size'

