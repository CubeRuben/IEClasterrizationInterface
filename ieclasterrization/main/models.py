from django.db import models

class Region(models.Model):
    name = models.CharField(max_length=256)

    def __str__(self):
        return self.name

class Industry(models.Model):
    name = models.CharField(max_length=256)

    def __str__(self):
        return self.name
 