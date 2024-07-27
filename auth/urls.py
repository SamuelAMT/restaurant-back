from django.urls import path, include

urlpatterns = [
    path('v1/', include('auth.v1.urls')),
]