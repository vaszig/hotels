import debug_toolbar
from django.contrib import admin
from django.urls import path, include

from app.views import list_hotels, search_hotels


urlpatterns = [
    path('__debug__/', include(debug_toolbar.urls)),
    path('admin/', admin.site.urls),
    path('', list_hotels, name='list_hotels'),
    path('api/search/', search_hotels, name='search_hotels'),
]
