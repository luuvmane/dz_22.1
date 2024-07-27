from django.contrib import admin
from .models import Product, BlogPost

admin.site.register(Product)


@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at', 'published', 'views')
    search_fields = ('title', 'content')
    list_filter = ('created_at', 'published')
    prepopulated_fields = {'slug': ('title',)}
