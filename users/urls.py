from django.urls import path
from . import views

app_name = 'users'
urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path(
        'profile/edit/<int:pk>',
        views.EditUserProfile.as_view(),
        name='edit-profile'
    )
]
