from django.contrib import admin
from django.urls import include, path, re_path
import debug_toolbar

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
    path('__debug__/', include(debug_toolbar.urls)),
    path('accounts/', include('allauth.urls')),
    re_path(r'^(?P<restaurant_name>[a-zA-Z0-9-_]+)/', include('restaurant.urls')),
]
