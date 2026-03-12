from django.db import models

class Site(models.Model):

    site_name = models.CharField(max_length=100)

    subdomain = models.CharField(max_length=100, unique=True)

    storage_path = models.CharField(max_length=200)

    created_at = models.DateTimeField(auto_now_add=True)