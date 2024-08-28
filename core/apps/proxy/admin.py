from django.contrib import admin
from django.utils.html import format_html

from core.apps.proxy.models import UserSite, SiteVisit


@admin.register(UserSite)
class UserSiteAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'slug', 'link')
    exclude = ['slug']
    
    @admin.display(
        description="Proxy link",
    )
    def link(self, obj):
        return format_html(f'<a href="http://localhost:8000/{obj.slug}/"> Visit {obj.title} </a> ')



@admin.register(SiteVisit)
class SiteVisitAdmin(admin.ModelAdmin):
    list_display = ('id', 'user_site__title', 'page_url', 'request_size', 'response_size')
    exclude = ['slug']
    
    @admin.display(
        description="Proxy link",
    )
    def link(self, obj):
        return format_html(f'<a href="http://localhost:8000/{obj.slug}/"> Visit {obj.title} </a> ')
