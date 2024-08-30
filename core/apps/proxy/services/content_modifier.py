import re
from functools import partial
from urllib.parse import urlparse, urlunparse

from core.apps.proxy.models import UserSite


class ContentModifierService:

    def __init__(self, new_schema: str, new_netloc: str, usersite: UserSite) -> None:
        self.new_schema = new_schema
        self.original_domain = urlparse(usersite.url).netloc
        self.original_scheme = urlparse(usersite.url).scheme
        self.new_netloc = new_netloc
        self.user_site_slug = usersite.slug

    def replace_link(self, match):
        original_link = match.group(1)
        parsed_url = urlparse(original_link)

        # Якщо посилання веде на оригінальний домен
        if not parsed_url.scheme and parsed_url.path or parsed_url.netloc == self.original_domain:
            # Змінюємо домен і додаємо user_site_slug до шляху
            new_path = f"/{self.user_site_slug}/{parsed_url.path.lstrip('/')}"

            # Формуємо новий URL
            new_url = urlunparse((
                self.new_schema, self.new_netloc,
                new_path,
                parsed_url.params, parsed_url.query, parsed_url.fragment
            ))
            
            return match.group(0).replace(match.group(1), new_url)
        # Посилання на зовнішній ресурс залишаємо без змін
        return match.group(0)

    def modify_links(self, content: str) -> str:
        # Регулярний вираз для пошуку всіх посилань
        # href= — шукає текст href=.
        # [\'"] — відповідність або одинарній, або подвійній лапці.
        # ([^\'"]+) — захоплює один чи більше символів, які не є лапками (ні одинарними, ні подвійними).
        # [\'"] — відповідність або одинарній, або подвійній лапці (закриваюча).
        relative_link_pattern = r'=[\'"](/[^\'"]+)[\'"]'
        full_path_pattern = r'[\'"](https?://([^\'" ]+))[\'"\s]'

        original_main_ulr = urlunparse((self.original_scheme, self.original_domain, '', '', '', ''))
        separate_full_path_pattern = fr'[^\'"]({original_main_ulr}([^\'"\s]+))[^\'"]'

        # Change all links in content.
        # As re.sub's function takes a single Match argument
        # use partial from functools for passsing self.
        partial_replace_link = partial(self.replace_link)

        for pattern in [full_path_pattern, relative_link_pattern, separate_full_path_pattern]:
            re.compile(pattern=pattern).sub(partial_replace_link, content)
        
        return content
