from rest_framework import pagination
from rest_framework.response import Response


class Pagination(pagination.PageNumberPagination):

    def get_paginated_response(self, data):
        return Response({
            'links': {
                'next': self.get_next_link(),
                'previous': self.get_previous_link()
            },
            'pagination': {
                'previous_page': self.page.number - 1 if self.page.number != 1 else None,
                'current_page': self.page.number,
                'next_page': self.page.number + 1 if self.page.has_next() else None,
                'page_size': self.page_size
            },
            'count': self.page.paginator.count,
            'total_pages': self.page.paginator.num_pages,
            'next': self.page.has_next(),
            'previous': self.page.has_previous(),
            'results': data
        })


class SimplePagination(pagination.PageNumberPagination): 

    def get_paginated_response(self, data):
        return Response({
            'records_filtered': self.page.paginator.count,
            'data': data
        })