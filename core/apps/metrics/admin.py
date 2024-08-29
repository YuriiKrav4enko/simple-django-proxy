from urllib.parse import urlencode
from django.contrib import admin
from django.urls import reverse_lazy
from django.utils.html import format_html

from core.apps.metrics.models import UserMetrics


@admin.register(UserMetrics)
# class UserMetricsAdmin(ExportMixin, admin.ModelAdmin):
class UserMetricsAdmin(admin.ModelAdmin):
    model = UserMetrics
    list_display = (
        # 'user_email', 'date_joined', 'last_login', 'verified', 'is_approved', 'account_type', 'active'
        'user_email', 'date_joined', 'last_login',
        'total_usersite_count', 'total_sitevisit_count',
        'total_size_bytes'
    )
    list_display_links = None
    ordering = ['-date_joined']
    actions = None
    date_hierarchy = 'date_joined'
    group_by_date_field = 'date_joined'

    def has_add_permission(self, request, obj=None):
        return False

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related('usersite_set', 'usersite_set__sitevisit_set')

    def user_email(self, obj):
        url = reverse_lazy('admin:users_user_changelist')
        query = urlencode({'q': obj.email})
        return format_html('<a target="_blank" href="{}?{}">{}</a>', url, query, obj.email)
    user_email.short_description = 'Email'

    def total_usersite_count(self, obj):
        return len(obj.usersite_set.all())

    def total_sitevisit_count(self, obj):
        sitevisit_count = 0
        for usersite in obj.usersite_set.all():
            sitevisit_count += len(usersite.sitevisit_set.all())

        return sitevisit_count

    def total_size_bytes(self, obj):
        size = 0
        for usersite in obj.usersite_set.all():
            for sitevisit in usersite.sitevisit_set.all():
                size += sitevisit.request_size + sitevisit.response_size

        return size
