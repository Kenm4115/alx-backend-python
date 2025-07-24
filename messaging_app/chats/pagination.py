from rest_framework.pagination import PageNumberPagination

class MessagePagination(PageNumberPagination):
    # Number of messages per page
    page_size = 20
    # Allow clients to override with ?page_size=<number>
    page_size_query_param = 'page_size'
    # Maximum allowed page size
    max_page_size = 100
