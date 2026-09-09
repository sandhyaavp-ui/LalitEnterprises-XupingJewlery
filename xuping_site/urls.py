from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.sitemaps.views import sitemap

from inquiries import admin_views
from pages.views import robots_txt
from .sitemaps import StaticViewSitemap, ProductSitemap, CollectionSitemap, BlogSitemap

sitemaps = {
    'static': StaticViewSitemap,
    'products': ProductSitemap,
    'collections': CollectionSitemap,
    'blogs': BlogSitemap,
}


urlpatterns = [
    # Must come before 'admin/' below: Django's path('admin/', admin.site.urls)
    # commits to admin.site.urls's own URLconf for anything under /admin/, so
    # an unmatched sub-path there 404s instead of falling through to app urls.
    path('admin/dashboard/', admin_views.dashboard, name='staff_dashboard'),
    path('admin/dashboard/booking/<int:booking_id>/status/', admin_views.update_booking_status, name='update_booking_status'),
    path('admin/dashboard/customer/<int:customer_id>/update/', admin_views.update_customer, name='update_customer'),
    path('admin/', admin.site.urls),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
    path('robots.txt', robots_txt, name='robots_txt'),
    path('', include('pages.urls')),
    path('', include('catalog.urls')),
    path('', include('inquiries.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])
