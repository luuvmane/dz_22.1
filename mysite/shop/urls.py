from django.urls import path
from .views import (
    ProductCreateView, ProductUpdateView, ProductDeleteView, ProductDetailView,
    ProductListView, VersionCreateView, VersionUpdateView, VersionDetailView
)
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', ProductListView.as_view(), name='product_list'),
    path('product/<int:pk>/', ProductDetailView.as_view(), name='product-detail'),
    path('product/create/', ProductCreateView.as_view(), name='product_create'),
    path('product/<int:pk>/edit/', ProductUpdateView.as_view(), name='product_edit'),
    path('product/<int:pk>/delete/', ProductDeleteView.as_view(), name='product_delete'),
    path('version/create/<int:product_id>/', VersionCreateView.as_view(), name='version-create'),
    path('version/<int:pk>/edit/', VersionUpdateView.as_view(), name='version_edit'),
    path('version/<int:pk>/', VersionDetailView.as_view(), name='version_detail'),
    path('products/', ProductListView.as_view(), name='product-list'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
