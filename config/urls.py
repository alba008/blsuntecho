from django.contrib import admin
from django.views.generic import TemplateView
from django.urls import include, path
from django.contrib.sitemaps.views import sitemap
from core.sitemaps import sitemaps

urlpatterns = [
    path("admin/", admin.site.urls),
    path("robots.txt", TemplateView.as_view(template_name="robots.txt", content_type="text/plain"), name="robots"),
    path("sitemap.xml", sitemap, {"sitemaps": sitemaps}, name="sitemap"),
    path("", include("core.urls")),
]
