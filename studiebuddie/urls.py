from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    # Point the root URL to the API urls
    path('api/', include('base.api.urls')),
]