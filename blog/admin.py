from django.contrib import admin
from .models import BlogPost


@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at', 'is_published', 'views_count')
    list_filter = ('is_published', 'created_at')
    search_fields = ('title', 'content')
    readonly_fields = ('created_at', 'views_count')

    fieldsets = (
        ('Основная информация', {
            'fields': ('title', 'content', 'preview')
        }),
        ('Публикация', {
            'fields': ('is_published',)
        }),
        ('Статистика', {
            'fields': ('created_at', 'views_count'),
            'classes': ('collapse',)
        }),
    )