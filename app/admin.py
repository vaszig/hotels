from django.contrib import admin

from .models import City, Hotel


admin.site.register([City, Hotel])