from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('event/', include('event.urls'), name='event'),
    path('user/', include('user.urls'), name='user'),
]