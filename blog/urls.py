from django.urls import path
from . import views

app_name = 'blog'
urlpatterns = [
    path('all/', views.show_all_posts, name='show-all-posts'),
    path('create/', views.create_post, name='create-post'),
    path('create-category/', views.CreateCategory.as_view(), name='create-category'),
    path('update-category/<int:pk>/', views.UpdateCategory.as_view(), name='update-category'),
    path('like-post/<int:id>', views.like_post, name='like-post'),
    path('edit/<int:pk>', views.edit_post, name='edit'),
    path('post/<int:pk>', views.ViewPost.as_view(), name='detail'),
    path('category/<slug:category_slug>/', views.FilterPostByCategory.as_view(), name='post-by-category'),
]
