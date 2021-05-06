from django.urls import path
from . import views

app_name = 'blog'
urlpatterns = [
    path('all/', views.show_all_posts, name='show-all-posts'),
    path('create/', views.create_post, name='create-post'),
]
