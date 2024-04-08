from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


DEFAULT_CURRENT_PAGE = 1
DEFAULT_PAGE_SIZE = 10


class CustomPagination(PageNumberPagination):
    current_page = DEFAULT_CURRENT_PAGE
    page_size = DEFAULT_PAGE_SIZE
    page_size_query_param = "page_size"

    def get_paginated_response(self, data):
        page_size = int(
            self.request.GET.get(self.page_size_query_param, self.page_size)
        )
        if page_size == -1:
            page_size = self.page.paginator.count
        return Response(
            {
                "links": {
                    "next": self.get_next_link(),
                    "previous": self.get_previous_link(),
                },
                "records_count": self.page.paginator.count,
                "pages_count": self.page.paginator.num_pages,
                "page": int(self.request.GET.get("page", self.current_page)),
                "page_size": page_size,
                "results": data,
            }
        )
