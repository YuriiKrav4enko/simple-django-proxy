import re
from urllib.parse import urlparse, urlunparse

from django.http import HttpRequest

from core.apps.proxy.models import UserSite


class ContentModifier:

    def modify_links(self, request: HttpRequest, usersite: UserSite, content: str) -> str:
        # Регулярний вираз для пошуку всіх посилань
        original_domain = urlparse(usersite.url).netloc
        href_pattern = re.compile(r'href="([^"]+)"')

        new_netloc = request.get_host()
        user_site_slug = usersite.slug

        def replace_link(match):
            original_link = match.group(1)
            parsed_url = urlparse(original_link)

            # Якщо посилання веде на оригінальний домен
            if parsed_url.netloc == original_domain:
                # Змінюємо домен і додаємо user_site_slug до шляху
                new_path = f"/{user_site_slug}{parsed_url.path}"

                # Формуємо новий URL
                new_url = urlunparse((
                    request.scheme,
                    new_netloc,
                    new_path,
                    parsed_url.params,
                    parsed_url.query,
                    parsed_url.fragment
                ))
                
                return f'href="{new_url}"'
            else:
                # Посилання на зовнішній ресурс залишаємо без змін
                return match.group(0)

        # Заміна всіх посилань у контенті
        modified_content = href_pattern.sub(replace_link, content)
        return modified_content
