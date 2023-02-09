from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Website(models.Model):
    name = models.CharField(max_length=255, unique=True)
    link = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now=True)
    last_scraped_at = models.DateTimeField(auto_now_add=True)
    last_scraped_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='websites')

    def __str__(self):
        return self.name


class Article(models.Model):
    title = models.TextField()
    description = models.TextField()
    DOM = models.TextField()
    published_at = models.DateTimeField(null=True, blank=True)
    link = models.CharField(max_length=255, unique=True)
    website = models.ForeignKey(
        Website, on_delete=models.CASCADE, related_name='articles')

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-published_at']


class History(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='scrape_history')
    website = models.ForeignKey(
        Website, on_delete=models.CASCADE, related_name='scrape_history')
    scraped_at = models.DateTimeField(auto_now=True)
