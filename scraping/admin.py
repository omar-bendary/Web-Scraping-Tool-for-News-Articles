from django.contrib import admin
from .models import Article, Website, History


@admin.register(Website)
class WebsiteAdmin(admin.ModelAdmin):
    list_display = ['name', 'last_scraped_by', 'last_scraped_at']


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ['title', 'website', 'published_at']


@admin.register(History)
class Historydmin(admin.ModelAdmin):
    list_display = ['user', 'website', 'scraped_at']
