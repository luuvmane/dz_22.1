from django.urls import path
from .views import (
    ProductCreateView, ProductUpdateView, ProductDeleteView, ProductDetailView,
    ProductListView, VersionCreateView, VersionUpdateView, VersionDetailView,
    BlogPostListView, BlogPostDetailView, BlogPostCreateView, BlogPostUpdateView,
    BlogPostDeleteView, CategoryListView
)
from django.conf import settings
from django.conf.urls.static import static
from django.views.decorators.cache import cache_page

urlpatterns = [

    path('', ProductListView.as_view(), name='product_list'),


    path('product/<int:pk>/', cache_page(60 * 60)(ProductDetailView.as_view()), name='product_detail'),


    path('product/create/', ProductCreateView.as_view(), name='product_create'),
    path('product/<int:pk>/edit/', ProductUpdateView.as_view(), name='product_edit'),
    path('product/<int:pk>/delete/', ProductDeleteView.as_view(), name='product_delete'),


    path('version/create/<int:product_id>/', VersionCreateView.as_view(), name='version_create'),
    path('version/<int:pk>/edit/', VersionUpdateView.as_view(), name='version_edit'),
    path('version/<int:pk>/', VersionDetailView.as_view(), name='version_detail'),

    path('categories/', CategoryListView.as_view(), name='category_list'),

    path('posts/', BlogPostListView.as_view(), name='blogpost_list'),
    path('post/create/', BlogPostCreateView.as_view(), name='blogpost_create'),
    path('post/<int:pk>/', BlogPostDetailView.as_view(), name='blogpost_detail'),
    path('post/<int:pk>/edit/', BlogPostUpdateView.as_view(), name='blogpost_edit'),
    path('post/<int:pk>/delete/', BlogPostDeleteView.as_view(), name='blogpost_delete'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
