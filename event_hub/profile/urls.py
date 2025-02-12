from django.urls import path
from . import views

urlpatterns = [
    path('', views.not_auth_profile, name='not_auth_profile'),
    path('<slug:slug>', views.profile, name='profile'),
    path('<slug:slug>/update', views.profile_update, name='profile_update'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('register/', views.register_user, name='register'),
]