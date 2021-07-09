from rest_framework import serializers

from . import models


class OrderSerializer(serializers.ModelSerializer):
    """
    Serializer for store.Order
    """

    class Meta:
        model = models.Order
        fields = (
            'pk',
            'owner',
            'status'
        )
