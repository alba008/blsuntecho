from django.contrib.sitemaps import Sitemap
from django.urls import reverse

from .views import PROJECT_CASE_STUDIES


class StaticPageSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.7

    def items(self):
        return [
            "core:home",
            "core:services",
            "core:about",
            "core:projects",
            "core:contact",
        ]

    def location(self, item):
        return reverse(item)


class ProjectSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.6

    def items(self):
        return list(PROJECT_CASE_STUDIES.keys())

    def location(self, item):
        return reverse("core:project_detail", kwargs={"slug": item})


sitemaps = {
    "static": StaticPageSitemap,
    "projects": ProjectSitemap,
}
