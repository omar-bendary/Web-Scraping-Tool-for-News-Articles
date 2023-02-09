from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import Website, Article, History


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ['username']


class WebsiteSerializer(serializers.ModelSerializer):
    last_scraped_by = UserSerializer()
    last_scraped_at = serializers.SerializerMethodField()
    created_at=serializers.SerializerMethodField()

    def get_last_scraped_at(self, obj):
        return obj.last_scraped_at.strftime('%B %d, %Y - (%I:%M) %p')
    def get_created_at(self, obj):
        return obj.last_scraped_at.strftime('%B %d, %Y - (%I:%M) %p')

    class Meta:
        model = Website
        fields = ['id','name', 'link', 'created_at',
                  'last_scraped_at', 'last_scraped_by']


class SimpleWebsiteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Website
        fields = ['name', 'link']


class ArticleSerializer(serializers.ModelSerializer):
    website = SimpleWebsiteSerializer()
    published_at = serializers.SerializerMethodField()

    def get_published_at(self, obj):
        # some articles have no published_at date
        try:
            return obj.published_at.strftime('%B %d, %Y')
        except:
            return obj.published_at
    class Meta:
        model = Article
        fields = ['title', 'description', 'DOM',
                  'published_at', 'link', 'website']


class HistorySerializer(serializers.ModelSerializer):
    user = UserSerializer()
    scraped_at = serializers.SerializerMethodField()

    def get_scraped_at(self, obj):
        return obj.scraped_at.strftime('%B %d, %Y - (%I:%M) %p')

    class Meta:
        model = History
        fields = ['scraped_at','user' ]

class ScrapingHistorySerializer(serializers.ModelSerializer):
    scrape_history = HistorySerializer(many=True)

    class Meta:
        model = Website
        fields = ['name','scrape_history' ]
