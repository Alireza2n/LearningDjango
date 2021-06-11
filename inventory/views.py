from django.views.generic import ListView
from rest_framework import generics

from . import models
from . import serializers


class ListProductView(ListView):
    """
    Shows a list of active products
    """
    queryset = models.Product.objects.filter(
        is_active=True
    )


"""
REST Views
"""


class ProductList(generics.ListAPIView):
    """
    Rest List view for product model
    """
    queryset = models.Product.objects.filter(is_active=True)
    serializer_class = serializers.ProductSerializer
