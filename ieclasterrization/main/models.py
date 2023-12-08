from django.db import models

class Region(models.Model):
    name = models.CharField(max_length=256)

class Industry(models.Model):
    name = models.CharField(max_length=256)
