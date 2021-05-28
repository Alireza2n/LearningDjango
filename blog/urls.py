from django.urls import path
from . import views

app_name = 'blog'
urlpatterns = [
    path('all/', views.show_all_posts, name='show-all-posts'),
    path('create/', views.create_post, name='create-post'),
    path('create-category/', views.CreateCategory.as_view(), name='create-category'),
    path('like-post/<int:id>', views.like_post, name='like-post'),
    path('edit/<int:pk>', views.edit_post, name='edit'),
]
