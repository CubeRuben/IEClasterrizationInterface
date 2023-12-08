from django.contrib import admin

from .models import Industry, Region

admin.site.register((Industry, Region))
