from rest_framework import serializers

from product.models import Product


class ProductSerializer(serializers.ModelSerializer):
    created_by = serializers.HiddenField(default=serializers.CurrentUserDefault())
    updated_by = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Product
        fields = ['name', 'price', 'created_by', 'updated_by']

