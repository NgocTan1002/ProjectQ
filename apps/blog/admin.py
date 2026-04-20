from django.contrib import admin
from .models import BlogCategory, Post

@admin.register(BlogCategory)
class BlogCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'is_active']
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'post_type', 'category', 'author', 'status', 'is_featured', 'view_count', 'published_at']
    list_filter = ['status', 'post_type', 'category']
    search_fields = ['title', 'short_description']
    prepopulated_fields = {'slug': ('title',)}
    list_editable = ['status', 'is_featured']
    date_hierarchy = 'published_at'
 
    fieldsets = [
        (None, {'fields': ['title', 'slug', 'post_type', 'category', 'author']}),
        ('Media', {'fields': ['thumbnail']}),
        ('Content', {'fields': ['short_description', 'content', 'read_time', 'tags'], 'classes': ['wide']}),
        ('Relations', {'fields': ['related_products', 'related_solutions']}),
        ('SEO', {'fields': ['meta_title', 'meta_description'], 'classes': ['collapse']}),
        ('Publishing', {'fields': ['status', 'published_at', 'is_featured', 'sort_order']}),
    ]