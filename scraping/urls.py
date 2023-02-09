from django.urls import path
from .views import WebsiteList, ReScrape, ArticleList, ScrapingHistoryList

urlpatterns = [
    path('websites/', WebsiteList.as_view()),
    path('re-scrape/<int:pk>/', ReScrape.as_view()),
    path('articles/', ArticleList.as_view()),
    path('scraping_history/', ScrapingHistoryList.as_view()),



]
