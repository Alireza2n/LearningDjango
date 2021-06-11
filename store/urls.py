from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views

# Use a default router to generate urls for ViewSets
router = DefaultRouter()
router.register('orders', views.OrderViewSet)

app_name = 'store'
urlpatterns = [
    path('add-to-cart/<int:product_id>', views.add_to_cart, name='add-to-cart'),
    path('delete-from-cart/<int:product_id>', views.delete_row, name='delete-from-cart'),
    path('cart/', views.view_cart, name='view-cart'),
    path('deduct/', views.deduct_from_cart, name='deduct-from-cart'),
    path('api/v1/', include(router.urls)),
]
