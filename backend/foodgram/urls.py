from django.contrib import admin
from django.urls import include, path

from .yasg import urlpatterns as doc_urls

api_patterns = [
    path('', include('api.urls'))
]

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(api_patterns)),
    path('api/', include('rest_framework.urls'))
]

urlpatterns += doc_urls
