from django.urls import path
from . import views

app_name = 'inventory'
urlpatterns = [
    path('', views.ListProductView.as_view(), name='list')
]
