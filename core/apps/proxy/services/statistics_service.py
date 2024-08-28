from django.http import HttpRequest
from requests import Response
from core.apps.proxy.models import SiteVisit, UserSite


class StatisticsService:
    def create_log_visit(
            self,
            user_site: UserSite,
            original_url: str,
            request_size: int,
            response_size: int
        ) -> None:
        SiteVisit.objects.create(
            user_site=user_site,
            page_url=original_url,
            request_size=request_size,
            response_size=response_size
        )

    @staticmethod
    def calculate_request_size(request: HttpRequest):
        # Розмір метода (наприклад, "GET", "POST")
        method_size = len(request.method) if request.method is not None else 0

        # Розмір URL (наприклад, "/example/path/")
        url_size = len(request.get_full_path())

        # Розмір заголовків
        headers_size = sum(
            len(key) + len(value)
            for key, value in request.headers.items()
        )

        # Розмір тіла запиту (для POST, PUT, PATCH запитів)
        body_size = 0
        if request.method in ['POST', 'PUT', 'PATCH']:
            if request.content_type == 'multipart/form-data':
                # Розмір файлів у тілі запиту
                for file in request.FILES.values():
                    body_size += file.size
                # Розмір інших полів у тілі запиту
                body_size += sum(len(k) + len(v) for k, v in request.POST.items())
            else:
                # Розмір даних для інших типів вмісту, наприклад, application/json або application/x-www-form-urlencoded
                body_size = len(request.body)

        # Загальний розмір запиту
        total_size = method_size + url_size + headers_size + body_size
        return total_size

    @staticmethod
    def calculate_response_size(response: Response):
        status_code_size = len(str(response.status_code))
        headers_size = sum(len(key) + len(value) for key, value in response.headers.items())
        body_size = len(response.content)
        total_size = status_code_size + headers_size + body_size
        return total_size
