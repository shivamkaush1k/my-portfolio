from django.contrib import admin
from django.utils.html import format_html
from .models import Blog, Category  # Same app only!

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "color_preview")
    prepopulated_fields = {"slug": ("name",)}
    
    def color_preview(self, obj):
        return format_html(
            f'<span style="display:inline-block;width:20px;height:20px;background:{obj.color};border-radius:50%;"></span>'
        )

@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ("title", "get_author", "category", "created_at", "is_published")
    list_filter = ("category", "is_published", "created_at")
    search_fields = ("title", "content")
    prepopulated_fields = {"slug": ("title",)}
    list_editable = ("is_published",)
    readonly_fields = ("created_at", "updated_at")
    
    def get_author(self, obj):
        return obj.author.username if obj.author else "No author"
