from django.contrib import admin
from .models import Product, BlogPost, Category


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'views')
    search_fields = ('name', 'category__name')
    list_filter = ('is_published',)
    actions = ['make_published', 'make_unpublished']

    def make_published(self, request, queryset):
        queryset.update(is_published=True)

    make_published.short_description = "Опубликовать выбранные продукты"

    def make_unpublished(self, request, queryset):
        queryset.update(is_published=False)

    make_unpublished.short_description = "Снять с публикации выбранные продукты"


@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at', 'published', 'views')
    search_fields = ('title', 'content')
    list_filter = ('created_at', 'published')
    prepopulated_fields = {'slug': ('title',)}


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

