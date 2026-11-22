from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from store.views import (
    ProductListView,
    ProductDetailView,
    LuxurySpecialView,
    WishlistView,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/products/', ProductListView.as_view(), name='product-list'),
    path('api/products/<slug:slug>/', ProductDetailView.as_view(), name='product-detail'),
    path('api/luxury-special/', LuxurySpecialView.as_view(), name='luxury-special'),
    path('api/me/wishlist/', WishlistView.as_view(), name='wishlist'),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [
        path('__debug__/', include(debug_toolbar.urls)),
    ]