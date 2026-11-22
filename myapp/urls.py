from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('feed/', views.feed, name='feed'),
    path('report/', views.report, name='report'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('add/', views.add_contribution, name='add_contribution'),
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', views.custom_logout, name='logout'),
    path('profile/<str:username>/', views.profile, name='profile'),
    path('profile/', views.my_profile, name='my_profile'),
    path('coordinator/', views.coordinator, name='coordinator_panel'),
    path('confirm/<int:pk>/', views.approve, name='confirm'),
    path('reject/<int:pk>/', views.reject, name='reject'),
    path('contribute/', views.contribute, name='contribute'),
]