from django.contrib.sitemaps import Sitemap
from django.urls import reverse

from catalog.models import Product, Collection
from pages.models import BlogPost


class StaticViewSitemap(Sitemap):
    priority = 0.6
    changefreq = 'monthly'

    def items(self):
        return [
            'pages:home',
            'catalog:product_list',
            'pages:blogs',
            'inquiries:contact',
            'inquiries:video_call_booking',
        ]

    def location(self, item):
        return reverse(item)


class ProductSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.8

    def items(self):
        return Product.objects.all()

    def location(self, obj):
        return reverse('catalog:product_detail', args=[obj.slug])


class CollectionSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.7

    def items(self):
        return Collection.objects.all()

    def location(self, obj):
        return reverse('catalog:collection_detail', args=[obj.slug])


class BlogSitemap(Sitemap):
    changefreq = 'monthly'
    priority = 0.5

    def items(self):
        return BlogPost.objects.all()

    def location(self, obj):
        return reverse('pages:blog_detail', args=[obj.slug])
