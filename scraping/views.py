from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import Website, Article, History
from .serializers import WebsiteSerializer, ArticleSerializer, ScrapingHistorySerializer
from .webscraping_tool.stack.spiders.maklat_articles import maklatArticles_scrape
from .webscraping_tool.stack.spiders.arab_media_society_articles import arab_media_society_scrape
from datetime import datetime
import json




class WebsiteList(ListAPIView):
    queryset = Website.objects.all()
    serializer_class = WebsiteSerializer


class ReScrape(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        website = Website.objects.get(id=pk)
        user = request.user

        def update_data(dataset_name):
            with open(dataset_name, "r") as dataset:
                data = json.load(dataset)

            for element in data:
                try:
                    article = Article()
                    article.title = element['article_title']
                    article.description = element['article_description']
                    article.DOM = element['article_DOM']

                    # some articles have no published_at date
                    try:
                        article.published_at = datetime.strptime(
                            element['article_published_at'], '%B %d, %Y').date()
                    except:
                        published_at = element['article_published_at']

                    article.link = element['article_link']
                    article.website = website
                    article.save()
                except:
                    pass

        def scrape_by_at():
            website.last_scraped_by = user
            website.last_scraped_at = datetime.utcnow()
            website.save()

        def log_scrape():
            History.objects.create(user=user, website=website)

        if website.name == "موقع مقالات Mklat.com":
            try:
                maklatArticles_scrape()
                update_data('scraped_datasets/maklat_articles_data.json')
                log_scrape()
                scrape_by_at()

                return Response({"success": True}, status=status.HTTP_202_ACCEPTED)
            except:
                return Response({"success": False})

        elif website.name == "Arab Media & Society":
            try:
                arab_media_society_scrape()
                update_data(
                    'scraped_datasets/arab_media_society_articles_data.json')
                log_scrape()
                scrape_by_at()
                return Response({"success": True}, status=status.HTTP_202_ACCEPTED)
            except:
                return  Response({"success": False})

        return  Response({"status": False})


class ArticleList(ListAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer


class ScrapingHistoryList(ListAPIView):
    queryset = Website.objects.all()
    serializer_class = ScrapingHistorySerializer
