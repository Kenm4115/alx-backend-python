from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

class MessagePagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100

    # ✅ Override the paginated response to include page.paginator.count
    def get_paginated_response(self, data):
        return Response({
            'total_count': self.page.paginator.count,   # 👈 explicit count
            'total_pages': self.page.paginator.num_pages,  # optional extra
            'current_page': self.page.number,              # optional extra
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'results': data
        })
