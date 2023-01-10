from rest_framework.pagination import PageNumberPagination


class AdvertisementPagination(PageNumberPagination):
    page_size = 20
    page_query_param = 'p'
    # max_page_size = 100