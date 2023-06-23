from rest_framework import pagination


class BusListPagination(pagination.PageNumberPagination):
    page_size = 100
    page_size_query_param = 'page_size'


class AdminBusListPagination(pagination.PageNumberPagination):
    page_size = 30
    page_size_query_param = 'page_size'


class OperatorTripPagination(pagination.PageNumberPagination):
    page_size = 30
    page_size_query_param = 'page_size'

class LocationListPagination(pagination.PageNumberPagination):
    page_size = 30
    page_size_query_param = 'page_size'
