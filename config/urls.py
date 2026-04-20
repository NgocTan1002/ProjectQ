from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),
    path("",         include("apps.core.urls",      namespace="core")),
    path("products/", include("apps.products.urls", namespace="products")),
    path("solutions/", include("apps.solutions.urls", namespace="solutions")),
#     path("cart/",    include("apps.cart.urls",      namespace="cart")),
#     path("orders/",  include("apps.orders.urls",    namespace="orders")),
#     path("contact/", include("apps.contacts.urls",  namespace="contacts")),
#     path("blog/",    include("apps.blog.urls",      namespace="blog")),
#     path("customers/", include("apps.customers.urls", namespace="customers")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)