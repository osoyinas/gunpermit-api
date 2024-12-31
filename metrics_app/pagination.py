from rest_framework.pagination import PageNumberPagination

MAX_SIZE = 2000
DEFAULT_SIZE = 10

class CustomPagination(PageNumberPagination):
    page_size = DEFAULT_SIZE

    def get_page_size(self, request):
        size = request.query_params.get('size', None)
        if size is not None and size.isdigit():
            size = int(size)
            if size < MAX_SIZE:
                return size
        return self.page_size
