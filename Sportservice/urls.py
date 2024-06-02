from django.contrib import admin
from django.urls import path, include

from mainapp.views import NotFoundView

urlpatterns = [
    path('admin/', admin.site.urls, name='admin'),
    path('', include('mainapp.urls')),
    path('', include('authapp.urls')),
    path('', include('rentapp.urls')),
    path('not_found/', NotFoundView.as_view(), name='not_found')
]
