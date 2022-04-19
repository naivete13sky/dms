from django.contrib.sitemaps import Sitemap
from .models import Job


class JobSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.9

    def items(self):
        return Job.published.all()

    def lastmod(self, obj):
        return obj.updated