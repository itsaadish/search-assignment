# backend/core/models.py
from django.db import models
from django.contrib.auth.models import User

class SearchQuery(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    raw_query = models.TextField()
    parsed_query = models.JSONField()
    status = models.CharField(max_length=20, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

class ProductResult(models.Model):
    search = models.ForeignKey(SearchQuery, on_delete=models.CASCADE, null=True, blank=True)
    website = models.CharField(max_length=100, null=True, blank=True)
    title = models.CharField(max_length=255, null=True, blank=True)
    price = models.CharField(max_length=50, null=True, blank=True)  # Changed to CharField
    image_url = models.URLField(null=True, blank=True)
    product_url = models.URLField(null=True, blank=True)
    size = models.CharField(max_length=50, null=True, blank=True)
    material = models.CharField(max_length=100, null=True, blank=True)
    gender = models.CharField(max_length=50, null=True, blank=True)
    scraped_at = models.DateTimeField(auto_now_add=True)