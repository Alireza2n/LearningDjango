from django.views.generic import ListView
from . import models


class ListProductView(ListView):
    """
    Shows a list of active products
    """
    queryset = models.Product.objects.filter(
        is_active=True
    )
