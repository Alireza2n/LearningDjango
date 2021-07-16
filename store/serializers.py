from rest_framework import serializers

from . import models


class OrderSerializer(serializers.HyperlinkedModelSerializer):
    """
    Serializer for store.Order
    """

    class Meta:
        model = models.Order
        fields = (
            'pk',
            'owner',
            'status',
            'orderitem_set'
        )


class OrderItemSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.OrderItem
        fields = (
            'pk',
            'product',
            'qty',
            'discount',
            'price',
        )
