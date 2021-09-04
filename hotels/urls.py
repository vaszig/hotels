import debug_toolbar
from django.contrib import admin
from django.urls import path, include

from app.views import list_hotels, search_hotels
from managers.admin import manager_site


urlpatterns = [
    path('__debug__/', include(debug_toolbar.urls)),
    path('admin/', admin.site.urls),
    path('', list_hotels, name='list_hotels'),
    path('managers/', manager_site.urls),
    path('api/search/', search_hotels, name='search_hotels'),
]
