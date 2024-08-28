from urllib.parse import urlparse

from core.apps.proxy.models import UserSite


class UserSiteService:
    
    @staticmethod
    def get_domain_from_url(url: str) -> str:
        return urlparse(url).netloc