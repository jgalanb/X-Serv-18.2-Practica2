from django.db import models

# Create your models here.
class Url(models.Model):
    URL_original = models.CharField(max_length=64)
    URL_acortada = models.CharField(max_length=64)
