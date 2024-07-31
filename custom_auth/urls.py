from django.urls import path, include

urlpatterns = [
    path('v1/', include('custom_auth.v1.urls')),
]
