from rest_framework import serializers

from . import models


class ProductSerializer(serializers.ModelSerializer):
    """
    Serializer class form inventory.Product
    """

    class Meta:
        model = models.Product
        fields = (
            'name',
            'description',
            'price'
        )
