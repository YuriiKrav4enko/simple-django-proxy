from functools import partial
import re
from urllib.parse import urlparse, urlunparse

from django.http import HttpRequest

from core.apps.proxy.models import UserSite


class ContentModifierService:

    def __init__(self, request: HttpRequest, usersite: UserSite) -> None:
        self.request = request
        self.usersite = usersite
        self.original_domain = urlparse(usersite.url).netloc
        self.new_netloc = request.get_host()
        self.user_site_slug = usersite.slug

    def replace_link(self, match):
        original_link = match.group(1)
        parsed_url = urlparse(original_link)

        # Якщо посилання веде на оригінальний домен
        if parsed_url.netloc == self.original_domain:
            # Змінюємо домен і додаємо user_site_slug до шляху
            new_path = f"/{self.user_site_slug}{parsed_url.path}"

            # Формуємо новий URL
            new_url = urlunparse((
                self.request.scheme,
                self.new_netloc,
                new_path,
                parsed_url.params,
                parsed_url.query,
                parsed_url.fragment
            ))
            
            return f'href="{new_url}"'
        else:
            # Посилання на зовнішній ресурс залишаємо без змін
            return match.group(0)

    def modify_links(self, content: str) -> str:
        # Регулярний вираз для пошуку всіх посилань
        href_pattern = re.compile(r'href="([^"]+)"')

        # Change all links in content.
        # As re.sub's function takes a single Match argument
        # use partial from functools for passsing self.
        partial_replace_link = partial(self.replace_link)
        modified_content = href_pattern.sub(partial_replace_link, content)
        return modified_content
