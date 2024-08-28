from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404
from django.views import View

from core.apps.proxy.models import UserSite
from core.apps.proxy.services.content_modifier import ContentModifier
from core.apps.proxy.services.proxy_service import ProxyService
from core.apps.proxy.services.statistics_service import StatisticsService


class ProxyView(View):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.proxy_service = ProxyService()
        self.statistics_service = StatisticsService()
        self.content_modifier = ContentModifier()

    def get(self, request: HttpRequest, user_site_slug: str, route: str, *args, **kwargs):
        return self.handle_request(request, user_site_slug, route)

    def post(self, request: HttpRequest, user_site_slug: str, route: str, *args, **kwargs):
        return self.handle_request(request, user_site_slug, route)

    def handle_request(self, request: HttpRequest, user_site_slug: str, route: str, *args, **kwargs):
        # Знаходимо відповідний UserSite за ім'ям користувача та слагом
        user_site = get_object_or_404(UserSite, user=request.user, slug=user_site_slug)

        # Відновлюємо повний URL для оригінального запиту
        original_url = ProxyService.build_original_url(user_site=user_site, route=route)

        # Обчислюємо розмір запиту
        request_size = StatisticsService.calculate_request_size(request=request)

        # Виконуємо запит до оригінального сайту через проксі-сервіс
        headers = self.proxy_service.build_headers(request)
        proxied_response = self.proxy_service.fetch_proxied_response(
            request=request,
            original_url=original_url,
            headers=headers
        )

        response_size = StatisticsService.calculate_response_size(response=proxied_response)
        # Логування статистики з врахуванням об'єму запиту
        self.statistics_service.create_log_visit(
            user_site=user_site,
            original_url=original_url,
            request_size=request_size,
            response_size=response_size
        )

        # Модифікуємо контент перед відправкою клієнту
        modified_content = self.content_modifier.modify_links(
            request=request,
            usersite=user_site,
            content=proxied_response.text
        )
        return HttpResponse(modified_content, content_type=proxied_response.headers['Content-Type'])
