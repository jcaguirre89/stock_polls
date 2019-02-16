
from django.contrib import admin
from django.urls import path, include

from users.views import Index

urlpatterns = [
    path('', Index.as_view(), name='index'),
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('polls/', include('polls.urls')),
    path('users/', include('users.urls')),
]
