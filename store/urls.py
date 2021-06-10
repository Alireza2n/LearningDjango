from django.urls import path

from . import views

app_name = 'store'
urlpatterns = [
    path('add-to-cart/<int:product_id>', views.add_to_cart, name='add-to-cart'),
    path('cart/', views.view_cart, name='view-cart'),
]
