from django.urls import path, include

app_name = 'custom_auth'

urlpatterns = [
    path('v1/', include('custom_auth.v1.urls')),
]
