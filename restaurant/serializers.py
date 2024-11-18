# restaurant/serializers.py

from rest_framework import serializers
from .models import Restaurant
from .models import Address
from address.serializers import AddressSerializer

class RestaurantSerializer(serializers.ModelSerializer):
    addresses = AddressSerializer(many=True)

    class Meta:
        model = Restaurant
        fields = [
            'restaurant_id',
            'cnpj',
            'name',
            'country_code',
            'phone',
            'email',
            'email_verified',
            'image',
            'website',
            'description',
            'role',
            'created_at',
            'updated_at',
            'admin',
            'customers',
            'employees',
            'login_logs',
            'addresses',
        ]

    def create(self, validated_data):
        addresses_data = validated_data.pop('addresses')
        restaurant = Restaurant.objects.create(**validated_data)
        for address_data in addresses_data:
            Address.objects.create(restaurant=restaurant, **address_data)
        return restaurant

    def update(self, instance, validated_data):
        addresses_data = validated_data.pop('addresses', None)
        
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        if addresses_data is not None:
            instance.addresses.all().delete()
            for address_data in addresses_data:
                Address.objects.create(restaurant=instance, **address_data)
        
        return instance