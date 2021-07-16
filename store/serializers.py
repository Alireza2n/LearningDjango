from rest_framework import serializers

from users.serializers import UserSerializer
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
            # 'orderitem_set'
        )
