from rest_framework import viewsets
from .models import Restaurant
from .serializers import RestaurantSerializer
from rest_framework.permissions import IsAuthenticated


class RestaurantViewSet(viewsets.ModelViewSet):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer
    permission_classes = [IsAuthenticated]
