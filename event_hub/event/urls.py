from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name='event'),
    path('<slug:slug>', views.event_detail, name='event_detail'),
]