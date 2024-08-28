from django.urls import re_path

from core.apps.proxy.views import ProxyView

urlpatterns = [
    re_path(r'^(?P<user_site_slug>[^/]+)/(?P<route>.*)?$', ProxyView.as_view(), name='proxy_view'),
]
