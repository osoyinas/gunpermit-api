from rest_framework.pagination import PageNumberPagination


class CustomPagination(PageNumberPagination):
    page_size = 10

    def get_page_size(self, request):
        size = request.query_params.get('size', None)
        if size is not None and size.isdigit():
            size = int(size)
            if size < 10:
                return size
        return self.page_size
