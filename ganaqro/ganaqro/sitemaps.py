from django.conf import settings
from django.contrib.sitemaps import Sitemap
from django.urls import reverse

from projects.models import Blog


class GanaqroSitemap(Sitemap):
    protocol = 'https'

    def get_domain(self, site=None):
        domain = getattr(settings, 'SITE_DOMAIN', 'www.ganaqro.az')
        return domain.replace('https://', '').replace('http://', '').strip('/')


class StaticViewSitemap(GanaqroSitemap):
    def items(self):
        return [
            'projects:home-page',
            'projects:about-page',
            'projects:product-page',
            'projects:blog-page',
            'projects:faq-page',
            'projects:contact-page',
        ]

    def location(self, item):
        return reverse(item)

    def priority(self, item):
        priorities = {
            'projects:home-page': 1.0,
            'projects:product-page': 0.9,
            'projects:contact-page': 0.8,
            'projects:about-page': 0.8,
            'projects:blog-page': 0.8,
            'projects:faq-page': 0.6,
        }
        return priorities.get(item, 0.8)

    def changefreq(self, item):
        freqs = {
            'projects:home-page': 'daily',
            'projects:blog-page': 'weekly',
            'projects:contact-page': 'monthly',
        }
        return freqs.get(item, 'weekly')


class BlogSitemap(GanaqroSitemap):
    changefreq = 'weekly'
    priority = 0.7

    def items(self):
        return Blog.objects.all()

    def location(self, obj):
        return reverse('projects:blog-detail', kwargs={'blog_id': obj.pk})

    def lastmod(self, obj):
        return obj.created_at
