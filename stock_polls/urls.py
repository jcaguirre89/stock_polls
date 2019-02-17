
from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView

from users.views import Index

urlpatterns = [
    path('', RedirectView.as_view(pattern_name='login')),
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('polls/', include('polls.urls')),
    path('users/', include('users.urls')),
]
