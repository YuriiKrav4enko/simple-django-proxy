import httpx
import requests
from django.http import HttpRequest

EXCLUDED_HEADERS = set([
    'connection', 'keep-alive', 'proxy-authenticate',
    'proxy-authorization', 'te', 'trailers', 'transfer-encoding',
    'upgrade',
    'content-encoding',

    'host', 'content-length', 'content-type', 'cookie',
])


class ProxyService:
    def __init__(self, http_client=None):
        self.http_client = http_client or httpx.Client()

    def fetch_proxied_response(
            self, request: HttpRequest, original_url: str, headers: dict,
            **kwargs
        ):
        if request.method is None:
            raise AttributeError  # TODO change for custom error
        return requests.request(
            method=request.method,
            url=original_url,
            headers=headers, **kwargs)

    def build_headers(self, request: HttpRequest):
        headers = {
            key: value for key, value in request.headers.items()
            if key.lower() not in EXCLUDED_HEADERS
        }
        return headers
    
    @staticmethod
    def build_original_url(user_site, route: str):
        # FIXME improve
        original_url = f"{user_site.url}/{route}"
        return original_url
